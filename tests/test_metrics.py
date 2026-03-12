from triadix.core.metrics import entropy, hamming, compute_coherence_metrics


def test_entropy_in_range():
    value = entropy(bytes(range(32)))
    assert 0.0 <= value <= 1.0


def test_hamming_in_range():
    a = b"\x00" * 32
    b = b"\xff" * 32
    value = hamming(a, b)
    assert 0.0 <= value <= 1.0


def test_compute_coherence_metrics_returns_tuple():
    h = bytes(range(32))
    En, In, dphi, Cn = compute_coherence_metrics(h, h, h)
    assert 0.0 <= En <= 1.0
    assert 0.0 <= In <= 1.0
    assert 0.0 <= dphi <= 1.0
    assert Cn >= 0.0