import json, tempfile
from bor.core import BoRRun
from bor.verify import verify_proof

def add(x, C, V): return x + C.get("offset", 0)
def square(x, C, V): return x * x

def test_verify_recomputes_success(tmp_path):
    run = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run.add_step(add).add_step(square)
    proof = run.finalize()
    proof_file = tmp_path / "proof.json"
    proof_file.write_text(json.dumps({"stage_hashes": proof.stage_hashes, "master": proof.master}))

    assert verify_proof(str(proof_file), 3, {"offset":2}, "v1.0", [add, square]) is True

def test_verify_detects_mismatch(tmp_path):
    run = BoRRun(S0=3, C={"offset":2}, V="v1.0").add_step(add).add_step(square)
    proof = run.finalize()
    bad_file = tmp_path / "bad.json"
    altered = proof.master[:-1] + "x"
    bad_file.write_text(json.dumps({"stage_hashes": proof.stage_hashes, "master": altered}))
    from bor.exceptions import HashMismatchError
    import pytest
    with pytest.raises(HashMismatchError):
        verify_proof(str(bad_file), 3, {"offset":2}, "v1.0", [add, square])

