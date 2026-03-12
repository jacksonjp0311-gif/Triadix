from triadix.core.node import TriadicNode
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def test_node_adopts_longer_valid_chain():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=8)
    node_b.engine.run(blocks=5)

    result = node_b.sync_from_peer(node_a)

    assert result.adopted is True
    assert result.reason == "candidate_longer_valid"
    assert len(node_b.engine.chain) == len(node_a.engine.chain)
    assert node_b.engine.is_chain_valid() is True


def test_node_rejects_shorter_chain():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=5)
    node_b.engine.run(blocks=8)

    result = node_b.sync_from_peer(node_a)

    assert result.adopted is False
    assert result.reason == "candidate_shorter"
    assert len(node_b.engine.chain) == 8


def test_node_sync_with_signed_transaction_chain():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=4.0,
        data="node-sync-payment",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    node_a.engine.create_genesis_block()
    node_a.engine.submit_transaction(tx)
    node_a.engine.build_block_from_mempool()

    while len(node_a.engine.chain) < 10:
        node_a.engine.add_block()

    result = node_b.sync_from_peer(node_a)

    assert result.adopted is True
    assert result.reason == "candidate_longer_valid"
    assert len(node_b.engine.chain) == len(node_a.engine.chain)
    assert node_b.engine.is_chain_valid() is True