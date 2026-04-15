"""Sprint RUST-MIG-1 Task 1 — bench harness baseline test.

Verifies that ``bench_rust_mig_baseline.run_baseline(out_path)`` writes
a JSON report containing one entry per migration candidate, with the
required per-candidate fields and a verdict column. The subprocess
dispatch is mocked so the test runs in well under 3 seconds — the real
bench is a separate manual invocation via the ``__main__`` entry point.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

# The module lives under scripts/vitruvius/bench/ — pytest conftest
# already adds scripts/ to sys.path so the ``vitruvius.*`` import works.
from vitruvius.bench import bench_rust_mig_baseline as baseline


REQUIRED_CANDIDATES = {
    "s1_adjacency_edges",
    "s2_weight_by_distance",
    "n1_wasserstein",
    "n4_mahalanobis",
    "s10_bloom",
    "g2_duplicate_detector",
    "p9_scanner_sha256",
    "p10_merkle_fs",
}

REQUIRED_FIELDS = {"wall_ms", "peak_rss_mb", "n", "verdict"}


def _fake_dispatch(
    candidate_id: str, *, n: int, timeout_s: float = 30.0
) -> dict[str, object]:
    """Return a deterministic fake subprocess result.

    The real dispatcher spawns ``/usr/bin/time -l python3 -c <script>``
    per candidate, which is slow. For the unit test we only need the
    JSON-writing code path to exercise: stub the dispatcher to return a
    plausible record. Mix hot + cold + aborted so the verdict column is
    exercised in all three states.
    """
    hot_ids = {"s1_adjacency_edges", "n4_mahalanobis", "p10_merkle_fs"}
    aborted_ids = {"g2_duplicate_detector"}
    if candidate_id in aborted_ids:
        return {
            "wall_ms": None,
            "peak_rss_mb": None,
            "n": n,
            "verdict": "aborted",
            "error": "stub: aborted",
        }
    wall_ms = 50.0 if candidate_id in hot_ids else 5.0
    peak_rss_mb = 12.0 if candidate_id in hot_ids else 4.0
    return {
        "wall_ms": wall_ms,
        "peak_rss_mb": peak_rss_mb,
        "n": n,
        "verdict": "hot" if candidate_id in hot_ids else "cold",
    }


def test_verdict_threshold_constants_are_exposed() -> None:
    assert baseline.VERDICT_THRESHOLD_WALL_MS == 25
    assert baseline.VERDICT_THRESHOLD_RSS_MB == 10


def test_classify_verdict_hot_cold_boundary() -> None:
    assert baseline.classify_verdict(wall_ms=26.0, peak_rss_mb=1.0) == "hot"
    assert baseline.classify_verdict(wall_ms=1.0, peak_rss_mb=11.0) == "hot"
    assert baseline.classify_verdict(wall_ms=25.0, peak_rss_mb=10.0) == "cold"
    assert baseline.classify_verdict(wall_ms=0.0, peak_rss_mb=0.0) == "cold"


def test_bench_rust_mig_baseline_writes_report(tmp_path: Path) -> None:
    out_path = tmp_path / "baseline.json"

    with patch.object(
        baseline,
        "_run_candidate_subprocess",
        side_effect=_fake_dispatch,
    ) as mock_dispatch:
        report = baseline.run_baseline(out_path)

    # The dispatcher was called once per candidate.
    assert mock_dispatch.call_count == len(REQUIRED_CANDIDATES)

    # The JSON file was written.
    assert out_path.is_file()
    on_disk = json.loads(out_path.read_text())
    assert on_disk == report

    # Every required candidate is present in the report.
    candidates = on_disk["candidates"]
    assert set(candidates.keys()) == REQUIRED_CANDIDATES

    # Every candidate has the required fields.
    for cid, entry in candidates.items():
        missing = REQUIRED_FIELDS - set(entry.keys())
        assert not missing, f"candidate {cid} missing fields: {missing}"
        assert entry["verdict"] in {"hot", "cold", "aborted"}
        assert isinstance(entry["n"], int)

    # The report carries the thresholds so the gate is auditable.
    assert on_disk["threshold_wall_ms"] == baseline.VERDICT_THRESHOLD_WALL_MS
    assert on_disk["threshold_peak_rss_mb"] == baseline.VERDICT_THRESHOLD_RSS_MB

    # The report carries a timestamp so the bench is traceable.
    assert "timestamp_utc" in on_disk
    assert isinstance(on_disk["timestamp_utc"], str)
