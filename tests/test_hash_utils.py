from bor.hash_utils import canonical_bytes, content_hash

def test_canonical_bytes_basic():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert canonical_bytes(a) == canonical_bytes(b)

def test_float_normalization():
    x = {"v": 1.234567890123456}
    y = {"v": 1.234567890123459}
    # after 12-digit normalization, bytes should match
    assert canonical_bytes(x) == canonical_bytes(y)

def test_content_hash_consistency():
    data = {"x": [1, 2, 3]}
    h1 = content_hash(data)
    h2 = content_hash({"x": [1, 2, 3]})
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 length

def test_non_serializable_error():
    import pytest
    from bor.exceptions import CanonicalizationError
    class X: pass
    with pytest.raises(CanonicalizationError):
        canonical_bytes(X())

