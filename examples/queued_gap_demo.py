from triadix.core.orchestrator import build_signed_transaction_payload
from triadix.core.http_client import submit_transaction, build_from_mempool, get_status


def main():
    node_a = "http://127.0.0.1:8001"

    print("Triadix v2.7 queued-gap mempool demo")
    print("")

    tx2 = build_signed_transaction_payload("gap-alice", "carol", 2.0, "future", 1)
    tx1 = build_signed_transaction_payload("gap-alice", "bob", 1.0, "first", 0)

    result_future = submit_transaction(node_a, tx2)
    print("Submit nonce 1 first:")
    print(result_future)
    print("")

    status_after_future = get_status(node_a)
    print("Status after future nonce submission:")
    print(status_after_future)
    print("")

    result_first = submit_transaction(node_a, tx1)
    print("Submit nonce 0:")
    print(result_first)
    print("")

    status_after_first = get_status(node_a)
    print("Status after gap fill:")
    print(status_after_first)
    print("")

    build_result = build_from_mempool(node_a, max_transactions=2)
    print("Build block:")
    print(build_result)


if __name__ == "__main__":
    main()