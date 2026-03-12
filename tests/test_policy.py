from triadix.core.node import TriadicNode


def test_sync_result_adopts_longer_valid_chain():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=9)
    node_b.engine.run(blocks=5)

    result = node_b.sync_from_peer(node_a)

    assert result.adopted is True
    assert result.reason == "candidate_longer_valid"
    assert len(node_b.engine.chain) == 9
    assert node_b.engine.is_chain_valid() is True


def test_sync_result_rejects_same_length_chain():
    node_a = TriadicNode("A")
    node_b = TriadicNode("B")

    node_a.engine.run(blocks=7)
    node_b.engine.run(blocks=7)

    result = node_b.sync_from_peer(node_a)

    assert result.adopted is False
    assert result.reason == "same_length_keep_local"
    assert len(node_b.engine.chain) == 7


def test_status_snapshot_has_expected_fields():
    node = TriadicNode("A")
    node.engine.run(blocks=4)

    snap = node.status_snapshot()

    assert "node_id" in snap
    assert "policy" in snap
    assert "chain_length" in snap
    assert "valid" in snap
    assert "healthy" in snap
    assert "mempool_size" in snap
    assert "peer_count" in snap