"""Sprint AUDIT-1 — Numerical integrity audit harness.

Does TWO independent things:

1. **Benchmark SHA-256 vs BLAKE3** at representative sizes (1 KB,
   64 KB, 1 MB) to decide whether replacing SHA-256 with BLAKE3
   on any hot path is worth the dependency cost.
2. **Static admission-gate gap analysis** — enumerates every
   data-entry point to canonical storage and checks whether it
   carries an integrity check. Returns a list of open gaps.

Emits a single JSON report with benchmark numbers + gap list +
recommendation for Task 2 of the advanced-tech audit plan.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Recommendation = Literal["GO_REPLACE", "GO_SUPPLEMENT", "GO_GAP", "NO_GO"]


@dataclass(frozen=True)
class IntegrityAuditResult:
    size_label: str
    size_bytes: int
    iterations: int
    sha256_wall_seconds: float
    blake3_wall_seconds: float
    speedup_ratio: float  # sha256 / blake3


def _timed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def bench_sha256_vs_blake3(*, sizes_kb: tuple[int, ...] = (1, 64, 1024)) -> list[IntegrityAuditResult]:
    import blake3 as blake3_mod

    results: list[IntegrityAuditResult] = []
    for size_kb in sizes_kb:
        size_bytes = size_kb * 1024
        payload = os.urandom(size_bytes)
        iterations = max(32, 2_000_000 // size_bytes)

        def sha256_loop():
            for _ in range(iterations):
                hashlib.sha256(payload).hexdigest()

        def blake3_loop():
            for _ in range(iterations):
                blake3_mod.blake3(payload).hexdigest()

        sha256_wall = _timed(sha256_loop)
        blake3_wall = _timed(blake3_loop)
        ratio = sha256_wall / blake3_wall if blake3_wall > 0 else 0.0

        results.append(IntegrityAuditResult(
            size_label=f"{size_kb}KB",
            size_bytes=size_bytes,
            iterations=iterations,
            sha256_wall_seconds=sha256_wall,
            blake3_wall_seconds=blake3_wall,
            speedup_ratio=ratio,
        ))
    return results


def audit_admission_gate_gaps() -> list[dict]:
    """Static enumeration of the admission-gate surface.

    Rather than trying to hook a runtime tracer, we hardcode the
    known entry points and flag whether each one already commits
    an integrity check. This list is maintained by hand — if you
    add a new canonical-storage writer, update this list.

    The purpose is NOT to be an exhaustive code audit. It's to
    surface whether the Task 2 decision gate should fire a
    gap-closure task even if BLAKE3 loses the benchmark.
    """
    return [
        {
            "site": "scripts/vitruvius/scanner.py::build_file_entries",
            "description": "Raw-layer file entry — SHA-256 via _sha256_of_file",
            "has_integrity_check": True,
            "algorithm": "sha256",
            "closed_by": "RI-009",
        },
        {
            "site": "scripts/vitruvius/merkle_fs.py::compute_directory_hash",
            "description": "Merkle directory hash — Sprint HP.1",
            "has_integrity_check": True,
            "algorithm": "sha256",
            "flag": "hp_merkle_fs",
        },
        {
            "site": "scripts/vitruvius/wiki/delta_tracker.py::compute_delta",
            "description": "Wiki delta tracker — SHA-256 per content block",
            "has_integrity_check": True,
            "algorithm": "sha256",
            "flag": "wiki_delta_tracking",
        },
        {
            "site": "scripts/vitruvius/promotion/__init__.py::run_promote",
            "description": "Phase 7 promotion — schema + registry validation + audit log",
            "has_integrity_check": True,
            "algorithm": "schema+audit_log",
            "closed_by": "Phase 7",
        },
        {
            "site": "scripts/vitruvius/graph/rocksdb_event_store.py::append",
            "description": "RocksDB event store append — JSON serialize, no content hash in value",
            "has_integrity_check": False,
            "algorithm": None,
            "gap_severity": "LOW",
            "gap_reason": (
                "RocksDB internal block-level checksums already protect against on-disk "
                "corruption. A per-value cryptographic commitment would catch RAM corruption "
                "or malicious writes but is not currently in the threat model."
            ),
        },
        {
            "site": "scripts/vitruvius/review/rocksdb_stateful_registry.py::put",
            "description": "RocksDB verdict cache put — JSON serialize, no content hash",
            "has_integrity_check": False,
            "algorithm": None,
            "gap_severity": "LOW",
            "gap_reason": (
                "Same as event store: RocksDB block checksums cover disk corruption. "
                "Verdict cache entries are regeneratable from the LLM; corruption is recoverable."
            ),
        },
        {
            "site": "scripts/vitruvius/geometric/inequality_compiler.py::check_compliance",
            "description": "Z3 SAT admission check for parametric constraints",
            "has_integrity_check": True,
            "algorithm": "z3_sat_check",
            "flag": "geom_csp_compiler",
        },
        {
            "site": "spatial-daemon/src/contract_writer.ts",
            "description": "TypeScript daemon contract file — writes JSON without a signature",
            "has_integrity_check": False,
            "algorithm": None,
            "gap_severity": "MEDIUM",
            "gap_reason": (
                "Python reads this file and trusts its contents. A truncated or corrupt write "
                "would silently produce wrong spatial results. Adding a SHA-256 or BLAKE3 "
                "footer would let the Python reader detect integrity failures."
            ),
        },
    ]


def compute_recommendation(*, blake3_vs_sha256_1mb_ratio: float, open_gap_count: int) -> Recommendation:
    """Decision gate — evaluated by Task 2 driver and written to the audit JSON.

    GO_REPLACE: BLAKE3 >= 2.5x faster at 1MB — worth replacing SHA-256 on file-hash paths.
    GO_SUPPLEMENT: BLAKE3 1.5-2.5x faster — keep SHA-256 (stable, already wired) but add
                   BLAKE3 as the default for new hot paths like the spatial-daemon contract.
    GO_GAP: BLAKE3 isn't a clear win but at least one open admission-gate gap exists —
            ship a gap-closure fix using the current SHA-256 toolchain.
    NO_GO: BLAKE3 isn't a win AND no open gaps — park the investigation.
    """
    if blake3_vs_sha256_1mb_ratio >= 2.5:
        return "GO_REPLACE"
    if blake3_vs_sha256_1mb_ratio >= 1.5:
        return "GO_SUPPLEMENT"
    if open_gap_count > 0:
        return "GO_GAP"
    return "NO_GO"


if __name__ == "__main__":
    import argparse
    import datetime as dt

    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes-kb", nargs="+", type=int, default=[1, 64, 1024])
    parser.add_argument("--out", type=Path, default=Path(".ai/10_state/audit_integrity_2026-04-15.json"))
    args = parser.parse_args()

    bench = bench_sha256_vs_blake3(sizes_kb=tuple(args.sizes_kb))
    gaps = audit_admission_gate_gaps()

    # Count only gaps marked as NOT having an integrity check.
    open_gaps = [g for g in gaps if not g["has_integrity_check"]]
    medium_or_higher_gaps = [g for g in open_gaps if g.get("gap_severity") in {"MEDIUM", "HIGH"}]

    # Pick the 1MB row for the decision gate.
    one_mb_row = next((r for r in bench if r.size_label == "1024KB"), None)
    one_mb_ratio = one_mb_row.speedup_ratio if one_mb_row else 0.0

    rec = compute_recommendation(
        blake3_vs_sha256_1mb_ratio=one_mb_ratio,
        open_gap_count=len(medium_or_higher_gaps),
    )

    report = {
        "timestamp_utc": dt.datetime.utcnow().isoformat() + "Z",
        "python_interpreter": os.sys.executable,
        "host": "darwin-arm64",
        "benchmarks": [
            {
                "size_label": r.size_label,
                "size_bytes": r.size_bytes,
                "iterations": r.iterations,
                "sha256_wall_seconds": round(r.sha256_wall_seconds, 6),
                "blake3_wall_seconds": round(r.blake3_wall_seconds, 6),
                "speedup_ratio": round(r.speedup_ratio, 4),
            }
            for r in bench
        ],
        "admission_gate_gaps": gaps,
        "open_gap_count": len(open_gaps),
        "medium_or_higher_open_gap_count": len(medium_or_higher_gaps),
        "decision_gate": {
            "blake3_vs_sha256_1mb_ratio": round(one_mb_ratio, 4),
            "threshold_go_replace": 2.5,
            "threshold_go_supplement": 1.5,
            "recommendation": rec,
            "notes": (
                f"BLAKE3 at 1MB: {round(one_mb_ratio, 2)}x vs SHA-256. "
                f"{len(medium_or_higher_gaps)} medium+ open admission-gate gap(s). "
                f"Decision: {rec}."
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
