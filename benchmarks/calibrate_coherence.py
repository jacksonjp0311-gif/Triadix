import json
import math
import statistics
from pathlib import Path

from triadix.core.engine import TriadicEngine


def percentile(values, p):
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    k = (len(values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    d0 = values[f] * (c - k)
    d1 = values[c] * (k - f)
    return d0 + d1


def run_case(blocks: int):
    engine = TriadicEngine()
    engine.run(blocks=blocks)
    cvals = [b.C for b in engine.chain]

    summary = {
        "blocks": blocks,
        "valid": engine.is_chain_valid(),
        "min": min(cvals),
        "max": max(cvals),
        "mean": statistics.mean(cvals),
        "median": statistics.median(cvals),
        "p05": percentile(cvals, 0.05),
        "p25": percentile(cvals, 0.25),
        "p50": percentile(cvals, 0.50),
        "p75": percentile(cvals, 0.75),
        "p95": percentile(cvals, 0.95),
    }

    summary["suggested_tau_lenient"] = summary["p05"]
    summary["suggested_tau_balanced"] = summary["p25"]
    summary["suggested_tau_strict"] = summary["p50"]

    return summary


def main():
    out_dir = Path("benchmarks") / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    sizes = [10, 100, 500, 1000]
    results = [run_case(n) for n in sizes]

    out_file = out_dir / "coherence_calibration.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("TRIADIX COHERENCE CALIBRATION")
    print("=" * 60)
    for row in results:
        print(
            f"blocks={row['blocks']:>4} | "
            f"valid={row['valid']} | "
            f"min={row['min']:.6f} | "
            f"mean={row['mean']:.6f} | "
            f"median={row['median']:.6f} | "
            f"max={row['max']:.6f}"
        )
        print(
            f"         p05={row['p05']:.6f} | "
            f"p25={row['p25']:.6f} | "
            f"p50={row['p50']:.6f} | "
            f"p75={row['p75']:.6f} | "
            f"p95={row['p95']:.6f}"
        )
        print(
            f"         tau_lenient={row['suggested_tau_lenient']:.6f} | "
            f"tau_balanced={row['suggested_tau_balanced']:.6f} | "
            f"tau_strict={row['suggested_tau_strict']:.6f}"
        )
        print("")

    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()