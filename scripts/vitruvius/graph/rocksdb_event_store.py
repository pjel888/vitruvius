"""Sprint HP.3-R — RocksDB-backed event-sourced graph store.

Public API mirrors ``vitruvius.graph.event_store.EventStore`` exactly so
the factory in Task 6 can swap backends transparently. Key layout:

- ``event:{event_id:010d}`` -> JSON payload (primary record)
- ``ts:{timestamp_utc}:{event_id:010d}`` -> b"{event_id:010d}"
  (secondary index for time-travel projection)

Duplicate detection uses ``db.get(primary_key)`` before write. ``count()``
iterates primary keys — at current scale (<10k events) this is cheap.
Optimize via a reserved ``meta:count`` key if the Task 8 bench shows
it's hot.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vitruvius.graph.event_store import GraphEvent

# Deferred import — rocksdict is an optional dependency. We want
# ImportError to surface at class instantiation time (so the Task 6
# factory can fall back to SQLite) rather than at module import
# time, so downstream consumers that never construct a
# RocksDBEventStore don't pay for an unavailable native lib.
_Rdict: Any = None
_AccessType: Any = None


def _require_rocksdict() -> tuple[Any, Any]:
    """Lazy-import rocksdict and return ``(Rdict, AccessType)``.

    rocksdict is an optional dependency. We want ImportError to
    surface at class instantiation / function call time (so the
    Task 6 factory can fall back to SQLite) rather than at module
    import time.
    """
    global _Rdict, _AccessType
    if _Rdict is not None and _AccessType is not None:
        return _Rdict, _AccessType
    try:
        from rocksdict import AccessType, Rdict
    except ImportError as exc:
        raise ImportError(
            "rocksdict is required for RocksDBEventStore. "
            "Install via `pip install rocksdict==0.3.29`."
        ) from exc
    _Rdict = Rdict
    _AccessType = AccessType
    return _Rdict, _AccessType


_EVENT_PREFIX = b"event:"
_TS_PREFIX = b"ts:"
_META_COUNT_KEY = b"meta:event_count"


def _event_key(event_id: int) -> bytes:
    return f"event:{event_id:010d}".encode("ascii")


def _ts_key(timestamp_utc: str, event_id: int) -> bytes:
    return f"ts:{timestamp_utc}:{event_id:010d}".encode("ascii")


class RocksDBEventStore:
    """RocksDB-backed event log with ``EventStore``-compatible API."""

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        Rdict, _unused_access_type = _require_rocksdict()
        self._db = Rdict(str(self._db_path))

    def append(self, event: GraphEvent) -> None:
        primary = _event_key(event.event_id)
        if self._db.get(primary) is not None:
            raise ValueError(
                f"duplicate event_id {event.event_id} — event log is "
                f"append-only, prior event cannot be overwritten"
            )
        value = json.dumps({
            "event_type": event.event_type,
            "edge_id": event.edge_id,
            "timestamp_utc": event.timestamp_utc,
            "payload": dict(event.payload),
        }, sort_keys=True).encode("utf-8")
        self._db[primary] = value
        self._db[_ts_key(event.timestamp_utc, event.event_id)] = (
            f"{event.event_id:010d}".encode("ascii")
        )
        # Sprint HP.3-R Task 8 optimization: maintain an O(1) count
        # so count() doesn't have to scan every key.
        current = self._db.get(_META_COUNT_KEY)
        next_value = (int(current) if current is not None else 0) + 1
        self._db[_META_COUNT_KEY] = str(next_value).encode("ascii")

    def count(self) -> int:
        """O(1) row count backed by a reserved meta:count key.

        The counter is maintained by :meth:`append` — each successful
        insert increments the value, duplicate rejections do not.
        Pre-Task 8 behaviour iterated every key with the event:
        prefix, which was O(n) per call and caused a 33.5s bottleneck
        in the Task 8 bench when called in a loop.
        """
        raw = self._db.get(_META_COUNT_KEY)
        if raw is None:
            return 0
        return int(raw)

    def close(self) -> None:
        self._db.close()


def project_graph_at_rocksdb(
    *,
    db_path: Path,
    timestamp_utc: str,
) -> dict[str, dict[str, Any]]:
    """Replay every event in the RocksDB store up to (and including)
    ``timestamp_utc`` and return ``{edge_id: latest_payload}``.

    Mirrors ``vitruvius.graph.event_store.project_graph_at`` semantics
    exactly:
    - Events are walked in ``(timestamp_utc ASC, event_id ASC)`` order
      using the ``ts:`` secondary index.
    - ``REJECTED`` events remove the edge from the projected state.
    - ``PROMOTED`` / ``AMENDED`` events upsert the edge.

    Opens a read-only RocksDB handle via ``AccessType.read_only()`` so
    it can run concurrently with an open :class:`RocksDBEventStore`
    writer — RocksDB permits unlimited concurrent read-only handles
    alongside a single writer via the LOCK file. A plain
    ``Rdict(path)`` call would trip the exclusive lock.
    """
    Rdict, AccessType = _require_rocksdict()
    db = Rdict(str(Path(db_path)), access_type=AccessType.read_only())
    try:
        state: dict[str, dict[str, Any]] = {}
        cutoff = timestamp_utc.encode("ascii")

        # Gather the (ts_key, primary_key) pairs we need to walk, in
        # order. The ts: secondary index is lex-sorted so iterating
        # RocksDB keys in natural order gives us chronological order
        # for free.
        ordered_ts_keys: list[bytes] = []
        for key in db.keys():
            if not key.startswith(_TS_PREFIX):
                continue
            # ts:<timestamp>:<event_id> — the timestamp itself
            # contains ``:`` characters (``HH:MM:SS``), so we split on
            # the LAST colon: left = full timestamp, right = event_id.
            # We want every key whose timestamp segment is <= cutoff.
            rest = key[len(_TS_PREFIX):]
            ts_segment, _sep, _tail = rest.rpartition(b":")
            if ts_segment > cutoff:
                continue
            ordered_ts_keys.append(key)

        ordered_ts_keys.sort()

        for ts_key in ordered_ts_keys:
            event_id_bytes = db[ts_key]
            primary = _EVENT_PREFIX + event_id_bytes
            raw = db.get(primary)
            if raw is None:
                continue
            record = json.loads(raw)
            edge_id = record["edge_id"]
            event_type = record["event_type"]
            if event_type == "REJECTED":
                state.pop(edge_id, None)
                continue
            if event_type in {"PROMOTED", "AMENDED"}:
                state[edge_id] = record["payload"]

        return state
    finally:
        db.close()
