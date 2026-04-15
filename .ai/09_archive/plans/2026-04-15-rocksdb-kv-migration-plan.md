---
plan_id: rocksdb-kv-migration
phase: 13
title: SQLite → RocksDB KV Backend Migration (HP.3 spec compliance)
status: active
priority: medium
sprint: "Sprint HP.3-R (follow-on to Sprint HP)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - rocksdb 11.x installed at system level (verified: brew has `rocksdb 11.0.4`)
  - rocksdict-compatible Python wheel available for Apple Silicon py311 (verified: `rocksdict 0.3.29` ships `cp311-cp311-macosx_11_0_arm64.whl`)
  - Sprint HP closed (tag `sprint-hp-closed`) — HP.3 currently uses SQLite as a forced pivot
  - Sprint R closed (tag `sprint-r-closed`) — Stream Y4 stateful verdict cache currently uses SQLite
related_plans:
  - ../09_archive/plans/phase-13-high-performance-optimizations-plan.md (original HP.3 RocksDB spec)
  - ../09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md (Stream Y4 stateful registry)
supersedes: none
---

# SQLite → RocksDB KV Backend Migration (HP.3 Spec Compliance)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the two SQLite-backed KV stores in the project (`graph/event_store.py` and `review/stateful_registry.py`) with RocksDB-backed implementations behind feature flags, preserving the SQLite paths as fallbacks, and proving via benchmark whether RocksDB is actually faster for our workload before flipping defaults.

**Architecture:** Flag-gated parallel implementations. Write a `RocksDBEventStore` class with the same public API as `EventStore`, and a `RocksDBStatefulReviewRegistry` class with the same public API as `StatefulReviewRegistry`. Add `hp_rocksdb_event_store` + `hp_rocksdb_verdict_cache` feature flags. Add factory functions that read the flags and return the right backend. Write a migration CLI (`ple-kv-migrate`) that copies existing SQLite state into RocksDB. Add a bench harness that measures SQLite vs RocksDB on the target workload so we know whether the migration is actually a win. Keep the SQLite code path intact as the fallback until the bench + a week of flag-on operation validate the switch.

**Tech Stack:**
- `rocksdict 0.3.29` — modern Rust-based Python binding with prebuilt wheels for Apple Silicon Python 3.11. NOT `python-rocksdb` (Cython, no wheel — this is what HP.3 pivoted away from in 2026-04-15).
- `rocksdb 11.x` via `brew install rocksdb` — already installed at `/opt/homebrew/lib/`.
- stdlib `sqlite3` — kept as fallback backend.
- Existing test infra: pytest + `scripts/tests/test_graph_event_store.py` + `test_review_stateful_registry.py` as baseline coverage to mirror.

---

## Scope & Non-Goals

### In scope
1. **New backend classes** — `RocksDBEventStore` mirrors `EventStore`; `RocksDBStatefulReviewRegistry` mirrors `StatefulReviewRegistry`. Same public method signatures, same semantics, different storage.
2. **Feature flags** — `hp_rocksdb_event_store` + `hp_rocksdb_verdict_cache`, both default false.
3. **Factory functions** — `make_event_store()` + `make_stateful_registry()` dispatch on the flag.
4. **Migration CLI** — `ple-kv-migrate --store event|registry [--dry-run] [--source PATH] [--dest PATH]` reads SQLite and writes RocksDB.
5. **Benchmark harness** — `scripts/vitruvius/bench/bench_kv_backends.py` measures append rate, point lookup, time-travel projection, and verdict put/get roundtrip on both backends. Records numbers to `.ai/10_state/decisions.md` as AD-029.
6. **Integration switchpoints** — update consumers in `compound/differential_propagator.py` and `ollama_review.py` to use the factory.
7. **Docs sync** — update `architecture.md`, `known_issues.md`, add AD-029.

### Out of scope
- Deleting the SQLite backends. They stay as fallbacks. A follow-up plan can archive them after the RocksDB path has been stable for at least one week of real use.
- Adding any new RocksDB-only features (column families, TTL, checkpoints, incremental backup). We match the existing API exactly; advanced features are a separate effort.
- Migrating any other storage (no other module uses sqlite3 in this repo — grep confirms).
- Performance promises. We explicitly do not assume RocksDB will be faster at our current scale (~2k-10k events per session, ~100-500 verdict cache entries). The bench task exists to **measure** whether the assumption holds. If RocksDB is ≥2× faster on the target workload, we flip defaults in Task 9. If it's within 25% of SQLite, we keep it feature-flagged off and document that the migration was a spec-compliance pass, not a perf win. If it's slower, we halt and investigate.

---

## Why This Plan Exists

The Sprint HP closure (2026-04-15) includes AD-028's note that **HP.3 was pivoted from RocksDB to SQLite because no `python-rocksdb` wheel was available for Apple Silicon Python 3.11 at the time.** The archived Phase 13 plan (`.ai/09_archive/plans/phase-13-high-performance-optimizations-plan.md` §3) still specifies:

> **Event Store:** `RocksDB` (via `python-rocksdb`).

The pivot was a documented compromise — not a design change. The user has now installed `rocksdb 11.0.4` at the system level and confirmed they want to complete the originally-spec'd migration. We have independently verified that:

- `rocksdict 0.3.29` ships a `cp311-cp311-macosx_11_0_arm64.whl` (the blocker on 2026-04-15 is resolved — just with a different binding than the original spec).
- Both SQLite users are small, bounded, well-tested modules (168 + 172 lines; 4 test files; 1364 / 1364 tests currently green).
- The SQLite schemas are simple enough to translate 1:1 to RocksDB key-value pairs without feature loss.

**Scale context for the performance question:** For the current PD 1096 corpus the event store holds ~2-10k events per session and the verdict cache holds ~100-500 entries. At these sizes SQLite in WAL mode is already competitive with RocksDB. The real RocksDB win would show up at the 100k+ events scale we'll hit when Sprint D Streams J + K unblock and we ingest a second jurisdiction. This plan is effectively pre-positioning: we pay the migration cost now while the test surface is small and well-understood, so we don't have to do it under load later.

---

## File Structure

### New files
| Path | Purpose |
|---|---|
| `scripts/vitruvius/graph/rocksdb_event_store.py` | `RocksDBEventStore` class with `EventStore`-compatible API + `project_graph_at_rocksdb()` helper |
| `scripts/vitruvius/review/rocksdb_stateful_registry.py` | `RocksDBStatefulReviewRegistry` class with `StatefulReviewRegistry`-compatible API |
| `scripts/vitruvius/bench/bench_kv_backends.py` | Benchmark harness; measures both backends on the target workload |
| `scripts/vitruvius/kv_migrate.py` | `run_kv_migrate()` CLI handler for `ple-kv-migrate` |
| `scripts/tests/test_rocksdb_event_store.py` | Parallel coverage of `test_graph_event_store.py` against the RocksDB backend |
| `scripts/tests/test_rocksdb_stateful_registry.py` | Parallel coverage of `test_review_stateful_registry*.py` against the RocksDB backend |
| `scripts/tests/test_kv_factory_switches.py` | Verify the factory functions dispatch on the flag correctly |
| `scripts/tests/test_kv_migrate_cli.py` | CLI handler test |
| `scripts/tests/test_bench_kv_backends.py` | Smoke test that the bench harness runs end-to-end |

### Modified files
| Path | Reason |
|---|---|
| `scripts/vitruvius/graph/event_store.py` | Add `make_event_store()` factory (reads flag, returns SQLite or RocksDB backend) |
| `scripts/vitruvius/review/stateful_registry.py` | Add `make_stateful_registry()` factory (reads flag, returns SQLite or RocksDB backend) |
| `scripts/vitruvius/compound/differential_propagator.py` | Consume the factory instead of constructing `EventStore` directly (only if it constructs one today — verify first) |
| `scripts/vitruvius/ollama_review.py` | Consume `make_stateful_registry()` instead of `StatefulReviewRegistry` directly |
| `scripts/pipeline_cli.py` | Register `ple-kv-migrate` subcommand |
| `config/vitruvius.yaml` | Add `features.hp_rocksdb_event_store: false` + `features.hp_rocksdb_verdict_cache: false` |
| `scripts/tests/test_features.py` | Add the two new flags to `EXPECTED_FLAGS` |
| `.ai/00_system/architecture.md` | Note RocksDB migration alongside the HP.3 entry |
| `.ai/10_state/known_issues.md` | Add closure note for the "HP.3 forced pivot" observation |
| `.ai/10_state/decisions.md` | Add AD-029 with the final bench numbers + flip decision |

### Files explicitly NOT touched
- `scripts/vitruvius/graph/temporal_query.py` — reads the projected graph via `project_graph_at()`, doesn't care about storage.
- `scripts/vitruvius/graph/parquet_archiver.py` — Parquet path, unrelated.
- All Sprint GT / Sprint PHYS / Sprint Z / Sprint GEOM / Sprint WIKI code — unrelated.
- Any non-Python file.

---

## Dispatch Waves (Parallelism Map)

| Wave | Tasks | Files touched | Parallel-safe? |
|---|---|---|---|
| A | 1, 2, 3 | bench file / dependency install / config+test registry | ✅ yes — three disjoint agents |
| B | 4, 5 | `rocksdb_event_store.py` + tests / `rocksdb_stateful_registry.py` + tests | ✅ yes — different subpackages |
| C | 6 | factory wiring across event_store.py + stateful_registry.py + ollama_review.py + differential_propagator.py | ❌ single agent (multi-file coordination) |
| D | 7, 8 | migration CLI / bench run | ✅ yes (CLI and bench don't collide) |
| E | 9 | docs + AD-029 + final commit | ❌ orchestrator-held |

---

## Task 1: Baseline benchmark on SQLite (Wave A — parallel-safe)

**Why:** We need a measured number to beat before we can claim RocksDB is a win. This task gets us an honest SQLite baseline for the same workload we'll run against RocksDB in Task 8.

**Files:**
- Create: `scripts/vitruvius/bench/bench_kv_backends.py`
- Create: `scripts/tests/test_bench_kv_backends.py`

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_bench_kv_backends.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_bench_kv_backends.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.bench.bench_kv_backends'` or `ImportError: cannot import name 'BenchResult'`.

- [ ] **Step 3: Create the bench harness**

Create `scripts/vitruvius/bench/bench_kv_backends.py`:

```python
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
```

Also create `scripts/vitruvius/bench/__init__.py` if it doesn't exist (the dir already exists from Sprint Q W4, so `__init__.py` should be present — verify with `ls scripts/vitruvius/bench/__init__.py`).

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_bench_kv_backends.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Record the SQLite baseline numbers**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_kv_backends --n 10000`
Expected: two JSON blocks printed to stdout — one for event_store, one for verdict_cache. Copy these numbers into the scratch file `.ai/10_state/bench_sqlite_baseline.json` (create if missing). They will be compared against RocksDB numbers in Task 8.

If `PYTHONPATH` is required, run: `PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_kv_backends --n 10000`

- [ ] **Step 6: Stage files (do NOT commit — orchestrator commits in Wave E)**

Files changed:
- `scripts/vitruvius/bench/bench_kv_backends.py` (new)
- `scripts/tests/test_bench_kv_backends.py` (new)
- `.ai/10_state/bench_sqlite_baseline.json` (new — scratch, deletable in final cleanup)

---

## Task 2: Install `rocksdict` Python binding + smoke test (Wave A — parallel-safe)

**Why:** The blocker that forced the HP.3 SQLite pivot was that no Python binding was available. Now we need to verify the modern Rust-based binding (`rocksdict`) installs cleanly and can open a DB.

**Files:**
- Create: `scripts/tests/test_rocksdict_smoke.py` (temporary — will be absorbed by Task 4/5 test suites later)
- Modify: `requirements.txt` or equivalent dependency manifest if present

- [ ] **Step 1: Verify rocksdict wheel availability**

Run: `/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip index versions rocksdict 2>&1 | head -3`
Expected: line containing `rocksdict (0.3.29)` or later.

Run: `/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip download --no-deps --dest /tmp/rocksdict-wheel rocksdict 2>&1 | tail -5`
Expected: `Saved /tmp/rocksdict-wheel/rocksdict-0.3.29-cp311-cp311-macosx_11_0_arm64.whl` (or equivalent for your arch).

- [ ] **Step 2: Install rocksdict**

Run: `/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip install rocksdict==0.3.29`
Expected: `Successfully installed rocksdict-0.3.29`.

Run: `/opt/homebrew/opt/python@3.11/bin/python3.11 -c "from rocksdict import Rdict, Options; print('rocksdict ready')"`
Expected: `rocksdict ready`.

- [ ] **Step 3: Write the smoke test**

Create `scripts/tests/test_rocksdict_smoke.py`:

```python
"""Sanity-check the rocksdict dependency is importable and can round-trip bytes.

This is a 3-line smoke test, not a full backend test. Task 4 and
Task 5 cover the actual class-level behaviour.
"""
from __future__ import annotations

from pathlib import Path

import pytest


def test_rocksdict_import_and_roundtrip(tmp_path: Path) -> None:
    rocksdict = pytest.importorskip("rocksdict")
    db = rocksdict.Rdict(str(tmp_path / "smoke.rocksdb"))
    try:
        db[b"k"] = b"v"
        assert db[b"k"] == b"v"
        assert db.get(b"nope") is None
    finally:
        db.close()
```

- [ ] **Step 4: Run the test**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rocksdict_smoke.py -v`
Expected: PASS.

- [ ] **Step 5: Record the version in a dependency manifest**

Check whether the repo has a canonical dependency list. Run: `ls requirements*.txt pyproject.toml 2>&1`

If `requirements.txt` exists: append `rocksdict==0.3.29` to it.

If no manifest exists in the repo root, the dependency is captured via pip and there's nothing to commit here — move on. (The `test_rocksdict_smoke.py` import guard with `pytest.importorskip` means CI on systems without rocksdict installed won't fail.)

- [ ] **Step 6: Stage files (do NOT commit)**

Files changed:
- `scripts/tests/test_rocksdict_smoke.py` (new)
- `requirements.txt` if present (modified)

---

## Task 3: Add feature flags + test registry entries (Wave A — parallel-safe)

**Why:** The nine prior sprints all followed the same pattern: new capability lands behind a flag defaulting to `false`, with a test-registry entry that makes CI fail if a flag is added to YAML without the corresponding test entry. We follow the same discipline for this migration.

**Files:**
- Modify: `config/vitruvius.yaml` — add 2 flag lines under `features:`
- Modify: `scripts/tests/test_features.py` — add 2 entries to `EXPECTED_FLAGS`

- [ ] **Step 1: Read the current features block of the YAML**

Run: `grep -A 2 '^features:' /Users/philiplewis/vitruvius/config/vitruvius.yaml | head -20`

Identify the section of the file where `hp_*` flags are grouped (e.g. `hp_merkle_fs`, `hp_sqlite_events`, `hp_wasm_kernels`, `hp_graphsage`).

- [ ] **Step 2: Add the new flags**

Under the `hp_*` group in `config/vitruvius.yaml` (alphabetical order if the existing group is alphabetical), insert:

```yaml
  hp_rocksdb_event_store: false    # Sprint HP.3-R — replace SQLite event log with RocksDB
  hp_rocksdb_verdict_cache: false  # Sprint HP.3-R — replace SQLite verdict cache with RocksDB
```

Exact placement: after the last existing `hp_*` flag, before the next flag group (likely `wiki_*` or `z_*`).

- [ ] **Step 3: Update `EXPECTED_FLAGS` in test_features.py**

Open `scripts/tests/test_features.py`. Find the `EXPECTED_FLAGS` list (it's a module-level frozenset or tuple). Add two entries in the same style as neighbours:

```python
    "hp_rocksdb_event_store", "hp_rocksdb_verdict_cache",
```

Place them alphabetically within the hp_* group to match existing style.

- [ ] **Step 4: Write a failing test that the new flags exist and default to false**

Add to `scripts/tests/test_features.py` (or a new file if that's the convention):

```python
def test_hp_rocksdb_event_store_defaults_false() -> None:
    from vitruvius.config import load_config
    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("hp_rocksdb_event_store") is False


def test_hp_rocksdb_verdict_cache_defaults_false() -> None:
    from vitruvius.config import load_config
    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("hp_rocksdb_verdict_cache") is False
```

- [ ] **Step 5: Run tests**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_features.py -v`
Expected: all tests PASS, including the 2 new ones. If the existing registry-enforcement test fires and fails, it means the flag was added to YAML but not to `EXPECTED_FLAGS` (or vice versa) — fix the mismatch.

- [ ] **Step 6: Stage files (do NOT commit)**

Files changed:
- `config/vitruvius.yaml` (modified — 2 lines added)
- `scripts/tests/test_features.py` (modified — 2 EXPECTED_FLAGS entries + 2 new default-false tests)

---

## Task 4: `RocksDBEventStore` class + tests (Wave B — parallel-safe with Task 5)

**Why:** Mirror the existing `EventStore` API on top of rocksdict so the upstream caller (`compound/differential_propagator.py`) can be switched via factory in Task 6 with zero behavioural change.

**Files:**
- Create: `scripts/vitruvius/graph/rocksdb_event_store.py`
- Create: `scripts/tests/test_rocksdb_event_store.py`

### Key design

Since `EventStore` uses an integer `event_id` as PK and needs lexicographic range iteration by timestamp for `project_graph_at()`, the RocksDB key layout is:

- **Primary key:** `event:{event_id:010d}` (10-digit zero-pad so lex sort == numeric sort for event_ids ≤ 10 billion)
- **Value:** JSON-encoded `{event_type, edge_id, timestamp_utc, payload}`
- **Secondary index for time-travel:** `ts:{timestamp_utc}:{event_id:010d}` → `{event_id:010d}` (the primary key). Iterating `ts:*` in lex order gives us events in timestamp order, stopping at the target timestamp.

Duplicate detection: `db.get(primary_key) is not None` before `db[key] = value`.

Count: `len(list(db.items()))` is slow at scale but fine for our n. Alternative: track count in a reserved `meta:count` key updated on every append. Go with the simple `sum(1 for _ in db.keys())` for now; document the optimization as a TODO in AD-029 if bench shows count() is hot.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_rocksdb_event_store.py` (mirrors `test_graph_event_store.py` but with the RocksDB backend):

```python
"""Sprint HP.3-R — RocksDB-backed event store tests (mirror SQLite coverage)."""
from __future__ import annotations

from pathlib import Path

import pytest

rocksdict = pytest.importorskip("rocksdict")

from vitruvius.graph.event_store import GraphEvent
from vitruvius.graph.rocksdb_event_store import (
    RocksDBEventStore,
    project_graph_at_rocksdb,
)


def _event(
    idx: int,
    *,
    kind: str,
    edge_id: str,
    ts: str,
    payload: dict | None = None,
) -> GraphEvent:
    return GraphEvent(
        event_id=idx,
        event_type=kind,
        edge_id=edge_id,
        timestamp_utc=ts,
        payload=payload or {},
    )


def test_append_and_count(tmp_path: Path) -> None:
    store = RocksDBEventStore(db_path=tmp_path / "events.rocksdb")
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z",
                             payload={"from": "law-pd-1096", "to": "concept-setbacks"}))
        store.append(_event(2, kind="PROMOTED", edge_id="rel-b", ts="2026-04-15T10:01:00Z",
                             payload={"from": "law-pd-1096", "to": "concept-yards"}))
        assert store.count() == 2
    finally:
        store.close()


def test_duplicate_event_id_raises(tmp_path: Path) -> None:
    store = RocksDBEventStore(db_path=tmp_path / "events.rocksdb")
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z"))
        with pytest.raises(ValueError, match="duplicate"):
            store.append(_event(1, kind="PROMOTED", edge_id="rel-a-different", ts="2026-04-15T10:05:00Z"))
        assert store.count() == 1
    finally:
        store.close()


def test_project_graph_at_timestamp(tmp_path: Path) -> None:
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    try:
        store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z",
                             payload={"type": "governs", "from": "law-a", "to": "concept-x"}))
        store.append(_event(2, kind="PROMOTED", edge_id="rel-b", ts="2026-04-15T10:05:00Z",
                             payload={"type": "governs", "from": "law-b", "to": "concept-y"}))
        store.append(_event(3, kind="REJECTED", edge_id="rel-a", ts="2026-04-15T10:10:00Z"))
    finally:
        store.close()

    at_10_02 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:02:00Z")
    assert set(at_10_02.keys()) == {"rel-a"}

    at_10_06 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:06:00Z")
    assert set(at_10_06.keys()) == {"rel-a", "rel-b"}

    at_10_11 = project_graph_at_rocksdb(db_path=db, timestamp_utc="2026-04-15T10:11:00Z")
    assert set(at_10_11.keys()) == {"rel-b"}


def test_reopen_persists(tmp_path: Path) -> None:
    db = tmp_path / "events.rocksdb"
    store = RocksDBEventStore(db_path=db)
    store.append(_event(1, kind="PROMOTED", edge_id="rel-a", ts="2026-04-15T10:00:00Z"))
    store.close()

    store2 = RocksDBEventStore(db_path=db)
    try:
        assert store2.count() == 1
    finally:
        store2.close()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rocksdb_event_store.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.graph.rocksdb_event_store'`.

- [ ] **Step 3: Implement `RocksDBEventStore`**

Create `scripts/vitruvius/graph/rocksdb_event_store.py`:

```python
"""Sprint HP.3-R — RocksDB-backed event-sourced graph store.

Public API mirrors ``vitruvius.graph.event_store.EventStore`` exactly so
the factory in Task 6 can swap backends transparently. Key layout:

- ``event:{event_id:010d}`` -> JSON payload (primary record)
- ``ts:{timestamp_utc}:{event_id:010d}`` -> b"{event_id:010d}" (secondary index for time-travel)

Duplicate detection uses ``db.get(primary_key)`` before write. Count
iterates primary keys; at our scale (<10k events) this is cheap.
Optimize via a ``meta:count`` reserved key if bench shows it's hot.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from vitruvius.graph.event_store import GraphEvent

# Deferred import — rocksdict is an optional dependency; we want
# ImportError to surface at class-instantiation time, not module
# import time, so the SQLite fallback path never pays for an
# unavailable native lib.
_Rdict: Any = None


def _require_rocksdict() -> Any:
    global _Rdict
    if _Rdict is not None:
        return _Rdict
    try:
        from rocksdict import Rdict
    except ImportError as exc:
        raise ImportError(
            "rocksdict is required for RocksDBEventStore. "
            "Install via `pip install rocksdict==0.3.29`."
        ) from exc
    _Rdict = Rdict
    return _Rdict


def _event_key(event_id: int) -> bytes:
    return f"event:{event_id:010d}".encode("ascii")


def _ts_key(timestamp_utc: str, event_id: int) -> bytes:
    return f"ts:{timestamp_utc}:{event_id:010d}".encode("ascii")


_EVENT_PREFIX = b"event:"
_TS_PREFIX = b"ts:"


class RocksDBEventStore:
    """RocksDB-backed event log with ``EventStore``-compatible API."""

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        Rdict = _require_rocksdict()
        self._db = Rdict(str(self._db_path))

    def append(self, event: GraphEvent) -> None:
        primary = _event_key(event.event_id)
        if self._db.get(primary) is not None:
            raise ValueError(
                f"duplicate event_id {event.event_id} — event log is "
                f"append-only, prior event cannot be overwritten"
            )
        value = json.dumps({
            "event_type": event.event_type,
            "edge_id": event.edge_id,
            "timestamp_utc": event.timestamp_utc,
            "payload": dict(event.payload),
        }, sort_keys=True).encode("utf-8")
        self._db[primary] = value
        self._db[_ts_key(event.timestamp_utc, event.event_id)] = f"{event.event_id:010d}".encode("ascii")

    def count(self) -> int:
        return sum(1 for k in self._db.keys() if k.startswith(_EVENT_PREFIX))

    def close(self) -> None:
        self._db.close()


def project_graph_at_rocksdb(
    *,
    db_path: Path,
    timestamp_utc: str,
) -> dict[str, dict[str, Any]]:
    """Replay events up to ``timestamp_utc`` and return ``{edge_id: latest_payload}``.

    Opens a fresh handle so this can run concurrently with a writer.
    Mirrors ``vitruvius.graph.event_store.project_graph_at`` semantics
    exactly.
    """
    Rdict = _require_rocksdict()
    db = Rdict(str(Path(db_path)))
    try:
        # Walk the time-index in lex (= chronological) order and
        # follow each pointer back to the primary record.
        state: dict[str, dict[str, Any]] = {}
        ts_cutoff = f"ts:{timestamp_utc}:".encode("ascii")
        for key in db.keys():
            if not key.startswith(_TS_PREFIX):
                continue
            if key > ts_cutoff and not key.startswith(ts_cutoff):
                # Any key whose ts: segment is strictly greater than
                # our cutoff is out of range. ``key > ts_cutoff`` also
                # catches equal-timestamp-higher-event_id rows which
                # we want to include, hence the prefix re-check.
                continue
            event_id_bytes = db[key]
            primary = b"event:" + event_id_bytes
            raw = db.get(primary)
            if raw is None:
                continue
            record = json.loads(raw)
            edge_id = record["edge_id"]
            event_type = record["event_type"]
            if event_type == "REJECTED":
                state.pop(edge_id, None)
                continue
            if event_type in {"PROMOTED", "AMENDED"}:
                state[edge_id] = record["payload"]
        return state
    finally:
        db.close()
```

**Self-check:** The time-travel loop uses a simple `db.keys()` iterator, which is O(n) in the total DB size. At our scale (≤10k events) this is fine. If Task 8's bench shows this is the hot path, the optimization is to use `db.iter()` with `seek()` to jump directly into the `ts:` prefix range — document the follow-up in AD-029.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rocksdb_event_store.py -v`
Expected: 4 tests PASS.

- [ ] **Step 5: Run the full suite to confirm nothing regressed**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -20`
Expected: `1368 passed` (1364 pre-Task-1 + 2 bench + 2 features + 4 rocksdb = 1372; exact count depends on Tasks 1-3 ordering). No regressions from the pre-session 1364 baseline.

- [ ] **Step 6: Stage files (do NOT commit)**

Files changed:
- `scripts/vitruvius/graph/rocksdb_event_store.py` (new)
- `scripts/tests/test_rocksdb_event_store.py` (new)

---

## Task 5: `RocksDBStatefulReviewRegistry` class + tests (Wave B — parallel-safe with Task 4)

**Why:** Mirror the existing `StatefulReviewRegistry` API. The composite PK is `(source_hash, relationship_hash, model_version)` — this translates cleanly to a colon-delimited RocksDB key.

**Files:**
- Create: `scripts/vitruvius/review/rocksdb_stateful_registry.py`
- Create: `scripts/tests/test_rocksdb_stateful_registry.py`

### Key design

- **Key:** `v:{source_hash}:{relationship_hash}:{model_version}` — colon-delimited, all ASCII. Hash values are already hex in the existing code so there's no quoting concern.
- **Value:** JSON-encoded `{verdict, self_confidence, created_utc}`. We don't re-store the PK fields in the value since they come back from the key during purge iteration.
- **purge_older_than:** iterate `v:*` prefix, decode value, check `created_utc < cutoff`, delete if so.
- **vacuum:** RocksDB has no equivalent — there's no VACUUM. We expose it as a no-op. The equivalent is `db.compact_range()` but at our scale it's not needed; document the no-op in a docstring.
- **disk_size_mb:** sum sizes of all files under the RocksDB directory.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_rocksdb_stateful_registry.py`:

```python
"""Sprint HP.3-R — RocksDB stateful review registry tests (mirror SQLite coverage)."""
from __future__ import annotations

from pathlib import Path

import pytest

rocksdict = pytest.importorskip("rocksdict")

from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry
from vitruvius.review.stateful_registry import VerdictRecord


def test_put_and_get_roundtrip(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        record = VerdictRecord(
            source_hash="src_abc", relationship_hash="rel_123",
            model_version="qwen2.5:7b-2026-04",
            verdict="keep", self_confidence=0.88,
            created_utc="2026-04-14T20:00:00Z",
        )
        reg.put(record)
        fetched = reg.get(
            source_hash="src_abc", relationship_hash="rel_123",
            model_version="qwen2.5:7b-2026-04",
        )
        assert fetched == record
    finally:
        reg.close()


def test_get_miss_returns_none(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        assert reg.get(source_hash="x", relationship_hash="y", model_version="z") is None
    finally:
        reg.close()


def test_model_version_scoping(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        r_v1 = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:v1",
                             verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z")
        r_v2 = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:v2",
                             verdict="reject", self_confidence=0.85, created_utc="2026-04-14T00:00:00Z")
        reg.put(r_v1)
        reg.put(r_v2)
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v1") == r_v1
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v2") == r_v2
    finally:
        reg.close()


def test_count_and_vacuum_noop(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        for i in range(5):
            reg.put(VerdictRecord(
                source_hash=f"s{i}", relationship_hash="r", model_version="m",
                verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
            ))
        assert reg.count() == 5
        reg.vacuum()  # must be a safe no-op
        assert reg.count() == 5
    finally:
        reg.close()


def test_purge_older_than(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        old = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:old",
                            verdict="keep", self_confidence=0.9, created_utc="2026-01-01T00:00:00Z")
        new = VerdictRecord(source_hash="s", relationship_hash="r", model_version="m:new",
                            verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z")
        reg.put(old)
        reg.put(new)
        assert reg.count() == 2

        deleted = reg.purge_older_than(cutoff_utc="2026-03-01T00:00:00Z")
        assert deleted == 1
        assert reg.count() == 1
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:new") == new
        assert reg.get(source_hash="s", relationship_hash="r", model_version="m:old") is None
    finally:
        reg.close()


def test_purge_all(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        for i in range(3):
            reg.put(VerdictRecord(
                source_hash=f"s{i}", relationship_hash="r", model_version="m",
                verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
            ))
        deleted = reg.purge_all()
        assert deleted == 3
        assert reg.count() == 0
    finally:
        reg.close()


def test_disk_size_mb_nonzero_after_write(tmp_path: Path) -> None:
    reg = RocksDBStatefulReviewRegistry(db_path=tmp_path / "reg.rocksdb")
    try:
        reg.put(VerdictRecord(
            source_hash="s", relationship_hash="r", model_version="m",
            verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
        ))
        # RocksDB writes are buffered; flush so the SST files exist.
        reg.flush()
        assert reg.disk_size_mb() > 0.0
    finally:
        reg.close()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rocksdb_stateful_registry.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.review.rocksdb_stateful_registry'`.

- [ ] **Step 3: Implement `RocksDBStatefulReviewRegistry`**

Create `scripts/vitruvius/review/rocksdb_stateful_registry.py`:

```python
"""Sprint HP.3-R — RocksDB-backed stateful verdict cache.

Public API mirrors ``vitruvius.review.stateful_registry.StatefulReviewRegistry``.
Key layout: ``v:{source_hash}:{relationship_hash}:{model_version}``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from vitruvius.review.stateful_registry import VerdictRecord

_Rdict: Any = None


def _require_rocksdict() -> Any:
    global _Rdict
    if _Rdict is not None:
        return _Rdict
    try:
        from rocksdict import Rdict
    except ImportError as exc:
        raise ImportError(
            "rocksdict is required for RocksDBStatefulReviewRegistry. "
            "Install via `pip install rocksdict==0.3.29`."
        ) from exc
    _Rdict = Rdict
    return _Rdict


_PREFIX = b"v:"


def _verdict_key(source_hash: str, relationship_hash: str, model_version: str) -> bytes:
    return f"v:{source_hash}:{relationship_hash}:{model_version}".encode("utf-8")


def _parse_key(key: bytes) -> tuple[str, str, str]:
    # v:{source_hash}:{relationship_hash}:{model_version}
    # model_version can contain colons (e.g. "qwen2.5:7b"), so we
    # split from the left only twice.
    text = key.decode("utf-8")
    assert text.startswith("v:")
    remainder = text[2:]
    source_hash, rest = remainder.split(":", 1)
    relationship_hash, model_version = rest.split(":", 1)
    return source_hash, relationship_hash, model_version


class RocksDBStatefulReviewRegistry:
    """RocksDB-backed verdict cache with ``StatefulReviewRegistry``-compatible API."""

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        Rdict = _require_rocksdict()
        self._db = Rdict(str(self._db_path))

    def put(self, record: VerdictRecord) -> None:
        key = _verdict_key(record.source_hash, record.relationship_hash, record.model_version)
        value = json.dumps({
            "verdict": record.verdict,
            "self_confidence": record.self_confidence,
            "created_utc": record.created_utc,
        }, sort_keys=True).encode("utf-8")
        self._db[key] = value

    def get(
        self,
        *,
        source_hash: str,
        relationship_hash: str,
        model_version: str,
    ) -> Optional[VerdictRecord]:
        key = _verdict_key(source_hash, relationship_hash, model_version)
        raw = self._db.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        return VerdictRecord(
            source_hash=source_hash,
            relationship_hash=relationship_hash,
            model_version=model_version,
            verdict=data["verdict"],
            self_confidence=data["self_confidence"],
            created_utc=data["created_utc"],
        )

    def count(self) -> int:
        return sum(1 for k in self._db.keys() if k.startswith(_PREFIX))

    def flush(self) -> None:
        """Force the active memtable to disk so ``disk_size_mb`` is meaningful."""
        # rocksdict exposes flush via the underlying DB handle.
        try:
            self._db.flush()
        except Exception:
            pass

    def vacuum(self) -> None:
        """No-op on RocksDB. SQLite's ``VACUUM`` reclaims deleted-row space;
        RocksDB handles this automatically during background compaction.
        Exposed for API compatibility with ``StatefulReviewRegistry``.
        """
        return

    def db_size_bytes(self) -> int:
        """Return total on-disk size of the RocksDB directory in bytes."""
        if not self._db_path.exists():
            return 0
        total = 0
        for entry in self._db_path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
        return total

    def disk_size_mb(self) -> float:
        return self.db_size_bytes() / (1024 * 1024)

    def purge_all(self) -> int:
        """Delete every verdict and return the deleted count."""
        to_delete = [k for k in self._db.keys() if k.startswith(_PREFIX)]
        for k in to_delete:
            del self._db[k]
        return len(to_delete)

    def purge_older_than(self, *, cutoff_utc: str) -> int:
        """Delete every verdict whose ``created_utc`` < ``cutoff_utc``.
        Returns the number of rows deleted.
        """
        deleted = 0
        to_delete: list[bytes] = []
        for k in self._db.keys():
            if not k.startswith(_PREFIX):
                continue
            raw = self._db.get(k)
            if raw is None:
                continue
            data = json.loads(raw)
            if data.get("created_utc", "") < cutoff_utc:
                to_delete.append(k)
        for k in to_delete:
            del self._db[k]
            deleted += 1
        return deleted

    def close(self) -> None:
        self._db.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rocksdb_stateful_registry.py -v`
Expected: 7 tests PASS.

- [ ] **Step 5: Run the full suite**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -10`
Expected: test counts grow by +7 since Task 4; no regressions.

- [ ] **Step 6: Stage files (do NOT commit)**

Files changed:
- `scripts/vitruvius/review/rocksdb_stateful_registry.py` (new)
- `scripts/tests/test_rocksdb_stateful_registry.py` (new)

---

## Task 6: Factory wiring (Wave C — serial)

**Why:** After Tasks 4 and 5 land, the two RocksDB classes exist but nothing uses them. This task adds the thin factory dispatch so the flag switches the consumer transparently. Must run after Tasks 4+5 because it imports both classes.

**Files:**
- Modify: `scripts/vitruvius/graph/event_store.py` — add `make_event_store()` factory
- Modify: `scripts/vitruvius/review/stateful_registry.py` — add `make_stateful_registry()` factory
- Modify: `scripts/vitruvius/compound/differential_propagator.py` — consume factory IFF it currently constructs `EventStore` directly (verify with `grep -n 'EventStore(' scripts/vitruvius/compound/differential_propagator.py` first)
- Modify: `scripts/vitruvius/ollama_review.py` — replace the direct `StatefulReviewRegistry(...)` call with `make_stateful_registry(...)`
- Create: `scripts/tests/test_kv_factory_switches.py`

- [ ] **Step 1: Write the failing factory-switch test**

Create `scripts/tests/test_kv_factory_switches.py`:

```python
"""Sprint HP.3-R — verify the make_*() factories dispatch on feature flags."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.event_store import EventStore, make_event_store
from vitruvius.review.stateful_registry import (
    StatefulReviewRegistry,
    make_stateful_registry,
)


def test_make_event_store_returns_sqlite_by_default(tmp_path: Path, monkeypatch) -> None:
    import vitruvius.config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_event_store": False})
    store = make_event_store(db_path=tmp_path / "ev.db")
    try:
        assert isinstance(store, EventStore)
    finally:
        store.close()


def test_make_event_store_returns_rocksdb_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore
    import vitruvius.config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_event_store": True})
    store = make_event_store(db_path=tmp_path / "ev.rocksdb")
    try:
        assert isinstance(store, RocksDBEventStore)
    finally:
        store.close()


def test_make_stateful_registry_returns_sqlite_by_default(tmp_path: Path, monkeypatch) -> None:
    import vitruvius.config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_verdict_cache": False})
    reg = make_stateful_registry(db_path=tmp_path / "reg.db")
    try:
        assert isinstance(reg, StatefulReviewRegistry)
    finally:
        reg.close()


def test_make_stateful_registry_returns_rocksdb_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry
    import vitruvius.config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"hp_rocksdb_verdict_cache": True})
    reg = make_stateful_registry(db_path=tmp_path / "reg.rocksdb")
    try:
        assert isinstance(reg, RocksDBStatefulReviewRegistry)
    finally:
        reg.close()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_kv_factory_switches.py -v`
Expected: FAIL with `ImportError: cannot import name 'make_event_store'` or similar.

- [ ] **Step 3: Add `make_event_store()` to event_store.py**

Append to `scripts/vitruvius/graph/event_store.py` (below the existing `Delta` class):

```python
# ---------------------------------------------------------------------------
# Sprint HP.3-R — factory dispatch
# ---------------------------------------------------------------------------


def make_event_store(*, db_path: Path):
    """Factory that returns either ``EventStore`` (SQLite) or
    ``RocksDBEventStore`` based on the ``hp_rocksdb_event_store`` feature flag.

    Keeps the SQLite path as the default so flag-OFF behaviour is
    byte-identical to the pre-Sprint-HP.3-R codebase.
    """
    try:
        from vitruvius import config as cfgmod
        flags = cfgmod._features_block()
    except Exception:
        flags = {}
    use_rocksdb = bool(flags.get("hp_rocksdb_event_store", False))
    if use_rocksdb:
        from vitruvius.graph.rocksdb_event_store import RocksDBEventStore
        return RocksDBEventStore(db_path=db_path)
    return EventStore(db_path=db_path)
```

- [ ] **Step 4: Add `make_stateful_registry()` to stateful_registry.py**

Append to `scripts/vitruvius/review/stateful_registry.py` (below `run_ple_registry_purge`):

```python
# ---------------------------------------------------------------------------
# Sprint HP.3-R — factory dispatch
# ---------------------------------------------------------------------------


def make_stateful_registry(*, db_path: Path):
    """Factory that returns either ``StatefulReviewRegistry`` (SQLite) or
    ``RocksDBStatefulReviewRegistry`` based on the ``hp_rocksdb_verdict_cache``
    feature flag. SQLite is the default.
    """
    try:
        from vitruvius import config as cfgmod
        flags = cfgmod._features_block()
    except Exception:
        flags = {}
    use_rocksdb = bool(flags.get("hp_rocksdb_verdict_cache", False))
    if use_rocksdb:
        from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry
        return RocksDBStatefulReviewRegistry(db_path=db_path)
    return StatefulReviewRegistry(db_path=db_path)
```

- [ ] **Step 5: Swap `ollama_review.py` to use the factory**

Run: `grep -n 'StatefulReviewRegistry' /Users/philiplewis/vitruvius/scripts/vitruvius/ollama_review.py`
Expected: a line like `from .review.stateful_registry import StatefulReviewRegistry, VerdictRecord` and a construction call.

Edit: change the import to also pull the factory:
```python
from .review.stateful_registry import (
    StatefulReviewRegistry,
    VerdictRecord,
    make_stateful_registry,
)
```

Then change the `StatefulReviewRegistry(db_path=...)` construction call to `make_stateful_registry(db_path=...)`.

**Critical:** this is the only construction site in `ollama_review.py`. Do NOT rename occurrences of `StatefulReviewRegistry` in type annotations or docstrings — those are fine as-is.

- [ ] **Step 6: Check differential_propagator.py for EventStore construction**

Run: `grep -n 'EventStore(' /Users/philiplewis/vitruvius/scripts/vitruvius/compound/differential_propagator.py`

If it constructs an `EventStore` directly, change the construction site to `make_event_store(db_path=...)` and add the import.

If it only imports `Delta` and doesn't construct `EventStore`, **leave it alone**. The `Delta` wrapper is shared by both backends.

Current state (verified at plan-write time): `differential_propagator.py` imports `Delta` only — nothing to change. Document this finding in the commit message.

- [ ] **Step 7: Run the factory-switch tests**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_kv_factory_switches.py -v`
Expected: 4 tests PASS.

- [ ] **Step 8: Run the full suite**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -10`
Expected: no regressions. The flag is still false by default, so every existing caller gets SQLite just as before.

- [ ] **Step 9: Stage files (do NOT commit)**

Files changed:
- `scripts/vitruvius/graph/event_store.py` (modified — `make_event_store()` appended)
- `scripts/vitruvius/review/stateful_registry.py` (modified — `make_stateful_registry()` appended)
- `scripts/vitruvius/ollama_review.py` (modified — construction call swapped)
- `scripts/tests/test_kv_factory_switches.py` (new)

---

## Task 7: `ple-kv-migrate` CLI (Wave D — parallel-safe with Task 8)

**Why:** When we flip the flags in production, any existing SQLite state needs to migrate to RocksDB. This task provides the one-shot migration tool. Idempotent (re-running does nothing if the destination already has the keys).

**Files:**
- Create: `scripts/vitruvius/kv_migrate.py`
- Modify: `scripts/pipeline_cli.py` — register the `ple-kv-migrate` subcommand
- Create: `scripts/tests/test_kv_migrate_cli.py`

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_kv_migrate_cli.py`:

```python
"""Sprint HP.3-R — migration CLI tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.event_store import EventStore, GraphEvent
from vitruvius.kv_migrate import run_kv_migrate
from vitruvius.review.stateful_registry import StatefulReviewRegistry, VerdictRecord


def test_migrate_event_store_copies_all_events(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    for i in range(5):
        src_store.append(GraphEvent(
            event_id=i,
            event_type="PROMOTED",
            edge_id=f"rel-{i}",
            timestamp_utc=f"2026-04-15T10:00:{i:02d}Z",
            payload={"n": i},
        ))
    src_store.close()

    rc = run_kv_migrate(store="event", source=src, dest=dest, dry_run=False)
    assert rc == 0

    dest_store = RocksDBEventStore(db_path=dest)
    try:
        assert dest_store.count() == 5
    finally:
        dest_store.close()


def test_migrate_event_store_is_idempotent(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    src_store.append(GraphEvent(
        event_id=42, event_type="PROMOTED", edge_id="rel-x",
        timestamp_utc="2026-04-15T10:00:00Z", payload={},
    ))
    src_store.close()

    # First migration.
    assert run_kv_migrate(store="event", source=src, dest=dest, dry_run=False) == 0
    # Second migration against the same dest must not double-write.
    assert run_kv_migrate(store="event", source=src, dest=dest, dry_run=False) == 0

    dest_store = RocksDBEventStore(db_path=dest)
    try:
        assert dest_store.count() == 1
    finally:
        dest_store.close()


def test_migrate_registry_copies_all_verdicts(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry

    src = tmp_path / "reg.sqlite"
    dest = tmp_path / "reg.rocksdb"

    src_reg = StatefulReviewRegistry(db_path=src)
    src_reg.put(VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    ))
    src_reg.close()

    rc = run_kv_migrate(store="registry", source=src, dest=dest, dry_run=False)
    assert rc == 0

    dest_reg = RocksDBStatefulReviewRegistry(db_path=dest)
    try:
        assert dest_reg.count() == 1
        record = dest_reg.get(source_hash="s", relationship_hash="r", model_version="m:v1")
        assert record is not None
        assert record.verdict == "keep"
    finally:
        dest_reg.close()


def test_migrate_dry_run_does_not_write(tmp_path: Path) -> None:
    pytest.importorskip("rocksdict")

    src = tmp_path / "src.sqlite"
    dest = tmp_path / "dest.rocksdb"

    src_store = EventStore(db_path=src)
    src_store.append(GraphEvent(
        event_id=1, event_type="PROMOTED", edge_id="rel-x",
        timestamp_utc="2026-04-15T10:00:00Z", payload={},
    ))
    src_store.close()

    rc = run_kv_migrate(store="event", source=src, dest=dest, dry_run=True)
    assert rc == 0
    # Dry-run must not create the dest directory.
    assert not dest.exists()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_kv_migrate_cli.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.kv_migrate'`.

- [ ] **Step 3: Implement the migration module**

Create `scripts/vitruvius/kv_migrate.py`:

```python
"""Sprint HP.3-R — one-shot SQLite → RocksDB migration CLI.

Handler for the ``ple-kv-migrate`` subcommand. Idempotent: re-running
against a populated destination is a no-op for already-present keys.

Usage:
    ple-kv-migrate --store event    --source events.sqlite  --dest events.rocksdb
    ple-kv-migrate --store registry --source reg.sqlite     --dest reg.rocksdb    [--dry-run]
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from vitruvius.graph.event_store import EventStore, GraphEvent, project_graph_at
from vitruvius.review.stateful_registry import StatefulReviewRegistry

StoreKind = Literal["event", "registry"]


def run_kv_migrate(
    *,
    store: StoreKind,
    source: Path,
    dest: Path,
    dry_run: bool = False,
) -> int:
    """Return 0 on success, non-zero on failure."""
    source = Path(source)
    dest = Path(dest)

    if not source.exists():
        print(f"source not found: {source}")
        return 1

    if store == "event":
        return _migrate_event_store(source=source, dest=dest, dry_run=dry_run)
    if store == "registry":
        return _migrate_registry(source=source, dest=dest, dry_run=dry_run)

    print(f"unknown --store value: {store!r} (expected 'event' or 'registry')")
    return 2


def _migrate_event_store(*, source: Path, dest: Path, dry_run: bool) -> int:
    import sqlite3

    # Read every event row directly from the SQLite file to avoid
    # any dependency on the EventStore class being compatible with
    # the migrated source schema.
    conn = sqlite3.connect(source)
    try:
        rows = conn.execute(
            "SELECT event_id, event_type, edge_id, timestamp_utc, payload_json "
            "FROM graph_events ORDER BY event_id ASC"
        ).fetchall()
    finally:
        conn.close()

    if dry_run:
        print(f"dry-run: would migrate {len(rows)} events from {source} to {dest}")
        return 0

    from vitruvius.graph.rocksdb_event_store import RocksDBEventStore
    import json

    dest_store = RocksDBEventStore(db_path=dest)
    copied = 0
    skipped = 0
    try:
        for (event_id, event_type, edge_id, timestamp_utc, payload_json) in rows:
            try:
                dest_store.append(GraphEvent(
                    event_id=int(event_id),
                    event_type=event_type,
                    edge_id=edge_id,
                    timestamp_utc=timestamp_utc,
                    payload=json.loads(payload_json) if payload_json else {},
                ))
                copied += 1
            except ValueError:
                # Duplicate event_id — already migrated.
                skipped += 1
    finally:
        dest_store.close()

    print(f"migrated: {copied} events copied, {skipped} skipped (idempotent)")
    return 0


def _migrate_registry(*, source: Path, dest: Path, dry_run: bool) -> int:
    import sqlite3

    conn = sqlite3.connect(source)
    try:
        rows = conn.execute(
            "SELECT source_hash, relationship_hash, model_version, "
            "verdict, self_confidence, created_utc FROM verdicts"
        ).fetchall()
    finally:
        conn.close()

    if dry_run:
        print(f"dry-run: would migrate {len(rows)} verdicts from {source} to {dest}")
        return 0

    from vitruvius.review.rocksdb_stateful_registry import (
        RocksDBStatefulReviewRegistry,
    )
    from vitruvius.review.stateful_registry import VerdictRecord

    dest_reg = RocksDBStatefulReviewRegistry(db_path=dest)
    copied = 0
    try:
        for (src_h, rel_h, model, verdict, conf, created) in rows:
            dest_reg.put(VerdictRecord(
                source_hash=src_h,
                relationship_hash=rel_h,
                model_version=model,
                verdict=verdict,
                self_confidence=float(conf),
                created_utc=created,
            ))
            copied += 1
    finally:
        dest_reg.close()

    print(f"migrated: {copied} verdicts copied")
    return 0
```

- [ ] **Step 4: Register the CLI subcommand**

Open `scripts/pipeline_cli.py` and add a subcommand. Find the argparse subparser block (there will be a pattern like `sub = parser.add_subparsers(...)` and several `sub.add_parser(...)` calls).

Add:
```python
    p_migrate = sub.add_parser("ple-kv-migrate", help="Sprint HP.3-R: migrate SQLite KV store to RocksDB")
    p_migrate.add_argument("--store", choices=["event", "registry"], required=True)
    p_migrate.add_argument("--source", type=Path, required=True)
    p_migrate.add_argument("--dest", type=Path, required=True)
    p_migrate.add_argument("--dry-run", action="store_true")
```

And in the dispatch block (usually a chain of `if args.command == "...": ...`):
```python
    if args.command == "ple-kv-migrate":
        from vitruvius.kv_migrate import run_kv_migrate
        return run_kv_migrate(
            store=args.store,
            source=args.source,
            dest=args.dest,
            dry_run=args.dry_run,
        )
```

**If `scripts/pipeline_cli.py` uses a different CLI dispatch pattern (e.g. click, typer), adapt to that pattern. The essential requirements are: new subcommand name `ple-kv-migrate`, flags `--store`, `--source`, `--dest`, `--dry-run`.**

- [ ] **Step 5: Run the tests**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_kv_migrate_cli.py -v`
Expected: 4 tests PASS.

- [ ] **Step 6: Smoke-test the CLI**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 scripts/pipeline_cli.py ple-kv-migrate --help 2>&1 | head -10`
Expected: help text listing `--store`, `--source`, `--dest`, `--dry-run`.

- [ ] **Step 7: Stage files (do NOT commit)**

Files changed:
- `scripts/vitruvius/kv_migrate.py` (new)
- `scripts/pipeline_cli.py` (modified — subcommand registered)
- `scripts/tests/test_kv_migrate_cli.py` (new)

---

## Task 8: RocksDB bench + decision gate (Wave D — parallel-safe with Task 7)

**Why:** With both backends live, we can finally measure whether the migration delivers the performance win the user is expecting. The bench outputs are the input to the AD-029 decision in Task 9.

**Files:**
- Modify: `scripts/vitruvius/bench/bench_kv_backends.py` — add `bench_event_store_rocksdb()` + `bench_verdict_cache_rocksdb()`
- Modify: `scripts/tests/test_bench_kv_backends.py` — add smoke tests for the RocksDB bench path

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_bench_kv_backends.py`:

```python
import pytest


def test_event_store_rocksdb_bench_runs(tmp_path):
    pytest.importorskip("rocksdict")
    from vitruvius.bench.bench_kv_backends import bench_event_store_rocksdb
    result = bench_event_store_rocksdb(db_path=tmp_path / "events.rocksdb", n_events=100)
    assert result.backend == "rocksdb"
    assert result.op == "event_store"
    assert result.n == 100
    assert result.wall_seconds > 0


def test_verdict_cache_rocksdb_bench_runs(tmp_path):
    pytest.importorskip("rocksdict")
    from vitruvius.bench.bench_kv_backends import bench_verdict_cache_rocksdb
    result = bench_verdict_cache_rocksdb(db_path=tmp_path / "reg.rocksdb", n_verdicts=100)
    assert result.backend == "rocksdb"
    assert result.op == "verdict_cache"
    assert result.n == 100
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_bench_kv_backends.py -v -k rocksdb`
Expected: FAIL with `ImportError: cannot import name 'bench_event_store_rocksdb'`.

- [ ] **Step 3: Add the RocksDB bench functions**

Append to `scripts/vitruvius/bench/bench_kv_backends.py`:

```python
# ---------------------------------------------------------------------------
# RocksDB bench functions (Sprint HP.3-R Task 8)
# ---------------------------------------------------------------------------


def bench_event_store_rocksdb(*, db_path: Path, n_events: int) -> BenchResult:
    from vitruvius.graph.rocksdb_event_store import (
        RocksDBEventStore,
        project_graph_at_rocksdb,
    )

    store = RocksDBEventStore(db_path=db_path)

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
        project_graph_at_rocksdb(db_path=db_path, timestamp_utc="2026-04-15T10:00:30Z")

    project_graph_at_seconds = _timed(project)
    total = append_seconds + point_lookup_seconds + project_graph_at_seconds

    return BenchResult(
        backend="rocksdb",
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


def bench_verdict_cache_rocksdb(*, db_path: Path, n_verdicts: int) -> BenchResult:
    from vitruvius.review.rocksdb_stateful_registry import RocksDBStatefulReviewRegistry

    reg = RocksDBStatefulReviewRegistry(db_path=db_path)

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
        backend="rocksdb",
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
```

Also extend the `if __name__ == "__main__":` block at the bottom to run both backends and print both results:

```python
if __name__ == "__main__":
    import argparse
    import tempfile

    parser = argparse.ArgumentParser(description="KV backend benchmark")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--backends", default="both", choices=["sqlite", "rocksdb", "both"])
    args = parser.parse_args()

    results: list[BenchResult] = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        if args.backends in ("sqlite", "both"):
            results.append(bench_event_store_sqlite(db_path=tmp / "events.sqlite", n_events=args.n))
            results.append(bench_verdict_cache_sqlite(db_path=tmp / "verdicts.sqlite", n_verdicts=args.n))
        if args.backends in ("rocksdb", "both"):
            results.append(bench_event_store_rocksdb(db_path=tmp / "events.rocksdb", n_events=args.n))
            results.append(bench_verdict_cache_rocksdb(db_path=tmp / "verdicts.rocksdb", n_verdicts=args.n))

    for r in results:
        print(result_as_json(r))
```

- [ ] **Step 4: Run the tests**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_bench_kv_backends.py -v`
Expected: 4 tests PASS (2 original SQLite + 2 new RocksDB).

- [ ] **Step 5: Run the real benchmark and record the numbers**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_kv_backends --n 10000 --backends both`
Expected: 4 JSON blocks printed. Save to `.ai/10_state/bench_kv_migration_2026-04-15.json` (this file is consumed by Task 9 for AD-029).

Suggested format for the saved file:
```json
{
  "timestamp_utc": "2026-04-15T...Z",
  "n": 10000,
  "results": [
    { "backend": "sqlite", "op": "event_store", ... },
    { "backend": "sqlite", "op": "verdict_cache", ... },
    { "backend": "rocksdb", "op": "event_store", ... },
    { "backend": "rocksdb", "op": "verdict_cache", ... }
  ],
  "deltas": {
    "event_store_wall_seconds_ratio_rocks_vs_sqlite": 0.0,
    "verdict_cache_wall_seconds_ratio_rocks_vs_sqlite": 0.0
  }
}
```

Compute the two ratio values by dividing RocksDB `wall_seconds` by SQLite `wall_seconds`. A ratio of 0.5 means RocksDB is 2× faster; a ratio of 1.0 means they're equivalent; a ratio of 2.0 means SQLite is 2× faster.

- [ ] **Step 6: Decision gate**

Inspect the ratios:

- **If both ratios ≤ 0.5** (RocksDB ≥ 2× faster): **Flip defaults.** In Task 9, change `hp_rocksdb_event_store: false` → `true` and `hp_rocksdb_verdict_cache: false` → `true`.
- **If both ratios between 0.5 and 1.25** (rough parity ± 25%): **Keep flags default-off.** RocksDB is still available via the flag but isn't the default. Task 9's AD-029 documents this as a "spec compliance, not perf win" outcome.
- **If either ratio > 1.25** (RocksDB measurably slower): **STOP.** Do not proceed to Task 9. Investigate the hot path (likely `count()` doing a full scan or `project_graph_at_rocksdb()` iterating the whole DB instead of using `seek()`). File a follow-up task and return control to the orchestrator.

Whichever bucket we land in, record the decision in Task 9's AD-029 with the actual numbers.

- [ ] **Step 7: Stage files (do NOT commit)**

Files changed:
- `scripts/vitruvius/bench/bench_kv_backends.py` (modified — RocksDB functions appended)
- `scripts/tests/test_bench_kv_backends.py` (modified — +2 RocksDB smoke tests)
- `.ai/10_state/bench_kv_migration_2026-04-15.json` (new — the actual measurement output)

---

## Task 9: Docs + AD-029 + final commit (Wave E — orchestrator-held)

**Why:** All code lands in one atomic commit at the end so there are no partial-state intermediate commits and no `git add` races between wave-parallel subagents. Also records the decision.

**Files:**
- Modify: `.ai/00_system/architecture.md` — append 1 paragraph about the RocksDB migration
- Modify: `.ai/10_state/known_issues.md` — add RI-013 if bench showed RocksDB is slower, OR add a closure note under RI-001 / whichever issue previously blocked HP.3
- Modify: `.ai/10_state/decisions.md` — append AD-029
- Modify: `.ai/03_plans/INDEX.md` — add a row for this plan (active → archived pattern)
- Modify: `config/vitruvius.yaml` — (conditional on Task 8 Step 6) flip flag defaults if the decision gate said so

- [ ] **Step 1: Write AD-029**

Append to `.ai/10_state/decisions.md`:

```markdown
## AD-029 — Sprint HP.3-R — RocksDB KV backend migration (2026-04-15)

**Context.** Sprint HP.3 (closed 2026-04-15, tag `sprint-hp-closed`) originally
specified RocksDB for the event store (`.ai/09_archive/plans/phase-13-high-performance-optimizations-plan.md`
§3) but pivoted to SQLite because no `python-rocksdb` wheel was available
for Apple Silicon Python 3.11. The Sprint R stateful verdict cache
(`stateful_registry.py`) also went with SQLite for the same reason.

User installed `rocksdb 11.0.4` via Homebrew on 2026-04-15 and requested
the migration. Verified that `rocksdict 0.3.29` ships a
`cp311-cp311-macosx_11_0_arm64.whl`, unblocking the original spec with a
modern Rust-based binding (not the old python-rocksdb Cython binding).

**Decision.** Shipped `RocksDBEventStore` and `RocksDBStatefulReviewRegistry`
classes with API parity against the SQLite versions. Both are gated
behind new feature flags (`hp_rocksdb_event_store`,
`hp_rocksdb_verdict_cache`) that default to **[FILL IN: false | true]**
based on the bench outcome below. SQLite code paths kept intact as
fallback.

**Benchmark (n=10,000):**

| Backend | Op | Wall seconds | Throughput (ops/sec) | vs SQLite |
|---|---|---|---|---|
| SQLite | event_store | [FILL] | [FILL] | 1.0× baseline |
| RocksDB | event_store | [FILL] | [FILL] | [FILL]× |
| SQLite | verdict_cache | [FILL] | [FILL] | 1.0× baseline |
| RocksDB | verdict_cache | [FILL] | [FILL] | [FILL]× |

Raw JSON: `.ai/10_state/bench_kv_migration_2026-04-15.json`.

**Outcome:** [pick one and delete the other two]

- **(a) RocksDB ≥ 2× faster on both ops** — flipping defaults to `true`.
  Flag-OFF SQLite path retained for at least one week of live operation
  before any cleanup.
- **(b) RocksDB within 25% of SQLite** — keeping defaults `false`. This
  migration is a spec-compliance pass (HP.3 original spec now honored)
  and a pre-positioning pass (RocksDB will matter at 100k+ events scale
  when Sprint D Streams J + K unblock the 2nd jurisdiction ingest).
- **(c) RocksDB slower** — stopped at Task 8 Step 6. Investigation
  needed: likely hot paths are `count()` full-scan and
  `project_graph_at_rocksdb()` full-scan iteration. Recorded as a
  follow-up task in the next plan.

**Migration path:** `ple-kv-migrate --store {event,registry} --source X --dest Y`
ships as an idempotent one-shot CLI. Operators flip the flag, run the
migrate command pointed at their existing SQLite files, then restart.

**Test delta:** +17 tests (2 bench + 1 rocksdict smoke + 4 event store +
7 registry + 4 CLI + 4 factory switch – 5 deduped from overlap). Full
suite at [FILL: final count] / [FILL: final count] passing.

**Commits:** `[FILL: final commit SHA]`.

**Follow-ups (not in this plan):**
- Archive the SQLite backend files once the RocksDB path has been
  stable for one week of real use.
- If bench outcome was (b), revisit after the Sprint D Streams J + K
  unblock and we have 100k+ events — RocksDB's advantage should show
  up at that scale.
- If `count()` or `project_graph_at_rocksdb()` was hot in bench,
  optimize with a reserved `meta:count` key + RocksDB `seek()` calls.
```

**Critical:** Every `[FILL]` placeholder in the AD above must be replaced with real numbers from the Task 8 bench output before the commit lands. Do not commit a template.

- [ ] **Step 2: Append the architecture note**

In `.ai/00_system/architecture.md`, find the "Post-Sprint-D Layered Additions" section (added by the 2026-04-15 docs cleanup plan). Under the "### Rust data plane" or similar subsection, append a new paragraph:

```markdown
### KV storage backends (Sprint HP.3-R, 2026-04-15)

The two persistent KV stores in the project (`graph/event_store.py` and
`review/stateful_registry.py`) now ship with parallel RocksDB backends
alongside the original SQLite implementations. Switches are controlled
by `features.hp_rocksdb_event_store` and `features.hp_rocksdb_verdict_cache`.
See AD-029 for the bench results that informed the default flag states.

Migration tool: `ple-kv-migrate --store {event,registry} --source X --dest Y [--dry-run]`.

RocksDB binding: `rocksdict 0.3.29` (modern Rust-based; NOT `python-rocksdb`).
```

- [ ] **Step 3: (Optional) Flip the flag defaults based on Task 8 decision**

If Task 8 Step 6 said "Flip defaults," edit `config/vitruvius.yaml`:

```yaml
  hp_rocksdb_event_store: true    # Sprint HP.3-R — bench showed ≥2× speedup (AD-029)
  hp_rocksdb_verdict_cache: true  # Sprint HP.3-R — bench showed ≥2× speedup (AD-029)
```

If Task 8 said "keep defaults off," skip this step.

If Task 8 said "RocksDB slower," this task should not have been reached — escalate to the user.

- [ ] **Step 4: Update `.ai/03_plans/INDEX.md`**

Insert a new row for this plan:

```
| 13-R | `rocksdb-kv-migration` | SQLite → RocksDB KV backend migration (HP.3 spec compliance) | ✅ Complete | Sprint HP.3-R | implementation_tdd | [../09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md](../09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md) |
```

(Or `🔥 In progress` if committing mid-execution — but Task 9 assumes all prior tasks landed successfully.)

- [ ] **Step 5: Archive this plan**

```bash
cd /Users/philiplewis/vitruvius && git mv .ai/03_plans/2026-04-15-rocksdb-kv-migration-plan.md .ai/09_archive/plans/
```

- [ ] **Step 6: Verify all expected changes are staged**

Run: `cd /Users/philiplewis/vitruvius && git status --short`
Expected (file list, order may vary):
```
M  config/vitruvius.yaml
M  scripts/pipeline_cli.py
M  scripts/vitruvius/bench/bench_kv_backends.py
M  scripts/vitruvius/graph/event_store.py
M  scripts/vitruvius/ollama_review.py
M  scripts/vitruvius/review/stateful_registry.py
A  scripts/vitruvius/graph/rocksdb_event_store.py
A  scripts/vitruvius/kv_migrate.py
A  scripts/vitruvius/review/rocksdb_stateful_registry.py
M  scripts/tests/test_features.py
A  scripts/tests/test_bench_kv_backends.py
A  scripts/tests/test_kv_factory_switches.py
A  scripts/tests/test_kv_migrate_cli.py
A  scripts/tests/test_rocksdb_event_store.py
A  scripts/tests/test_rocksdb_stateful_registry.py
A  scripts/tests/test_rocksdict_smoke.py
M  .ai/00_system/architecture.md
M  .ai/03_plans/INDEX.md
M  .ai/10_state/decisions.md
A  .ai/10_state/bench_kv_migration_2026-04-15.json
R  .ai/03_plans/2026-04-15-rocksdb-kv-migration-plan.md -> .ai/09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md
```

Any file not in this list should be investigated before committing.

- [ ] **Step 7: Run the full test suite one last time**

Run: `cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ --tb=short 2>&1 | tail -5`
Expected: `[1364 + 17] passed` or similar. No regressions.

- [ ] **Step 8: Stage and commit**

```bash
cd /Users/philiplewis/vitruvius && \
  git add config/vitruvius.yaml \
          scripts/pipeline_cli.py \
          scripts/vitruvius/bench/bench_kv_backends.py \
          scripts/vitruvius/graph/event_store.py \
          scripts/vitruvius/graph/rocksdb_event_store.py \
          scripts/vitruvius/kv_migrate.py \
          scripts/vitruvius/ollama_review.py \
          scripts/vitruvius/review/rocksdb_stateful_registry.py \
          scripts/vitruvius/review/stateful_registry.py \
          scripts/tests/test_bench_kv_backends.py \
          scripts/tests/test_features.py \
          scripts/tests/test_kv_factory_switches.py \
          scripts/tests/test_kv_migrate_cli.py \
          scripts/tests/test_rocksdb_event_store.py \
          scripts/tests/test_rocksdb_stateful_registry.py \
          scripts/tests/test_rocksdict_smoke.py \
          .ai/00_system/architecture.md \
          .ai/03_plans/INDEX.md \
          .ai/09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md \
          .ai/10_state/bench_kv_migration_2026-04-15.json \
          .ai/10_state/decisions.md

git commit -m "$(cat <<'EOF'
feat(hp): Sprint HP.3-R — RocksDB KV backend migration (spec compliance)

Completes the original HP.3 spec by shipping RocksDB-backed event
store and verdict cache alongside the SQLite fallbacks that were
used during Sprint HP due to the python-rocksdb wheel blocker.

Delivers:
- RocksDBEventStore (scripts/vitruvius/graph/rocksdb_event_store.py)
  mirroring EventStore public API
- RocksDBStatefulReviewRegistry
  (scripts/vitruvius/review/rocksdb_stateful_registry.py) mirroring
  StatefulReviewRegistry public API
- make_event_store() + make_stateful_registry() factories gating on
  hp_rocksdb_event_store / hp_rocksdb_verdict_cache flags
- ple-kv-migrate CLI (scripts/vitruvius/kv_migrate.py) — idempotent
  one-shot SQLite → RocksDB migration
- Bench harness (scripts/vitruvius/bench/bench_kv_backends.py)
  measuring both backends on the target workload
- AD-029 in .ai/10_state/decisions.md documenting the bench results
  and the flag default decision

Binding: rocksdict 0.3.29 (modern Rust-based Python binding, NOT
python-rocksdb which was the original HP.3 blocker).

Flag defaults: [FILL based on Task 8 outcome]

Test suite: [FILL: pre] → [FILL: post] passing.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

**Replace every `[FILL]` before running the commit.**

- [ ] **Step 9: Tag the closure (optional)**

```bash
git tag sprint-hp3r-closed HEAD -m "Sprint HP.3-R — RocksDB KV migration closed; see AD-029"
```

---

## Self-Review Checklist

**1. Spec coverage** — User asked for a plan to migrate SQLite → RocksDB, referencing previous archived research.
- Archived research read: ✅ `phase-13-high-performance-optimizations-plan.md` §3 confirms RocksDB was the original spec. ✅ `per-layer-embeddings-agentic-upgrade-plan.md` is archived and Stream Y4 was the verdict cache origin.
- Scope: ✅ both SQLite users (`event_store.py` + `stateful_registry.py`) covered.
- Migration path: ✅ `ple-kv-migrate` CLI handles data transport.
- Decision gate: ✅ Task 8 Step 6 explicitly refuses to flip defaults without bench data.

**2. Placeholder scan** — The only `[FILL]` placeholders are inside AD-029 and the final commit message, where they are EXPLICITLY flagged as "must be replaced with real numbers from Task 8 before commit". This is intentional — we can't know the numbers at plan-write time.

All other steps have concrete code, concrete file paths, and concrete commands.

**3. Type consistency** — Checked:
- `RocksDBEventStore.append(event: GraphEvent)` — matches `EventStore.append()`
- `RocksDBEventStore.count() -> int` — matches
- `RocksDBEventStore.close() -> None` — matches
- `project_graph_at_rocksdb()` signature matches `project_graph_at()` signature
- `RocksDBStatefulReviewRegistry.put(record: VerdictRecord)` — matches
- `RocksDBStatefulReviewRegistry.get(source_hash, relationship_hash, model_version) -> Optional[VerdictRecord]` — matches
- `RocksDBStatefulReviewRegistry.purge_older_than(cutoff_utc)` — matches
- `vacuum()` is a no-op on RocksDB but API-compatible — documented.
- `make_event_store()` and `make_stateful_registry()` signatures and return types declared in Task 6.

**4. Performance claim honesty** — The plan **does not promise** RocksDB will be faster. Task 8 measures it. Task 9's AD-029 template has three outcome branches. The decision gate in Task 8 Step 6 explicitly STOPS execution if RocksDB is slower.

**5. Fallback path preserved** — SQLite code is never deleted in this plan. Archival is called out as a follow-up for "after at least one week of real use on the RocksDB path."

**6. Parallelism map verified** — Wave A tasks are disjoint (bench file / dependency install / config + test registry). Wave B tasks touch different subpackages. Wave C is serial because it coordinates across 4 files. Wave D tasks are disjoint (CLI module / bench extension). Wave E is orchestrator-only.

---

## Execution Handoff

Plan complete and saved to `.ai/03_plans/2026-04-15-rocksdb-kv-migration-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Wave-parallel dispatch of Tasks 1/2/3 (Wave A) → Tasks 4/5 (Wave B) → Task 6 (Wave C) → Tasks 7/8 (Wave D) → Task 9 (Wave E). Two-stage review (spec compliance + code quality) after each task.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints for review.

Which approach?
