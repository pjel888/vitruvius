"""Sanity-check the rocksdict dependency is importable and can round-trip bytes.

This is a 3-line smoke test, not a full backend test. Task 4 and
Task 5 cover the actual class-level behaviour.
"""
from __future__ import annotations

from pathlib import Path

import pytest


def test_rocksdict_import_and_roundtrip(tmp_path: Path) -> None:
    rocksdict = pytest.importorskip("rocksdict")
    db = rocksdict.Rdict(str(tmp_path / "smoke.rocksdb"))
    try:
        db[b"k"] = b"v"
        assert db[b"k"] == b"v"
        assert db.get(b"nope") is None
    finally:
        db.close()
