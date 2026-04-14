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


def test_cli_purge_handler_deletes_old_rows(tmp_path: Path, capsys) -> None:
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
