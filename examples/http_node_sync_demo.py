import time

from triadix.core.http_client import get_status, get_chain, sync_chain


def main():
    node_a = "http://127.0.0.1:8001"
    node_b = "http://127.0.0.1:8002"

    print("HTTP node-to-node transport demo")
    print("Assumes two Triadix API nodes are already running:")
    print("  node A on :8001")
    print("  node B on :8002")
    print("")

    print("Fetching status...")
    status_a_before = get_status(node_a)
    status_b_before = get_status(node_b)

    print(f"Node A before: {status_a_before}")
    print(f"Node B before: {status_b_before}")
    print("")

    print("Fetching chain from node A...")
    chain_payload = get_chain(node_a)

    print("Syncing node B from node A chain...")
    sync_result = sync_chain(node_b, chain_payload["chain"])

    time.sleep(0.5)

    status_a_after = get_status(node_a)
    status_b_after = get_status(node_b)

    print("")
    print("Sync result:")
    print(sync_result)
    print("")
    print(f"Node A after: {status_a_after}")
    print(f"Node B after: {status_b_after}")


if __name__ == "__main__":
    main()