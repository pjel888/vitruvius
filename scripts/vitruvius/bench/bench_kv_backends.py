"""Benchmark harness for KV backends (SQLite baseline + RocksDB).

Measures the same workload against both backends so the migration
decision can be made on real numbers rather than vibes. Run via
``python -m vitruvius.bench.bench_kv_backends`` or the test suite.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vitruvius.graph.event_store import EventStore, GraphEvent, project_graph_at
from vitruvius.review.stateful_registry import StatefulReviewRegistry, VerdictRecord


@dataclass(frozen=True)
class BenchResult:
    backend: str  # "sqlite" | "rocksdb"
    op: str  # "event_store" | "verdict_cache"
    n: int
    wall_seconds: float
    throughput_per_second: float
    breakdown: dict[str, float] = field(default_factory=dict)


def _timed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def bench_event_store_sqlite(*, db_path: Path, n_events: int) -> BenchResult:
    """Measure append + point-lookup + time-travel projection against SQLite."""
    store = EventStore(db_path=db_path)

    def append_all():
        for i in range(n_events):
            store.append(GraphEvent(
                event_id=i,
                event_type="PROMOTED",
                edge_id=f"rel-{i:06d}",
                timestamp_utc=f"2026-04-15T10:00:{i % 60:02d}Z",
                payload={"from": f"law-{i}", "to": f"concept-{i}"},
            ))

    append_seconds = _timed(append_all)

    def lookup_all():
        for _ in range(n_events):
            store.count()

    point_lookup_seconds = _timed(lookup_all)
    store.close()

    def project():
        project_graph_at(db_path=db_path, timestamp_utc="2026-04-15T10:00:30Z")

    project_graph_at_seconds = _timed(project)
    total = append_seconds + point_lookup_seconds + project_graph_at_seconds

    return BenchResult(
        backend="sqlite",
        op="event_store",
        n=n_events,
        wall_seconds=total,
        throughput_per_second=n_events / total if total > 0 else 0.0,
        breakdown={
            "append_seconds": append_seconds,
            "point_lookup_seconds": point_lookup_seconds,
            "project_graph_at_seconds": project_graph_at_seconds,
        },
    )


def bench_verdict_cache_sqlite(*, db_path: Path, n_verdicts: int) -> BenchResult:
    """Measure put + get-hit + get-miss against SQLite."""
    reg = StatefulReviewRegistry(db_path=db_path)

    def put_all():
        for i in range(n_verdicts):
            reg.put(VerdictRecord(
                source_hash=f"src-{i:06d}",
                relationship_hash=f"rel-{i:06d}",
                model_version="bench:v1",
                verdict="keep" if i % 2 == 0 else "reject",
                self_confidence=0.5 + (i % 10) / 20.0,
                created_utc=f"2026-04-15T10:00:{i % 60:02d}Z",
            ))

    put_seconds = _timed(put_all)

    def get_hit_all():
        for i in range(n_verdicts):
            reg.get(
                source_hash=f"src-{i:06d}",
                relationship_hash=f"rel-{i:06d}",
                model_version="bench:v1",
            )

    get_hit_seconds = _timed(get_hit_all)

    def get_miss_all():
        for i in range(n_verdicts):
            reg.get(
                source_hash=f"src-{i:06d}",
                relationship_hash=f"rel-{i:06d}",
                model_version="nonexistent",
            )

    get_miss_seconds = _timed(get_miss_all)
    reg.close()

    total = put_seconds + get_hit_seconds + get_miss_seconds
    return BenchResult(
        backend="sqlite",
        op="verdict_cache",
        n=n_verdicts,
        wall_seconds=total,
        throughput_per_second=n_verdicts / total if total > 0 else 0.0,
        breakdown={
            "put_seconds": put_seconds,
            "get_hit_seconds": get_hit_seconds,
            "get_miss_seconds": get_miss_seconds,
        },
    )


def result_as_json(result: BenchResult) -> str:
    return json.dumps({
        "backend": result.backend,
        "op": result.op,
        "n": result.n,
        "wall_seconds": round(result.wall_seconds, 4),
        "throughput_per_second": round(result.throughput_per_second, 2),
        "breakdown": {k: round(v, 4) for k, v in result.breakdown.items()},
    }, indent=2)


if __name__ == "__main__":
    import argparse
    import tempfile

    parser = argparse.ArgumentParser(description="KV backend benchmark")
    parser.add_argument("--n", type=int, default=10_000)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        ev = bench_event_store_sqlite(db_path=tmp / "events.sqlite", n_events=args.n)
        print(result_as_json(ev))
        vc = bench_verdict_cache_sqlite(db_path=tmp / "verdicts.sqlite", n_verdicts=args.n)
        print(result_as_json(vc))
