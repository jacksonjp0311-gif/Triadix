from triadix.core.node import TriadicNode


def test_node_has_stable_identity_object():
    node = TriadicNode(label="test-node", base_url="http://127.0.0.1:9999")

    assert isinstance(node.identity.node_id, str)
    assert node.identity.label == "test-node"
    assert node.identity.base_url == "http://127.0.0.1:9999"


def test_peer_metadata_is_stored_as_records():
    node = TriadicNode("A")
    node.add_peer("peer-1", base_url="http://127.0.0.1:8002", label="node-b")

    peers = node.list_peers()

    assert len(peers) == 1
    assert peers[0]["peer_id"] == "peer-1"
    assert peers[0]["base_url"] == "http://127.0.0.1:8002"
    assert peers[0]["label"] == "node-b"


def test_status_snapshot_contains_identity_fields():
    node = TriadicNode(label="alpha", base_url="http://127.0.0.1:8001")
    snap = node.status_snapshot()

    assert "node_id" in snap
    assert "node_label" in snap
    assert "node_base_url" in snap
    assert snap["node_label"] == "alpha"
    assert snap["node_base_url"] == "http://127.0.0.1:8001"