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