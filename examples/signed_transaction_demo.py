from triadix.core.engine import TriadicEngine
from triadix.core.wallet import generate_wallet
from triadix.core.transactions import sign_transaction
from triadix.models.block import Transaction


def main():
    engine = TriadicEngine()

    private_key, public_key = generate_wallet()

    tx = Transaction(
        sender="alice",
        receiver="bob",
        amount=2.5,
        data="signed-demo-payment",
        public_key=public_key,
    )
    sign_transaction(tx, private_key)

    engine.create_genesis_block()
    engine.add_block([tx])

    while len(engine.chain) < 12:
        engine.add_block()

    print("Signed transaction demo")
    print(f"Blocks: {len(engine.chain)}")
    print(f"Valid: {engine.is_chain_valid()}")
    print(f"Healthy: {engine.is_healthy()}")
    print(f"Stats: {engine.coherence_stats()}")


if __name__ == "__main__":
    main()