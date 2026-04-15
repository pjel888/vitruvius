"""Sprint HP.3-R — one-shot SQLite → RocksDB KV migration.

Handler for the ``ple-kv-migrate`` CLI subcommand. Idempotent:
re-running against a populated destination is a no-op for keys that
already exist.

Usage:
    ple-kv-migrate --store event    --source events.sqlite  --dest events.rocksdb
    ple-kv-migrate --store registry --source reg.sqlite     --dest reg.rocksdb    [--dry-run]

Reads the SQLite source directly (via stdlib ``sqlite3``) so the
migration does not depend on the ``EventStore`` or
``StatefulReviewRegistry`` classes being able to open the source
file. Writes via the ``RocksDBEventStore`` / ``RocksDBStatefulReviewRegistry``
classes so the destination layout matches what the runtime code
will consume.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Literal

StoreKind = Literal["event", "registry"]


def run_kv_migrate(
    *,
    store: StoreKind,
    source: Path,
    dest: Path,
    dry_run: bool = False,
) -> int:
    """Return 0 on success, non-zero on failure."""
    source = Path(source)
    dest = Path(dest)

    if not source.exists():
        print(f"source not found: {source}")
        return 1

    if store == "event":
        return _migrate_event_store(source=source, dest=dest, dry_run=dry_run)
    if store == "registry":
        return _migrate_registry(source=source, dest=dest, dry_run=dry_run)

    print(f"unknown --store value: {store!r} (expected 'event' or 'registry')")
    return 2


def _migrate_event_store(*, source: Path, dest: Path, dry_run: bool) -> int:
    # Read every event row directly from SQLite so the migration does
    # not depend on the EventStore class being able to open the source.
    conn = sqlite3.connect(source)
    try:
        rows = conn.execute(
            "SELECT event_id, event_type, edge_id, timestamp_utc, payload_json "
            "FROM graph_events ORDER BY event_id ASC"
        ).fetchall()
    finally:
        conn.close()

    if dry_run:
        print(f"dry-run: would migrate {len(rows)} events from {source} to {dest}")
        return 0

    from vitruvius.graph.event_store import GraphEvent
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore

    dest_store = RocksDBEventStore(db_path=dest)
    copied = 0
    skipped = 0
    try:
        for (event_id, event_type, edge_id, timestamp_utc, payload_json) in rows:
            payload = json.loads(payload_json) if payload_json else {}
            event = GraphEvent(
                event_id=int(event_id),
                event_type=event_type,
                edge_id=edge_id,
                timestamp_utc=timestamp_utc,
                payload=payload,
            )
            try:
                dest_store.append(event)
                copied += 1
            except ValueError as exc:
                # Duplicate event_id means this row was already
                # migrated on a prior run. Idempotent skip.
                if "duplicate" not in str(exc):
                    raise
                skipped += 1
    finally:
        dest_store.close()

    print(f"migrated: {copied} events copied, {skipped} skipped (idempotent)")
    return 0


def _migrate_registry(*, source: Path, dest: Path, dry_run: bool) -> int:
    conn = sqlite3.connect(source)
    try:
        rows = conn.execute(
            "SELECT source_hash, relationship_hash, model_version, "
            "verdict, self_confidence, created_utc FROM verdicts"
        ).fetchall()
    finally:
        conn.close()

    if dry_run:
        print(f"dry-run: would migrate {len(rows)} verdicts from {source} to {dest}")
        return 0

    from vitruvius.review.rocksdb_stateful_registry import (
        RocksDBStatefulReviewRegistry,
    )
    from vitruvius.review.stateful_registry import VerdictRecord

    dest_reg = RocksDBStatefulReviewRegistry(db_path=dest)
    copied = 0
    try:
        for (src_h, rel_h, model, verdict, conf, created) in rows:
            dest_reg.put(VerdictRecord(
                source_hash=src_h,
                relationship_hash=rel_h,
                model_version=model,
                verdict=verdict,
                self_confidence=float(conf),
                created_utc=created,
            ))
            copied += 1
    finally:
        dest_reg.close()

    print(f"migrated: {copied} verdicts copied")
    return 0
