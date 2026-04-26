# AEC-BB Shadow Placement QA `/v2` Route Validation

**Date:** 2026-04-26
**Scope:** tenth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added `GET /v2/backbone/placement-qa` in `api/index.ts`.
- Added `buildShadowBackbonePlacementQaPreview` and a dedicated placement QA
  report resolver/reader fenced to
  `006_System-Manifests/aec-mepfs-backbone/placement-qa/`.
- The route reads the generated placement QA report only and returns compact
  summary fields: run metadata, counts, required coverage, warnings, contract
  status, safety boundaries, and artifact paths.
- The route does not return `case_results`, authoring case IDs, raw
  `expected_output`, source text, standards text, or protected content.
- No Explorer files were changed.

## Generated Evidence

Fresh parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 21
- Cases passed: 21
- New required parity category:
  `shadow_backbone_placement_qa_preview`

Report warning:

- `integration_rollback_proof_plan: rollback proof is planned, not executed`
- This warning is inherited readiness metadata and does not authorize runtime
  graph mutation.

## Gemini / Kimi Review

- Gemini CLI was present but blocked by account/service authorization:
  Google Code Assist returned HTTP 403, service disabled.
- Kimi CLI was present but produced no output within the bounded 20-second
  advisory attempt (`KIMI_TIMEOUT_NO_OUTPUT`).
- External model output was therefore unavailable for this slice; verification
  relies on repo tests, generated parity evidence, and subagent plan/test
  review.

## Verification

- `cd api && bun test v2Backbone.test.ts`
  - Result: 18 passed.
- `cd api && bun test`
  - Result: 36 passed.
- `cd api && bunx tsc --noEmit`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py`
  - Result: 55 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 91 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T024015Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 21/21 cases passed.
- `cd explorer && bun test`
  - Result: 39 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with existing Vite chunk-size warning.
- `python3 -m json.tool scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
  - Result: passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/api-explorer-parity-report.json`
  - Result: passed.
- `git diff --check`
  - Result: passed.

## Safety Invariants

- No Neo4j writes: no write query path or loader touched; the route reads a JSON
  report.
- No KG rebuild: no pipeline, graph build, reset, or rebuild command added or
  run.
- No protected content ingest: response is summary-only and does not expose
  source text or per-case payloads.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: no Explorer files changed.
- Preview/read-only/shadow-only behavior remains opt-in: route is additive under
  `/v2/backbone/placement-qa`; v1 routes are unchanged.
- Generated artifacts are file-backed and auditable: parity report written under
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/`.
- API/consumer parity is tested by API unit tests and the parity runner.

## Known Residual Risks

- The route summarizes the existing three-case pilot placement QA report only.
  It does not close the future 250-case golden dataset target.
- Gemini/Kimi advisory review remains unavailable in this environment.
- Explorer does not yet render placement QA details; adding that would require a
  separate opt-in preview packet and component tests.

## Next Recommended Safe Slice

Add an opt-in Explorer preview section for the placement QA summary, or harden
report-reader validation for additional file-backed evidence. Do not change the
default graph, write Neo4j, rebuild KG, or ingest protected content.
