from triadix.core.hashes import triadic_hash_cycle

ZERO32 = b"\x00" * 32


def test_triadic_hash_cycle_returns_three_hashes():
    hE, hI, hC = triadic_hash_cycle(ZERO32, ZERO32, ZERO32, b"abc")
    assert isinstance(hE, bytes)
    assert isinstance(hI, bytes)
    assert isinstance(hC, bytes)
    assert len(hE) == 32
    assert len(hI) == 32
    assert len(hC) == 32