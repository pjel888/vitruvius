# AEC-MEPFS Explorer Default-Adoption Prep Validation

```yaml
date: 2026-04-27
lane: explorer-default-adoption
classification: GREEN_PREP_AND_REGRESSION_PROOF_ONLY
starting_commit: fd307465
ending_commit: pending
branch: main
working_tree_before: dirty after implementation, clean relative to pushed baseline before lane start
packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_explorer_default_adoption_packet.md
```

## Scope

This lane completes repo-actionable Explorer default-adoption preparation without enabling Explorer default adoption. It adds no-behavior-change regression proof and a static preflight report that confirms the current Explorer default remains the legacy `default` perspective while the AEC-MEPFS Backbone remains explicit opt-in preview only.

## Files inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-closure-packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_four_gated_lanes_reopen_packet.md`
- `explorer/src/App.tsx`
- `explorer/src/stores/useSceneStore.ts`
- `explorer/src/components/HomeScreen.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/api/graphApi.ts`
- `api/index.ts`

## Files changed

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_explorer_default_adoption_packet.md`
- `.ai/05_logs/2026-04-27_aec_mepfs_explorer_default_adoption_validation.md`
- `scripts/vitruvius/kg/backbone_explorer_default_adoption.py`
- `scripts/tests/test_kg_backbone_explorer_default_adoption.py`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption/20260427T120719Z/explorer-default-adoption-report.json`

## Implementation summary

- Added an Explorer default-adoption packet that keeps adoption disabled and documents the future UX, adapter, parity, and rollback gates.
- Added a file-backed static preflight reporter for Explorer default-adoption readiness.
- Updated the reporter after Spark review so safety invariants are derived from explicit checks and pattern evidence instead of fixed constants.
- Added API route inventory checks to the Explorer preflight report so preview routes and default-off guarded resolver status are verified alongside front-end checks.
- Added Python tests for the preflight reporter, including failure cases for changed default perspective, automatic preview fetch, missing API preview route, default-on feature flag, unsafe run id, unsafe output path, and source path escaping.
- Added Explorer integration tests proving `/explore` loads the legacy `default` graph without AEC preview fetches and HomeScreen default entry points preload the legacy `default` graph.

## Generated artifacts

- `006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption/20260427T120719Z/explorer-default-adoption-report.json`

Key artifact facts:

- `ok: true`
- `status.explorerDefaultAdoptionEnabled: false`
- `status.defaultAdoptionReady: false`
- `status.currentDefaultPerspective: default`
- `status.aecBackbonePreviewMode: explicit_user_opt_in`
- `api_route_inventory.previewRoutesMissing: []`
- `api_route_inventory.resolverRoutePolicy: guarded_default_off`
- all safety invariants false.

## Commands and results

```bash
python3 -m compileall -q scripts/vitruvius/kg/backbone_explorer_default_adoption.py
# pass

PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_explorer_default_adoption.py -q
# 8 passed

PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_explorer_default_adoption --run-id 20260427T120719Z
# ok true; report generated

(cd explorer && bun test app.searchInspector.integration.test.tsx components/componentInteraction.test.tsx api/graphApi.test.ts)
# 27 pass, 0 fail, 208 expect() calls

(cd explorer && bun run lint)
# pass

(cd explorer && bun run build)
# pass with existing Vite chunk-size warning

git diff --check
# pass
```

## Spark review

Attempted with `codex exec -m gpt-5.3-codex-spark -s read-only`.

Findings:

1. High: safety invariants were fixed constants instead of derived from checks.
2. Medium: backend/API checks were missing from the preflight.
3. Medium: exact-text front-end heuristics remain limited and should be backed by tests/future adapter checks.

Disposition:

- Accepted findings 1 and 2. The reporter now derives safety invariants from checks and pattern evidence, and includes API route inventory status.
- Finding 3 is partially mitigated by Explorer integration tests and documented as a residual risk for the future graph-adapter/default-adoption packet; full AST/semantic checks are not required for this no-behavior-change prep slice.

## Kimi review

Attempted with local `kimi` advisory review.

Findings:

- Kimi found no safety over-authorization issues and confirmed no accidental default graph switch, no automatic AEC preview fetch, no protected payload exposure, no Neo4j/KG mutation, no default-on flags, no broad live authorization, and no misleading status language.
- Kimi identified one actionable gap: this validation log was referenced by the packet but did not yet exist.

Disposition:

- Accepted. This validation log closes the missing artifact gap.

## Safety invariants

Confirmed for this prep lane:

- broad/global `LIVE_RUNTIME_AUTHORIZED`: not introduced.
- Neo4j mutation: not introduced.
- KG rebuild/reload/reset: not introduced.
- protected ingest/exposure: not introduced.
- Explorer default adoption: not enabled.
- silent default graph switch: not introduced.
- automatic AEC preview fetch: not introduced.
- default-on feature flag: not introduced.
- runtime threshold pass/fail claims: not part of this lane.

## Residual risks / next boundary

Actual Explorer default adoption remains `UNSATISFIED_YELLOW`. The next implementation packet must define a graph adapter from AEC-MEPFS preview/API payloads to Explorer `GraphNode[]`/`GraphEdge[]`, a visible selector or escape path, route/API parity evidence, and rollback proof before any default switch can be implemented.
