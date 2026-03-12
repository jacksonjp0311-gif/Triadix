from triadix.core.orchestrator import (
    seed_node_with_signed_transaction,
    sync_node_from_peer_url,
    http_flow_snapshot,
)


def main():
    node_a = "http://127.0.0.1:8001"
    node_b = "http://127.0.0.1:8002"

    print("Triadix HTTP end-to-end demo")
    print("Expected running nodes:")
    print("  node A -> 127.0.0.1:8001")
    print("  node B -> 127.0.0.1:8002")
    print("")

    before = http_flow_snapshot(node_a, node_b)
    print("Before:")
    print(before)
    print("")

    seed_result = seed_node_with_signed_transaction(
        node_a,
        sender="alice",
        receiver="bob",
        amount=11.0,
        data="v1.9-http-demo",
        nonce=0,
    )
    print("Seed result:")
    print(seed_result)
    print("")

    sync_result = sync_node_from_peer_url(node_a, node_b)
    print("Sync result:")
    print(sync_result)
    print("")

    after = http_flow_snapshot(node_a, node_b)
    print("After:")
    print(after)


if __name__ == "__main__":
    main()