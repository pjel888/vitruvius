---
task: aec-mepfs-shadow-parity-resolver-route-hygiene
phase: validation
created: 2026-04-26
author: CODEX
status: PASS
---

# AEC-MEPFS Shadow Parity Resolver-Route Hygiene Validation

## Scope

Thirty-seventh AEC-MEPFS shadow slice: prevent forbidden `/v2/resolve*` runtime
resolver routes from being represented as ordinary v2 parity cases while runtime
resolver adoption remains blocked.

## Files Changed

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_parity_runner.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `006_System-Manifests/aec-mepfs-backbone/parity/20260426T124014Z/api-explorer-parity-report.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/thirty-seventh-shadow-parity-resolver-route-hygiene-packet.md`
- `.ai/05_logs/2026-04-26_aec_bb_shadow_parity_resolver_route_hygiene_validation.md`

## Implementation Summary

- Added `_is_forbidden_v2_parity_route(...)` and a contract error for v2 parity
  cases using `/v2/resolve` or `/v2/resolve/trace*`.
- Replaced stale `API-CASE-003` in the S2 readiness fixture with implemented
  `GET /v2/backbone/evidence` preview coverage.
- Added focused contract tests for all blocked resolver route shapes.
- Added parity-runner preflight test proving forbidden resolver parity cases
  fail before command execution.

## Generated Evidence Summary

Parity report:
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T124014Z/api-explorer-parity-report.json`

- `ok: true`
- 6/6 declared parity commands passed.
- 26/26 parity cases passed.
- 26 required parity categories recorded.
- No parity fixture route starts with `/v2/resolve`.

## Verification Commands

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Result before edits: indexed and current commit matched `2d33300`; status
    up-to-date.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius _validate_api_explorer_parity_case --direction upstream --depth 3 --include-tests`
  - Result: MEDIUM; direct impact through `validate_backbone_contract`, no
    affected processes.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius validate_backbone_contract --direction upstream --depth 3 --include-tests`
  - Result: CRITICAL public validator root; no affected processes; mitigated by
    keeping the code change local to the v2 parity route predicate and running
    the full backbone-focused suite.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_parity_runner.py -q`
  - Result: 61 passed.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone*.py -q`
  - Result: 182 passed.
- `python3 -m py_compile scripts/vitruvius/kg/backbone_contracts.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_parity_runner.py`
  - Result: passed.
- `PYTHONPATH=scripts python3 scripts/vitruvius/kg/backbone_parity_runner.py --run-id 20260426T124014Z`
  - Result: passed and wrote the fresh parity report.
- Fixture route sanity check over `valid_readiness_s2.json` and
  `api-explorer-parity-cases.json`
  - Result: no forbidden resolver parity routes remain.

## Advisory Review

- Gemini CLI review remains blocked by the existing 403 service-disabled
  response; no findings were produced.
- Kimi CLI review was attempted against the narrowed staged source diff and
  produced no output after nearly two minutes. The process was terminated and
  the advisory lane is recorded as timed out for this slice.

## Safety Invariant Confirmation

- No Neo4j writes or queries.
- No KG rebuild/reset/load.
- No protected content ingest.
- No feature-flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No live resolver invocation.
- Generated parity artifact is file-backed and auditable.

## Residual Risks

- Downstream boundary audit, benchmark, and evidence manifest still reference
  the earlier parity report until the next clean-source evidence refresh.
- Runtime resolver implementation and live API route mounting remain blocked.

## Next Recommended Safe Slice

Commit and push this parity hygiene slice. Then regenerate route inventory,
boundary audit, benchmark, and evidence manifest from the clean source tree
using the new parity report.
