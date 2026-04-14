"""Stream W3.2 — linter rejects concepts missing stringency_vector."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.linting import lint_concept_file


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_lint_accepts_valid_stringency(tmp_path: Path) -> None:
    path = tmp_path / "doors.md"
    _write(path, (
        "---\n"
        "id: concept-doors\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "stringency_vector: maximize\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# doors\n"
    ))
    issues = lint_concept_file(path)
    assert [i for i in issues if i.code == "missing_stringency_vector"] == []


def test_lint_rejects_missing_stringency(tmp_path: Path) -> None:
    path = tmp_path / "doors.md"
    _write(path, (
        "---\n"
        "id: concept-doors\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# doors\n"
    ))
    issues = lint_concept_file(path)
    assert any(i.code == "missing_stringency_vector" for i in issues)


def test_lint_rejects_invalid_stringency_value(tmp_path: Path) -> None:
    path = tmp_path / "doors.md"
    _write(path, (
        "---\n"
        "id: concept-doors\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "stringency_vector: flexible\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# doors\n"
    ))
    issues = lint_concept_file(path)
    assert any(i.code == "invalid_stringency_vector" for i in issues)
