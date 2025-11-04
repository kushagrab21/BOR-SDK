"""
Module: core
------------
Implements BoRRun, BoRStep, and Proof structures.
Each step in reasoning emits a fingerprint hi,
and all fingerprints concatenate into HMASTER.
"""

from dataclasses import dataclass, asdict
from typing import Any, Callable, List, Dict
import inspect
from bor.hash_utils import content_hash, canonical_bytes
from bor.exceptions import DeterminismError, HashMismatchError

@dataclass
class BoRStep:
    """Represents a single deterministic reasoning step."""
    fn_name: str
    input_state: Any
    config: Dict
    code_version: str
    fingerprint: str = None

    def compute_fingerprint(self):
        """Compute and store fingerprint for this step."""
        payload = {
            "fn": self.fn_name,
            "input": self.input_state,
            "config": self.config,
            "version": self.code_version,
        }
        self.fingerprint = content_hash(payload)
        return self.fingerprint

@dataclass
class Proof:
    """Holds list of step hashes and master proof fingerprint."""
    stage_hashes: List[str]
    master: str

class BoRRun:
    """
    Controller for executing deterministic reasoning chains.
    Usage:
        run = BoRRun(S0, C, V)
        run.add_step(fn1).add_step(fn2)
        proof = run.finalize()
        run.verify()
    """
    def __init__(self, S0: Any, C: Dict, V: str):
        self.initial_state = S0
        self.config = C
        self.code_version = V
        self.steps: List[BoRStep] = []
        self._final_state = None
        self.proof: Proof | None = None

    # --- Step execution ---
    def add_step(self, fn: Callable):
        """Apply a deterministic function and record its fingerprint."""
        if not callable(fn):
            raise DeterminismError("Step must be a callable.")
        prev_state = self.initial_state if not self.steps else self._final_state

        try:
            output_state = fn(prev_state, self.config, self.code_version)
        except Exception as e:
            raise DeterminismError(f"Function {fn.__name__} failed deterministically: {e}")

        step = BoRStep(fn.__name__, prev_state, self.config, self.code_version)
        step.compute_fingerprint()
        self.steps.append(step)
        self._final_state = output_state
        return self

    # --- Final proof computation ---
    def finalize(self) -> Proof:
        """Compute master proof HMASTER by concatenating all step fingerprints."""
        if not self.steps:
            raise DeterminismError("No steps added to BoRRun.")
        concatenated = "".join([s.fingerprint for s in self.steps])
        master = content_hash(concatenated)
        self.proof = Proof([s.fingerprint for s in self.steps], master)
        return self.proof

    # --- Verification ---
    def verify(self) -> bool:
        """Recompute proof deterministically and check master equality."""
        if not self.proof:
            raise DeterminismError("Run must be finalized before verification.")
        recomputed = self.finalize()
        if recomputed.master != self.proof.master:
            raise HashMismatchError("Master proof mismatch: reasoning diverged.")
        return True

    def summary(self) -> Dict:
        """Return dictionary summary of current run."""
        return {
            "initial_state": self.initial_state,
            "num_steps": len(self.steps),
            "fingerprints": [s.fingerprint for s in self.steps],
            "HMASTER": self.proof.master if self.proof else None,
        }

