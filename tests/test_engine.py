from triadix.core.engine import TriadicEngine
from triadix.models.block import Transaction
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction


def test_engine_run_produces_valid_chain():
    engine = TriadicEngine()
    engine.run(blocks=5)
    assert len(engine.chain) == 5
    assert engine.is_chain_valid() is True


def test_tamper_detection_breaks_validation():
    engine = TriadicEngine()
    engine.run(blocks=5)
    engine.chain[2].hE = "deadbeef"
    assert engine.is_chain_valid() is False


def test_custom_transaction_block():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.25,
        data="test",
        public_key=public_key,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.add_block([tx])

    assert engine.is_chain_valid() is True