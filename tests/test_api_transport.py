from triadix.core.node import TriadicNode
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def test_exported_chain_can_sync_into_fresh_node():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=6)
    result = node_b.try_sync_from_chain_data(node_a.export_chain())

    assert result.adopted is True
    assert node_b.engine.is_chain_valid() is True
    assert len(node_b.engine.chain) == 6


def test_signed_transaction_can_enter_mempool_flow():
    node = TriadicNode("api-test")
    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=7.0,
        data="api-flow",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    node.engine.create_genesis_block()
    node.engine.submit_transaction(tx)
    block = node.engine.build_block_from_mempool()

    assert block.index >= 1
    assert node.engine.is_chain_valid() is True