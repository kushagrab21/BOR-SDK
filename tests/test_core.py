from bor.core import BoRRun
from bor.hash_utils import content_hash

def add(x, C, V):
    return x + C.get("offset", 0)

def square(x, C, V):
    return x * x

def test_two_step_chain_determinism():
    run1 = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run1.add_step(add).add_step(square)
    proof1 = run1.finalize()

    run2 = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run2.add_step(add).add_step(square)
    proof2 = run2.finalize()

    assert proof1.master == proof2.master
    assert len(proof1.master) == 64

def test_proof_changes_with_input():
    runA = BoRRun(S0=3, C={"offset":2}, V="v1.0").add_step(add).add_step(square).finalize()
    runB = BoRRun(S0=4, C={"offset":2}, V="v1.0").add_step(add).add_step(square).finalize()
    assert runA.master != runB.master

def test_verify_functionality():
    run = BoRRun(S0=5, C={"offset":1}, V="v1.0")
    run.add_step(add).add_step(square)
    proof = run.finalize()
    assert run.verify() is True

