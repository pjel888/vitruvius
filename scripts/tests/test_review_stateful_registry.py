"""Stream Y4.1 — SQLite stateful review registry tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.review.stateful_registry import (
    StatefulReviewRegistry,
    VerdictRecord,
)


def test_put_and_get_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)

    record = VerdictRecord(
        source_hash="src_abc",
        relationship_hash="rel_123",
        model_version="qwen2.5:7b-2026-04",
        verdict="keep",
        self_confidence=0.88,
        created_utc="2026-04-14T20:00:00Z",
    )
    reg.put(record)

    fetched = reg.get(
        source_hash="src_abc",
        relationship_hash="rel_123",
        model_version="qwen2.5:7b-2026-04",
    )
    assert fetched == record


def test_get_miss_returns_none(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    assert reg.get(source_hash="x", relationship_hash="y", model_version="z") is None


def test_model_version_scoping(tmp_path: Path) -> None:
    """Different model versions must create separate entries."""
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)

    r_v1 = VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    )
    r_v2 = VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v2",
        verdict="reject", self_confidence=0.85, created_utc="2026-04-14T00:00:00Z",
    )
    reg.put(r_v1)
    reg.put(r_v2)

    assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v1") == r_v1
    assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v2") == r_v2


def test_count_and_vacuum(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    for i in range(5):
        reg.put(VerdictRecord(
            source_hash=f"s{i}",
            relationship_hash="r",
            model_version="m",
            verdict="keep",
            self_confidence=0.9,
            created_utc="2026-04-14T00:00:00Z",
        ))
    assert reg.count() == 5
    reg.vacuum()  # must not raise
    assert reg.count() == 5
