---
task: aec-mepfs-backbone
phase: explorer-runtime-status-parity
created: 2026-04-27
author: CODEX
status: BOUNDARY_APPROVED
classification: GREEN/YELLOW-6
---

# Explorer Runtime-Status Parity Packet

## Purpose

Align the API and Explorer evidence-preview surface with the current guarded
resolver-runtime state. The latest consolidated evidence manifest records
`resolver_route_policy: guarded_default_off` and
`benchmark_runtime_threshold_disposition: not_evaluated_shadow_file_backed_only`,
but the preview API and Explorer UI still surfaced only older boolean language.

This packet authorizes a bounded evidence-only parity update so users can see the
current guarded/default-off status without triggering resolver calls, graph
adoption, or threshold pass/fail claims.

## Authority

- Project-owner standing directive: GREEN work for docs, parity fixtures,
  evidence manifests, API preview parity tests, and Explorer opt-in preview
  tests.
- YELLOW-6 conditions are satisfied because the change preserves the existing
  opt-in AEC-MEPFS preview and does not introduce automatic fetches, default
  graph adoption, resolver invocation, or hidden feature cutover.

## Allowed Scope

- Add sanitized `resolverRoutePolicy` and
  `benchmarkRuntimeThresholdDisposition` fields to the compact
  `/v2/backbone/evidence` preview summary.
- Require those fields in current evidence-manifest previews so stale
  unmounted-only evidence fails closed.
- Render the two fields in the existing Explorer evidence subsection only after
  the user clicks `Load evidence summary`.
- Update parity fixtures, API tests, Explorer tests, and active planning docs so
  they distinguish legacy unmounted-only evidence from current guarded
  default-off route policy.

## Blocked Scope

This packet does not authorize:

- unguarded or default-on `/v2/resolve*` behavior
- Explorer calling `/v2/resolve*`
- automatic AEC-MEPFS preview fetches
- Explorer default graph adoption or perspective cutover
- Neo4j write/reset/reload/promote behavior
- KG rebuild/reload/reset
- protected source ingest or protected payload exposure
- runtime threshold pass/fail claims
- broad or global `LIVE_RUNTIME_AUTHORIZED` status

## Implementation Plan

1. Extend the evidence preview builder and TypeScript type with the two sanitized
   runtime-status summary fields.
2. Update Explorer evidence rendering and tests so the status is visible only in
   the already opt-in evidence section.
3. Update parity fixture assertions for evidence-preview runtime-status parity.
4. Reconcile active parity/scorecard docs with current guarded-default-off
   semantics.
5. Run focused API, Explorer, parity, and safety checks.

## Verification Commands

Minimum verification:

```bash
git diff --check
(cd api && bun test v2Backbone.test.ts)
(cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx)
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_parity_runner.py -q
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id <RUN_ID>
```

Safety greps must distinguish documentation guardrail mentions from code
behavior and confirm no unauthorized runtime adoption.

## Evidence Artifacts

- Validation log under `.ai/05_logs/`.
- Refreshed parity report under
  `006_System-Manifests/aec-mepfs-backbone/parity/` because the parity fixture
  changes.
- GitNexus refresh after commit per repo convention.

## Completion Criteria

- API evidence preview returns route policy and threshold disposition from the
  current manifest.
- Explorer evidence subsection displays those fields only after explicit evidence
  load.
- Tests prove the opt-in preview and current graph state remain unchanged.
- Parity runner passes with the updated fixture.
- Safety checks show no Neo4j/KG/protected/default-adoption/default-on/threshold
  cutover behavior.
- Evidence log exists, working tree is clean after commit, and branch is pushed.

## Next Boundary

After this packet, remaining repo-actionable AEC-MEPFS work should be derived
from a fresh backlog scan. The placeholder benchmark command in the S3 readiness
fixture remains a later benchmark/parity-harness cleanup candidate unless this
packet creates a real benchmark command.
