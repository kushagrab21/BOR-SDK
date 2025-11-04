import json, os
from bor.core import BoRRun
from bor.store import ProofStore

def add(x,C,V): return x + C.get("offset", 0)
def square(x,C,V): return x * x

def test_json_store_cycle(tmp_path):
    store = ProofStore(root=tmp_path)
    run = BoRRun(3, {"offset":2}, "v1.0").add_step(add).add_step(square)
    proof = run.finalize()
    path = store.save("demo", proof)
    loaded = store.load("demo")
    assert proof.master == loaded.master
    assert os.path.exists(path)

def test_sqlite_store_cycle(tmp_path):
    store = ProofStore(root=tmp_path, use_sqlite=True)
    run = BoRRun(4, {"offset":2}, "v1.0").add_step(add).add_step(square)
    proof = run.finalize()
    store.save("ledger", proof)
    labels = store.list_proofs()
    assert "ledger" in labels
    loaded = store.load("ledger")
    assert loaded.master == proof.master

