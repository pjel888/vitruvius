---
plan_id: phase-8b-geo-topological-graph
phase: "Phase 8B / 10B (System-Level Performance + Spatial Graph)"
title: "Geo-Topological Knowledge Graph: Binary Vault & Octree Engine"
status: planned
priority: high
sprint: "Sprint GT — System Hardening"
version: 1.1.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/Geo-Topological Knowledge Graph.md
  - .ai/03_plans/statistical-architectural-upgrade-plan.md
  - .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md
  - .ai/03_plans/phase-8-graph-contract-indexing-plan.md
  - scripts/vitruvius/graph/event_store.py   # Sprint HP.3 — foundation for GT.3
  - scripts/vitruvius/engine_rs/              # In-flight this wave — foundation for GT.2 and GT.4
takes_precedence_over:
  - "Decoupled Spatial Daemon (Stream N) in 3d-spatial-intelligence-upgrade-plan.md (Upgrades TS to Rust)"
---

# Phase 8B Implementation Plan: Geo-Topological Knowledge Graph

> **Objective:** Operationalize the **Spatial Memory** system by building a high-performance Rust Data Plane. This replaces the linear search with $O(\log n)$ Octree traversals and connects physical proximity to topological relationships via **Spatial GraphRAG**.

## Status (2026-04-15)

- **GT.1 (Binary Data Plane / pyo3 bridge)** — **🟢 In-flight in this wave** (`feat/sprint-r-per-layer-embeddings`). Another implementer in this 2026-04-15 dispatch is shipping the `scripts/vitruvius/engine_rs/` pyo3 Rust crate. See commit history on this branch. **Do not re-spec.**
- **GT.2 (Sparse Linear Octree)** — **🟢 In-flight in this wave** (`feat/sprint-r-per-layer-embeddings`). Same implementer is landing the `LinearOctree` type, SIMD bounds checker, and point/sphere/frustum queries. See commit history. **Do not re-spec.**
- **GT.3 (Temporal Knowledge Graph)** — **🔵 TDD-expanded below.** Reuses the shipped Sprint HP.3 SQLite event store (`scripts/vitruvius/graph/event_store.py`) instead of RocksDB. Three bite-sized tasks (GT.3.1, GT.3.2, GT.3.3).
- **GT.4 (Geo-Topological Bridging / Spatial GraphRAG)** — **🔵 TDD-expanded below.** Bridges the in-flight engine_rs `LinearOctree` with the Phase 8 graph snapshot. Three bite-sized tasks (GT.4.1, GT.4.2, GT.4.3). **Cannot start until GT.2 has shipped a Python-callable `LinearOctree`.**
- **GT.5 (Hardware Hardening)** — **🔵 TDD-expanded below.** Pure Python, stdlib-first. Three bite-sized tasks (GT.5.1, GT.5.2, GT.5.3). All parallel-safe with the other streams.

## 1. Architectural Strategy: The Binary Vault

To survive on an 8GB M2, Vitruvius must stop treating the filesystem as a collection of text files and start treating it as a **Memory-Mapped Binary Vault**.

1.  **Zero-Copy Exchange:** Use **Apache Arrow** to share data between Python and Rust without serialization overhead.
2.  **Pre-Aligned Access:** Use **FlatBuffers** for $O(1)$ access to spatial octants.
3.  **Event-Sourced Temporal Graph:** Reuse the shipped Sprint HP.3 SQLite event store (`scripts/vitruvius/graph/event_store.py`) for the temporal quadruple $(s, p, o, t)$ store. (The original plan called for RocksDB; we landed SQLite in HP.3 because no pre-built rocksdb wheel was available on the host, and WAL-mode SQLite gives the same atomic-append semantics.)

---

## 2. Dependencies

| Dependency | Needed by | Source of truth |
|---|---|---|
| Rust toolchain (sourced from `~/.cargo/env`) | GT.1, GT.2 | Installed on host, managed by the in-flight GT.1/GT.2 agent |
| `scripts/vitruvius/engine_rs/` (pyo3 crate) | GT.2, GT.4 | **In-flight in this wave** — see commit history on `feat/sprint-r-per-layer-embeddings` |
| `pyarrow` | GT.3.3 | Already installed as a transitive dependency of Docling |
| `scripts/vitruvius/graph/event_store.py` | GT.3.2 | Shipped in Sprint HP.3 (see `project_graph_at`) |
| `scripts/vitruvius/graph/contract.py` | GT.3.1 | Shipped in Phase 8 (extended in-place) |
| Python `mmap` stdlib | GT.5.1 | Stdlib |
| Python `hashlib` + stdlib `bytearray` | GT.5.2 | Stdlib (no external bitarray) |
| Python `statistics` stdlib | GT.5.3 | Stdlib |

---

## 3. Cross-stream coordination

- **GT.3 is fully independent** of GT.1/GT.2. It only touches `scripts/vitruvius/graph/` Python modules and can land in parallel with the Rust work.
- **GT.4 is blocked on GT.2.** It cannot start until the in-flight GT.2 agent has exposed a Python-callable `LinearOctree` with at least a `query_sphere(center_xyz, radius) -> list[str]` method. If GT.2 is still in flight when a GT.4 task is picked up, the picker should poll the branch for the pyo3 module first.
- **GT.5.1 mmap loader** is Python-only and parallel-safe with everything else (it doesn't need the Rust crate — it's a thin wrapper around `mmap` stdlib that the Rust engine can also import via FFI later).
- **GT.5.2 Bloom filter** is a pure utility with zero cross-stream coupling.
- **GT.5.3 MC Dropout** is a pure math utility with zero cross-stream coupling.

---

## 4. Execution Streams

### Stream GT.1: The Binary Data Plane (Rust/Python Bridge)

**Status: in-flight in the 2026-04-15 ollama-online unblock pass — see commit history on `feat/sprint-r-per-layer-embeddings`.**

Original narrative targets (preserved for context, **not re-spec'd**):
- Setup `pyo3` bridge in `scripts/vitruvius/engine_rs/`.
- Implement FlatBuffer schemas for `SpatialNode` and `LegalEdge`.
- Configure Apache Arrow buffers for zero-copy geometry streaming.
- Benchmark 10,000 node reads; target <5ms Python-to-Rust roundtrip.

### Stream GT.2: Sparse Linear Octree Engine (The "Where")

**Status: in-flight in the 2026-04-15 ollama-online unblock pass — see commit history on `feat/sprint-r-per-layer-embeddings`.**

Original narrative targets (preserved for context, **not re-spec'd**):
- Linear Octree with flat `Vec` storage for cache locality.
- SIMD-optimized bounds checker (8 octants per cycle).
- Recursive search (point, sphere, frustum).
- Traverse a 100k-node model; target <1ms search time.

---

## 5. Stream GT.3 — Temporal Knowledge Graph (TDD Expansion)

**Goal:** Upgrade Phase 8 edges to time-bound quadruples $(s, p, o, t)$ using the shipped Sprint HP.3 SQLite event store.

### Task GT.3.1: Temporal Edge Schema

**Files:**
- Modify: `scripts/vitruvius/graph/contract.py` (add `TemporalEdge` dataclass + `validate_temporal_edge`)
- Create: `scripts/tests/test_temporal_edge_schema.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_temporal_edge_schema.py
"""Sprint GT Stream GT.3.1 — TemporalEdge schema."""
from __future__ import annotations

import pytest

from vitruvius.graph.contract import (
    ContractViolation,
    GraphEdge,
    TemporalEdge,
    validate_temporal_edge,
)


def test_temporal_edge_round_trip() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0001",
        status="verified",
        valid_from="1977-02-19T00:00:00Z",
        valid_until="2004-11-30T00:00:00Z",
    )
    assert edge.from_id == "law-pd-1096"
    assert edge.valid_from == "1977-02-19T00:00:00Z"
    assert edge.valid_until == "2004-11-30T00:00:00Z"
    validate_temporal_edge(edge)


def test_temporal_edge_open_interval_allowed() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0002",
        status="verified",
        valid_from="2004-12-01T00:00:00Z",
        valid_until=None,
    )
    validate_temporal_edge(edge)


def test_temporal_edge_rejects_bad_valid_from() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0003",
        status="verified",
        valid_from="not-a-date",
        valid_until=None,
    )
    with pytest.raises(ContractViolation):
        validate_temporal_edge(edge)


def test_temporal_edge_rejects_inverted_interval() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0004",
        status="verified",
        valid_from="2010-01-01T00:00:00Z",
        valid_until="2005-01-01T00:00:00Z",
    )
    with pytest.raises(ContractViolation):
        validate_temporal_edge(edge)


def test_temporal_edge_ordering_is_stable() -> None:
    a = TemporalEdge(
        from_id="law-pd-1096", to_id="concept-x", type="requires",
        evidence_id="rel-001", status="verified",
        valid_from="2000-01-01T00:00:00Z", valid_until=None,
    )
    b = TemporalEdge(
        from_id="law-pd-1096", to_id="concept-x", type="requires",
        evidence_id="rel-002", status="verified",
        valid_from="2010-01-01T00:00:00Z", valid_until=None,
    )
    ordered = sorted([b, a], key=lambda e: e.valid_from)
    assert ordered[0].valid_from == "2000-01-01T00:00:00Z"
    assert ordered[1].valid_from == "2010-01-01T00:00:00Z"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_temporal_edge_schema.py -v`

Expected: FAIL with `ImportError: cannot import name 'TemporalEdge' from 'vitruvius.graph.contract'`.

- [ ] **Step 3: Implement `TemporalEdge` in `scripts/vitruvius/graph/contract.py`**

Append after the existing `GraphEdge` dataclass:

```python
@dataclass(frozen=True)
class TemporalEdge:
    """Stream GT.3.1 — a time-bound edge: (s, p, o, [valid_from, valid_until)).

    ``valid_until`` is ``None`` for open intervals (edge is still valid).
    Timestamps MUST be ISO-8601 UTC strings to match the rest of the
    graph contract.
    """
    from_id: str
    to_id: str
    type: str
    evidence_id: str
    status: str
    valid_from: str
    valid_until: str | None = None


def validate_temporal_edge(edge: TemporalEdge) -> None:
    """Validate a TemporalEdge. Delegates the s/p/o checks to the
    regular ``validate_edge`` helper by projecting onto a GraphEdge,
    then layers on the valid_from/valid_until checks on top."""
    projection = GraphEdge(
        from_id=edge.from_id,
        to_id=edge.to_id,
        type=edge.type,
        evidence_id=edge.evidence_id,
        status=edge.status,
    )
    validate_edge(projection)

    if not isinstance(edge.valid_from, str) or not _ISO_DATE_RE.match(edge.valid_from):
        raise ContractViolation(
            f"temporal edge valid_from {edge.valid_from!r} is not a valid ISO-8601 date"
        )
    if edge.valid_until is not None:
        if not isinstance(edge.valid_until, str) or not _ISO_DATE_RE.match(edge.valid_until):
            raise ContractViolation(
                f"temporal edge valid_until {edge.valid_until!r} is not a valid ISO-8601 date"
            )
        if edge.valid_until <= edge.valid_from:
            raise ContractViolation(
                f"temporal edge valid_until {edge.valid_until!r} must be strictly after "
                f"valid_from {edge.valid_from!r}"
            )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_temporal_edge_schema.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/graph/contract.py scripts/tests/test_temporal_edge_schema.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.3.1 TemporalEdge schema + validator"
```

---

### Task GT.3.2: Versioned Retrieval (Query At Timestamp)

**Files:**
- Create: `scripts/vitruvius/graph/temporal_query.py`
- Create: `scripts/tests/test_temporal_query.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_temporal_query.py
"""Sprint GT Stream GT.3.2 — versioned retrieval of TemporalEdges."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.contract import TemporalEdge
from vitruvius.graph.temporal_query import query_at


@pytest.fixture
def three_edge_timeline() -> list[TemporalEdge]:
    return [
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-001", status="verified",
            valid_from="1977-02-19T00:00:00Z",
            valid_until="2004-11-30T00:00:00Z",
        ),
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-002", status="verified",
            valid_from="2004-12-01T00:00:00Z",
            valid_until="2015-12-31T00:00:00Z",
        ),
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-003", status="verified",
            valid_from="2016-01-01T00:00:00Z",
            valid_until=None,
        ),
    ]


def test_query_in_first_window_returns_first_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="1990-06-15T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-001"


def test_query_in_second_window_returns_second_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2008-08-08T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-002"


def test_query_in_open_window_returns_current_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2026-04-15T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-003"


def test_query_before_first_window_is_empty(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="1900-01-01T00:00:00Z",
    )
    assert result == []


def test_query_at_exact_boundary_includes_starting_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2004-12-01T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-002"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_temporal_query.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.graph.temporal_query'`.

- [ ] **Step 3: Implement `temporal_query.py`**

```python
# scripts/vitruvius/graph/temporal_query.py
"""Sprint GT Stream GT.3.2 — versioned retrieval for TemporalEdges.

Mirrors the projection semantics of
``scripts/vitruvius/graph/event_store.project_graph_at`` (Sprint HP.3)
but works on the in-memory ``TemporalEdge`` list that the Phase 8
snapshot builder produces. The event store's ``project_graph_at``
remains the authoritative on-disk projector; this module is the
in-memory equivalent that reads from a pre-materialised list.
"""
from __future__ import annotations

from typing import Iterable

from vitruvius.graph.contract import TemporalEdge


def query_at(
    edges: Iterable[TemporalEdge],
    *,
    timestamp_utc: str,
) -> list[TemporalEdge]:
    """Return every ``TemporalEdge`` whose
    ``valid_from <= timestamp_utc`` and
    (``valid_until`` is ``None`` or ``timestamp_utc < valid_until``).

    Timestamps are compared as ISO-8601 strings — the contract
    validator guarantees the format is lexicographically sortable.
    """
    matches: list[TemporalEdge] = []
    for edge in edges:
        if edge.valid_from > timestamp_utc:
            continue
        if edge.valid_until is not None and timestamp_utc >= edge.valid_until:
            continue
        matches.append(edge)
    return matches
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_temporal_query.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/graph/temporal_query.py scripts/tests/test_temporal_query.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.3.2 versioned retrieval for TemporalEdges"
```

---

### Task GT.3.3: Parquet Archiver for Cold Storage

**Files:**
- Create: `scripts/vitruvius/graph/parquet_archiver.py`
- Create: `scripts/tests/test_parquet_archiver.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_parquet_archiver.py
"""Sprint GT Stream GT.3.3 — Parquet archiver round-trip."""
from __future__ import annotations

from pathlib import Path

import pytest

pyarrow = pytest.importorskip("pyarrow")

from vitruvius.graph.contract import TemporalEdge
from vitruvius.graph.parquet_archiver import (
    read_temporal_edges_from_parquet,
    write_temporal_edges_to_parquet,
)


@pytest.fixture
def five_edge_snapshot() -> list[TemporalEdge]:
    return [
        TemporalEdge(
            from_id=f"law-pd-109{i}",
            to_id="concept-egress-width",
            type="requires",
            evidence_id=f"rel-{i:04d}",
            status="verified",
            valid_from=f"200{i}-01-01T00:00:00Z",
            valid_until=None if i == 4 else f"201{i}-01-01T00:00:00Z",
        )
        for i in range(5)
    ]


def test_round_trip_preserves_row_count(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    assert out.exists()
    recovered = read_temporal_edges_from_parquet(out)
    assert len(recovered) == 5


def test_round_trip_preserves_field_values(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    recovered = read_temporal_edges_from_parquet(out)

    for original, restored in zip(five_edge_snapshot, recovered):
        assert restored.from_id == original.from_id
        assert restored.to_id == original.to_id
        assert restored.type == original.type
        assert restored.evidence_id == original.evidence_id
        assert restored.status == original.status
        assert restored.valid_from == original.valid_from
        assert restored.valid_until == original.valid_until


def test_round_trip_preserves_open_interval(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    recovered = read_temporal_edges_from_parquet(out)
    assert recovered[4].valid_until is None


def test_empty_list_round_trips(tmp_path: Path) -> None:
    out = tmp_path / "empty.parquet"
    write_temporal_edges_to_parquet([], out)
    assert out.exists()
    recovered = read_temporal_edges_from_parquet(out)
    assert recovered == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_parquet_archiver.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.graph.parquet_archiver'`.

- [ ] **Step 3: Implement `parquet_archiver.py`**

```python
# scripts/vitruvius/graph/parquet_archiver.py
"""Sprint GT Stream GT.3.3 — Parquet archiver for TemporalEdge snapshots.

Uses pyarrow (already installed as a transitive Docling dependency).
Produces a columnar Parquet file suitable for cold-storage archival
of graph snapshots at a given UTC timestamp.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pyarrow as pa
import pyarrow.parquet as pq

from vitruvius.graph.contract import TemporalEdge


_SCHEMA = pa.schema([
    ("from_id", pa.string()),
    ("to_id", pa.string()),
    ("type", pa.string()),
    ("evidence_id", pa.string()),
    ("status", pa.string()),
    ("valid_from", pa.string()),
    ("valid_until", pa.string()),  # nullable — None becomes pa.null()
])


def write_temporal_edges_to_parquet(
    edges: Iterable[TemporalEdge],
    path: Path,
) -> None:
    """Write a sequence of TemporalEdges to a Parquet file at ``path``.
    The parent directory is created if missing. An empty iterable
    still produces a valid, schema-only Parquet file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = list(edges)
    columns: dict[str, list] = {
        "from_id": [e.from_id for e in rows],
        "to_id": [e.to_id for e in rows],
        "type": [e.type for e in rows],
        "evidence_id": [e.evidence_id for e in rows],
        "status": [e.status for e in rows],
        "valid_from": [e.valid_from for e in rows],
        "valid_until": [e.valid_until for e in rows],
    }
    table = pa.Table.from_pydict(columns, schema=_SCHEMA)
    pq.write_table(table, path)


def read_temporal_edges_from_parquet(path: Path) -> list[TemporalEdge]:
    """Read a Parquet file produced by ``write_temporal_edges_to_parquet``
    and rebuild the list of TemporalEdges. Preserves ``None`` for the
    open-interval ``valid_until`` column."""
    table = pq.read_table(Path(path))
    n = table.num_rows
    if n == 0:
        return []

    from_id = table.column("from_id").to_pylist()
    to_id = table.column("to_id").to_pylist()
    type_ = table.column("type").to_pylist()
    evidence_id = table.column("evidence_id").to_pylist()
    status = table.column("status").to_pylist()
    valid_from = table.column("valid_from").to_pylist()
    valid_until = table.column("valid_until").to_pylist()

    return [
        TemporalEdge(
            from_id=from_id[i],
            to_id=to_id[i],
            type=type_[i],
            evidence_id=evidence_id[i],
            status=status[i],
            valid_from=valid_from[i],
            valid_until=valid_until[i],
        )
        for i in range(n)
    ]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_parquet_archiver.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/graph/parquet_archiver.py scripts/tests/test_parquet_archiver.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.3.3 Parquet archiver for TemporalEdge snapshots"
```

---

## 6. Stream GT.4 — Geo-Topological Bridging (TDD Expansion)

**Goal:** Seed GraphRAG with physical proximity results drawn from the in-flight `engine_rs` `LinearOctree`.

> **Cross-stream gate:** Do not start these tasks until the GT.2 implementer has landed a Python-callable `LinearOctree` with at least an `insert(id, xyz, aabb)` / `query_sphere(center, radius) -> list[str]` pair. If the branch does not yet expose `from vitruvius.engine_rs import LinearOctree`, poll the branch commit log before starting.

### Task GT.4.1: Proximity Jump — Octree → Snapshot Bridge

**Files:**
- Create: `scripts/vitruvius/spatial/proximity_jump.py`
- Create: `scripts/tests/test_proximity_jump.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_proximity_jump.py
"""Sprint GT Stream GT.4.1 — proximity jump from octree to snapshot IDs."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from vitruvius.spatial.proximity_jump import proximity_jump_seed


@dataclass
class FakeOctree:
    """Test double — the real one comes from engine_rs (Stream GT.2)."""
    points: dict[str, tuple[float, float, float]]

    def query_sphere(
        self, center: tuple[float, float, float], radius: float
    ) -> list[str]:
        cx, cy, cz = center
        hits = []
        for pid, (x, y, z) in self.points.items():
            dist_sq = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            if dist_sq <= radius * radius:
                hits.append(pid)
        return hits


@dataclass
class FakeGraphNode:
    id: str


@dataclass
class FakeSnapshot:
    nodes: list[FakeGraphNode]


def test_proximity_jump_returns_two_closest() -> None:
    octree = FakeOctree(
        points={
            "spatial-col-01": (0.0, 0.0, 0.0),
            "spatial-col-02": (0.5, 0.5, 0.0),
            "spatial-col-03": (10.0, 10.0, 10.0),
            "spatial-col-04": (0.8, 0.0, 0.0),
            "spatial-col-05": (100.0, 100.0, 100.0),
        }
    )
    snapshot = FakeSnapshot(
        nodes=[
            FakeGraphNode(id="spatial-col-01"),
            FakeGraphNode(id="spatial-col-02"),
            FakeGraphNode(id="spatial-col-03"),
            FakeGraphNode(id="spatial-col-04"),
            FakeGraphNode(id="spatial-col-05"),
        ]
    )
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert sorted(seeds) == ["spatial-col-01", "spatial-col-02", "spatial-col-04"]


def test_proximity_jump_filters_unknown_ids() -> None:
    octree = FakeOctree(
        points={
            "spatial-col-01": (0.0, 0.0, 0.0),
            "spatial-ghost-99": (0.1, 0.1, 0.0),  # not in snapshot
        }
    )
    snapshot = FakeSnapshot(nodes=[FakeGraphNode(id="spatial-col-01")])
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert seeds == ["spatial-col-01"]


def test_proximity_jump_empty_result() -> None:
    octree = FakeOctree(
        points={"spatial-far-01": (1000.0, 1000.0, 1000.0)}
    )
    snapshot = FakeSnapshot(nodes=[FakeGraphNode(id="spatial-far-01")])
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert seeds == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_proximity_jump.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.spatial.proximity_jump'`.

- [ ] **Step 3: Implement `proximity_jump.py`**

```python
# scripts/vitruvius/spatial/proximity_jump.py
"""Sprint GT Stream GT.4.1 — bridge engine_rs octree → Phase 8 snapshot.

Takes an octree (duck-typed — any object with
``query_sphere(center_xyz, radius) -> list[str]``) and a snapshot
(duck-typed — any object with an iterable ``.nodes`` attribute whose
elements expose an ``.id`` attribute) and returns the set of
snapshot-node IDs that fall inside the sphere.
"""
from __future__ import annotations

from typing import Any, Protocol


class _OctreeLike(Protocol):
    def query_sphere(
        self, center: tuple[float, float, float], radius: float
    ) -> list[str]:
        ...


def proximity_jump_seed(
    *,
    octree: _OctreeLike,
    focal_xyz: tuple[float, float, float],
    radius: float,
    snapshot: Any,
) -> list[str]:
    """Return snapshot-node IDs that lie within ``radius`` of ``focal_xyz``.

    IDs returned by the octree that are NOT present in the snapshot
    are filtered out — a stale octree entry should not poison the
    GraphRAG seed set.
    """
    octree_hits = list(octree.query_sphere(focal_xyz, radius))
    known_ids = {node.id for node in snapshot.nodes}
    return [hit for hit in octree_hits if hit in known_ids]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_proximity_jump.py -v`

Expected: 3 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/proximity_jump.py scripts/tests/test_proximity_jump.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.4.1 proximity-jump seed from octree to snapshot"
```

---

### Task GT.4.2: Geometric Weighting (Distance Decay)

**Files:**
- Modify: `scripts/vitruvius/spatial/proximity_jump.py` (add `weight_by_distance`)
- Create: `scripts/tests/test_geometric_weighting.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_geometric_weighting.py
"""Sprint GT Stream GT.4.2 — exponential distance weighting."""
from __future__ import annotations

import math

import pytest

from vitruvius.spatial.proximity_jump import weight_by_distance


def test_closer_seed_has_higher_weight() -> None:
    seeds = {
        "spatial-a": (0.0, 0.0, 0.0),
        "spatial-b": (5.0, 0.0, 0.0),
    }
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert weights["spatial-a"] > weights["spatial-b"]


def test_weight_at_origin_is_one() -> None:
    seeds = {"spatial-a": (0.0, 0.0, 0.0)}
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert math.isclose(weights["spatial-a"], 1.0, abs_tol=1e-9)


def test_weight_follows_exp_minus_lambda_d() -> None:
    seeds = {"spatial-a": (3.0, 4.0, 0.0)}  # distance 5
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.2,
    )
    expected = math.exp(-0.2 * 5.0)
    assert math.isclose(weights["spatial-a"], expected, abs_tol=1e-9)


def test_empty_input_returns_empty() -> None:
    weights = weight_by_distance(
        {},
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert weights == {}


def test_larger_lambda_decays_faster() -> None:
    seeds = {
        "spatial-a": (10.0, 0.0, 0.0),
    }
    slow = weight_by_distance(
        seeds, focal_xyz=(0.0, 0.0, 0.0), lambda_decay=0.05
    )
    fast = weight_by_distance(
        seeds, focal_xyz=(0.0, 0.0, 0.0), lambda_decay=0.5
    )
    assert slow["spatial-a"] > fast["spatial-a"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_geometric_weighting.py -v`

Expected: FAIL with `ImportError: cannot import name 'weight_by_distance'`.

- [ ] **Step 3: Extend `proximity_jump.py` with the weight helper**

Append to `scripts/vitruvius/spatial/proximity_jump.py`:

```python
import math
from typing import Mapping


def weight_by_distance(
    seeds: Mapping[str, tuple[float, float, float]],
    *,
    focal_xyz: tuple[float, float, float],
    lambda_decay: float = 0.1,
) -> dict[str, float]:
    """Return ``{seed_id: exp(-lambda_decay * d)}`` for each seed.

    ``d`` is Euclidean distance from ``focal_xyz``. Output values
    lie in ``(0.0, 1.0]`` — the seed AT the focal point scores 1.0,
    seeds far away asymptote to 0.0. Empty input returns an empty
    dict.
    """
    fx, fy, fz = focal_xyz
    weights: dict[str, float] = {}
    for seed_id, (x, y, z) in seeds.items():
        distance = math.sqrt((x - fx) ** 2 + (y - fy) ** 2 + (z - fz) ** 2)
        weights[seed_id] = math.exp(-lambda_decay * distance)
    return weights
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_geometric_weighting.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/proximity_jump.py scripts/tests/test_geometric_weighting.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.4.2 exponential distance weighting for seeds"
```

---

### Task GT.4.3: Spatial Edge Generator (`physically_adjacent_to`)

**Files:**
- Create: `scripts/vitruvius/spatial/spatial_edge_builder.py`
- Modify: `config/vitruvius.yaml` (add `gt_spatial_edges: false` flag)
- Create: `scripts/tests/test_spatial_edge_builder.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_edge_builder.py
"""Sprint GT Stream GT.4.3 — spatial edge generator for adjacent AABBs."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from vitruvius.spatial.spatial_edge_builder import (
    SpatialPoint,
    build_spatial_adjacency_edges,
)


@dataclass
class AABB:
    min_xyz: tuple[float, float, float]
    max_xyz: tuple[float, float, float]


def test_two_overlapping_points_produce_one_edge() -> None:
    points = [
        SpatialPoint(
            id="spatial-col-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="spatial-col-02",
            aabb=AABB(min_xyz=(0.5, 0.5, 0.5), max_xyz=(1.5, 1.5, 1.5)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert len(edges) == 1
    assert edges[0].from_id == "spatial-col-01"
    assert edges[0].to_id == "spatial-col-02"
    assert edges[0].type == "physically_adjacent_to"


def test_two_distant_points_produce_no_edges() -> None:
    points = [
        SpatialPoint(
            id="spatial-col-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="spatial-col-02",
            aabb=AABB(min_xyz=(10.0, 10.0, 10.0), max_xyz=(11.0, 11.0, 11.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert edges == []


def test_touching_edges_count_as_adjacent() -> None:
    points = [
        SpatialPoint(
            id="spatial-wall-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="spatial-wall-02",
            aabb=AABB(min_xyz=(1.0, 0.0, 0.0), max_xyz=(2.0, 1.0, 1.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert len(edges) == 1


def test_three_points_produces_stable_pair_ordering() -> None:
    points = [
        SpatialPoint(
            id="spatial-a",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="spatial-b",
            aabb=AABB(min_xyz=(0.5, 0.5, 0.5), max_xyz=(1.5, 1.5, 1.5)),
        ),
        SpatialPoint(
            id="spatial-c",
            aabb=AABB(min_xyz=(0.9, 0.9, 0.9), max_xyz=(2.0, 2.0, 2.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    # Three mutually-overlapping AABBs → 3 choose 2 = 3 unique pairs.
    assert len(edges) == 3
    pair_set = {(e.from_id, e.to_id) for e in edges}
    assert pair_set == {
        ("spatial-a", "spatial-b"),
        ("spatial-a", "spatial-c"),
        ("spatial-b", "spatial-c"),
    }
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_edge_builder.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.spatial.spatial_edge_builder'`.

- [ ] **Step 3: Implement `spatial_edge_builder.py`**

```python
# scripts/vitruvius/spatial/spatial_edge_builder.py
"""Sprint GT Stream GT.4.3 — `physically_adjacent_to` edge generator.

For every pair of SpatialPoints whose AABBs intersect (or touch)
this module emits one GraphEdge with predicate
``physically_adjacent_to``. The builder uses Python-native AABB
intersection for the O(n^2) first implementation; when the
engine_rs LinearOctree lands (Stream GT.2), the builder can be
rewritten to use the octree's neighbour enumerator for
O(n log n) behaviour.

The snapshot builder is expected to call this function only when
``config.features.gt_spatial_edges`` is true.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class SpatialPoint:
    id: str
    aabb: Any  # duck-typed: needs .min_xyz and .max_xyz 3-tuples


@dataclass(frozen=True)
class SpatialEdge:
    from_id: str
    to_id: str
    type: str = "physically_adjacent_to"


def _aabbs_intersect(a: Any, b: Any) -> bool:
    ax0, ay0, az0 = a.min_xyz
    ax1, ay1, az1 = a.max_xyz
    bx0, by0, bz0 = b.min_xyz
    bx1, by1, bz1 = b.max_xyz
    if ax1 < bx0 or bx1 < ax0:
        return False
    if ay1 < by0 or by1 < ay0:
        return False
    if az1 < bz0 or bz1 < az0:
        return False
    return True


def build_spatial_adjacency_edges(
    points: Iterable[SpatialPoint],
) -> list[SpatialEdge]:
    """Return one SpatialEdge per pair of intersecting AABBs.

    Edges are emitted in input order — if ``points[i]`` precedes
    ``points[j]`` and their AABBs intersect, the edge is
    ``SpatialEdge(from_id=points[i].id, to_id=points[j].id)``.
    """
    materialised = list(points)
    edges: list[SpatialEdge] = []
    for i in range(len(materialised)):
        for j in range(i + 1, len(materialised)):
            if _aabbs_intersect(materialised[i].aabb, materialised[j].aabb):
                edges.append(
                    SpatialEdge(
                        from_id=materialised[i].id,
                        to_id=materialised[j].id,
                    )
                )
    return edges
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_edge_builder.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/spatial_edge_builder.py scripts/tests/test_spatial_edge_builder.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.4.3 physically_adjacent_to edge generator behind gt_spatial_edges flag"
```

---

## 7. Stream GT.5 — Hardware Hardening (TDD Expansion)

**Goal:** Mathematically eliminate memory pressure on the 8GB M2 host. All three tasks are pure Python, stdlib-first, and parallel-safe with every other Sprint GT stream.

### Task GT.5.1: mmap Loader for Binary Octree Pages

**Files:**
- Create: `scripts/vitruvius/engine_rs/mmap_loader.py`
- Create: `scripts/tests/test_mmap_loader.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_mmap_loader.py
"""Sprint GT Stream GT.5.1 — mmap-backed page loader for octree binary files."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.engine_rs.mmap_loader import (
    MmapPageReader,
    open_page_file,
)


@pytest.fixture
def fixture_page_file(tmp_path: Path) -> Path:
    """Write a 256-byte fixture page file: bytes 0..255 repeating."""
    path = tmp_path / "page_000.bin"
    path.write_bytes(bytes(range(256)))
    return path


def test_open_page_file_returns_reader(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        assert isinstance(reader, MmapPageReader)
        assert reader.size == 256


def test_read_first_100_bytes(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        data = reader.read(0, 100)
        assert len(data) == 100
        assert data == bytes(range(100))


def test_read_midfile_slice(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        data = reader.read(50, 10)
        assert data == bytes(range(50, 60))


def test_read_beyond_eof_raises(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        with pytest.raises(ValueError):
            reader.read(250, 100)  # 250 + 100 > 256


def test_context_manager_releases_mmap(fixture_page_file: Path) -> None:
    reader = open_page_file(fixture_page_file)
    with reader:
        pass
    # After exit the underlying mmap should be closed; reading
    # should fail with RuntimeError (our wrapper) or ValueError
    # (bare mmap).
    with pytest.raises((RuntimeError, ValueError)):
        reader.read(0, 1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_mmap_loader.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.engine_rs.mmap_loader'`.

- [ ] **Step 3: Implement `mmap_loader.py`**

```python
# scripts/vitruvius/engine_rs/mmap_loader.py
"""Sprint GT Stream GT.5.1 — mmap-backed lazy page loader.

Thin Python wrapper around ``mmap.mmap`` so the GT.2 engine_rs
Rust crate (and the Python side) can share the same on-disk
octree page format. Keeping the loader in Python makes it
available before the Rust crate finishes its mmap integration
and lets the test suite exercise page behaviour without building
Rust.
"""
from __future__ import annotations

import mmap
from pathlib import Path
from types import TracebackType
from typing import Optional


class MmapPageReader:
    """Context-managed, read-only view over a binary page file."""

    def __init__(self, fh, mm: mmap.mmap) -> None:
        self._fh = fh
        self._mm: Optional[mmap.mmap] = mm

    @property
    def size(self) -> int:
        if self._mm is None:
            raise RuntimeError("page file is closed")
        return len(self._mm)

    def read(self, offset: int, length: int) -> bytes:
        if self._mm is None:
            raise RuntimeError("page file is closed")
        if offset < 0 or length < 0:
            raise ValueError(f"offset/length must be non-negative (got {offset}, {length})")
        if offset + length > len(self._mm):
            raise ValueError(
                f"read range [{offset}, {offset + length}) exceeds "
                f"page file size {len(self._mm)}"
            )
        return bytes(self._mm[offset : offset + length])

    def close(self) -> None:
        if self._mm is not None:
            self._mm.close()
            self._mm = None
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    def __enter__(self) -> "MmapPageReader":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()


def open_page_file(path: Path) -> MmapPageReader:
    """Open a binary page file and return a read-only
    ``MmapPageReader``. Caller must use the returned reader as a
    context manager (or explicitly call ``close``)."""
    path = Path(path)
    fh = open(path, "rb")
    mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
    return MmapPageReader(fh, mm)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_mmap_loader.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/engine_rs/mmap_loader.py scripts/tests/test_mmap_loader.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.5.1 mmap-backed page reader for octree binary files"
```

---

### Task GT.5.2: Bloom Filter for Ingestion Dedup

**Files:**
- Create: `scripts/vitruvius/foraging/bloom_filter.py`
- Create: `scripts/tests/test_bloom_filter.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_bloom_filter.py
"""Sprint GT Stream GT.5.2 — Bloom filter for ingestion dedup."""
from __future__ import annotations

import random

import pytest

from vitruvius.foraging.bloom_filter import BloomFilter


def test_contains_returns_false_before_add() -> None:
    bf = BloomFilter(size=1024, hash_count=4)
    assert bf.contains("hello") is False


def test_add_then_contains_returns_true() -> None:
    bf = BloomFilter(size=1024, hash_count=4)
    bf.add("hello")
    assert bf.contains("hello") is True


def test_many_items_reproducible() -> None:
    bf = BloomFilter(size=10000, hash_count=5)
    for i in range(100):
        bf.add(f"item-{i}")
    for i in range(100):
        assert bf.contains(f"item-{i}") is True


def test_false_positive_rate_under_5_percent() -> None:
    random.seed(42)
    bf = BloomFilter(size=10000, hash_count=7)
    inserted = {f"inserted-{i}" for i in range(1000)}
    for item in inserted:
        bf.add(item)

    false_positives = 0
    trials = 2000
    for i in range(trials):
        probe = f"probe-{i}"
        if probe in inserted:
            continue
        if bf.contains(probe):
            false_positives += 1

    rate = false_positives / trials
    assert rate < 0.05, f"false positive rate {rate:.3%} exceeds 5% budget"


def test_invalid_size_raises() -> None:
    with pytest.raises(ValueError):
        BloomFilter(size=0, hash_count=4)
    with pytest.raises(ValueError):
        BloomFilter(size=1024, hash_count=0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_bloom_filter.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.foraging.bloom_filter'`.

- [ ] **Step 3: Implement `bloom_filter.py`**

```python
# scripts/vitruvius/foraging/bloom_filter.py
"""Sprint GT Stream GT.5.2 — stdlib-only Bloom filter.

Uses ``hashlib.blake2b`` with distinct salts to derive
``hash_count`` independent hash functions, and stores the
bit-vector in a ``bytearray`` (no third-party bitarray
dependency). Intended for dropping redundant ingestion records
before they hit the engine.
"""
from __future__ import annotations

import hashlib


class BloomFilter:
    def __init__(self, size: int, hash_count: int) -> None:
        if size <= 0:
            raise ValueError(f"size must be positive (got {size})")
        if hash_count <= 0:
            raise ValueError(f"hash_count must be positive (got {hash_count})")
        self._size = int(size)
        self._hash_count = int(hash_count)
        byte_len = (self._size + 7) // 8
        self._bits = bytearray(byte_len)

    def _positions(self, item: str) -> list[int]:
        data = item.encode("utf-8")
        positions: list[int] = []
        for k in range(self._hash_count):
            salt = k.to_bytes(4, "little")
            digest = hashlib.blake2b(data + salt, digest_size=8).digest()
            positions.append(int.from_bytes(digest, "little") % self._size)
        return positions

    def add(self, item: str) -> None:
        for pos in self._positions(item):
            self._bits[pos // 8] |= 1 << (pos % 8)

    def contains(self, item: str) -> bool:
        for pos in self._positions(item):
            if not (self._bits[pos // 8] & (1 << (pos % 8))):
                return False
        return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_bloom_filter.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/foraging/bloom_filter.py scripts/tests/test_bloom_filter.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.5.2 stdlib Bloom filter for ingestion dedup"
```

---

### Task GT.5.3: MC Dropout Epistemic Uncertainty

**Files:**
- Create: `scripts/vitruvius/graph/mc_dropout.py`
- Create: `scripts/tests/test_mc_dropout.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_mc_dropout.py
"""Sprint GT Stream GT.5.3 — Monte Carlo dropout epistemic uncertainty."""
from __future__ import annotations

import math

import pytest

from vitruvius.graph.mc_dropout import compute_epistemic_uncertainty


def test_identical_predictions_are_zero_uncertainty() -> None:
    preds = [0.8] * 20
    result = compute_epistemic_uncertainty(preds)
    assert math.isclose(result, 0.0, abs_tol=1e-9)


def test_spread_predictions_are_positive_uncertainty() -> None:
    preds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    result = compute_epistemic_uncertainty(preds)
    assert result > 0.0


def test_uncertainty_increases_with_spread() -> None:
    tight = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.6]
    wide = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 1.0]
    assert compute_epistemic_uncertainty(wide) > compute_epistemic_uncertainty(tight)


def test_empty_predictions_raises() -> None:
    with pytest.raises(ValueError):
        compute_epistemic_uncertainty([])


def test_single_prediction_is_zero_uncertainty() -> None:
    result = compute_epistemic_uncertainty([0.7])
    assert math.isclose(result, 0.0, abs_tol=1e-9)


def test_num_samples_caps_the_input() -> None:
    # num_samples=3 → only the first 3 predictions are considered.
    preds = [0.1, 0.1, 0.1, 0.9, 0.9, 0.9]
    result = compute_epistemic_uncertainty(preds, num_samples=3)
    assert math.isclose(result, 0.0, abs_tol=1e-9)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_mc_dropout.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.graph.mc_dropout'`.

- [ ] **Step 3: Implement `mc_dropout.py`**

```python
# scripts/vitruvius/graph/mc_dropout.py
"""Sprint GT Stream GT.5.3 — Monte Carlo dropout epistemic uncertainty.

Given the list of per-sample predictions collected from a model
run with dropout ENABLED at inference time (classic Gal & Ghahramani
2016 MC-dropout recipe), this module reports the sample variance
as the epistemic uncertainty estimate. Stdlib-only — no numpy
dependency so it can run on the 8GB M2 boot path.
"""
from __future__ import annotations

import statistics
from typing import Sequence


def compute_epistemic_uncertainty(
    model_predictions: Sequence[float],
    *,
    num_samples: int = 20,
) -> float:
    """Return the sample variance over at most ``num_samples`` MC
    dropout predictions.

    Raises ``ValueError`` if ``model_predictions`` is empty.
    A single prediction returns 0.0 (variance is undefined for
    one sample, but for our API we treat it as "no spread").
    """
    if not model_predictions:
        raise ValueError("model_predictions must be a non-empty sequence")

    window = list(model_predictions)[: max(0, int(num_samples))]
    if len(window) <= 1:
        return 0.0

    return float(statistics.variance(window))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_mc_dropout.py -v`

Expected: 6 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/graph/mc_dropout.py scripts/tests/test_mc_dropout.py
git commit -m "feat(engine_rs): Sprint GT Stream GT.5.3 MC dropout epistemic uncertainty utility"
```

---

## 8. Tech Stack Requirements

- **Engine:** Rust (`pyo3`, `arrow`, `flatbuffers`, `memmap2`) — landed by the in-flight GT.1/GT.2 agent.
- **Math:** `glam` or `nalgebra` for SIMD-accelerated 3D primitives — scoped to GT.1/GT.2.
- **Python:** `pyarrow` (already installed via Docling transitive — used by GT.3.3). No new Python dependencies for GT.3/GT.4/GT.5 beyond stdlib + pyarrow.
- **Storage:** SQLite (stdlib) via the shipped Sprint HP.3 `EventStore`. (The original spec called for RocksDB; we did not take that dependency — see `scripts/vitruvius/graph/event_store.py` module docstring for rationale.)

---

## 9. Implementation Workflow

1.  **Foundation (in-flight):** GT.1 + GT.2 ship the Rust crate, Linear Octree, and pyo3 bridge.
2.  **Temporal (parallel-safe, start immediately):** GT.3.1 → GT.3.2 → GT.3.3 against the existing event store.
3.  **Hardware (parallel-safe, start immediately):** GT.5.1, GT.5.2, GT.5.3 — each is fully independent.
4.  **Spatial Bridging (gated on GT.2):** GT.4.1 → GT.4.2 → GT.4.3 once `from vitruvius.engine_rs import LinearOctree` imports cleanly.
5.  **Inference wiring (FUTURE):** Plumb the spatial-temporal seed set into the review prompt context. Tracked in a follow-up plan once Streams GT.3 and GT.4 are green.

---

## 10. Success Metrics

| Metric | Baseline (Traditional) | Target (Geo-Topological) |
|---|---|---|
| **Search Speed** | $O(N)$ (Scan all rules) | $O(\log N)$ (Octree Pruning) |
| **Data Access** | JSON Parsing (Slow) | Zero-Copy Arrow (Instant) |
| **Memory Footprint** | Loads full dataset | Loads active pages (mmap) |
| **Reasoning Quality** | Semantic-only | Semantic + Physical Proximity |
| **Temporal Fidelity** | Latest version only | Versioned query at any ISO-8601 timestamp |
| **Ingestion Dedup** | None (full pipeline pays) | Bloom filter short-circuits redundant inputs |
| **Epistemic Honesty** | Point estimates | MC-dropout variance per decision |
