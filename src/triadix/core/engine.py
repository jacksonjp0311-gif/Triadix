import json
import math
import time
from pathlib import Path

from ..models.block import Block, Transaction
from ..utils.config import get_config
from ..visualization.plots import generate_plots
from .hashes import triadic_hash_cycle
from .metrics import compute_coherence_metrics

ZERO32 = b"\x00" * 32


def percentile(values: list[float], p: float) -> float | None:
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    k = (len(values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] * (c - k) + values[c] * (k - f)


class TriadicEngine:
    def __init__(self):
        self.config = get_config()
        self.chain: list[Block] = []
        self.hE = ZERO32
        self.hI = ZERO32
        self.hC = ZERO32

    def canonical_payload(self, transactions: list[Transaction]) -> bytes:
        payload_obj = [tx.to_dict() for tx in transactions]
        return json.dumps(
            payload_obj,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

    def _append_block(self, transactions: list[Transaction]) -> Block:
        payload = self.canonical_payload(transactions)

        prev_hE = self.hE
        prev_hI = self.hI
        prev_hC = self.hC

        self.hE, self.hI, self.hC = triadic_hash_cycle(
            self.hE, self.hI, self.hC, payload
        )

        En, In, dphi, Cn = compute_coherence_metrics(
            self.hE, self.hI, self.hC
        )

        block = Block(
            index=len(self.chain),
            previous_hE=prev_hE.hex(),
            previous_hI=prev_hI.hex(),
            previous_hC=prev_hC.hex(),
            transactions=transactions,
            timestamp=time.time(),
            hE=self.hE.hex(),
            hI=self.hI.hex(),
            hC=self.hC.hex(),
            E=En,
            I=In,
            dphi=dphi,
            C=Cn
        )
        self.chain.append(block)
        return block

    def create_genesis_block(self) -> Block:
        if self.chain:
            return self.chain[0]

        genesis_txs = [
            Transaction(
                sender="genesis",
                receiver="system",
                amount=0.0,
                data="triadix-genesis"
            )
        ]
        return self._append_block(genesis_txs)

    def add_block(self, transactions: list[Transaction] | None = None) -> Block:
        if not self.chain:
            self.create_genesis_block()

        if transactions is None:
            transactions = [
                Transaction(
                    sender="system",
                    receiver="system",
                    amount=0.0,
                    data=f"block-{len(self.chain)}"
                )
            ]

        return self._append_block(transactions)

    def run(self, blocks: int | None = None):
        blocks = blocks or self.config.blocks

        if not self.chain:
            self.create_genesis_block()

        while len(self.chain) < blocks:
            self.add_block()

        self.save_state()
        generate_plots(self.chain, self.config.run_root)
        return self.chain

    def is_chain_valid(self, tolerance: float = 1e-12) -> bool:
        hE = ZERO32
        hI = ZERO32
        hC = ZERO32

        for i, block in enumerate(self.chain):
            if i == 0:
                expected_prev_hE = ZERO32.hex()
                expected_prev_hI = ZERO32.hex()
                expected_prev_hC = ZERO32.hex()
            else:
                expected_prev_hE = self.chain[i - 1].hE
                expected_prev_hI = self.chain[i - 1].hI
                expected_prev_hC = self.chain[i - 1].hC

            if block.previous_hE != expected_prev_hE:
                return False
            if block.previous_hI != expected_prev_hI:
                return False
            if block.previous_hC != expected_prev_hC:
                return False

            payload = self.canonical_payload(block.transactions)
            hE, hI, hC = triadic_hash_cycle(hE, hI, hC, payload)

            if block.hE != hE.hex():
                return False
            if block.hI != hI.hex():
                return False
            if block.hC != hC.hex():
                return False

            En, In, dphi, Cn = compute_coherence_metrics(hE, hI, hC)

            if not math.isclose(block.E, En, rel_tol=0.0, abs_tol=tolerance):
                return False
            if not math.isclose(block.I, In, rel_tol=0.0, abs_tol=tolerance):
                return False
            if not math.isclose(block.dphi, dphi, rel_tol=0.0, abs_tol=tolerance):
                return False
            if not math.isclose(block.C, Cn, rel_tol=0.0, abs_tol=tolerance):
                return False

        return True

    def coherence_stats(self) -> dict:
        cvals = [b.C for b in self.chain]
        if not cvals:
            return {}

        count_ge_tau = sum(1 for x in cvals if x >= self.config.tau)
        frac_ge_tau = count_ge_tau / len(cvals)

        return {
            "min": min(cvals),
            "max": max(cvals),
            "mean": sum(cvals) / len(cvals),
            "p05": percentile(cvals, 0.05),
            "p25": percentile(cvals, 0.25),
            "p50": percentile(cvals, 0.50),
            "p75": percentile(cvals, 0.75),
            "p95": percentile(cvals, 0.95),
            "final": cvals[-1],
            "count_ge_tau": count_ge_tau,
            "fraction_ge_tau": frac_ge_tau,
        }

    def is_healthy(self) -> bool:
        stats = self.coherence_stats()
        if not stats:
            return False

        mode = (self.config.health_mode or "p05").lower()

        if mode == "all":
            return stats["fraction_ge_tau"] == 1.0
        if mode == "fraction":
            return stats["fraction_ge_tau"] >= self.config.health_min_fraction
        if mode == "p25":
            return stats["p25"] >= self.config.tau
        if mode == "p50":
            return stats["p50"] >= self.config.tau
        if mode == "p95":
            return stats["p95"] >= self.config.tau

        # default p05
        return stats["p05"] >= self.config.tau

    def save_state(self) -> None:
        state_dir = Path(self.config.run_root) / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        with open(state_dir / "ledger_state.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "blocks": len(self.chain),
                    "tau": self.config.tau,
                    "health_mode": self.config.health_mode,
                    "health_min_fraction": self.config.health_min_fraction,
                    "valid": self.is_chain_valid(),
                    "healthy": self.is_healthy(),
                    "coherence_stats": self.coherence_stats(),
                    "chain": [b.to_dict() for b in self.chain]
                },
                f,
                indent=2
            )