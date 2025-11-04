"""
Module: hash_utils
------------------
Canonical encoding and hashing utilities for deterministic fingerprint generation.
"""

import json
import hashlib
import decimal
from bor.exceptions import CanonicalizationError

# === Configuration constants ===
_FLOAT_PRECISION = 12  # digits of precision for float normalization

def _normalize_floats(obj):
    """Recursively normalize all floats to fixed precision Decimals."""
    if isinstance(obj, float):
        return float(format(decimal.Decimal(str(obj)), f".{_FLOAT_PRECISION}g"))
    elif isinstance(obj, list):
        return [_normalize_floats(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: _normalize_floats(v) for k, v in obj.items()}
    else:
        return obj

def canonical_bytes(obj) -> bytes:
    """
    Convert an arbitrary Python object into canonical JSON bytes.
    Rules:
    - sort_keys=True for deterministic key ordering
    - separators=(',', ':') to remove whitespace
    - floats normalized via fixed precision
    - raise CanonicalizationError on non-serializable objects
    """
    try:
        normalized = _normalize_floats(obj)
        return json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as e:
        raise CanonicalizationError(f"Failed to canonicalize object: {e}")

def content_hash(obj) -> str:
    """
    Compute SHA-256 hex digest of canonical_bytes(obj).
    """
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

