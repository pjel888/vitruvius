"""Merkle directory hash — deterministic, stream-based, millisecond latency.

Stream A Task A5 regression tests. The hash must be:
  1. Deterministic on identical trees (same content → same hash)
  2. Sensitive to content change in any file
  3. Sensitive to filename rename (even if content is preserved)
  4. Sensitive to file addition or removal
  5. Insensitive to mtime / ctime / atime (bytes only, not stat data)
  6. Dotfile-insensitive by default (.DS_Store and friends are noise)
  7. Per-directory rollup exposed for fast subtree skip in status.py
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from vitruvius.merkle.directory_hash import (
    DirectoryHashRecord,
    calculate_directory_hash,
)


def _make_tree(root: Path) -> None:
    (root / "a").mkdir()
    (root / "a" / "file1.txt").write_text("hello")
    (root / "a" / "file2.txt").write_text("world")
    (root / "b").mkdir()
    (root / "b" / "file3.txt").write_text("vitruvius")


def test_hash_is_deterministic(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash


def test_hash_changes_when_file_content_changes(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").write_text("HELLO")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_changes_when_file_renamed(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").rename(tmp_path / "a" / "renamed.txt")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_changes_when_file_added(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "new.txt").write_text("added")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_changes_when_file_removed(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").unlink()
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_unchanged_when_mtime_changes_but_content_stable(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    # Touch every file's mtime to (now + 1 day) without rewriting content
    target = time.time() + 86400
    for p in tmp_path.rglob("*"):
        if p.is_file():
            os.utime(p, (target, target))
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash


def test_record_contains_per_directory_hashes(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    record = calculate_directory_hash(tmp_path)
    assert isinstance(record, DirectoryHashRecord)
    assert record.root_hash
    relative_keys = set(record.per_directory.keys())
    assert "." in relative_keys
    assert "a" in relative_keys
    assert "b" in relative_keys


def test_subdirectory_hash_changes_isolate_to_their_subtree(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    r1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").write_text("CHANGED")
    r2 = calculate_directory_hash(tmp_path)
    # 'a' changed, 'b' did not
    assert r1.per_directory["a"] != r2.per_directory["a"]
    assert r1.per_directory["b"] == r2.per_directory["b"]


def test_ignores_dotfiles_by_default(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / ".DS_Store").write_text("mac noise")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash


def test_ignore_dotfiles_can_be_disabled(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    (tmp_path / "a" / ".DS_Store").write_text("mac noise")
    h_ignored = calculate_directory_hash(tmp_path, ignore_dotfiles=True)
    h_counted = calculate_directory_hash(tmp_path, ignore_dotfiles=False)
    assert h_ignored.root_hash != h_counted.root_hash


def test_empty_directory_produces_stable_hash(tmp_path: Path) -> None:
    h1 = calculate_directory_hash(tmp_path)
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash
    assert h1.root_hash != ""


def test_raises_on_nonexistent_path(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        calculate_directory_hash(tmp_path / "nope")


def test_raises_on_file_instead_of_directory(tmp_path: Path) -> None:
    p = tmp_path / "a_file.txt"
    p.write_text("hi")
    with pytest.raises(ValueError):
        calculate_directory_hash(p)


def test_handles_large_binary_file_via_streaming(tmp_path: Path) -> None:
    """Stream chunks are 64KB; a 200KB file exercises >3 chunks."""
    (tmp_path / "big.bin").write_bytes(b"X" * 200_000)
    record = calculate_directory_hash(tmp_path)
    assert record.root_hash
    # Same content → same hash even at non-trivial size
    record2 = calculate_directory_hash(tmp_path)
    assert record.root_hash == record2.root_hash
