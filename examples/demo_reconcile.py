"""
Mini Reconciliation Example – finance flavored
"""
from bor.core import BoRRun
from bor.decorators import step

@step(name="ingest_ledger")
def ingest(s, C, V):
    return {"entries": [100, 200, 300]}

@step(name="sum_entries")
def totalize(s, C, V):
    return sum(s["entries"])

@step(name="apply_adjustment")
def adjust(s, C, V):
    return s + C.get("adjust", 0)

if __name__ == "__main__":
    run = BoRRun(S0=None, C={"adjust": -50}, V="v1.0")
    run.add_step(ingest).add_step(totalize).add_step(adjust)
    proof = run.finalize()
    print("Ledger Proof HMASTER:", proof.master)

