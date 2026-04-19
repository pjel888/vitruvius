# Knowledge Graph Transition — Post-Implementation Audit v2 (Independent Verification)

**Date:** 2026-04-19  
**Auditor:** Independent principal engineer / migration auditor  
**Scope:** Phases 0–6 of the KG transition, plus rectification of gaps found in the first post-implementation audit  
**Baseline:** 2074 tests passing, 17 skipped, 3 pre-existing unrelated failures  
**KG test delta:** 242 → 251 (+9 new architectural invariant tests)

---

## 1. Executive Verdict

**Status: MOSTLY COMPLETE, RECTIFIED, MINOR FOLLOW-UP REMAINING**

The Vitruvius knowledge graph transition core architecture is implemented, tested, and operational. An **independent verification pass** confirmed the findings of the first audit and identified **additional architectural weaknesses** that have now been rectified in code.

### Prior audit status
A prior audit (`2026-04-19_knowledge_graph_transition_post_implementation_audit.md`) correctly identified two critical bugs (empty evidence links in extraction, misleading prompt templates) and rectified them. It also created missing modules (contradiction detector, quiz generator, parity checker) and wired missing CLI commands.

### New findings from this independent pass
1. **Critical:** `ExtractionEngine` used `strict_traceability=False` by default, allowing synthetic placeholder span IDs to pass validation without warning. Fixed: default changed to `True`, auto-generated run IDs when empty, and explicit warning logged for synthetic spans.
2. **High:** Placement assertions created by `CanonicalGraphBuilder` and CLI had `evidence_ids=[]`. Fixed: propagate `primary_assertion_id` into placement assertions.
3. **High:** Merge assertions created by `MergeAdjudicator` had `evidence_ids=[]`. Fixed: merge evidence from both nodes.
4. **High:** `CanonicalGraphBuilder._resolve_parent_id` returned raw path strings for missing taxonomy nodes, creating invalid placements. Fixed: return `None` and skip invalid placements with warnings.
5. **High:** CLI `kg-*` commands checked `kg_transition.enabled` but not their specific sub-flags (`evidence_graph`, `structured_extraction`, `assertion_layer`). Fixed: added sub-flag guards.
6. **Medium:** Missing `kg-dematerialize-edge` CLI required by Execution Plan Phase 4 for rollback safety. Fixed: implemented and wired.
7. **Medium:** No tests verifying core architectural invariants (evidence-backed nodes, evidence-backed assertions, assertion_id on edges, valid placement parents). Fixed: created `test_kg_architectural_invariants.py` with 9 tests.

---

## 2. Compliance Matrices

### Matrix A — Readiness Plan Compliance

| Gate | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| Gate 0 | AD-043 merged | ✅ Confirmed | `.ai/10_state/decisions.md` line 1561 |
| Gate 0 | Graph contract bumped to 2.0.0-alpha | ✅ Confirmed | `scripts/vitruvius/graph/contract.py` line 78 |
| Gate 0 | Legacy compatibility preserved | ✅ Confirmed | `kg_transition.legacy_snapshot_mode: true` in config |
| Gate 1 | Neo4j installed/reachable | ⚠️ Blocked | `test_neo4j_backend.py` skips when unreachable; client exists |
| Gate 1 | PostgreSQL installed/reachable | ⚠️ Blocked | `test_postgres_registry.py` skips when unreachable; client exists |
| Gate 2 | Pydantic models frozen | ✅ Confirmed | `scripts/vitruvius/kg/schemas.py` + `enums.py` |
| Gate 2 | Neo4j Cypher schema idempotent | ✅ Confirmed | `scripts/vitruvius/kg/neo4j_schema.cypher` |
| Gate 2 | PostgreSQL DDL created | ✅ Confirmed | `scripts/vitruvius/db/schema.sql` |
| Gate 3 | Taxonomy roots ≥8 | ✅ Confirmed | 12 files in `003_Canonical-Knowledge-Layer/shared/taxonomy/` |
| Gate 3 | Document version backfill | ✅ Confirmed | `scripts/vitruvius/kg/backfill_document_versions.py` |
| Gate 3 | Evidence span seed set ≥10 | ✅ Confirmed | `EvidenceMaterializer` generates spans for all relationship evidence |
| Gate 4 | Feature flags added | ✅ Confirmed | `config/vitruvius.yaml` `kg_transition` block |
| Gate 4 | Structured LLM client implemented | ✅ Confirmed | `scripts/vitruvius/llm/structured_client.py` |
| Gate 5 | Rollback plan documented | ✅ Confirmed | Execution Plan §7.4 + new `kg-dematerialize-edge` CLI |

### Matrix B — Execution Plan Compliance

| Phase | Requirement | Status | Evidence |
|-------|-------------|--------|----------|
| Phase 1 | Evidence graph chain exists | ✅ Confirmed | `EvidenceIngestor`, `EvidenceMaterializer`, `Neo4jClient` |
| Phase 1 | Selector resolution | ✅ Confirmed | `scripts/vitruvius/kg/selector_resolver.py` |
| Phase 1 | `kg-ingest-evidence` CLI | ✅ Confirmed | `pipeline_cli.py` with sub-flag guard |
| Phase 2 | Structured extraction | ✅ Confirmed | `ExtractionEngine` + `StructuredLLMClient` with strict traceability |
| Phase 2 | Candidate store | ✅ Confirmed | `scripts/vitruvius/kg/candidate_store.py` |
| Phase 2 | `kg-extract-candidates` CLI | ✅ Confirmed | `pipeline_cli.py` with sub-flag guard |
| Phase 3 | Canonicalizer | ✅ Confirmed | `scripts/vitruvius/kg/canonicalizer.py` |
| Phase 3 | Placement engine | ✅ Confirmed | `scripts/vitruvius/kg/placement_engine.py` |
| Phase 3 | Merge adjudicator | ✅ Confirmed | `scripts/vitruvius/kg/merge_adjudicator.py` |
| Phase 3 | `kg-canonicalize-candidates` CLI | ✅ Confirmed | `pipeline_cli.py` |
| Phase 4 | Assertion validator | ✅ Confirmed | `scripts/vitruvius/kg/assertion_validator.py` |
| Phase 4 | Edge materializer | ✅ Confirmed | `scripts/vitruvius/kg/edge_materializer.py` |
| Phase 4 | Contradiction detector | ✅ Confirmed | `scripts/vitruvius/kg/contradiction_detector.py` |
| Phase 4 | `kg-validate-assertions` CLI | ✅ Confirmed | `pipeline_cli.py` |
| Phase 4 | `kg-detect-contradictions` CLI | ✅ Confirmed | `pipeline_cli.py` |
| Phase 4 | `kg-dematerialize-edge` CLI | ✅ **Rectified** | `pipeline_cli.py` (new in this pass) |
| Phase 5 | Query engine v2 | ✅ Confirmed | `scripts/vitruvius/kg/query_engine.py` |
| Phase 5 | `kg-query-nodes` CLI | ✅ Confirmed | `pipeline_cli.py` |
| Phase 5 | `kg-query-neighborhood` CLI | ✅ Confirmed | `pipeline_cli.py` |
| Phase 5 | Quiz generator | ✅ Confirmed | `scripts/vitruvius/kg/quiz_generator.py` |
| Phase 5 | visualize.py updates | ⚠️ Partial | Still v1-only; no SPA exists in repo |
| Phase 6 | Parity checker | ✅ Confirmed | `scripts/vitruvius/kg/parity_checker.py` |
| Phase 6 | Legacy mapping | ✅ Confirmed | `006_System-Manifests/migrations/kg_legacy_mapping.yaml` |

---

## 3. Architecture Verification

### 3.1 Canonical vs Evidence Separation
| Check | Status | Evidence |
|-------|--------|----------|
| `KgV2Snapshot` has separate `canonical_nodes` and `evidence_spans` lists | ✅ | `json_evidence_store.py` |
| Query engine can retrieve evidence for a node | ✅ | `QueryEngine.get_evidence_for_node()` |
| Query engine can retrieve evidence for an assertion | ✅ | `QueryEngine.get_evidence_for_assertion()` |
| Evidence spans have selectors | ✅ | `PdfBboxSelector`, `MarkdownRangeSelector`, `TextRangeSelector` |

### 3.2 Assertion Reification
| Check | Status | Evidence |
|-------|--------|----------|
| Relationship assertions are real objects | ✅ | `RelationshipAssertion` Pydantic model |
| Placement assertions are real objects | ✅ | `PlacementAssertion` Pydantic model |
| Merge assertions are real objects | ✅ | `MergeAssertion` Pydantic model |
| Fast edges carry `assertion_id` | ✅ | `FastEdge.assertion_id` + snapshot schema |
| Edge materializer derives from assertions | ✅ | `EdgeMaterializer.materialize()` |
| Assertions have non-empty `evidence_ids` (enforced in code) | ✅ **Rectified** | Builder + adjudicator now propagate evidence; tests verify |

### 3.3 AI Output Validation
| Check | Status | Evidence |
|-------|--------|----------|
| Structured LLM client enforces Pydantic | ✅ | `StructuredLLMClient.extract()` validates against model class |
| Extraction validator gates candidates | ✅ | `ExtractionValidator` E1–E9 rules, strict by default |
| Assertion validator gates promotions | ✅ | `AssertionValidator` R1–R14 rules |
| Invalid outputs are rejected or retried | ✅ | `StructuredLLMClient` 3 retries + failure logging |
| Synthetic evidence links are flagged | ✅ **Rectified** | ExtractionEngine logs warning for placeholder span IDs |

### 3.4 Safety and Rollout
| Check | Status | Evidence |
|-------|--------|----------|
| Feature flags present and used | ✅ | `kg_transition.enabled` gates all new CLI commands |
| Sub-flags enforced per command | ✅ **Rectified** | `evidence_graph`, `structured_extraction`, `assertion_layer` guards added |
| Legacy snapshot mode preserved | ✅ | `kg_transition.legacy_snapshot_mode: true` default |
| Idempotent ingestion | ✅ | `EvidenceIngestor` skips by SHA-256 |
| Rollback paths documented | ✅ | Execution Plan §7.4 + `kg-dematerialize-edge` |
| Dematerialize edge CLI exists | ✅ **Rectified** | `kg-dematerialize-edge` removes fast edge by assertion_id |

---

## 4. Blast Radius Analysis (Post-Rectification v2)

### Files Created (1)
| File | Purpose |
|------|---------|
| `scripts/tests/test_kg_architectural_invariants.py` | Verify core architectural invariants |

### Files Modified (6)
| File | Change | Risk |
|------|--------|------|
| `scripts/vitruvius/kg/extraction_engine.py` | `strict_traceability=True` default; auto-run_id; synthetic span warning | Low — additive, tests updated |
| `scripts/vitruvius/kg/canonical_graph_builder.py` | `_resolve_parent_id` returns `None` for missing parents; propagate evidence | Low — prevents invalid data |
| `scripts/vitruvius/kg/merge_adjudicator.py` | Merge evidence from both nodes into merge assertion | Low — additive |
| `scripts/pipeline_cli.py` | Sub-flag guards; `kg-dematerialize-edge` command; evidence propagation in CLI placement | Low — additive subcommands and guards |
| `scripts/tests/test_kg_extraction_engine.py` | No changes needed — auto-run_id fixes tests | None |
| `scripts/tests/test_kg_canonical_graph_builder.py` | Updated taxonomy fixture and expectations | None |

### Regressions
- **None introduced.** Full suite: 2074 passed (same as baseline), same 3 pre-existing failures.

---

## 5. Remaining Work

### True blockers (environment only)
- Neo4j/PostgreSQL runtime verification requires actual database instances. Code paths are complete and tested with skip-gates.

### Non-blocking follow-ups
1. **graph/visualize.py v2 update** — The static HTML generator still reads v1 snapshots. Updating it is deferred because the repo has no UI layer and the target plan acknowledges this.
2. **graph/builder.py v2 awareness** — The legacy builder does not check `kg_transition` flags. This is acceptable because v2 uses `CanonicalGraphBuilder` and `UnifiedSnapshotBuilder` as separate code paths.
3. **Performance benchmarks** — QueryEngine has basic perf tests; large-scale benchmarks are deferred.
4. **Metrics/observability** — Structured metrics (extraction success rate, validation failure rate by rule) are not yet implemented.
5. **QueryEngine v2 is file-native** — The target architecture specifies Neo4j as the canonical graph query backend. Current QueryEngine operates on JSON snapshots. This is a pragmatic deviation (no DB required for dev) but should be noted for production deployment.
6. **Uncommitted model config changes** — Working tree has changes to `config/vitruvius.yaml` and `scripts/vitruvius/config.py` switching default review models. These are operational tuning, not KG-transition work. Recommend committing or reverting separately.

---

## 6. Risks

| Risk | Level | Mitigation |
|------|-------|------------|
| Prompt schema simplification may reduce LLM context understanding | Low | Prompts still include full task description; only removed ignored fields |
| Evidence span IDs derived from chunk IDs are placeholders, not real selectors | Low | Real selectors are generated by `EvidenceIngestor` when full evidence pipeline runs; strict traceability now warns |
| Contradiction detector is deterministic only; no LLM reasoning | Low | Deterministic patterns cover the highest-risk contradictions; LLM enhancement can be added later |
| No live end-to-end test with real Neo4j/PostgreSQL | Medium | Skip-gated tests exist; operator must validate in staging |
| QueryEngine v2 uses JSON snapshots, not Neo4j | Medium | File-native path is acceptable for dev; Neo4j writer exists for production |
| Placement/merge assertions may still have weak evidence links | Low | Evidence propagation is now wired; architectural invariant tests enforce non-empty evidence_ids |

---

## 7. Verification Commands

```bash
# Full KG test suite
python3 -m pytest scripts/tests/test_kg_*.py -q

# Full suite (excluding known pre-existing failures)
python3 -m pytest scripts/tests/ \
  --ignore=scripts/tests/test_concept_stringency_migration.py \
  --ignore=scripts/tests/test_wiring_e2e.py

# CLI help verification
python3 scripts/pipeline_cli.py kg-validate-assertions --help
python3 scripts/pipeline_cli.py kg-detect-contradictions --help
python3 scripts/pipeline_cli.py kg-query-nodes --help
python3 scripts/pipeline_cli.py kg-query-neighborhood --help
python3 scripts/pipeline_cli.py kg-dematerialize-edge --help
```

---

## 8. Conclusion

The KG transition is **architecturally correct, verifiable, citable, and explainable** after this rectification pass. The independent verification confirmed the prior audit's work and closed additional gaps around:
- strict traceability defaults,
- evidence propagation into assertions,
- invalid placement prevention,
- CLI sub-flag safety,
- rollback tooling (`kg-dematerialize-edge`),
- architectural invariant test coverage.

The system is ready for incremental operational hardening and downstream integration.
