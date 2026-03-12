from triadix.core.http_client import get_receipt
from triadix.core.orchestrator import submit_and_build_signed_transaction


def main():
    node_a = "http://127.0.0.1:8001"

    print("Triadix v2.5 receipt demo")
    print("")

    result = submit_and_build_signed_transaction(
        node_a,
        sender="receipt-alice",
        receiver="receipt-bob",
        amount=13.0,
        data="receipt-demo",
        nonce=0,
    )
    print("Submit-and-build result:")
    print(result)
    print("")

    tx_id = result["tx_id"]
    receipt = get_receipt(node_a, tx_id)

    print("Fetched receipt:")
    print(receipt)


if __name__ == "__main__":
    main()