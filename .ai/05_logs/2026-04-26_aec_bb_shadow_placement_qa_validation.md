# AEC-BB Shadow Placement QA Validation

**Date:** 2026-04-26
**Scope:** ninth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added a file-backed placement/authoring QA runner:
  `scripts/vitruvius/kg/backbone_placement_qa.py`.
- Added focused tests:
  `scripts/tests/test_kg_backbone_placement_qa.py`.
- The runner validates `valid_readiness_s2.json` with the existing contract
  validator before QA evaluation.
- The runner checks pilot coverage for:
  - L3/L4 LD-8 `PlacementAssertion` auto-accept threshold,
  - L1/L2 human-review routing and AI-authoring prohibition,
  - legacy document-derived label alias/source-label handling.
- No runtime placement engine, Neo4j write, KG rebuild, protected source ingest,
  feature flag, API route, or Explorer default graph behavior was added.

## Generated Evidence

Fresh placement QA report:

`006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`

Report counts:

- Cases total: 3
- Cases passed: 3
- Auto-accept cases: 1
- Required coverage:
  - `l3_l4_ld8_auto_accept`: true
  - `l1_l2_human_review`: true
  - `legacy_label_alias`: true

Report warning:

- `shadow_rollback_plan: rollback proof is planned, not executed`
- This warning is inherited from the S2 fixture and does not authorize runtime
  graph mutation.

## Gemini / Kimi Review

- Gemini CLI was present but blocked by account/service authorization:
  Google Code Assist returned HTTP 403, service disabled.
- Kimi CLI was present but timed out after the bounded 20-second advisory
  attempt with no output.
- A post-compaction retry confirmed Gemini remains blocked with the same HTTP
  403 service-disabled response. The first bounded shell timeout wrapper was
  unavailable on this macOS host; the direct Kimi retry produced no output and
  was treated as unavailable.
- External model output was therefore unavailable for this slice; verification
  relies on repo tests and generated evidence.

## Verification

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_contracts.py`
  - Result: 48 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_placement_qa --run-id 20260426T015915Z`
  - Result: ok, 3/3 cases passed, required coverage true.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_*.py`
  - Result: 98 passed.
- `python3 -m py_compile scripts/vitruvius/kg/backbone_placement_qa.py`
  - Result: passed.
- `bun test` from `api/`
  - Result: 30 passed.
- `bun test` from `explorer/`
  - Result: 39 passed.
- `bun run lint` from `explorer/`
  - Result: passed.
- `bun run build` from `explorer/`
  - Result: passed with existing Vite chunk-size warning.
- `git diff --check`
  - Result: passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
  - Result: passed.

## Safety Invariants

- No Neo4j writes: confirmed by diff scope and runner implementation.
- No KG rebuild: confirmed by diff scope and commands run.
- No protected content ingest: runner reads fixture metadata only.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: no Explorer files changed.
- Preview/read-only/shadow-only behavior remains opt-in: this slice adds no
  preview or runtime consumer.
- Generated artifacts are file-backed and auditable: placement QA report written
  under `006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/`.

## Known Residual Risks

- The report covers the three existing S2 pilot cases only. It does not close
  the full 250-case golden dataset target in the taxonomy authoring/migration
  QA pack.
- Gemini/Kimi advisory review could not provide actionable findings because
  local access was unavailable or timed out.
- The placement QA report is not yet exposed through a read-only `/v2` route or
  Explorer preview. That must be separately packeted.

## Next Recommended Safe Slice

Add a read-only `/v2` placement QA summary route over this report, plus API
tests, without changing Explorer defaults or runtime graph behavior.
