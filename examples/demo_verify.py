"""
Example: Verification Engine and CLI demo
----------------------------------------
Creates a proof, saves it, and re-verifies from file.
Run:
    python examples/demo_verify.py
Or:
    python -m bor.verify proofs/proof.json --initial '{"value":3}' --config '{"offset":2}' --stages examples.demo_verify add square
"""
import json, tempfile
from bor.core import BoRRun
from bor.verify import verify_proof

def add(x, C, V): return x + C.get("offset", 0)
def square(x, C, V): return x * x

if __name__ == "__main__":
    run = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run.add_step(add).add_step(square)
    proof = run.finalize()
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump({"stage_hashes": proof.stage_hashes, "master": proof.master}, f)
        proof_path = f.name
    print(f"Proof stored at {proof_path}")
    verify_proof(proof_path, 3, {"offset":2}, "v1.0", [add, square])

