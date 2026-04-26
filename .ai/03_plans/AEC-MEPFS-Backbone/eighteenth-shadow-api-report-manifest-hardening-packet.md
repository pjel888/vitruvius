---
task: aec-mepfs-shadow-api-report-manifest-hardening
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Eighteenth Shadow Slice: API Report Manifest Hardening

## Scope

Harden the existing API-side file-backed shadow report and artifact readers.

This slice keeps all current `/v2` preview routes additive and shadow-only. It
does not add a route, mount `/v2/resolve`, query or write Neo4j, rebuild the KG,
ingest protected content, change feature flags, or alter Explorer defaults.

## Research Baseline

- After the source preview and resolver QA slices, the active state points to
  file-backed QA/evidence hardening before runtime cutover.
- Architect advisory identified the shared API shadow readers in `api/index.ts`
  as a high-value, low-risk hardening target because all existing preview
  routes depend on them.
- GitNexus impact for the exact touched functions returned LOW risk:
  `readShadowBackboneConsumerReport`, `readShadowBackbonePlacementQaReport`,
  `readShadowBackboneStagingArtifact`, `readShadowBackboneGraphArtifact`,
  `resolveShadowBackboneReportPath`,
  `resolveShadowBackbonePlacementQaReportPath`, and
  `resolveShadowBackboneArtifactPath`.

## Audit Findings

- The API readers already fenced paths by report root and failed closed, but
  they accepted any filename inside the fenced roots.
- Invalid JSON diagnostics depended on the JS runtime parse message rather than
  a stable shadow report/artifact label and path.
- Tightening the existing readers improves preview reliability without changing
  route shape or runtime adoption.

## Implementation Plan

1. Add centralized path resolution for shadow report/artifact roots and expected
   filenames.
2. Require:
   - `shadow-staging-consumer-report.json`
   - `shadow-backbone-staging.json`
   - `shadow-backbone-graph.json`
   - `placement-qa-report.json`
3. Add a shared JSON-object reader with deterministic invalid-JSON diagnostics.
4. Export the report and graph path resolvers only for focused API tests.
5. Add API tests for invalid JSON and wrong-filename fail-closed behavior.
6. Regenerate parity evidence.

## Plan Critique

- [C001] Do not broaden this into route adoption or resolver runtime work.
- [C002] Keep the response schemas stable; path/JSON hardening should only
  affect failure cases.
- [C003] Preserve existing shadow path root fences.
- [C004] Do not write persistent test output; temporary invalid-report files
  must be cleaned after tests.

## Execution Checklist

- [x] Run GitNexus impact on exact API reader/path symbols.
- [x] Implement filename fencing and deterministic JSON diagnostics.
- [x] Add focused API tests.
- [x] Run focused API tests.
- [x] Generate fresh API/Explorer parity report.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Update evidence/state docs.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No new `/v2` route.
- No `/v2/resolve` mounting.
- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No canonical source/content admission.
