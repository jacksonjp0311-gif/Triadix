from __future__ import annotations

import time
import uuid

from ..models.block import Transaction
from ..models.node import NodeIdentity, PeerRecord
from .engine import TriadicEngine
from .policy import LongestValidChainPolicy, SyncResult


class TriadicNode:
    def __init__(self, node_id: str | None = None, policy=None, label: str = "", base_url: str = ""):
        actual_id = node_id or str(uuid.uuid4())
        self.identity = NodeIdentity(
            node_id=actual_id,
            label=label,
            base_url=base_url,
            created_at=time.time(),
        )
        self.engine = TriadicEngine()
        self.peers: dict[str, PeerRecord] = {}
        self.policy = policy or LongestValidChainPolicy()

    @property
    def node_id(self) -> str:
        return self.identity.node_id

    def set_identity_metadata(self, label: str | None = None, base_url: str | None = None) -> None:
        if label is not None:
            self.identity.label = label
        if base_url is not None:
            self.identity.base_url = base_url

    def add_peer(self, peer_id: str, base_url: str = "", label: str = "") -> None:
        existing = self.peers.get(peer_id)
        added_at = existing.added_at if existing else time.time()
        self.peers[peer_id] = PeerRecord(
            peer_id=peer_id,
            base_url=base_url,
            label=label,
            added_at=added_at,
        )

    def list_peers(self) -> list[dict]:
        return [peer.to_dict() for peer in sorted(self.peers.values(), key=lambda p: p.peer_id)]

    def export_chain(self) -> list[dict]:
        return [b.to_dict() for b in self.engine.chain]

    def export_node_state(self) -> dict:
        return {
            "identity": self.identity.to_dict(),
            "peers": self.list_peers(),
            "engine": self.engine.export_state(),
        }

    def load_node_state(self, data: dict) -> None:
        identity = data.get("identity", {})
        self.identity = NodeIdentity(
            node_id=identity.get("node_id", self.identity.node_id),
            label=identity.get("label", ""),
            base_url=identity.get("base_url", ""),
            created_at=identity.get("created_at", time.time()),
        )

        self.peers = {}
        for peer in data.get("peers", []):
            record = PeerRecord(
                peer_id=peer["peer_id"],
                base_url=peer.get("base_url", ""),
                label=peer.get("label", ""),
                added_at=peer.get("added_at", 0.0),
            )
            self.peers[record.peer_id] = record

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
        report = self.engine.status_report()
        return {
            "node_id": self.identity.node_id,
            "node_label": self.identity.label,
            "node_base_url": self.identity.base_url,
            "node_created_at": self.identity.created_at,
            "policy": getattr(self.policy, "name", self.policy.__class__.__name__),
            "peer_count": len(self.peers),
            "peers": self.list_peers(),
            **report,
        }