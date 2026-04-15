"""Sprint HP.3-R — ple-kv-migrate CLI tests.

Covers: event store migration (end-to-end), idempotency on re-run,
verdict cache migration, dry-run does not write.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.event_store import EventStore, GraphEvent
from vitruvius.kv_migrate import run_kv_migrate
from vitruvius.review.stateful_registry import StatefulReviewRegistry, VerdictRecord


def test_migrate_event_store_copies_all_events(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    for i in range(5):
        src_store.append(GraphEvent(
            event_id=i,
            event_type="PROMOTED",
            edge_id=f"rel-{i}",
            timestamp_utc=f"2026-04-15T10:00:{i:02d}Z",
            payload={"n": i},
        ))
    src_store.close()

    rc = run_kv_migrate(store="event", source=src, dest=dest, dry_run=False)
    assert rc == 0

    dest_store = RocksDBEventStore(db_path=dest)
    try:
        assert dest_store.count() == 5
    finally:
        dest_store.close()


def test_migrate_event_store_is_idempotent(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    src_store.append(GraphEvent(
        event_id=42, event_type="PROMOTED", edge_id="rel-x",
        timestamp_utc="2026-04-15T10:00:00Z", payload={},
    ))
    src_store.close()

    # First migration.
    assert run_kv_migrate(store="event", source=src, dest=dest, dry_run=False) == 0
    # Second migration against the same dest must not double-write.
    assert run_kv_migrate(store="event", source=src, dest=dest, dry_run=False) == 0

    dest_store = RocksDBEventStore(db_path=dest)
    try:
        assert dest_store.count() == 1
    finally:
        dest_store.close()


def test_migrate_registry_copies_all_verdicts(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry

    src = tmp_path / "reg.sqlite"
    dest = tmp_path / "reg.rocksdb"

    src_reg = StatefulReviewRegistry(db_path=src)
    src_reg.put(VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    ))
    src_reg.close()

    rc = run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False)
    assert rc == 0

    dest_reg = RocksDBStatefulReviewRegistry(db_path=dest)
    try:
        assert dest_reg.count() == 1
        record = dest_reg.get(source_hash="s", relationship_hash="r", model_version="m:v1")
        assert record is not None
        assert record.verdict == "keep"
        assert record.self_confidence == 0.9
    finally:
        dest_reg.close()


def test_migrate_dry_run_does_not_write(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    src_store.append(GraphEvent(
        event_id=1, event_type="PROMOTED", edge_id="rel-x",
        timestamp_utc="2026-04-15T10:00:00Z", payload={},
    ))
    src_store.close()

    rc = run_kv_migrate(store="event", source=src, dest=dest, dry_run=True)
    assert rc == 0
    # Dry-run must not create the dest directory.
    assert not dest.exists()


def test_migrate_registry_is_idempotent(tmp_path: Path) -> None:
    """Sprint HP.3-R Task 7 supplement: re-running the registry
    migration against a populated destination must report the
    second-run rows as ``skipped (idempotent)`` rather than silently
    overwriting them — mirrors the event-store idempotency behaviour.
    """
    pytest.importorskip("rocksdict")
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry

    src = tmp_path / "reg.sqlite"
    dest = tmp_path / "reg.rocksdb"

    src_reg = StatefulReviewRegistry(db_path=src)
    src_reg.put(VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    ))
    src_reg.close()

    # First run.
    assert run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False) == 0

    # Second run against the same dest must not double-write.
    assert run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False) == 0

    dest_reg = RocksDBStatefulReviewRegistry(db_path=dest)
    try:
        # Still exactly 1 verdict after two runs.
        assert dest_reg.count() == 1
    finally:
        dest_reg.close()


def test_migrate_registry_reports_skipped_on_rerun(tmp_path: Path, capsys) -> None:
    """Sprint HP.3-R Task 7 supplement: the operator-visible print
    on a re-run must explicitly report ``skipped (idempotent)`` so
    the operator can distinguish a first-time migration from a
    redundant re-run.
    """
    pytest.importorskip("rocksdict")

    src = tmp_path / "reg.sqlite"
    dest = tmp_path / "reg.rocksdb"

    src_reg = StatefulReviewRegistry(db_path=src)
    src_reg.put(VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    ))
    src_reg.close()

    # First run: 1 copied, 0 skipped.
    assert run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False) == 0
    out_first = capsys.readouterr().out
    assert "1 verdicts copied" in out_first
    assert "0 skipped" in out_first

    # Second run: 0 copied, 1 skipped.
    assert run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False) == 0
    out_second = capsys.readouterr().out
    assert "0 verdicts copied" in out_second
    assert "1 skipped" in out_second
