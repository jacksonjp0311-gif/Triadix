from triadix.core.orchestrator import build_signed_transaction_payload


def test_build_signed_transaction_payload_contains_signature_and_public_key():
    payload = build_signed_transaction_payload(
        sender="alice",
        receiver="bob",
        amount=5.0,
        data="helper-test",
        nonce=0,
    )

    assert payload["sender"] == "alice"
    assert payload["receiver"] == "bob"
    assert payload["amount"] == 5.0
    assert payload["nonce"] == 0
    assert isinstance(payload["public_key"], str)
    assert isinstance(payload["signature"], str)
    assert len(payload["public_key"]) > 0
    assert len(payload["signature"]) > 0