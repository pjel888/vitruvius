"""Integration: status.py exposes a flag-gated Merkle fast-skip path.

Task A7 of Stream A — adds a NEW function ``compute_status_with_merkle``
to status.py without modifying any existing code path. Existing
``run_status`` behaves identically regardless of the flag state.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.features import Features
from vitruvius.status import MerkleStatus, compute_status_with_merkle


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    t = tmp_path / "tree"
    t.mkdir()
    (t / "a.pdf").write_bytes(b"%PDF stable")
    return t


def test_flag_off_returns_noop_sentinel(tree: Path) -> None:
    features = Features(flags={})
    result = compute_status_with_merkle(root=tree, features=features)
    assert isinstance(result, MerkleStatus)
    assert result.root_hash == ""
    assert result.skipped is False


def test_flag_on_returns_non_empty_hash(tree: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    result = compute_status_with_merkle(root=tree, features=features)
    assert result.root_hash != ""
    # First run with no previous_hash => nothing to compare => skipped=False
    assert result.skipped is False


def test_unchanged_directory_is_skipped(tree: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    result1 = compute_status_with_merkle(root=tree, features=features)
    result2 = compute_status_with_merkle(
        root=tree,
        features=features,
        previous_hash=result1.root_hash,
    )
    assert result2.skipped is True
    assert result2.root_hash == result1.root_hash


def test_changed_directory_is_not_skipped(tree: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    result1 = compute_status_with_merkle(root=tree, features=features)
    (tree / "b.pdf").write_bytes(b"%PDF new")
    result2 = compute_status_with_merkle(
        root=tree,
        features=features,
        previous_hash=result1.root_hash,
    )
    assert result2.skipped is False
    assert result2.root_hash != result1.root_hash


def test_previous_hash_with_flag_off_does_not_skip(tree: Path) -> None:
    features = Features(flags={})
    result = compute_status_with_merkle(
        root=tree,
        features=features,
        previous_hash="any_hash_goes_here",
    )
    assert result.skipped is False
    assert result.root_hash == ""


def test_mtime_touch_does_not_break_skip(tree: Path) -> None:
    """Content-only hash ⇒ mtime touches still count as unchanged."""
    import os
    import time

    features = Features(flags={"a_merkle_hash": True})
    result1 = compute_status_with_merkle(root=tree, features=features)
    target = time.time() + 86400
    for p in tree.rglob("*"):
        if p.is_file():
            os.utime(p, (target, target))
    result2 = compute_status_with_merkle(
        root=tree,
        features=features,
        previous_hash=result1.root_hash,
    )
    assert result2.skipped is True
