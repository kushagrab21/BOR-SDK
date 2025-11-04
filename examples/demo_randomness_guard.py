"""
Demonstrates detection of non-determinism.
"""
from bor.core import BoRRun
from bor.decorators import step
import random
from bor.exceptions import DeterminismError

@step
def nondeterministic_fn(s, C, V):
    # introduces randomness deliberately
    return s + random.random()

if __name__ == "__main__":
    try:
        run = BoRRun(S0=1, C={}, V="v1.0")
        run.add_step(nondeterministic_fn).finalize()
    except DeterminismError as e:
        print("⚠ Detected non-determinism:", e)

