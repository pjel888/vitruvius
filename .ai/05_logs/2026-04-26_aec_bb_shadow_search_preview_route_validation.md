# AEC-BB Shadow Search Preview Route Validation

**Date:** 2026-04-26
**Scope:** fifteenth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added an additive file-backed `GET /v2/search` route.
- Added a compact search preview schema:
  `aec-bb-shadow-v2-search-preview/v1`.
- Searched staged BackboneNode labels, preferred labels, path codes, and
  authored aliases.
- Returned selected node metadata plus the detail route for
  `/v2/backbone/node/:id`.
- Kept source provenance at file-backed artifact paths only.
- Did not change Explorer defaults, v1 routes, Neo4j code, KG pipeline code,
  source ingestion, or feature flags.

## Cleanup Plan

1. Keep the route additive under `/v2/search`.
2. Reuse existing file-backed shadow report, staging artifact, and graph
   validation.
3. Fail closed when the graph artifact is missing or runtime boundaries drift.
4. Expose only sanitized BackboneNode metadata and authored aliases.
5. Regenerate parity evidence after the route-backed alias search case is
   connected.

## Code-Impact Evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Indexed commit before slice: `c4b7036`
  - Current commit before slice: `c4b7036`
  - Status: up to date.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneTaxonomyPreview --direction upstream --include-tests`
  - Risk: LOW
  - Impacted count: 3
  - Direct impacts: `api/index.ts`, `api/v2Backbone.test.ts`

Risk disposition: the new helper is additive and route-local. The implementation
is verified with route tests, broad API tests, Explorer tests, parity runner
evidence, and architect review.

## Verification

- `cd api && bun test v2Backbone.test.ts`
  - Result: 30 passed.
- `cd api && bunx tsc --noEmit`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 95 passed.
- `cd api && bun test`
  - Result: 48 passed.
- `cd explorer && bun test`
  - Result: 42 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with the existing Vite chunk-size warning.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T043021Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 23/23 cases passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json >/dev/null`
  - Result: passed.
- `git diff --check`
  - Result: passed.

Generated parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 23
- Cases passed: 23

## Advisory Review

- Gemini CLI was attempted with `--approval-mode plan`; it remained blocked by
  account-side HTTP 403 before producing findings.
- Kimi CLI was attempted with `--plan`; it produced no actionable final
  findings within the bounded run and did not edit files.

## Architect Review

Native architect review returned `APPROVED` with two LOW findings:
locale-dependent normalization/tie-breaking and parity coverage limited to
happy-path search. Both were addressed before commit by switching to
locale-independent lowercase/ASCII comparisons and adding `API-PARITY-002A` for
the empty-query client-error path.

Final native architect re-review returned `APPROVED (CLEAR)` with no scoped
findings after those fixes.

## Cleanup Pass

AI slop cleanup was scoped to the slice-owned API route, focused route tests,
parity fixture, generated parity report, and state/evidence docs. Behavior was
locked by the route tests and parity runner before cleanup. No dead code,
duplicated branch, speculative abstraction, or boundary cleanup justified
additional code edits. Focused route tests, API typecheck, JSON validation, and
`git diff --check` were rerun after the evidence-log correction.

## Safety Invariants

- No Neo4j writes: no Neo4j write path changed or run.
- No KG rebuild: no reset, rebuild, load, or pipeline command run.
- No protected content ingest: route exposes staged BackboneNode metadata and
  authored aliases only.
- No feature flag cutover: no feature flag file changed.
- No Explorer default graph adoption: no Explorer runtime file changed.
- Preview/read-only/shadow-only behavior remains additive under `/v2`.
- Generated artifacts are auditable under
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/`.

## Known Residual Risks

- `integration_rollback_proof_plan` remains a planned warning in the parity
  report; it is not required for this API-only shadow preview slice.
- Runtime integration remains blocked exactly as before.
- Search currently covers staged BackboneNode metadata only; document, source,
  placement, and resolver search remain future shadow-only surfaces.

## Next Recommended Safe Slice

Choose the next bounded shadow-only/read-only improvement from fresh evidence.
Prefer one of:

- route-backed resolver/trace preview contracts without runtime mutation,
- route-backed source metadata preview that does not expose protected source
  payloads,
- additional report/manifest hardening,
- Explorer preview-only rendering refinements that do not adopt the default
  graph.
