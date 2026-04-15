"""Sprint HP.3-R Task 6 — verify make_*() factories dispatch on feature flags.

Four tests:
- make_event_store returns EventStore (SQLite) when flag is OFF
- make_event_store returns RocksDBEventStore when flag is ON
- make_stateful_registry returns StatefulReviewRegistry (SQLite) when flag is OFF
- make_stateful_registry returns RocksDBStatefulReviewRegistry when flag is ON

The RocksDB tests are gated on `pytest.importorskip("rocksdict")` so
CI on systems without the binding still passes (the SQLite default
path is still exercised).
"""
from __future__ import annotations

from pathlib import Path

import pytest


def test_make_event_store_returns_sqlite_by_default(tmp_path: Path, monkeypatch) -> None:
    from vitruvius.graph.event_store import EventStore, make_event_store
    import vitruvius.config as cfgmod

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_event_store": False})
    store = make_event_store(db_path=tmp_path / "ev.sqlite")
    try:
        assert isinstance(store, EventStore)
    finally:
        store.close()


def test_make_event_store_returns_rocksdb_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.event_store import make_event_store
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore
    import vitruvius.config as cfgmod

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_event_store": True})
    store = make_event_store(db_path=tmp_path / "ev.rocksdb")
    try:
        assert isinstance(store, RocksDBEventStore)
    finally:
        store.close()


def test_make_stateful_registry_returns_sqlite_by_default(tmp_path: Path, monkeypatch) -> None:
    from vitruvius.review.stateful_registry import (
        StatefulReviewRegistry,
        make_stateful_registry,
    )
    import vitruvius.config as cfgmod

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_verdict_cache": False})
    reg = make_stateful_registry(db_path=tmp_path / "reg.sqlite")
    try:
        assert isinstance(reg, StatefulReviewRegistry)
    finally:
        reg.close()


def test_make_stateful_registry_returns_rocksdb_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry
    from vitruvius.review.stateful_registry import make_stateful_registry
    import vitruvius.config as cfgmod

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_verdict_cache": True})
    reg = make_stateful_registry(db_path=tmp_path / "reg.rocksdb")
    try:
        assert isinstance(reg, RocksDBStatefulReviewRegistry)
    finally:
        reg.close()
