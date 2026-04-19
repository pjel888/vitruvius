# 05 — PR Sequence: Taxonomy Governance Build

> **Scope:** Pull request sequence for building the governed taxonomy architecture.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `03_implementation_plan.md`

---

## Global Rules for Every PR

1. **No PR without a plan.** Every PR must reference a phase in `03_implementation_plan.md` and a gap in `04_gap_matrix.md`.
2. **Definition of Done (DoD) is mandatory.** Every PR has a DoD checklist. No PR merges without all items checked.
3. **Rollback condition is mandatory.** Every PR must state the exact rollback command or revert commit.
4. **No breaking changes in v1.** All changes to v1 API/UI are additive-only.
5. **Shadow graph first.** Any PR that touches the runtime graph must include shadow graph build + parity check.
6. **Migration generate → diff → review → apply.** No direct in-place mutation of canonical content.
7. **All PRs require at least one steward review** for canonical/content changes, one engineer review for schema/runtime changes.

---

## PR-00: Project Bootstrap

**Branch:** `feat/taxonomy-governance-bootstrap`
**Phase:** 0 (preparatory)
**Gaps:** None (infrastructure)

### Scope
- Create `003_Canonical-Knowledge-Layer/backbone/` directory
- Add `scripts/vitruvius/taxonomy/` package
- Add `006_System-Manifests/audits/taxonomy-governance/` directory
- Update `config/vitruvius.yaml` with feature flags: `k_taxonomy_v2: false`, `k_jurisdictional_overrides: false`, `k_standards_mapping: false`, `k_vitruvian_context: false`

### Definition of Done
- [ ] Directory structure exists
- [ ] Feature flags are readable by pipeline CLI
- [ ] `scripts/vitruvius/taxonomy/__init__.py` exists
- [ ] No runtime behavior changes

### Rollback
```bash
git revert <commit>
rm -rf scripts/vitruvius/taxonomy/
```

---

## PR-01: Backbone Schema + Neo4j Indexes

**Branch:** `feat/backbone-schema`
**Phase:** 0
**Gaps:** G001 (partial), G002, G048, G049, G050

### Scope
- Add `BackboneNode` Pydantic model
- Add `IdRedirect` Pydantic model
- Add `FacetEnum` models
- Extend `CanonicalNode` with new fields
- Add Neo4j Cypher: new labels, properties, constraints, indexes
- Add PostgreSQL schema: `id_redirect`, `taxonomy_release` tables
- Add TypeScript types: `GraphNode` extensions, `FacetFilter`, `ResolvedContext`

### Definition of Done
- [ ] All Pydantic models pass `mypy scripts/vitruvius/kg/schemas.py`
- [ ] All TypeScript types pass `tsc --noEmit` in `explorer/`
- [ ] Neo4j Cypher script runs without error on empty database
- [ ] PostgreSQL schema script runs without error
- [ ] `scripts/vitruvius/taxonomy/validate_backbone.py` exists and validates L1–L2 structure
- [ ] Unit tests for `BackboneNode` and `IdRedirect`
- [ ] Feature flags wired to schema loading

### Rollback
```bash
git revert <commit>
# Manual: drop new Neo4j indexes and labels
# Manual: drop new PostgreSQL tables
```

---

## PR-02a: Jurisdiction Model (Graph Schema)

**Branch:** `feat/jurisdiction-model-graph`
**Phase:** 4
**Gaps:** G013, G014 (partial)

### Scope
- Add Neo4j labels: `Jurisdiction`, `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition`
- Add Neo4j edges: `WITHIN_JURISDICTION`, `HAS_EDITION`, `SUPERSEDES`, `SUPERSEDED_BY`
- Add Cypher constraints and indexes for new labels

### Definition of Done
- [ ] Cypher script runs without error
- [ ] Unit test: create jurisdiction hierarchy, query by code
- [ ] Unit test: create authority document family + edition + supersession chain
- [ ] Schema documentation updated

### Rollback
```bash
git revert <commit>
# Manual: drop new labels and edge types
```

---

## PR-02b: Jurisdiction Model (Data Schema)

**Branch:** `feat/jurisdiction-model-data`
**Phase:** 4
**Gaps:** G013, G014 (partial), G015

### Scope
- Add Pydantic models: `Jurisdiction`, `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition`, `ApplicabilityRule`
- Add PostgreSQL tables for all models
- Add `ApplicabilityRule` engine with precedence resolver

### Definition of Done
- [ ] All models pass `mypy`
- [ ] PostgreSQL schema migration runs without error
- [ ] Unit test: jurisdiction precedence resolver (`local > regional > national`)
- [ ] Unit test: applicability rule evaluation

### Rollback
```bash
git revert <commit>
# Manual: drop new PostgreSQL tables
```

---

## PR-02c: Jurisdiction Model (API Contract)

**Branch:** `feat/jurisdiction-model-api`
**Phase:** 4, 6
**Gaps:** G031 (partial)

### Scope
- Add API v2 types: `JurisdictionResponse`, `AuthorityDocumentResponse`, `ResolvedContext`
- Add API v2 endpoint stubs: `GET /v2/jurisdiction/:code`, `POST /v2/resolve`
- Add contract tests (stubs return 501 Not Implemented)

### Definition of Done
- [ ] All new TypeScript types pass `tsc --noEmit`
- [ ] Contract tests pass
- [ ] OpenAPI spec updated (if applicable)

### Rollback
```bash
git revert <commit>
```

---

## PR-03: DocumentVersion vs DocumentEdition Separation

**Branch:** `feat/doc-edition-separation`
**Phase:** 0 (schema), 4 (data)
**Gaps:** G020, G021, G022

### Scope
- Create `AuthorityDocumentEdition` Pydantic model
- Create `AuthorityDocumentFamily` Pydantic model
- Preserve existing `DocumentVersion` (no breaking changes)
- Add `SUPERSEDES` / `SUPERSEDED_BY` edge support
- Update graph builder to emit both `DocumentVersion` and `AuthorityDocumentEdition` nodes

### Definition of Done
- [ ] `DocumentVersion` model unchanged (backward compatibility)
- [ ] New models pass `mypy`
- [ ] Graph builder unit test: emits both label types
- [ ] Neo4j Cypher: `SUPERSEDES` edge type added

### Rollback
```bash
git revert <commit>
# Manual: remove AuthorityDocumentEdition nodes from Neo4j
```

---

## PR-04: Standards Mapping Schema

**Branch:** `feat/standards-mapping-schema`
**Phase:** 5
**Gaps:** G023

### Scope
- Add `StandardReference` Pydantic model
- Add `StandardMapping` Pydantic model
- Add Neo4j edge: `MAPS_TO_STANDARD`
- Add PostgreSQL table: `standard_mapping`

### Definition of Done
- [ ] Models pass `mypy`
- [ ] Neo4j Cypher runs without error
- [ ] PostgreSQL migration runs without error
- [ ] Unit test: create standard reference + mapping

### Rollback
```bash
git revert <commit>
# Manual: drop standard_mapping table, remove MAPS_TO_STANDARD edges
```

---

## PR-05: ID Generator + Redirect Table

**Branch:** `feat/id-generator-redirects`
**Phase:** 2
**Gaps:** G006, G007

### Scope
- `id_generator.py`: deterministic, seeded, collision-free `VTN-*` generator
- `scripts/vitruvius/taxonomy/populate_redirects.py`: maps all existing semantic slugs to new IDs
- PostgreSQL `id_redirect` table population
- Neo4j: add `canonical_id` property to existing nodes

### Definition of Done
- [ ] 10k generated IDs, zero collisions (unit test)
- [ ] All ~105 concept IDs and ~340 source IDs mapped
- [ ] `id_redirect` CSV committed to `006_System-Manifests/audits/taxonomy-governance/`
- [ ] Neo4j `canonical_id` property present on all existing nodes
- [ ] Unit test: lookup old ID → new ID

### Rollback
```bash
git revert <commit>
# Manual: remove canonical_id properties from Neo4j
# Manual: truncate id_redirect table
```

---

## PR-06: HTTP Redirect Handler

**Branch:** `feat/http-redirect-handler`
**Phase:** 2
**Gaps:** G008

### Scope
- API v1: return `canonical_id` in all node responses (additive)
- API v2: `GET /v2/node/:canonical_id` resolves opaque IDs
- HTTP 308 Permanent Redirect for old semantic slug URLs
- Unit tests for redirect behavior

### Definition of Done
- [ ] v1 endpoints return `canonical_id` (additive, no breaking changes)
- [ ] v2 endpoint resolves `VTN-*` IDs
- [ ] 308 redirect test: old slug → new canonical URL
- [ ] Regression test: v1 clients still work

### Rollback
```bash
git revert <commit>
```

---

## PR-07: Facet Assignment Engine

**Branch:** `feat/facet-assignment-engine`
**Phase:** 3
**Gaps:** G009, G010

### Scope
- `scripts/vitruvius/taxonomy/assign_facets.py`: reads concept frontmatter, assigns facets based on backbone + rules
- Update concept frontmatter with new facet fields
- `validate_facets.py`: checks for nulls, unknown values, cross-field rules
- Home-domain assignment rulebook implementation

### Definition of Done
- [ ] All ~105 concepts have non-null facet values
- [ ] `validate_facets.py` passes with zero errors
- [ ] Home-domain rulebook applied (cross-cutting subjects assigned correctly)
- [ ] Diff review: concept frontmatter changes reviewed by steward

### Rollback
```bash
git revert <commit>
# Manual: run scripts/vitruvius/taxonomy/rollback_facets.py
```

---

## PR-08: Philippine Jurisdiction Pack

**Branch:** `feat/philippine-jurisdiction-pack`
**Phase:** 4
**Gaps:** G016, G017

### Scope
- Extract Philippine rules from `scripts/vitruvius/rules/canonical_rules.yaml`
- Create `config/jurisdictions/PH.yaml` with jurisdiction hierarchy
- Create `AuthorityDocumentFamily` and `AuthorityDocumentEdition` records for Philippine codes
- Create `ApplicabilityRule` records for Philippine obligations
- Remove `regulatory_basis` from concept frontmatter; replace with `SUPPORTED_BY` edges + overlays

### Definition of Done
- [ ] `config/jurisdictions/PH.yaml` passes schema validation
- [ ] All Philippine source documents have `AuthorityDocumentEdition` nodes
- [ ] No `regulatory_basis` remains in concept frontmatter
- [ ] `SUPPORTED_BY` edges connect concepts to evidence spans
- [ ] Overlay nodes connect concepts to jurisdiction + edition
- [ ] Steward review of jurisdiction pack

### Rollback
```bash
git revert <commit>
# Manual: restore regulatory_basis in concept frontmatter
# Manual: remove jurisdiction nodes and edges
```

---

## PR-09: Seed Standards Mappings

**Branch:** `feat/seed-standards-mappings`
**Phase:** 5
**Gaps:** G024

### Scope
- Create 20+ `StandardMapping` records for Philippine building codes
- Target systems: OmniClass, Uniclass, IFC, MasterFormat, ICC
- Add `GET /v2/standards` endpoint (stub → full implementation)

### Definition of Done
- [ ] 20+ mappings committed
- [ ] `GET /v2/standards?system=OmniClass` returns mappings
- [ ] Mappings reviewed for accuracy

### Rollback
```bash
git revert <commit>
# Manual: remove StandardMapping edges
```

---

## PR-10: Neo4j Full-Text Search Index

**Branch:** `feat/neo4j-fts-index`
**Phase:** 6
**Gaps:** G027

### Scope
- Create Neo4j full-text index `canonicalSearch` on `label`, `aliases`, `summary`, `path_code`
- Add composite indexes for facet filtering
- Add performance benchmark: <200ms for 10k-node graph

### Definition of Done
- [ ] FTS index created successfully
- [ ] Benchmark test passes (<200ms)
- [ ] Index is documented in `scripts/vitruvius/kg/neo4j_schema.cypher`

### Rollback
```bash
git revert <commit>
# Manual: DROP INDEX canonicalSearch
```

---

## PR-11: API v2 Implementation

**Branch:** `feat/api-v2-implementation`
**Phase:** 6
**Gaps:** G028, G031, G032

### Scope
- Implement all v2 endpoints:
  - `GET /v2/taxonomy` — governed backbone tree
  - `GET /v2/search?q=...&facets=...&jurisdiction=...&date=...` — FTS + facet filtering
  - `GET /v2/node/:id` — facets, mappings, provenance, related nodes
  - `POST /v2/resolve` — jurisdiction-aware context resolution
  - `GET /v2/jurisdiction/:code` — jurisdiction chain + applicable documents
  - `GET /v2/standards?system=...&code=...`
- Contract tests for all endpoints
- Regression tests for v1 endpoints

### Definition of Done
- [ ] All v2 endpoints pass contract tests
- [ ] All v1 endpoints pass regression tests
- [ ] OpenAPI spec updated
- [ ] Response latency <200ms for search, <100ms for node lookup

### Rollback
```bash
git revert <commit>
# Manual: remove v2 route handlers
```

---

## PR-12: Explorer Read-Only Updates

**Branch:** `feat/explorer-readonly-v2`
**Phase:** 7
**Gaps:** G034, G035, G036, G037, G038

### Scope
- `FacetPanel` component
- `JurisdictionSelector` component
- `LayerBadge` component
- Updated node detail page with facets, overlays, standards mappings
- Dynamic node/edge type rendering (no hardcoded lists)
- Taxonomy tree continues to work (backward-compatible)

### Definition of Done
- [ ] Explorer builds without errors (`npm run build`)
- [ ] Facet panel visible on node detail pages
- [ ] Jurisdiction selector visible in search bar
- [ ] Layer badges visible on node cards
- [ ] Taxonomy tree renders correctly for v1 data
- [ ] No write operations exposed in UI

### Rollback
```bash
git revert <commit>
```

---

## PR-13: Migration Runner

**Branch:** `feat/migration-runner`
**Phase:** 8
**Gaps:** G044, G045, G046

### Scope
- `scripts/vitruvius/taxonomy/migrate_to_v2.py`:
  1. **Generate:** Read old frontmatter, produce new frontmatter in `staging/`
  2. **Diff:** Show Git diff of staging vs current
  3. **Review:** Human steward reviews diff, approves/rejects
  4. **Apply:** Move staging to canonical, commit
- `scripts/vitruvius/taxonomy/rollback.py`: restores pre-migration state
- `scripts/vitruvius/taxonomy/validate_post_migration.py`: checks all nodes pass schema

### Definition of Done
- [ ] Migration runner runs without error on test copy of repo
- [ ] Diff review process documented
- [ ] Apply script is idempotent (second run produces zero changes)
- [ ] Rollback script restores pre-migration state
- [ ] All validation scripts pass post-migration
- [ ] Migration log committed to `006_System-Manifests/runs/`

### Rollback
```bash
git revert <commit>
# Manual: run scripts/vitruvius/taxonomy/rollback.py
```

---

## PR-14: Shadow Graph + Parity Check

**Branch:** `feat/shadow-graph-parity`
**Phase:** 9
**Gaps:** G047, G049, G050

### Scope
- `scripts/vitruvius/taxonomy/build_shadow_graph.py`: builds shadow graph with all new labels/properties/edges
- `scripts/vitruvius/taxonomy/parity_check.py`: compares v1 vs v2 API responses for all query patterns
- Feature flag `k_taxonomy_v2` toggles shadow read mode
- Shadow read observation period (1 week)

### Definition of Done
- [ ] Shadow graph built successfully
- [ ] Parity check passes: 100% match for all v1 query patterns
- [ ] Feature flag toggles shadow read without restart
- [ ] Shadow graph is queryable via API v2
- [ ] Parity check script runs in CI

### Rollback
```bash
git revert <commit>
# Manual: delete shadow graph labels
# Manual: set k_taxonomy_v2 = false
```

---

## PR-15: Governance Artifacts

**Branch:** `feat/governance-artifacts`
**Phase:** 10
**Gaps:** G040, G041, G042

### Scope
- `steward_runbook.md`: change process, PRD template, escalation path
- `review_queue_spec.md`: proposal format, review criteria, approval workflow
- `ai_policy.md`: AI permissions, confidence thresholds, human approval requirements
- Training data: 50 manually classified concepts for facet model calibration
- Update all plan docs (`00`–`07`) to reflect implementation reality

### Definition of Done
- [ ] All governance docs committed to `.ai/03_plans/taxonomy-governance/`
- [ ] Steward roster published
- [ ] AI policy reviewed by at least one steward
- [ ] Training data committed to `006_System-Manifests/audits/taxonomy-governance/`

### Rollback
```bash
git revert <commit>
```

---

## PR-16: Cross-Discipline Relationship Taxonomy

**Branch:** `feat/cross-discipline-relationships`
**Phase:** 3 (extends facet model), 4 (extends jurisdiction model)
**Gaps:** New — extends relationship vocabulary

### Scope
- Update `scripts/vitruvius/rules/relationship_registry.yaml` with cross-discipline predicates
- Add `primary_domain` facet type to Neo4j schema
- Add cross-discipline edge validation to `promotion_validator.py`
- Add `validate_graph.py` cycle detection for `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS`
- Add confidence thresholding rules per predicate type

### Definition of Done
- [ ] All predicates from `01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md` §2 are in registry
- [ ] `promotion_validator.py` rejects unregistered predicates
- [ ] `validate_graph.py` detects cycles in `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS`
- [ ] Unit tests for each new predicate type
- [ ] Domain pair constraint matrix is loadable by validator

### Rollback
```bash
git revert <commit>
# Manual: restore relationship_registry.yaml
```

---

## PR-17: Vitruvian Context Resolver Engine

**Branch:** `feat/vitruvian-context-resolver`
**Phase:** 6b, 11
**Gaps:** New — core IP

### Scope
- `scripts/vitruvius/resolver/` package:
  - `context_parser.py`
  - `jurisdiction_resolver.py`
  - `overlay_resolver.py`
  - `precedence_engine.py`
  - `evidence_aggregator.py`
  - `standards_mapper.py`
  - `influence_traverser.py`
  - `response_builder.py`
  - `resolver.py` — main entrypoint
- `POST /v2/resolve` API endpoint
- In-memory cache layer
- `k_vitruvian_context` feature flag

### Definition of Done
- [ ] All 8 test cases (TC-01 through TC-08) pass
- [ ] Latency <100ms for single concept, <200ms for search+resolve
- [ ] Reasoning trace present in 100% of responses
- [ ] Cache hit rate >50% for repeated queries
- [ ] No mutations to canonical nodes during resolution
- [ ] Feature flag `k_vitruvian_context` controls enablement

### Rollback
```bash
git revert <commit>
# Manual: set k_vitruvian_context = false
```

---

## PR-18: Explorer Vitruvian Context UI

**Branch:** `feat/explorer-vitruvian-context`
**Phase:** 7 (extends Explorer)
**Gaps:** New — UI for resolver

### Scope
- "Affected Disciplines" panel on node detail page
- "Why this applies" reasoning trace viewer
- "Context switcher" (change jurisdiction/date to see different resolutions)
- "Cross-discipline influence" graph visualization
- Layer badge updates: show resolved state vs canonical state

### Definition of Done
- [ ] Explorer builds without errors
- [ ] Node detail page shows affected disciplines
- [ ] Context switcher changes resolution in real-time
- [ ] Reasoning trace is human-readable
- [ ] No write operations exposed

### Rollback
```bash
git revert <commit>
```

---

## PR Dependency Graph

```
PR-00 (Bootstrap)
  │
  ▼
PR-01 (Backbone Schema) ──► PR-07 (Facet Assignment)
  │                           │
  ▼                           ▼
PR-02a (Jurisdiction Graph) ◄─┘
  │
  ▼
PR-02b (Jurisdiction Data)
  │
  ▼
PR-02c (Jurisdiction API)
  │
  ▼
PR-03 (DocEdition Separation)
  │
  ▼
PR-04 (Standards Schema) ──► PR-09 (Seed Mappings)
  │
  ▼
PR-05 (ID Generator) ──► PR-06 (HTTP Redirect)
  │
  ▼
PR-08 (PH Jurisdiction Pack)
  │
  ▼
PR-10 (Neo4j FTS) ──► PR-11 (API v2)
  │                       │
  ▼                       ▼
PR-14 (Shadow Graph)    PR-12 (Explorer Updates)
  │                       │
  ▼                       ▼
PR-13 (Migration Runner)  PR-15 (Governance)
  │
  ▼
PR-15 (Governance)
  │
  ▼
PR-16 (Cross-Discipline Edges)
  │
  ▼
PR-17 (Vitruvian Context Resolver)
  │
  ▼
PR-18 (Explorer VC UI)
```

**Critical path:** PR-00 → PR-01 → PR-07 → PR-16 → PR-02a → PR-02b → PR-02c → PR-03 → PR-08 → PR-10 → PR-11 → PR-14 → PR-13 → PR-15 → PR-17 → PR-18

---

## Merge Criteria Summary

| PR | Steward Review | Engineer Review | Parity Check | Migration Test | Rollback Verified |
|----|---------------|-----------------|-------------|---------------|-------------------|
| PR-00 | — | ✅ | — | — | ✅ |
| PR-01 | — | ✅ | — | — | ✅ |
| PR-02a | — | ✅ | — | — | ✅ |
| PR-02b | — | ✅ | — | — | ✅ |
| PR-02c | — | ✅ | — | — | ✅ |
| PR-03 | — | ✅ | — | — | ✅ |
| PR-04 | — | ✅ | — | — | ✅ |
| PR-05 | ✅ | ✅ | — | — | ✅ |
| PR-06 | — | ✅ | — | — | ✅ |
| PR-07 | ✅ | ✅ | — | — | ✅ |
| PR-08 | ✅ | ✅ | — | — | ✅ |
| PR-09 | ✅ | ✅ | — | — | ✅ |
| PR-10 | — | ✅ | — | — | ✅ |
| PR-11 | — | ✅ | ✅ | — | ✅ |
| PR-12 | — | ✅ | ✅ | — | ✅ |
| PR-13 | ✅ | ✅ | — | ✅ | ✅ |
| PR-14 | — | ✅ | ✅ | — | ✅ |
| PR-15 | ✅ | — | — | — | ✅ |
| PR-16 | ✅ | ✅ | — | — | ✅ |
| PR-17 | — | ✅ | ✅ | — | ✅ |
| PR-18 | — | ✅ | ✅ | — | ✅ |

---

## Shadow Graph + Shadow Read Milestones

Before any feature flag is enabled, the following milestones must be met:

| Milestone | PR | Evidence | Gate |
|-----------|-----|----------|------|
| Shadow graph built | PR-14 | Neo4j graph with `__shadow__` prefix labels exists | D |
| Parity check passes | PR-14 | `parity_check.py` returns 100% match | D |
| Shadow read enabled | PR-14 | `k_taxonomy_v2 = true`, API v2 reads from shadow graph | D |
| 1-week observation | PR-14 | Error rate <0.1%, no user-reported issues | D |
| Cutover approved | PR-14 | Steward + engineer sign-off | D |
| Primary graph deprecated | PR-14 (post-cutover) | After 1 month of stable shadow graph | Later |

**Critical rule:** No cutover without 1-week shadow read observation period.
