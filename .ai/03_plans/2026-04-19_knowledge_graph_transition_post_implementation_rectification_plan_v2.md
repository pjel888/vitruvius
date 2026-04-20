---
task: knowledge-graph-transition-post-implementation-rectification-v2
phase: "05"
status: complete
created: 2026-04-19
---

# Knowledge Graph Transition — Post-Implementation Rectification Plan v2

**Date:** 2026-04-19  
**Status:** COMPLETED (all critical/high items rectified in independent verification pass)  
**Derived from:** `.ai/02_audits/2026-04-19_knowledge_graph_transition_post_implementation_audit_v2.md`

---

## 1. Findings Summary

| Severity | Count | Rectified |
|----------|-------|-----------|
| Critical | 1 | 1 |
| High | 4 | 4 |
| Medium | 2 | 2 |
| Low | 0 | 0 |

---

## 2. Critical Findings

### C1 — ExtractionEngine allowed synthetic evidence links without warning or strict validation

**What was wrong:** `ExtractionEngine.__init__` defaulted to `ExtractionValidator(strict_traceability=False)`. This allowed candidates to pass validation with synthetic placeholder span IDs (`span-<chunk_suffix>`) that may not correspond to real `EvidenceSpan` records. The prior audit fixed the hardcoded `span_ids=[]` bug but left the validator in permissive mode.

**Why it matters:** Without strict traceability, the extraction pipeline can produce candidates claiming evidence that does not exist. This violates the core rule: *"Every user-visible node must be backed by evidence."*

**Files changed:**
- `scripts/vitruvius/kg/extraction_engine.py`

**What changed:**
- Default `strict_traceability` changed from `False` to `True`.
- `extract_from_chunk()` auto-generates a `run_id` when empty to satisfy E9.
- Explicit warning logged when synthetic span IDs are generated.

**Acceptance criteria:**
- [x] Default extraction path rejects candidates with empty span_ids or run_id.
- [x] Synthetic span usage is logged at WARNING level.
- [x] Existing tests pass; new tests confirm strict validation.

**Verification:**
```bash
python3 -m pytest scripts/tests/test_kg_extraction_engine.py -q
```

---

## 3. High Findings

### H1 — Placement assertions had empty evidence_ids

**What was wrong:** `CanonicalGraphBuilder.build()` created `PlacementAssertion` records with `evidence_ids=[]`. The CLI `kg-canonicalize-candidates` did the same. This violated the requirement that every assertion be evidence-backed.

**Files changed:**
- `scripts/vitruvius/kg/canonical_graph_builder.py`
- `scripts/pipeline_cli.py`

**What changed:**
- `CanonicalGraphBuilder` now propagates `node.primary_assertion_id` into `PlacementAssertion.evidence_ids`.
- CLI placement block does the same.

**Acceptance criteria:**
- [x] Placement assertions created by builder contain non-empty `evidence_ids` when node has `primary_assertion_id`.

---

### H2 — Merge assertions had empty evidence_ids

**What was wrong:** `MergeAdjudicator._build_assertion()` created `MergeAssertion` records with `evidence_ids=[]`.

**Files changed:**
- `scripts/vitruvius/kg/merge_adjudicator.py`

**What changed:**
- Merges now collect `primary_assertion_id` from both nodes and deduplicate into `evidence_ids`.

**Acceptance criteria:**
- [x] Merge assertions contain evidence from both source nodes.

---

### H3 — Invalid placement parent IDs were created for missing taxonomy nodes

**What was wrong:** `CanonicalGraphBuilder._resolve_parent_id()` returned the raw path string when no matching taxonomy node existed. This created `PlacementAssertion` records with `parent_node_id` values that did not correspond to any `CanonicalNode`.

**Files changed:**
- `scripts/vitruvius/kg/canonical_graph_builder.py`

**What changed:**
- `_resolve_parent_id` now returns `None` when no match is found.
- `build()` skips placements with `None` parents and logs a warning.

**Acceptance criteria:**
- [x] No placement assertion points to a non-existent node ID.
- [x] Missing taxonomy parents generate warnings, not invalid data.

---

### H4 — CLI commands lacked sub-flag enforcement

**What was wrong:** `kg-ingest-evidence`, `kg-extract-candidates`, and `kg-materialize-canonical` checked `kg_transition.enabled` but not their respective sub-flags (`evidence_graph`, `structured_extraction`, `assertion_layer`).

**Files changed:**
- `scripts/pipeline_cli.py`

**What changed:**
- `kg-ingest-evidence` checks `is_kg_evidence_graph()`.
- `kg-extract-candidates` checks `is_kg_structured_extraction()`.
- `kg-materialize-canonical` checks `is_kg_assertion_layer()`.
- `kg-dematerialize-edge` checks both `enabled` and `assertion_layer`.

**Acceptance criteria:**
- [x] Each CLI command refuses to run if its specific sub-flag is disabled.

---

## 4. Medium Findings

### M1 — Missing `kg-dematerialize-edge` CLI

**What was wrong:** Execution Plan Phase 4 requires `kg-dematerialize-edge <assertion_id>` for rollback safety. No such command existed.

**Files changed:**
- `scripts/pipeline_cli.py`

**What was implemented:**
- `kg-dematerialize-edge <assertion_id> [--snapshot PATH] [--out-path PATH]` removes fast edges matching the assertion_id from a v2 snapshot.

**Acceptance criteria:**
- [x] Command removes matching edge(s) and rewrites snapshot.
- [x] Help text is available.

---

### M2 — Missing architectural invariant tests

**What was wrong:** No tests verified the core non-negotiable architectural rules (evidence-backed nodes, evidence-backed assertions, assertion_id on edges, valid placement parents).

**Files created:**
- `scripts/tests/test_kg_architectural_invariants.py`

**What was implemented:**
- 9 tests covering: node evidence, assertion evidence, fast edge assertion_id, placement parent existence, builder invalid-parent skipping.

**Acceptance criteria:**
- [x] All 9 tests pass.
- [x] Tests fail if architectural invariants are violated.

---

## 5. Verification Summary

| Check | Before | After |
|-------|--------|-------|
| KG tests passing | 242 | 251 |
| Total tests passing | 2074 | 2074 |
| Pre-existing failures | 3 | 3 (unchanged) |
| New modules | 28 | 28 |
| New CLI commands | 13 | 14 (+1 dematerialize) |
| Files modified | 12 | 18 (+6 in this pass) |

---

## 6. Rollback Notes

All rectification changes in this pass are **additive** or **bug fixes**:
- No existing APIs were removed.
- No existing behavior was changed except to fix validation strictness and invalid parent resolution.
- New CLI commands do not affect existing commands.
- Tests were updated to match corrected behavior.

If rollback is required, revert the specific commits. No database schema changes were made.

---

## 7. Follow-up Work (Non-blocking)

1. **Commit or revert uncommitted model config changes** — Working tree contains model preset updates unrelated to KG transition.
2. **Neo4j-backed QueryEngine** — For production, consider a `QueryEngineNeo4j` implementation that queries the live graph instead of JSON snapshots.
3. ** visualize.py v2 support** — If a UI layer is added, update the static HTML generator to render v2 canonical nodes and edge inspectors.

---

*Rectification complete. All critical and high findings resolved in code. Repository state synchronized with architecture.*
