from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def make_tx(sender: str, receiver: str, nonce: int):
    private_key, public_key = generate_wallet()
    tx = Transaction(
        sender=sender,
        receiver=receiver,
        amount=float(nonce + 1),
        data=f"tx-{receiver}",
        public_key=public_key,
        nonce=nonce,
    )
    sign_transaction(tx, private_key)
    return tx


def test_future_nonce_goes_to_waiting_queue():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx = make_tx("alice", "carol", 1)
    result = engine.submit_transaction(tx)

    assert result["queued"] is True
    assert len(engine.mempool) == 0
    assert len(engine.waiting_mempool) == 1


def test_gap_fill_promotes_waiting_transaction():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx_future = make_tx("alice", "carol", 1)
    tx_now = make_tx("alice", "bob", 0)

    engine.submit_transaction(tx_future)
    result = engine.submit_transaction(tx_now)

    assert result["queued"] is False
    assert len(engine.waiting_mempool) == 0
    assert len(engine.ordered_mempool()) == 2
    assert [tx.nonce for tx in engine.ordered_mempool()] == [0, 1]


def test_build_includes_promoted_transactions():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx_future = make_tx("alice", "carol", 1)
    tx_now = make_tx("alice", "bob", 0)

    engine.submit_transaction(tx_future)
    engine.submit_transaction(tx_now)

    block = engine.build_block_from_mempool(max_transactions=2)

    assert [tx.nonce for tx in block.transactions] == [0, 1]
    assert len(engine.waiting_mempool) == 0
    assert len(engine.mempool) == 0


def test_stale_nonce_still_rejected():
    engine = TriadicEngine()
    engine.create_genesis_block()

    tx0 = make_tx("alice", "bob", 0)
    engine.submit_transaction(tx0)
    engine.build_block_from_mempool()

    stale = make_tx("alice", "carol", 0)

    try:
        engine.submit_transaction(stale)
        assert False, "Expected stale nonce rejection"
    except ValueError as exc:
        assert "Replay/stale nonce" in str(exc)