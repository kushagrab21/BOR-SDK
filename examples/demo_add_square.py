"""
Example: add→square chain with and without @step decorator
"""
from bor.core import BoRRun
from bor.decorators import step

# undecorated
def add_plain(x, C, V):
    return x + C.get("offset", 0)

# decorated with a friendly name
@step(name="square_step")
def square(x, C, V):
    return x * x

if __name__ == "__main__":
    run = BoRRun(S0=3, C={"offset":2}, V="v1.0")
    run.add_step(add_plain).add_step(square)
    proof = run.finalize()
    print("HMASTER:", proof.master)
    print("Steps:", [s.fn_name for s in run.steps])

