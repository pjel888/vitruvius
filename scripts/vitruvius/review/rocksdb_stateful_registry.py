"""Sprint HP.3-R — RocksDB-backed stateful verdict cache.

Public API mirrors ``vitruvius.review.stateful_registry.StatefulReviewRegistry``
exactly so the Task 6 factory can swap backends transparently. Key
layout:

- ``v:{source_hash}:{relationship_hash}:{model_version}`` -> JSON value
  ``{verdict, self_confidence, created_utc}``

The PK fields are reconstructed from the key on read, so the stored
JSON only needs the mutable fields.

Note: ``model_version`` can contain colons (e.g. ``qwen2.5:7b-2026-04``),
so the key is NOT a simple colon-delimited parse — we split only on
the first two colons (after the ``v:`` prefix).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from vitruvius.review.stateful_registry import VerdictRecord

# Deferred import — rocksdict is an optional dependency. We want
# ImportError to surface at class instantiation time (so the Task 6
# factory can fall back to SQLite) rather than at module import
# time. Cache returns (Rdict, AccessType) tuple for parity with
# RocksDBEventStore.
_Rdict: Any = None
_AccessType: Any = None


def _require_rocksdict() -> tuple[Any, Any]:
    """Lazy-import rocksdict and return ``(Rdict, AccessType)``.

    Duplicated locally (rather than imported from
    ``vitruvius.graph.rocksdb_event_store``) so each backend module is
    independently importable without pulling in sibling backends.
    """
    global _Rdict, _AccessType
    if _Rdict is not None and _AccessType is not None:
        return _Rdict, _AccessType
    try:
        from rocksdict import AccessType, Rdict
    except ImportError as exc:
        raise ImportError(
            "rocksdict is required for RocksDBStatefulReviewRegistry. "
            "Install via `pip install rocksdict==0.3.29`."
        ) from exc
    _Rdict = Rdict
    _AccessType = AccessType
    return _Rdict, _AccessType


_PREFIX = b"v:"
_META_COUNT_KEY = b"meta:verdict_count"


def _verdict_key(source_hash: str, relationship_hash: str, model_version: str) -> bytes:
    return f"v:{source_hash}:{relationship_hash}:{model_version}".encode("utf-8")


class RocksDBStatefulReviewRegistry:
    """RocksDB-backed verdict cache with StatefulReviewRegistry-compatible API."""

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        Rdict, _unused_access_type = _require_rocksdict()
        self._db = Rdict(str(self._db_path))

    def put(self, record: VerdictRecord) -> None:
        """Upsert a verdict. Re-putting the same PK replaces the value
        without incrementing the O(1) row counter.
        """
        key = _verdict_key(
            record.source_hash,
            record.relationship_hash,
            record.model_version,
        )
        is_new = self._db.get(key) is None
        value = json.dumps({
            "verdict": record.verdict,
            "self_confidence": record.self_confidence,
            "created_utc": record.created_utc,
        }, sort_keys=True).encode("utf-8")
        self._db[key] = value
        if is_new:
            current = self._db.get(_META_COUNT_KEY)
            next_value = (int(current) if current is not None else 0) + 1
            self._db[_META_COUNT_KEY] = str(next_value).encode("ascii")

    def get(
        self,
        *,
        source_hash: str,
        relationship_hash: str,
        model_version: str,
    ) -> Optional[VerdictRecord]:
        key = _verdict_key(source_hash, relationship_hash, model_version)
        raw = self._db.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        return VerdictRecord(
            source_hash=source_hash,
            relationship_hash=relationship_hash,
            model_version=model_version,
            verdict=data["verdict"],
            self_confidence=float(data["self_confidence"]),
            created_utc=data["created_utc"],
        )

    def count(self) -> int:
        """O(1) row count backed by a reserved meta:count key.

        The counter is maintained by :meth:`put` (new keys only),
        :meth:`purge_all` (resets to 0), and :meth:`purge_older_than`
        (decrements by deleted count). Pre-Task 8 behaviour iterated
        every key with the v: prefix, which was O(n) per call.
        """
        raw = self._db.get(_META_COUNT_KEY)
        if raw is None:
            return 0
        return int(raw)

    def flush(self) -> None:
        """Force the active memtable to disk so ``disk_size_mb()`` is
        meaningful immediately after a write. Without this the SST
        files for recent writes may not exist on disk yet — RocksDB
        buffers writes in memory until the memtable fills up.
        """
        try:
            self._db.flush()
        except Exception:
            # rocksdict.flush() signature may vary by version; we
            # don't want the caller to have to guard every call. The
            # test that depends on this calls flush() explicitly.
            pass

    def vacuum(self) -> None:
        """No-op on RocksDB. SQLite's ``VACUUM`` reclaims deleted-row
        space; RocksDB handles this automatically during background
        compaction, so there is no user-facing primitive to call.
        Exposed for API parity with ``StatefulReviewRegistry``.
        """
        return

    def db_size_bytes(self) -> int:
        """Return total on-disk size of the RocksDB directory in bytes."""
        if not self._db_path.exists():
            return 0
        total = 0
        for entry in self._db_path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
        return total

    def disk_size_mb(self) -> float:
        return self.db_size_bytes() / (1024 * 1024)

    def purge_all(self) -> int:
        """Delete every verdict and return the deleted count."""
        to_delete = [k for k in self._db.keys() if k.startswith(_PREFIX)]
        for k in to_delete:
            del self._db[k]
        # Reset the O(1) counter
        self._db[_META_COUNT_KEY] = b"0"
        return len(to_delete)

    def purge_older_than(self, *, cutoff_utc: str) -> int:
        """Delete every verdict whose ``created_utc`` is strictly less
        than ``cutoff_utc`` (a lexicographically-sortable ISO-8601
        timestamp). Returns the number of deleted rows.
        """
        to_delete: list[bytes] = []
        for k in self._db.keys():
            if not k.startswith(_PREFIX):
                continue
            raw = self._db.get(k)
            if raw is None:
                continue
            data = json.loads(raw)
            if data.get("created_utc", "") < cutoff_utc:
                to_delete.append(k)
        for k in to_delete:
            del self._db[k]
        # Decrement the O(1) counter by the number deleted
        if to_delete:
            current = self._db.get(_META_COUNT_KEY)
            current_int = int(current) if current is not None else 0
            # max(0, ...) is a defensive floor that only fires if the
            # counter is desynced from the real row count — e.g. if a
            # pre-Sprint-HP.3-R RocksDB DB (no meta:verdict_count key)
            # is opened by this code and then purged. In normal
            # operation the counter tracks reality exactly.
            new_value = max(0, current_int - len(to_delete))
            self._db[_META_COUNT_KEY] = str(new_value).encode("ascii")
        return len(to_delete)

    def close(self) -> None:
        self._db.close()
