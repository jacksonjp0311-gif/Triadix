from __future__ import annotations

from triadix.core.http_client import (
    get_status,
    get_receipt,
    set_identity,
    get_chain,
    list_peers,
    register_peer,
    submit_transaction,
    build_from_mempool,
    submit_and_build,
    seed_demo,
    sync_chain,
    save_state,
    load_state,
)
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def build_signed_transaction_payload(
    sender: str,
    receiver: str,
    amount: float,
    data: str,
    nonce: int,
) -> dict:
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        data=data,
        public_key=public_key,
        nonce=nonce,
    )
    sign_transaction(tx, private_key)
    return tx.to_dict()


def submit_and_build_signed_transaction(
    base_url: str,
    sender: str = "alice",
    receiver: str = "bob",
    amount: float = 10.0,
    data: str = "submit-and-build-payment",
    nonce: int = 0,
) -> dict:
    tx_payload = build_signed_transaction_payload(
        sender=sender,
        receiver=receiver,
        amount=amount,
        data=data,
        nonce=nonce,
    )
    return submit_and_build(base_url, tx_payload)