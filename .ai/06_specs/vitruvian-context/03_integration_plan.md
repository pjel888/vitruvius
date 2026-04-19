# 08 — Vitruvian Context Integration Plan

> **Scope:** How the Vitruvian Context resolver and cross-discipline relationship taxonomy integrate with the existing taxonomy governance build (Phases 0–10).
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `03_implementation_plan.md`, `01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md`, `02_RESOLVER_ENGINE_SPEC.md`

---

## 1. Executive Summary

The Vitruvian Context is not a separate project. It is a **runtime layer** that sits on top of the taxonomy governance infrastructure built in Phases 0–10. This document defines:

1. Where the Vitruvian Context plugs into existing phases
2. Which existing PRs require updates
3. What new PRs are needed
4. Integration acceptance criteria

**Key insight:** Phases 0–5 build the data model. Phases 6–7 build the API and UI. Phase 8–9 validate migration. **The Vitruvian Context is Phase 6b (API v2 extension) and Phase 11 (new runtime layer).**

---

## 2. Integration Points

### 2.1 Data Model Integration

| Existing Component | Vitruvian Context Dependency | Integration Point |
|-------------------|------------------------------|-------------------|
| `BackboneNode` (Phase 1) | `primary_domain` resolution | `BELONGS_TO_DOMAIN` edge |
| `CanonicalNode` facets (Phase 3) | Context filtering | `FacetFilter` in resolve query |
| `Jurisdiction` model (Phase 4) | Precedence resolution | `WITHIN_JURISDICTION` edges + chain |
| `Overlay` model (Phase 4) | Applicability rules | `HAS_OVERLAY` + `APPLIES_IN` edges |
| `AuthorityDocumentEdition` (Phase 4) | Temporal resolution | `SUPERSEDES` edges |
| `StandardMapping` (Phase 5) | Standards output | `MAPS_TO_STANDARD` edges |
| Cross-discipline edges (new) | Influence traversal | `CONSTRAINS`, `AFFECTS`, etc. |

### 2.2 API Integration

| Existing Endpoint | Vitruvian Context Extension |
|-------------------|----------------------------|
| `GET /v2/node/:id` | Add `influences` and `reasoning_trace` fields |
| `GET /v2/search` | Add `expand_domains` and `max_hops` params |
| `POST /v2/resolve` | **This IS the Vitruvian Context endpoint** |
| `GET /v2/jurisdiction/:code` | Used by resolver for chain building |

### 2.3 UI Integration

| Existing Component | Vitruvian Context Extension |
|-------------------|----------------------------|
| Node detail page | Add "Affected Disciplines" panel |
| Search results | Add "Cross-discipline influences" preview |
| Jurisdiction selector | Drives `POST /v2/resolve` context |
| Layer badges | Show resolved vs canonical state |

---

## 3. PR Updates to Existing Sequence

### PR-01 Update: Backbone Schema

**Addition:** Add `BackboneNode` label and `BELONGS_TO_DOMAIN` / `primary_domain` facets to Neo4j schema.

**Impact:** Minimal. Already planned in PR-01. No structural change.

### PR-02b Update: Jurisdiction Data Schema

**Addition:** Add `precedence_rank` field to `Jurisdiction` model.

**Rationale:** Resolver needs deterministic precedence ordering.

```python
# Addition to Jurisdiction model
precedence_rank: int  # 0=project, 1=municipal, 2=agency, 3=state, 4=national, 5=supranational, 6=international
```

### PR-02c Update: Jurisdiction API Contract

**Addition:** `POST /v2/resolve` endpoint contract.

```typescript
// Added to API v2 contract
POST /v2/resolve
Body: {
  concept_id?: string;
  path_code?: string;
  search_text?: string;
  return_type: "concept" | "overlay" | "evidence" | "standards" | "full";
  facets?: FacetFilter;
  expand_domains?: string[];
  max_hops?: number;
  context: ResolutionContext;
}
```

### PR-07 Update: Facet Assignment Engine

**Addition:** Ensure `primary_domain` facet is always populated and matches `BELONGS_TO_DOMAIN`.

**Validation rule:**
```python
# validate_facets.py addition
assert concept.primary_domain == backbone_node.path_code.split('.')[0]
```

### PR-11 Update: API v2 Implementation

**Addition:** Implement `POST /v2/resolve` with full Vitruvian Context logic.

**Acceptance criteria addition:**
- TC-01 through TC-05 pass (from `02_RESOLVER_ENGINE_SPEC.md` §8)
- Latency targets met (§7)
- Reasoning trace present in every response

---

## 4. New PRs

### PR-16: Cross-Discipline Relationship Taxonomy

**Branch:** `feat/cross-discipline-relationships`
**Phase:** 3 (extends facet model), 4 (extends jurisdiction model)
**Gaps:** New — extends relationship vocabulary

**Scope:**
- Update `scripts/vitruvius/rules/relationship_registry.yaml` with new predicates
- Add `primary_domain` facet type to Neo4j schema
- Add cross-discipline edge validation to `promotion_validator.py`
- Add `validate_graph.py` cycle detection
- Add confidence thresholding rules

**Definition of Done:**
- [ ] All predicates from `01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md` §2 are in registry
- [ ] `promotion_validator.py` rejects unregistered predicates
- [ ] `validate_graph.py` detects cycles in `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS`
- [ ] Unit tests for each new predicate type
- [ ] Domain pair constraint matrix is loadable by validator

**Rollback:**
```bash
git revert <commit>
# Manual: restore relationship_registry.yaml
```

**Dependencies:** PR-01 (backbone schema)

---

### PR-17: Vitruvian Context Resolver Engine

**Branch:** `feat/vitruvian-context-resolver`
**Phase:** 6b (new), 11 (new runtime layer)
**Gaps:** New — core IP

**Scope:**
- `scripts/vitruvius/resolver/` package:
  - `context_parser.py` — parses ResolutionContext
  - `jurisdiction_resolver.py` — builds jurisdiction chain
  - `overlay_resolver.py` — selects applicable overlays
  - `precedence_engine.py` — applies precedence rules
  - `evidence_aggregator.py` — gathers evidence spans
  - `standards_mapper.py` — resolves standards mappings
  - `influence_traverser.py` — cross-discipline influence search
  - `response_builder.py` — assembles ResolvedTruth
  - `resolver.py` — main `resolve()` entrypoint
- `POST /v2/resolve` API endpoint implementation
- Cache layer (Redis or in-memory) for common resolutions
- Monitoring: latency, cache hit rate, error rate

**Definition of Done:**
- [ ] All 8 test cases (TC-01 through TC-08 from spec) pass
- [ ] Latency <100ms for single concept, <200ms for search+resolve
- [ ] Reasoning trace present in 100% of responses
- [ ] Cache hit rate >50% for repeated queries
- [ ] No mutations to canonical nodes during resolution
- [ ] Feature flag `k_vitruvian_context` controls enablement

**Rollback:**
```bash
git revert <commit>
# Manual: set k_vitruvian_context = false
```

**Dependencies:** PR-02b (jurisdiction data), PR-04 (standards), PR-07 (facets), PR-16 (cross-discipline edges)

---

### PR-18: Explorer Vitruvian Context UI

**Branch:** `feat/explorer-vitruvian-context`
**Phase:** 7 (extends Explorer)
**Gaps:** New — UI for resolver

**Scope:**
- "Affected Disciplines" panel on node detail page
- "Why this applies" reasoning trace viewer
- "Context switcher" (change jurisdiction/date to see different resolutions)
- "Cross-discipline influence" graph visualization
- Layer badge updates: show resolved state vs canonical state

**Definition of Done:**
- [ ] Explorer builds without errors
- [ ] Node detail page shows affected disciplines
- [ ] Context switcher changes resolution in real-time
- [ ] Reasoning trace is human-readable
- [ ] No write operations exposed

**Rollback:**
```bash
git revert <commit>
```

**Dependencies:** PR-12 (Explorer read-only updates), PR-17 (resolver engine)

---

## 5. Updated PR Dependency Graph

```
PR-00 (Bootstrap)
  │
  ▼
PR-01 (Backbone Schema) ──► PR-07 (Facet Assignment) ──► PR-16 (Cross-Discipline Edges)
  │                           │                              │
  ▼                           ▼                              ▼
PR-02a (Jurisdiction Graph) ◄─┘                         PR-17 (Vitruvian Context Resolver)
  │                                                         │
  ▼                                                         ▼
PR-02b (Jurisdiction Data)                             PR-18 (Explorer VC UI)
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
PR-10 (Neo4j FTS) ──► PR-11 (API v2) ──► PR-17 (Vitruvian Context Resolver)
  │
  ▼
PR-12 (Explorer Updates) ──► PR-18 (Explorer VC UI)
  │
  ▼
PR-14 (Shadow Graph)
  │
  ▼
PR-13 (Migration Runner)
  │
  ▼
PR-15 (Governance)
```

**Critical path for Vitruvian Context:** PR-01 → PR-07 → PR-16 → PR-02b → PR-04 → PR-11 → PR-17 → PR-18

---

## 6. Phase Mapping

| Original Phase | Vitruvian Context Integration |
|---------------|------------------------------|
| 0 — Schema + Infrastructure | Add `precedence_rank`, `confidence` fields to base models |
| 1 — Backbone Design + Lock | Ensure `primary_domain` is assigned; validate `BELONGS_TO_DOMAIN` |
| 2 — ID Migration + Redirects | No change |
| 3 — Facet Model + Classification | Add `primary_domain` facet validation; cross-discipline edge stubs |
| 4 — Jurisdiction Model + Packs | Add `precedence_rank` to jurisdiction packs; build `WITHIN_JURISDICTION` chains |
| 5 — Standards Mapping | No change |
| 6 — API v2 + Search v2 | **Implement `POST /v2/resolve`**; add `expand_domains` to search |
| 7 — Explorer Read-Only Updates | Add VC UI panels (PR-18) |
| 8 — Migration Runner + Backfill | Validate cross-discipline edges post-migration |
| 9 — Shadow Graph + Parity | Include resolver parity checks |
| 10 — Governance + Validation | Add VC test cases to validation suite |
| **11 — Vitruvian Context (NEW)** | **PR-17: Resolver engine; PR-18: Explorer UI** |

---

## 7. Acceptance Criteria for Vitruvian Context

### 7.1 Functional

| ID | Criteria | Test |
|----|----------|------|
| VC-01 | Same query, different jurisdiction → different answer | TC-01 vs TC-02 |
| VC-02 | Same concept, different date → different edition | TC-01 with historical date |
| VC-03 | Local rule overrides national rule | TC-02 (Makati > PH) |
| VC-04 | Cross-discipline influences are traversable | TC-03 |
| VC-05 | Every answer includes reasoning trace | Inspect all TC responses |
| VC-06 | Invalid jurisdiction returns error | TC-05 |
| VC-07 | Future date returns warning | TC-04 |
| VC-08 | Missing overlay returns canonical only | Query concept with no PH overlay |

### 7.2 Performance

| ID | Criteria | Test |
|----|----------|------|
| VC-P01 | Single concept resolution <100ms | Benchmark 1000 queries |
| VC-P02 | Search + resolution <200ms | Benchmark 1000 queries |
| VC-P03 | Influence traversal (2 hops) <150ms | Benchmark 1000 queries |
| VC-P04 | Cache hit rate >50% | Analytics after 1 week |

### 7.3 Non-Functional

| ID | Criteria | Verification |
|----|----------|-------------|
| VC-N01 | No canonical node mutations | Audit all resolver Cypher queries |
| VC-N02 | Deterministic output | Same input × 1000 = identical output |
| VC-N03 | Feature flag gated | `k_vitruvian_context = false` disables endpoint |
| VC-N04 | Backward compatible | v1 and v2 endpoints unchanged when flag is off |

---

## 8. Risk Integration

| Existing Risk | Vitruvian Context Impact | Mitigation |
|--------------|-------------------------|------------|
| R01 (ID breaks references) | Resolver uses `canonical_id`; no impact | N/A |
| R02 (Explorer UI breaks) | New UI panels behind feature flag | `k_vitruvian_context` gates all UI changes |
| R03 (PH rules don't generalize) | Precedence engine must handle all jurisdiction types | Test with US-IBC and EU-Eurocode mock packs |
| R04 (Search regression) | Resolver adds latency to search | Cache layer; async resolution for search previews |
| R05 (Governance gap) | Resolver must not "hallucinate" rules | All overlays pre-approved; resolver only selects |
| R06 (Data loss) | Resolver is read-only | Audit Cypher; no write permissions |
| R07 (AI corrupts backbone) | AI must not influence resolver logic | Precedence rules are hardcoded; no AI in resolver |
| R08 (Performance — jurisdiction) | Resolver is the primary latency source | Precomputed chains; cached resolutions |
| R09 (Jurisdiction pack complexity) | Resolver must handle multiple packs | Namespace isolation; pack validation |
| R10 (Standards ambiguity) | Resolver returns confidence scores | Filter by threshold; show uncertainty |
| R11 (Shadow parity) | Resolver must work on shadow graph | Parity check includes resolver test cases |
| R12 (Migration corruption) | No migration needed for resolver | Resolver is runtime code, not data |
| R13 (API contract instability) | `POST /v2/resolve` is additive | Versioned path; no breaking changes |

---

## 9. Governance

### 9.1 Resolver Change Control

The Vitruvian Context resolver is **critical infrastructure**. Changes require:

1. **Architect review** for algorithm changes
2. **Steward review** for precedence rule changes
3. **Performance benchmark** before merge
4. **Full test suite pass** (TC-01 through TC-08)

### 9.2 Precedence Rule Lock

Precedence rules (§4.1 of `02_RESOLVER_ENGINE_SPEC.md`) are **locked** after PR-17 merges. Changes require:

1. Written justification
2. Impact analysis on all jurisdiction packs
3. Approval by 2+ stewards from different domains

### 9.3 AI Policy

The Vitruvian Context resolver contains **zero AI logic**. It is:
- Deterministic
- Rule-based
- Precedence-driven
- Evidence-traceable

AI may propose overlays, edges, or mappings. The resolver only selects from pre-existing graph data.

---

## 10. Summary

The Vitruvian Context is not a new project. It is the **capstone runtime layer** that makes Phases 0–10 valuable. Without it, the graph is a knowledge map. With it, the system is a **decision engine**.

**What changes:**
- 3 new PRs (PR-16, PR-17, PR-18)
- 5 existing PRs get minor updates
- 1 new phase (Phase 11)
- 8 new test cases
- Cache layer for performance

**What does NOT change:**
- Backbone governance (still human-locked L1–L2)
- Overlay creation process (still pre-approved)
- API v1 (still additive-only)
- Migration strategy (still shadow-first)

**First deliverable:** PR-16 (cross-discipline relationship taxonomy) can begin as soon as PR-01 merges.
