import pytest

from triadix.core.engine import TriadicEngine
from triadix.core.transactions import sign_transaction
from triadix.core.wallet import generate_wallet
from triadix.models.block import Transaction


def test_signed_transaction_is_accepted_into_block():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=2.0,
        data="signed-payment",
        public_key=public_key,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.add_block([tx])

    assert engine.is_chain_valid() is True


def test_unsigned_transaction_is_rejected():
    engine = TriadicEngine()
    _, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=2.0,
        data="unsigned-payment",
        public_key=public_key,
    )

    engine.create_genesis_block()

    with pytest.raises(ValueError):
        engine.add_block([tx])