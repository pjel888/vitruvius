# AEC-BB Shadow Node Preview Route Validation

**Date:** 2026-04-26
**Scope:** fourteenth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added an additive file-backed `GET /v2/backbone/node/:id` route.
- Added a compact node preview schema:
  `aec-bb-shadow-v2-backbone-node-preview/v1`.
- Resolved staged BackboneNode records by VTN ID, canonical ID, or path code.
- Returned selected node metadata plus immediate relationships from the sibling
  `shadow-backbone-graph.json` artifact.
- Kept source provenance at file-backed artifact paths only.
- Did not change Explorer defaults, v1 routes, Neo4j code, KG pipeline code,
  source ingestion, or feature flags.

## Cleanup Plan

1. Keep the route additive under `/v2/backbone/node/:id`.
2. Reuse existing file-backed shadow report and artifact validation.
3. Fail closed when the graph artifact is missing or runtime boundaries drift.
4. Expose only sanitized node and edge preview fields.
5. Regenerate parity evidence after the route-backed VTN/provenance cases are
   connected.

## Code-Impact Evidence

- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneTaxonomyPreview --direction upstream --include-tests`
  - Earlier slice-selection evidence: LOW impact, 3 impacted nodes.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius api/index.ts --direction upstream --include-tests`
  - Follow-up direct file target attempt could not resolve `api/index.ts` as a
    GitNexus symbol target.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneNodePreview --direction upstream --include-tests`
  - Follow-up direct symbol target attempt could not resolve the new helper
    before index refresh.

Risk disposition: the new helper is additive and route-local. The implementation
is verified with route tests, broad API tests, Explorer tests, parity runner
evidence, and architect re-review.

## Verification

- `cd api && bun test v2Backbone.test.ts`
  - Result: 24 passed.
- `cd api && bunx tsc --noEmit`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 95 passed.
- `cd api && bun test`
  - Result: 42 passed.
- `cd explorer && bun test`
  - Result: 42 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with the existing Vite chunk-size warning.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T041305Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 22/22 cases passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json >/dev/null`
  - Result: passed.
- `git diff --check`
  - Result: passed.

Generated parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 22
- Cases passed: 22

## Advisory Review

- Gemini CLI was attempted with `--approval-mode plan`; it remained blocked by
  account-side HTTP 403 before producing findings.
- Kimi CLI was attempted with `--plan`; it produced no actionable final
  findings within the bounded run and did not edit files.
- Native verifier review returned `APPROVED` before architect re-review, with
  no blocking gaps.
- Native architect review initially returned `REJECTED` because:
  - missing graph artifacts degraded to empty relationship arrays,
  - malformed escaped node IDs returned 503.
- Both findings were fixed:
  - node preview now requires the shadow graph artifact,
  - malformed escaped node IDs now return `400 SHADOW_BACKBONE_NODE_ID_INVALID`.

## Architect Review

Native architect re-review returned `APPROVED` after the fixes.

## Safety Invariants

- No Neo4j writes: no Neo4j write path changed or run.
- No KG rebuild: no reset, rebuild, load, or pipeline command run.
- No protected content ingest: route exposes staged metadata and graph
  provenance paths only.
- No feature flag cutover: no feature flag file changed.
- No Explorer default graph adoption: no Explorer runtime file changed.
- Preview/read-only/shadow-only behavior remains additive under `/v2`.
- Generated artifacts are auditable under
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/`.

## Known Residual Risks

- `integration_rollback_proof_plan` remains a planned warning in the parity
  report; it is not required for this API-only shadow preview slice.
- Runtime integration remains blocked exactly as before.
- The route currently exposes immediate file-backed relationships only, not a
  broader resolved neighborhood or document placement view.

## Next Recommended Safe Slice

Choose the next bounded shadow-only/read-only improvement from fresh evidence.
Prefer one of:

- route-backed resolver/trace preview contracts without runtime mutation,
- additional report/manifest hardening,
- API/Explorer parity hardening for remaining planned `/v2` surfaces,
- Explorer preview-only rendering refinements that do not adopt the default
  graph.
