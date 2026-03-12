import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_wallet() -> tuple[str, str]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return (
        base64.b64encode(private_bytes).decode("utf-8"),
        base64.b64encode(public_bytes).decode("utf-8"),
    )


def load_private_key(private_key_b64: str) -> Ed25519PrivateKey:
    key_bytes = base64.b64decode(private_key_b64.encode("utf-8"))
    return Ed25519PrivateKey.from_private_bytes(key_bytes)


def load_public_key(public_key_b64: str) -> Ed25519PublicKey:
    key_bytes = base64.b64decode(public_key_b64.encode("utf-8"))
    return Ed25519PublicKey.from_public_bytes(key_bytes)