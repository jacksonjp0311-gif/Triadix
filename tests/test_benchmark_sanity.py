from triadix.core.engine import TriadicEngine


def test_engine_can_run_10_blocks():
    engine = TriadicEngine()
    engine.run(blocks=10)
    assert len(engine.chain) == 10
    assert engine.is_chain_valid() is True