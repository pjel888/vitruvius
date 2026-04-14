from __future__ import annotations

import pytest
from pathlib import Path

from vitruvius.registry_rotation import (
    RotationPlan,
    RotationReport,
    apply_rotation,
    plan_rotation,
    run_rotate_registries,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_registry_file(tmp_path: Path, stamp: str, family: str) -> Path:
    p = tmp_path / f"{stamp}_{family}"
    p.write_text("")
    return p


# ---------------------------------------------------------------------------
# Core rotation tests
# ---------------------------------------------------------------------------

def test_empty_registries_dir_plans_nothing(tmp_path):
    report = plan_rotation(tmp_path, keep=30)
    assert report.plans == ()
    assert report.total_kept == 0
    assert report.total_pruned == 0


def test_single_family_below_keep_threshold(tmp_path):
    stamps = [f"2026041{i}T000000Z" for i in range(5)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    assert len(report.plans) == 1
    plan = report.plans[0]
    assert len(plan.kept) == 5
    assert len(plan.pruned) == 0
    assert report.total_kept == 5
    assert report.total_pruned == 0


def test_single_family_exactly_at_keep_threshold(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(30)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    assert len(report.plans) == 1
    plan = report.plans[0]
    assert len(plan.kept) == 30
    assert len(plan.pruned) == 0
    assert report.total_kept == 30
    assert report.total_pruned == 0


def test_single_family_above_keep_threshold(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    assert len(report.plans) == 1
    plan = report.plans[0]
    assert len(plan.kept) == 30
    assert len(plan.pruned) == 5
    assert report.total_kept == 30
    assert report.total_pruned == 5


def test_multi_family_rotation_independent(tmp_path):
    for i in range(35):
        _make_registry_file(tmp_path, f"20260413T{i:06d}Z", "raw_file_registry.csv")
    for i in range(20):
        _make_registry_file(tmp_path, f"20260413T{i:06d}Z", "conversion_registry.csv")
    for i in range(40):
        _make_registry_file(tmp_path, f"20260413T{i:06d}Z", "spreadsheet_registry.csv")

    report = plan_rotation(tmp_path, keep=30)
    assert len(report.plans) == 3

    by_family = {p.family: p for p in report.plans}

    raw = by_family["raw_file_registry.csv"]
    assert len(raw.kept) == 30
    assert len(raw.pruned) == 5

    conv = by_family["conversion_registry.csv"]
    assert len(conv.kept) == 20
    assert len(conv.pruned) == 0

    spread = by_family["spreadsheet_registry.csv"]
    assert len(spread.kept) == 30
    assert len(spread.pruned) == 10

    assert report.total_kept == 80
    assert report.total_pruned == 15


def test_keep_zero_prunes_everything(tmp_path):
    stamps = [f"2026041{i}T000000Z" for i in range(5)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=0)
    assert len(report.plans) == 1
    plan = report.plans[0]
    assert len(plan.kept) == 0
    assert len(plan.pruned) == 5
    assert report.total_kept == 0
    assert report.total_pruned == 5


def test_newest_first_ordering_in_plan(tmp_path):
    stamps = [
        "20260413T000000Z",
        "20260413T010000Z",
        "20260413T020000Z",
        "20260413T030000Z",
        "20260413T040000Z",
    ]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    plan = report.plans[0]
    kept_stamps = [p.name.split("_")[0] for p in plan.kept]
    assert kept_stamps == sorted(kept_stamps, reverse=True)


# ---------------------------------------------------------------------------
# Pattern matching tests
# ---------------------------------------------------------------------------

def test_latest_files_are_ignored(tmp_path):
    (tmp_path / "latest_raw_file_registry.csv").write_text("")
    (tmp_path / "latest_conversion_registry.csv").write_text("")
    report = plan_rotation(tmp_path, keep=30)
    assert report.plans == ()
    assert report.total_kept == 0
    assert report.total_pruned == 0


def test_non_timestamped_files_ignored(tmp_path):
    (tmp_path / "canonical_registry.csv").write_text("")
    (tmp_path / "source_registry.csv").write_text("")
    report = plan_rotation(tmp_path, keep=30)
    assert report.plans == ()


def test_malformed_timestamp_ignored(tmp_path):
    # Missing T, Z and seconds — 8 digits underscore only
    (tmp_path / "20260413_raw_file_registry.csv").write_text("")
    report = plan_rotation(tmp_path, keep=30)
    assert report.plans == ()


def test_non_csv_files_ignored(tmp_path):
    (tmp_path / "20260413T000000Z_raw_file_registry.txt").write_text("")
    report = plan_rotation(tmp_path, keep=30)
    assert report.plans == ()


# ---------------------------------------------------------------------------
# apply_rotation tests
# ---------------------------------------------------------------------------

def test_apply_rotation_deletes_pruned_files(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    assert report.total_pruned == 5

    applied = apply_rotation(report)
    remaining = list(tmp_path.glob("*.csv"))
    assert len(remaining) == 30
    assert applied.total_pruned == 5


def test_apply_rotation_does_not_touch_kept_files(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    plan = report.plans[0]
    kept_paths = list(plan.kept)

    apply_rotation(report)
    for p in kept_paths:
        assert p.exists(), f"Kept file was deleted: {p}"


def test_apply_rotation_returns_report_with_dry_run_false(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)
    assert report.dry_run is True
    applied = apply_rotation(report)
    assert applied.dry_run is False


def test_apply_rotation_raises_if_file_missing(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")
    report = plan_rotation(tmp_path, keep=30)

    # Pre-delete one of the pruned files
    first_pruned = report.plans[0].pruned[0]
    first_pruned.unlink()

    with pytest.raises(FileNotFoundError):
        apply_rotation(report)


# ---------------------------------------------------------------------------
# run_rotate_registries (CLI entry) tests
# ---------------------------------------------------------------------------

def test_run_rotate_registries_dry_run_does_not_delete(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")

    rc = run_rotate_registries(keep=30, dry_run=True, registries_dir=tmp_path)
    assert rc == 0
    assert len(list(tmp_path.glob("*.csv"))) == 35


def test_run_rotate_registries_apply_deletes(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")

    rc = run_rotate_registries(keep=30, dry_run=False, registries_dir=tmp_path)
    assert rc == 0
    assert len(list(tmp_path.glob("*.csv"))) == 30


def test_run_rotate_registries_prints_summary(tmp_path, capsys):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")

    run_rotate_registries(keep=30, dry_run=True, registries_dir=tmp_path)
    out = capsys.readouterr().out
    assert "rotate-registries" in out
    assert "raw_file_registry.csv" in out
    # kept and pruned counts present
    assert "30" in out
    assert "5" in out


def test_run_rotate_registries_explicit_registries_dir_override(tmp_path):
    stamps = [f"20260413T{i:06d}Z" for i in range(35)]
    for s in stamps:
        _make_registry_file(tmp_path, s, "raw_file_registry.csv")

    real_registries = Path("/Users/philiplewis/vitruvius/006_System-Manifests/registries")
    real_count_before = len(list(real_registries.glob("*.csv")))

    rc = run_rotate_registries(keep=30, dry_run=False, registries_dir=tmp_path)
    assert rc == 0

    # Real registries dir untouched
    real_count_after = len(list(real_registries.glob("*.csv")))
    assert real_count_after == real_count_before

    # tmp_path was rotated
    assert len(list(tmp_path.glob("*.csv"))) == 30


# ---------------------------------------------------------------------------
# Dataclass smoke tests
# ---------------------------------------------------------------------------

def test_rotation_plan_is_frozen():
    plan = RotationPlan(family="raw_file_registry.csv", kept=(), pruned=())
    with pytest.raises(Exception):
        plan.family = "other.csv"  # type: ignore[misc]


def test_rotation_report_is_frozen():
    report = RotationReport(plans=(), total_kept=0, total_pruned=0, dry_run=True)
    with pytest.raises(Exception):
        report.dry_run = False  # type: ignore[misc]


def test_plan_rotation_rejects_negative_keep(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="keep must be"):
        plan_rotation(tmp_path, keep=-1)
