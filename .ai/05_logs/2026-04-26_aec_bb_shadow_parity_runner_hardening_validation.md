# AEC-BB Shadow Parity Runner Hardening Validation

**Date:** 2026-04-26
**Scope:** eighth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Expanded the report-producing parity runner from 14 to 20 required parity
  categories.
- Expanded the allowlisted parity command registry from 3 to 6 commands.
- Made these already implemented shadow surfaces mandatory parity evidence:
  - file-backed shadow graph artifact checks,
  - compact `GET /v2/backbone` shadow summary route,
  - bounded `GET /v2/backbone/taxonomy` graph preview route,
  - fail-closed graph drift behavior,
  - opt-in Explorer preview isolation.
- Added a preflight guard requiring every declared parity command to have at
  least one named parity case, so headline command counts cannot drift from the
  case matrix.
- No runtime API route, Explorer default graph path, Neo4j loader, KG rebuild
  command, feature flag, protected source ingest path, or canonical content
  admission path was added.

## Generated Evidence

Fresh parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T014754Z/api-explorer-parity-report.json`

Report counts:

- Commands declared: 6
- Commands run: 6
- Commands passed: 6
- Cases declared: 20
- Cases passed: 20

Report warning:

- `integration_rollback_proof_plan: rollback proof is planned, not executed`
- This warning is inherited from the readiness fixture and does not authorize
  runtime graph mutation.

## Gemini / Kimi Review

- Gemini CLI was present but blocked by account/service authorization:
  Google Code Assist returned HTTP 403, service disabled.
- Kimi CLI was present but produced no advisory output and had to be killed
  after hanging. No Kimi finding was applied.
- External model output was therefore unavailable for this slice; verification
  relies on repo tests and generated evidence.

## Verification

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py`
  - Result: 54 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 29 passed.
- `cd api && bun test v2Backbone.test.ts perspectiveContracts.test.ts`
  - Result: 27 passed.
- `cd explorer && bun test src/app.searchInspector.integration.test.tsx src/utils/labels.test.ts src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts`
  - Result: 27 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T014754Z`
  - Result: ok, 6/6 commands passed, 20/20 cases passed.
- Architect review:
  - Result before fix: BLOCK.
  - Findings: one declared command lacked named case coverage; impact wording
    in the packet was too absolute compared with historical S4 impact evidence.
  - Fix: added required `shadow_backbone_contract_validation` parity case,
    added runner validation that every declared command has at least one named
    case, and reconciled the impact evidence wording.
- `cd api && bun test`
  - Result: 30 passed.
- `cd explorer && bun test`
  - Result: 39 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with the existing Vite chunk-size warning for the
    `vis-network` chunk.
- Post-fix focused check:
  - `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py`
  - Result: 55 passed.

## Safety Invariants

- No Neo4j writes: confirmed by diff scope and command registry.
- No KG rebuild: confirmed by diff scope and commands run.
- No protected content ingest: confirmed by fixture/report-only changes.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: no Explorer runtime code changed.
- Preview/read-only/shadow-only behavior remains opt-in: covered by Explorer
  integration test and parity case `API-PARITY-020`.
- Generated artifacts are file-backed and auditable: parity report written
  under `006_System-Manifests/aec-mepfs-backbone/parity/20260426T014754Z/`.
- API/consumer parity is tested: parity cases `API-PARITY-015` through
  `API-PARITY-020` are now required.

## Known Residual Risks

- Gemini/Kimi advisory review could not provide actionable findings because
  local access was unavailable or hung.
- The parity runner still proves current file-backed shadow surfaces only. It
  does not authorize future `/v2` route families, Neo4j writes, runtime registry
  admission, protected content ingest, or Explorer default graph adoption.

## Next Recommended Safe Slice

Create the next separate packet for file-backed classification/placement QA
over admitted `BackboneNode` rows and existing authoring/migration QA fixtures.
