"""Sprint HP.3-R — RocksDB stateful review registry tests (mirror SQLite coverage)."""
from __future__ import annotations

from pathlib import Path

import pytest

rocksdict = pytest.importorskip("rocksdict")

from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry
from vitruvius.review.stateful_registry import VerdictRecord


def test_put_and_get_roundtrip(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        record = VerdictRecord(
            source_hash="src_abc", relationship_hash="rel_123",
            model_version="qwen2.5:7b-2026-04",
            verdict="keep", self_confidence=0.88,
            created_utc="2026-04-14T20:00:00Z",
        )
        reg.put(record)
        fetched = reg.get(
            source_hash="src_abc", relationship_hash="rel_123",
            model_version="qwen2.5:7b-2026-04",
        )
        assert fetched == record
    finally:
        reg.close()


def test_get_miss_returns_none(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        assert reg.get(source_hash="x", relationship_hash="y", model_version="z") is None
    finally:
        reg.close()


def test_model_version_scoping(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        r_v1 = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:v1",
                             verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z")
        r_v2 = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:v2",
                             verdict="reject", self_confidence=0.85, created_utc="2026-04-14T00:00:00Z")
        reg.put(r_v1)
        reg.put(r_v2)
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v1") == r_v1
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v2") == r_v2
    finally:
        reg.close()


def test_count_and_vacuum_noop(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        for i in range(5):
            reg.put(VerdictRecord(
                source_hash=f"s{i}", relationship_hash="r", model_version="m",
                verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
            ))
        assert reg.count() == 5
        reg.vacuum()  # must be a safe no-op
        assert reg.count() == 5
    finally:
        reg.close()


def test_purge_older_than(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        old = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:old",
                            verdict="keep", self_confidence=0.9, created_utc="2026-01-01T00:00:00Z")
        new = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:new",
                            verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z")
        reg.put(old)
        reg.put(new)
        assert reg.count() == 2

        deleted = reg.purge_older_than(cutoff_utc="2026-03-01T00:00:00Z")
        assert deleted == 1
        assert reg.count() == 1
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:new") == new
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:old") is None
    finally:
        reg.close()


def test_purge_all(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        for i in range(3):
            reg.put(VerdictRecord(
                source_hash=f"s{i}", relationship_hash="r", model_version="m",
                verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
            ))
        deleted = reg.purge_all()
        assert deleted == 3
        assert reg.count() == 0
    finally:
        reg.close()


def test_disk_size_mb_nonzero_after_write(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        reg.put(VerdictRecord(
            source_hash="s", relationship_hash="r", model_version="m",
            verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
        ))
        # RocksDB writes are buffered; flush so the SST files exist.
        reg.flush()
        assert reg.disk_size_mb() > 0.0
    finally:
        reg.close()
