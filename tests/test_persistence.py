from pathlib import Path

from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def test_engine_save_and_load_roundtrip(tmp_path):
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=3.0,
        data="persist-test",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx)
    engine.build_block_from_mempool()

    while len(engine.chain) < 12:
        engine.add_block()

    path = tmp_path / "node_state.json"
    saved = engine.save_to_file(str(path))
    loaded = TriadicEngine.load_from_file(saved)

    assert Path(saved).exists()
    assert loaded.is_chain_valid() is True
    assert len(loaded.chain) == len(engine.chain)
    assert loaded.account_nonces == engine.account_nonces


def test_loaded_engine_preserves_mempool(tmp_path):
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    engine.create_genesis_block()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=1.0,
        data="mempool-persist",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)
    engine.submit_transaction(tx)

    path = tmp_path / "node_state_with_mempool.json"
    saved = engine.save_to_file(str(path))
    loaded = TriadicEngine.load_from_file(saved)

    assert len(loaded.mempool) == 1
    assert loaded.mempool[0].sender == "alice"