"""Stream Y4.3 — purge_older_than + disk_size_mb + CLI handler tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from vitruvius.review.stateful_registry import (
    StatefulReviewRegistry,
    VerdictRecord,
    run_ple_registry_purge,
)


def _record(idx: int, created: datetime) -> VerdictRecord:
    return VerdictRecord(
        source_hash=f"s{idx}",
        relationship_hash="r",
        model_version="m",
        verdict="keep",
        self_confidence=0.9,
        created_utc=created.isoformat(),
    )


def test_purge_older_than(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    now = datetime.now(timezone.utc)
    reg.put(_record(1, now - timedelta(days=10)))
    reg.put(_record(2, now - timedelta(days=1)))
    assert reg.count() == 2

    deleted = reg.purge_older_than(cutoff_utc=(now - timedelta(days=5)).isoformat())
    assert deleted == 1
    assert reg.count() == 1


def test_disk_size_mb_reports_positive(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    now = datetime.now(timezone.utc)
    for i in range(50):
        reg.put(_record(i, now))
    assert reg.disk_size_mb() > 0


def test_cli_purge_handler_missing_db(tmp_path: Path, capsys) -> None:
    rc = run_ple_registry_purge(db_path=tmp_path / "nope.sqlite", days=30)
    assert rc == 0
    out = capsys.readouterr().out
    assert "no registry at" in out


def test_cli_purge_handler_deletes_old_rows(tmp_path: Path, capsys, monkeypatch) -> None:
    """Explicitly exercise the SQLite backend path through the CLI.

    Sprint HP.3-R AD-029 flipped hp_rocksdb_verdict_cache default to true.
    This test predates that flip and was written to exercise the SQLite
    registry specifically (it creates a file-based sqlite DB at
    tmp_path / 'reg.sqlite'). Force the factory to return the SQLite
    class so the test keeps exercising its original target path.
    """
    import vitruvius.review.stateful_registry as srmod
    monkeypatch.setattr(
        srmod,
        "make_stateful_registry",
        lambda *, db_path: StatefulReviewRegistry(db_path=db_path),
    )

    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    now = datetime.now(timezone.utc)
    reg.put(_record(1, now - timedelta(days=60)))  # old — should be purged
    reg.put(_record(2, now - timedelta(days=5)))   # recent — retained
    reg.close()

    rc = run_ple_registry_purge(db_path=db, days=30)
    assert rc == 0
    out = capsys.readouterr().out
    assert "purged: 1 rows" in out

    reg2 = StatefulReviewRegistry(db_path=db)
    try:
        assert reg2.count() == 1
    finally:
        reg2.close()


def test_run_ple_registry_purge_uses_factory_when_flag_on(tmp_path, monkeypatch):
    """Sprint HP.3-R Task 6 supplement: the purge CLI must go through
    make_stateful_registry so that when hp_rocksdb_verdict_cache is on,
    it purges the RocksDB data directory instead of opening a stale
    SQLite file at the same path.

    Rather than require a live RocksDB at db_path (which the purge path
    checks for file-existence first and returns 0 for), we monkeypatch
    make_stateful_registry itself and assert it was called. This proves
    the CLI is routing through the factory layer.
    """
    import pytest
    import vitruvius.review.stateful_registry as srmod

    calls = []

    class _StubRegistry:
        def __init__(self, *, db_path):
            calls.append(("init", db_path))

        def purge_older_than(self, *, cutoff_utc):
            calls.append(("purge_older_than", cutoff_utc))
            return 0

        def vacuum(self):
            calls.append(("vacuum",))

        def disk_size_mb(self):
            return 0.0

        def close(self):
            calls.append(("close",))

    def fake_factory(*, db_path):
        return _StubRegistry(db_path=db_path)

    monkeypatch.setattr(srmod, "make_stateful_registry", fake_factory)

    # Create an empty file at db_path so the existence check passes.
    db_path = tmp_path / "reg.sqlite"
    db_path.touch()

    rc = srmod.run_ple_registry_purge(db_path=db_path, days=30)
    assert rc == 0

    # The factory must have been called exactly once with the given path.
    init_calls = [c for c in calls if c[0] == "init"]
    assert len(init_calls) == 1, f"expected 1 factory init call, got {init_calls}"
    assert init_calls[0][1] == db_path

    # The purge + vacuum + close calls must all fire on the stub.
    kinds = [c[0] for c in calls]
    assert "purge_older_than" in kinds
    assert "vacuum" in kinds
    assert "close" in kinds
