"""
Module: store
-------------
Local persistence layer for proofs.  
Two modes: JSON (default) and SQLite (optional).
"""

import json, sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from bor.core import Proof

class ProofStore:
    def __init__(self, root: str = ".bor_store", use_sqlite: bool = False):
        self.root = Path(root)
        self.use_sqlite = use_sqlite
        self.root.mkdir(exist_ok=True)
        if use_sqlite:
            self.db_path = self.root / "proofs.db"
            self._init_db()

    # SQLite setup
    def _init_db(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS proofs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT,
                master TEXT NOT NULL,
                stage_hashes TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()
        con.close()

    # Save proof (JSON or SQLite)
    def save(self, label: str, proof: Proof) -> Path:
        if self.use_sqlite:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(
                "INSERT INTO proofs(label, master, stage_hashes) VALUES(?,?,?)",
                (label, proof.master, json.dumps(proof.stage_hashes)),
            )
            con.commit()
            con.close()
            return self.db_path
        else:
            p = self.root / f"{label}.json"
            data = {"label": label, "master": proof.master, "stage_hashes": proof.stage_hashes}
            p.write_text(json.dumps(data, indent=2))
            return p

    # Load proof (by label)
    def load(self, label: str) -> Proof:
        if self.use_sqlite:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("SELECT master, stage_hashes FROM proofs WHERE label=? ORDER BY id DESC LIMIT 1", (label,))
            row = cur.fetchone()
            con.close()
            if not row:
                raise FileNotFoundError(f"No proof named {label}")
            return Proof(json.loads(row[1]), row[0])
        else:
            p = self.root / f"{label}.json"
            if not p.exists():
                raise FileNotFoundError(f"No proof named {label}")
            d = json.loads(p.read_text())
            return Proof(d["stage_hashes"], d["master"])

    # List stored proofs (labels only)
    def list_proofs(self) -> List[str]:
        if self.use_sqlite:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("SELECT label FROM proofs ORDER BY timestamp DESC")
            labels = [r[0] for r in cur.fetchall()]
            con.close()
            return labels
        return [ p.stem for p in self.root.glob("*.json") ]

