# Explorer Source-Gap Browser Context

## Task

Add a graph-wide, read-only source-gap workqueue browser to Explorer so operators can triage source/resource attachment gaps without first selecting an individual node.

## Desired Outcome

The AEC-MEPFS rail preview should let the operator load the latest source-gap workqueue, inspect total/returned node and relationship source gaps, see top proposed resources, and understand that the view is review-only and does not create Resource Layer links or mutate the active graph.

## Known Facts

- `GET /v2/backbone/source-gap-workqueue` exists and returns a bounded preview.
- `getSourceGapWorkqueue()` exists in `explorer/src/api/graphApi.ts`.
- NodeInspector already shows node-specific `sourceGapWorkqueue` in the Context tab.
- `BackbonePreviewPanel` already has lazy-load sections for taxonomy readiness, placement QA, evidence summary, and pending improvement overlays.
- `ExplorerRail` owns request-id guarded lazy-load state for those preview sections.

## Constraints

- No active graph mutation.
- No Resource Layer mutation.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No pending overlay/source-link admission.
- Keep output dense and operator-focused.

## Likely Touchpoints

- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
