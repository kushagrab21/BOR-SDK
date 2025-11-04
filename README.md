# Blockchain of Reasoning (BoR) SDK v0.1.0-beta

BoR brings *reasoning integrity* to computation — turning logic itself into
a verifiable, replayable chain of deterministic proofs.

## Install

```bash
pip install bor-sdk
```

Or from source:

```bash
git clone https://github.com/kushagra-bhatnagar/bor-sdk.git
cd bor-sdk
pip install -e .
```

## Quick Start

```python
from bor.core import BoRRun
from bor.decorators import step

@step
def add(x, C, V): return x + C["offset"]

@step
def square(x, C, V): return x * x

run = BoRRun(S0=3, C={"offset":2}, V="v1.0")
run.add_step(add).add_step(square)
proof = run.finalize()
print("HMASTER:", proof.master)
```

Result → identical HMASTER on every machine.

## Features

- ✅ **Deterministic Proof Generation**: Same inputs always produce same HMASTER
- ✅ **Step-by-Step Fingerprinting**: Each reasoning step gets cryptographic hash
- ✅ **@step Decorator**: Type-safe decorator with signature enforcement
- ✅ **Replay Verification**: Prove computation integrity through deterministic replay
- ✅ **Dual Persistence**: JSON (dev-friendly) and SQLite (production-ready)
- ✅ **CLI Interface**: Command-line verification tools
- ✅ **Zero Dependencies**: Pure Python implementation

## Core Concepts

### BoRRun
The central controller for executing deterministic reasoning chains.

```python
run = BoRRun(S0=initial_state, C=config_dict, V="version_string")
run.add_step(fn1).add_step(fn2).add_step(fn3)
proof = run.finalize()
```

### Proof
Contains stage hashes and master proof (HMASTER).

```python
proof.stage_hashes  # List of per-step fingerprints
proof.master        # 64-character SHA-256 HMASTER
```

### Verification
Replay and verify stored proofs.

```python
from bor.verify import verify_proof

verify_proof("proof.json", S0, C, V, [fn1, fn2, fn3])
# Output: ✅ Proof verification successful.
```

### Persistence
Save and load proofs locally.

```python
from bor.store import ProofStore

# JSON mode (default)
store = ProofStore(root=".bor_store")
store.save("my_proof", proof)
loaded = store.load("my_proof")

# SQLite mode
store = ProofStore(root=".bor_store", use_sqlite=True)
store.save("my_proof", proof)
labels = store.list_proofs()
```

## Examples

See the `examples/` directory for complete demonstrations:

- `demo_add_square.py` - Basic 2-step chain
- `demo_pipeline.py` - Multi-step data processing
- `demo_reconcile.py` - Finance ledger reconciliation
- `demo_verify.py` - Proof storage and verification
- `demo_randomness_guard.py` - Non-determinism detection

## CLI Usage

Verify proofs from the command line:

```bash
python -m bor.verify proof.json \
  --initial '3' \
  --config '{"offset":2}' \
  --version 'v1.0' \
  --stages module.fn1 module.fn2
```

## Testing

Run the comprehensive test suite:

```bash
pytest
```

All 16 tests should pass.

## Architecture

```
BoR SDK v0.1 Architecture:
┌─────────────────────────────────────────────┐
│        User Application Layer               │
├─────────────────────────────────────────────┤
│  @step Decorator  │  BoRRun API  │  CLI     │
├─────────────────────────────────────────────┤
│     Proof Engine (core.py)                  │
│  ┌──────────┬──────────┬──────────┐        │
│  │ BoRStep  │  Proof   │  HMASTER │        │
│  └──────────┴──────────┴──────────┘        │
├─────────────────────────────────────────────┤
│  Canonicalization & Hashing (hash_utils)   │
├─────────────────────────────────────────────┤
│  Verification Engine (verify.py)            │
├─────────────────────────────────────────────┤
│  Persistence Layer (store.py)               │
│  ┌──────────────┬──────────────┐           │
│  │  JSON Store  │ SQLite Store │           │
│  └──────────────┴──────────────┘           │
└─────────────────────────────────────────────┘
```

## Requirements

- Python >= 3.9
- No external dependencies (stdlib only)

## License

MIT License

## Contributing

Issues and pull requests welcome at https://github.com/kushagra-bhatnagar/bor-sdk

---

Developed by Kushagra Bhatnagar — November 2025

