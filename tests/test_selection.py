from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def make_tx(receiver: str, nonce: int):
    private_key, public_key = generate_wallet()
    tx = Transaction(
        sender="alice",
        receiver=receiver,
        amount=float(nonce + 1),
        data=f"tx-{receiver}",
        public_key=public_key,
        nonce=nonce,
    )
    sign_transaction(tx, private_key)
    return tx


def test_deterministic_mempool_ordering():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx1 = make_tx("bob", 0)
    tx2 = make_tx("carol", 1)
    tx3 = make_tx("dave", 2)

    engine.submit_transaction(tx1)
    engine.submit_transaction(tx2)
    engine.submit_transaction(tx3)

    ordered = engine.ordered_mempool()
    assert [tx.nonce for tx in ordered] == [0, 1, 2]
    assert [tx.receiver for tx in ordered] == ["bob", "carol", "dave"]


def test_build_respects_max_transactions_limit():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx1 = make_tx("bob", 0)
    tx2 = make_tx("carol", 1)
    tx3 = make_tx("dave", 2)

    engine.submit_transaction(tx1)
    engine.submit_transaction(tx2)
    engine.submit_transaction(tx3)

    block = engine.build_block_from_mempool(max_transactions=2)

    assert len(block.transactions) == 2
    assert len(engine.mempool) == 1
    assert engine.last_selection_report["selected_count"] == 2
    assert engine.last_selection_report["remaining_count"] == 1
    assert [tx.nonce for tx in block.transactions] == [0, 1]


def test_selection_report_contains_selected_ids():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx1 = make_tx("bob", 0)
    tx2 = make_tx("carol", 1)

    engine.submit_transaction(tx1)
    engine.submit_transaction(tx2)
    engine.build_block_from_mempool(max_transactions=1)

    report = engine.last_selection_report
    assert "selected_ids" in report
    assert len(report["selected_ids"]) == 1