---
task: aec-mepfs-shadow-taxonomy-preview
phase: 05
created: 2026-04-26
author: CODEX
status: ACCEPTED
supersedes: null
---

# Fifth Shadow Slice: Taxonomy Readiness Preview

## Scope

Add the next bounded AEC-MEPFS Backbone shadow consumer slice:
`GET /v2/backbone/taxonomy` plus an opt-in Explorer detail preview inside the
existing AEC-MEPFS rail panel.

This slice is a **readiness/detail preview**, not a canonical taxonomy graph.
The current shadow staging artifact contains predicate-registry and
source-rights-registry metadata. It does not yet contain admitted
`BackboneNode` records, graph edges, canonical content, or Neo4j-backed
taxonomy state.

## Research Baseline

- `.ai/01_roadmap/current-phase.md` lists the next concrete AEC action as a
  separate packet for a remaining `/v2` route or staging-detail preview.
- `.ai/STRATEGIC_NEXT_MOVE.md` says the next slice must be chosen from fresh
  impact evidence and must keep live graph/reset/cutover work blocked.
- GitNexus status is up to date at commit `84e5e3d`.
- The current staging artifact is
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-backbone-staging.json`.
- Artifact shape: predicate registry, source-rights registry, counts,
  source paths, status, and shadow-only boundaries.

## Audit Findings

- `GET /v2/backbone` currently reads only the consumer report and returns a
  compact summary.
- A detail route must validate both the consumer report and the staging
  artifact before exposing any preview data.
- The preview must be explicit about incompleteness: registry metadata is
  present, canonical taxonomy nodes are not.
- The shared Explorer `api()` helper has CRITICAL blast radius, so this slice
  must not alter its behavior.
- UI behavior must stay opt-in and must not alter `perspectiveId`, graph nodes,
  graph edges, feature flags, or Neo4j state.

## Implementation Plan

1. Add a backend schema version and pure builder for a sanitized taxonomy
   readiness preview.
2. Add `GET /v2/backbone/taxonomy` that reads the current consumer report,
   resolves the referenced staging artifact within the shadow-staging root,
   validates shadow boundaries, and fails closed on mismatch.
3. Return only safe registry metadata: predicate names/categories/classes,
   source-family clearance summaries, counts, boundaries, and explicit
   completeness flags.
4. Add focused backend tests for success, safe projection, and fail-closed
   boundary validation.
5. Add frontend types and a narrow API wrapper without changing the shared
   request helper.
6. Extend the existing opt-in panel with an explicit detail button and compact
   registry-readiness rendering.
7. Add component and integration tests proving details are not fetched by
   default and do not replace graph state.
8. Run focused API and Explorer QA, then live-smoke the preview server.

## Plan Critique

- [C001] Naming the route `taxonomy` can overstate readiness. Response copy and
  UI must explicitly state that no canonical taxonomy tree is available yet.
- [C002] Returning raw registry rows could leak planning-only source notes or
  source content. The backend must sanitize rows and avoid examples,
  non-examples, official URLs, blocking notes, or standards text.
- [C003] The detail route reads the staging artifact referenced by the consumer
  report. Path resolution must remain inside the shadow-staging root.
- [C004] A detail fetch on panel-open would increase coupling. Keep the detail
  fetch behind a second explicit action.

## Execution Checklist

- [x] Capture current working tree and active state.
- [x] Run GitNexus status/query and exact-symbol impact review.
- [x] Inspect current shadow artifact shape.
- [x] Implement backend route and tests.
- [x] Implement Explorer detail preview and tests.
- [x] Run UltraQA verification loop.
- [x] Update validation/state/docs.
- [ ] Commit, refresh GitNexus, and push.

## Completion Evidence

- `api/index.ts` adds `GET /v2/backbone/taxonomy` and
  `buildShadowBackboneTaxonomyPreview`.
- `api/v2Backbone.test.ts` covers the success path, sanitized projection, and
  fail-closed artifact-boundary validation.
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx` adds an
  explicit detail control inside the existing opt-in preview panel.
- `explorer/src/app.searchInspector.integration.test.tsx` verifies detail data
  is not fetched by default and does not replace graph state.
- Validation log:
  `.ai/05_logs/2026-04-26_aec_bb_shadow_taxonomy_preview_validation.md`.

## Explicit Non-Goals

- No Neo4j reset, load, dump, or write.
- No KG rebuild.
- No feature flag default change.
- No Explorer default graph replacement.
- No protected source content exposure.
- No claim that registry metadata is the admitted AEC-MEPFS Backbone graph.
