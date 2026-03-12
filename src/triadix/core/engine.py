import json
import math
import time
from pathlib import Path

from ..models.block import Block, Transaction
from ..utils.config import get_config
from ..visualization.plots import generate_plots
from .hashes import triadic_hash_cycle
from .metrics import compute_coherence_metrics
from .transactions import verify_transaction

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
        self.mempool: list[Transaction] = []
        self.account_nonces: dict[str, int] = {}

    def canonical_payload(self, transactions: list[Transaction]) -> bytes:
        payload_obj = [tx.to_dict() for tx in transactions]
        return json.dumps(
            payload_obj,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

    def current_expected_nonce(self, sender: str) -> int:
        return self.account_nonces.get(sender, 0)

    def pending_expected_nonce(self, sender: str) -> int:
        expected = self.current_expected_nonce(sender)
        sender_pending = sorted(
            [tx for tx in self.mempool if tx.sender == sender],
            key=lambda tx: tx.nonce
        )
        for tx in sender_pending:
            if tx.nonce == expected:
                expected += 1
            else:
                break
        return expected

    def validate_transactions(self, transactions: list[Transaction], use_mempool_view: bool = False) -> None:
        seen_sender_nonces = set()
        expected_map: dict[str, int] = {}

        for tx in transactions:
            if tx.sender == "genesis" and tx.receiver == "system":
                continue
            if tx.sender == "system" and tx.receiver == "system":
                continue

            if not verify_transaction(tx):
                raise ValueError("Invalid transaction signature detected.")

            if tx.sender not in expected_map:
                if use_mempool_view:
                    expected_map[tx.sender] = self.pending_expected_nonce(tx.sender)
                else:
                    expected_map[tx.sender] = self.current_expected_nonce(tx.sender)

            expected_nonce = expected_map[tx.sender]
            key = (tx.sender, tx.nonce)

            if key in seen_sender_nonces:
                raise ValueError("Duplicate sender nonce in transaction set.")
            seen_sender_nonces.add(key)

            if tx.nonce != expected_nonce:
                raise ValueError(
                    f"Invalid nonce for sender {tx.sender}: got {tx.nonce}, expected {expected_nonce}."
                )

            expected_map[tx.sender] = expected_nonce + 1

    def apply_transactions(self, transactions: list[Transaction]) -> None:
        for tx in transactions:
            if tx.sender == "genesis" and tx.receiver == "system":
                continue
            if tx.sender == "system" and tx.receiver == "system":
                continue
            self.account_nonces[tx.sender] = tx.nonce + 1

    def submit_transaction(self, tx: Transaction) -> None:
        self.validate_transactions([tx], use_mempool_view=True)
        self.mempool.append(tx)

    def build_block_from_mempool(self, max_transactions: int | None = None) -> Block:
        if not self.chain:
            self.create_genesis_block()

        if not self.mempool:
            return self.add_block()

        if max_transactions is None:
            selected = list(self.mempool)
            self.mempool.clear()
        else:
            selected = self.mempool[:max_transactions]
            self.mempool = self.mempool[max_transactions:]

        return self._append_block(selected)

    def _append_block(self, transactions: list[Transaction]) -> Block:
        self.validate_transactions(transactions, use_mempool_view=False)
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
        self.apply_transactions(transactions)
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
        replay_nonces: dict[str, int] = {}

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

            seen_sender_nonces = set()
            for tx in block.transactions:
                if tx.sender == "genesis" and tx.receiver == "system":
                    continue
                if tx.sender == "system" and tx.receiver == "system":
                    continue

                if not verify_transaction(tx):
                    return False

                expected_nonce = replay_nonces.get(tx.sender, 0)
                key = (tx.sender, tx.nonce)

                if key in seen_sender_nonces:
                    return False
                seen_sender_nonces.add(key)

                if tx.nonce != expected_nonce:
                    return False

                replay_nonces[tx.sender] = tx.nonce + 1

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

    def is_health_evaluable(self) -> bool:
        return len(self.chain) >= self.config.min_health_blocks

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

        return stats["p05"] >= self.config.tau

    def status_report(self) -> dict:
        health_evaluable = self.is_health_evaluable()
        return {
            "chain_length": len(self.chain),
            "valid": self.is_chain_valid(),
            "healthy": self.is_healthy() if health_evaluable else None,
            "health_evaluable": health_evaluable,
            "health_note": None if health_evaluable else (
                f"Health policy is calibrated for chains with at least {self.config.min_health_blocks} blocks."
            ),
            "tau": self.config.tau,
            "health_mode": self.config.health_mode,
            "mempool_size": len(self.mempool),
            "account_nonces": self.account_nonces,
            "coherence_stats": self.coherence_stats(),
        }

    def export_state(self) -> dict:
        return {
            "hE": self.hE.hex(),
            "hI": self.hI.hex(),
            "hC": self.hC.hex(),
            "chain": [b.to_dict() for b in self.chain],
            "mempool": [tx.to_dict() for tx in self.mempool],
            "account_nonces": self.account_nonces,
            "status": self.status_report(),
        }

    def save_to_file(self, filepath: str | None = None) -> str:
        target = filepath or self.config.state_file
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.export_state(), f, indent=2)

        return str(path)

    @classmethod
    def load_from_file(cls, filepath: str) -> "TriadicEngine":
        path = Path(filepath)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        engine = cls()
        engine.chain = []
        engine.mempool = [Transaction(**tx) for tx in data.get("mempool", [])]
        engine.account_nonces = {
            str(k): int(v) for k, v in data.get("account_nonces", {}).items()
        }

        for block_data in data.get("chain", []):
            txs = [Transaction(**tx) for tx in block_data["transactions"]]
            block = Block(
                index=block_data["index"],
                previous_hE=block_data["previous"]["hE"],
                previous_hI=block_data["previous"]["hI"],
                previous_hC=block_data["previous"]["hC"],
                transactions=txs,
                timestamp=block_data["timestamp"],
                hE=block_data["hE"],
                hI=block_data["hI"],
                hC=block_data["hC"],
                E=block_data["metrics"]["E"],
                I=block_data["metrics"]["I"],
                dphi=block_data["metrics"]["dphi"],
                C=block_data["metrics"]["C"],
            )
            engine.chain.append(block)

        engine.hE = bytes.fromhex(data["hE"]) if data.get("hE") else ZERO32
        engine.hI = bytes.fromhex(data["hI"]) if data.get("hI") else ZERO32
        engine.hC = bytes.fromhex(data["hC"]) if data.get("hC") else ZERO32

        return engine

    def save_state(self) -> None:
        state_dir = Path(self.config.run_root) / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        with open(state_dir / "ledger_state.json", "w", encoding="utf-8") as f:
            json.dump(
                self.status_report() | {
                    "chain": [b.to_dict() for b in self.chain]
                },
                f,
                indent=2
            )