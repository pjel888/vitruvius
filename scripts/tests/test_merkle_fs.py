"""Sprint HP Stream HP.1 — Merkle directory hash tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.merkle_fs import (
    DirectoryHash,
    calculate_directory_hash,
    dir_has_changed,
)


def test_empty_directory_is_deterministic(tmp_path: Path) -> None:
    a = tmp_path / "a"
    a.mkdir()
    h1 = calculate_directory_hash(a)
    h2 = calculate_directory_hash(a)
    assert isinstance(h1, DirectoryHash)
    assert h1.digest == h2.digest
    assert h1.file_count == 0


def test_same_content_same_hash(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "x.md").write_text("hello", encoding="utf-8")
    (b / "x.md").write_text("hello", encoding="utf-8")
    assert calculate_directory_hash(a).digest == calculate_directory_hash(b).digest


def test_content_mutation_changes_hash(tmp_path: Path) -> None:
    a = tmp_path / "a"
    a.mkdir()
    (a / "x.md").write_text("hello", encoding="utf-8")
    h1 = calculate_directory_hash(a)
    (a / "x.md").write_text("hello world", encoding="utf-8")
    h2 = calculate_directory_hash(a)
    assert h1.digest != h2.digest


def test_subdirectory_mutation_propagates(tmp_path: Path) -> None:
    a = tmp_path / "a"
    (a / "sub").mkdir(parents=True)
    (a / "sub" / "inner.md").write_text("v1", encoding="utf-8")
    h1 = calculate_directory_hash(a)

    (a / "sub" / "inner.md").write_text("v2", encoding="utf-8")
    h2 = calculate_directory_hash(a)
    assert h1.digest != h2.digest


def test_file_count_is_recursive(tmp_path: Path) -> None:
    a = tmp_path / "a"
    (a / "sub").mkdir(parents=True)
    (a / "top.md").write_text("x", encoding="utf-8")
    (a / "sub" / "one.md").write_text("x", encoding="utf-8")
    (a / "sub" / "two.md").write_text("x", encoding="utf-8")
    report = calculate_directory_hash(a)
    assert report.file_count == 3


def test_dir_has_changed_detects_updates(tmp_path: Path) -> None:
    a = tmp_path / "a"
    a.mkdir()
    (a / "x.md").write_text("v1", encoding="utf-8")
    h1 = calculate_directory_hash(a)

    # No change — must be False
    assert dir_has_changed(a, previous_digest=h1.digest) is False

    # Mutation — must be True
    (a / "x.md").write_text("v2", encoding="utf-8")
    assert dir_has_changed(a, previous_digest=h1.digest) is True
