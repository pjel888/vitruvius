---
task: aec-mepfs-backbone
phase: third-shadow-v2-backbone-route-implementation-packet
created: 2026-04-26
author: CODEX
status: IMPLEMENTED-AND-VALIDATED
---

# Third Shadow V2 Backbone Route Implementation Packet

## Status

Status: authorized bounded implementation for the first additive
`GET /v2/backbone` shadow read route.

This packet supersedes the planning-only status of
`shadow-v2-api-read-route-planning-packet.md` only for the single route named
here.

## Authorized Slice

Add the smallest API read route:

- `GET /v2/backbone`

The route may read only:

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-staging-consumer-report.json`

The route response may include:

- response schema version
- run ID
- report status
- predicate/source counts
- read-only boundary status
- no-ingest boundary coverage
- artifact/report paths

## Prohibited Scope

This packet does not authorize:

- Explorer adoption or default UI calls
- v1 API behavior changes
- Neo4j writes or reads for Backbone data
- graph rebuild/reset/cleanup
- feature flags or default-on cutover
- protected standards/legal source content ingest
- full registry row exposure through the API
- edits to `CanonicalNode`, `TaxonomyLoader`, `Neo4jLoader`, or
  `UnifiedSnapshotBuilder`

## Impact Review

Fresh pre-change evidence:

- GitNexus index status: up to date at `11c8df0`
- API route file: `api/index.ts`
- `runQuery` impact: LOW; direct dependents are `api/index.ts`,
  `getPerspectiveNodeCount`, `QueryPanel`, and `api/perspectiveContracts.test.ts`
- `buildPerspectiveQueries` impact: LOW; direct dependents are `api/index.ts`
  and `api/perspectiveContracts.test.ts`

Implementation will avoid changing `runQuery`, `buildPerspectiveQueries`, v1
route handlers, Explorer client code, and Neo4j query behavior.

## Test Plan

Before implementation:

- `cd api && bun test`
  - PASS: 18 tests

Route-shape tests to add before route implementation:

- success response for `GET /v2/backbone` from the real consumer report
- fail-closed response when the configured report path is missing
- helper-level fail-closed validation when `ok` is false
- helper-level fail-closed validation when runtime cutover boundaries are true

Post-implementation verification:

- `cd api && bun test`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_shadow_report_reader.py`
- generated consumer report remains `ok: true`
- read-only Neo4j smoke still reports `BackboneShadow` count 0
- Git diff review and GitNexus post-change status

## Runtime Boundary

The route is additive and shadow-only. It is not a primary graph route, not an
Explorer route, not a feature flag, and not evidence of runtime cutover.

## Implementation Result

Implemented by:

- `api/index.ts`
- `api/v2Backbone.test.ts`

The route reads the existing shadow consumer report and returns a compact
summary only. It does not return predicate registry rows, source-rights registry
rows, protected source content, or primary graph data.

Verification evidence:

- `cd api && bun test v2Backbone.test.ts`
  - PASS: 4 passed
- `cd api && bun test`
  - PASS: 22 passed
- `cd api && bunx tsc --noEmit`
  - PASS

Additional boundary verification is recorded in
`.ai/05_logs/2026-04-26_aec_bb_shadow_v2_backbone_route_validation.md`.
