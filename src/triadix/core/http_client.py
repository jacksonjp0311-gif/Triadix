import requests


def get_status(base_url: str) -> dict:
    response = requests.get(f"{base_url}/status", timeout=10)
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


def register_peer(base_url: str, peer_id: str) -> dict:
    response = requests.post(
        f"{base_url}/peers",
        json={"peer_id": peer_id},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def submit_transaction(base_url: str, tx: dict) -> dict:
    response = requests.post(f"{base_url}/transactions", json=tx, timeout=20)
    response.raise_for_status()
    return response.json()


def build_from_mempool(base_url: str) -> dict:
    response = requests.post(f"{base_url}/build", timeout=20)
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


def sync_chain(base_url: str, chain: list[dict]) -> dict:
    response = requests.post(
        f"{base_url}/sync",
        json={"chain": chain},
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