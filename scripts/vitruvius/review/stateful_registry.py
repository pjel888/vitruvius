"""Stream Y4.1 — SQLite-backed persistent verdict cache.

Keyed by ``(source_hash, relationship_hash, model_version)``. On
re-runs, the pipeline skips the LLM entirely for any candidate whose
verdict is already cached under the current model_version. Closes the
Phase 6A Resume gap at the root.

Principle P3 note: this module introduces persistent state. That
state is (a) opt-in via ``features.y_stateful_registry``, (b)
flushable via the ``ple-registry-purge`` CLI (Y4.3), (c) separately
versioned from code via the ``model_version`` key, (d) never read
outside this module.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class VerdictRecord:
    source_hash: str
    relationship_hash: str
    model_version: str
    verdict: str
    self_confidence: float
    created_utc: str


class StatefulReviewRegistry:
    """SQLite-backed cache of LLM review verdicts.

    Instances hold an open connection; call :meth:`close` when done.
    The registry is safe to instantiate multiple times against the
    same ``db_path`` — SQLite handles concurrent readers fine, and
    the primary-key UPSERT in :meth:`put` makes writes idempotent.
    """

    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS verdicts (
        source_hash       TEXT NOT NULL,
        relationship_hash TEXT NOT NULL,
        model_version     TEXT NOT NULL,
        verdict           TEXT NOT NULL,
        self_confidence   REAL NOT NULL,
        created_utc       TEXT NOT NULL,
        PRIMARY KEY (source_hash, relationship_hash, model_version)
    );
    """

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute(self._SCHEMA)
        self._conn.commit()

    def put(self, record: VerdictRecord) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO verdicts "
            "(source_hash, relationship_hash, model_version, verdict, self_confidence, created_utc) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                record.source_hash,
                record.relationship_hash,
                record.model_version,
                record.verdict,
                record.self_confidence,
                record.created_utc,
            ),
        )
        self._conn.commit()

    def get(
        self,
        *,
        source_hash: str,
        relationship_hash: str,
        model_version: str,
    ) -> Optional[VerdictRecord]:
        row = self._conn.execute(
            "SELECT source_hash, relationship_hash, model_version, "
            "verdict, self_confidence, created_utc "
            "FROM verdicts "
            "WHERE source_hash=? AND relationship_hash=? AND model_version=?",
            (source_hash, relationship_hash, model_version),
        ).fetchone()
        if row is None:
            return None
        return VerdictRecord(*row)

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM verdicts").fetchone()
        return int(row[0])

    def db_size_bytes(self) -> int:
        """Return the on-disk size of the SQLite file in bytes."""
        try:
            return self._db_path.stat().st_size
        except FileNotFoundError:
            return 0

    def vacuum(self) -> None:
        """Run ``VACUUM`` on the underlying connection.

        Called by the Y4.3 ``ple-registry-purge`` CLI after a bulk
        delete to reclaim disk space.
        """
        self._conn.execute("VACUUM")
        self._conn.commit()

    def purge_all(self) -> int:
        """Delete every row from the registry and return the deleted count."""
        before = self.count()
        self._conn.execute("DELETE FROM verdicts")
        self._conn.commit()
        return before

    def purge_older_than(self, *, cutoff_utc: str) -> int:
        """Stream Y4.3 — delete every row whose ``created_utc`` is
        strictly less than ``cutoff_utc`` (a lexicographically-sortable
        ISO-8601 timestamp). Returns the number of rows deleted.
        """
        cursor = self._conn.execute(
            "DELETE FROM verdicts WHERE created_utc < ?",
            (cutoff_utc,),
        )
        self._conn.commit()
        return int(cursor.rowcount)

    def disk_size_mb(self) -> float:
        """Stream Y4.3 — return the on-disk size of the SQLite file in MB."""
        try:
            return self._db_path.stat().st_size / (1024 * 1024)
        except FileNotFoundError:
            return 0.0

    def close(self) -> None:
        self._conn.close()


def run_ple_registry_purge(
    *,
    db_path: Path,
    days: int = 30,
) -> int:
    """Stream Y4.3 — CLI handler for the ``ple-registry-purge`` subcommand.

    Deletes every row older than ``days`` days from the registry at
    ``db_path``, runs VACUUM to reclaim space, prints a one-line
    summary, and returns ``0`` on success. If ``db_path`` does not
    exist the handler prints ``no registry at <path>`` and still
    returns ``0`` (idempotent).
    """
    from datetime import datetime, timedelta, timezone

    db_path = Path(db_path)
    if not db_path.exists():
        print(f"no registry at {db_path}")
        return 0
    reg = StatefulReviewRegistry(db_path=db_path)
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        deleted = reg.purge_older_than(cutoff_utc=cutoff)
        reg.vacuum()
        size_mb = reg.disk_size_mb()
        print(f"purged: {deleted} rows | size_after: {size_mb:.2f} MB")
    finally:
        reg.close()
    return 0
