import requests


def get_status(base_url: str) -> dict:
    response = requests.get(f"{base_url}/status", timeout=10)
    response.raise_for_status()
    return response.json()


def get_chain(base_url: str) -> dict:
    response = requests.get(f"{base_url}/chain", timeout=20)
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


def sync_chain(base_url: str, chain: list[dict]) -> dict:
    response = requests.post(
        f"{base_url}/sync",
        json={"chain": chain},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()