from triadix.core.orchestrator import (
    build_signed_transaction_payload,
    submit_and_build_signed_transaction,
)


def test_signed_payload_builder_still_returns_signature():
    payload = build_signed_transaction_payload(
        sender="alice",
        receiver="bob",
        amount=2.0,
        data="v2.1-test",
        nonce=0,
    )

    assert isinstance(payload["public_key"], str)
    assert isinstance(payload["signature"], str)
    assert payload["nonce"] == 0


def test_submit_and_build_helper_exists():
    assert callable(submit_and_build_signed_transaction)