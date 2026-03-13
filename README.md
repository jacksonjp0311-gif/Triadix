TRIADIX
Three hashes. One truth. Zero blind spots.

A coherence-native ledger kernel for deterministic validation, drift observability, and triadic state integrity.

Why Triadix exists

Most ledgers answer one question:

Did the chain link correctly?

Triadix answers two:

Did the chain link correctly?
And is the evolving internal state still coherent?

That second question is the reason this project exists.

Triadix extends ordinary hash-chaining with a triadic state cycle:

hE

hI

hC

Each block updates all three channels, then computes coherence metrics over the resulting state. The goal is not just to preserve linkage, but to expose drift, distribution, and health inside the chain itself.

Canonical result

Triadix v1.2 passed its current anchor stress run:

100,000 blocks

valid = True

healthy = True

3,442.35 blocks/sec

tau = 0.244

health_mode = p25

Coherence profile

min: 0.209818

mean: 0.248315

max: 0.273224

p05: 0.236975

p25: 0.244040

p50: 0.248575

p75: 0.252928

p95: 0.258508

final: 0.249249

fraction >= tau: 0.751170

This is the current benchmark anchor for the repository.

What Triadix is

Triadix v1.2 is a working ledger kernel with:

triadic hash-state evolution

deterministic payload canonicalization

explicit genesis creation

full recomputation-based validation

tamper detection

empirical coherence calibration

percentile-based health policy

test and benchmark scaffolding

This is the kernel first.

What Triadix is not

Triadix v1.2 is not yet:

a distributed L1 network

an L2 system

a staking protocol

a smart contract VM

a validator network

a finished consensus layer

Those come after the kernel is proven.

Core model
Triadic state cycle

Each block advances three coupled channels derived from different payload views:

hE — raw payload path

hI — sorted-byte payload path

hC — pre-hashed payload path

This gives Triadix a richer internal state transition than a single linear digest.

Validation

A chain is valid if:

previous triadic references match

recomputed triadic hashes match stored values

recomputed metrics match stored values

Health

A chain is healthy if its coherence distribution satisfies a calibrated policy.

Current default policy:

tau = 0.244

health_mode = p25

That means health is evaluated against the lower quartile of the coherence distribution, rather than requiring every block to clear threshold.

Why it matters

Triadix is aimed at systems where plain integrity is not enough.

Strong fit areas include:

AI provenance ledgers

scientific reproducibility logs

drift-aware audit trails

compliance-oriented execution records

coherence-aware blockchain research

If a system needs to preserve not just state, but state quality, Triadix is the right kind of primitive.

Repository layout

Triadix/
├── src/triadix/
│ ├── cli.py
│ ├── models/
│ ├── core/
│ ├── utils/
│ └── visualization/
├── tests/
├── benchmarks/
├── docs/
├── examples/
└── manifest/

Quick start
Install

pip install -e .[dev]

Run tests

python -m pytest -q

Run the CLI

triadix run --blocks 96

Run the ultra benchmark

python .\benchmarks\ultra_nuclear_test.py

Triadix v1.3 introduces signed transaction support with wallet key generation, cryptographic verification, tamper rejection, enforced admission rules, and a working end-to-end signed transaction demo.

Triadix v1.4 adds a mempool, sender nonce tracking, replay rejection, block assembly from pending transactions, and an end-to-end mempool demo with valid and healthy execution.

Triadix v1.5 introduces multi-node chain sync, deterministic valid-chain adoption, and signed-transaction chain transfer between nodes.

Triadix v1.7 introduces a minimal transport-layer scaffold with node status, chain export/sync flow, signed transaction transport semantics, and passing transport-level tests.

Triadix v1.8 introduces a runnable API-node layer with FastAPI transport, HTTP client helpers, local multi-port launch scripts, and passing transport-level tests.

Triadix v1.9 completes the first end-to-end local HTTP flow: signed transaction submission, block build, chain fetch, and valid-chain adoption between API nodes.

Triadix v2.0 consolidates the stack with unified status reporting, health evaluability rules, cleaner API/node snapshots, and aligned demo semantics across local HTTP transport.

Triadix v2.1 extends the HTTP node layer with peer registration, demo-chain seeding, submit-and-build flow, and a cleaner local orchestration path for multi-node testing.

Triadix v2.2 adds durable node persistence with save/load support for chain state, mempool state, account nonces, and API-level recovery flow.

Triadix v2.3 adds stable node identity, peer metadata records, enriched node snapshots, and a cleaner trust surface for multi-node coordination.

Triadix v2.4 adds periodic chain checkpoints, persisted checkpoint metadata, and checkpoint-verified sync for safer chain import and adoption.

Triadix v2.5 adds deterministic transaction IDs, receipt generation, receipt persistence, and API-level receipt lookup for clean transaction outcome proof.

Triadix v2.6 adds deterministic mempool ordering, configurable transaction selection limits, and selection diagnostics for explainable block assembly.

Triadix v2.7 adds queued-gap mempool handling, allowing future-nonce transactions to wait safely until missing earlier nonces arrive while preserving deterministic selection and replay protection.



