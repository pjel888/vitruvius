# AEC-BB Shadow Explorer Test-Hygiene Validation

**Date:** 2026-04-26
**Scope:** twelfth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Changed only `explorer/src/components/componentInteraction.test.tsx`.
- Wrapped the two asynchronous clipboard-copy clicks in the existing
  `NodeInspector exposes unpin and clear-isolation actions` test with
  `act(...)`.
- No runtime component, API route, KG loader, Neo4j, feature flag, source
  ingest, or Explorer default graph code changed.

## Cleanup Plan

1. Reproduce the existing React warning in the focused component test.
2. Keep runtime behavior fixed and adjust only the test harness.
3. Re-run the focused component test and regenerate the parity report to prove
   the warning is gone from parity evidence.

## Evidence

Baseline warning reproduction:

- `cd explorer && bun test src/components/componentInteraction.test.tsx 2>&1 | tee /tmp/vitruvius-componentInteraction-before.log`
  - Result: 15 passed.
  - Warning reproduced: `An update to CopyValueButton inside a test was not wrapped in act(...).`

Fresh focused test after fix:

- `cd explorer && bun test src/components/componentInteraction.test.tsx 2>&1 | tee /tmp/vitruvius-componentInteraction-after.log`
  - Result: 15 passed.
  - `act(...)` warning absent.

Fresh parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T032507Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 22
- Cases passed: 22

The parity command containing `src/components/componentInteraction.test.tsx`
now has clean stderr for the copy-button path; the only retained report warning
is inherited readiness metadata:

- `integration_rollback_proof_plan: rollback proof is planned, not executed`

## Code-Impact Evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Indexed commit: `5b9bada`
  - Current commit: `5b9bada`
  - Status: up to date
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius CopyValueButton --direction upstream`
  - Risk: LOW
  - Impacted count: 0
  - Direct impacts: 0
  - Affected processes: 0

## Verification

- `cd explorer && bun test src/components/componentInteraction.test.tsx`
  - Result: 15 passed.
- `cd explorer && bun test`
  - Result: 42 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with the existing Vite chunk-size warning.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T032507Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 22/22 cases passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/parity/20260426T032507Z/api-explorer-parity-report.json >/dev/null && git diff --check`
  - Result: passed.

## Safety Invariants

- No Neo4j writes: no Neo4j or Cypher write path changed.
- No KG rebuild: no pipeline, graph build, reset, or rebuild command added or
  run.
- No protected content ingest: no source/content reader changed.
- No feature flag cutover: no feature flag files changed.
- No Explorer default graph adoption: no runtime Explorer graph loading logic
  changed.
- Preview/read-only/shadow-only behavior remains opt-in.
- Generated artifacts are file-backed and auditable under
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T032507Z/`.

## Gemini / Kimi Review

- Gemini CLI was rerun against the bounded diff with `--approval-mode plan`.
  It remained blocked by account-side HTTP 403 before producing any advisory
  findings.
- Kimi CLI was rerun against the bounded diff with `--plan` and a one-step
  limit. It produced no actionable review findings and did not edit repository
  files.

## Architect Review

- Native architect review returned `APPROVED`.
- Finding summary: the diff is test-harness-only, the shadow/read-only boundary
  is preserved, and the docs/logs consistently point to the clean
  `20260426T032507Z` parity report.

## Known Residual Risks

- This only removes the copy-button `act(...)` warning from the parity-relevant
  component test. It does not address unrelated future React warning classes.
- Runtime integration remains blocked exactly as before.

## Next Recommended Safe Slice

Prefer file-backed report-reader hardening or another narrowly scoped
read-only/shadow-only evidence improvement. Do not change the default graph,
write Neo4j, rebuild KG, ingest protected content, or promote shadow artifacts.
