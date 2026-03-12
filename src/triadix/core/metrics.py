import numpy as np


def entropy(b: bytes) -> float:
    values, counts = np.unique(
        np.frombuffer(b, dtype=np.uint8),
        return_counts=True
    )
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)) / 8.0)


def hamming(a: bytes, b: bytes) -> float:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b)) / (8 * len(a))


def compute_coherence_metrics(
    hE: bytes,
    hI: bytes,
    hC: bytes,
) -> tuple[float, float, float, float]:
    En = entropy(hE)
    In = entropy(hI)
    dphi = (
        hamming(hE, hI)
        + hamming(hI, hC)
        + hamming(hC, hE)
    ) / 3.0
    Cn = (En * In) / (1.0 + abs(dphi))
    return En, In, dphi, Cn