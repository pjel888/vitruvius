"""Smoke test for the integrity audit harness."""
from __future__ import annotations

import pytest

blake3 = pytest.importorskip("blake3")


def test_integrity_audit_runs() -> None:
    from vitruvius.bench.bench_integrity_audit import (
        IntegrityAuditResult,
        bench_sha256_vs_blake3,
        audit_admission_gate_gaps,
    )

    # SHA-256 vs BLAKE3 at the three representative sizes
    bench = bench_sha256_vs_blake3(sizes_kb=(1, 64, 1024))
    assert isinstance(bench, list)
    assert len(bench) == 3
    for r in bench:
        assert isinstance(r, IntegrityAuditResult)
        assert r.sha256_wall_seconds > 0
        assert r.blake3_wall_seconds > 0

    # Admission-gate gap analysis (static: enumerates code paths)
    gaps = audit_admission_gate_gaps()
    assert isinstance(gaps, list)
    assert all(isinstance(g, dict) for g in gaps)
    assert all("site" in g and "has_integrity_check" in g for g in gaps)


def test_integrity_recommendation() -> None:
    from vitruvius.bench.bench_integrity_audit import compute_recommendation

    # BLAKE3 >= 2.5x faster at the 1 MB size → GO (replace SHA-256)
    assert compute_recommendation(blake3_vs_sha256_1mb_ratio=3.0, open_gap_count=0) == "GO_REPLACE"
    # BLAKE3 1.5-2.5x faster → GO_SUPPLEMENT (add BLAKE3 for new hot paths but keep SHA-256)
    assert compute_recommendation(blake3_vs_sha256_1mb_ratio=1.8, open_gap_count=0) == "GO_SUPPLEMENT"
    # BLAKE3 <1.5x faster → NO_GO on the hash swap, but may still GO on gap closure
    assert compute_recommendation(blake3_vs_sha256_1mb_ratio=1.1, open_gap_count=0) == "NO_GO"
    # Any open gap at the admission gate → GO_GAP (ship a fix even if BLAKE3 loses)
    assert compute_recommendation(blake3_vs_sha256_1mb_ratio=1.1, open_gap_count=2) == "GO_GAP"
