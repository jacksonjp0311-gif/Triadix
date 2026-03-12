from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction, compute_tx_id
from triadix.models.block import Transaction


def test_tx_id_is_deterministic():
    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.0,
        data="x",
        public_key="pub",
        nonce=0,
    )
    a = compute_tx_id(tx)
    b = compute_tx_id(tx)
    assert a == b


def test_receipt_created_after_block_inclusion():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=2.0,
        data="receipt-test",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx)
    engine.build_block_from_mempool()

    receipt = engine.get_receipt(tx.tx_id)
    assert receipt is not None
    assert receipt.tx_id == tx.tx_id
    assert receipt.included is True
    assert receipt.sender == "alice"


def test_receipts_persist_roundtrip(tmp_path):
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=3.0,
        data="persist-receipt",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx)
    engine.build_block_from_mempool()

    path = tmp_path / "receipt_state.json"
    saved = engine.save_to_file(str(path))
    loaded = TriadicEngine.load_from_file(saved)

    receipt = loaded.get_receipt(tx.tx_id)
    assert receipt is not None
    assert receipt.tx_id == tx.tx_id