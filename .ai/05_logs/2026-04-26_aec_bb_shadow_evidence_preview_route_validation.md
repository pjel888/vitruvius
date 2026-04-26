# AEC-MEPFS Shadow Evidence Preview Route Validation

**Date:** 2026-04-26  
**Scope:** Twenty-third AEC-MEPFS shadow slice  
**Status:** validated pending commit/push

## Scope

Implemented a compact, read-only `GET /v2/backbone/evidence` route over the
file-backed shadow evidence manifest. The route exposes sanitized manifest
metadata only: report status, graph counts, boundary/benchmark/route counts,
safety invariant booleans, evidence file labels/schema versions/paths, and
input hash count.

No Explorer UI/default adoption was added in this slice.

## Files Changed

- `api/index.ts`
- `api/v2Backbone.test.ts`
- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/vitruvius/kg/backbone_parity_runner.py`
- `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`
- `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
- `scripts/tests/test_kg_backbone_api_route_inventory.py`
- `scripts/tests/test_kg_backbone_shadow_boundary_audit.py`
- `scripts/tests/test_kg_backbone_shadow_benchmark.py`
- `scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/twenty-third-shadow-evidence-preview-route-packet.md`

## Generated Artifacts

- `006_System-Manifests/aec-mepfs-backbone/parity/20260426T090300Z/api-explorer-parity-report.json`
  - `ok: true`
  - `commands_run: 6`
  - `commands_passed: 6`
  - `cases_declared: 25`
  - `cases_passed: 25`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T090320Z/api-route-inventory-report.json`
  - `ok: true`
  - `route_count: 22`
  - `preview_routes_present: 7`
  - `preview_routes_required: 7`
  - `resolve_route_mounted: false`
  - `trace_route_mounted: false`
- `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T090340Z/shadow-boundary-audit-report.json`
  - `ok: true`
  - `checks_passed: 10`
  - `checks_total: 10`
  - graph counts: 7 nodes, 4 edges, 3 roots, max depth 2
- `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T090400Z/benchmark-report.json`
  - `ok: true`
  - 5/5 local file-backed operations passing
  - `runtime_thresholds_evaluated: false`
- `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T090420Z/shadow-evidence-manifest-report.json`
  - `ok: true`
  - `artifact_count: 9`
  - `preview_routes_present: 7`
  - `preview_routes_required: 7`
  - `route_count: 22`
  - `boundary_checks_passed: 10`
  - `benchmark_operations_passed: 5`

## Impact / Blast Radius Evidence

- GitNexus CLI impact checks were run before editing:
  - `buildShadowBackbonePlacementQaPreview`: LOW, 1 impacted dependent.
  - `resolveShadowBackbonePlacementQaReportPath`: LOW, 0 impacted dependents.
  - `run_parity_fixture`: LOW, 2 impacted dependents.
  - `run_api_route_inventory`: LOW, 5 impacted dependents.
- `omx_code_intel` MCP transport was unavailable with `Transport closed`; the
  CLI/file-backed path was used instead.
- `omx team` tmux runtime was not started because `TMUX=unset`; native
  subagent review was attempted instead.

## Verification

- `python3 -m py_compile scripts/vitruvius/kg/backbone_api_route_inventory.py scripts/vitruvius/kg/backbone_parity_runner.py scripts/vitruvius/kg/backbone_shadow_boundary_audit.py scripts/vitruvius/kg/backbone_shadow_benchmark.py scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
  - passed
- `python3 -m py_compile scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
  - passed
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
  - 55 passed
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
  - 144 passed
- `cd api && bun test v2Backbone.test.ts`
  - 56 passed, 0 failed, 207 expectations
- `cd explorer && bun test src/api/graphApi.test.ts src/app.searchInspector.integration.test.tsx`
  - 7 passed, 0 failed, 63 expectations
- `python3 -m json.tool` over the five regenerated reports
  - passed
- `git diff -U0` safety scan for newly added Neo4j/runQuery/KG rebuild/
  feature-flag/default-Explorer adoption patterns
  - no matches
- `git diff --check`
  - passed
- `npx --yes gitnexus@1.6.2-rc.10 status`
  - indexed commit and current commit both `80f7ebf`; status up to date before
    committing this slice

The first broad Python attempt failed because three test fixture writers still
omitted `/v2/backbone/evidence` or pointed at the pre-route manifest paths. The
fixtures were updated to include the seventh preview route and fresh
`20260426T090300Z` through `20260426T090420Z` evidence paths, then the focused
Python suite passed.

Additional verification expected after commit:

- GitNexus post-commit refresh

## Advisory Review

- Gemini CLI was available at `/opt/homebrew/bin/gemini`, but advisory review
  failed with HTTP 403: the account service is disabled. No model findings were
  available.
- Kimi CLI was available at `/Users/philiplewis/.local/bin/kimi`, but advisory
  review timed out after 60 seconds. No model findings were available.
- Native verifier subagent launch initially hit the max-agent limit; the stale
  completed explorer was closed and a verifier review was then launched.
  Verdict: PASS. It found no safety regression, confirmed the route is fenced
  to `006_System-Manifests/aec-mepfs-backbone/evidence-manifest`, confirmed
  25/25 parity cases, 7/7 preview routes, resolver routes unmounted, and all
  boundary safety invariants true. Residual caveat: generated reports record
  `working_tree_dirty: true`, so they prove the uncommitted slice rather than a
  clean post-commit baseline.

## Safety Invariants

- No Neo4j writes: confirmed by implementation and route/static evidence.
- No Neo4j query path: the new route reads a JSON manifest only.
- No KG rebuild: no pipeline command was run.
- No protected content ingest: output is report metadata only.
- No feature flag cutover: boundary audit confirms required flags remain off.
- No Explorer default graph adoption: no Explorer files changed.
- No `/v2/resolve` route mounting: route inventory and boundary audit confirm
  resolver and trace routes remain unmounted.
- Preview/read-only/shadow-only behavior remains opt-in and file-backed.
- Generated artifacts are hash-backed and auditable.

## Residual Risks

- Gemini/Kimi advisory review was unavailable; rely on local tests, generated
  evidence, and native verifier output.
- Runtime resolver/API/Explorer/Neo4j latency thresholds remain intentionally
  unevaluated.
- The evidence preview is API-only; Explorer display remains a separate opt-in
  slice if needed.

## Next Safe Slice

After commit/push and a fresh loop, prefer one of:

- an opt-in Explorer button/subsection for `/v2/backbone/evidence`, if the user
  needs visual access to the consolidated evidence;
- additional manifest/report drift checks;
- a route inventory consumer parity check that compares API response shapes to
  the generated manifest without changing Explorer defaults.
