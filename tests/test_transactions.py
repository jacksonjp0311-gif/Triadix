from triadix.core.transactions import sign_transaction, verify_transaction
from triadix.core.wallet import generate_wallet
from triadix.models.block import Transaction


def test_signed_transaction_verifies():
    private_key, public_key = generate_wallet()
    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.5,
        data="payment",
        public_key=public_key,
    )
    sign_transaction(tx, private_key)
    assert verify_transaction(tx) is True


def test_tampered_transaction_fails():
    private_key, public_key = generate_wallet()
    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.5,
        data="payment",
        public_key=public_key,
    )
    sign_transaction(tx, private_key)
    tx.amount = 99.9
    assert verify_transaction(tx) is False


def test_missing_signature_fails():
    _, public_key = generate_wallet()
    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.5,
        data="payment",
        public_key=public_key,
    )
    assert verify_transaction(tx) is False