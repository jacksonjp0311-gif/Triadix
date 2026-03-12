from __future__ import annotations

from triadix.core.http_client import (
    get_status,
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


def seed_node_with_signed_transaction(
    base_url: str,
    sender: str = "alice",
    receiver: str = "bob",
    amount: float = 10.0,
    data: str = "http-seeded-payment",
    nonce: int = 0,
) -> dict:
    tx_payload = build_signed_transaction_payload(
        sender=sender,
        receiver=receiver,
        amount=amount,
        data=data,
        nonce=nonce,
    )
    submit_result = submit_transaction(base_url, tx_payload)
    build_result = build_from_mempool(base_url)
    return {
        "submit_result": submit_result,
        "build_result": build_result,
    }


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


def sync_node_from_peer_url(source_url: str, target_url: str) -> dict:
    chain_payload = get_chain(source_url)
    return sync_chain(target_url, chain_payload["chain"])


def http_flow_snapshot(source_url: str, target_url: str) -> dict:
    return {
        "source_status": get_status(source_url),
        "target_status": get_status(target_url),
        "source_peers": list_peers(source_url),
        "target_peers": list_peers(target_url),
    }


def register_bidirectional_peers(node_a_url: str, node_b_url: str) -> dict:
    a = register_peer(node_a_url, node_b_url)
    b = register_peer(node_b_url, node_a_url)
    return {
        "node_a_peer_result": a,
        "node_b_peer_result": b,
    }


def seed_demo_chain(base_url: str, blocks: int = 12) -> dict:
    return seed_demo(base_url, blocks=blocks)


def persist_node_state(base_url: str, filepath: str | None = None) -> dict:
    return save_state(base_url, filepath)


def restore_node_state(base_url: str, filepath: str) -> dict:
    return load_state(base_url, filepath)