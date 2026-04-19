# 02 — Readiness Plan: Taxonomy Governance Architecture

> **Scope:** Scorecard and readiness assessment for adopting the governed global AEC taxonomy with jurisdictional overlays.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`

---

## Executive Summary

Vitruvius has strong foundational infrastructure but weak taxonomy governance primitives. This plan replaces broad readiness scores with **six pass/fail gates**. No gate may be skipped. The critical path is: **Gate A-draft (schema drafted) → Gate B (backbone frozen) → Gate A-locked (schema locked) → Gate C (redirects tested) → Gate D (shadow parity) → Gate E (API stable) → Gate F (migration idempotent)**.

**Note on Gate A vs Gate B:** Schema must be *drafted* before backbone work begins (so backbone nodes can be validated against the schema), but the schema is only *locked* after the backbone is frozen (because backbone reality may require schema adjustments). This matches the implementation plan: Phase 0 drafts the schema, Phase 1 freezes the backbone, then schema is finalized.

---

## Readiness Gates

### Gate A: Schema Locked
**Question:** Are all Pydantic, Neo4j, PostgreSQL, and TypeScript schemas for the new model designed, reviewed, and committed?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| A1 | `CanonicalNode` extended with `canonical_id`, `path_code`, `primary_domain`, `knowledge_type`, `asset_scope`, `lifecycle_stage`, `project_type`, `performance_topic`, `release_version`, `steward` | Schema files in `scripts/vitruvius/kg/schemas.py` | Backend | 🔴 Not ready |
| A2 | New models exist: `Jurisdiction`, `Authority`, `AuthorityDocumentFamily`, `AuthorityDocumentEdition`, `ApplicabilityRule`, `Overlay`, `StandardReference`, `StandardMapping`, `Localization`, `TaxonomyRelease`, `IdRedirect`, `BackboneNode` | Schema files validated | Backend | 🔴 Not ready |
| A3 | Neo4j schema extended: new labels, edges, indexes, FTS index | `scripts/vitruvius/kg/neo4j_schema.cypher` committed | Backend | 🔴 Not ready |
| A4 | PostgreSQL tables extended: `id_redirect`, `jurisdiction`, `authority`, `authority_document_family`, `authority_document_edition`, `applicability_rule`, `overlay`, `standard_reference`, `standard_mapping`, `localization`, `taxonomy_release` | `scripts/vitruvius/db/schema.sql` committed | Backend | 🔴 Not ready |
| A5 | TypeScript types extended: `GraphNode`, `TaxonomyNode`, `Jurisdiction`, `StandardMapping`, `FacetFilter`, `ResolvedContext` | `explorer/src/types/index.ts` committed | Frontend | 🔴 Not ready |
| A6 | Feature flags defined: `k_taxonomy_v2`, `k_jurisdictional_overrides`, `k_standards_mapping` | `config/vitruvius.yaml` updated | Backend | 🔴 Not ready |

**Exit criteria:** All A1–A6 checkpoints pass code review and type check.

---

### Gate B: L1/L2 Backbone Frozen
**Question:** Is the human-authored L1–2 backbone complete, validated, and steward-assigned?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| B1 | 15 L1 domains authored with definitions | `003_Canonical-Knowledge-Layer/backbone/backbone-l1.yaml` | Editorial | 🔴 Not ready |
| B2 | L2 depth complete under each L1 domain | `003_Canonical-Knowledge-Layer/backbone/backbone-l2.yaml` | Editorial | 🔴 Not ready |
| B3 | Every L1–L2 node has `canonical_id`, `path_code`, `pref_label`, `definition`, `steward` | Validation script passes | Editorial | 🔴 Not ready |
| B4 | Stewards assigned and notified | Steward roster documented | Governance | 🔴 Not ready |
| B5 | Backbone validation script passes (uniqueness, parentage, path code format) | `scripts/vitruvius/taxonomy/validate_backbone.py` passes | Backend | 🔴 Not ready |

**Exit criteria:** All B1–B5 checkpoints pass. L3–L4 may be incomplete but must have placeholder stubs.

**Blocker:** This gate is on the critical path. No facet assignment or cross-discipline edge creation can proceed without a frozen backbone.

---

### Gate C: Redirect Infrastructure Tested
**Question:** Can the system generate opaque IDs, maintain redirects, and resolve old slugs to new IDs?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| C1 | ID generator produces unique `VTN-*` IDs | Unit test: 10k IDs, zero collisions | Backend | 🔴 Not ready |
| C2 | `id_redirect` table populated with all ~105 concept mappings | `id_redirect` CSV or SQL dump | Data | 🔴 Not ready |
| C3 | API v1 returns `canonical_id` field for old slug requests | Contract test passes | Backend | 🔴 Not ready |
| C4 | API v2 resolves `VTN-*` IDs correctly | Contract test passes | Backend | 🔴 Not ready |
| C5 | Explorer redirects old URLs to new canonical URLs | E2E test passes | Frontend | 🔴 Not ready |

**Exit criteria:** All C1–C5 checkpoints pass.

---

### Gate D: Shadow Graph Parity Achieved
**Question:** Does the shadow graph (v2) produce identical or richer results than the primary graph (v1) for all v1 queries?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| D1 | Shadow graph built from migrated canonical Markdown | Neo4j graph with shadow labels exists | Backend | 🔴 Not ready |
| D2 | Parity check script compares v1 vs v2 responses | `scripts/vitruvius/taxonomy/parity_check.py` passes | Backend | 🔴 Not ready |
| D3 | `/taxonomy` v1 and v2 return equivalent trees | Diff shows only additive fields | Backend | 🔴 Not ready |
| D4 | `/search` v1 and v2 return equivalent results for identical queries | Diff shows only additive fields | Backend | 🔴 Not ready |
| D5 | `/node/:id` v1 and v2 return equivalent core data | Diff shows only additive fields | Backend | 🔴 Not ready |

**Exit criteria:** D2 passes with 100% parity for all v1 query patterns.

---

### Gate E: API v2 Contract Stable
**Question:** Are all v2 endpoints implemented, contract-tested, and backward-compatible?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| E1 | `GET /v2/taxonomy` returns governed backbone tree | Contract test passes | Backend | 🔴 Not ready |
| E2 | `GET /v2/search` supports `facets`, `jurisdiction`, `date` params | Contract test passes | Backend | 🔴 Not ready |
| E3 | `GET /v2/node/:id` returns facets, mappings, provenance | Contract test passes | Backend | 🔴 Not ready |
| E4 | `POST /v2/resolve` returns jurisdiction-resolved overlays | Contract test passes | Backend | 🔴 Not ready |
| E5 | `GET /v2/jurisdiction/:code` returns jurisdiction chain | Contract test passes | Backend | 🔴 Not ready |
| E6 | `GET /v2/standards` returns standards mapping lookup | Contract test passes | Backend | 🔴 Not ready |
| E7 | v1 endpoints still pass all existing contract tests | Regression test suite passes | Backend | 🔴 Not ready |

**Exit criteria:** All E1–E7 checkpoints pass.

---

### Gate F: Migration Runner Idempotent
**Question:** Can the migration runner be run multiple times without corruption, and can it be rolled back?

| Checkpoint | Pass Criteria | Evidence | Owner | Status |
|-----------|---------------|----------|-------|--------|
| F1 | Migration runner generates transformed output without mutating source | Output written to staging directory first | Data | 🔴 Not ready |
| F2 | Diff review stage exists: human reviews before apply | PR process documented | Data | 🔴 Not ready |
| F3 | Idempotency: second run produces zero changes | Unit test passes | Backend | 🔴 Not ready |
| F4 | Rollback script restores pre-migration state | `scripts/vitruvius/taxonomy/rollback.py` passes | Backend | 🔴 Not ready |
| F5 | All ~105 concepts + ~340 sources pass schema validation post-migration | Validation script passes | Data | 🔴 Not ready |

**Exit criteria:** All F1–F5 checkpoints pass.

---

## Gate Dependency Graph

```
Gate B (Backbone frozen) ──► Gate A (Schema locked)
                                    │
                                    ▼
                            Gate C (Redirects tested)
                                    │
                                    ▼
                            Gate D (Shadow parity)
                                    │
                                    ▼
                            Gate E (API v2 stable)
                                    │
                                    ▼
                            Gate F (Migration idempotent)
```

**Critical path:** A-draft → B → A-locked → C → D → E → F

---

## Blockers

| Blocker | Impact | Mitigation | Gate Blocked |
|---------|--------|------------|-------------|
| B1 — No human-authored L1–2 backbone exists | Cannot assign facets or validate schema | Founder/editorial team must author backbone | B |
| B2 — Semantic slug IDs deeply embedded | Changing IDs breaks references | Redirect table must be built and tested before migration | C |
| B3 — UI hardcodes node/edge types and assumes single jurisdiction | Schema change risks breaking Explorer | Additive-only evolution; gate new UI behind `k_taxonomy_v2` | D, E |
| B4 — No search index for facet filtering | Facet search will be slow | Add Neo4j FTS + composite indexes before Gate D | A |
| B5 — Philippine-only canonical rules | Generalizing to other jurisdictions requires new rule sets | Extract PH rules into `jurisdiction/PH/` pack | B |

---

## Prerequisites

| Prerequisite | Owner | Estimated Effort | Gate |
|-------------|-------|-----------------|------|
| Approve target backbone L1 domains (15 domains) | Founder/Editorial | 1–2 days | B |
| Confirm canonical ID format (`VTN-<kind>-<7 digits>`) | Founder/Architect | 0.5 days | B |
| Confirm jurisdiction hierarchy storage model (YAML editorial + Neo4j runtime) | Architect | 0.5 days | A |
| Confirm standards mapping storage (Neo4j edges + PostgreSQL reporting) | Architect | 0.5 days | A |
| Set up Neo4j full-text index | Backend | 1 day | A |
| Confirm taxonomy release versioning policy (semver) | Governance | 0.5 days | B |
| Define AI policy for backbone vs facet classification | Governance | 0.5 days | B |

---

## Reuse vs Replace Analysis

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Six-layer filesystem architecture | **Reuse** | Already aligned with target |
| Neo4j graph store | **Reuse** | Extensible; add labels/properties/edges |
| PostgreSQL registry | **Reuse** | Add tables for jurisdiction, standards, taxonomy release |
| Markdown + YAML frontmatter editorial format | **Reuse with extensions** | Add new frontmatter keys |
| Semantic slug IDs | **Replace** | Must become opaque `VTN-*` IDs with redirect table |
| `Taxonomy`/`Topic`/`Subtopic` node labels | **Adapt** | Retain as legacy aliases during transition |
| `taxonomy_path` array of IDs | **Replace** | Use `path_code` string + graph edges |
| `regulatory_basis` inside concept frontmatter | **Replace** | Separate into `SUPPORTED_BY` edges + jurisdiction overlays |
| Hardcoded API perspectives | **Adapt** | Add dynamic perspective builder; keep legacy as aliases |
| Explorer `TreeItem` recursive renderer | **Reuse** | Can render any tree given `children` array |
| vis-network graph canvas | **Reuse** | Color palettes need extension, not replacement |
| Pipeline CLI | **Reuse** | Add subcommands for backbone validation, jurisdiction import |
| Canonical rules YAML | **Adapt** | Extend rule schema to match jurisdiction/authority document patterns |
| Feature-flag governance | **Reuse** | Gate all new work behind flags |

---

## Quick Wins (Can Ship Before Gate B)

| Win | Effort | Impact | Gate |
|-----|--------|--------|------|
| Add `path_code`, `canonical_id`, `steward`, `release_version` fields to `CanonicalNode` schema | 1 day | Enables backbone metadata | A |
| Add `StandardReference` + `StandardMapping` Pydantic models | 1 day | Enables standards crosswalk prototyping | A |
| Add `Jurisdiction` Pydantic model | 1 day | Enables jurisdiction pack design | A |
| Add Neo4j indexes for new fields | 0.5 days | Prevents performance regression | A |
| Add `/health/schema` API endpoint | 0.5 days | Helps clients detect schema changes | E |

---

## Long-Lead Items (After Gate B)

| Item | Effort | Impact | Gate |
|------|--------|--------|------|
| Human-authored L1–4 backbone | 2–3 weeks | Critical path; blocks facet assignment | B |
| ID migration from slugs to opaque IDs | 1–2 weeks | High risk; must preserve redirects | C |
| Jurisdiction precedence resolver | 1 week | Core capability | D |
| Search index + facet filtering | 1 week | Required for usable UI | D |
| Explorer UI refactor | 1–2 weeks | User-facing | E |
| Full migration + backfill + regression test | 1–2 weeks | High risk | F |

---

## Final Readiness Verdict

| Area | Verdict |
|------|---------|
| Infrastructure (pipeline, graph store, registry) | **Ready to extend** |
| Taxonomy content (backbone, facets, mappings) | **Not ready — Gate B blocked** |
| Schema (Neo4j, Pydantic, TypeScript) | **Not ready — Gate A blocked** |
| API / UI | **Not ready — Gates D/E blocked** |
| Search / retrieval | **Not ready — Gate D blocked** |
| Governance (stewards, change control, AI policy) | **Not ready — Gate B blocked** |

**Overall readiness:** The codebase is structurally capable, but **no gate is currently passable**. The first deliverable must be Gate B (backbone frozen).
