import base64
import hashlib
import json
from cryptography.exceptions import InvalidSignature

from ..models.block import Transaction
from .wallet import load_private_key, load_public_key


def transaction_signing_payload(tx: Transaction) -> bytes:
    payload = {
        "sender": tx.sender,
        "receiver": tx.receiver,
        "amount": tx.amount,
        "data": tx.data,
        "public_key": tx.public_key,
        "nonce": tx.nonce,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_tx_id(tx: Transaction) -> str:
    return hashlib.sha256(transaction_signing_payload(tx)).hexdigest()


def sign_transaction(tx: Transaction, private_key_b64: str) -> Transaction:
    private_key = load_private_key(private_key_b64)
    signature = private_key.sign(transaction_signing_payload(tx))
    tx.signature = base64.b64encode(signature).decode("utf-8")
    tx.tx_id = compute_tx_id(tx)
    return tx


def verify_transaction(tx: Transaction) -> bool:
    if not tx.public_key or not tx.signature:
        return False
    try:
        public_key = load_public_key(tx.public_key)
        signature = base64.b64decode(tx.signature.encode("utf-8"))
        public_key.verify(signature, transaction_signing_payload(tx))
        expected_tx_id = compute_tx_id(tx)
        if tx.tx_id and tx.tx_id != expected_tx_id:
            return False
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False