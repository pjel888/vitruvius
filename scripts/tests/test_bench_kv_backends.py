"""Smoke test for the bench harness. Fast (N=100) so CI can run it."""
from __future__ import annotations

from pathlib import Path

from vitruvius.bench.bench_kv_backends import (
    BenchResult,
    bench_event_store_sqlite,
    bench_verdict_cache_sqlite,
)


def test_event_store_sqlite_bench_runs(tmp_path: Path) -> None:
    result = bench_event_store_sqlite(db_path=tmp_path / "events.sqlite", n_events=100)
    assert isinstance(result, BenchResult)
    assert result.backend == "sqlite"
    assert result.op == "event_store"
    assert result.n == 100
    assert result.wall_seconds > 0
    assert result.throughput_per_second > 0
    # Should also measure point-lookup and time-travel projection times
    assert "append_seconds" in result.breakdown
    assert "point_lookup_seconds" in result.breakdown
    assert "project_graph_at_seconds" in result.breakdown


def test_verdict_cache_sqlite_bench_runs(tmp_path: Path) -> None:
    result = bench_verdict_cache_sqlite(db_path=tmp_path / "verdicts.sqlite", n_verdicts=100)
    assert isinstance(result, BenchResult)
    assert result.backend == "sqlite"
    assert result.op == "verdict_cache"
    assert result.n == 100
    assert "put_seconds" in result.breakdown
    assert "get_hit_seconds" in result.breakdown
    assert "get_miss_seconds" in result.breakdown
