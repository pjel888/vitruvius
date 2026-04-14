"""Integration: scanner.py exposes a flag-gated Merkle scan function.

Task A6 of Stream A — adds a NEW function ``scan_with_merkle`` to scanner.py
without modifying any existing code path. Existing ``build_file_entries``,
``build_tree_lines`` and ``run_scan`` behave identically regardless of
whether ``features.a_merkle_hash`` is on or off.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.features import Features
from vitruvius.merkle import calculate_directory_hash
from vitruvius.scanner import MerkleScanResult, scan_with_merkle


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A tree *inside* tmp_path so sibling registry files don't contaminate."""
    t = tmp_path / "tree"
    t.mkdir()
    (t / "laws").mkdir()
    (t / "laws" / "a.pdf").write_bytes(b"%PDF-1.4 fake")
    (t / "laws" / "b.pdf").write_bytes(b"%PDF-1.4 fake 2")
    return t


def test_scan_with_merkle_flag_on_matches_direct_call(tree: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    result = scan_with_merkle(root=tree, features=features)
    expected = calculate_directory_hash(tree)
    assert isinstance(result, MerkleScanResult)
    assert result.root_hash == expected.root_hash
    assert result.record is not None


def test_scan_with_merkle_flag_off_returns_sentinel(tree: Path) -> None:
    features = Features(flags={})
    result = scan_with_merkle(root=tree, features=features)
    assert result.root_hash == ""
    assert result.record is None


def test_scan_with_merkle_writes_csv_registry_when_path_given(
    tree: Path, tmp_path: Path
) -> None:
    features = Features(flags={"a_merkle_hash": True})
    registry = tmp_path / "merkle_registry.csv"
    scan_with_merkle(root=tree, features=features, registry_path=registry)
    assert registry.exists()
    lines = registry.read_text().strip().split("\n")
    assert lines[0] == "relative_path,hash"
    # At least the two real dirs '.' and 'laws' should appear
    body = "\n".join(lines[1:])
    assert "." in body
    assert "laws" in body


def test_scan_with_merkle_registry_not_written_when_flag_off(
    tree: Path, tmp_path: Path
) -> None:
    features = Features(flags={})
    registry = tmp_path / "merkle_registry.csv"
    scan_with_merkle(root=tree, features=features, registry_path=registry)
    assert not registry.exists()


def test_scan_with_merkle_registry_deterministic_across_runs(
    tree: Path, tmp_path: Path
) -> None:
    features = Features(flags={"a_merkle_hash": True})
    registry_a = tmp_path / "r_a.csv"
    registry_b = tmp_path / "r_b.csv"
    scan_with_merkle(root=tree, features=features, registry_path=registry_a)
    scan_with_merkle(root=tree, features=features, registry_path=registry_b)
    assert registry_a.read_text() == registry_b.read_text()


def test_scan_with_merkle_registry_sorted_alphabetically(
    tree: Path, tmp_path: Path
) -> None:
    features = Features(flags={"a_merkle_hash": True})
    registry = tmp_path / "r.csv"
    scan_with_merkle(root=tree, features=features, registry_path=registry)
    rows = [
        line.split(",", 1)[0]
        for line in registry.read_text().strip().split("\n")[1:]
    ]
    assert rows == sorted(rows)
