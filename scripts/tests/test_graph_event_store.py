"""Sprint HP Stream HP.3 — SQLite-backed event-sourced graph store tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.event_store import (
    EventStore,
    GraphEvent,
    project_graph_at,
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
    store = EventStore(db_path=tmp_path / "events.sqlite")
    try:
        store.append(_event(
            1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z",
            payload={"from": "law-pd-1096", "to": "concept-setbacks"},
        ))
        store.append(_event(
            2, kind="PROMOTED", edge_id="rel-b", ts="2026-04-15T10:01:00Z",
            payload={"from": "law-pd-1096", "to": "concept-yards"},
        ))
        assert store.count() == 2
    finally:
        store.close()


def test_append_is_idempotent_on_replay(tmp_path: Path) -> None:
    db = tmp_path / "events.sqlite"
    store = EventStore(db_path=db)
    try:
        store.append(_event(
            1, kind="PROMOTED", edge_id="rel-a",
            ts="2026-04-15T10:00:00Z",
        ))
        store.close()

        # Re-open and re-append the same event_id. Second insert must
        # be a no-op (primary key conflict raises ValueError).
        store2 = EventStore(db_path=db)
        with pytest.raises(ValueError, match="duplicate"):
            store2.append(_event(
                1, kind="PROMOTED", edge_id="rel-a-different",
                ts="2026-04-15T10:05:00Z",
            ))
        assert store2.count() == 1
        store2.close()
    finally:
        pass


def test_project_graph_at_timestamp(tmp_path: Path) -> None:
    store = EventStore(db_path=tmp_path / "events.sqlite")
    try:
        store.append(_event(
            1, kind="PROMOTED", edge_id="rel-a",
            ts="2026-04-15T10:00:00Z",
            payload={"type": "governs", "from": "law-a", "to": "concept-x"},
        ))
        store.append(_event(
            2, kind="PROMOTED", edge_id="rel-b",
            ts="2026-04-15T10:05:00Z",
            payload={"type": "governs", "from": "law-b", "to": "concept-y"},
        ))
        store.append(_event(
            3, kind="REJECTED", edge_id="rel-a",
            ts="2026-04-15T10:10:00Z",
        ))
    finally:
        store.close()

    # As of 10:02 — only rel-a exists (PROMOTED but not yet rejected).
    at_10_02 = project_graph_at(
        db_path=tmp_path / "events.sqlite",
        timestamp_utc="2026-04-15T10:02:00Z",
    )
    assert set(at_10_02.keys()) == {"rel-a"}

    # As of 10:06 — rel-a and rel-b both live.
    at_10_06 = project_graph_at(
        db_path=tmp_path / "events.sqlite",
        timestamp_utc="2026-04-15T10:06:00Z",
    )
    assert set(at_10_06.keys()) == {"rel-a", "rel-b"}

    # As of 10:11 — rel-a was rejected, only rel-b left.
    at_10_11 = project_graph_at(
        db_path=tmp_path / "events.sqlite",
        timestamp_utc="2026-04-15T10:11:00Z",
    )
    assert set(at_10_11.keys()) == {"rel-b"}
