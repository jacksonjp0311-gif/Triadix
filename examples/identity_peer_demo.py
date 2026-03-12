from triadix.core.orchestrator import (
    set_node_identities,
    register_bidirectional_peers,
    seed_demo_chain,
    http_flow_snapshot,
)


def main():
    node_a = "http://127.0.0.1:8001"
    node_b = "http://127.0.0.1:8002"

    print("Triadix v2.3 identity + peer metadata demo")
    print("")

    identities = set_node_identities(node_a, node_b)
    print("Identity update:")
    print(identities)
    print("")

    peers = register_bidirectional_peers(node_a, node_b)
    print("Peer metadata registration:")
    print(peers)
    print("")

    seed = seed_demo_chain(node_a, blocks=12)
    print("Seed node A:")
    print(seed)
    print("")

    snapshot = http_flow_snapshot(node_a, node_b)
    print("Snapshot:")
    print(snapshot)


if __name__ == "__main__":
    main()