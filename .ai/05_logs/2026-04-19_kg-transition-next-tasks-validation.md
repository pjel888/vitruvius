# KG Transition — Next Tasks Validation Report

**Date:** 2026-04-19  
**Commit baseline:** cbb642b ("KG transition: AssertionValidator + EdgeMaterializer")  
**New commit:** TBD  
**Branch:** main

---

## Summary

All four prioritized next tasks from the KG transition handoff have been implemented and validated:

1. ✅ **Task 1 — Wire EdgeMaterializer into EvidenceMaterializer**
2. ✅ **Task 4 — Query Engine v2**
3. ✅ **Task 5 — Neo4j loader**
4. ✅ **Gate 6 — Review queue CLI**

---

## Task 1 — EdgeMaterializer Integration

### Changes
- `scripts/vitruvius/kg/json_evidence_store.py`
  - Added `fast_edges: list[dict]` to `KgV2Snapshot`
  - Updated `to_dict()`, `read()`, `entity_counts()`
- `scripts/vitruvius/kg/assertion_validator.py`
  - Implemented **R2**: `edge_type` must be a registered `EdgeType` enum member
- `scripts/vitruvius/kg/evidence_materializer.py`
  - Added `_materialize_fast_edges()` method
  - Builds `canonical_index` from snapshot + concept files on disk
  - Runs `AssertionValidator` on each `RelationshipAssertion`
  - Feeds validated assertions to `EdgeMaterializer`
  - Stores produced edges in `snapshot.fast_edges`
- `scripts/tests/test_edge_materializer.py` (new)
  - 10 tests: happy path, skip unvalidated, include unvalidated, write snapshot, multiple assertions, integration with `EvidenceMaterializer`, snapshot roundtrip, R2 validation

### Validation
- `python3 -m pytest scripts/tests/test_edge_materializer.py -v` → **10 passed**

---

## Task 4 — Query Engine v2

### Changes
- `scripts/vitruvius/kg/query_engine.py` (new)
  - `QueryEngine` class loads `KgV2Snapshot` from JSON path
  - Builds in-memory indexes on load:
    - `node_by_id`
    - `assertions_by_node` (bidirectional)
    - `edges_by_node` (bidirectional)
    - `node_label_index` (lowercase label → node ids)
  - Methods:
    - `get_node_by_id(node_id) -> CanonicalNode | None`
    - `get_assertions_for_node(node_id) -> list[RelationshipAssertion]`
    - `get_edges_for_node(node_id) -> list[dict]`
    - `search_nodes_by_label(query, limit=10) -> list[CanonicalNode]`
  - File-native; no DB required
- `scripts/tests/test_kg_query_engine.py` (new)
  - 12 tests: node lookup, unknown node, bidirectional assertions, bidirectional edges, exact label search, case-insensitive search, substring search, limit respect, empty results, snapshot roundtrip

### Validation
- `python3 -m pytest scripts/tests/test_kg_query_engine.py -v` → **12 passed**

---

## Task 5 — Neo4j Loader

### Changes
- `scripts/vitruvius/kg/neo4j_loader.py` (new)
  - `Neo4jLoader` class takes `KgV2Snapshot` + optional `edge_snapshot_path`
  - `to_cypher()` generates idempotent `MERGE` statements for:
    - `CanonicalNode`
    - `DocumentVersion`
    - `Section`
    - `Chunk`
    - `EvidenceSpan`
    - `Assertion`
    - `FAST_EDGE` relationships (typed by `edge_type`)
  - `write_cypher(out_path)` dumps to `.cypher` file
  - `load(client)` executes against Neo4j when `is_kg_neo4j_backend()` is true and client provided
  - Safe Cypher string escaping for literals and property maps
- `scripts/tests/test_kg_neo4j_loader.py` (new)
  - 19 tests: escaping, property map generation, all entity merge statements, fast edge generation, external edge snapshot reading, file write, load with flag off, load with mock client

### Validation
- `python3 -m pytest scripts/tests/test_kg_neo4j_loader.py -v` → **19 passed**

---

## Gate 6 — Review Queue CLI

### Changes
- `scripts/pipeline_cli.py`
  - Added `kg-review-queue` subcommand
    - `--status` filter (default `REVIEW_REQUIRED`)
    - `--snapshot` override (defaults to latest in `005_Operational-Intelligence-Layer/graph/kg-v2/`)
    - Prints formatted table of assertions
  - Added `kg-review-action` subcommand
    - `assertion_id` positional argument
    - `--action {approve,reject,escalate}` (required)
    - `--reason` optional
    - `--snapshot` override
    - Mutates assertion state and rewrites snapshot atomically
- `scripts/tests/test_kg_review_queue.py` (new)
  - 7 tests: list filtering, validated filtering, empty results, approve mutation, reject mutation, escalate mutation, no-match handling

### Validation
- `python3 -m pytest scripts/tests/test_kg_review_queue.py -v` → **7 passed**
- `python3 -m py_compile scripts/pipeline_cli.py` → syntax clean

---

## Test Totals

| Suite | Tests | Status |
|-------|-------|--------|
| test_kg_assertion_validator.py | 16 | ✅ passed |
| test_kg_schemas.py | 26 | ✅ passed |
| test_evidence_materializer.py | 20 | ✅ passed |
| test_section_extractor.py | 8 | ✅ passed |
| test_edge_materializer.py | 10 | ✅ passed |
| test_kg_query_engine.py | 12 | ✅ passed |
| test_kg_neo4j_loader.py | 19 | ✅ passed |
| test_kg_review_queue.py | 7 | ✅ passed |
| **Total** | **118** | ✅ **passed** |

**Target was ≥86.** Result: **118 passed** (+48 over target).

### Legacy baseline verification
- `python3 -m pytest scripts/tests/test_kg_assertion_validator.py scripts/tests/test_kg_schemas.py scripts/tests/test_evidence_materializer.py scripts/tests/test_section_extractor.py -v` → **70 passed** (unchanged from baseline)

---

## Risks and Caveats

1. **Snapshot path discovery** — `kg-review-queue` and `kg-review-action` default to the newest `*_kg_v2_snapshot.json` in `005_Operational-Intelligence-Layer/graph/kg-v2/`. If the directory is empty, they emit a clear error and exit with code 1.
2. **Neo4j dependency** — The loader uses lazy import; tests mock the client. No new pip dependencies were added.
3. **R2 edge_type validation** — Now enforced in `AssertionValidator`. Existing tests using valid `EdgeType` values pass; invalid values correctly fail.
4. **fast_edges backward compatibility** — `KgV2Snapshot.read()` defaults `fast_edges` to `[]` when the field is absent in older snapshots.

---

## State Update

- Milestone tracker: No change required (KG transition is not tracked in the main phase roadmap; it is a cross-cutting architecture initiative).
- Current phase: Unchanged (ready-family aggregate residual hardening remains the active sprint).
- No governing plans were modified; this work is a continuation of the accepted KG transition handoff.
