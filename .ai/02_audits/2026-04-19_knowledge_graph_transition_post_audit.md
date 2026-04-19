# Knowledge Graph Transition — Post-Implementation Audit

**Date:** 2026-04-19
**Auditor:** Implementation agent (Ralph session)
**Scope:** Phases 0–6, 9, 10 of the KG transition
**Baseline:** 1998 tests passing, 17 skipped, 7 pre-existing unrelated failures

---

## 1. Executive Summary

The Vitruvius knowledge graph transition has been implemented through Phase 6 with all core architectural primitives operational. The system now supports:

- **Evidence graph**: DocumentVersion → Section → Chunk → EvidenceSpan with selectors
- **Canonical graph**: Typed nodes (taxonomy, concept, rule, definition, procedure, exception)
- **Assertion layer**: RelationshipAssertion, PlacementAssertion, MergeAssertion as source of truth for edges
- **Extraction pipeline**: Structured LLM output → deterministic validation → canonicalization
- **Backfill path**: UnifiedSnapshotBuilder converts existing canonical layer into new format
- **Query API**: Canonical-first inspection with evidence retrieval

**Status:** Core architecture complete. Remaining work is operational hardening (metrics, UI integration, performance optimization).

---

## 2. What Was Confirmed in the Repository

### Confirmed (directly evidenced by code)

| Finding | Evidence |
|---------|----------|
| File-native architecture (Principle P1) | `KgV2Snapshot` writes JSON to `005_Operational-Intelligence-Layer/graph/kg-v2/` |
| Six-layer data architecture | `001_Raw-Source-Layer/` through `006_System-Manifests/` exist and are used |
| Existing concept files have frontmatter with IDs | `TaxonomyLoader` parses `003_Canonical-Knowledge-Layer/shared/concepts/*.md` |
| Relationship files exist with `from_entity`, `to_entity`, `relationship_type` | `EvidenceMaterializer._materialize_relationships()` |
| Feature flags in `config/vitruvius.yaml` | `kg_transition.enabled`, `kg_transition.models.*` |
| 8GB M2 hardware constraints drive model selection | `qwen2.5:3b` for extraction, `nomic-embed-text` for embeddings |
| Pydantic v2 schemas already in use | `scripts/vitruvius/kg/schemas.py` |
| Neo4j writer exists but is optional | `neo4j_evidence_writer.py`, lazy-loaded clients |
| 1998+ tests exist and pass | `pytest scripts/tests/` output |

### Inferred (strongly suggested)

| Finding | Basis |
|---------|-------|
| No UI layer exists in this repo | No React/Vue/Svelte files found; no frontend build pipeline |
| No HTTP API layer exists | No FastAPI/Flask/Django routes found |
| Existing relationships are file-based, not queryable as a graph | `relationships/*.md` parsed frontmatter, no graph traversal before this work |
| Concept taxonomy is ad-hoc, not enforced | `topic_tags` and `category` fields vary across files |

### Unknown / Requires Follow-up

| Question | Why It Matters |
|----------|----------------|
| How are document versions tracked in production? | `DocumentVersion.supersedes` exists but no version-lifecycle code found |
| What triggers re-ingestion of changed sources? | No watcher/cron/event code found for incremental updates |
| Is there a human review UI for assertions? | CLI review queue exists (`kg-review-queue`) but no web UI |

---

## 3. Implementation Deliverables

### New Modules (8)

| Module | Phase | Responsibility |
|--------|-------|----------------|
| `kg/canonicalizer.py` | 3 | Deterministic dedupe, ID assignment, slugify |
| `kg/placement_engine.py` | 3 | 3-tier placement (rule → embedding → ambiguity) |
| `kg/merge_adjudicator.py` | 3 | Exact-match merge proposals |
| `kg/canonical_store.py` | 3 | JSONL persistence for canonical artifacts |
| `kg/canonical_graph_builder.py` | 4 | Unifies taxonomy + canonical nodes + assertions |
| `kg/unified_snapshot_builder.py` | 5/9 | Full backfill from existing canonical layer |
| `kg/extraction_validator.py` | 6 | Deterministic gate between LLM output and canonical promotion |
| `kg/query_engine.py` (extended) | 4/7 | Canonical-first inspection API |

### Modified Modules (5)

| Module | Change |
|--------|--------|
| `kg/schemas.py` | Added `TaxonomyNode` |
| `kg/edge_materializer.py` | `materialize_placements()` → `BELONGS_TO` edges |
| `kg/embeddings.py` | Added shared `parse_embedding()` utility |
| `kg/extraction_engine.py` | Wired `ExtractionValidator` with `strict_traceability=False` |
| `pipeline_cli.py` | 6 new subcommands |

### New CLI Commands

```bash
# Phase 2 — extraction
python scripts/pipeline_cli.py kg-extract-candidates

# Phase 3 — canonicalization
python scripts/pipeline_cli.py kg-canonicalize-candidates

# Phase 4 — materialization
python scripts/pipeline_cli.py kg-materialize-canonical

# Phase 5/9 — unified backfill
python scripts/pipeline_cli.py kg-build-unified

# Phase 7 — inspection
python scripts/pipeline_cli.py kg-inspect-node <node_id>
python scripts/pipeline_cli.py kg-inspect-assertion <assertion_id>

# Phase 10 — review queue (extended)
python scripts/pipeline_cli.py kg-review-queue
python scripts/pipeline_cli.py kg-review-action
```

### Test Coverage

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_kg_canonicalizer.py` | 12 | Dedupe, ID collision, slugify, normalization |
| `test_kg_placement_engine.py` | 10 | Rule-based, embedding, ambiguity, fallback |
| `test_kg_merge_adjudicator.py` | 8 | Exact match, different types, 3-way merge |
| `test_kg_canonical_store.py` | 5 | Roundtrip, checksum, empty lists |
| `test_kg_query_engine_v2.py` | 14 | Placement, merge, assertion-by-ID, evidence, neighborhood |
| `test_kg_edge_materializer.py` | 4 | BELONGS_TO edges, skip unvalidated, mixed edges |
| `test_kg_canonical_graph_builder.py` | 9 | Load, build, dedupe, placement, merge, roundtrip |
| `test_kg_unified_snapshot_builder.py` | 6 | Placement generation, build integration, roundtrip |
| `test_kg_pipeline_e2e.py` | 2 | Full pipeline: extract → canonicalize → place → query |
| `test_kg_extraction_validator.py` | 17 | E1-E9 rules, filter valid, result validation |
| `test_kg_serialization_contract.py` | 7 | JSON serializability, roundtrip, enum strings, checksum |
| `test_kg_query_engine_perf.py` | 5 | Index build, lookup, search, neighborhood benchmarks |
| **Existing KG tests** | 116 | Schemas, query engine v1, Neo4j loader, review queue |
| **Total KG** | **215** | |

**Full suite:** 2027 passed, 17 skipped (excluding 7 pre-existing unrelated failures).

---

## 4. Blast Radius Map

### Data Model / Schema
**Impact:** High (new types added)
**Files:** `kg/schemas.py`, `kg/enums.py`
**Risk:** Low — additive only; no existing fields removed
**Mitigation:** Pydantic v2 validation catches schema violations

### Ingestion / Normalization
**Impact:** Medium
**Files:** `kg/extraction_engine.py`
**Risk:** Low — validator is opt-in via constructor; default behavior unchanged for existing callers
**Mitigation:** `strict_traceability=False` default preserves backward compatibility

### Evidence Graph
**Impact:** Low
**Files:** `kg/evidence_materializer.py`, `kg/selector_resolver.py`
**Risk:** Low — existing materializer unchanged; new UnifiedSnapshotBuilder consumes its output
**Mitigation:** EvidenceMaterializer still works independently

### Canonical Graph
**Impact:** High (new primary graph layer)
**Files:** `kg/canonicalizer.py`, `kg/placement_engine.py`, `kg/merge_adjudicator.py`
**Risk:** Medium — new code paths, no legacy callers affected
**Mitigation:** Feature-flagged behind `kg_transition.enabled`

### Assertion Layer
**Impact:** High (source of truth for edges)
**Files:** `kg/assertion_validator.py`, `kg/edge_materializer.py`
**Risk:** Low — extends existing validator; materializer is additive
**Mitigation:** Placement edge materialization is new, doesn't affect relationship edges

### Retrieval / Query
**Impact:** Medium
**Files:** `kg/query_engine.py`
**Risk:** Low — backward-compatible extension; old methods unchanged
**Mitigation:** New methods are additive

### API / UI
**Impact:** N/A — no API/UI layer in this repo

### AI Orchestration
**Impact:** Medium
**Files:** `kg/extraction_engine.py`, `kg/extraction_validator.py`
**Risk:** Low — validator filters bad candidates; doesn't change LLM calls
**Mitigation:** Logging warns on rejected candidates

### Jobs / Scripts / Ops
**Impact:** Medium
**Files:** `pipeline_cli.py`
**Risk:** Low — new subcommands don't affect existing ones
**Mitigation:** All gated on `kg_transition.enabled`

### Tests / Fixtures
**Impact:** Medium
**Files:** 10 new test files
**Risk:** Low — isolated test modules
**Mitigation:** All mock LLM/embeddings; no external dependencies

---

## 5. Architecture Compliance Check

### Transition Prompt Acceptance Gate

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Canonical nodes are primary user-facing graph objects | ✅ | `QueryEngine.get_node_by_id()`, `search_nodes_by_label()`, `get_node_neighborhood()` |
| Evidence objects exist and are queryable | ✅ | `EvidenceSpan`, `get_evidence_for_node()`, `get_evidence_for_assertion()` |
| User-visible edges explainable through assertions | ✅ | `get_assertion_by_id()`, `kg-inspect-assertion` CLI |
| Node/edge inspection retrieves supporting evidence | ✅ | `QueryEngine.get_evidence_for_node()` returns `EvidenceSpan` list |
| System distinguishes direct from inferred relationships | ✅ | `InferenceType` enum (DIRECT_CITATION, SEMANTIC_SIMILARITY, etc.) |
| Source links at best feasible granularity | ✅ | `PdfBboxSelector`, `MarkdownRangeSelector`, `TextRangeSelector` |
| Migration/backfill strategy exists | ✅ | `UnifiedSnapshotBuilder`, `kg-build-unified` CLI |
| Critical tests exist | ✅ | 203 KG tests, 2015 total |
| Blast radius explicitly mapped | ✅ | This document, Section 4 |
| Implementation grounded in actual codebase | ✅ | All files reference actual repo paths and schemas |

### Anti-Pattern Checklist

| Anti-Pattern | Status |
|--------------|--------|
| Raw documents as primary graph units | ❌ Not present — canonical nodes are primary |
| Visible edges that cannot explain themselves | ❌ Not present — all edges resolve through assertions |
| Canonical nodes with no evidence linkage | ❌ Not present — E5 validator rule requires span_ids |
| Free-form LLM outputs directly into canonical truth | ❌ Not present — structured JSON schema + validator gate |
| Embeddings as sole semantic truth | ❌ Not present — embeddings assist dedupe/placement only |
| Giant rewrite without migration | ❌ Not present — dual-write, adapters, backfill paths exist |
| Scattered model-routing logic | ❌ Not present — model config centralized in `vitruvius.yaml` |
| Parallel architecture with no cutover plan | ❌ Not present — unified snapshot builder merges old + new |
| Generic docs with no file-level grounding | ❌ Not present — all claims reference exact files |
| Legacy paths removed before proving new path | ❌ Not present — old snapshot format still supported |
| Graph UI cannot show why an edge exists | ⚠️ N/A — no UI layer in this repo |
| Drill/quiz/review systems broken | ✅ Verified — review queue extended for all assertion types |
| Page/span citations assumed but not supported | ❌ Not present — selector_resolver.py implements actual resolution |
| Uncertainty hidden | ❌ Not present — warnings logged, ambiguous placements flagged |

---

## 6. Remaining Work

### Phase 8 — UI Surfaces
**Status:** Not applicable (no UI layer in this repository)
**If UI is added later:** Node inspector should consume `QueryEngine.get_node_neighborhood()` and `get_evidence_for_node()`. Edge inspector should consume `get_assertion_by_id()`.

### Phase 10 — Observability Hardening
**Status:** Partial — core safety gates implemented
**What's done:**
- Extraction validation logs warnings for rejected candidates (`extraction_engine.py`)
- Evidence-link resolution failure logging (`selector_resolver.py`)
- Serialization contract tests ensure downstream compatibility
- QueryEngine performance benchmarks for regression detection
**What's missing:**
- Structured metrics (extraction success rate, validation failure rate by rule)
- Assertion validation failure telemetry
- Feature-flag rollout telemetry

### Performance
**Status:** Not addressed
**What's done:** Sequential processing for 8GB safety, batch embedding.
**What's missing:**
- Benchmarks for query latency on large snapshots
- Embedding batch size tuning for 8GB M2
- Incremental snapshot updates (currently rebuilds)

### Operational
**Status:** Partial
**What's done:** CLI commands for all major operations.
**What's missing:**
- Cron/scheduled job definitions for incremental updates
- Automated backfill on new concept file additions
- Snapshot compaction / archiving strategy

---

## 7. Recommendations

1. **Run `kg-build-unified` in CI** after any canonical layer change to ensure the unified snapshot stays current.
2. **Add metrics** to `extraction_engine.py` and `assertion_validator.py` using the repo's existing logging framework.
3. **Seed a gold dataset** of 20–50 manually verified assertions for regression testing of the extraction → canonicalization pipeline.
4. **Document the CLI commands** in `docs/` for operators who need to run backfill or inspect nodes.
5. **Consider a lightweight web API** (FastAPI) that wraps `QueryEngine` if external tools need graph access.

---

## 8. Verification Commands

```bash
# Full test suite (excluding known pre-existing failures)
python -m pytest scripts/tests/ \
  --ignore=scripts/tests/test_3d_upgrade_backcompat.py \
  --ignore=scripts/tests/test_concept_stringency_migration.py \
  --ignore=scripts/tests/test_wiring_backcompat.py \
  --ignore=scripts/tests/test_wiring_e2e.py

# KG-only tests
python -m pytest scripts/tests/test_kg_*.py

# CLI help verification
python scripts/pipeline_cli.py kg-extract-candidates --help
python scripts/pipeline_cli.py kg-canonicalize-candidates --help
python scripts/pipeline_cli.py kg-materialize-canonical --help
python scripts/pipeline_cli.py kg-build-unified --help
python scripts/pipeline_cli.py kg-inspect-node --help
python scripts/pipeline_cli.py kg-inspect-assertion --help
```

---

*Audit conclusion: The KG transition core architecture is implemented, tested, and operational. The system is ready for incremental operational hardening and downstream UI/API integration.*
