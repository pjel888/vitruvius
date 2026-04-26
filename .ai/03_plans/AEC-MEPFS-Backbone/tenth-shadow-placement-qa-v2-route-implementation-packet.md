---
task: aec-mepfs-shadow-placement-qa-v2-route
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Tenth Shadow Slice: Placement QA `/v2` Preview Route

## Scope

Expose the existing file-backed placement/authoring QA report through an
additive read-only API route:

`GET /v2/backbone/placement-qa`

The route summarizes
`006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
without exposing per-case payloads or changing Explorer defaults.

## Research Baseline

- `ACTIVE_WORK.md` and `STRATEGIC_NEXT_MOVE.md` identify a read-only placement
  QA `/v2` summary route as the next bounded shadow slice.
- `ninth-shadow-placement-qa-implementation-packet.md` generated a passing
  placement QA report but intentionally did not expose a runtime/API/Explorer
  consumer.
- Existing `/v2/backbone` and `/v2/backbone/taxonomy` routes use file-backed
  report readers, path-fenced resolvers, fail-closed builders, and route-shape
  tests in `api/v2Backbone.test.ts`.

## Audit Findings

- The placement QA report was not visible to API consumers except by reading
  the manifest directly.
- Adding a summary route is safer than invoking runtime placement because it
  reads only the already generated report.
- Any route must stay summary-only. Returning `case_results` would widen the
  surface and risk exposing future per-case source payloads.

## Implementation Plan

1. Add a dedicated placement QA report root, default report path, resolver, and
   reader in `api/index.ts`.
2. Add `buildShadowBackbonePlacementQaPreview` to validate schema, report
   status, contract status, required coverage, counts, and safety boundaries.
3. Add `GET /v2/backbone/placement-qa` with a route-specific fail-closed
   `503` response.
4. Extend `api/v2Backbone.test.ts` with success, missing-report, report-status,
   boundary, coverage, and path-fence tests.
5. Extend the parity runner required category set and parity cases fixture so
   the new route is mandatory in generated API/Explorer parity evidence.
6. Generate a fresh parity report.

## Plan Critique

- [C001] Do not return `case_results` or future protected content payloads.
- [C002] Do not reuse the shadow-staging path root for placement QA reports.
- [C003] Do not change v1 API routes or Explorer default behavior.
- [C004] Do not treat the inherited rollback warning as runtime readiness.

## Execution Checklist

- [x] Inspect API route conventions and parity runner conventions.
- [x] Run GitNexus impact on existing API/parity symbols.
- [x] Implement route, builder, resolver, and tests.
- [x] Add required parity category and case.
- [x] Generate fresh parity report with 21/21 cases passing.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused API and parity verification.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No runtime `PlacementEngine` execution.
- No canonical source/content admission.
