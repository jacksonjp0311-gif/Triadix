from triadix.core.node import TriadicNode
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def main():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=5.0,
        data="policy-sync-demo-payment",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx, private_key)

    node_a.engine.create_genesis_block()
    node_a.engine.submit_transaction(tx)
    node_a.engine.build_block_from_mempool()

    while len(node_a.engine.chain) < 12:
        node_a.engine.add_block()

    node_b.engine.run(blocks=5)

    print("Before sync")
    print(node_a.status_snapshot())
    print(node_b.status_snapshot())

    result = node_b.sync_from_peer(node_a)

    print("")
    print("Sync result")
    print(result)

    print("")
    print("After sync")
    print(node_a.status_snapshot())
    print(node_b.status_snapshot())


if __name__ == "__main__":
    main()