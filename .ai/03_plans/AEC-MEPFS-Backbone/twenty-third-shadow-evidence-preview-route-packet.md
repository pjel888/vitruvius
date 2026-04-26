---
task: aec-mepfs-shadow-evidence-preview-route
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twenty-Third Shadow Slice: Evidence Preview Route

## Scope

Add a compact read-only `GET /v2/backbone/evidence` preview route over the
current consolidated shadow evidence manifest. The route must expose only
sanitized manifest metadata: report status, graph counts, route counts,
benchmark counts, safety invariants, artifact labels, schema versions, paths,
and hash counts.

This slice is an additive API preview only. It does not add Explorer default
adoption, start runtime graph integration, mount `/v2/resolve`, call Neo4j,
rebuild the KG, ingest protected content, change feature flags, or promote
shadow artifacts.

## Research Baseline

- The twenty-second slice created
  `shadow-evidence-manifest-report.json`, but no `/v2` consumer can preview the
  consolidated evidence yet.
- Existing AEC-MEPFS preview routes already use file-backed report readers,
  strict filename/root fences, fail-closed builders, and Bun route tests.
- Adding a new route requires refreshing dependent file-backed evidence:
  parity cases, route inventory, boundary audit, benchmark, and evidence
  manifest defaults should all point at the newest shadow packet.

## Audit Findings

- The route is safe only if it reads the manifest file directly and exposes a
  compact summary, not the source reports' full payloads.
- The route inventory must treat the new route as a required preview route so
  future removals fail closed.
- The parity runner needs a new required case category so the route is covered
  by generated parity evidence.
- Regenerated boundary/benchmark/manifest reports must avoid mixed evidence
  vintages after the route is added.

## Implementation Plan

1. Add evidence-manifest constants, path resolver, reader, and compact preview
   builder to `api/index.ts`.
2. Add `GET /v2/backbone/evidence` with deterministic fail-closed errors.
3. Extend `api/v2Backbone.test.ts` with route, builder, path-fence, invalid JSON,
   unsafe invariant, and wrong-filename tests.
4. Update `backbone_api_route_inventory.py` required preview routes and tests.
5. Add a parity case/category for the evidence route and regenerate parity
   evidence.
6. Regenerate route inventory, boundary audit, benchmark, and evidence manifest
   reports over the new route/parity evidence.
7. Update docs/logs/state to point at the new evidence.

## Plan Critique

- [C001] Do not expose full source report payloads or protected source content.
- [C002] Do not add Explorer UI in this slice; keep Explorer default adoption
  unchanged.
- [C003] Keep output and input paths fenced to the evidence-manifest directory.
- [C004] Do not mount runtime resolver routes or use the Neo4j driver in the
  new route path.
- [C005] Regenerate dependent evidence after code changes; stale route
  inventory or boundary reports are not acceptable.

## Execution Checklist

- [x] Inspect current route, parity, inventory, boundary, benchmark, and
  manifest patterns.
- [x] Run GitNexus impact checks for the touched route/build/report surfaces.
- [x] Implement API route and tests.
- [x] Update route inventory and parity case coverage.
- [x] Regenerate parity, route inventory, boundary audit, benchmark, and
  evidence manifest reports.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused and broader affected verification.
- [ ] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Validation Summary

- Route: `GET /v2/backbone/evidence`
- Default evidence manifest:
  `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T090420Z/shadow-evidence-manifest-report.json`
- Regenerated route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T090320Z/api-route-inventory-report.json`
  with 22 direct Hono routes, 7/7 preview routes present, and resolver routes
  unmounted.
- Regenerated parity:
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T090300Z/api-explorer-parity-report.json`
  with 25/25 cases and 6/6 commands passing.
- Regenerated boundary audit:
  `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T090340Z/shadow-boundary-audit-report.json`
  with 10/10 checks passing.
- Regenerated benchmark:
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T090400Z/benchmark-report.json`
  with 5/5 file-backed operations passing and runtime thresholds still not
  evaluated.
- Evidence preview tests cover happy path, missing file, invalid JSON,
  outside-root rejection, wrong-filename rejection, report `ok: false`,
  artifact `ok: false`, safety-invariant drift, artifact-count drift,
  malformed hashes, preview-route drift, and full-payload non-exposure.

## Explicit Non-Goals

- No Explorer rendering change.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No `/v2/resolve` route mounting.
- No runtime latency claim.
