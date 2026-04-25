---
task: taxonomy-first-relationship-quality
phase: 05
created: 2026-04-25
author: PLANNER
status: AMENDED_MVP_EXECUTED
---

# Taxonomy-First Relationship Quality Plan

## RALPLAN-DR Summary

### Principles

- Pre-launch code should implement the intended architecture, not preserve legacy compatibility by default.
- Relationship quality depends on the taxonomy substrate; enrich after the target taxonomy is admitted.
- Every semantic edge must be typed, directional, evidence-backed, and reviewable.
- Do not improve graph metrics by bulk-validating shallow candidate edges.
- Feature flags may gate rollout, but they must not hide absent runtime contracts.

### Decision Drivers

- The current graph has only 4 semantic assertions out of 432 assertions.
- The current shared taxonomy is operational, but the governed taxonomy/backbone is not present at runtime.
- Cross-subject and cross-discipline relationships require a stable taxonomy/backbone to avoid rework.

### Viable Options

1. **Taxonomy-first rebuild path - recommended**
   - Admit/build the governed backbone taxonomy, map current concepts/rules into it, then run taxonomy-aware relationship enrichment.
   - Pros: aligns with intended architecture; avoids preserving stale taxonomy behavior; improves future graph quality.
   - Cons: larger first step; requires backbone validation before relationship gains appear.

2. **Current-taxonomy enrichment path**
   - Use the existing shared taxonomy to generate richer semantic relationships now.
   - Pros: faster visible relationship improvement.
   - Cons: risks rework when taxonomy v2/backbone is admitted; accommodates old structure as product behavior.

3. **Flag flip path**
   - Turn on `k_taxonomy_v2` immediately.
   - Rejected: the `backbone/` corpus and validation/runtime path are absent, so this would create false confidence.

## Decision

Use Option 1: taxonomy-first rebuild path.

## MVP Amendment - 2026-04-25

After this plan was written, the operator explicitly constrained the current
work:

- do **not** rebuild `001-Laws`
- improve the Explorer MVP using the existing `001-Laws` derived content
- do not claim the current shared taxonomy is the final governed backbone

The implemented MVP path therefore uses Option 2 as a temporary overlay, not as
the long-term architecture:

- add review-required semantic concept-to-concept assertions from existing rule
  evidence and canonical source `Referenced Concepts` sections
- add concept-to-document support assertions so document fragments such as SPP
  205 attach to their concept in evidence views
- keep all new deterministic assertions `review_required` / `pending`
- leave `k_taxonomy_v2` disabled and do not create false backbone readiness

The original taxonomy-first decision remains the target architecture after the
MVP surface is stabilized.

## ADR

### Decision

Relationship-quality improvement should target the governed taxonomy/backbone architecture, not the current shared taxonomy as a permanent surface.

### Drivers

- Current relationship semantics are too shallow for Explorer reasoning.
- Current shared taxonomy exists, but the intended governed backbone is not admitted.
- Pre-launch status allows replacing stale architecture instead of preserving compatibility.

### Alternatives Considered

- Enrich immediately against shared taxonomy: rejected because it makes the old taxonomy a compatibility target.
- Flip `k_taxonomy_v2`: rejected because runtime files/contracts are absent.
- Continue Explorer-only UX fixes: insufficient because it masks data quality issues.

### Consequences

- The next execution packet must create or admit the backbone taxonomy before major semantic enrichment.
- Current shared taxonomy can be used as migration input and verification baseline.
- Relationship enrichment becomes a downstream phase after backbone validation and mapping.

## Execution Plan

### Phase 1 - Backbone Admission Audit

- Verify whether any intended backbone source artifacts exist outside `003_Canonical-Knowledge-Layer/backbone/`.
- If absent, create a bounded backbone admission packet from taxonomy-governance docs and current shared taxonomy.
- Define what is human-locked versus AI-proposable in the current pre-launch context.

### Phase 2 - Backbone Runtime Implementation

- Add `003_Canonical-Knowledge-Layer/backbone/` with governed taxonomy files.
- Add validation for uniqueness, parentage, path codes, and steward/authority metadata.
- Wire the KG builder to use backbone taxonomy as the primary taxonomy source.
- Remove or demote old shared-taxonomy runtime behavior rather than preserving it as a peer path.

### Phase 3 - Concept and Rule Mapping

- Map existing `concept` and `rule` nodes to the governed taxonomy/backbone.
- Generate `BELONGS_TO_DOMAIN` or equivalent backbone placement edges from explicit facets.
- Keep old `taxonomy_path` only as migration evidence until replaced.

### Phase 4 - Taxonomy-Aware Relationship Enrichment

- Generate candidate semantic edges using known canonical IDs and backbone paths.
- Start with a narrow predicate set:
  - `CONSTRAINS`
  - `REQUIRES`
  - `APPLIES_TO` or `REGULATED_BY`
  - `AFFECTS`
- Block vague `RELATED_TO` for new cross-domain enrichment.
- Keep AI output as candidates, not admitted truth.

### Phase 5 - Review, Quality Gates, and Explorer Trust

- Add a relationship quality report that tracks semantic density, predicate distribution, evidence coverage, review state, and taxonomy coverage.
- Add Explorer filters for explicit versus inferred/candidate edges.
- Require edge inspector provenance for every semantic relationship.

## MVP Execution Checklist

- [x] Add deterministic relationship enrichment over the existing snapshot without raw/canonical rebuild.
- [x] Score source-level concept co-occurrence to avoid turning broad document lists into unfiltered graph edges.
- [x] Add document support assertions for referenced concepts, including SPP 205 -> Standards of Professional Practice.
- [x] Make the Concepts perspective concept-only and semantic-edge-only.
- [x] Keep provenance/document support in the Evidence perspective rather than polluting the concept map.
- [x] Extend quality reporting to separate structural and semantic relationship counts.
- [x] Reload Neo4j from the enriched snapshot only.

## Acceptance Criteria

- A committed governed taxonomy/backbone exists or the plan stops before claiming taxonomy v2 readiness.
- `k_taxonomy_v2` is not enabled until validation passes.
- The new relationship pipeline does not rely on old shared taxonomy as a compatibility contract.
- Semantic relationship count increases through reviewed/enriched candidates, not bulk validation.
- Explorer can explain why each semantic edge exists.

## Test Plan

- Unit tests for backbone validation.
- Snapshot tests for concept/rule placement into the governed taxonomy.
- Relationship candidate tests with closed predicate vocabulary and known endpoint whitelist.
- Quality-report tests for semantic density and provenance warnings.
- Explorer/API tests for new edge provenance and taxonomy-backed filters.

## Follow-Ups

- Decide whether the active in-progress Explorer UX patch should be committed before opening the taxonomy/backbone execution packet.
- Decide whether to rebuild `001-Laws` after backbone admission or wait for multi-subject aggregate admission.
