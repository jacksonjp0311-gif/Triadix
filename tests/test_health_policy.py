from triadix.core.engine import TriadicEngine


def test_engine_health_stats_exist():
    engine = TriadicEngine()
    engine.run(blocks=20)
    stats = engine.coherence_stats()

    assert "p05" in stats
    assert "p50" in stats
    assert "p95" in stats
    assert 0.0 <= stats["fraction_ge_tau"] <= 1.0


def test_engine_health_check_returns_bool():
    engine = TriadicEngine()
    engine.run(blocks=20)
    assert isinstance(engine.is_healthy(), bool)