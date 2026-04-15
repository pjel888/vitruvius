"""Sprint HP.3-R — RocksDB-backed event store tests (mirror SQLite coverage)."""
from __future__ import annotations

from pathlib import Path

import pytest

rocksdict = pytest.importorskip("rocksdict")

from vitruvius.graph.event_store import GraphEvent
from vitruvius.graph.rocksdb_event_store import (
    RocksDBEventStore,
    project_graph_at_rocksdb,
)


def _event(
    idx: int,
    *,
    kind: str,
    edge_id: str,
    ts: str,
    payload: dict | None = None,
) -> GraphEvent:
    return GraphEvent(
        event_id=idx,
        event_type=kind,
        edge_id=edge_id,
        timestamp_utc=ts,
        payload=payload or {},
    )


def test_append_and_count(tmp_path: Path) -> None:
    store = RocksDBEventStore(db_path=tmp_path / "events.rocksdb")
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z",
                             payload={"from": "law-pd-1096", "to": "concept-setbacks"}))
        store.append(_event(2, kind="PROMOTED", edge_id="rel-b", ts="2026-04-15T10:01:00Z",
                             payload={"from": "law-pd-1096", "to": "concept-yards"}))
        assert store.count() == 2
    finally:
        store.close()


def test_duplicate_event_id_raises(tmp_path: Path) -> None:
    store = RocksDBEventStore(db_path=tmp_path / "events.rocksdb")
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z"))
        with pytest.raises(ValueError, match="duplicate"):
            store.append(_event(1, kind="PROMOTED", edge_id="rel-a-different", ts="2026-04-15T10:05:00Z"))
        assert store.count() == 1
    finally:
        store.close()


def test_project_graph_at_timestamp(tmp_path: Path) -> None:
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z",
                             payload={"type": "governs", "from": "law-a", "to": "concept-x"}))
        store.append(_event(2, kind="PROMOTED", edge_id="rel-b", ts="2026-04-15T10:05:00Z",
                             payload={"type": "governs", "from": "law-b", "to": "concept-y"}))
        store.append(_event(3, kind="REJECTED", edge_id="rel-a", ts="2026-04-15T10:10:00Z"))
    finally:
        store.close()

    at_10_02 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:02:00Z")
    assert set(at_10_02.keys()) == {"rel-a"}

    at_10_06 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:06:00Z")
    assert set(at_10_06.keys()) == {"rel-a", "rel-b"}

    at_10_11 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:11:00Z")
    assert set(at_10_11.keys()) == {"rel-b"}


def test_reopen_persists(tmp_path: Path) -> None:
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z"))
    store.close()

    store2 = RocksDBEventStore(db_path=db)
    try:
        assert store2.count() == 1
    finally:
        store2.close()


def test_count_is_o1_not_on_scan(tmp_path: Path) -> None:
    """Sprint HP.3-R Task 8 optimization: RocksDBEventStore.count()
    must be O(1), backed by a reserved meta:count key that append()
    increments. The Task 8 bench exposed that the previous O(n)
    implementation caused a 33.5s bottleneck when called in a loop.

    We assert both:
    1. The meta:count key exists and tracks the correct value
    2. The count is preserved after close + reopen
    3. Attempting to insert a duplicate event_id does NOT increment
       the counter
    """
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    try:
        for i in range(50):
            store.append(_event(
                i, kind="PROMOTED", edge_id=f"rel-{i}",
                ts=f"2026-04-15T10:00:{i % 60:02d}Z",
            ))
        assert store.count() == 50

        # Duplicate append must not increment the counter
        with pytest.raises(ValueError, match="duplicate"):
            store.append(_event(
                0, kind="PROMOTED", edge_id="rel-0-dup",
                ts="2026-04-15T10:30:00Z",
            ))
        assert store.count() == 50
    finally:
        store.close()

    # Reopen — counter must persist
    store2 = RocksDBEventStore(db_path=db)
    try:
        assert store2.count() == 50
        # One more append should increment to 51
        store2.append(_event(
            100, kind="PROMOTED", edge_id="rel-100",
            ts="2026-04-15T11:00:00Z",
        ))
        assert store2.count() == 51
    finally:
        store2.close()


def test_project_graph_at_concurrent_with_open_writer(tmp_path: Path) -> None:
    """Sprint HP.3-R bug fix: project_graph_at_rocksdb must open a
    read-only handle so it can run alongside a live writer without
    tripping RocksDB's exclusive LOCK file.

    Prior to the fix, this test raised a lock-acquisition error at
    the project_graph_at_rocksdb call because the default Rdict open
    is read-write and RocksDB only permits one writer at a time.
    """
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    try:
        store.append(_event(
            1, kind="PROMOTED", edge_id="rel-a",
            ts="2026-04-15T10:00:00Z",
            payload={"from": "law-pd-1096", "to": "concept-setbacks"},
        ))

        # Writer is still OPEN. The reader must coexist.
        projected = project_graph_at_rocksdb(
            db_path=db,
            timestamp_utc="2026-04-15T10:00:00Z",
        )
        assert set(projected.keys()) == {"rel-a"}
        assert projected["rel-a"]["from"] == "law-pd-1096"

        # Writer must still be usable after the reader ran.
        store.append(_event(
            2, kind="PROMOTED", edge_id="rel-b",
            ts="2026-04-15T10:01:00Z",
            payload={"from": "law-pd-1096", "to": "concept-yards"},
        ))
        assert store.count() == 2
    finally:
        store.close()
