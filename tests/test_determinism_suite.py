"""
Deterministic Tests Suite
Ensures identical runs → identical HMASTER.
"""
from bor.core import BoRRun
from bor.decorators import step

@step
def add_one(x, C, V): return x + 1
@step
def times_two(x, C, V): return x * 2

def test_reproducibility_three_runs():
    C = {}
    masters = []
    for _ in range(3):
        run = BoRRun(S0=5, C=C, V="v1.0")
        run.add_step(add_one).add_step(times_two)
        masters.append(run.finalize().master)
    assert len(set(masters)) == 1, "Non-deterministic behavior detected"

def test_input_change_affects_hash():
    r1 = BoRRun(5, {}, "v1.0").add_step(add_one).add_step(times_two).finalize().master
    r2 = BoRRun(6, {}, "v1.0").add_step(add_one).add_step(times_two).finalize().master
    assert r1 != r2

