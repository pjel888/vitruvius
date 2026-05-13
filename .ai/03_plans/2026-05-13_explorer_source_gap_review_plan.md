# Plan: Explorer Source Gap Review Surface

## Objective
Expose source-grounding gap workqueue artifacts in Explorer so operators can see what still needs source evidence while inspecting a node.

## Implementation Plan
1. Add a read-only API payload builder in `api/index.ts` for `GET /v2/backbone/source-gap-workqueue`.
2. Resolve latest or explicit source-grounding inventory run, tolerate missing/partial files, and filter by `nodeId` when supplied.
3. Return summary counts, capped workqueue items, source-link proposals grouped by proposal id, artifact paths, and explicit safety boundaries.
4. Add Explorer types and a `getSourceGapWorkqueue` client function.
5. Extend `NodeInspector` Context tab with a compact source-gap review section that fetches by selected node id.
6. Add focused API/client/UI tests.
7. Update roadmap/state and write validation evidence.

## Plan Critique
- This does not solve source admission; it only improves operator visibility. That is intentional because source-link admission needs a separate governed steward workflow.
- A global workqueue dashboard would help later, but selected-node context gives immediate Explorer value with smaller UI blast radius.
- Filtering by node id may miss some indirect thematic source gaps. That is acceptable for the first Explorer surface because the workqueue itself still has global artifacts.

## Execution Checklist
- [ ] API route returns read-only payload when artifacts exist.
- [ ] API route returns safe empty payload when artifacts are missing.
- [ ] Node filtering includes direct node items and relationship items touching the node.
- [ ] Explorer client path is covered by tests.
- [ ] NodeInspector renders safety boundary and source proposal rows.
- [ ] Tests prove no admission/mutation flags are true.
- [ ] Validation report records exact test commands and results.
