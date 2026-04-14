"""Stream O.3 — content-hash duplicate detector stub tests."""
from __future__ import annotations

from pathlib import Path

from vitruvius.foraging.duplicate_detector import (
    DuplicateReport,
    find_duplicate,
    hash_document_content,
)


def test_hash_is_deterministic() -> None:
    a = hash_document_content(b"hello world")
    b = hash_document_content(b"hello world")
    assert a == b
    assert len(a) == 64  # sha256 hex


def test_hash_changes_with_content() -> None:
    a = hash_document_content(b"hello")
    b = hash_document_content(b"hello!")
    assert a != b


def test_find_duplicate_hit(tmp_path: Path) -> None:
    existing = tmp_path / "existing.md"
    existing.write_bytes(b"sample document body")
    incoming = b"sample document body"
    report = find_duplicate(incoming, [existing])
    assert isinstance(report, DuplicateReport)
    assert report.is_duplicate is True
    assert report.matched_path == existing


def test_find_duplicate_miss(tmp_path: Path) -> None:
    existing = tmp_path / "existing.md"
    existing.write_bytes(b"sample document body")
    incoming = b"different body entirely"
    report = find_duplicate(incoming, [existing])
    assert report.is_duplicate is False
    assert report.matched_path is None


def test_find_duplicate_empty_corpus() -> None:
    report = find_duplicate(b"any bytes", [])
    assert report.is_duplicate is False
    assert report.matched_path is None
