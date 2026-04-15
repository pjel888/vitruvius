"""Sprint HP Stream HP.3 — SQLite-backed event-sourced graph store.

An append-only event log keyed by ``event_id`` (caller-assigned,
typically monotonic). Each row records a graph lifecycle event
(``PROMOTED`` / ``REJECTED`` / ``AMENDED``) plus a free-form JSON
payload with the edge's fields at the time of the event.

The :func:`project_graph_at` helper replays the log up to a given
UTC timestamp and returns a dict ``{edge_id: latest_event_payload}``
so the caller can reconstruct the graph state at any historical
point.

The plan originally specified RocksDB; we use stdlib ``sqlite3``
instead because no pre-built python-rocksdb wheel was available on
this host. SQLite's WAL mode gives the same atomic-append semantics
and the on-disk file is git-tracked alongside the rest of the
project.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class GraphEvent:
    event_id: int
    event_type: str  # "PROMOTED" | "REJECTED" | "AMENDED"
    edge_id: str
    timestamp_utc: str
    payload: Mapping[str, Any] = field(default_factory=dict)


class EventStore:
    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS graph_events (
        event_id      INTEGER PRIMARY KEY,
        event_type    TEXT NOT NULL,
        edge_id       TEXT NOT NULL,
        timestamp_utc TEXT NOT NULL,
        payload_json  TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS graph_events_edge_ts
        ON graph_events(edge_id, timestamp_utc);
    """

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.executescript(self._SCHEMA)
        self._conn.commit()

    def append(self, event: GraphEvent) -> None:
        """Insert a new event. Raises :class:`ValueError` if the
        ``event_id`` already exists — events are immutable."""
        try:
            self._conn.execute(
                "INSERT INTO graph_events "
                "(event_id, event_type, edge_id, timestamp_utc, payload_json) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    event.event_id,
                    event.event_type,
                    event.edge_id,
                    event.timestamp_utc,
                    json.dumps(dict(event.payload), sort_keys=True),
                ),
            )
            self._conn.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"duplicate event_id {event.event_id} — event log is "
                f"append-only, prior event cannot be overwritten"
            ) from exc

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM graph_events").fetchone()
        return int(row[0])

    def close(self) -> None:
        self._conn.close()


def project_graph_at(
    *,
    db_path: Path,
    timestamp_utc: str,
) -> dict[str, dict[str, Any]]:
    """Replay every event in ``db_path`` up to and including
    ``timestamp_utc`` and return the resulting graph state.

    Return value is ``{edge_id: latest_payload}``. Edges that have
    been REJECTED (or whose last event at ``timestamp_utc`` is a
    REJECTED event) are excluded.

    Opens a fresh read-only connection so this function can run
    concurrently with an open :class:`EventStore` writer.
    """
    conn = sqlite3.connect(Path(db_path))
    try:
        rows = conn.execute(
            "SELECT event_id, event_type, edge_id, timestamp_utc, payload_json "
            "FROM graph_events "
            "WHERE timestamp_utc <= ? "
            "ORDER BY timestamp_utc ASC, event_id ASC",
            (timestamp_utc,),
        ).fetchall()
    finally:
        conn.close()

    state: dict[str, dict[str, Any]] = {}
    for _event_id, event_type, edge_id, _ts, payload_json in rows:
        if event_type == "REJECTED":
            state.pop(edge_id, None)
            continue
        payload = json.loads(payload_json) if payload_json else {}
        if event_type in {"PROMOTED", "AMENDED"}:
            state[edge_id] = payload
    return state


# ---------------------------------------------------------------------------
# Stream S3.1 — Delta wrapper for the differential dataflow engine.
# ---------------------------------------------------------------------------

from dataclasses import asdict
from typing import Literal

DeltaKind = Literal["upsert", "delete"]


@dataclass(frozen=True)
class Delta:
    """A single immutable change recorded in the event store.

    The differential propagator (Stream S3.3) consumes Deltas and walks the
    dependency tracker (Stream S3.2) to enumerate downstream consumers.
    """

    event_id: str
    edge_id: str
    kind: DeltaKind
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in ("upsert", "delete"):
            raise ValueError(f"Delta.kind must be 'upsert' or 'delete', got {self.kind!r}")
        if not self.event_id:
            raise ValueError("Delta.event_id must be non-empty")
        if not self.edge_id:
            raise ValueError("Delta.edge_id must be non-empty")

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> "Delta":
        data = json.loads(raw)
        return cls(
            event_id=data["event_id"],
            edge_id=data["edge_id"],
            kind=data["kind"],
            payload=data.get("payload", {}),
        )
