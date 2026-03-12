import json
import math
import statistics
import time
from pathlib import Path

from triadix.core.engine import TriadicEngine


def percentile(values, p):
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    k = (len(values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] * (c - k) + values[c] * (k - f)


def main():
    # Choose a size big enough to be meaningful but still practical.
    blocks = 10000

    t0 = time.perf_counter()
    engine = TriadicEngine()
    chain = engine.run(blocks=blocks)
    elapsed = time.perf_counter() - t0

    cvals = [b.C for b in chain]

    result = {
        "test_name": "triadix_nuclear_test",
        "version": "1.2.0",
        "blocks": blocks,
        "elapsed_seconds": elapsed,
        "blocks_per_second": (blocks / elapsed) if elapsed > 0 else None,
        "valid": engine.is_chain_valid(),
        "healthy_under_tau": all(b.C >= engine.config.tau for b in chain),
        "tau": engine.config.tau,
        "coherence": {
            "min": min(cvals),
            "max": max(cvals),
            "mean": statistics.mean(cvals),
            "median": statistics.median(cvals),
            "p05": percentile(cvals, 0.05),
            "p25": percentile(cvals, 0.25),
            "p50": percentile(cvals, 0.50),
            "p75": percentile(cvals, 0.75),
            "p95": percentile(cvals, 0.95),
            "final": cvals[-1],
        }
    }

    out_dir = Path("benchmarks") / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "nuclear_test.json"
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("TRIADIX NUCLEAR TEST")
    print("=" * 60)
    print(f"blocks            : {result['blocks']}")
    print(f"elapsed_seconds   : {result['elapsed_seconds']:.6f}")
    print(f"blocks_per_second : {result['blocks_per_second']:.2f}")
    print(f"valid             : {result['valid']}")
    print(f"healthy_under_tau : {result['healthy_under_tau']}")
    print(f"tau               : {result['tau']:.6f}")
    print("")
    print("COHERENCE")
    print(f"min    : {result['coherence']['min']:.6f}")
    print(f"mean   : {result['coherence']['mean']:.6f}")
    print(f"median : {result['coherence']['median']:.6f}")
    print(f"max    : {result['coherence']['max']:.6f}")
    print(f"p05    : {result['coherence']['p05']:.6f}")
    print(f"p25    : {result['coherence']['p25']:.6f}")
    print(f"p50    : {result['coherence']['p50']:.6f}")
    print(f"p75    : {result['coherence']['p75']:.6f}")
    print(f"p95    : {result['coherence']['p95']:.6f}")
    print(f"final  : {result['coherence']['final']:.6f}")
    print("")
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()