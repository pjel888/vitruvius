# AEC-BB Shadow Resolver QA Validation

**Date:** 2026-04-26
**Scope:** seventeenth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added a file-backed resolver QA runner:
  `scripts/vitruvius/kg/backbone_resolver_qa.py`.
- Added focused tests:
  `scripts/tests/test_kg_backbone_resolver_qa.py`.
- The runner validates `valid_readiness_s2.json` with the existing contract
  validator before QA evaluation.
- The runner checks pilot coverage for:
  - deterministic `single_value` results,
  - deterministic `composed` results,
  - `conflict` results that require review and explain incompatibility,
  - `none` results with insufficient confidence.
- The runner statically fails if `/v2/resolve` or `/v2/resolve/trace` is
  mounted in `api/index.ts`.
- No runtime resolver, Neo4j write, KG rebuild, protected source ingest,
  feature flag, API route, or Explorer default graph behavior was added.

## Generated Evidence

Fresh resolver QA report:

`006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/resolver-qa-report.json`

Report counts:

- Cases total: 4
- Cases passed: 4
- Required coverage:
  - `single_value_deterministic`: true
  - `composed_deterministic`: true
  - `conflict_review_required`: true
  - `none_insufficient`: true
- API route status:
  - `resolveRouteMounted`: false
  - `traceRouteMounted`: false

Report warning:

- `shadow_rollback_plan: rollback proof is planned, not executed`
- This warning is inherited from the S2 fixture and does not authorize runtime
  graph mutation.

## Gemini / Kimi Review

- Gemini CLI was present locally, but the advisory attempt was blocked by
  Google Code Assist HTTP 403 service-disabled response.
- Kimi CLI was present locally, but the bounded plan-mode advisory attempt
  timed out after 60 seconds without actionable findings.
- External model output was therefore unavailable for this slice; verification
  relies on repo tests and generated evidence.
- Native architect review returned `APPROVED`. It found no safety/regression
  blockers and confirmed the slice remains file-backed, shadow-only, and
  disconnected from Neo4j, KG rebuilds, protected ingest, feature flags,
  Explorer defaults, and mounted `/v2/resolve` routes.
- Architect watch item: the `/v2/resolve` route-boundary guard is regex-based
  against `api/index.ts`; update that detector if API route registration style
  changes later.

## Verification

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_resolver_qa.py`
  - Result: 8 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id 20260426T060300Z`
  - Result: ok, 4/4 cases passed, required coverage true.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_vitruvian_context_resolver.py`
  - Result: 60 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_vitruvian_context_resolver.py`
  - Result: 115 passed.
- `python3 -m py_compile scripts/vitruvius/kg/backbone_resolver_qa.py`
  - Result: passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/resolver-qa-report.json`
  - Result: passed.
- `cd api && bun test v2Backbone.test.ts`
  - Result: 38 passed.
- `git diff --check`
  - Result: passed.
- `npx gitnexus --help`
  - Result: stopped after it attempted to install an unpinned GitNexus 1.6.3
    package and hung; the repo-pinned `./scripts/gitnexus_analyze.sh` wrapper
    remains the required post-commit refresh path.

## Safety Invariants

- No Neo4j writes: confirmed by diff scope and runner implementation.
- No KG rebuild: confirmed by diff scope and commands run.
- No protected content ingest: runner reads fixture metadata only.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: no Explorer files changed.
- Preview/read-only/shadow-only behavior remains opt-in: this slice adds no
  preview or runtime consumer.
- Generated artifacts are file-backed and auditable: resolver QA report written
  under `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/`.
- API/consumer parity is not widened: no API/Explorer route was added.

## Known Residual Risks

- The report covers the four existing S2 pilot resolver cases only. It does
  not close the future large resolver golden dataset, non-PH disposition,
  benchmark harness, or exact `/v2/resolve` runtime API assertions.
- Runtime resolver implementation remains blocked behind a separate packet.

## Next Recommended Safe Slice

Implement API-side shadow report/manifest hardening for the existing
file-backed `/v2` preview loaders, or another similarly bounded report
reliability slice, without mounting resolver routes or changing Explorer
defaults.
