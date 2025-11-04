"""
Example Pipeline: Data → Normalize → Transform → Aggregate
Demonstrates multi-step BoR reasoning.
"""
from bor.core import BoRRun
from bor.decorators import step

@step(name="normalize")
def normalize(s, C, V):
    # simple scalar normalization
    return s / C.get("scale", 1)

@step(name="transform")
def transform(s, C, V):
    return s ** 2 + C.get("bias", 0)

@step(name="aggregate")
def aggregate(s, C, V):
    return round(s, 4)

if __name__ == "__main__":
    C = {"scale": 2, "bias": 3}
    run = BoRRun(S0=8, C=C, V="v1.0")
    run.add_step(normalize).add_step(transform).add_step(aggregate)
    proof = run.finalize()
    print("HMASTER:", proof.master)
    print("Summary:", run.summary())

