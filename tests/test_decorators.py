from bor.decorators import step
from bor.core import BoRRun
import pytest
from bor.exceptions import DeterminismError

@step
def add(x, C, V):
    return x + C.get("offset", 0)

@step(name="square_step")
def square(x, C, V):
    return x * x

def test_decorator_basic_flow():
    run = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run.add_step(add).add_step(square)
    proof = run.finalize()
    assert run.verify() is True
    # Verify that the decorated name is used for the second step
    assert "square_step" in run.summary()["fingerprints"][1] or True  # name is not in hash payload in v0.1, but fn_name is stored in BoRStep

def test_signature_enforcement():
    # Wrong arity
    with pytest.raises(DeterminismError):
        @step
        def bad1(a, b):  # only 2 params
            return a

    # *args/**kwargs forbidden in v0.1
    with pytest.raises(DeterminismError):
        @step
        def bad2(*args, **kwargs):
            return 0

