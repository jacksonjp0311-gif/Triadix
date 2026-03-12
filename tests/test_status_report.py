from triadix.core.engine import TriadicEngine
from triadix.core.node import TriadicNode


def test_health_not_evaluable_on_tiny_chain():
    engine = TriadicEngine()
    engine.create_genesis_block()
    report = engine.status_report()

    assert report["chain_length"] == 1
    assert report["health_evaluable"] is False
    assert report["healthy"] is None
    assert isinstance(report["health_note"], str)


def test_health_evaluable_on_demo_scale_chain():
    engine = TriadicEngine()
    engine.run(blocks=12)
    report = engine.status_report()

    assert report["chain_length"] == 12
    assert report["health_evaluable"] is True
    assert isinstance(report["healthy"], bool)


def test_node_snapshot_contains_unified_status_fields():
    node = TriadicNode("A")
    node.engine.run(blocks=12)
    snap = node.status_snapshot()

    assert "health_evaluable" in snap
    assert "health_note" in snap
    assert "tau" in snap
    assert "health_mode" in snap