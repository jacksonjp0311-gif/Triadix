import hashlib


def H(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


def triadic_hash_cycle(
    hE: bytes,
    hI: bytes,
    hC: bytes,
    payload: bytes,
) -> tuple[bytes, bytes, bytes]:
    pE = payload
    pI = bytes(sorted(payload))
    pC = hashlib.sha256(payload).digest()

    new_hE = H(hE + hI + hC + pE)
    new_hI = H(hI + hC + hE + pI)
    new_hC = H(hC + hE + hI + pC)

    return new_hE, new_hI, new_hC