---
plan_id: phase-8-graph-contract-indexing
phase: 8
title: Graph Contract & Filesystem-Backed Indexing
status: gated
priority: medium
sprint: "Post-Sprint-C (after Phase 7 produces >= 50 verified relationships)"
version: 1.0.0
plan_type: design_spec
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 7 Promotion Governance shipping, >= 50 verified relationships
  - Filesystem Graph Contract frozen (master-roadmap §3.6)
dependencies:
  - .ai/06_specs/relationship-schema.md
  - .ai/06_specs/source-schema.md
  - .ai/06_specs/concept-schema.md
  - 003_Canonical-Knowledge-Layer/shared/relationships/
related_plans:
  - phase-7-promotion-governance-plan.md (upstream)
  - phase-9-query-ai-layer-plan.md (downstream)
gate:
  condition: "Phase 7 producing >= 50 verified relationships with zero audit violations for >= 1 week"
  rationale: "Build graph on validated edges only; do not graph draft data."
unblocks:
  - Phase 9 Query & AI Layer
  - Deterministic graph snapshots for external consumers
---

# Phase 8 — Graph Contract & Indexing Design Plan

**Goal:** Build the first queryable index over promoted relationships using a filesystem-backed graph implementation. Freeze the Filesystem Graph Contract from `master-roadmap.md` §3.6 and verify it against real PD 1096 data before any consideration of an external graph database.

**Architecture:** A new `graph/` subsystem in `scripts/vitruvius/` with four modules: `graph_contract.py` (schema validator for nodes and edges), `graph_builder.py` (walks canonical layer and produces typed node/edge records), `graph_snapshot.py` (emits a deterministic `latest_graph_snapshot.json` under `005_Operational-Intelligence-Layer/graph/`), and `graph_traverse.py` (typed, evidence-aware traversal helpers). The graph is rebuilt from scratch on every run — it is a cache of the canonical layer, not a separate source of truth.

**Tech Stack:** Python stdlib only. No graph database, no NetworkX dependency (the graph is small; linear walks are adequate and keep principle P1 intact).

---

## Why "Filesystem-Backed First"

Introducing Neo4j, Dgraph, or any external graph database before the contract is locked would:
1. Tie the schema to a specific query language.
2. Break principle P1 (filesystem is the database).
3. Make determinism hard — an external DB introduces query-engine version drift.

Once the filesystem contract is verified against real data, a later phase MAY add an opt-in external index. This plan does not enable that.

## Scope Boundary

**In scope:**
- Node schema from `master-roadmap.md` §3.6: `id, type, slug, trust_level, last_updated_utc`.
- Edge schema from §3.6: `from_id, to_id, type, evidence_id, status (verified|unverified)`.
- Walker over `003_Canonical-Knowledge-Layer/shared/{sources,concepts,relationships}`.
- Deterministic JSON snapshot (byte-identical outputs for identical inputs).
- Integrity checks: orphan detection, dangling-edge detection, predicate compatibility.
- Traversal helpers: `neighbors`, `typed_edges`, `evidence_joined_paths`.
- CLI commands: `build-graph`, `query-graph`, `export-graph-snapshot`.

**Out of scope:**
- Neo4j / Dgraph / external graph database integration.
- Visualization (Cytoscape, D3) — that's a Phase 9 / UI concern.
- NL querying (Phase 9).
- Embeddings, RAG, or vector search.

## File Structure

| Path | Purpose |
|---|---|
| `scripts/vitruvius/graph/__init__.py` | Package marker |
| `scripts/vitruvius/graph/contract.py` | Node / edge dataclasses + schema validator |
| `scripts/vitruvius/graph/builder.py` | Walker: canonical → nodes + edges |
| `scripts/vitruvius/graph/snapshot.py` | Deterministic JSON snapshot writer |
| `scripts/vitruvius/graph/integrity.py` | Orphan / dangling / type checks |
| `scripts/vitruvius/graph/traverse.py` | `neighbors`, `typed_edges`, `evidence_joined_paths` |
| `scripts/pipeline_cli.py` | Modify — register new commands |
| `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json` | Generated artifact |
| `005_Operational-Intelligence-Layer/graph/latest_graph_integrity_report.json` | Generated artifact |
| `scripts/tests/test_graph_contract.py` | Schema validation tests |
| `scripts/tests/test_graph_builder.py` | Walker tests with fixture canonical tree |
| `scripts/tests/test_graph_snapshot.py` | Determinism test |
| `scripts/tests/test_graph_traverse.py` | Traversal tests |

---

## Contract Shapes (frozen in `contract.py`)

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class GraphNode:
    id: str                  # canonical ID (law-*, concept-*, rel-*)
    type: str                # "source" | "concept" | "attribute"
    slug: str                # filename-safe slug
    trust_level: str         # from source trust_level or "derived" for concepts
    last_updated_utc: str    # ISO-8601 UTC


@dataclass(frozen=True)
class GraphEdge:
    from_id: str
    to_id: str
    type: str                # predicate from the closed vocabulary
    evidence_id: str         # rel-* relationship record ID
    status: str              # "verified" | "unverified"


@dataclass
class GraphSnapshot:
    schema_version: str      # "1.0.0"
    generated_at_utc: str
    node_count: int
    edge_count: int
    nodes: list[GraphNode]
    edges: list[GraphEdge]
```

Schema validator rejects any record where:
- `id` does not start with a known prefix (`law-`, `irr-`, `concept-`, `rel-`, `source-`, `handout-`, `reviewer-`, `law-section-`).
- `type` is not in `{"source", "concept", "attribute"}`.
- `trust_level` is not in `{"primary", "secondary", "tertiary", "unverified", "derived"}`.

## Walker Algorithm

```
1. Walk 003_Canonical-Knowledge-Layer/shared/sources/*.md
     → emit GraphNode(type="source") per file, parsed from frontmatter.
2. Walk 003_Canonical-Knowledge-Layer/shared/concepts/*.md
     → emit GraphNode(type="concept") per file.
     → trust_level = "derived"; concepts inherit trust from their regulatory_basis.
3. Walk 003_Canonical-Knowledge-Layer/shared/relationships/*.md
     → for each file with canonical_status in {"promoted", "verified"}:
         emit GraphEdge(
             from_id=record.from_entity,
             to_id=record.to_entity,
             type=record.relationship_type,
             evidence_id=record.id,
             status="verified" if canonical_status == "verified" else "unverified",
         )
4. Sort nodes by id, edges by (from_id, type, to_id, evidence_id).
5. Return GraphSnapshot with deterministic ordering.
```

Sorting is the key to byte-identical determinism.

## Integrity Checks

`integrity.py` runs after the walker and emits a report:

| Check | Definition | Severity |
|---|---|---|
| **Orphan node** | Node with zero incident edges (outgoing + incoming). | Warning |
| **Dangling edge** | Edge whose `from_id` or `to_id` is not in the node set. | Error |
| **Unknown predicate** | Edge `type` not in the closed vocabulary. | Error |
| **Incompatible pair** | `(from_type, to_type)` not allowed for the predicate per the registry. | Error |
| **Stale evidence** | `evidence_id` does not resolve to an existing relationship file. | Error |

Build fails (returns non-zero) if any Error-severity check fires. Warnings are logged but do not abort.

## Traversal API

```python
def neighbors(snapshot: GraphSnapshot, node_id: str, *, direction: str = "out") -> list[GraphNode]: ...
def typed_edges(snapshot: GraphSnapshot, node_id: str, predicate: str) -> list[GraphEdge]: ...
def evidence_joined_paths(
    snapshot: GraphSnapshot,
    from_id: str,
    to_id: str,
    *,
    max_depth: int = 3,
) -> list[list[GraphEdge]]:
    """BFS-style; returns up to N shortest evidence-joined paths."""
```

No graph library. Direct list walks are fine at the expected scale (~1000 nodes, ~5000 edges for the full PD 1096 corpus).

## Snapshot Format

```json
{
  "schema_version": "1.0.0",
  "generated_at_utc": "2026-05-01T00:00:00Z",
  "node_count": 25,
  "edge_count": 60,
  "nodes": [
    {"id": "concept-building-permit", "type": "concept", "slug": "building-permit",
     "trust_level": "derived", "last_updated_utc": "2026-05-01T00:00:00Z"}
  ],
  "edges": [
    {"from_id": "law-national-building-code-of-the-philippines",
     "to_id": "concept-building-permit",
     "type": "governs",
     "evidence_id": "rel-pd-1096-governs-building-permit",
     "status": "verified"}
  ]
}
```

## CLI Commands

| Command | Action |
|---|---|
| `build-graph` | Walk canonical layer, run contract validator + integrity checks, write snapshot. Returns non-zero on Error severity. |
| `build-graph --dry-run` | Walker + integrity checks only; no file writes. |
| `export-graph-snapshot --format json` | Read the latest snapshot, write to stdout. Future format options: `jsonl`, `cytoscape` (deferred). |
| `query-graph --from ID --to ID [--max-depth N]` | Run `evidence_joined_paths` and print the results as a tree. |

## Task Sequence (High-Level)

The actual TDD task breakdown follows the Phase 7 pattern (write test, run fail, implement, run pass, commit). Seven tasks in this order:

1. **`contract.py`** — dataclasses and validator. Tests for each rejection rule.
2. **`builder.py`** — walker over sources and concepts. Fixture canonical tree.
3. **`builder.py`** — walker over relationships with merge handling.
4. **`integrity.py`** — five integrity checks. Test each fire-condition.
5. **`snapshot.py`** — deterministic JSON writer. Byte-identical determinism test.
6. **`traverse.py`** — three traversal functions. Test on a hand-built fixture graph.
7. **`pipeline_cli.py`** — register all three commands. Smoke test.

Deferred to this plan's implementation phase: writing out each step with code. When Phase 8 starts, this plan will be expanded from design-spec to full TDD style matching `phase-7-promotion-governance-plan.md`.

## Gating Metrics

- `orphan_rate` == 0 (no Warning orphans on the PD 1096 core corpus).
- `dangling_edge_count` == 0 (Error-severity; blocks build).
- `determinism_check`: running `build-graph` twice produces byte-identical snapshots.
- `build_latency_ms` < 2000 for ≤1000 nodes (no optimization yet; fine for MVP).

## Non-Goals
- External graph database integration.
- Visualization UI.
- NL-to-graph query translation (Phase 9).
- Graph embeddings.

## Risks
| Risk | Mitigation |
|---|---|
| Sorting not enough for determinism (e.g., dict ordering in JSON writer) | Use `json.dumps(..., sort_keys=True, indent=2)` and assert it in the determinism test. |
| Snapshot grows unwieldy as corpus expands | Acceptable for Phase 8 MVP; split into per-type snapshots in a follow-up if size exceeds ~10 MB. |
| Concepts with no regulatory basis cause "derived" trust ambiguity | Acceptable; orphan warning is the signal to enrich the concept (Phase 3C). |

## Open Design Questions
- Should edges carry `confidence_score` (copied from the relationship record)? Current answer: yes, as an optional field not in the required contract. Add in a follow-up task if Phase 9 needs it.
- Should the graph record `superseded` edges as "historical" or drop them entirely? Current answer: drop from the live graph; they remain in the canonical layer for provenance.

## Self-Review Checklist (pre-expansion)
- Every field in `master-roadmap.md` §3.6 is represented in `GraphNode` / `GraphEdge`.
- Every integrity check maps to a roadmap §9 KPI (`orphan rate`, `contract violation count`).
- The walker produces outputs that satisfy the determinism test.

## Execution Handoff
This plan is in **design-spec** form. Before execution, expand Tasks 1–7 into Phase-7-style TDD with code in every step. Execution itself should be subagent-driven because the contract validator is long.
