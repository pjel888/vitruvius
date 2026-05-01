## Plan Summary

**Plan saved to:** `.omx/plans/placement-qa-v2-route-plan-20260426.md`

**Scope:**
- 4 tasks across 2 implementation files and 1 existing artifact contract
- Estimated complexity: LOW

**Key Deliverables:**
1. Additive read-only `GET /v2/backbone/placement-qa` route over the existing file-backed placement QA report.
2. Focused API tests that verify success, fail-closed behavior, and boundary preservation.

## Implementation Plan

1. Add a placement-QA report reader path in [api/index.ts](/Users/philiplewis/vitruvius/api/index.ts).
Acceptance criteria:
- Reads only `006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json` by default.
- Uses a dedicated placement-QA report root/path constant and path guard, separate from shadow-staging artifacts.
- Fails closed with a typed API error when the report is missing, malformed, outside the allowed root, or not a JSON object.

2. Add a compact response builder in [api/index.ts](/Users/philiplewis/vitruvius/api/index.ts) following the existing `/v2/backbone` shadow-route pattern.
Acceptance criteria:
- Returns a summary-only payload: schema version, source/status, run ID, case totals, proposal-level counts, review-queue counts, required coverage, contract-validation ok/errors/warnings, safety boundaries, and artifact/report path.
- Preserves shadow-only/file-backed/no-runtime boundaries and rejects any report with `live_neo4j_writes`, `kg_rebuild`, `protected_content_ingest`, `feature_flag_cutover`, `explorer_default_adoption`, or non-shadow state enabled.
- Does not expose fixture rows, protected content, or any data outside the placement QA report.

3. Add `GET /v2/backbone/placement-qa` in [api/index.ts](/Users/philiplewis/vitruvius/api/index.ts).
Acceptance criteria:
- Route is additive only; no changes to existing `/v2/backbone`, `/v2/backbone/taxonomy`, Explorer defaults, feature flags, Neo4j behavior, or runtime placement flows.
- Route returns `200` for the current passing report and `503` with a stable error code for unavailable/invalid reports.
- Route naming and handler shape remain consistent with the existing shadow summary routes.

4. Extend [api/v2Backbone.test.ts](/Users/philiplewis/vitruvius/api/v2Backbone.test.ts) with focused placement-QA tests.
Acceptance criteria:
- Success test against the real report asserts the expected run ID `20260426T015915Z`, `casesTotal: 3`, `casesPassed: 3`, required coverage keys all `true`, and all prohibited boundaries `false`.
- Missing-report test asserts fail-closed `503` behavior.
- Helper-level validation tests cover at least: report `ok !== true`, unsafe boundary flip, and root/path escape rejection.
- Tests assert the response is summary-only and does not introduce runtime or Explorer cutover semantics.

## Verification Plan

- `cd api && bun test v2Backbone.test.ts`
- `cd api && bun test`
- Optional hardening check if the route adds exported helpers: `cd api && bunx tsc --noEmit`

## Blockers

- No hard blocker for this slice.
- Residual caution: the source report currently carries the warning `shadow_rollback_plan: rollback proof is planned, not executed`. That is not a blocker for a read-only summary route, but the route should surface the warning as report metadata rather than reinterpret it as runtime readiness.

**Does this plan capture your intent?**
- `proceed` - Show executable next-step commands
- `adjust [X]` - Return to interview to modify
- `restart` - Discard and start fresh
