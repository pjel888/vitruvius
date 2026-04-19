# 00 — Locked Decisions

> **Scope:** Architecture decisions that are now final. Implementation agents must treat these as non-negotiable.
> **Date:** 2026-04-19
> **Authority:** `.ai/13_research/governed taxonomy/`

---

## Implementation Invariants

These invariants are hard rules. Any plan, PR, or code change that violates them must be rejected.

| # | Invariant | Rationale | Enforcement |
|---|-----------|-----------|-------------|
| I1 | The canonical backbone never forks by jurisdiction. | Jurisdiction is an applicability condition, not a subject domain. Forking the tree per country creates drift and false confidence. | Schema review + Critic agent gate |
| I2 | Old semantic IDs are never deleted. | `concept-building-permit` and all legacy slugs remain resolvable forever via the `id_redirect` table. | Migration runner idempotency check + Neo4j constraint |
| I3 | Jurisdiction-specific meaning is modeled as overlays, edges, and applicability rules—not as mutated canonical nodes. | A canonical node has one global meaning. Local obligations attach via `HAS_OVERLAY` + `APPLIES_IN`. | Schema validation: `CanonicalNode` must not contain jurisdiction-specific fields that change definition |
| I4 | API v2 is strictly additive. | Old clients (`/taxonomy`, `/search`, `/node/:id`) continue to work unchanged during transition. | Contract tests for v1 endpoints must pass on every PR |
| I5 | Rollout is shadow-first. | Build a shadow graph and shadow API reads before flipping `k_taxonomy_v2`. No direct cutover without parity checks. | Gate E (shadow graph parity) must pass before feature flag enablement |
| I6 | `DocumentVersion` (extraction artifact) and `DocumentEdition` (normative code/standard edition) are separate entities. | Collapsing them corrupts provenance. A PDF extraction is not the same as a published code edition. | Schema validation + Pydantic model separation |
| I7 | L1–L2 backbone nodes are human-locked. AI may not propose, create, or mutate them. | The top-level domain structure is editorial policy, not inference. | `taxonomy_seeding` flag + review queue + steward approval |
| I8 | L3–L4 additions may be AI-proposed, but only through the review workflow with human approval. | AI can classify into the tree, but cannot change the tree without review. | Assertion layer (`PlacementAssertion`) + review queue |
| I9 | The Vitruvian Context resolver never mutates canonical nodes. | The resolver selects and composes truth; it does not create, modify, or hallucinate rules. | All resolver Cypher is read-only; no write permissions |
| I10 | Cross-discipline edges are typed and contextual. No vague `RELATED_TO` edges between domains. | Untyped edges destroy multi-disciplinary reasoning. | `relationship_registry.yaml` + `promotion_validator.py` reject unregistered predicates |

---

## Locked Decisions

### LD-1: Backbone Source of Truth

**Decision:** `003_Canonical-Knowledge-Layer/backbone/`

**Rationale:** The six-layer architecture places canonical knowledge in Layer 3. The backbone is canonical knowledge. Placing it in `config/` would blur the layer boundary and imply it is machine-generated configuration.

**Repo impact:**
- New directory: `003_Canonical-Knowledge-Layer/backbone/`
- Files: `backbone-l1.yaml`, `backbone-l2.yaml`, `backbone-l3.yaml`, `backbone-l4.yaml` (or a single unified file)
- Validation script: `scripts/vitruvius/taxonomy/validate_backbone.py`

**Rejected alternatives:**
- `config/taxonomy/backbone/` — violates six-layer separation
- Git submodule — adds operational complexity without benefit at this scale

---

### LD-2: Canonical ID Format

**Decision:** `VTN-<kind>-<7 digits>`

**Kind values (locked):**
- `DOM` — domain (L1–L4 backbone node)
- `CON` — concept (canonical knowledge node)
- `RUL` — rule
- `DEF` — definition
- `PRO` — procedure
- `EXC` — exception
- `JUR` — jurisdiction
- `AUT` — authority
- `ADF` — authority document family
- `ADE` — authority document edition
- `APP` — applicability rule
- `OVR` — overlay
- `STD` — standard reference
- `MAP` — standard mapping
- `LOC` — localization
- `REL` — taxonomy release

**Rationale:** Opaque, sortable, collision-resistant, human-readable kind prefix. Seven digits supports 10 million IDs per kind.

**Repo impact:**
- `scripts/vitruvius/taxonomy/id_generator.py`
- `scripts/vitruvius/db/schema.sql` (`id_redirect` table)
- All new canonical nodes use this format

**Rejected alternatives:**
- Semantic slugs with redirect — slugs mutate, breaking stability
- UUID — no kind prefix, harder to debug

---

### LD-3: API Versioning

**Decision:** `/v2/` URL prefix

**Rationale:** Explicit, cache-friendly, easy to route, obvious to consumers.

**Repo impact:**
- `api/index.ts` — new routes under `/v2/`
- Old routes (`/taxonomy`, `/search`, `/node/:id`) remain at root
- v1 routes receive additive fields only (new fields old clients ignore)

**Rejected alternatives:**
- `?version=2` — pollutes query params, harder to cache
- `Accept` header — harder to debug in browser

---

### LD-4: MVP Search

**Decision:** Neo4j full-text search (`db.index.fulltext.queryNodes`) + server-side Python post-processing for facet/context ranking

**Rationale:** No new infrastructure. Neo4j 5.26 Community supports FTS. Performance is acceptable for <50k nodes. Upgrade path to external index is additive.

**Repo impact:**
- `scripts/vitruvius/kg/neo4j_schema.cypher` — `CREATE FULLTEXT INDEX canonicalSearch`
- `api/index.ts` — `/v2/search` calls FTS then ranks in Python

**Rejected alternatives:**
- Meilisearch/Typesense for MVP — adds operational complexity; evaluate only if FTS latency exceeds 200ms at scale

---

### LD-5: Runtime Storage Pattern

**Decision:** Three-tier runtime

| Tier | Technology | Responsibility |
|------|-----------|---------------|
| Editorial source of truth | Git-managed Markdown/YAML | Backbone, jurisdiction packs, standards mappings, localization sidecars |
| Graph traversal + relationship resolution | Neo4j 5.26 Community | Nodes, edges, paths, precedence resolution |
| Registry + reporting + audit | PostgreSQL 16 | `id_redirect`, `file_registry`, `review_queue`, `taxonomy_release`, jurisdiction tables |

**Rationale:** Matches existing stack. Editorial content lives in git for review/diff/rollback. Graph store handles traversal. Relational store handles tabular reporting.

**Repo impact:** No new infrastructure. Extend existing schemas.

---

### LD-6: Rollout Pattern

**Decision:** Shadow graph + shadow API reads before feature flag enablement

**Steps (locked):**
1. Build shadow Neo4j graph from migrated canonical Markdown (separate graph or separate labels)
2. Stand up `/v2/` API routes reading from shadow graph
3. Run parity checks: v1 vs v2 responses for identical queries
4. Only after parity passes, flip `k_taxonomy_v2: true`
5. Monitor for 48 hours before considering shadow graph the primary graph

**Rationale:** Prevents cutover failures. Allows rollback by flipping flag.

**Repo impact:**
- `config/vitruvius.yaml` — `k_taxonomy_v2: false` (default)
- Migration runner — writes to shadow labels first
- Parity check script — `scripts/vitruvius/taxonomy/parity_check.py`

---

### LD-7: Old ID Handling

**Decision:** Redirect table, never delete

**Rationale:** All existing URLs (`/node/concept-building-permit`), graph references, and frontmatter must remain resolvable.

**Implementation:**
- PostgreSQL table `id_redirect`:
  - `legacy_id` (PK) — e.g., `concept-building-permit`
  - `canonical_id` — e.g., `VTN-CON-000184`
  - `redirect_type` — `permanent` or `superseded`
  - `created_at`
- API v1: `/node/concept-building-permit` returns `301` or body with `canonical_id` field
- API v2: `/v2/node/VTN-CON-000184` is the canonical route

---

### LD-8: Backbone Governance

**Decision:**
- L1–L2: Human-locked. AI may not propose changes. Changes require PRD + steward approval + two-human review.
- L3–L4: AI may propose additions via `PlacementAssertion`. Auto-accept ≥0.92 confidence for single-clear leaf. Queue 0.75–0.91 for review. Reject <0.75.

**Rationale:** Prevents AI from destabilizing the global backbone while allowing it to enrich lower levels.

---

### LD-9: MVP Scope Boundary

**Decision:** v1 includes only:

1. Backbone (L1–L4)
2. Opaque IDs + redirects
3. Facet model (primary_domain, asset_scope, lifecycle_stage, knowledge_type, project_type, performance_topic)
4. Jurisdiction hierarchy
5. Authority document family + edition model
6. Standards mapping structure (schema + sample seed)
7. API v2
8. Search v2 (FTS + facet filtering)
9. Migration runner
10. Read-only Explorer updates (facet panel, jurisdiction selector, evidence panel)

**Deferred to v1.1:**
- Localization (sidecar files ready but not wired to UI)
- Project-specific overlays (schema ready, no UI)
- Review queue UI (API endpoints ready, no Explorer component)
- External search engine (Neo4j FTS only for MVP)
- Broad international standards seed pack (sample mappings only)

**Deferred to later:**
- Embedding-based semantic search
- Climate zone / hazard zone applicability rules
- Multi-language editorial UI
- Automated standards ingestion from official APIs

---

### LD-10: Home-Domain Assignment Policy

**Decision:** Cross-cutting topics are assigned to a single primary domain using tie-break rules.

**Rulebook (locked):**

| Cross-cutting topic | Primary domain | Rationale |
|--------------------|----------------|-----------|
| Accessibility | `taxonomy-accessibility` | Subject-specific L1 domain exists |
| Fire / life safety | `taxonomy-fire-life-safety` | Subject-specific L1 domain exists |
| Sustainability / energy / carbon | `taxonomy-sustainability` | Subject-specific L1 domain exists |
| Acoustics | `taxonomy-performance` | Performance aspect across domains |
| Egress / means of escape | `taxonomy-fire-life-safety` | Primary life safety concern |
| Security / hardening | `taxonomy-performance` | Risk/resilience performance aspect |
| Water efficiency | `taxonomy-sustainability` | Sustainability lens |
| Indoor environmental quality | `taxonomy-performance` | Human performance outcome |
| Seismic design | `taxonomy-structural` | Engineering discipline |
| Wind design | `taxonomy-structural` | Engineering discipline |
| Flood design | `taxonomy-civil-infrastructure` | Infrastructure discipline |
| BIM / IFC / data templates | `taxonomy-digital-delivery` | Digital delivery lens |

**Rule:** If a subject has its own L1 domain (accessibility, fire/life safety, sustainability), it lives there. If it is a performance attribute across domains, it lives in `taxonomy-performance`. If it is an engineering discipline, it lives in the relevant engineering domain. If still ambiguous, assign to `taxonomy-regulatory` as the default regulatory home.

---

## Consequences of Locked Decisions

| Decision | If violated, what breaks |
|----------|-------------------------|
| LD-1 (backbone in Layer 3) | Six-layer separation becomes meaningless; editorial content drifts into config |
| LD-2 (opaque IDs) | Links break, graph references corrupt, bookmarks die, AI classifications become unstable |
| LD-3 (`/v2/` prefix) | Cache invalidation becomes unpredictable; client confusion |
| LD-4 (Neo4j FTS MVP) | May need to revisit if node count exceeds 100k or query latency exceeds 200ms |
| LD-5 (three-tier runtime) | Editorial changes cannot be reviewed/diffed; graph and relational concerns mix |
| LD-6 (shadow-first) | Production cutover failures with no instant rollback |
| LD-7 (redirects) | All existing URLs and graph references break |
| LD-8 (L1–L2 locked) | AI corrupts global taxonomy structure; editorial governance collapses |
| LD-9 (MVP boundary) | Scope creep delays launch by months; critical path blocked |
| LD-10 (home-domain rules) | Migration review becomes subjective; same concept assigned to different domains by different reviewers |

---

### LD-11: Vitruvian Context Is Read-Only

**Decision:** The Vitruvian Context resolver is a read-only runtime layer. It never creates, modifies, or deletes nodes, edges, overlays, or rules.

**Rationale:** The resolver's power comes from selection and composition, not mutation. If the resolver can change the graph, it becomes un-auditable and its outputs become untrustworthy. All overlays, rules, and mappings must be pre-approved and pre-ingested.

**Repo impact:**
- `scripts/vitruvius/resolver/` — all modules are read-only
- Neo4j user permissions — resolver service account has `READ` only
- API endpoint `POST /v2/resolve` — validates no write operations in Cypher

**Consequence if violated:** Resolver produces phantom rules; audit trail breaks; system becomes a black box.

---

### LD-12: Cross-Discipline Edge Taxonomy Is Closed

**Decision:** Only predicates from the cross-discipline relationship taxonomy (`01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md` §2) are permitted for inter-domain edges. `RELATED_TO`, `CONNECTED_TO`, `SIMILAR_TO`, and other vague predicates are forbidden.

**Rationale:** Multi-disciplinary reasoning requires typed, directional, confidence-scored edges. Vague edges cannot answer "how does structural constrain architecture?" — they only say "these are somehow related."

**Repo impact:**
- `scripts/vitruvius/rules/relationship_registry.yaml` — extended with new predicates
- `promotion_validator.py` — rejects unregistered predicates
- `validate_graph.py` — detects cycles in `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS`
- Migration script — retypes or flags all existing `RELATED_TO` inter-domain edges

**Consequence if violated:** Graph becomes unreadable by machines; Explorer UI cannot render meaningful cross-discipline panels; AI cannot reason across domains.

---

## Who Can Override

Only the founder/architect can override a locked decision. Overrides require:
1. Written ADR update
2. Impact analysis on all dependent PRs
3. State reconciliation in `milestone-tracker.md`
