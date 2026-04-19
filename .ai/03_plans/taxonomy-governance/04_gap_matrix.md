# 04 — Gap Matrix: Current State → Target State

> **Scope:** Tabulated inventory of every gap between current taxonomy implementation and the governed global AEC taxonomy architecture.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `01_codebase_audit.md`, `02_readiness_plan.md`

---

## Legend

| Column | Meaning |
|--------|---------|
| **Gap ID** | Unique identifier (G001–G999) |
| **Category** | Content, Schema, API, UI, Search, Governance, Migration, Infrastructure |
| **Locked Decision** | Which locked decision (D1–D10) this gap is constrained by |
| **MVP / v1.1 / Later** | When this gap must be closed |
| **Layer** | Canonical (backbone), Overlay (jurisdiction/rules), Runtime (API/search/UI) |
| **Current State** | What exists today |
| **Target State** | What must exist |
| **Effort** | Estimated size (XS = <1 day, S = 1–3 days, M = 1 week, L = 2+ weeks, XL = 1+ month) |
| **Owner** | Responsible role |
| **Blocking** | Which downstream work is blocked until this gap is closed |

---

## Backbone

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G001 | Content | D1 | MVP | Canonical | Shallow 3-level taxonomy (12 taxonomies → 24 topics → 55 subtopics) | 15 L1 domains with L2–L4 depth, governed backbone | L | Editorial | Facet assignment, API v2 tree, Explorer rendering |
| G002 | Content | D1 | MVP | Canonical | No backbone versioning | Git-tagged backbone releases (semver) | S | Editorial | Change tracking, migration baseline |
| G003 | Content | D1 | MVP | Canonical | No steward assignment | Every L1–L2 node has assigned human steward | S | Governance | Change control, review queue |
| G004 | Content | D1 | v1.1 | Canonical | L3–L4 nodes mixed (human + AI) | L3–L4 AI-proposable via review queue | M | Data | AI policy, review queue spec |
| G005 | Content | D10 | MVP | Canonical | No home-domain assignment rulebook | Cross-cutting subjects assigned to single home domain | S | Editorial | Duplicate prevention, search predictability |

## IDs + Redirects

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G006 | Schema | D3 | MVP | Canonical | Semantic slug IDs (`concept-building-permit`) | Opaque `VTN-*` IDs with redirect table | M | Data | All runtime references, API contracts, UI URLs |
| G007 | Schema | D3 | MVP | Runtime | No `id_redirect` table | PostgreSQL `id_redirect` table + graph edges | S | Backend | Old ID resolution, migration runner |
| G008 | Schema | D3 | MVP | Runtime | No HTTP redirect for old IDs | 308 Permanent Redirect from old slugs to new IDs | XS | Backend | SEO, bookmark preservation |

## Facets

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G009 | Schema | D2 | MVP | Canonical | No facet model | 6 facets: `knowledge_type`, `asset_scope`, `lifecycle_stage`, `project_type`, `performance_topic`, `primary_domain` | M | Data | Search v2 filtering, Explorer facet panel |
| G010 | Content | D2 | MVP | Canonical | No facet assignments on ~105 concepts | All concepts have validated facet values | M | Data | Search accuracy, Explorer filtering |
| G011 | Schema | D2 | v1.1 | Canonical | No confidence scoring for facet values | AI-proposed facets with confidence + review queue | M | Data | AI-assisted classification |
| G012 | Schema | D2 | Later | Canonical | No cross-field facet rules | Composite validation (e.g., `lifecycle_stage=construction` → `project_type` cannot be `operation`) | S | Backend | Data quality |

## Jurisdiction + Overlay

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G013 | Schema | D4, D7 | MVP | Overlay | No jurisdiction entity | `Jurisdiction` model with hierarchical codes | S | Backend | Applicability rules, API v2 resolution |
| G014 | Schema | D4, D7 | MVP | Overlay | No authority model | `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition` models | M | Backend | Document lifecycle, supersession |
| G015 | Schema | D4, D7 | MVP | Overlay | No applicability rules | `ApplicabilityRule` engine with precedence resolver | M | Backend | Jurisdiction resolution, overlay creation |
| G016 | Content | D7 | MVP | Overlay | Jurisdiction implicit (folder paths, source IDs) | Explicit jurisdiction packs (YAML per jurisdiction) | M | Data | Multi-jurisdiction support |
| G017 | Schema | D7 | MVP | Overlay | `regulatory_basis` inside concept frontmatter | `SUPPORTED_BY` edges + `Overlay` nodes + `ApplicabilityRule` | M | Data | Separation of canonical and local meaning |
| G018 | Schema | D4 | v1.1 | Overlay | No project-specific overlays | `ProjectOverlay` model for custom rules | M | Backend | Project-specific governance |
| G019 | Schema | D7 | v1.1 | Overlay | No temporal queries | `effective_on` date parameter for edition resolution | S | Backend | Historical compliance checking |

## DocumentVersion vs DocumentEdition

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G020 | Schema | D6 | MVP | Canonical | `DocumentVersion` conflates extraction artifact with normative edition | Separate `DocumentVersion` (artifact) and `AuthorityDocumentEdition` (normative) | S | Backend | Edition lifecycle, supersession |
| G021 | Schema | D6 | MVP | Canonical | No edition supersession model | `SUPERSEDES` / `SUPERSEDED_BY` edges between editions | XS | Backend | Historical compliance |
| G022 | Schema | D6 | MVP | Canonical | No `AuthorityDocumentFamily` | Family node grouping all editions of a single code/standard | XS | Backend | Document discovery |

## Standards

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G023 | Schema | D5 | MVP | Overlay | No standards mapping model | `StandardReference` + `StandardMapping` models | S | Backend | Crosswalk queries |
| G024 | Content | D5 | MVP | Overlay | No standards mappings in data | 20+ seed mappings (OmniClass, Uniclass, IFC, MasterFormat, ICC) | S | Data | Search v2 standards endpoint |
| G025 | Schema | D5 | v1.1 | Overlay | No confidence thresholding | `confidence` field on `StandardMapping` + filter | XS | Backend | Mapping quality |
| G026 | Content | D5 | Later | Overlay | No bulk standards import | CSV/JSON import for standard mappings | M | Data | Scale |

## Search

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G027 | Infrastructure | D9 | MVP | Runtime | No dedicated search index | Neo4j full-text index `canonicalSearch` | S | Backend | Search v2 performance |
| G028 | API | D9 | MVP | Runtime | Substring `CONTAINS` search | FTS + facet filtering + jurisdiction ranking | M | Backend | Search v2 UX |
| G029 | API | D9 | v1.1 | Runtime | No semantic search | Vector similarity search (embeddings) | L | Backend | Advanced search |
| G030 | API | D9 | v1.1 | Runtime | No autocomplete | Prefix + fuzzy autocomplete endpoint | S | Backend | Search UX |

## API

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G031 | API | D8 | MVP | Runtime | No API v2 endpoints | `/v2/taxonomy`, `/v2/search`, `/v2/node/:id`, `/v2/resolve`, `/v2/jurisdiction/:code`, `/v2/standards` | M | Backend | Explorer v2, external consumers |
| G032 | API | D8 | MVP | Runtime | v1 endpoints may not be backward-compatible | v1 endpoints are additive-only; no breaking changes | S | Backend | Client stability |
| G033 | API | D8 | v1.1 | Runtime | No GraphQL endpoint | GraphQL for flexible queries | L | Backend | Developer experience |

## UI / Explorer

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G034 | UI | D8 | MVP | Runtime | Hardcoded 8 node types | Dynamic node type rendering from `knowledge_type` + `primary_domain` | M | Frontend | Explorer flexibility |
| G035 | UI | D8 | MVP | Runtime | Hardcoded 7 edge types | Dynamic edge type rendering from graph metadata | S | Frontend | Explorer flexibility |
| G036 | UI | D1 | MVP | Runtime | No facet panel | `FacetPanel` component showing 6 facets | S | Frontend | Facet discovery |
| G037 | UI | D7 | MVP | Runtime | No jurisdiction selector | `JurisdictionSelector` component | S | Frontend | Jurisdiction-aware search |
| G038 | UI | D1 | MVP | Runtime | No layer badges | `LayerBadge` component (canonical / overlay / evidence) | XS | Frontend | Content trust visualization |
| G039 | UI | D8 | v1.1 | Runtime | No review queue UI | Read-only view of pending proposals | M | Frontend | Governance visibility |

## Governance

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G040 | Governance | D1 | MVP | Canonical | No steward runbook | `steward_runbook.md` with change process | S | Governance | Change control |
| G041 | Governance | D1 | MVP | Canonical | No review queue spec | `review_queue_spec.md` with proposal format + criteria | S | Governance | AI-proposable L3–L4 |
| G042 | Governance | D1 | MVP | Canonical | No AI policy | `ai_policy.md` defining AI permissions and confidence thresholds | S | Governance | AI-assisted classification |
| G043 | Governance | D1 | v1.1 | Canonical | No governance dashboard | Metrics: proposal count, review time, steward activity | L | Governance | Operational visibility |

## Migration

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G044 | Migration | D3 | MVP | Runtime | No migration runner | `migrate_to_v2.py`: generate → diff → review → apply | M | Data | Content cutover |
| G045 | Migration | D3 | MVP | Runtime | No rollback script | `rollback.py` restores pre-migration state | S | Data | Risk mitigation |
| G046 | Migration | D2 | MVP | Runtime | No staging directory | `003_Canonical-Knowledge-Layer/staging/` for diff review | XS | Data | Safe migration |
| G047 | Migration | D3 | MVP | Runtime | No parity check | `parity_check.py` compares v1 vs v2 for all query patterns | M | Backend | Shadow graph validation |

## Infrastructure

| Gap ID | Category | Locked Decision | MVP / v1.1 / Later | Layer | Current State | Target State | Effort | Owner | Blocking |
|--------|----------|----------------|-------------------|-------|---------------|--------------|--------|-------|----------|
| G048 | Infrastructure | D8 | MVP | Runtime | No feature flags for taxonomy v2 | `k_taxonomy_v2`, `k_jurisdictional_overrides`, `k_standards_mapping` in `config/vitruvius.yaml` | XS | Backend | Gated rollout |
| G049 | Infrastructure | D9 | MVP | Runtime | No shadow graph support | Shadow graph build + shadow read mode | M | Backend | Risk-free cutover |
| G050 | Infrastructure | D9 | MVP | Runtime | No parity monitoring | Parity check + alerting | S | Backend | Cutover confidence |

---

## Gap Summary by Phase

| Phase | Gaps Closed | Total Effort |
|-------|------------|--------------|
| 0 — Schema + Infrastructure | G048, G049, G050, G027 | M |
| 1 — Backbone Design + Lock | G001, G002, G003, G005 | L |
| 2 — ID Migration + Redirects | G006, G007, G008 | M |
| 3 — Facet Model + Classification | G009, G010, G012 | M |
| 4 — Jurisdiction Model + Packs | G013, G014, G015, G016, G017, G020, G021, G022 | L |
| 5 — Standards Mapping | G023, G024 | S |
| 6 — API v2 + Search v2 | G028, G031, G032 | M |
| 7 — Explorer Read-Only Updates | G034, G035, G036, G037, G038 | M |
| 8 — Migration Runner + Backfill | G044, G045, G046 | M |
| 9 — Shadow Graph + Parity | G047 | M |
| 10 — Governance + Validation | G040, G041, G042 | S |
| **v1.1** | G004, G011, G018, G019, G025, G029, G030, G033, G039, G043 | XL |
| **Later** | G026 | M |

---

## Gap Dependency Graph

```
G001 (Backbone) ──► G009 (Facets) ──► G010 (Facet assignments)
  │                     │                  │
  │                     ▼                  ▼
  │               G031 (API v2) ◄─── G028 (Search)
  │                     │                  │
  │                     ▼                  ▼
  │               G034 (Explorer) ◄─ G036, G037, G038
  │
  ▼
G006 (Opaque IDs) ──► G007 (Redirects) ──► G044 (Migration)
  │                     │                      │
  │                     ▼                      ▼
  │               G008 (308 redirect)    G045 (Rollback)
  │                                          │
  │                                          ▼
  │                                    G047 (Parity)
  │                                          │
  │                                          ▼
  │                                    G049 (Shadow graph)
  │
  ▼
G013 (Jurisdiction) ──► G014 (Authority docs) ──► G015 (Applicability)
  │                       │                        │
  │                       ▼                        ▼
  │                 G020 (DocEdition)          G017 (Overlay)
  │                       │                        │
  │                       ▼                        ▼
  │                 G021 (Supersession)      G016 (PH pack)
  │
  ▼
G023 (Standards) ──► G024 (Mappings)
```
