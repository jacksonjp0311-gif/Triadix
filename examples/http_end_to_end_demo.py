from triadix.core.orchestrator import (
    http_flow_snapshot,
    register_bidirectional_peers,
    seed_demo_chain,
    sync_node_from_peer_url,
)


def main():
    node_a = "http://127.0.0.1:8001"
    node_b = "http://127.0.0.1:8002"

    print("Triadix v2.1 HTTP demo")
    print("")

    before = http_flow_snapshot(node_a, node_b)
    print("Before:")
    print(before)
    print("")

    peer_result = register_bidirectional_peers(node_a, node_b)
    print("Peer registration:")
    print(peer_result)
    print("")

    seed_result = seed_demo_chain(node_a, blocks=12)
    print("Seed demo chain on node A:")
    print(seed_result)
    print("")

    sync_result = sync_node_from_peer_url(node_a, node_b)
    print("Sync node B from node A:")
    print(sync_result)
    print("")

    after = http_flow_snapshot(node_a, node_b)
    print("After:")
    print(after)


if __name__ == "__main__":
    main()