TRIADIX  
**"Three hashes. One truth. Zero blind spots."**

A coherence-native ledger system focused on two guarantees at once:
1) chain integrity, and 2) internal state coherence over time.

---

## Executive Summary

Triadix started as a deterministic triadic ledger kernel and has evolved into a broader local node stack with:
- deterministic block validation,
- signed transactions,
- mempool + queued-gap handling,
- receipt generation,
- node identity and peer metadata,
- checkpoint-aware chain sync,
- HTTP API transport.

The repository includes runnable demos, a CLI, API-node workflows, benchmark scripts, and a comprehensive automated test suite.

---

## Why Triadix Exists

Most chains answer: **"Is linkage intact?"**

Triadix also answers: **"Is the chain's internal state evolution still coherent?"**

Instead of a single digest path, Triadix evolves three related hash channels per block and computes coherence metrics from that state. This creates a drift-observable ledger primitive for provenance-heavy and audit-heavy environments.

---

## Architecture at a Glance

### Triadic State Cycle

Each block advances three channels:
- `hE`: raw payload path
- `hI`: sorted-byte canonical payload path
- `hC`: pre-hashed payload path

### Validation Model

A chain is valid when recomputation confirms:
- previous triadic references,
- triadic hash values,
- stored per-block metrics.

### Health Model

A chain is healthy when coherence distribution satisfies policy thresholds (for example p25-based policy against `tau`).

---

## Repository Analysis

### 1) Product Surface

Triadix currently exposes four practical surfaces:
- **Core engine** (`src/triadix/core/engine.py`) for chain construction, validation, health checks, mempool logic, transaction admission, receipts, and checkpoint behavior.
- **Node layer** (`src/triadix/core/node.py`) for identity, peer metadata, sync, and orchestrated node behavior.
- **HTTP API** (`src/triadix/core/api.py`) for status, peers, transaction submission, block building, chain export, and receipt access.
- **CLI** (`src/triadix/cli.py`) for local run and validate loops.

### 2) Code Organization and Intent

- `src/triadix/core/`: primary runtime logic (engine, transactions, wallet, API, sync/orchestration).
- `src/triadix/models/`: data structures such as blocks, receipts, and node records.
- `src/triadix/utils/`: configuration and utilities.
- `src/triadix/visualization/`: plotting helpers for coherence/state output.
- `tests/`: broad coverage over engine behavior, policy, transport, persistence, sync, mempool, receipts, and checkpoints.
- `examples/`: runnable demonstrations by capability layer.
- `benchmarks/`: stress/performance calibration and benchmark utilities.
- `docs/`: conceptual and flow documentation.

### 3) Maturity Signals

The project demonstrates engineering maturity through:
- deterministic, recomputation-first validation,
- extensive pytest coverage across core and network-adjacent flows,
- explicit examples for real workflows,
- benchmark artifacts/checkpoints for repeatability,
- API and CLI entry points suitable for local integration testing.

### 4) Tradeoffs / Current Boundaries

Triadix is a strong **kernel + local node transport stack**, but not yet a full decentralized production network. It does not currently present a finalized consensus protocol, smart-contract runtime, or fully hardened distributed validator economy.

---

## Directory Structure

```text
Triadix/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── triadix/
│       ├── __init__.py
│       ├── __version__.py
│       ├── cli.py
│       ├── core/
│       │   ├── api.py
│       │   ├── engine.py
│       │   ├── node.py
│       │   ├── orchestrator.py
│       │   ├── transactions.py
│       │   ├── wallet.py
│       │   └── ...
│       ├── models/
│       │   ├── block.py
│       │   ├── node.py
│       │   └── receipt.py
│       ├── utils/
│       └── visualization/
├── tests/
├── examples/
├── benchmarks/
│   └── results/
├── docs/
├── manifest/
└── scripts/
```

---

## Installation

### Requirements

- Python 3.10+
- `pip`

### Recommended Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .[dev]
```

### Verify Installation

```bash
triadix --help
python -m pytest -q
```

---

## Quick Start

### CLI Run

```bash
triadix run --blocks 96
```

### CLI Validation

```bash
triadix validate --blocks 96
```

### Start API Node

```bash
python -m triadix.core.server --host 127.0.0.1 --port 8000
```

### Run Example Scripts

```bash
python examples/basic_run.py
python examples/signed_transaction_demo.py
python examples/mempool_demo.py
python examples/http_end_to_end_demo.py
```

---

## API Snapshot

The FastAPI service (`src/triadix/core/api.py`) includes routes such as:
- `GET /` project/version heartbeat,
- `GET /status` node + engine status snapshot,
- `GET /chain` chain and checkpoint export,
- `GET /peers` peer registry view,
- `GET /receipts/{tx_id}` transaction receipt retrieval,
- `POST /transactions` transaction submission,
- `POST /build` block assembly from mempool,
- `POST /peers` peer registration,
- `POST /identity` node metadata updates.

---

## Testing and Quality

The test suite covers:
- engine correctness,
- hash behavior,
- policy and health evaluation,
- signed transactions and admission rules,
- mempool and queued-gap handling,
- receipt persistence and retrieval,
- node sync, API transport, and orchestrator flow,
- checkpoint and persistence behavior,
- benchmark sanity checks.

Run all tests:

```bash
python -m pytest -q
```

---

## Benchmarks and Performance

The repository includes benchmark runners and result artifacts under `benchmarks/` and `benchmarks/results/`.

Typical commands:

```bash
python benchmarks/benchmark_triadix.py
python benchmarks/ultra_nuclear_test.py
python benchmarks/deep_nuclear_test.py
```

Use these to profile throughput, coherence distribution, and policy behavior under higher block counts.

---

## Version Progression (Repository Narrative)

- **v1.2**: triadic ledger kernel baseline.
- **v1.3**: signed transaction support and wallet flow.
- **v1.4**: mempool + nonce/replay protection + block assembly.
- **v1.5**: multi-node sync and deterministic valid-chain adoption.
- **v1.7–v1.9**: transport scaffolding and full local HTTP flow.
- **v2.0–v2.7**: status model cleanup, peer metadata, persistence, checkpoints, receipts, deterministic selection diagnostics, queued-gap handling.

---

## Practical Use Cases

Triadix is a strong fit for:
- AI provenance ledgers,
- scientific and simulation reproducibility trails,
- compliance and audit-grade execution logs,
- drift-aware data lineage systems,
- blockchain research centered on coherence-aware integrity.

---

## License

MIT.
