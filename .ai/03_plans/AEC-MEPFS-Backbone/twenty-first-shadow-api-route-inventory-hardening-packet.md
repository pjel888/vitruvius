---
task: aec-mepfs-shadow-api-route-inventory
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twenty-First Shadow Slice: API Route Inventory Hardening

## Scope

Add a shared file-backed API route inventory for AEC-MEPFS Backbone shadow
safety checks and wire the resolver QA, boundary audit, and benchmark runners
to that shared route-status surface.

This slice is static evidence hardening only. It does not add, remove, or mount
any API route; start the API server; call Explorer; query or write Neo4j;
rebuild the KG; ingest protected content; change feature flags; or promote any
shadow artifact to the live graph.

## Research Baseline

- The twentieth benchmark validation and verifier review identified one shared
  residual risk: route-safety checks were narrow regex scans over `api/index.ts`.
- The resolver QA, boundary audit, and benchmark runners all need the same
  route-boundary truth:
  - required `/v2` preview routes must remain present
  - `/v2/resolve` and `/v2/resolve/trace` must remain unmounted
- The current API route style is direct Hono `app.<method>(...)` declarations in
  `api/index.ts`.

## Audit Findings

- The duplicated route scans were safe for the current route style but would
  drift independently if route-check logic changed.
- The right safe slice is a centralized static inventory and generated report,
  not a runtime route, server call, or feature flag.
- Full TypeScript AST parsing remains unnecessary for the current direct Hono
  route style, but this inventory creates one boundary to replace if routes
  later move into nested routers.

## Implementation Plan

1. Add `scripts/vitruvius/kg/backbone_api_route_inventory.py`.
2. Inventory direct Hono `app.<method>(...)` route declarations while ignoring
   string/comment lookalikes.
3. Produce
   `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/<run-id>/api-route-inventory-report.json`.
4. Expose helper summaries for:
   - resolver QA cached route-status shape
   - boundary audit / benchmark route-status shape
5. Wire `backbone_resolver_qa.py`, `backbone_shadow_boundary_audit.py`, and
   `backbone_shadow_benchmark.py` to the shared inventory helpers.
6. Add focused tests for inventory parsing, forbidden resolver routes, missing
   preview routes, path fences, run-ID fences, missing API index, and helper
   report-shape compatibility.
7. Regenerate route inventory evidence and refresh boundary/benchmark reports
   over the shared route inventory.

## Plan Critique

- [C001] Do not create a runtime route or start the API server.
- [C002] Preserve existing resolver QA and boundary audit report semantics.
- [C003] Fail closed if required preview routes disappear or resolver routes
  are mounted.
- [C004] Keep output path fenced to the route-inventory report directory and
  current run ID.
- [C005] Record the residual limitation: this inventories current direct Hono
  route declarations, not arbitrary nested router composition.

## Execution Checklist

- [x] Inspect current docs, logs, TODOs, and the route-check residual risk.
- [x] Run GitNexus query/impact checks before touching existing route-check
  functions.
- [x] Implement the shared static route inventory and report runner.
- [x] Wire resolver QA, boundary audit, and benchmark runners to the shared
  route inventory.
- [x] Add focused route-inventory and integration tests.
- [x] Generate fresh route inventory, boundary audit, and benchmark evidence.
- [ ] Attempt Gemini/Kimi advisory review and record availability.
- [ ] Run focused and broader affected Python/API verification.
- [ ] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Explicit Non-Goals

- No new `/v2` route.
- No `/v2/resolve` mounting.
- No API server startup or runtime route call.
- No Explorer runtime call or default graph adoption.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No canonical source/content admission.
