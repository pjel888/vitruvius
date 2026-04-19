"""Tests for backfill_document_versions.py."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backfill_document_versions import (
    backfill_canonical_sources,
    backfill_raw_sources,
)


class FakePostgresClient:
    """In-memory stand-in for PostgresClient."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def insert_document_version(self, record: dict[str, Any]) -> None:
        self.records.append(record)

    def verify_connectivity(self) -> bool:
        return True

    def close(self) -> None:
        pass


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    canonical = repo / "003_Canonical-Knowledge-Layer" / "shared"

    # Canonical source
    sources_dir = canonical / "sources"
    sources_dir.mkdir(parents=True)
    (sources_dir / "law-pd-1096.md").write_text(
        "---\n"
        "id: law-pd-1096-national-building-code\n"
        "title: National Building Code of the Philippines\n"
        "trust_level: primary\n"
        "canonical_status: draft\n"
        "---\n\n"
        "# National Building Code\n"
    )

    # Raw source
    raw_dir = repo / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096"
    raw_dir.mkdir(parents=True)
    (raw_dir / "nbc.pdf").write_text("fake pdf content")

    return repo


class TestBackfillCanonicalSources:
    def test_backfill_creates_record(self, fake_repo: Path) -> None:
        pg = FakePostgresClient()
        canonical_root = fake_repo / "003_Canonical-Knowledge-Layer" / "shared"
        count = backfill_canonical_sources(pg, canonical_root)

        assert count == 1
        assert len(pg.records) == 1
        rec = pg.records[0]
        assert rec["id"] == "docv-law-pd-1096-national-building-code-v1"
        assert rec["document_id"] == "doc-law-pd-1096-national-building-code"
        assert rec["title"] == "National Building Code of the Philippines"
        assert rec["mime_type"] == "text/markdown"
        assert len(rec["sha256"]) == 64

    def test_missing_dir_warns(self, tmp_path: Path) -> None:
        pg = FakePostgresClient()
        count = backfill_canonical_sources(pg, tmp_path / "nonexistent")
        assert count == 0


class TestBackfillRawSources:
    def test_backfill_creates_record(self, fake_repo: Path) -> None:
        pg = FakePostgresClient()
        raw_root = fake_repo / "001_Raw-Source-Layer"
        count = backfill_raw_sources(pg, raw_root)

        assert count == 1
        assert len(pg.records) == 1
        rec = pg.records[0]
        assert rec["document_id"] == "doc-nbc"
        assert rec["mime_type"] == "application/pdf"
        assert len(rec["sha256"]) == 64

    def test_missing_dir_warns(self, tmp_path: Path) -> None:
        pg = FakePostgresClient()
        count = backfill_raw_sources(pg, tmp_path / "nonexistent")
        assert count == 0
