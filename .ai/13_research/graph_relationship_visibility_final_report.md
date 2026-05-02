# Graph Relationship Visibility Final Report

Date: 2026-05-01
Status: Implemented and locally validated

## 1. Summary of bug/root cause

The graph data was not missing the user's example relationship. The active AEC-MEPFS shadow graph contains `VTN-DOM-0012436--has_facet--VTN-DOM-0012495`, connecting Toyo Ito to Sendai Mediatheque through a semantic `HAS_FACET` person-work edge.

The Explorer UI hid the relationship because its edge filters were seeded from a static edge-type list that did not include the real AEC-MEPFS semantic edge types. Filter reconciliation only reset filters when there was no overlap. Since `HAS_CHILD` overlapped, semantic relationships such as `HAS_FACET`, `MAPS_TO_EXTERNAL_STANDARD`, `GOVERNS`, `REQUIRES`, and `CONSTRAINS` remained filtered out, while the inspector could still list them from node detail data.

A secondary issue was hydration/store divergence: query and expansion paths could merge nodes/edges into the canvas without updating the canonical Explorer store, and selected-node direct relationship endpoints were not fetched when a selected relationship target was outside the currently visible subset.

## 2. Files changed

### Backend/API

- `api/graph/relationshipVisibility.ts` - new normalized relationship, neighborhood, validation, and duplicate-candidate utilities.
- `api/index.ts` - added selected-node neighborhood API route and normalized relationship metadata on node detail relationships.
- `api/validateGraphRelationships.ts` - new graph relationship validation and duplicate-canonicalization report writer.
- `api/graphRelationshipVisibility.test.ts` - new relationship normalization, hidden-reason, broken-reference, and duplicate-detection tests.
- `api/v2Backbone.test.ts` - added Sendai Mediatheque / Toyo Ito neighborhood regression and detail/neighborhood consistency coverage.

### Explorer/UI

- `explorer/src/types/index.ts` - added graph neighborhood and extended relationship detail types.
- `explorer/src/api/graphApi.ts` - added `getNodeNeighborhood` client helper.
- `explorer/src/api/graphApi.test.ts` - added client contract coverage for the neighborhood route.
- `explorer/src/stores/useSceneStore.ts` - added ID-based `mergeGraphData` store helper.
- `explorer/src/App.tsx` - added selected-node 1-hop hydration and dynamic filter reconciliation.
- `explorer/src/components/ExplorerRail.tsx` - added dynamic edge type discovery for filter controls.
- `explorer/src/components/inspector/NodeInspector.tsx` - added hidden relationship counts, semantic/hierarchy badges, visible/hidden reason badges, and reveal controls.
- `explorer/src/components/componentInteraction.test.tsx` - added NodeInspector hidden semantic relationship/reveal test.
- `explorer/src/components/graph/NodeContextMenu.tsx` - added direct relationship expansion and store merge for expansions.
- `explorer/src/components/graph/QueryPanel.tsx` - merged query results into the canonical store.
- `explorer/src/app.searchInspector.integration.test.tsx` - updated mocked API surface for neighborhood hydration.

### Reports/logs

- `.ai/13_research/graph_relationship_visibility_loop_progress.md`
- `.ai/13_research/graph_relationship_visibility_final_report.md`
- `.ai/13_research/graph_duplicate_canonicalization_report.md`
- `.ai/05_logs/2026-05-01_graph_relationship_visibility_loop.md`
- `.ai/10_state/decisions.md`

## 3. Data path before/after

### Before

1. Raw graph data included both hierarchy and semantic edges.
2. `/node/:id` relationship details could expose incoming/outgoing semantic relationships.
3. `/perspective/aec-mepfs/nodes?profile=render` provided a compact graph to the Explorer canvas.
4. Frontend filters were seeded from a static edge-type list and omitted many real AEC-MEPFS edge types.
5. Canvas rendering and inspector relationships could disagree: inspector listed relationships that the canvas silently filtered out.
6. Query/expand canvas merges did not always update the canonical scene store, creating additional divergence risk.

### After

1. Raw graph data is normalized by `relationshipVisibility.ts` for relationship category, direction, endpoints, and hidden reasons.
2. `/node/:id` detail relationships include relationship IDs, source/target IDs, category, and semantic/hierarchy flags.
3. `/node/:id/neighborhood` returns the selected node, hydrated direct endpoint nodes, direct incoming/outgoing edges, normalized relationships, counts, and hidden reasons.
4. Explorer graph-load reconciliation unions actual available node and edge types into filters so real relationship types are not silently suppressed.
5. The Explorer rail exposes dynamic edge types from the loaded graph.
6. Node selection triggers 1-hop direct relationship hydration for the active graph when not editing a saved scene.
7. Query/expand/neighborhood results merge by ID into the canonical store.
8. NodeInspector discloses hidden relationship counts and reasons and can reveal/focus direct relationships.

## 4. What now happens when selecting a node

When a user selects a node, the Explorer requests its direct neighborhood through `/node/:id/neighborhood` and merges any missing direct endpoint nodes/edges into the graph store. The selected node remains highlighted. The relationship tab shows the total direct relationship count, semantic count, hierarchy count, and hidden count if current filters or isolation still hide a relationship. Each relationship row indicates whether it is currently visible in the graph or hidden by a specific reason such as edge type, node type, or isolation. Clicking a relationship reveals the necessary filters, clears isolation, selects the related node, and focuses it.

## 5. Hidden relationships

Hidden relationships are no longer silently dropped in the inspector. They are counted and annotated with reasons. The user can use `Show all direct relationships` to add the relationship edge types and related node types to the active filters and request graph focus. High-degree nodes remain bounded by the neighborhood route limit and truncation flag rather than unboundedly expanding the graph.

## 6. Semantic and hierarchy edges

The normalizer classifies edges as hierarchy or semantic. `HAS_CHILD` and hierarchy-marked edges are hierarchy. Cross-link and domain-specific edges such as `HAS_FACET`, `MAPS_TO_EXTERNAL_STANDARD`, `GOVERNS`, `REQUIRES`, `CONSTRAINS`, and non-hierarchy `PART_OF` are available as semantic/cross-link relationships. The UI exposes dynamic edge type filters so semantic edge types can be toggled directly.

## 7. Duplicate/canonicalization findings

The loop added duplicate detection but performed no automatic merges. This is intentional: the graph contains many repeated labels across different taxonomy contexts, and reckless merging would damage ontology meaning.

Validation generated `.ai/13_research/graph_duplicate_canonicalization_report.md` with:

- duplicate normalized-label groups: 544
- structurally safer review candidates: 251
- unsafe/manual-review candidates: 293
- concrete-related duplicate groups: 2

Concrete findings:

- `concrete`: `VTN-DOM-0000068`, `VTN-DOM-0000267` - queued for steward review.
- `reinforced concrete`: `VTN-DOM-0000271`, `VTN-DOM-0012147` - queued for steward review.

No canonical labels, aliases, node-resource links, or edge endpoints were mutated.

## 8. Specific results

### Sendai Mediatheque / Toyo Ito

Present and covered by regression test:

- Sendai Mediatheque: `VTN-DOM-0012495`
- Toyo Ito: `VTN-DOM-0012436`
- Edge: `VTN-DOM-0012436--has_facet--VTN-DOM-0012495`
- Edge type: `HAS_FACET`
- Category: semantic

`GET /node/VTN-DOM-0012495/neighborhood?depth=1&direction=both` now returns the Toyo Ito node and the connecting edge. `/node/VTN-DOM-0012495` incoming relationship details also include the same relationship ID and semantic classification.

### Building

The active graph has a hierarchy edge connecting the Building work bucket to Sendai Mediatheque:

- `VTN-DOM-0000757--broader_than--VTN-DOM-0012495`
- API edge type: `HAS_CHILD`

The fix does not need fake edges to connect Building to Toyo Ito. Instead, selecting Sendai Mediatheque reveals the direct semantic Toyo Ito relationship; selecting Building can traverse to Sendai through hierarchy and then to Toyo Ito through semantic relationship hydration.

### Concrete

Concrete-like nodes exist, but obvious safe merge was not performed because duplicate label groups span multiple IDs and contexts. The duplicate report identifies exact candidate IDs for steward review and keeps genuinely distinct concrete concepts such as reinforced concrete, concrete formwork, concrete quality, concrete slab, and concrete materials separate unless future review authorizes aliasing or merging.

## 9. Tests added/updated

- Normalized relationship service test: all direct incoming/outgoing relationships with hydrated endpoint nodes.
- Hidden relationship reason test: semantic edges hidden by filters report explicit hidden reasons.
- Broken edge reference validation test.
- Duplicate canonical detection test.
- Sendai Mediatheque / Toyo Ito API regression test.
- Node detail vs neighborhood relationship consistency assertion.
- Explorer API route contract for `getNodeNeighborhood`.
- NodeInspector UI test for hidden semantic relationships and reveal action.
- Existing Resource Layer tests continue to pass.

## 10. Validation added

`api/validateGraphRelationships.ts` checks active graph node/edge consistency and writes duplicate review output. It validates:

- every edge source node exists;
- every edge target node exists;
- no duplicate edge IDs;
- selected-edge normalization categories are available;
- hierarchy and semantic edge counts are measured;
- duplicate canonical labels and concrete duplicate candidates are reported for review.

## 11. Commands run

```bash
bash ./scripts/refresh_code_intelligence.sh
bun test api/graphRelationshipVisibility.test.ts
bun test api/v2Backbone.test.ts
cd api && bun test
cd explorer && bun test
cd explorer && bun run build
bun run api/validateGraphRelationships.ts
bun run api/validateResourceLayer.ts
```

Post-implementation code-intelligence refresh and change-impact checks were run after final file updates; results are recorded in the final response.

## 12. Test/build/validation results

- `cd api; bun test`: 134 pass, 0 fail.
- `cd explorer; bun test`: 108 pass, 0 fail.
- `cd explorer; bun run build`: passed; Vite emitted existing chunk-size warnings.
- `bun run api/validateGraphRelationships.ts`: `ok: true`, 0 broken relationship issues, 9,994 hierarchy edges, 3,676 semantic edges, duplicate report generated.
- `bun run api/validateResourceLayer.ts`: `ok: true`, blockers `[]`, expected standards context warnings retained.

## 13. Kimi review summary

### Diagnosis review

A long Kimi diagnosis prompt timed out after 184 seconds. A shorter no-tools review succeeded.

Kimi flagged:

- possible N+1 selection fetches;
- need to hydrate both endpoints of visible/direct edges;
- dynamic filter performance concerns;
- type registry drift between loader and filter UI;
- inspector/canvas source split;
- hidden badge clutter;
- depth ambiguity;
- risk that revealing semantic edges changes graph density.

Accepted:

- selected-node hydration uses an explicit bounded 1-hop route;
- endpoint nodes are returned with direct edges;
- hidden reasons are aggregated in the relationship tab and per relationship;
- validation detects broken relationships and duplicate canonical labels;
- default render payload remains compact.

Deferred/rejected:

- Broad initial rendering of every relationship without progressive disclosure was rejected for performance and readability.
- Hard ontology allowlisting of dynamic edge controls is deferred; current active edge types are governed AEC-MEPFS relation types, but future system/internal relation categories should be grouped/allowlisted.

### Implementation review

Kimi flagged:

- high-degree node payload limits;
- dynamic type allowlisting;
- store merge dedupe by canonical IDs;
- avoiding resource-layer schema regression;
- reason-specific badge clarity;
- not running whole-graph validation inside synchronous request paths;
- partial normalization risks;
- stale response store merge risk.

Accepted:

- `/node/:id/neighborhood` is bounded and returns truncation state.
- Store merge dedupes by node/edge ID.
- Whole-graph validation is a script, not a request-path operation.
- Resource Layer routes and tests were run as regressions.

Deferred:

- Stronger user-facing edge-type grouping/allowlisting.
- Response-version protection for concurrent optimistic graph edits; current Explorer graph editing is local/dev and non-production.

### Final review

Kimi's final no-tools review concluded that the relationship visibility fix addresses UI masking and selected-node hydration, but it does not complete canonical integrity because 544 duplicate normalized-label groups remain unmerged. Kimi flagged that duplicate fragmentation can still split neighborhoods, pathfinding, centrality, and semantic reasoning even when the UI now reveals direct edges. Kimi also flagged dynamic filter default risk and high-degree hydration risk.

Accepted:

- Do not claim canonical duplicate issues are solved by this loop.
- Treat duplicate/canonical stewardship as the mandatory next loop.
- Keep this loop's result scoped to visibility, hydration, consistency signals, validation, and duplicate reporting.

Deferred:

- Actual duplicate merge/alias application remains blocked until a steward-reviewed merge workflow exists.
- Broader regression coverage across duplicate groups should be added in the duplicate stewardship loop.

## 14. Resource Layer regression status

Resource Layer behavior was preserved:

- No broad backfill was performed.
- No fake URLs/resources/files were added.
- No local files were auto-linked.
- No candidates were promoted.
- ASCE/FHWA needs-review records were not promoted.
- ACI broad mapping remains rejected.
- WBDG remains contextual guidance.
- Resource Layer API tests passed as part of `cd api; bun test`.
- `bun run api/validateResourceLayer.ts` passed with expected warnings and no blockers.

## 15. Remaining gaps

1. Dynamic edge controls should eventually be grouped by ontology category and hide any future system/internal-only edge types from learner-facing filters.
2. Duplicate canonical-label report needs a reviewer workflow and steward decision packet before any safe merge/alias application.
3. High-degree nodes may need UI pagination for direct-neighborhood expansion if future graph enrichment creates very large ego networks.
4. Scene-mode selected-node hydration is intentionally skipped to avoid mutating saved scenes unexpectedly; a future scene-safe reveal workflow could add an explicit opt-in.
5. Search canonicalization still needs a steward-reviewed alias/canonical map before automatically redirecting duplicates such as concrete.

## 16. Recommended next loop

Build a graph steward workflow for duplicate/canonical candidate review:

- render duplicate groups with labels, taxonomy context, descriptions, edge counts, and resource links;
- support merge/alias/keep-separate decisions in dry-run mode;
- validate preservation of all incoming/outgoing edges and Resource Layer node links;
- only apply safe decisions after explicit steward approval;
- add canonical search preference based on approved steward decisions.

