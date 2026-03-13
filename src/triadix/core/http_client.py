import requests


def get_status(base_url: str) -> dict:
    response = requests.get(f"{base_url}/status", timeout=10)
    response.raise_for_status()
    return response.json()


def get_receipt(base_url: str, tx_id: str) -> dict:
    response = requests.get(f"{base_url}/receipts/{tx_id}", timeout=10)
    response.raise_for_status()
    return response.json()


def set_identity(base_url: str, label: str | None = None, base_url_value: str | None = None) -> dict:
    response = requests.post(
        f"{base_url}/identity",
        json={"label": label, "base_url": base_url_value},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def get_chain(base_url: str) -> dict:
    response = requests.get(f"{base_url}/chain", timeout=20)
    response.raise_for_status()
    return response.json()


def list_peers(base_url: str) -> dict:
    response = requests.get(f"{base_url}/peers", timeout=10)
    response.raise_for_status()
    return response.json()


def register_peer(base_url: str, peer_id: str, peer_base_url: str = "", label: str = "") -> dict:
    response = requests.post(
        f"{base_url}/peers",
        json={"peer_id": peer_id, "base_url": peer_base_url, "label": label},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def submit_transaction(base_url: str, tx: dict) -> dict:
    response = requests.post(f"{base_url}/transactions", json=tx, timeout=20)
    response.raise_for_status()
    return response.json()


def build_from_mempool(base_url: str, max_transactions: int | None = None) -> dict:
    payload = {"max_transactions": max_transactions} if max_transactions is not None else {}
    response = requests.post(f"{base_url}/build", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


def submit_and_build(base_url: str, tx: dict) -> dict:
    response = requests.post(
        f"{base_url}/submit-and-build",
        json=tx,
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def seed_demo(base_url: str, blocks: int = 12) -> dict:
    response = requests.post(
        f"{base_url}/seed-demo",
        json={"blocks": blocks},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def sync_chain(base_url: str, chain: list[dict], checkpoints: dict[str, str] | None = None) -> dict:
    response = requests.post(
        f"{base_url}/sync",
        json={"chain": chain, "checkpoints": checkpoints},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def save_state(base_url: str, filepath: str | None = None) -> dict:
    response = requests.post(
        f"{base_url}/save-state",
        json={"filepath": filepath},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def load_state(base_url: str, filepath: str) -> dict:
    response = requests.post(
        f"{base_url}/load-state",
        json={"filepath": filepath},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()