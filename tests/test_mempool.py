import pytest

from triadix.core.engine import TriadicEngine
from triadix.core.transactions import sign_transaction
from triadix.core.wallet import generate_wallet
from triadix.models.block import Transaction


def test_submit_transaction_to_mempool_and_build_block():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=3.0,
        data="mempool-payment",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx)

    assert len(engine.mempool) == 1

    engine.build_block_from_mempool()

    assert len(engine.mempool) == 0
    assert engine.account_nonces["alice"] == 1
    assert engine.is_chain_valid() is True


def test_replay_nonce_is_rejected():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx1 = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.0,
        data="first",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx1, private_key)

    tx2 = Transaction(
        sender="alice",
        receiver="carol",
        amount=1.0,
        data="replay",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx2, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx1)
    engine.build_block_from_mempool()

    with pytest.raises(ValueError):
        engine.submit_transaction(tx2)


def test_next_nonce_is_accepted():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx1 = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.0,
        data="first",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx1, private_key)

    tx2 = Transaction(
        sender="alice",
        receiver="carol",
        amount=2.0,
        data="second",
        public_key=public_key,
        nonce=1,
    )
    sign_transaction(tx2, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx1)
    engine.build_block_from_mempool()

    engine.submit_transaction(tx2)
    engine.build_block_from_mempool()

    assert engine.account_nonces["alice"] == 2
    assert engine.is_chain_valid() is True