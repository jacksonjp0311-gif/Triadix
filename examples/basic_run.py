from triadix.core.engine import TriadicEngine


def main():
    engine = TriadicEngine()
    engine.run(blocks=12)
    print(f"Generated {len(engine.chain)} blocks.")
    print(f"Valid: {engine.is_chain_valid()}")


if __name__ == "__main__":
    main()