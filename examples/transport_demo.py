from triadix.core.node import TriadicNode
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def main():
    node_a = TriadicNode("node-a")
    node_b = TriadicNode("node-b")

    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=9.0,
        data="transport-demo",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    node_a.engine.create_genesis_block()
    node_a.engine.submit_transaction(tx)
    node_a.engine.build_block_from_mempool()

    while len(node_a.engine.chain) < 10:
        node_a.engine.add_block()

    print("Transport demo")
    print(f"Node A status before export: {node_a.status_snapshot()}")
    print(f"Node B status before sync:   {node_b.status_snapshot()}")

    result = node_b.try_sync_from_chain_data(node_a.export_chain())

    print("")
    print(f"Sync result: {result}")
    print(f"Node B status after sync:    {node_b.status_snapshot()}")


if __name__ == "__main__":
    main()