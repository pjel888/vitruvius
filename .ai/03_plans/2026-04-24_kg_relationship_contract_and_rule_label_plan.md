# KG Relationship Contract and Rule Label Improvement Plan

## Metadata
- **Status:** bounded slice validated 2026-04-24
- **Created:** 2026-04-24
- **Audit:** `.ai/02_audits/2026-04-24_kg_relationship_quality_and_graph_ux_audit.md`
- **Scope:** bounded first slice for relationship quality + rule-name UX

## Goal
Improve KG trust and usability by aligning relationship semantics across layers and making rule-node names concise, stable, taxonomy-aware, and distinct from full evidence text.

## Non-Goals
- Do not bulk-validate existing candidate assertions.
- Do not add a large ontology or many new predicates.
- Do not re-review/backfill the full historical graph in this first slice.
- Do not tune force-directed layout as a substitute for data quality.

## Phase 1 — Relationship Contract Alignment

### Tasks
- [ ] Reconcile predicate vocabulary across:
  - `.ai/06_specs/relationship-schema.md`
  - `scripts/vitruvius/rules/relationship_registry.yaml`
  - `scripts/vitruvius/kg/enums.py`
  - `scripts/vitruvius/kg/evidence_materializer.py`
- [ ] Decide whether `covers` becomes official or is removed from runtime behavior.
- [ ] Replace silent fallback mapping in `_edge_type_from_string()` with explicit mapping + validation warning/failure.
- [ ] Add tests that fail if schema/registry/materializer mappings drift.

### Acceptance Criteria
- Every allowed legacy predicate has an explicit KG v2 mapping.
- No predicate exists in only one layer without an intentional compatibility note.
- Unknown predicates fail validation or produce a hard warning that blocks graph-quality claims.

## Phase 2 — Persisted Display Labels for Rule Nodes

### Tasks
- [ ] Add optional `display_label` to `CanonicalNode` in `scripts/vitruvius/kg/schemas.py`.
- [ ] Update `rule_extractor.py` to generate:
  - `label`: source-faithful full rule/evidence label,
  - `display_label`: concise taxonomy-aware graph label,
  - `summary`: full evidence snippet / legal source text.
- [ ] Use taxonomy leaf + target concept + action cue where possible.
- [ ] Keep API `displayLabel` fallback, but prefer persisted `display_label` when available.
- [ ] Add tests for stable rule display labels and collision behavior within taxonomy branches.

### Acceptance Criteria
- Rule graph labels are short enough to scan.
- Full evidence text remains accessible in inspector/source panels.
- Rebuilding the same snapshot generates stable `display_label` values.
- API and Explorer use `displayLabel` for compact surfaces while preserving canonical `id` and full `label`.

## Phase 3 — Relationship Distribution Quality Report

### Tasks
- [ ] Add a snapshot audit/report command or test helper that summarizes:
  - predicate distribution,
  - review-state distribution,
  - validation-state distribution,
  - concept/rule taxonomy coverage,
  - bidirectional duplicate-like relationships,
  - evidence count per assertion.
- [ ] Emit warnings when the graph is overwhelmingly structural (`DEFINED_BY`/`SUPPORTED_BY`) and low on semantic edges.

### Acceptance Criteria
- Operators can see whether a snapshot is semantically useful, not just structurally valid.
- The report makes relationship-quality regressions visible before Explorer UX claims are made.

## Phase 4 — Deferred Semantic Enrichment Design

Only after Phases 1–3 pass:
- Design taxonomy-aware candidate edge generation.
- Distinguish explicit, reviewed, and taxonomy-lifted/inferred edges.
- Validate with stratified sampling before promotion.

## Validation Strategy
- TDD for schema, mapper, rule-label, and snapshot-quality report behavior.
- Run targeted KG tests first, then broader relevant KG test suite.
- Rebuild a KG v2 snapshot on a bounded dataset and compare relationship distributions before/after.
- Stop if predicate mappings are ambiguous or taxonomy paths fail to resolve.

## Post-Audit Execution Status - 2026-04-24

The bounded `001-Laws` rebuild/QA slice is validated.

- Clean rebuilt snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`.
- Scope: 181 canonical source pages, all with `source_relative_markdown_path` under `001-Laws/`; 2 of those are under `001-Laws/refined_markdown/test/...`.
- Rule title quality: 214 rules, 0 duplicate display labels, 0 generic display labels, 0 display-title truncation markers.
- Source title quality: 181 source pages, 0 non-`001-Laws` source paths, 0 generic/invalid source titles after frontmatter repair.
- Neo4j: cleared to 0 nodes, loaded 5911/5911 Cypher statements with 0 errors, ended at 2429 nodes.
- Verification: 48 targeted title/quality tests, 86 KG materialization tests, 174 pipeline/canonicalization tests, 294 `test_kg*.py` tests, 13 API tests, 16 Explorer tests, and `explorer` production build passed.

Deferred: relationship semantics remain shallow in this laws-only graph (`DEFINED_BY=214`, `SUPPORTED_BY=214`, `REQUIRES=3`, `RELATED_TO=1`). Cross-subject relationships such as Laws to Utilities require a later aggregate/cross-subject enrichment pass after multiple subjects are admitted.

## Key Files
- `.ai/06_specs/relationship-schema.md`
- `scripts/vitruvius/rules/relationship_registry.yaml`
- `scripts/vitruvius/kg/enums.py`
- `scripts/vitruvius/kg/evidence_materializer.py`
- `scripts/vitruvius/kg/rule_extractor.py`
- `scripts/vitruvius/kg/schemas.py`
- `scripts/tests/test_kg_*.py`
- `api/index.ts`
- `explorer/src/utils/labels.ts`
