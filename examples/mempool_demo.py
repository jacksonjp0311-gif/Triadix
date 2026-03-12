from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def main():
    engine = TriadicEngine()
    private_key, public_key = generate_wallet()

    tx1 = Transaction(
        sender="alice",
        receiver="bob",
        amount=2.5,
        data="mempool-demo-1",
        public_key=public_key,
        nonce=0,
    )
    sign_transaction(tx1, private_key)

    tx2 = Transaction(
        sender="alice",
        receiver="carol",
        amount=1.0,
        data="mempool-demo-2",
        public_key=public_key,
        nonce=1,
    )
    sign_transaction(tx2, private_key)

    engine.create_genesis_block()
    engine.submit_transaction(tx1)
    engine.submit_transaction(tx2)

    print("Before block build")
    print(f"Mempool size: {len(engine.mempool)}")

    engine.build_block_from_mempool()

    while len(engine.chain) < 12:
        engine.add_block()

    print("Mempool + nonce demo")
    print(f"Blocks: {len(engine.chain)}")
    print(f"Mempool size: {len(engine.mempool)}")
    print(f"Account nonces: {engine.account_nonces}")
    print(f"Valid: {engine.is_chain_valid()}")
    print(f"Healthy: {engine.is_healthy()}")
    print(f"Stats: {engine.coherence_stats()}")


if __name__ == "__main__":
    main()