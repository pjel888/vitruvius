# Graph Relationship Visibility Loop Progress

Date: 2026-05-01
Status: Implementation and validation pass in progress

## Task intent

Fix the Explorer graph so ontology relationships in the file-backed AEC-MEPFS graph are visible or explicitly disclosed instead of being silently hidden by UI filters or missing endpoint hydration. Preserve the Resource Layer reviewer workflow and avoid broad backfill or fake resources.

## Repository diagnosis findings

1. Graph nodes are served from the active AEC-MEPFS shadow graph artifact: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json`.
2. The active graph has 10,018 nodes and 13,670 edges.
3. Edge data is stored as shadow graph edge rows with `from_id`, `to_id`, `predicate`, optional relation metadata, and API-mapped render `type` values.
4. Hierarchy and semantic relationships are mixed in the same edge artifact. The dominant hierarchy edge is `HAS_CHILD`; semantic edges include `HAS_FACET`, `MAPS_TO_EXTERNAL_STANDARD`, `REQUIRES`, `CONSTRAINS`, `GOVERNS`, `PART_OF`, and others.
5. The selected-node inspector uses `/node/:id`, which is built from the same AEC-MEPFS Explorer graph index and includes incoming and outgoing relationships.
6. The graph canvas receives the perspective graph from `/perspective/aec-mepfs/nodes?profile=render` and applies frontend node/edge filters before rendering.
7. The root cause was not missing graph data. It was frontend visibility/filter divergence: static edge filters omitted real AEC semantic edge types, and filter reconciliation only reset filters when there was no intersection. Because `HAS_CHILD` existed, semantic types like `HAS_FACET` stayed hidden.
8. Scene/query subsets could also diverge because query and expansion results were merged into the canvas controller but not always into the persistent scene store, and selected-node direct endpoint hydration did not occur.
9. Existing relationship list and graph canvas were therefore not guaranteed to agree: the inspector could list a relationship that the graph filtered or failed to hydrate.
10. Exact regression case exists in the active graph: `VTN-DOM-0012495` Sendai Mediatheque and `VTN-DOM-0012436` Toyo Ito are connected by `VTN-DOM-0012436--has_facet--VTN-DOM-0012495` (`HAS_FACET`, semantic/person-work).

## Implemented changes

### Backend/API

- Added `api/graph/relationshipVisibility.ts`:
  - normalizes graph relationships into one canonical service representation;
  - classifies edges as hierarchy or semantic;
  - builds selected-node neighborhoods with hydrated endpoint nodes;
  - reports hidden relationship reasons when filters exclude relation types/categories;
  - validates broken edge references and duplicate edge IDs;
  - detects duplicate canonical-label candidates for steward review without mutating graph data.
- Added `GET /node/:id/neighborhood` for AEC-MEPFS nodes:
  - supports `depth`, `limit`, `direction`, `relTypes`, `includeHierarchyEdges`, and `includeSemanticEdges`;
  - returns nodes, edges, normalized relationships, direct counts, hidden relationships, and truncation status.
- Updated `/node/:id` relationship details so incoming/outgoing relation rows include relationship ID, source/target IDs, category, and semantic/hierarchy flags.
- Kept compact render graph payload bounded; extra relation metadata is exposed through detail/neighborhood routes rather than bloating default render edges.
- Added `api/validateGraphRelationships.ts` validation and duplicate report generation.

### Explorer/UI

- Added `getNodeNeighborhood` client helper.
- Added scene-store `mergeGraphData` helper so query/expand/hydration results update the canonical Explorer store instead of only the canvas controller.
- Changed graph-load filter reconciliation to union actual available node and edge types into the active filter sets, preventing new AEC edge types from being silently hidden.
- Changed Explorer filter rail to show dynamic edge types from the loaded graph, so `HAS_FACET`, `MAPS_TO_EXTERNAL_STANDARD`, `GOVERNS`, etc. are user-toggleable.
- On selected-node changes, Explorer fetches and merges the node's 1-hop direct neighborhood when not in a saved scene.
- NodeInspector relationship tab now shows direct relationship counts, semantic/hierarchy counts, hidden counts, per-relationship visible/hidden badges, and a `Show all direct relationships` action.
- Relation row click reveals needed filters, clears isolation, selects the related node, and requests focus.
- Node context menu now includes `Expand direct relationships` and expansion/query merge paths update the scene store.

## Duplicate/canonicalization findings

- No duplicate nodes were auto-merged.
- `api/validateGraphRelationships.ts` generated `.ai/13_research/graph_duplicate_canonicalization_report.md`.
- Validation found 544 duplicate normalized-label groups in the active graph, of which 251 appear structurally safer review candidates and 293 require manual steward review.
- Concrete-specific findings:
  - `concrete`: `VTN-DOM-0000068`, `VTN-DOM-0000267` queued for review, not auto-merged.
  - `reinforced concrete`: `VTN-DOM-0000271`, `VTN-DOM-0012147` queued for review, not auto-merged.
- This preserves the user's goal of canonical concepts while respecting the no-reckless-merge rule.

## Kimi review status

- Diagnosis review attempt with a long prompt timed out after 184 seconds.
- Short no-tools diagnosis review succeeded. Accepted corrections: keep selected-neighborhood fetch bounded, ensure full endpoint hydration, add validation against type-registry drift, and avoid hiding inspector/canvas source divergence.
- Short no-tools implementation review succeeded. Accepted corrections: preserve bounded default render payloads, keep neighborhood route limited/truncated, ensure store merges dedupe by ID, and defer unsafe duplicate merges.
- Rejected/deferred Kimi suggestions are recorded in the final report.

## Validation run so far

- `cd api; bun test` passed: 134 pass, 0 fail.
- `cd explorer; bun test` passed: 108 pass, 0 fail.
- `cd explorer; bun run build` passed with existing Vite chunk-size warning.
- `bun run api/validateGraphRelationships.ts` passed: 0 broken relationship issues, 3,676 semantic edges detected.
- `bun run api/validateResourceLayer.ts` passed with expected two warnings for standards missing edition/version context and no blockers.

## Remaining steps in this loop

1. Run final validation commands after report/state updates.
2. Run post-implementation code-intelligence refresh and change-impact checks.
3. Run final Kimi critique with validation evidence.
4. Update final report, validation log, and decisions ledger.
