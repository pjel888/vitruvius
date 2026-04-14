"""Stream W4.3 — benchmark harness self-test.

Stream W4.4 — decision log automation self-test.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.bench.run_wiring_bench import (
    BenchResult,
    append_decision_entry,
    bench_stage,
    run_all_stages,
)


def test_bench_stage_returns_result() -> None:
    result = bench_stage("no_op", lambda: None, iterations=3)
    assert isinstance(result, BenchResult)
    assert result.stage == "no_op"
    assert result.iterations == 3
    assert result.avg_ms >= 0
    assert result.peak_rss_mb >= 0


def test_run_all_stages_emits_one_result_per_stage() -> None:
    stages = {
        "first": lambda: sum(range(100)),
        "second": lambda: sorted(range(50)),
    }
    results = run_all_stages(stages, iterations=2)
    assert len(results) == 2
    assert {r.stage for r in results} == {"first", "second"}


def test_append_decision_entry(tmp_path: Path) -> None:
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n\n", encoding="utf-8")

    append_decision_entry(
        decisions_file,
        entry_id="AD-W001",
        title="Stream W.1 wiring run",
        summary="Bench shows NB prefilter saves 42ms per candidate",
    )

    content = decisions_file.read_text(encoding="utf-8")
    assert "AD-W001" in content
    assert "Stream W.1 wiring run" in content
    assert "NB prefilter saves 42ms" in content


def test_append_decision_is_idempotent(tmp_path: Path) -> None:
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n\n", encoding="utf-8")

    for _ in range(3):
        append_decision_entry(
            decisions_file,
            entry_id="AD-W001",
            title="dup check",
            summary="Should only appear once",
        )

    content = decisions_file.read_text(encoding="utf-8")
    assert content.count("AD-W001") == 1
