from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

from vitruvius.models import FileEntry
from vitruvius.scanner import build_file_entries
from vitruvius.reports import write_csv

HELLO_WORLD_SHA256 = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_file_entry_has_sha256_field() -> None:
    import dataclasses

    fields = {f.name: f for f in dataclasses.fields(FileEntry)}
    assert "sha256" in fields
    assert fields["sha256"].type is str or fields["sha256"].type == "str"


def test_build_file_entries_computes_sha256_for_known_content(tmp_path: Path) -> None:
    (tmp_path / "hello.txt").write_bytes(b"hello world")
    entries = build_file_entries(tmp_path)
    assert len(entries) == 1
    assert entries[0].sha256 == HELLO_WORLD_SHA256


def test_build_file_entries_differs_for_different_content(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_bytes(b"content alpha")
    (tmp_path / "b.txt").write_bytes(b"content beta")
    entries = build_file_entries(tmp_path)
    hashes = [e.sha256 for e in entries]
    assert hashes[0] != hashes[1]


def test_build_file_entries_matches_for_identical_content(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_bytes(b"same content")
    (tmp_path / "b.txt").write_bytes(b"same content")
    entries = build_file_entries(tmp_path)
    hashes = [e.sha256 for e in entries]
    assert hashes[0] == hashes[1]


def test_build_file_entries_handles_large_file(tmp_path: Path) -> None:
    chunk_size = 65536
    data = bytes(range(256)) * (200 * 1024 // 256)
    assert len(data) > chunk_size
    (tmp_path / "large.bin").write_bytes(data)

    expected = hashlib.sha256(data).hexdigest()
    entries = build_file_entries(tmp_path)
    assert len(entries) == 1
    assert entries[0].sha256 == expected


def test_write_csv_includes_sha256_column(tmp_path: Path) -> None:
    entry = FileEntry(
        relative_path="docs/readme.txt",
        name="readme.txt",
        extension=".txt",
        size_bytes=11,
        modified_utc="2026-01-01T00:00:00+00:00",
        sha256=HELLO_WORLD_SHA256,
        parent_folder="docs",
        top_category="docs",
    )
    out_csv = tmp_path / "out.csv"
    write_csv(out_csv, [entry])

    with out_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    assert "sha256" in headers
    assert headers.index("sha256") == headers.index("modified_utc") + 1
    assert rows[0]["sha256"] == HELLO_WORLD_SHA256
