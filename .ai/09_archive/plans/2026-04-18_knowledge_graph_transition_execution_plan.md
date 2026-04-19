# Vitruvius — Knowledge Graph Transition: Execution Plan (v2)

**Prepared:** 2026-04-18  
**Status:** `PROPOSED`  
**Derived from:** `.ai/03_plans/vitruvius_knowledge_graph_transition_implementation_plan.md`  
**Informed by:**
- `.ai/02_audits/2026-04-18_knowledge_graph_transition_codebase_audit.md` (v2)
- `.ai/03_plans/2026-04-18_knowledge_graph_transition_readiness_plan.md` (v2)
**Audience:** Engineering, data pipeline, graph layer, AI orchestration, product  
**Purpose:** Concrete, phased, file-level implementation plan to transition Vitruvius from a document-primary JSON snapshot graph to a taxonomy-centered, evidence-backed canonical knowledge graph.

---

## 1. Implementation Strategy

**Incremental transition. No big-bang rewrite.**

The existing pipeline (`scan → convert → refine → canonicalize → extract → review → promote → build-graph`) is the only proven path from raw documents to validated relationships. It must remain operational throughout.

**Core rules:**
1. All new code is feature-flagged behind `kg_transition.*`.
2. The legacy JSON snapshot pipeline (`build-graph`) continues until Phase 6.
3. File-native lineage (Layers 1–4) is never modified by the new graph DB code.
4. Neo4j and PostgreSQL are treated as Layer 5 operational indexes, not sources of truth.
5. Every phase produces a working CLI command that can be demonstrated end-to-end.

---

## 2. Phase Map

| Phase | Name | Duration | Goal |
|-------|------|----------|------|
| 0 | Readiness | 10–14 days | Close all readiness gates |
| 1 | Evidence Graph | 7–10 days | Ingest documents into evidence nodes with selectors |
| 2 | Atomic Extraction | 7–10 days | Extract structured candidates using schema-constrained LLM outputs |
| 3 | Canonicalization & Placement | 7–10 days | Deduplicate, normalize, place into taxonomy, create assertions |
| 4 | Assertion Layer | 7–10 days | Validate assertions, materialize fast edges, detect contradictions |
| 5 | Query Switch | 5–7 days | Product queries use canonical graph first; evidence is secondary |
| 6 | Legacy Deprecation | 5–7 days | Stop writing to old structures; archive after parity |

**Total:** ~48–67 days (~10–14 weeks at 50% engineering bandwidth)

---

## 3. Phase 0 — Readiness

**Objective:** Close all readiness gates so Sprint 1 can begin safely.

**This phase is fully defined in the Readiness Plan.** The Execution Plan begins assuming Phase 0 is complete.

**Key deliverables assumed ready:**
- AD-043 merged; graph contract bumped to `2.0.0-alpha`
- Neo4j + PostgreSQL provisioned and reachable
- Pydantic models frozen in `scripts/vitruvius/kg/schemas.py`
- Taxonomy roots seeded
- Document versions backfilled
- Structured LLM client implemented
- Feature flags added

---

## 4. Phase 1 — Build the Evidence Graph

### 4.1 Objective

For every source document, create a chain of evidence nodes:

```text
DocumentVersion → Section → Chunk → EvidenceSpan
```

Each span must have a resolvable selector and a verifiable quote.

### 4.2 Why This Phase Exists First

The evidence graph is the foundation. Without it, canonical nodes and assertions have no provable backing. The target plan's non-negotiable rule #2 states: "Every user-visible node must be backed by evidence." Evidence must exist before canonical nodes can be validated.

### 4.3 Exact Code Areas Touched

#### Modified Files

| File | Change | Lines (approx) |
|------|--------|----------------|
| `scripts/vitruvius/parsers/base_parser.py` | Add `section_map` and `chunk_map` to `ParseResult` | 30–40 |
| `scripts/vitruvius/parsers/opendataloader_parser.py` | Populate `section_map` from sidecar JSON or markdown headers | 40–60 |
| `scripts/vitruvius/parsers/docling_parser.py` | Populate `section_map` from docling output | 20–30 |
| `scripts/vitruvius/normalization/refine.py` | Preserve section boundaries in refined output; emit `section_map` manifest | 30–50 |
| `scripts/pipeline_cli.py` | Add `kg-ingest-evidence`, `kg-ingest-evidence-batch`, `kg-resolve-span` subcommands | 60–80 |
| `config/vitruvius.yaml` | Add `kg_transition` block (if not done in Phase 0) | 15–20 |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/evidence_ingestor.py` | Orchestrate document → version → section → chunk → span pipeline |
| `scripts/vitruvius/kg/normalized_element.py` | `NormalizedElement` Pydantic model |
| `scripts/vitruvius/kg/selector_resolver.py` | Resolve selectors to text; validate quotes |
| `scripts/vitruvius/kg/neo4j_evidence_writer.py` | Write evidence chain to Neo4j |
| `scripts/vitruvius/kg/backfill_document_versions.py` | One-time backfill script for existing sources |
| `scripts/tests/test_evidence_ingestor.py` | End-to-end evidence ingestion tests |
| `scripts/tests/test_selector_resolver.py` | Selector resolution accuracy tests |
| `scripts/tests/test_neo4j_evidence_writer.py` | Neo4j evidence graph structure tests |

### 4.4 Data / Schema Changes

- **Neo4j:** Create node labels `DocumentVersion`, `Section`, `Chunk`, `EvidenceSpan`.
- **PostgreSQL:** Insert rows into `document_version` table.
- **No changes** to `001_`–`004_` file layers.

### 4.5 Migrations / Backfills

- Run `backfill_document_versions.py` once to create v1 records for all ~60 existing sources.
- Compute SHA-256 from raw files in `001_Raw-Source-Layer/`.

### 4.6 API / Backend Changes

- No HTTP API yet. New CLI subcommands only.

### 4.7 Frontend / UI Changes

- None. Evidence graph is not user-visible yet.

### 4.8 Feature Flags / Rollout Controls

```yaml
kg_transition:
  enabled: true          # Must be true for this phase
  evidence_graph: true   # Enable this phase
  neo4j_backend: true    # Enable Neo4j writes
  postgres_registry: true # Enable PostgreSQL writes
```

All other flags remain `false`.

### 4.9 Success Criteria

- [ ] A PDF document ingests into the evidence graph with ≥90% of sections/chunks resolvable.
- [ ] A Markdown document ingests with `heading_path` selectors that resolve to correct text.
- [ ] Selector resolver passes quote-matching on 100% of seed spans.
- [ ] Neo4j query `MATCH (d:DocumentVersion)-[:HAS_SECTION]->(s)-[:HAS_CHUNK]->(c)-[:HAS_SPAN]->(e) RETURN count(e)` returns expected count.
- [ ] Existing `build-graph` still produces valid v1 snapshot (backward compatibility).

### 4.10 Rollback / Failure Containment

- If evidence ingestion corrupts Neo4j, delete evidence nodes only: `MATCH (n:DocumentVersion|Section|Chunk|EvidenceSpan) DETACH DELETE n`.
- File-native data is untouched. Re-ingestion is idempotent (skips by SHA-256).

---

## 5. Phase 2 — Extract Atomic Knowledge Units

### 5.1 Objective

From chunks, extract structured candidates:
- `concept`
- `definition`
- `rule`
- `procedure`
- `exception`
- `constraint`
- `term` / `alias`
- `relationship_assertion` candidates

Every extraction must use schema-constrained LLM outputs (Pydantic-validated). Every candidate must cite ≥1 evidence span ID.

### 5.2 Why This Phase Exists Second

Canonical nodes cannot be created without atomic knowledge units. The current pipeline extracts relationships from full document text. The target pipeline extracts typed entities from chunks, then derives relationships between them.

### 5.3 Exact Code Areas Touched

#### Modified Files

| File | Change |
|------|--------|
| `scripts/vitruvius/relationships_sections.py` | Replace or extend regex extraction with structured LLM extraction gated by `kg_transition.structured_extraction` |
| `scripts/vitruvius/concept_enrichment.py` | Add structured LLM path for rule/definition/exception extraction when flag is on |
| `scripts/vitruvius/ollama_review.py` | Extend `build_prompt()` to support assertion review, not just relationship review |
| `scripts/pipeline_cli.py` | Add `kg-extract-candidates`, `kg-extract-candidates-batch`, `kg-validate-candidates` subcommands |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/extraction_engine.py` | `ExtractionEngine` class: `extract_concepts()`, `extract_rules()`, `extract_definitions()`, `extract_relationship_assertions()` |
| `scripts/vitruvius/kg/prompts/concept_extraction_prompt.txt` | One-task prompt for concept extraction |
| `scripts/vitruvius/kg/prompts/rule_extraction_prompt.txt` | One-task prompt for rule extraction |
| `scripts/vitruvius/kg/prompts/definition_extraction_prompt.txt` | One-task prompt for definition extraction |
| `scripts/vitruvius/kg/prompts/relationship_assertion_prompt.txt` | One-task prompt for edge extraction |
| `scripts/vitruvius/kg/candidate_store.py` | PostgreSQL tables: `candidate_nodes`, `candidate_assertions` |
| `scripts/tests/test_extraction_engine.py` | Mocked LLM extraction tests |
| `scripts/tests/test_candidate_store.py` | CRUD and status transition tests |

### 5.4 Data / Schema Changes

- **PostgreSQL:** Add `candidate_nodes` and `candidate_assertions` tables.
- **Neo4j:** No writes yet. Candidates are staged in PostgreSQL before promotion.

### 5.5 AI Orchestration Changes

- **Local models** (`gemma4:31b`): First-pass entity extraction, type classification, alias extraction.
- **Cloud models** (if available): Hard parent-placement decisions, cross-document legal reasoning.
- **Deterministic logic:** Schema validation, duplicate blocking, confidence thresholding.

**Critical rule:** One task per model call. One schema per task. No "do everything in one prompt" jobs.

### 5.6 Feature Flags

```yaml
kg_transition:
  structured_extraction: true   # Enable this phase
```

### 5.7 Success Criteria

- [ ] ≥90% of LLM extraction outputs pass Pydantic validation on first try (seed test set of 50 chunks).
- [ ] Every candidate node has ≥1 supporting span ID.
- [ ] Every candidate assertion has `reasoning_summary` and `evidence_ids`.
- [ ] Extraction run is auditable: `extraction_run` → `candidate_nodes` → `evidence_spans` chain is queryable.
- [ ] No raw parser output is consumed by extraction engine (only `NormalizedElement`).

### 5.8 Rollback

- If extraction quality is poor, set `structured_extraction: false`. Candidates remain in PostgreSQL but are not promoted.
- Re-extraction is idempotent by `extraction_run_id`.

---

## 6. Phase 3 — Canonicalize and Place

### 6.1 Objective

Turn noisy candidates into reusable canonical knowledge objects:
1. Normalize casing and naming.
2. Deduplicate exact and near-duplicates.
3. Resolve aliases.
4. Create canonical IDs.
5. Place nodes into seeded taxonomy.
6. Create `placement_assertion` objects.
7. Send ambiguous items to review queue.

### 6.2 Why This Phase Exists Third

Extraction produces candidates. Canonicalization promotes only validated candidates. The taxonomy must be seeded before placement can occur (hence Phase 0 taxonomy seeding).

### 6.3 Exact Code Areas Touched

#### Modified Files

| File | Change |
|------|--------|
| `scripts/vitruvius/promotion_validator.py` | Extend 17-rule validator to validate `CanonicalNode` and `PlacementAssertion` candidates |
| `scripts/vitruvius/promotion/__init__.py` | Extend batch runner to write promoted canonical nodes to Neo4j (not just Markdown files) |
| `scripts/pipeline_cli.py` | Add `kg-canonicalize-candidates`, `kg-review-placement`, `kg-promote-canonical-node` subcommands |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/canonicalizer.py` | `normalize_label()`, `dedupe_candidates()`, `resolve_aliases()`, `assign_canonical_id()` |
| `scripts/vitruvius/kg/placement_engine.py` | Taxonomy placement: deterministic rules → nearest-neighbor → cluster suggestion → AI adjudication → review queue |
| `scripts/vitruvius/kg/merge_adjudicator.py` | `propose_merge()`, `adjudicate_merge()` |
| `scripts/vitruvius/kg/neo4j_canonical_writer.py` | Write `CanonicalNode` and `PlacementAssertion` to Neo4j |
| `scripts/tests/test_canonicalizer.py` | Dedupe precision/recall tests |
| `scripts/tests/test_placement_engine.py` | Parent correctness tests |
| `scripts/tests/test_merge_adjudicator.py` | Merge precision tests |

### 6.4 Data / Schema Changes

- **Neo4j:** Create `CanonicalNode` nodes with `PLACEMENT_ASSERTION` relationships to taxonomy parents.
- **PostgreSQL:** Enqueue ambiguous placements/merges in `review_queue`.

### 6.5 Promotion Rules (New)

A `CanonicalNode` can become `validated` only if:
- type is valid (`NodeType` enum)
- id is stable (`<type>-<slug>`)
- evidence count ≥ 1
- summary exists (non-empty)
- taxonomy placement exists (has `PlacementAssertion`)
- no unresolved hard-duplicate conflict

### 6.6 Feature Flags

```yaml
kg_transition:
  taxonomy_seeding: true   # Allow AI to propose deeper placements
```

**Policy:** AI can propose subtopics, concept clusters, rule placements, alias groups. New top-level branches require human review.

### 6.7 Success Criteria

- [ ] Dedupe precision ≥ 95% on gold dataset (no false merges).
- [ ] Dedupe recall ≥ 90% on gold dataset.
- [ ] Top-level taxonomy drift rate = 0% (no AI-invented roots).
- [ ] 100% of promoted canonical nodes have `taxonomy_path` and `summary`.
- [ ] Review queue contains all ambiguous placements and merges.

### 6.8 Rollback

- Demote canonical nodes to `candidate` status in Neo4j.
- Restore review queue items to `pending`.
- Legacy snapshot is unaffected.

---

## 7. Phase 4 — Build Assertions and Materialized Edges

### 7.1 Objective

1. Create `relationship_assertion` objects for all candidate edges.
2. Attach reasoning summary + evidence IDs.
3. Validate assertions against promotion rules.
4. Materialize fast traversal edges in Neo4j only for validated assertions.
5. Keep both: assertion node (source of truth) + direct edge (fast traversal).

### 7.2 Why This Phase Exists Fourth

Edges must be explainable. A relationship is not just an edge — it is a claim. Without assertions, the UI cannot answer "why are these two nodes connected?"

### 7.3 Exact Code Areas Touched

#### Modified Files

| File | Change |
|------|--------|
| `scripts/vitruvius/promotion_validator.py` | Add assertion validation rules (reasoning_summary exists, evidence count ≥ 1, inference_type declared, confidence ≥ 0.85, no contradiction blocker) |
| `scripts/vitruvius/graph/builder.py` | Add v2 build path: materialize fast edges from validated assertions when `kg_transition.legacy_snapshot_mode: false` |
| `scripts/pipeline_cli.py` | Add `kg-validate-assertions`, `kg-materialize-edges`, `kg-detect-contradictions`, `kg-dematerialize-edge` subcommands |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/assertion_validator.py` | `AssertionValidator` class with promotion rules |
| `scripts/vitruvius/kg/edge_materializer.py` | `materialize_fast_edge()` — creates direct Neo4j edge with `assertion_id` property |
| `scripts/vitruvius/kg/contradiction_detector.py` | Offline contradiction sweep (OVERRIDES vs APPLIES_TO, REQUIRES vs EXCLUDES, conflicting inference_types) |
| `scripts/tests/test_assertion_validator.py` | All promotion rules tested |
| `scripts/tests/test_edge_materializer.py` | Fast edges created only for validated assertions |
| `scripts/tests/test_contradiction_detector.py` | Known contradiction patterns detected |

### 7.4 Neo4j Pattern

```cypher
// Source of truth
(CanonicalNode)<-[:FROM]-(Assertion:RelationshipAssertion)-[:TO]->(CanonicalNode)
(Assertion)-[:SUPPORTED_BY]->(EvidenceSpan)
(Assertion)-[:GENERATED_BY]->(ExtractionRun)
(Assertion)-[:REVIEWED_BY]->(Review)

// Fast traversal edge
(CanonicalNode)-[:DEPENDS_ON {assertion_id: "assert-...", confidence: 0.94}]->(CanonicalNode)
```

### 7.5 Feature Flags

```yaml
kg_transition:
  assertion_layer: true   # Enable this phase
```

### 7.6 Success Criteria

- [ ] 100% of visible edges in Neo4j carry an `assertion_id` property.
- [ ] 100% of validated assertions have `reasoning_summary` and `evidence_ids`.
- [ ] Invalid assertions are rejected; none are silently promoted.
- [ ] Contradiction detector finds ≥80% of seeded contradiction pairs.
- [ ] Dematerialization rollback restores graph to pre-promotion state.

### 7.7 Rollback

- `kg-dematerialize-edge <assertion_id>` removes the fast edge but preserves the assertion node.
- Re-materialization is idempotent.

---

## 8. Phase 5 — Switch Product Queries

### 8.1 Objective

1. Search canonical nodes and assertions first, documents second.
2. Graph UI uses canonical nodes as default view.
3. Edge inspector resolves assertion records.
4. Answer generation uses canonical nodes + evidence spans.
5. Quizzes use canonical rules/concepts, not chunks.

### 8.2 Why This Phase Exists Fifth

The product must use the new graph. Until this phase, the new graph is an invisible sidecar.

### 8.3 Exact Code Areas Touched

#### Modified Files

| File | Change |
|------|--------|
| `scripts/vitruvius/query/engine.py` | Add `QueryEngineV2` class or new functions that query Neo4j canonical graph first, evidence second |
| `scripts/vitruvius/query/cli.py` | Add `kg-query-nodes`, `kg-query-neighborhood`, `kg-query-assertion` subcommands |
| `scripts/vitruvius/graph/visualize.py` | Update HTML generator to show canonical nodes by default; add edge inspector panel with assertion detail |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/query_engine_v2.py` | `search_nodes()`, `get_neighborhood()`, `get_assertion_detail()`, `build_answer()` |
| `scripts/vitruvius/kg/quiz_generator.py` | Generate quizzes from validated concept/rule/definition nodes |
| `scripts/tests/test_query_engine_v2.py` | Search relevance, neighborhood completeness |

### 8.4 UI Changes (Static HTML)

Since no SPA exists, update the Cytoscape.js HTML generator:
- Default view: canonical nodes + semantic edges only.
- Inspector panel (edge click): relationship label, reasoning summary, inference type, evidence bundle, confidence, source links.
- Evidence cards: document title, page, quote, deep link.

**Note:** If the team decides to build a real SPA, that work should happen in parallel and is not part of this execution plan.

### 8.5 API Changes

No HTTP API yet. Continue with CLI subcommands. If an API is needed, build it after this phase using the query engine v2 functions.

### 8.6 Feature Flags

```yaml
kg_transition:
  legacy_snapshot_mode: false   # Stop building v1 snapshots for product queries
```

**Rule:** Keep `legacy_snapshot_mode: true` until parity is confirmed.

### 8.7 Success Criteria

- [ ] Query results prioritize validated canonical nodes over source documents.
- [ ] Edge click payload contains full assertion detail + evidence + deep links.
- [ ] Quiz questions are derived from canonical rules/concepts, not raw chunks.
- [ ] API response time < 500ms for node + neighborhood queries on the laws aggregate.
- [ ] Legacy `query-structured` CLI still works when `legacy_snapshot_mode: true`.

### 8.8 Rollback

- Set `legacy_snapshot_mode: true`.
- Rebuild v1 JSON snapshot.
- All product queries fall back to legacy path.

---

## 9. Phase 6 — Deprecate Legacy Document-Primary Graph

### 9.1 Objective

1. Keep legacy mapping for compatibility.
2. Stop writing to old JSON snapshot structures.
3. Archive old visualizations if needed.
4. Remove old query paths after parity is confirmed.
5. Update all documentation.

### 9.2 Exact Code Areas Touched

#### Modified Files

| File | Change |
|------|--------|
| `scripts/vitruvius/graph/builder.py` | Add guard: skip v1 build when `legacy_snapshot_mode: false` |
| `scripts/vitruvius/graph/snapshot.py` | Deprecation warning when v1 snapshots are read |
| `README.md` | Update architecture diagram |
| `AGENTS.md` | Update graph layer description |
| `docs/CANONICALIZATION_RULES.md` | Add new node types |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/vitruvius/kg/parity_checker.py` | Verify legacy snapshot vs Neo4j graph equivalence |

### 9.3 Cutover Criteria

- [ ] Parity checker reports ≥95% coverage of legacy nodes/edges in new graph.
- [ ] Remaining gaps are explicitly documented (orphans, deprecated sources).
- [ ] `build-graph` no longer writes v1 JSON when `legacy_snapshot_mode: false`.
- [ ] All documentation reflects new architecture.
- [ ] No references to "document-primary graph" as current state in root docs.

### 9.4 Cleanup Actions

- Move old visualization HTMLs to `004_Derived-Content-Layer/archive/`.
- Update `.ai/01_roadmap/current-phase.md` to next active work.
- Update `.ai/01_roadmap/milestone-tracker.md`: mark "KG Transition" as complete.
- Add AD-044: "Knowledge Graph Transition Complete" to `.ai/10_state/decisions.md`.

### 9.5 Irreversibility Warning

**Phase 6 is irreversible.** Once v1 snapshot code is removed, the legacy path cannot be restored. Do not execute Phase 6 until:
- Product queries have run on the new graph for ≥30 days without critical regression.
- All stakeholders have signed off.
- A full backup of the last v1 snapshot exists.

---

## 10. PR Slicing / Workstream Slicing

Do not submit one giant PR. Slice as follows:

### PR 1: Phase 0 Infrastructure
- AD-043, contract bump, Pydantic schemas, Neo4j/PostgreSQL connectivity, feature flags
- **Files:** `contract.py`, `kg/schemas.py`, `kg/enums.py`, `kg/neo4j_schema.cypher`, `db/schema.sql`, `config/vitruvius.yaml`, tests

### PR 2: Phase 1 Evidence Graph
- Parser structural output, evidence ingestion, selector resolution, backfill script
- **Files:** `parsers/base_parser.py`, `parsers/opendataloader_parser.py`, `kg/evidence_ingestor.py`, `kg/selector_resolver.py`, `kg/neo4j_evidence_writer.py`, tests

### PR 3: Phase 2 Atomic Extraction
- Structured LLM client, extraction engine, candidate store, prompts
- **Files:** `llm/structured_client.py`, `kg/extraction_engine.py`, `kg/candidate_store.py`, `kg/prompts/*.txt`, tests

### PR 4: Phase 3 Canonicalization
- Canonicalizer, placement engine, merge adjudicator, Neo4j canonical writer
- **Files:** `kg/canonicalizer.py`, `kg/placement_engine.py`, `kg/merge_adjudicator.py`, `kg/neo4j_canonical_writer.py`, tests

### PR 5: Phase 4 Assertions
- Assertion validator, edge materializer, contradiction detector
- **Files:** `kg/assertion_validator.py`, `kg/edge_materializer.py`, `kg/contradiction_detector.py`, tests

### PR 6: Phase 5 Query Switch
- Query engine v2, quiz generator, visualize.py updates
- **Files:** `kg/query_engine_v2.py`, `kg/quiz_generator.py`, `query/engine.py`, `graph/visualize.py`, tests

### PR 7: Phase 6 Deprecation
- Parity checker, legacy freeze, documentation updates
- **Files:** `kg/parity_checker.py`, `graph/builder.py`, `README.md`, `AGENTS.md`, docs

---

## 11. Data Migration Strategy

### 11.1 Legacy Mapping

**File:** `006_System-Manifests/migrations/kg_legacy_mapping.yaml`

Catalog all existing `source-*` and `concept-*` IDs. Map to new canonical IDs where applicable.

```yaml
mappings:
  nodes:
    - legacy_id: law-pd-1096
      new_ids: [docv-pd1096-v1]  # becomes DocumentVersion, not CanonicalNode
    - legacy_id: concept-building-permit
      new_ids: [concept-building-permit]  # may remain if type is already "concept"
  edges:
    - legacy_id: rel-concept-floor-area-affects-concept-building-height
      new_assertion_id: assert-concept-floor-area-affects-concept-building-height-0001
```

### 11.2 Document-Primary → Evidence

- `source-*` nodes in v1 snapshot become `DocumentVersion` nodes in evidence graph.
- They are **not** primary canonical nodes. They are evidence containers.

### 11.3 Concept Migration

- Existing `concept-*` pages are **candidates**, not validated canonical nodes.
- Run them through the canonicalization pipeline (dedupe, placement, enrichment).
- Only promote if they pass validation rules.

### 11.4 Edge Migration

- Existing `GraphEdge` records become `RelationshipAssertion` candidates.
- `evidence_snippet` strings must be linked to `EvidenceSpan` records (may require manual curation if selectors are missing).
- Materialize new fast edges only after assertions are validated.

### 11.5 Coexistence Strategy

| Phase | Legacy Path | New Path |
|-------|------------|----------|
| 1–3 | Active (v1 snapshots) | Sidecar (Neo4j evidence + candidates) |
| 4 | Active | Sidecar (assertions materialized) |
| 5 | Active but product queries switch to new path | Primary |
| 6 | Frozen, then removed | Primary |

---

## 12. Risk Controls

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Local LLM cannot achieve ≥90% structured output validity | Medium | High | Fallback to cloud models; reduce extraction scope to smaller seed set |
| Neo4j operational complexity exceeds team capacity | Medium | High | Start with Community Edition; use Kuzu skill as transferrable knowledge; keep file-native lineage as backup |
| AD-001 conflict stalls decision-making | Medium | Critical | Draft AD-043 now; escalate to roadmap gatekeeper if blocked |
| Parser structural output breaks existing conversion pipeline | Low | High | Extend `ParseResult` with optional fields; all existing parsers continue returning `markdown_text` unchanged |
| Concept pages are too shallow to seed canonical graph | High | Medium | Use only 10–20 well-enriched concepts for Sprint 1; treat others as candidates requiring enrichment |
| Big-bang temptation | Medium | Critical | Enforce PR slicing; every PR must be reviewable in <1 hour; feature flags gate all new behavior |
| Phase 6 executed prematurely | Low | Critical | Require 30-day burn-in on new graph; parity checker ≥95%; stakeholder sign-off |

---

## 13. Validation Plan

### 13.1 Build a Gold Dataset

**Location:** `006_System-Manifests/gold/`

Include:
- Clean PDF
- Scanned PDF
- Markdown
- Tables
- Sections with exceptions
- Cross-references
- Definition-heavy sections
- Rule-heavy sections

### 13.2 Evaluation Dimensions

| Dimension | Metric | Target |
|-----------|--------|--------|
| Parsing quality | Text recovery, section detection, page/span fidelity | ≥95% section detection accuracy |
| Extraction quality | Correct node type, label, boundary | ≥85% correct type; ≥90% correct label |
| Canonicalization quality | Merge precision, merge recall, alias correctness | ≥95% precision; ≥90% recall |
| Taxonomy placement quality | Parent correctness, top-level drift rate | ≥90% parent correctness; 0% top-level drift |
| Edge quality | Relation precision, explanation correctness, evidence support | ≥85% relation precision; 100% explanation exists |
| Citation quality | Link resolves, highlight resolves, quote matches source | 100% link resolves; 100% quote matches |

### 13.3 Minimum Acceptance Criteria

The new graph is not production-ready until:
- 100% of visible nodes have evidence
- 100% of visible edges resolve to an assertion record
- 100% of visible assertions have a reasoning summary
- 100% of evidence links resolve to a source location
- Taxonomy roots are stable
- Legacy graph parity is acceptable for key product flows

---

## 14. Immediate Next Implementation Sprint

### Sprint 1: Evidence Graph End-to-End (7–10 days)

**Goal:** A minimal working flow where a document is ingested, evidence spans are stored, and one concept-to-rule edge is created as an assertion with explanation + citation.

**Tasks:**
1. Extend `BaseParser.parse()` to return `section_map` (2 days).
2. Implement `EvidenceSpan` Pydantic model + `Selector` variants (1 day).
3. Implement `selector_resolver.py` with quote validation (2 days).
4. Implement `neo4j_evidence_writer.py` with evidence chain pattern (2 days).
5. Add `kg-ingest-evidence` CLI subcommand (1 day).
6. Write tests for all new modules (2 days).

**Deliverable:**
```bash
python scripts/pipeline_cli.py kg-ingest-evidence \
  "001_Raw-Source-Layer/001-Laws/PD-1096/nbc.pdf"
# → Neo4j contains DocumentVersion → Section → Chunk → EvidenceSpan chain
# → Selector resolution passes for all spans
```

**Success criteria:**
- Neo4j evidence graph query returns correct span count.
- Selector resolver passes 100% of seed spans.
- Existing `build-graph` still produces valid v1 snapshot.

---

*End of Execution Plan*
