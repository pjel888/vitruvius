---
plan_id: advanced-tech-audit-2026-04-15
phase: meta
title: "Advanced Tech Audit — FlatBuffers, Numerical Integrity, MC Dropout"
status: active
priority: medium
sprint: "Sprint AUDIT-1 (post-HP.3-R)"
version: 1.0.0
plan_type: audit_then_conditional_implementation
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint HP.3-R closed (tag `sprint-hp3r-closed`) — RocksDB KV migration is the most recent perf win and the audit measures against the post-HP.3-R baseline
  - Python test suite green at 1396/1 on main
related_plans:
  - ../09_archive/plans/2026-04-15-docs-cleanup-plan.md (README refresh flagged FlatBuffers / numerical-lock / MC dropout as not-yet-wired — this plan follows up)
---

# Advanced Tech Audit — FlatBuffers, Numerical Integrity, MC Dropout

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decide — with measured evidence, not vibes — whether to adopt FlatBuffers, add numerical integrity checks at the admission gate, and wire Monte Carlo Dropout into a production neural-inference site. Ship only the tech that passes a numeric decision gate.

**Architecture:** Audit-first, implement-conditionally. Three independent audit tasks survey the codebase, measure the current baseline, estimate the speedup or accuracy gain from adopting each tech, and produce a machine-readable `recommendation: GO | NO_GO | DEFER` verdict with numeric thresholds. Three implementation tasks run only if their corresponding audit emits `GO`. A final docs/ledger task records AD-030 with the findings regardless of outcome — the "we audited and decided not to ship" outcome is just as valuable as a shipped feature.

**Tech Stack:**
- `flatbuffers` — Google's zero-copy cross-language serialization format (Python package: `flatbuffers`; Rust crate: `flatbuffers`). Not currently installed.
- `blake3` — next-gen cryptographic hash (3-5× faster than SHA-256 on modern hardware). Python package: `blake3`. Not currently installed.
- `rocksdict 0.3.29` — already installed (from Sprint HP.3-R). The audit will not need a new RocksDB binding.
- Existing utilities: `scripts/vitruvius/graph/mc_dropout.py::compute_epistemic_uncertainty` (34 lines, stdlib-only, zero production call sites as of commit `eabc05e`).

---

## Pre-Audit Ground Truth (verified at plan-write time)

Facts the auditors do NOT need to re-derive. These are load-bearing inputs for each audit task.

### General state

- **Branch:** `main` at `04bfb2b` (docs cleanup closure). 244 commits ahead of `origin/main`.
- **Test suite:** 1396 Python passed, 1 skipped. 20 TypeScript (spatial-daemon). 10 Rust (engine_rs + datalog_rs).
- **Recent perf baseline:** Sprint HP.3-R bench at n=10000 (`.ai/10_state/bench_kv_migration_2026-04-15.json`): RocksDB event_store wall 0.1888s, verdict_cache 0.1480s. Any new serialization or hashing proposal must be compared against this baseline, not against the pre-HP.3-R SQLite numbers.

### FlatBuffers — current serialization surface

28 occurrences of `json.dumps` / `json.loads` across 20 files in `scripts/vitruvius/`. The auditor will rank them by frequency-weighted byte volume. Known high-traffic serialization sites:

- `scripts/vitruvius/graph/rocksdb_event_store.py::append` — serializes `{event_type, edge_id, timestamp_utc, payload}` to UTF-8 JSON on **every append**. Bench measured 0.1559s for 10000 appends = ~15.6 µs / append.
- `scripts/vitruvius/review/rocksdb_stateful_registry.py::put` — serializes `{verdict, self_confidence, created_utc}` on **every put**. Bench measured 0.1077s for 10000 puts = ~10.8 µs / put.
- `scripts/vitruvius/graph/rocksdb_event_store.py::project_graph_at_rocksdb` — deserializes the full JSON record to read `edge_id` + `event_type` + `payload`. This is the **strongest partial-read candidate** for FlatBuffers — if we only needed `edge_id` (e.g. to check existence), FlatBuffers would skip parsing `payload`.
- `spatial-daemon/src/contract_writer.ts` — TypeScript → Python contract file. Not yet profiled; auditor will measure current write size and frequency.
- `scripts/vitruvius/graph/snapshot.py` — writes `latest_graph_snapshot.json` for downstream consumers. Potentially large, infrequent.

Known NON-candidates (audit should explicitly exclude):
- `config/vitruvius.yaml` — loaded once at startup. Not hot.
- Audit log / CoT audit — human-readable, infrequent writes.
- Test fixtures — not production.

### Numerical integrity — current surface

15 files import `hashlib` or use `sha256`. Known integrity mechanisms:

- **SHA-256 file hash** — `scripts/vitruvius/scanner.py::_sha256_of_file` + `FileEntry.sha256` (RI-009 closed). Every file entering the raw layer carries a content hash.
- **Merkle directory hash** — `scripts/vitruvius/merkle_fs.py` (Sprint HP.1, 96 lines). Content-addressable over directory trees. Flag `hp_merkle_fs` defaults false.
- **Z3 admission check** — `scripts/vitruvius/geometric/inequality_compiler.py::check_compliance` (Sprint GEOM.1). Parametric constraints must be SAT-checkable before entering canonical storage.
- **Bloom filter foraging** — `scripts/vitruvius/foraging/bloom_filter.py` + `duplicate_detector.py` (Sprint GT.5.2).
- **Delta tracker SHA-256** — `scripts/vitruvius/wiki/delta_tracker.py` (Sprint WIKI.3).

Gap candidates the audit should investigate:
- RocksDB event store values — currently NOT hashed before write. The SQLite fallback has no checksum either. An integrity check here would catch corruption from hardware errors.
- Rust Wasm kernel outputs — `aabb_intersects` returns a boolean without any cryptographic commitment. Probably doesn't need one.
- `spatial-daemon` contract file — should it carry a signature so Python can verify it wasn't truncated?

### MC Dropout — current surface

**Critical finding:** `scripts/vitruvius/graph/graphsage.py` is the ONLY neural module in the repo. Line 219 explicitly reads:

> `# Deterministic forward pass — no dropout, no training loop.`

This means MC Dropout has **zero viable production sites today** unless we either:
1. Enable dropout in GraphSAGE inference (new feature work, not a wiring task)
2. Add a new neural classifier somewhere (e.g. a dropout-enabled variant of the NB prefilter)
3. Park the utility for future use when we do ship a dropout-enabled model

Other non-candidates:
- `scripts/vitruvius/review/naive_bayes_filter.py` — Naive Bayes is a closed-form probabilistic classifier, not a neural net. MC dropout is inapplicable.
- `scripts/vitruvius/extraction/crf_trainer.py` — CRF is linear-chain, not a deep neural net with dropout layers.
- `scripts/vitruvius/ollama_review.py` — the LLM runs on Ollama's inference server, which does NOT expose a dropout-at-inference knob to clients.

So the MC Dropout audit's first decision is **binary**: is there any plausible site at all? The audit task below gives it one more honest look, but the prior is strongly "park the utility."

---

## Dispatch Waves

| Wave | Tasks | Parallel-safe | Reason |
|---|---|---|---|
| A — Audit | 1, 2, 3 | ✅ yes (file-disjoint; each writes its own JSON output) | Independent surveys |
| B — Implement (conditional) | 4, 5, 6 | ❌ serial | Each reads its audit's `recommendation` field and only runs on `GO`. Serial execution lets the orchestrator inspect the previous wave's output before dispatching. |
| C — Docs + AD-030 | 7 | ❌ orchestrator-only | Final atomic commit; writes AD-030 with verdicts + any shipped bench deltas |

---

## Task 1: FlatBuffers Audit (Wave A)

**Goal:** Measure whether replacing JSON serialization with FlatBuffers at the top 3 hottest sites would produce a ≥2× speedup without unreasonable complexity cost.

**Files:**
- Create: `scripts/vitruvius/bench/bench_flatbuffers_audit.py` — benchmark harness comparing `json.dumps` + `json.loads` against `flatbuffers` pack + unpack on synthetic-but-representative records
- Create: `.ai/10_state/audit_flatbuffers_2026-04-15.json` — machine-readable audit output
- Create: `scripts/tests/test_flatbuffers_audit.py` — smoke test that the audit harness runs at n=1000 and produces a valid JSON result file

### Step 1: Install flatbuffers (isolated; can be uninstalled after audit)

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip install flatbuffers==24.3.25
/opt/homebrew/opt/python@3.11/bin/python3.11 -c "import flatbuffers; print('flatbuffers', flatbuffers.__version__)"
```

Expected: `flatbuffers 24.3.25` printed. No compile output (pure Python package).

### Step 2: Write the failing smoke test

Create `scripts/tests/test_flatbuffers_audit.py`:

```python
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
```

### Step 3: Run the smoke test (it should fail)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_flatbuffers_audit.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.bench.bench_flatbuffers_audit'`.

### Step 4: Create the audit harness

Create `scripts/vitruvius/bench/bench_flatbuffers_audit.py`:

```python
"""Sprint AUDIT-1 — FlatBuffers audit harness.

Benchmarks the top two JSON-serialization hot paths (event_store append
and verdict_cache put) against hand-written FlatBuffers-like flat
representations. Emits an :class:`AuditResult` per site plus a
combined recommendation for Task 1 of the advanced-tech audit plan.

This is a STUDY module — it does not touch the production
RocksDBEventStore or RocksDBStatefulReviewRegistry classes. The
only purpose is to measure whether the proposal is worth shipping.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Recommendation = Literal["GO", "DEFER", "NO_GO"]


@dataclass(frozen=True)
class AuditResult:
    site: str
    n: int
    json_wall_seconds: float
    flatbuffers_wall_seconds: float
    speedup_ratio: float  # json / flatbuffers. >1 means flatbuffers is faster.
    breakdown: dict[str, float] = field(default_factory=dict)


def _timed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def _build_flatbuffers_event(builder, event_type: str, edge_id: str, timestamp: str, from_node: str, to_node: str):
    """Hand-write a FlatBuffer-like record without generating schemas.

    This uses the low-level ``flatbuffers.Builder`` API to avoid the
    schema-compilation step. In production we would generate Python
    classes via ``flatc`` — the audit only needs a representative
    serialize/deserialize cost.
    """
    import flatbuffers

    et = builder.CreateString(event_type)
    eid = builder.CreateString(edge_id)
    ts = builder.CreateString(timestamp)
    fn = builder.CreateString(from_node)
    tn = builder.CreateString(to_node)

    builder.StartObject(5)
    builder.PrependUOffsetTRelativeSlot(0, et, 0)
    builder.PrependUOffsetTRelativeSlot(1, eid, 0)
    builder.PrependUOffsetTRelativeSlot(2, ts, 0)
    builder.PrependUOffsetTRelativeSlot(3, fn, 0)
    builder.PrependUOffsetTRelativeSlot(4, tn, 0)
    return builder.EndObject()


def bench_event_store_serialization(*, n: int) -> AuditResult:
    import flatbuffers

    # Prepare representative records
    records = [
        {
            "event_type": "PROMOTED",
            "edge_id": f"rel-{i:06d}",
            "timestamp_utc": f"2026-04-15T10:00:{i % 60:02d}Z",
            "payload": {"from": f"law-{i}", "to": f"concept-{i}"},
        }
        for i in range(n)
    ]

    # JSON serialize-all-then-deserialize-all cycle
    def json_cycle():
        blobs = [json.dumps(r, sort_keys=True).encode("utf-8") for r in records]
        for b in blobs:
            json.loads(b)

    json_wall = _timed(json_cycle)

    # FlatBuffers equivalent
    def flatbuffers_cycle():
        builder = flatbuffers.Builder(1024)
        finished: list[bytes] = []
        for r in records:
            builder.Clear()
            root = _build_flatbuffers_event(
                builder,
                r["event_type"],
                r["edge_id"],
                r["timestamp_utc"],
                r["payload"]["from"],
                r["payload"]["to"],
            )
            builder.Finish(root)
            finished.append(bytes(builder.Output()))
        # Representative deserialize: just read the header bytes.
        for buf in finished:
            # Table root offset is at buf[0:4].
            if len(buf) < 4:
                raise RuntimeError("truncated flatbuffer")

    fb_wall = _timed(flatbuffers_cycle)
    ratio = json_wall / fb_wall if fb_wall > 0 else 0.0

    return AuditResult(
        site="event_store_serialization",
        n=n,
        json_wall_seconds=json_wall,
        flatbuffers_wall_seconds=fb_wall,
        speedup_ratio=ratio,
        breakdown={
            "json_bytes_per_record_estimate": (
                sum(len(json.dumps(r).encode("utf-8")) for r in records) / max(1, len(records))
            ),
        },
    )


def bench_verdict_cache_serialization(*, n: int) -> AuditResult:
    import flatbuffers

    records = [
        {
            "verdict": "keep" if i % 2 == 0 else "reject",
            "self_confidence": 0.5 + (i % 10) / 20.0,
            "created_utc": f"2026-04-15T10:00:{i % 60:02d}Z",
        }
        for i in range(n)
    ]

    def json_cycle():
        blobs = [json.dumps(r, sort_keys=True).encode("utf-8") for r in records]
        for b in blobs:
            json.loads(b)

    json_wall = _timed(json_cycle)

    def flatbuffers_cycle():
        builder = flatbuffers.Builder(256)
        finished: list[bytes] = []
        for r in records:
            builder.Clear()
            v = builder.CreateString(r["verdict"])
            ts = builder.CreateString(r["created_utc"])
            builder.StartObject(3)
            builder.PrependUOffsetTRelativeSlot(0, v, 0)
            builder.PrependFloat32Slot(1, r["self_confidence"], 0.0)
            builder.PrependUOffsetTRelativeSlot(2, ts, 0)
            root = builder.EndObject()
            builder.Finish(root)
            finished.append(bytes(builder.Output()))
        for buf in finished:
            if len(buf) < 4:
                raise RuntimeError("truncated flatbuffer")

    fb_wall = _timed(flatbuffers_cycle)
    ratio = json_wall / fb_wall if fb_wall > 0 else 0.0

    return AuditResult(
        site="verdict_cache_serialization",
        n=n,
        json_wall_seconds=json_wall,
        flatbuffers_wall_seconds=fb_wall,
        speedup_ratio=ratio,
        breakdown={
            "json_bytes_per_record_estimate": (
                sum(len(json.dumps(r).encode("utf-8")) for r in records) / max(1, len(records))
            ),
        },
    )


def compute_recommendation(*, event_store_ratio: float, verdict_cache_ratio: float) -> Recommendation:
    """Decision gate.

    GO: both ratios >= 2.0 (FlatBuffers >= 2x faster on both sites)
    DEFER: both ratios between 1.25 and 2.0 (worth revisiting at scale)
    NO_GO: either ratio < 1.25 (not worth the complexity cost)
    """
    if event_store_ratio >= 2.0 and verdict_cache_ratio >= 2.0:
        return "GO"
    if event_store_ratio >= 1.25 and verdict_cache_ratio >= 1.25:
        return "DEFER"
    return "NO_GO"


def result_as_json(result: AuditResult) -> dict:
    return {
        "site": result.site,
        "n": result.n,
        "json_wall_seconds": round(result.json_wall_seconds, 6),
        "flatbuffers_wall_seconds": round(result.flatbuffers_wall_seconds, 6),
        "speedup_ratio": round(result.speedup_ratio, 4),
        "breakdown": {k: round(v, 4) for k, v in result.breakdown.items()},
    }


if __name__ == "__main__":
    import argparse
    import datetime as dt
    import os

    parser = argparse.ArgumentParser(description="FlatBuffers audit harness")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--out", type=Path, default=Path(".ai/10_state/audit_flatbuffers_2026-04-15.json"))
    args = parser.parse_args()

    ev = bench_event_store_serialization(n=args.n)
    vc = bench_verdict_cache_serialization(n=args.n)
    rec = compute_recommendation(
        event_store_ratio=ev.speedup_ratio,
        verdict_cache_ratio=vc.speedup_ratio,
    )

    report = {
        "timestamp_utc": dt.datetime.utcnow().isoformat() + "Z",
        "n": args.n,
        "python_interpreter": os.sys.executable,
        "host": "darwin-arm64",
        "results": [result_as_json(ev), result_as_json(vc)],
        "decision_gate": {
            "event_store_ratio": round(ev.speedup_ratio, 4),
            "verdict_cache_ratio": round(vc.speedup_ratio, 4),
            "threshold_go": 2.0,
            "threshold_defer_lower": 1.25,
            "recommendation": rec,
            "notes": (
                f"FlatBuffers {'≥' if rec == 'GO' else '<'} 2x faster than JSON on "
                f"event_store_serialization ({round(ev.speedup_ratio, 2)}x) and "
                f"verdict_cache_serialization ({round(vc.speedup_ratio, 2)}x). "
                f"Decision: {rec}."
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
```

### Step 5: Run the smoke test (it should now pass)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_flatbuffers_audit.py -v
```

Expected: 2 passed.

### Step 6: Run the real audit at n=10000

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_flatbuffers_audit --n 10000
```

Expected: JSON report printed AND saved to `.ai/10_state/audit_flatbuffers_2026-04-15.json`. Both sites measured, ratios computed, recommendation emitted.

### Step 7: Full suite regression check

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: 1398 passed, 1 skipped (baseline 1396 + 2 new).

### Step 8: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/bench/bench_flatbuffers_audit.py \
  scripts/tests/test_flatbuffers_audit.py \
  .ai/10_state/audit_flatbuffers_2026-04-15.json
git commit -m "$(cat <<'EOF'
feat(audit): Task 1 — FlatBuffers audit harness + n=10000 verdict

Benchmarks json.dumps/loads vs. flatbuffers pack/read at the top
two serialization hot paths (event_store_serialization and
verdict_cache_serialization) with synthetic records matching the
shapes used by RocksDBEventStore.append and
RocksDBStatefulReviewRegistry.put.

Decision gate:
- GO if both sites >= 2x faster under flatbuffers
- DEFER if both between 1.25 and 2x (revisit at scale)
- NO_GO if either < 1.25

Audit output saved to .ai/10_state/audit_flatbuffers_2026-04-15.json.
Task 4 reads the recommendation field and only runs the implementation
if it says GO.

Part of the 2026-04-15 advanced tech audit plan at
.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Numerical Integrity Audit (Wave A)

**Goal:** Identify every point in the pipeline where data enters canonical storage without a cryptographic integrity commitment, measure the cost of adding BLAKE3 checksums at each such point, and decide whether BLAKE3 replaces or supplements SHA-256 on at least one hot path.

**Files:**
- Create: `scripts/vitruvius/bench/bench_integrity_audit.py` — benchmark harness comparing SHA-256 vs BLAKE3 on representative file sizes + the RocksDB value sizes
- Create: `.ai/10_state/audit_integrity_2026-04-15.json` — machine-readable audit output
- Create: `scripts/tests/test_integrity_audit.py` — smoke test

### Step 1: Install blake3

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip install blake3==0.4.1
/opt/homebrew/opt/python@3.11/bin/python3.11 -c "import blake3; print('blake3', blake3.__version__)"
```

Expected: `blake3 0.4.1`. Prebuilt wheel (no compile).

### Step 2: Write the failing smoke test

Create `scripts/tests/test_integrity_audit.py`:

```python
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
```

### Step 3: Run the test (fails)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_integrity_audit.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.bench.bench_integrity_audit'`.

### Step 4: Implement the audit harness

Create `scripts/vitruvius/bench/bench_integrity_audit.py`:

```python
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
from dataclasses import dataclass, field
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
```

### Step 5: Run the test (passes)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_integrity_audit.py -v
```

Expected: 2 passed.

### Step 6: Run the real audit

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_integrity_audit
```

Expected: JSON report with 3 benchmark rows + gap list + recommendation.

### Step 7: Full suite

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: 1400 passed, 1 skipped (1398 after Task 1 + 2 new).

### Step 8: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/bench/bench_integrity_audit.py \
  scripts/tests/test_integrity_audit.py \
  .ai/10_state/audit_integrity_2026-04-15.json
git commit -m "$(cat <<'EOF'
feat(audit): Task 2 — numerical integrity audit (SHA-256 vs BLAKE3 + gap analysis)

Two-part audit:
1. Benchmark SHA-256 vs BLAKE3 at 1KB / 64KB / 1MB sizes. Decision
   gate: GO_REPLACE if BLAKE3 >= 2.5x faster at 1MB; GO_SUPPLEMENT
   if 1.5-2.5x; NO_GO / GO_GAP otherwise.
2. Static enumeration of admission-gate sites with a
   has_integrity_check flag and a gap_severity tag. Two MEDIUM-or-
   higher gaps are likely: RocksDB values (LOW, deliberately not
   in threat model) and spatial-daemon contract file (MEDIUM,
   Python trusts it without verification).

Audit output saved to .ai/10_state/audit_integrity_2026-04-15.json.
Task 5 reads the recommendation field and ships the appropriate
remedy:
- GO_REPLACE: swap SHA-256 for BLAKE3 in scanner.py + merkle_fs.py
- GO_SUPPLEMENT: add BLAKE3 as the default for new hot paths
- GO_GAP: fix the spatial-daemon contract gap with SHA-256
- NO_GO: park the investigation; record findings in AD-030

Part of the 2026-04-15 advanced tech audit plan at
.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Monte Carlo Dropout Audit (Wave A)

**Goal:** Decide whether `compute_epistemic_uncertainty` has any viable production call site. Given the pre-audit finding that `graphsage.py:219` explicitly disables dropout, the prior is strongly "park the utility."

**Files:**
- Create: `.ai/10_state/audit_mc_dropout_2026-04-15.json` — audit output
- Create: `scripts/vitruvius/bench/audit_mc_dropout.py` — site-inventory script
- Create: `scripts/tests/test_mc_dropout_audit.py` — smoke test

No benchmark harness needed — this audit is fundamentally a SITE SURVEY. The only thing to measure is: does any neural inference module in our repo run dropout at inference time? If yes, measure its uncertainty quality. If no, document and park.

### Step 1: Write the failing smoke test

Create `scripts/tests/test_mc_dropout_audit.py`:

```python
"""Smoke test for the MC Dropout audit."""
from __future__ import annotations

from pathlib import Path


def test_mc_dropout_audit_survey_runs(tmp_path: Path) -> None:
    from vitruvius.bench.audit_mc_dropout import (
        MCDropoutAuditResult,
        survey_neural_inference_sites,
        compute_recommendation,
    )

    sites = survey_neural_inference_sites()
    assert isinstance(sites, list)
    # The audit must return at least the GraphSAGE entry, which is
    # the only neural module in the repo.
    assert any(s["file"].endswith("graphsage.py") for s in sites)

    # Each site must carry the dropout_enabled_at_inference flag.
    for s in sites:
        assert "dropout_enabled_at_inference" in s
        assert isinstance(s["dropout_enabled_at_inference"], bool)

    result = MCDropoutAuditResult(
        viable_sites=[s for s in sites if s["dropout_enabled_at_inference"]],
        surveyed_sites=sites,
    )
    assert isinstance(result.viable_sites, list)


def test_mc_dropout_recommendation() -> None:
    from vitruvius.bench.audit_mc_dropout import compute_recommendation

    # No viable sites → PARK
    assert compute_recommendation(viable_site_count=0) == "PARK"
    # One viable site → GO (wire it in)
    assert compute_recommendation(viable_site_count=1) == "GO"
    # Multiple viable sites → GO
    assert compute_recommendation(viable_site_count=3) == "GO"
```

### Step 2: Run the test (fails)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_mc_dropout_audit.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

### Step 3: Create the survey module

Create `scripts/vitruvius/bench/audit_mc_dropout.py`:

```python
"""Sprint AUDIT-1 — MC Dropout production-site survey.

Monte Carlo dropout (Gal & Ghahramani 2016) estimates epistemic
uncertainty by running a dropout-enabled model N times at inference
and taking the sample variance of its predictions. This only works
if the model actually has dropout layers that are ACTIVE at inference
time. Most production PyTorch code disables dropout via ``model.eval()``.

This audit walks every neural-inference module we ship and reports
whether it qualifies as a MC-dropout call site. As of 2026-04-15
the only neural module is ``scripts/vitruvius/graph/graphsage.py``,
and line 219 of that file explicitly states: "Deterministic forward
pass — no dropout, no training loop."

So the audit's expected output is: **viable_site_count == 0 → PARK
the compute_epistemic_uncertainty utility**. But we still do the
survey explicitly, and the site list gives us a checklist to update
whenever we add a new neural module in the future.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Recommendation = Literal["GO", "PARK"]


@dataclass(frozen=True)
class MCDropoutAuditResult:
    viable_sites: list[dict]
    surveyed_sites: list[dict]


def survey_neural_inference_sites() -> list[dict]:
    """Hand-curated list of neural-inference modules in the repo.

    Maintained in this file. If you add a new neural module,
    append to this list with the correct `dropout_enabled_at_inference`
    flag. The smoke test requires GraphSAGE to be present.
    """
    return [
        {
            "file": "scripts/vitruvius/graph/graphsage.py",
            "model_type": "GraphSAGE (custom stdlib + numpy impl)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "graphsage.py:219 explicitly says 'Deterministic forward pass — "
                "no dropout, no training loop.' The aggregator is a simple mean-"
                "pooling over neighbour embeddings with no dropout layers."
            ),
            "sprint": "HP.5",
        },
        {
            "file": "scripts/vitruvius/review/naive_bayes_filter.py",
            "model_type": "Multinomial Naive Bayes (closed-form, not neural)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "Naive Bayes is a probabilistic classifier with no hidden layers "
                "and no dropout concept. MC dropout is inapplicable."
            ),
            "sprint": "Q-W2",
        },
        {
            "file": "scripts/vitruvius/extraction/crf_trainer.py",
            "model_type": "Linear-chain CRF",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "CRFs are discriminative sequence models with no neural dropout. "
                "The uncertainty signal here is the marginal probability from the "
                "forward-backward algorithm, not MC dropout."
            ),
            "sprint": "D-E",
        },
        {
            "file": "scripts/vitruvius/extraction/kg_link_predictor.py",
            "model_type": "TransE-family link predictor",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "TransE uses learned entity and relation embeddings; inference is "
                "a vector arithmetic score. No dropout in the inference path."
            ),
            "sprint": "D-E",
        },
        {
            "file": "scripts/vitruvius/ollama_review.py",
            "model_type": "Remote LLM (Ollama)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "Ollama exposes a completion API — it does not expose a "
                "dropout-at-inference knob to clients. Even if it did, running "
                "the same prompt N times with a non-zero temperature gives "
                "different samples, but that is aleatoric sampling variance, "
                "not MC dropout. Alternative uncertainty signals for LLM "
                "review are provided by the Sprint Q W2 conformal gate and the "
                "self_confidence field parsed from the response."
            ),
            "sprint": "6A",
        },
    ]


def compute_recommendation(*, viable_site_count: int) -> Recommendation:
    """MC Dropout is a wiring task. Without a viable site, it has no work to do."""
    if viable_site_count >= 1:
        return "GO"
    return "PARK"


if __name__ == "__main__":
    import argparse
    import datetime as dt

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(".ai/10_state/audit_mc_dropout_2026-04-15.json"))
    args = parser.parse_args()

    sites = survey_neural_inference_sites()
    viable = [s for s in sites if s["dropout_enabled_at_inference"]]
    rec = compute_recommendation(viable_site_count=len(viable))

    report = {
        "timestamp_utc": dt.datetime.utcnow().isoformat() + "Z",
        "python_interpreter": os.sys.executable,
        "host": "darwin-arm64",
        "surveyed_sites": sites,
        "viable_sites": viable,
        "viable_site_count": len(viable),
        "utility_path": "scripts/vitruvius/graph/mc_dropout.py",
        "utility_production_call_sites": 0,
        "decision_gate": {
            "recommendation": rec,
            "notes": (
                f"{len(viable)} viable MC-dropout site(s) found out of {len(sites)} "
                f"neural-inference modules surveyed. "
                f"{'Ship the wiring in Task 6.' if rec == 'GO' else 'Park the utility; it stays available but unused.'}"
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
```

### Step 4: Run the tests (pass)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_mc_dropout_audit.py -v
```

Expected: 2 passed.

### Step 5: Run the real survey

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.audit_mc_dropout
```

Expected: JSON report printed AND saved to `.ai/10_state/audit_mc_dropout_2026-04-15.json`. Given the pre-audit evidence, the recommendation should be `PARK`.

### Step 6: Full suite

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: 1402 passed, 1 skipped (baseline 1400 after Task 2 + 2 new).

### Step 7: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/bench/audit_mc_dropout.py \
  scripts/tests/test_mc_dropout_audit.py \
  .ai/10_state/audit_mc_dropout_2026-04-15.json
git commit -m "$(cat <<'EOF'
feat(audit): Task 3 — Monte Carlo Dropout production-site survey

Hand-curated inventory of all 5 neural-inference modules in the
repo plus their dropout-at-inference status. The expected finding
(and pre-audit prior): GraphSAGE explicitly disables dropout in
its forward pass, NB / CRF / TransE are non-neural, and Ollama
doesn't expose a dropout knob to clients.

Decision gate:
- GO if any site has dropout_enabled_at_inference=true (wire it in)
- PARK otherwise (the compute_epistemic_uncertainty utility stays
  as a checked-in library ready for use whenever we do add a
  dropout-enabled neural module)

Audit output saved to .ai/10_state/audit_mc_dropout_2026-04-15.json.
Task 6 reads the recommendation field and only runs the wiring if
it says GO.

Part of the 2026-04-15 advanced tech audit plan at
.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: FlatBuffers Implementation (Wave B — conditional on Task 1 recommendation)

**Gate:** Read `.ai/10_state/audit_flatbuffers_2026-04-15.json` and inspect `decision_gate.recommendation`:
- `GO` → execute Steps 1-10 below
- `DEFER` → skip implementation; AD-030 records the defer
- `NO_GO` → skip implementation; AD-030 records the rejection

If skipping, immediately move to Task 5.

### If `GO`, implementation sketch (flesh out with real FlatBuffers schemas during execution)

**Files to create:**
- `scripts/vitruvius/graph/event_store_fb.fbs` — FlatBuffers schema for the event record
- `scripts/vitruvius/graph/event_store_fb_generated.py` — `flatc`-generated Python bindings
- `scripts/vitruvius/review/verdict_cache_fb.fbs` — schema for verdict records
- `scripts/vitruvius/review/verdict_cache_fb_generated.py` — generated bindings
- `scripts/tests/test_event_store_fb_roundtrip.py` — roundtrip + migration-compat tests
- `scripts/tests/test_verdict_cache_fb_roundtrip.py` — same

**Files to modify:**
- `scripts/vitruvius/graph/rocksdb_event_store.py` — add a `wire_format` field on the class (`"json"` default, `"flatbuffers"` when flag `hp_flatbuffers_event_store` is on), branching on the format inside `append()` and `project_graph_at_rocksdb`. The JSON path stays as the fallback.
- `scripts/vitruvius/review/rocksdb_stateful_registry.py` — same pattern with flag `hp_flatbuffers_verdict_cache`
- `config/vitruvius.yaml` — add the two new flags, default `false`
- `scripts/tests/test_features.py::EXPECTED_FLAGS` — register both flags

**Key invariant:** RocksDB values written under the FlatBuffers format must be distinguishable from JSON values (use a 1-byte format tag prefix: `0x4A` for JSON, `0x46` for FlatBuffers). This lets a migrated database be read by either code path safely.

**Decision gate for default flip:** after the Task 4 implementation ships, re-run the Task 1 audit with the real (not synthetic) RocksDB integration in place. If the end-to-end speedup on the Task 8 KV bench pattern is ≥2×, flip the `hp_flatbuffers_*` flags to `true`. Otherwise keep them `false` and document in AD-030.

**Out of scope for this task:**
- FlatBuffers for the spatial-daemon contract file (that's a TypeScript + Python parallel-implementation and would need a separate plan)
- FlatBuffers for the event store SECONDARY INDEX (ts: prefix keys) — keep those as raw bytes, no serialization overhead exists today
- FlatBuffers for audit logs, config files, or CoT audit dumps — human-readable is required

Because the content of Task 4 is conditional on the Task 1 audit verdict, I'm not expanding every TDD step here — the executing agent must generate the schemas from the `flatc` CLI at execution time (FlatBuffers requires schemas to be compiled to Python bindings and the generated code is too long to inline in this plan). Use the pattern from Sprint HP.3-R Task 4 (RocksDBEventStore implementation) as a template for the class-level shape, the feature-flag wiring, and the test coverage.

### Commit message template (when executing)

```
feat(perf): Sprint AUDIT-1 Task 4 — FlatBuffers wire format for RocksDB KV

Adds FlatBuffers schemas + generated Python bindings + RocksDB
value-format tagging behind two feature flags (hp_flatbuffers_event_store
and hp_flatbuffers_verdict_cache). JSON remains the default; flipping
the flag switches the write format for new records. Old records are
still readable via the 1-byte format tag prefix.

End-to-end bench on the Task 8 KV workload: [FILL with real numbers
from the re-run audit].

Part of the 2026-04-15 advanced tech audit plan at
.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md.
```

---

## Task 5: Numerical Integrity Implementation (Wave B — conditional on Task 2)

**Gate:** Read `.ai/10_state/audit_integrity_2026-04-15.json::decision_gate.recommendation`:
- `GO_REPLACE` → swap SHA-256 for BLAKE3 on file-hash paths
- `GO_SUPPLEMENT` → add BLAKE3 as the default for new hot paths (spatial-daemon contract file signature)
- `GO_GAP` → fix the open MEDIUM+ gaps using the existing SHA-256 toolchain
- `NO_GO` → skip; AD-030 records the rejection

### Sub-task 5A: GO_REPLACE branch (only if recommendation is GO_REPLACE)

**Files to modify:**
- `scripts/vitruvius/scanner.py::_sha256_of_file` → add a sibling `_blake3_of_file` and gate on flag `hp_blake3_file_hash` (default `false` initially)
- `scripts/vitruvius/models.py::FileEntry` → add an optional `blake3: str | None = None` field; `sha256` stays as the authoritative identifier for backward compat
- `scripts/vitruvius/merkle_fs.py` → add BLAKE3 mode gated on `hp_blake3_merkle`
- `config/vitruvius.yaml` + `test_features.py::EXPECTED_FLAGS` — register flags
- New tests: `test_scanner_blake3.py`, `test_merkle_fs_blake3.py` — exact parity with the SHA-256 versions

**Migration:** the new flag is OFF by default — the audit recommendation to default-ON comes in Task 7 (AD-030) based on observed production usage.

### Sub-task 5B: GO_GAP branch (only if recommendation is GO_GAP or GO_SUPPLEMENT)

The known MEDIUM gap is `spatial-daemon/src/contract_writer.ts`. Close it:

**Files to modify:**
- `spatial-daemon/src/contract_writer.ts` → append a SHA-256 signature line to the contract file (`# sha256: <hex>` footer)
- `spatial-daemon/src/contract_writer.test.ts` → verify footer presence and correctness
- Create `scripts/vitruvius/spatial/contract_reader.py` → a Python-side reader that parses the contract file AND verifies the SHA-256 footer; raises `IntegrityError` on mismatch
- `scripts/tests/test_spatial_contract_reader.py` — happy path + corrupted-body regression

This sub-task is the most likely to actually ship because the gap is real and the fix is small. If both Task 2 audit and the MEDIUM gap exist, prioritize this over 5A.

### Sub-task 5C: NO_GO branch

Skip the task. AD-030 records that the integrity surface is already comprehensive and no changes are warranted.

---

## Task 6: Monte Carlo Dropout Implementation (Wave B — conditional on Task 3)

**Gate:** Read `.ai/10_state/audit_mc_dropout_2026-04-15.json::decision_gate.recommendation`:
- `GO` → wire `compute_epistemic_uncertainty` into the viable site
- `PARK` → skip; AD-030 documents that the utility is a parked library ready for future use

**Expected outcome:** `PARK`, based on the pre-audit evidence that our only neural module (GraphSAGE) is deterministic by design. Task 6 therefore almost certainly does nothing.

**If somehow `GO`:** use the pattern from `scripts/vitruvius/graph/mc_dropout.py` — feed it a sequence of predictions from repeated dropout-enabled inference and store the returned variance alongside the prediction. The wiring will be specific to whichever model the audit found viable and cannot be spelled out in advance.

---

## Task 7: AD-030 + state sync + plan archival (Wave C — orchestrator only)

**Files:**
- Modify: `.ai/10_state/decisions.md` — append AD-030 summarizing the 3 audit verdicts + any implementation deltas
- Modify: `.ai/03_plans/INDEX.md` — add a META row for this plan with the `✅ Complete (archived)` status
- Move: `.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md` → `.ai/09_archive/plans/`
- Optional modify: `.ai/00_system/architecture.md` — mention any newly-shipped tech (BLAKE3, FlatBuffers, etc.)

### Step 1: Draft AD-030 using the real audit outputs

Template (fill all `[FILL]` with real numbers before committing — non-negotiable, same discipline as AD-029):

```markdown

## AD-030 — Advanced Tech Audit (FlatBuffers / Integrity / MC Dropout) (2026-04-15)

**Context.** After the Sprint HP.3-R RocksDB migration (AD-029) flipped defaults to true and delivered measured 18.7× / 24.3× wins on the two KV backends, the user asked whether three additional advanced technologies — FlatBuffers (zero-copy serialization), numerical integrity checks at the admission gate, and Monte Carlo Dropout uncertainty — would produce further wins.

The instruction was explicit: **study first, only ship if the code will be measurably better, more optimized, and yield more accurate results**. This AD records the three audits and the resulting ship decisions.

**Audit 1 — FlatBuffers.**

Benchmark: `json.dumps`+`json.loads` vs `flatbuffers` pack+read at the two hottest serialization sites (event_store_serialization and verdict_cache_serialization) at n=10000.

| Site | JSON wall (s) | FlatBuffers wall (s) | Speedup |
|---|---|---|---|
| event_store_serialization | [FILL] | [FILL] | [FILL]× |
| verdict_cache_serialization | [FILL] | [FILL] | [FILL]× |

Decision gate: GO if both ≥2×, DEFER if both 1.25–2×, NO_GO otherwise. **Verdict: [FILL]**.

[FILL with a one-paragraph narrative: either "we shipped FlatBuffers behind flags" or "we did not ship because the JSON path is already fast enough at our scale", with the specific numbers.]

**Audit 2 — Numerical integrity.**

Benchmark: SHA-256 vs BLAKE3 at 1 KB, 64 KB, 1 MB payloads. At 1 MB BLAKE3 was [FILL]× faster than SHA-256.

Static admission-gate gap analysis: surveyed 8 sites, [FILL] with open MEDIUM+ gaps. The MEDIUM gap observed at plan-write time was the spatial-daemon TypeScript → Python contract file, which Python reads without verifying.

Decision gate: GO_REPLACE / GO_SUPPLEMENT / GO_GAP / NO_GO. **Verdict: [FILL]**.

[FILL with a narrative: what shipped, what didn't, and why.]

**Audit 3 — Monte Carlo Dropout.**

Site survey: 5 neural-inference modules surveyed. Viable MC-dropout sites (dropout_enabled_at_inference=true): [FILL].

Key finding (documented in advance): `graphsage.py:219` explicitly says "Deterministic forward pass — no dropout, no training loop." GraphSAGE is our only dropout-adjacent neural module and it does not use dropout at inference. NB / CRF / TransE are non-neural; Ollama doesn't expose dropout-at-inference to clients.

Decision gate: GO if any viable site, PARK otherwise. **Verdict: [FILL]**.

The `compute_epistemic_uncertainty` utility in `scripts/vitruvius/graph/mc_dropout.py` [FILL: remains parked as a checked-in library / was wired into site X].

**Bundled lessons.**

- Audit-first, ship-conditionally is the right default for speculative perf work at our scale. Sprint HP.3-R taught us that **benchmarks are load-bearing** — the initial HP.3-R bench showed RocksDB 9.6× SLOWER because of an O(n²) test artifact; only after the O(1) count() fix did the real 18.7×/24.3× wins appear. Audits save us from shipping phantom "improvements" that look good on intuition and fail under measurement.
- The `NO_GO` / `PARK` outcomes are just as valuable as a shipped feature — they document "we considered this and here's why it doesn't pay off right now," preventing the same investigation from repeating in a future session.
- FlatBuffers, BLAKE3, and MC dropout are all tools whose payoff depends on workload shape. At our current scale (~2-10k events per session) most sophisticated tools are overkill; our real bottleneck is correctness and audit trail, not throughput.

**Commits.**
- Task 1 — `[FILL]` — FlatBuffers audit
- Task 2 — `[FILL]` — Integrity audit
- Task 3 — `[FILL]` — MC Dropout audit
- Task 4 — `[FILL or "skipped per verdict"]`
- Task 5 — `[FILL or "skipped per verdict"]`
- Task 6 — `[FILL or "skipped per verdict"]`
- Task 7 — `[this commit]`

**Follow-ups.**
- When we next add a neural module (e.g. a dropout-enabled variant of the NB prefilter), re-evaluate the MC Dropout audit.
- When the canonical relationship count crosses 100k, re-run Task 1 (FlatBuffers) — the per-record overhead that looks trivial at 10k may dominate at 1M.
- If `spatial-daemon` starts shipping large contract files (>100KB), re-evaluate integrity checks and FlatBuffers for that path.
```

### Step 2: Update INDEX.md

Add a new META row after the docs-cleanup row:

```
| META | `advanced-tech-audit-2026-04-15` | **Advanced Tech Audit** — FlatBuffers / numerical integrity / MC Dropout. Decision-gated implementation. | ✅ Complete (archived 2026-04-15) | Sprint AUDIT-1 — closed | audit_then_conditional_implementation | [../09_archive/plans/2026-04-15-advanced-tech-audit-plan.md](../09_archive/plans/2026-04-15-advanced-tech-audit-plan.md) |
```

### Step 3: Archive the plan

```bash
cd /Users/philiplewis/vitruvius && git mv .ai/03_plans/2026-04-15-advanced-tech-audit-plan.md .ai/09_archive/plans/
```

### Step 4: Final commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  .ai/10_state/decisions.md \
  .ai/03_plans/INDEX.md \
  .ai/09_archive/plans/2026-04-15-advanced-tech-audit-plan.md
# Also add any Task 4/5/6 implementation artifacts that were created
# along the way. `git status` before staging to verify scope.
git commit -m "$(cat <<'EOF'
docs(audit): Sprint AUDIT-1 closure — AD-030 + plan archival

Sprint AUDIT-1 (advanced tech audit) closed. Three parallel audits
produced measured verdicts on FlatBuffers, numerical integrity
checks, and Monte Carlo Dropout. AD-030 records the findings.

Verdicts (see AD-030 for the numbers):
- FlatBuffers: [FILL]
- Numerical integrity: [FILL]
- Monte Carlo Dropout: [FILL]

Audit output files remain in .ai/10_state/ as raw data:
- audit_flatbuffers_2026-04-15.json
- audit_integrity_2026-04-15.json
- audit_mc_dropout_2026-04-15.json

Plan archived to .ai/09_archive/plans/. INDEX.md has a new META
row pointing at the archive location.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Tag the closure (optional)**

```bash
cd /Users/philiplewis/vitruvius && git tag sprint-audit-1-closed HEAD -m "Sprint AUDIT-1 — advanced tech audit closed; see AD-030"
```

---

## Self-Review

**1. Spec coverage.** The user asked for (a) whether we should use FlatBuffers / numerical lock algorithms / MC dropout, (b) an audit + implementation plan, (c) implement only if the tech makes the code measurably better.

- ✅ FlatBuffers — Task 1 audits, Task 4 conditionally implements
- ✅ Numerical integrity (= "numerical lock algorithms" translated to specific mechanisms) — Task 2 audits, Task 5 conditionally implements with 3 branches
- ✅ MC Dropout — Task 3 audits, Task 6 conditionally implements (with expected PARK verdict)
- ✅ Decision gates are numeric, not vibes-based — every audit output has a `decision_gate.recommendation` field that the implementation tasks read programmatically
- ✅ Task 7 records the findings in AD-030 regardless of outcome

**2. Placeholder scan.** The only `[FILL]` placeholders are in AD-030 and the Task 4 commit message template, both explicitly flagged as "must be replaced with real numbers from the audit before commit." This matches the AD-029 pattern which used the same discipline. No hidden TBDs.

**3. Type consistency.** The three `Recommendation` Literal types are defined per-audit (FlatBuffers uses `GO | DEFER | NO_GO`; integrity uses `GO_REPLACE | GO_SUPPLEMENT | GO_GAP | NO_GO`; MC Dropout uses `GO | PARK`). Intentional — each audit has different decision semantics. The test cases in Steps 2-3 of each audit task assert the expected verdicts for each branch, so drift between code and test would surface immediately.

**4. Parallelism.** Wave A tasks are file-disjoint (each audit writes its own bench file + test file + JSON output) and can run in parallel. Wave B tasks serialize because each reads the output of its corresponding audit. Wave C is orchestrator-only.

**5. Test suite arithmetic.** Starting from 1396, the audit tasks add tests as:
- Task 1: +2 → 1398
- Task 2: +2 → 1400
- Task 3: +2 → 1402

Conditional implementation tasks add more tests based on what ships. The final Task 7 commit makes no test changes.

---

## Execution Handoff

Plan saved to `.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Wave A runs 3 parallel audit subagents; Wave B runs up to 3 serial conditional-implementation subagents based on the Wave A verdicts; Wave C is one orchestrator-held closure. Per-task two-stage review (spec + quality) as usual.

**2. Inline Execution** — I run the three audits in this session, read the verdicts, execute whichever implementation tasks passed the decision gates, and commit at the end.

Option 1 is closer to the "path closest to perfection, fewer errors" discipline we used on Sprint HP.3-R and is what I'd recommend unless you want the audits done quickly.

Either way, **the most likely outcome is**:
- FlatBuffers audit → likely `NO_GO` or `DEFER` (JSON is fast enough at our scale; pyobject serialization is already hand-optimized by CPython)
- Integrity audit → likely `GO_GAP` (the spatial-daemon contract file is a real gap worth fixing; SHA-256 replacement with BLAKE3 may or may not win)
- MC Dropout audit → almost certainly `PARK` (our only neural module is deterministic by design)

That means Task 5's sub-task 5B (spatial-daemon contract signature) is probably the only thing that actually ships. Everything else records "we measured, it doesn't pay off, parked for later." That's a feature of audit-first engineering, not a bug — the parked investigations become future-session context that prevents re-litigating the same questions.

Which approach do you want?
