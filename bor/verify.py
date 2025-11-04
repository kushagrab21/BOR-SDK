"""
Module: verify
--------------
Performs deterministic replay verification of a saved proof.
Also exposes a small CLI utility:  python -m bor.verify proof.json
"""

import json
import argparse
from pathlib import Path
from bor.core import BoRRun, Proof
from bor.exceptions import DeterminismError, HashMismatchError

def verify_proof(proof_path: str, S0, C, V, stages) -> bool:
    """
    Load a stored proof file (JSON) and re-execute the reasoning chain.
    Compare recomputed master hash with stored one.
    Returns True if identical, else raises HashMismatchError.
    """
    p = Path(proof_path)
    if not p.exists():
        raise FileNotFoundError(f"Proof file not found: {proof_path}")

    proof_data = json.loads(p.read_text())
    stored_master = proof_data.get("master")
    stored_stage_hashes = proof_data.get("stage_hashes", [])

    # Recompute
    run = BoRRun(S0, C, V)
    for fn in stages:
        run.add_step(fn)
    new_proof = run.finalize()

    if new_proof.master != stored_master:
        raise HashMismatchError(
            f"Verification failed!\nStored={stored_master}\nRecomputed={new_proof.master}"
        )

    # Optional: confirm stage-by-stage equality
    if stored_stage_hashes and stored_stage_hashes != new_proof.stage_hashes:
        print("⚠ Stage hashes differ, but master proof still matches.")

    print("✅ Proof verification successful.")
    return True


# === CLI entry ===
def _cli():
    parser = argparse.ArgumentParser(description="Verify a BoR proof JSON file.")
    parser.add_argument("proof", help="Path to proof.json")
    parser.add_argument("--config", default="{}", help="JSON string for config C")
    parser.add_argument("--version", default="v1.0", help="Code version string")
    parser.add_argument("--initial", default="{}", help="JSON for initial state S0")
    parser.add_argument("--stages", nargs="+", required=False,
                        help="Python module-qualified function names to replay")
    args = parser.parse_args()

    S0 = json.loads(args.initial)
    C = json.loads(args.config)
    V = args.version

    if not args.stages:
        raise DeterminismError("Must supply stage function names for replay.")

    # Dynamic import of stage functions
    import importlib
    stages = []
    for s in args.stages:
        mod_name, fn_name = s.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        stages.append(getattr(mod, fn_name))

    verify_proof(args.proof, S0, C, V, stages)


if __name__ == "__main__":
    _cli()

