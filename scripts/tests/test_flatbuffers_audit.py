"""Smoke test for the FlatBuffers audit harness."""
from __future__ import annotations

from pathlib import Path

import pytest

flatbuffers = pytest.importorskip("flatbuffers")


def test_flatbuffers_audit_runs_at_n_1000(tmp_path: Path) -> None:
    from vitruvius.bench.bench_flatbuffers_audit import (
        AuditResult,
        bench_event_store_serialization,
        bench_verdict_cache_serialization,
    )

    ev = bench_event_store_serialization(n=1000)
    assert isinstance(ev, AuditResult)
    assert ev.site == "event_store_serialization"
    assert ev.n == 1000
    assert ev.json_wall_seconds > 0
    assert ev.flatbuffers_wall_seconds > 0
    assert ev.speedup_ratio == pytest.approx(
        ev.json_wall_seconds / ev.flatbuffers_wall_seconds, rel=1e-6
    )

    vc = bench_verdict_cache_serialization(n=1000)
    assert vc.site == "verdict_cache_serialization"
    assert vc.n == 1000
    assert vc.speedup_ratio > 0


def test_flatbuffers_audit_verdict_emits_recommendation(tmp_path: Path) -> None:
    from vitruvius.bench.bench_flatbuffers_audit import compute_recommendation

    # Speedup > 2x on both sites → GO
    assert compute_recommendation(
        event_store_ratio=2.5, verdict_cache_ratio=3.0
    ) == "GO"
    # Speedup between 1.25 and 2 → DEFER
    assert compute_recommendation(
        event_store_ratio=1.5, verdict_cache_ratio=1.4
    ) == "DEFER"
    # Speedup < 1.25 or any mix below threshold → NO_GO
    assert compute_recommendation(
        event_store_ratio=0.9, verdict_cache_ratio=2.5
    ) == "NO_GO"
    assert compute_recommendation(
        event_store_ratio=1.1, verdict_cache_ratio=1.1
    ) == "NO_GO"
