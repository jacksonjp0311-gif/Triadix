from triadix.core.orchestrator import build_signed_transaction_payload
from triadix.core.http_client import submit_transaction, build_from_mempool, get_status


def main():
    node_a = "http://127.0.0.1:8001"

    print("Triadix v2.6 selection demo")
    print("")

    txs = [
        build_signed_transaction_payload("alice", "bob", 1.0, "a", 0),
        build_signed_transaction_payload("alice", "carol", 2.0, "b", 1),
        build_signed_transaction_payload("alice", "dave", 3.0, "c", 2),
    ]

    submit_results = []
    for tx in txs:
        submit_results.append(submit_transaction(node_a, tx))

    print("Submitted:")
    print(submit_results)
    print("")

    build_result = build_from_mempool(node_a, max_transactions=2)
    print("Build with max_transactions=2:")
    print(build_result)
    print("")

    status = get_status(node_a)
    print("Status after build:")
    print(status)


if __name__ == "__main__":
    main()