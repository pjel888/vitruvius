# Explorer Source Gap Review Context

## Task
Continue the autonomous improvement loop by making source-grounding gaps from the AEC relationship/node campaigns visible in Explorer.

## Desired Outcome
- Operators can click an AEC node in Explorer and see related source-grounding gap workqueue items and source-link proposals.
- The surface is read-only and review-only.
- No active graph, Resource Layer, Neo4j, or Postgres mutation is introduced.

## Known Evidence
- `aec-source-grounding-inventory` now writes `source-grounding-gap-workqueue.jsonl` and `source-link-proposals.jsonl`.
- Latest smoke artifact: `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/SOURCE_GAP_WORKQUEUE_SMOKE_FINAL/`.
- Existing Explorer/API source context path: `POST /v2/answer/context`, `GET /node/:id`, and `NodeInspector` Context tab.
- Existing pending overlay path: `GET /v2/backbone/improvement-overlay`.

## Constraints
- Pending-only and proposal-only semantics remain intact.
- Do not admit source links, relationships, or node consolidations.
- Do not expose protected source payload text.
- Do not write databases.
- Preserve Explorer usability on large graphs.

## Touchpoints
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/inspector/NodeInspector.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `.ai` roadmap/state/validation documents

## Open Questions
- Whether to expose a global source-gap panel later. Current slice keeps the UX scoped to selected-node inspection.
