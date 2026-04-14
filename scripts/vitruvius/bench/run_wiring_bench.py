"""Stage-by-stage benchmark harness (latency + peak RSS).

Stream W4.3 scaffolding — provides :class:`BenchResult`, :func:`bench_stage`,
:func:`run_all_stages`, and (W4.4) :func:`append_decision_entry` so
Sprint Q closure can automate the decision log from a real run.
"""
from __future__ import annotations

import gc
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping


@dataclass(frozen=True)
class BenchResult:
    stage: str
    iterations: int
    avg_ms: float
    peak_rss_mb: float


def _peak_rss_mb() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # On macOS ru_maxrss is in bytes; on Linux it is in kilobytes.
    if sys.platform == "darwin":
        return rss / (1024 * 1024)
    return rss / 1024


def bench_stage(
    stage: str,
    func: Callable[[], object],
    *,
    iterations: int = 5,
) -> BenchResult:
    """Run ``func`` ``iterations`` times, returning average latency in ms
    and the observed peak RSS in MB for the current process.
    """
    gc.collect()
    start_rss = _peak_rss_mb()
    durations: list[float] = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        durations.append((t1 - t0) * 1000)
    end_rss = _peak_rss_mb()
    return BenchResult(
        stage=stage,
        iterations=iterations,
        avg_ms=sum(durations) / len(durations),
        peak_rss_mb=max(start_rss, end_rss),
    )


def run_all_stages(
    stages: Mapping[str, Callable[[], object]],
    *,
    iterations: int = 5,
) -> list[BenchResult]:
    """Run every ``(name, callable)`` in ``stages`` through :func:`bench_stage`
    and return one ordered :class:`BenchResult` per stage.
    """
    return [bench_stage(name, fn, iterations=iterations) for name, fn in stages.items()]


def append_decision_entry(
    decisions_file: Path,
    *,
    entry_id: str,
    title: str,
    summary: str,
) -> None:
    """Stream W4.4 — idempotently append an AD entry to decisions.md.

    If ``entry_id`` already appears in the file, the function is a no-op.
    """
    text = decisions_file.read_text(encoding="utf-8") if decisions_file.exists() else ""
    if entry_id in text:
        return
    block = (
        f"\n## {entry_id} — {title}\n"
        f"\n- Date: {time.strftime('%Y-%m-%d')}\n"
        f"- Summary: {summary}\n"
    )
    with decisions_file.open("a", encoding="utf-8") as f:
        f.write(block)


def main() -> int:
    """Stub CLI runnable — real stages wired in a future task."""
    results = run_all_stages(
        {
            "noop": lambda: None,
            "range_sum": lambda: sum(range(10_000)),
        },
        iterations=10,
    )
    import json
    print(json.dumps([r.__dict__ for r in results], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
