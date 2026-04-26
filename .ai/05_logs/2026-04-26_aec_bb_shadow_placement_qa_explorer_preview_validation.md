# AEC-BB Shadow Placement QA Explorer Preview Validation

**Date:** 2026-04-26
**Scope:** eleventh AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added `getBackbonePlacementQaPreview()` in `explorer/src/api/graphApi.ts`.
- Added an additive `BackbonePlacementQaPreview` Explorer type.
- Added placement QA preview state and explicit loading in
  `explorer/src/components/ExplorerRail.tsx`.
- Added a compact placement QA subsection in
  `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`.
- Extended Explorer tests so placement QA fetches only after the explicit
  `Load placement QA summary` action and does not replace graph state,
  selected perspective, nodes, or edges.
- Extended API/Explorer parity evidence with
  `shadow_placement_qa_preview_opt_in_isolation`.

## Generated Evidence

Fresh parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T031555Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 22
- Cases passed: 22
- New required parity category:
  `shadow_placement_qa_preview_opt_in_isolation`
- The parity command for Explorer opt-in isolation now includes
  `src/api/graphApi.test.ts`, which pins the Explorer placement QA path and
  schema version to the server contract.

Report warning:

- `integration_rollback_proof_plan: rollback proof is planned, not executed`
- This warning is inherited readiness metadata and does not authorize runtime
  graph mutation.

## Gemini / Kimi Review

- Gemini CLI was present but blocked by account/service authorization:
  Google Code Assist returned HTTP 403, service disabled.
- Kimi CLI was present but produced no output within the bounded advisory
  attempt; the hung `Kimi Code` process was killed and recorded as
  `KIMI_TIMEOUT_NO_OUTPUT`.
- Both advisory checks were retried after the schema-contract fix and remained
  unavailable for the same reasons.
- External model output was therefore unavailable for this slice; verification
  relies on repo tests, generated parity evidence, and native subagent review.

## Subagent Review

- Planner review saved:
  `.omx/plans/aec-mepfs-shadow-explorer-placement-qa-preview-plan-2026-04-26.md`
  and approved the explicit-action Explorer preview shape.
- Test review recommended three minimum assertions: panel opt-in loading,
  placement summary rendering, and ExploreView graph-state isolation. All three
  are now covered.
- Architect review initially returned `WATCH` for schema-contract drift in the
  Explorer mocks and stale impact evidence. The fix aligned mock schema values
  to `aec-bb-shadow-v2-backbone-placement-qa-preview/v1`, added
  `src/api/graphApi.test.ts` to pin the Explorer route/schema to the server
  contract, and refreshed impact evidence for `getBackbonePlacementQaPreview`.
- Follow-up architect review returned `APPROVED` / `Architectural Status:
  CLEAR`.

## Code-Impact Evidence

GitNexus MCP tools were not exposed through the available MCP surface, so this
slice used the pinned GitNexus CLI.

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Indexed commit: `d6a8fbe`
  - Current commit: `d6a8fbe`
  - Status: up to date
- `BackbonePreviewPanel`
  - Risk: LOW
  - Impacted count: 0
  - Affected processes: 0
- `ExplorerRail`
  - Risk: LOW
  - Impacted count: 0
  - Affected processes: 0
- `getBackbonePlacementQaPreview`
  - Risk: LOW
  - Impacted count: 2
  - Direct impacts: 1
  - Affected process: `ExplorerRail`
- `run_parity_fixture`
  - Risk: LOW
  - Impacted count: 2
  - Direct impacts: 1
  - Affected processes: 0

The central type barrel `explorer/src/types/index.ts` was changed additively to
declare a new preview response type. No existing type contracts were narrowed or
renamed.

## Verification

- `cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx`
  - Result: 22 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py`
  - Result: 55 passed.
- `cd api && bun test`
  - Result: 36 passed.
- `cd explorer && bun test`
  - Result: 42 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with existing Vite chunk-size warning.
- `cd api && bunx tsc --noEmit`
  - Result: passed.
- `python3 -m json.tool scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T031555Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 22/22 cases passed.
- `git diff --check`
  - Result: passed.

The parity runner surfaced pre-existing React `act(...)` warnings from the
copy-button component test path, but all Explorer tests passed and the warnings
are outside the placement QA preview behavior.

## Safety Invariants

- No Neo4j writes: no loader, driver, Cypher write, or Neo4j client path was
  added or run.
- No KG rebuild: no pipeline, graph build, reset, or rebuild command was added
  or run.
- No protected content ingest: the Explorer renders compact summary fields only
  and never requests per-case payloads.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: placement QA is shown only inside the
  non-default AEC-MEPFS preview after an explicit click.
- Preview/read-only/shadow-only behavior remains opt-in: the integration test
  proves placement QA fetch count remains zero until the explicit action.
- Generated artifacts are file-backed and auditable: parity report written
  under `006_System-Manifests/aec-mepfs-backbone/parity/20260426T031555Z/`.
- API/consumer parity is tested by API unit tests, Explorer tests, and the
  parity runner.

## Known Residual Risks

- The placement QA preview summarizes the existing three-case pilot report only;
  it does not close the future large golden dataset target.
- Gemini/Kimi advisory review remains unavailable in this environment.
- The UI still depends on the existing `/v2/backbone/placement-qa` summary
  route and does not independently validate report internals in the browser.
- React copy-button `act(...)` warnings remain in the broader component test
  path and should be cleaned in a separate focused UI test-hygiene slice.

## Next Recommended Safe Slice

Prefer file-backed report-reader hardening or UI test-hygiene cleanup for the
pre-existing React `act(...)` warnings. Do not change the default graph, write
Neo4j, rebuild KG, ingest protected content, or promote shadow artifacts to the
live runtime.
