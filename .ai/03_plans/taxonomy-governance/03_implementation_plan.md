# 03 — Implementation Plan: Taxonomy Governance

> **Scope:** Phased build of the governed global AEC taxonomy architecture.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `01_codebase_audit.md`, `02_readiness_plan.md`

---

## Implementation Invariants

These invariants are non-negotiable for every phase. Any phase that violates an invariant must be rejected.

1. **Backbone never forks by jurisdiction.** The L1–L3 backbone is a single global subject taxonomy. Jurisdiction-specific obligations are overlays, not backbone branches.
2. **Old IDs are never deleted.** All existing semantic slugs remain resolvable. They map to new opaque `VTN-*` IDs via the `id_redirect` table and graph edges.
3. **Canonical nodes remain globally meaningful.** No jurisdiction-specific meaning is stored inside `CanonicalNode`. Regulatory context is stored in `AuthorityDocumentEdition` + `Overlay` + `ApplicabilityRule`.
4. **DocumentVersion ≠ DocumentEdition.** `DocumentVersion` is for extraction artifacts (PDF → Markdown). `AuthorityDocumentEdition` is for normative code/standard editions. They are separate entities with separate lifecycles.
5. **API v2 is additive only.** No v1 endpoint is modified, deprecated, or removed. v2 endpoints are new paths or new query params.
6. **Shadow-read before cutover.** Every new data path is built in a shadow graph / shadow read first. Cutover only happens after parity checks pass.
7. **Human-locked L1–L2, AI-proposable L3–L4.** Only humans modify backbone nodes ≤L2. AI may propose L3–L4 additions through the review queue.
8. **No breaking changes without a migration runner.** Every schema or ID change is accompanied by an idempotent migration script and a rollback script.

---

## Phase Summary

| Phase | Name | Duration | Owner | Deliverable |
|-------|------|----------|-------|-------------|
| 0 | Schema + Infrastructure | 1–2 weeks | Backend | Schema files, indexes, feature flags |
| 1 | Backbone Design + Lock | 2–3 weeks | Editorial | `backbone-l1.yaml`, `backbone-l2.yaml`, `steward_roster.md` |
| 2 | ID Migration + Redirects | 1–2 weeks | Data | `id_redirect` table, opaque ID generator, parity tests |
| 3 | Facet Model + Classification | 1–2 weeks | Data | `knowledge_type`, `asset_scope`, `lifecycle_stage`, `project_type`, `performance_topic` fields assigned to all concepts; cross-discipline edge stubs |
| 11 | Vitruvian Context Runtime | 1–2 weeks | Backend | Resolver engine, `POST /v2/resolve`, cross-discipline influence traversal, cache layer |
| 4 | Jurisdiction Model + Packs | 1–2 weeks | Backend | `Jurisdiction`, `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition`, `ApplicabilityRule`, `Overlay` models; PH pack extracted |
| 5 | Standards Mapping | 1 week | Backend | `StandardReference`, `StandardMapping`, `maps_to_standard` edges; seed mappings |
| 6 | API v2 + Search v2 | 1–2 weeks | Backend | New endpoints, Neo4j FTS, facet filtering, jurisdiction resolution |
| 7 | Explorer Read-Only Updates | 1 week | Frontend | Facet panel, jurisdiction selector, layer badges, tree rendering |
| 8 | Migration Runner + Backfill | 1–2 weeks | Data | Idempotent migration script, rollback script, validation suite |
| 9 | Shadow Graph + Parity | 1 week | Backend | Shadow graph build, parity check, feature flag cutover |
| 10 | Governance + Validation | 1 week | Governance | Steward runbook, review queue spec, AI policy, training data |
| 11 | Vitruvian Context Runtime | 1–2 weeks | Backend | Resolver engine (`scripts/vitruvius/resolver/`), `POST /v2/resolve`, cross-discipline influence traversal, cache layer, reasoning trace |

**Critical path:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 8 → 9 → 10 → 11

---

## Phase 0: Schema + Infrastructure (Week 1–2)

### Acceptance Criteria
1. All new Pydantic models pass `mypy`.
2. All new Neo4j indexes are created by a single Cypher script.
3. All new PostgreSQL tables are created by a single SQL script.
4. All new TypeScript types pass `tsc --noEmit`.
5. Feature flags are wired to `config/vitruvius.yaml` and readable by the pipeline.

### MVP Scope
- `CanonicalNode` extended with: `canonical_id`, `path_code`, `primary_domain`, `knowledge_type`, `asset_scope`, `lifecycle_stage`, `project_type`, `performance_topic`, `release_version`, `steward`
- `BackboneNode` model with: `canonical_id`, `path_code`, `level`, `parent_path_code`, `pref_label`, `definition`, `aliases`, `scope_note`, `steward`
- `IdRedirect` model with: `old_id`, `new_id`, `scope`, `reason`, `redirect_type` (`permanent`/`temporary`)
- `FacetEnum` models for each facet dimension
- Neo4j: add `BackboneNode` label, facet property indexes, `canonicalSearch` FTS index
- PostgreSQL: add `id_redirect`, `taxonomy_release` tables
- TypeScript: extend `GraphNode`, add `FacetFilter`, `ResolvedContext`

### v1.1 Scope
- `Localization` model + PostgreSQL table
- `ProjectOverlay` model + PostgreSQL table

### Later Scope
- Composite facet validation (cross-field rules)
- AI-suggested facet values (confidence-scored)

### Rollback
- Drop new Neo4j indexes and labels (migration script reversible)
- Drop new PostgreSQL tables (migration script reversible)
- Remove feature flags from config

---

## Phase 1: Backbone Design + Lock (Week 3–5)

### Acceptance Criteria
1. `backbone-l1.yaml` contains exactly 15 L1 domains with definitions, stewards, and scope notes.
2. `backbone-l2.yaml` contains all L2 nodes with valid parent references.
3. `steward_roster.md` assigns a human owner to every L1–L2 node.
4. `validate_backbone.py` passes with zero errors.
5. Git tag `backbone-v1.0.0` is created.
6. No AI tool has modified any L1–L2 node.

### MVP Scope
- Author 15 L1 domains (see §6 Home-Domain Assignment Rulebook)
- Author L2 depth (typically 3–6 nodes per L1)
- L3 stubs with TODO markers
- L4 stubs with TODO markers
- Validation script: uniqueness, parentage, path code format, steward presence

### v1.1 Scope
- Author L3–L4 depth (AI may propose; human must approve)
- Add cross-reference edges (`RELATED_TO_DOMAIN`)
- Add `scope_note` and `example_concepts` fields

### Later Scope
- Backbone change log
- Steward change process (PRD + review queue)
- Cross-domain review for edge cases

### Rollback
- Revert Git commits on `003_Canonical-Knowledge-Layer/backbone/`
- Validation failure blocks any downstream phase

---

## Phase 2: ID Migration + Redirects (Week 5–7)

### Acceptance Criteria
1. `id_redirect` table contains a mapping for every existing semantic slug.
2. Opaque ID generator produces unique `VTN-*` IDs with zero collisions in 10k samples.
3. API v1 returns `canonical_id` field alongside old `id` for all nodes.
4. API v2 resolves `VTN-*` IDs correctly.
5. Old semantic slugs return HTTP 308 Permanent Redirect to new canonical URLs.
6. Parity check: v1 and v2 return identical core data for every existing node.

### MVP Scope
- `id_generator.py`: deterministic, seeded, collision-free
- `id_redirect` population script: maps ~105 concepts, ~340 sources
- Neo4j: add `canonical_id` property to existing nodes
- API v1: add `canonical_id` to response (additive)
- API v2: new route `GET /v2/node/:canonical_id`
- HTTP 308 redirect handler for old URLs

### v1.1 Scope
- Bulk redirect import for new jurisdictions
- Redirect analytics (track 308 hits)

### Later Scope
- AI-assisted ID reconciliation during new jurisdiction onboarding

### Rollback
- `rollback_ids.py`: remove `canonical_id` properties, clear `id_redirect` table, remove 308 handler

---

## Phase 3: Facet Model + Classification (Week 7–9)

### Acceptance Criteria
1. Every concept node has non-null values for all 6 facet fields.
2. Facet assignments are stored in Neo4j properties and Markdown frontmatter.
3. `validate_facets.py` passes: no nulls, no unknown values, cross-field rules satisfied.
4. Search v1 continues to work (facet fields are additive; no breaking changes).
5. Home-domain assignment rulebook (§6) is applied correctly.

### MVP Scope
- `knowledge_type`: concept, rule, definition, procedure, exception, principle
- `asset_scope`: building, infrastructure, site, system, component, material
- `lifecycle_stage`: planning, design, construction, operation, demolition, reuse
- `project_type`: residential, commercial, industrial, institutional, public_works, mixed_use
- `performance_topic`: structural, fire_life_safety, accessibility, sustainability, energy, acoustics, daylight, ventilation, water, durability
- `primary_domain`: assigned from backbone (15 domains)
- Cross-discipline edge stubs: `primary_domain`, `BELONGS_TO_DOMAIN`, `USED_IN`, `CONSTRAINS`, `AFFECTS`, `REQUIRES`, `INFLUENCES`, `EXECUTED_IN`, `REGULATED_BY`
- Assignment: AI-assisted bulk classification with human review

### v1.1 Scope
- `localization` facet (language, region variant)
- AI-suggested facet values with confidence scores
- Facet change audit trail

### Later Scope
- Cross-cutting subjects: accessibility, fire/life safety, sustainability, acoustics, energy, resilience, egress — home-domain assignment rulebook enforcement
- Composite facet rules (e.g., `lifecycle_stage=construction` → `project_type` cannot be `operation`)

### Rollback
- `rollback_facets.py`: remove facet properties from Neo4j, revert frontmatter changes

---

## Phase 4: Jurisdiction Model + Packs (Week 9–11)

### Acceptance Criteria
1. `Jurisdiction` model supports hierarchical codes (`PH`, `PH-MetroManila`, `PH-MetroManila-Makati`).
2. `AuthorityDocumentEdition` model supports normative editions with effective date, repeal date, and supersession chain.
3. Philippine rules are extracted into `config/jurisdictions/PH.yaml`.
4. `ApplicabilityRule` engine resolves jurisdiction precedence correctly.
5. Overlay nodes are created for all Philippine regulatory obligations.
6. No jurisdiction-specific meaning is stored in `CanonicalNode`.

### MVP Scope
- Models: `Jurisdiction`, `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition`, `ApplicabilityRule`, `Overlay`
- PostgreSQL tables for all models
- Neo4j labels and edges: `Jurisdiction`, `AuthorityDocumentEdition`, `APPLIES_IN`, `HAS_OVERLAY`, `WITHIN_JURISDICTION`, `SUPERSEDES`
- Extract Philippine rules from `canonical_rules.yaml` into `config/jurisdictions/PH.yaml`
- Jurisdiction precedence resolver: `local > regional > national`
- `POST /v2/resolve` endpoint for jurisdiction-aware context

### v1.1 Scope
- Additional jurisdiction packs (e.g., `US-IBC`, `EU-Eurocode`)
- Project-specific overlays
- Temporal queries (`effective_on` date)

### Later Scope
- Full international standards seed pack
- Automated jurisdiction pack generation from legal databases

### Rollback
- `rollback_jurisdiction.py`: remove jurisdiction nodes, edges, and PostgreSQL rows

---

## Phase 5: Standards Mapping (Week 11–12)

### Acceptance Criteria
1. `StandardReference` nodes exist for 5+ standards systems (e.g., OmniClass, Uniclass, IFC, MasterFormat, ICC).
2. `StandardMapping` edges connect canonical nodes to standard codes with confidence scores.
3. `GET /v2/standards?system=OmniClass&code=...` returns mappings.
4. No canonical node meaning depends on a standard mapping.

### MVP Scope
- `StandardReference` model: `system`, `code`, `title`, `url`, `version`
- `StandardMapping` model: `canonical_id`, `standard_id`, `mapping_type`, `confidence`, `mapped_by`
- Seed 20+ sample mappings for Philippine building codes
- Neo4j edges: `MAPS_TO_STANDARD`
- API endpoint: `GET /v2/standards`

### v1.1 Scope
- Bulk import from standards CSVs
- Confidence threshold filtering
- Mapping review queue

### Later Scope
- Automated standards alignment from IFC/COBie exports
- Cross-standard equivalence (e.g., OmniClass ↔ Uniclass)

### Rollback
- `rollback_standards.py`: remove `StandardReference` nodes and `MAPS_TO_STANDARD` edges

---

## Phase 6: API v2 + Search v2 (Week 12–14)

### Acceptance Criteria
1. All v2 endpoints are contract-tested.
2. Neo4j FTS index returns results in <200ms for 10k-node graph.
3. Facet filtering returns correct subsets.
4. Jurisdiction resolution returns correct overlays.
5. v1 endpoints pass regression tests.

### MVP Scope
- `GET /v2/taxonomy` — governed backbone tree
- `GET /v2/search?q=...&facets=...&jurisdiction=...&date=...&expand_domains=...`
- `GET /v2/node/:id` — facets, mappings, provenance, related nodes, cross-discipline influences
- `POST /v2/resolve` — **Vitruvian Context resolver**: jurisdiction-aware context resolution with reasoning trace
- `GET /v2/jurisdiction/:code` — jurisdiction chain + applicable documents
- `GET /v2/standards?system=...&code=...`
- Neo4j FTS index `canonicalSearch`

### v1.1 Scope
- Semantic search (embeddings)
- Autocomplete endpoint
- Search analytics

### Later Scope
- GraphQL endpoint
- Federated search across multiple knowledge graphs

### Rollback
- Remove v2 route handlers
- Drop FTS index

---

## Phase 7: Explorer Read-Only Updates (Week 13–14)

### Acceptance Criteria
1. Explorer renders facet badges on node detail pages.
2. Explorer shows jurisdiction selector in search bar.
3. Explorer displays layer badges (canonical vs overlay vs evidence).
4. Taxonomy tree continues to work (backward-compatible rendering).
5. No write operations are exposed in UI.

### MVP Scope
- `FacetPanel` component
- `JurisdictionSelector` component
- `LayerBadge` component
- Updated `GraphNode` type usage
- Read-only node detail page with facets, overlays, and standards mappings

### v1.1 Scope
- Review queue UI (read-only view of pending proposals)
- Localization toggle
- Search filter UI for facets

### Later Scope
- Backbone editing UI (steward-only)
- Overlay editing UI (authority-specific)

### Rollback
- Revert `explorer/src/` commits

---

## Phase 8: Migration Runner + Backfill (Week 14–16)

### Acceptance Criteria
1. Migration runner transforms all ~105 concepts and ~340 sources.
2. Output is written to staging directory; human reviews diff.
3. Diff review is approved by at least one steward.
4. Apply script is idempotent: second run produces zero changes.
5. Rollback script restores pre-migration state.
6. All validation scripts pass post-migration.

### MVP Scope
- `migrate_to_v2.py`: reads old frontmatter, writes new frontmatter
- Staging directory: `003_Canonical-Knowledge-Layer/staging/`
- Diff review: Git diff of staging vs current
- Apply script: moves staging to canonical
- Rollback script: restores from Git backup branch
- Validation: `validate_backbone.py`, `validate_facets.py`, `parity_check.py`

### v1.1 Scope
- Incremental migration (only changed nodes)
- Migration analytics (time, error rate, human review time)

### Later Scope
- Automated migration scheduling
- Migration dry-run reporting

### Rollback
- Run `rollback.py` + restore Git branch

---

## Phase 9: Shadow Graph + Parity (Week 16–17)

### Acceptance Criteria
1. Shadow graph is built with all new labels/properties/edges.
2. Parity check passes: v1 query results == v2 query results for all existing query patterns.
3. Feature flag `k_taxonomy_v2` can be toggled without restart.
4. Shadow read mode: v2 routes read from shadow graph, v1 from primary graph.
5. Cutover is reversible within 5 minutes.

### MVP Scope
- Shadow graph: Neo4j graph with `__shadow__` prefix on labels
- Parity check script: compares all v1 vs v2 API responses
- Feature flag integration: `k_taxonomy_v2` toggles shadow read
- Cutover: atomic switch (transactional)
- Rollback: revert to primary graph within 5 minutes

### v1.1 Scope
- Gradual rollout (canary by user segment)
- Real-time parity monitoring

### Later Scope
- Multi-shadow support (A/B testing new schema versions)

### Rollback
- Toggle `k_taxonomy_v2` to `false`
- Delete shadow graph labels

---

## Phase 10: Governance + Validation (Week 17–18)

### Acceptance Criteria
1. Steward runbook is published.
2. Review queue spec is implemented.
3. AI policy document is committed.
4. Training data for facet classification is curated.
5. All documentation (`00_locked_decisions.md` through `07_golden_example.md`) is updated to reflect implementation reality.

### MVP Scope
- `steward_runbook.md`: change process, PRD template, escalation path
- `review_queue_spec.md`: proposal format, review criteria, approval workflow
- `ai_policy.md`: what AI can propose, what requires human approval, confidence thresholds
- Training data: 50 manually classified concepts for facet model calibration
- Documentation update: all plan docs synced with implementation

### v1.1 Scope
- Automated review queue metrics
- Steward rotation process
- AI policy compliance checker

### Later Scope
- Governance dashboard
- Cross-jurisdiction coordination process

### Rollback
- N/A (governance artifacts are additive)

---

## Phase 11: Vitruvian Context Runtime (Week 18–20)

### Acceptance Criteria
1. `POST /v2/resolve` returns `ResolvedTruth` with reasoning trace for all test cases (TC-01 through TC-08).
2. Resolver latency <100ms for single concept, <200ms for search+resolve (benchmarked).
3. Cache hit rate >50% for repeated queries after 1 week.
4. No canonical node mutations during resolution (audit verified).
5. Cross-discipline influence traversal returns typed, confidence-scored edges.
6. Feature flag `k_vitruvian_context` gates all resolver functionality.

### MVP Scope
- `scripts/vitruvius/resolver/` package with 8 modules:
  - `context_parser.py` — parses `ResolutionContext`
  - `jurisdiction_resolver.py` — builds jurisdiction chain
  - `overlay_resolver.py` — selects applicable overlays by precedence
  - `precedence_engine.py` — applies jurisdiction + temporal + standards precedence
  - `evidence_aggregator.py` — gathers `SUPPORTED_BY` evidence spans
  - `standards_mapper.py` — resolves `MAPS_TO_STANDARD` edges
  - `influence_traverser.py` — cross-discipline edge traversal (`CONSTRAINS`, `AFFECTS`, etc.)
  - `response_builder.py` — assembles `ResolvedTruth` with reasoning trace
  - `resolver.py` — main `resolve()` entrypoint
- `POST /v2/resolve` API endpoint
- In-memory cache layer for common resolutions (TTL: 1 hour)
- `k_vitruvian_context` feature flag

### v1.1 Scope
- Redis cache backend
- Project-specific overlay resolution
- Batch resolution API (resolve multiple concepts in one call)
- Resolver analytics (query patterns, cache hit rates, latency percentiles)

### Later Scope
- GraphQL resolver endpoint
- Real-time resolver monitoring dashboard
- AI-assisted query expansion (suggest related concepts via influence graph)

### Rollback
- `k_vitruvian_context = false`
- Remove resolver route handlers
- Clear resolver cache

---

## Shadow-First Rollout

Every phase that touches the runtime graph must follow this pattern:

```
1. Build shadow graph (new labels/properties/edges in parallel)
2. Run parity check (v1 vs shadow)
3. If parity fails: fix, rebuild, recheck
4. If parity passes: enable shadow-read for v2 routes (feature flag)
5. Monitor for 1 week (error rate, latency, user reports)
6. If stable: cut over (v2 reads from shadow graph)
7. Keep primary graph for 1 month as fallback
8. If no issues: deprecate primary graph labels
```

**Critical rule:** No phase cuts over without passing parity checks and a 1-week shadow-read observation period.

---

## Home-Domain Assignment Rulebook

Cross-cutting subjects must be assigned to a single home domain in the backbone. This prevents duplicate concept nodes and ensures search predictability.

| Subject | Home Domain | Rationale | Example |
|---------|-------------|-----------|---------|
| Accessibility | `taxonomy-accessibility` | Subject-specific domain exists | Ramps, tactile paving |
| Fire / Life Safety | `taxonomy-fire-life-safety` | Subject-specific domain exists | Sprinklers, egress paths |
| Sustainability | `taxonomy-sustainability` | Subject-specific domain exists | LEED, green materials |
| Acoustics | `taxonomy-performance` | Performance aspect of multiple domains | STC ratings, noise isolation |
| Energy | `taxonomy-performance` | Performance aspect of multiple domains | U-value, HVAC efficiency |
| Resilience | `taxonomy-structural` or `taxonomy-sustainability` | Depends on hazard type | Seismic, flood, wind |
| Egress | `taxonomy-fire-life-safety` | Primary life safety concern | Exit width, travel distance |

**Rule:** If a subject has its own L1 domain (accessibility, fire/life safety, sustainability), it lives there. If it is a performance attribute across domains, it lives in `taxonomy-performance`.

**Facet, not backbone:** A concept's applicability across domains is expressed via `performance_topic` facet, not by duplicating the concept in multiple backbone branches.

---

## DocumentVersion vs DocumentEdition Separation

| Aspect | DocumentVersion | AuthorityDocumentEdition |
|--------|-----------------|------------------------|
| **Purpose** | Tracks extraction artifact (PDF → Markdown) | Tracks normative code/standard edition |
| **Properties** | `sha256`, `source_path`, `extraction_method`, `extracted_at` | `edition_number`, `effective_date`, `repeal_date`, `supersedes`, `jurisdiction`, `authority` |
| **Lifecycle** | Created on every PDF conversion | Created on every code/standard release |
| **Mutability** | Immutable (new conversion = new version) | Immutable (new edition = new node) |
| **Relationship** | `EXTRACTED_FROM` → source file | `HAS_EDITION` → `AuthorityDocumentFamily` |
| **Example** | "BP 344 PDF converted to Markdown on 2025-03-01" | "BP 344, 2009 Edition, effective 2009-04-15" |

**Implementation:**
- Preserve existing `DocumentVersion` nodes and properties.
- Create new `AuthorityDocumentEdition` label in Neo4j.
- Create new `AuthorityDocumentFamily` label (e.g., "National Building Code of the Philippines").
- Link `AuthorityDocumentEdition` → `AuthorityDocumentFamily` via `HAS_EDITION`.
- Link `CanonicalNode` → `AuthorityDocumentEdition` via `SUPPORTED_BY` (evidence) and `APPLIES_IN` + `HAS_OVERLAY` (jurisdiction-specific obligation).

---

## MVP vs v1.1 vs Later

### MVP (Must Have for First Release)
- Backbone (L1–L2 frozen, L3–L4 stubs)
- Opaque IDs + redirect table
- Facet model (6 facets assigned to all concepts)
- Jurisdiction model (hierarchy + PH pack + precedence resolver)
- Authority document family/edition model
- Standards mapping structure (5+ systems, 20+ mappings)
- API v2 (all endpoints)
- Search v2 (Neo4j FTS + facet filtering)
- Migration runner (idempotent + rollback)
- Shadow graph + parity checks
- Read-only Explorer updates (facets, jurisdiction, layer badges)
- Governance artifacts (steward runbook, AI policy, review queue spec)
- Vitruvian Context resolver (`POST /v2/resolve`, reasoning trace, cross-discipline influence traversal)

### v1.1 (Next Quarter)
- Localization (language, region variant)
- Project-specific overlays
- Review queue UI (read-only)
- Semantic search (embeddings)
- Additional jurisdiction packs (US-IBC, EU-Eurocode)
- Bulk standards import
- AI-suggested facet values with confidence scores
- Search analytics

### Later (Backlog)
- Full international standards seed pack
- GraphQL endpoint
- Federated search
- Multi-shadow A/B testing
- Automated jurisdiction pack generation
- Backbone change log with full audit trail
- Cross-jurisdiction coordination process
- Governance dashboard
