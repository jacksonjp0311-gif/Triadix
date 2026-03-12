from triadix.core.engine import TriadicEngine
from triadix.core.node import TriadicNode


def test_checkpoint_map_exists_for_built_chain():
    engine = TriadicEngine()
    engine.run(blocks=12)

    checkpoints = engine.checkpoint_map()

    assert isinstance(checkpoints, dict)
    assert "0" in checkpoints
    assert "5" in checkpoints
    assert "10" in checkpoints or "11" in checkpoints


def test_checkpoint_verification_passes_for_matching_chain():
    engine = TriadicEngine()
    engine.run(blocks=12)

    checkpoints = engine.checkpoint_map()

    assert engine.verify_checkpoint_map(checkpoints) is True


def test_checkpoint_verification_fails_for_mismatch():
    engine = TriadicEngine()
    engine.run(blocks=12)

    checkpoints = engine.checkpoint_map()
    first_key = sorted(checkpoints.keys())[0]
    checkpoints[first_key] = "deadbeef"

    assert engine.verify_checkpoint_map(checkpoints) is False


def test_sync_rejects_candidate_with_bad_checkpoints():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=12)
    exported = node_a.export_chain()
    bad_checkpoints = node_a.engine.checkpoint_map()
    first_key = sorted(bad_checkpoints.keys())[0]
    bad_checkpoints[first_key] = "deadbeef"

    result = node_b.try_sync_from_chain_data(exported, checkpoint_map=bad_checkpoints)

    assert result.adopted is False
    assert result.reason == "candidate_checkpoint_mismatch"
    assert result.checkpoint_verified is False