from __future__ import annotations

from ..models.block import Transaction
from .engine import TriadicEngine
from .policy import LongestValidChainPolicy, SyncResult


class TriadicNode:
    def __init__(self, node_id: str, policy=None):
        self.node_id = node_id
        self.engine = TriadicEngine()
        self.peers: set[str] = set()
        self.policy = policy or LongestValidChainPolicy()

    def add_peer(self, peer_id: str) -> None:
        self.peers.add(peer_id)

    def export_chain(self) -> list[dict]:
        return [b.to_dict() for b in self.engine.chain]

    def rebuild_engine_from_chain_data(self, chain_data: list[dict]) -> TriadicEngine:
        rebuilt = TriadicEngine()

        for i, block_data in enumerate(chain_data):
            txs = [
                Transaction(**tx_dict)
                for tx_dict in block_data["transactions"]
            ]

            if i == 0:
                rebuilt.create_genesis_block()
                continue

            if txs and all(
                tx.sender == "system" and tx.receiver == "system"
                for tx in txs
            ):
                rebuilt.add_block()
            else:
                rebuilt.add_block(txs)

        return rebuilt

    def try_sync_from_chain_data(self, chain_data: list[dict]) -> SyncResult:
        candidate = self.rebuild_engine_from_chain_data(chain_data)
        result = self.policy.choose(self.engine, candidate)

        if result.adopted:
            self.engine = candidate

        return result

    def sync_from_peer(self, peer: "TriadicNode") -> SyncResult:
        return self.try_sync_from_chain_data(peer.export_chain())

    def status_snapshot(self) -> dict:
        return {
            "node_id": self.node_id,
            "policy": getattr(self.policy, "name", self.policy.__class__.__name__),
            "chain_length": len(self.engine.chain),
            "valid": self.engine.is_chain_valid(),
            "healthy": self.engine.is_healthy(),
            "mempool_size": len(self.engine.mempool),
            "peer_count": len(self.peers),
        }