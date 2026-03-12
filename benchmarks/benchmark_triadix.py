import json
import time
from pathlib import Path

from triadix.core.engine import TriadicEngine


def bench(blocks: int) -> dict:
    t0 = time.perf_counter()
    engine = TriadicEngine()
    engine.run(blocks=blocks)
    elapsed = time.perf_counter() - t0

    return {
        "blocks": blocks,
        "elapsed_seconds": elapsed,
        "blocks_per_second": (blocks / elapsed) if elapsed > 0 else None,
        "valid": engine.is_chain_valid(),
        "min_coherence": min(b.C for b in engine.chain),
        "max_coherence": max(b.C for b in engine.chain),
        "final_coherence": engine.chain[-1].C,
    }


def main():
    out_dir = Path("benchmarks") / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    sizes = [10, 100, 500, 1000]
    results = [bench(n) for n in sizes]

    out_file = out_dir / "benchmark_results.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("TRIADIX BENCHMARK RESULTS")
    print("=" * 40)
    for row in results:
        print(
            f"blocks={row['blocks']:>4} | "
            f"time={row['elapsed_seconds']:.6f}s | "
            f"bps={row['blocks_per_second']:.2f} | "
            f"valid={row['valid']} | "
            f"Cmin={row['min_coherence']:.6f} | "
            f"Cmax={row['max_coherence']:.6f}"
        )

    print("")
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()