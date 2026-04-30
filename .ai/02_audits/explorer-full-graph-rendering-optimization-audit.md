# Explorer Full-Graph Rendering Optimization Audit

Date: 2026-04-30

## UX preservation checklist
- App route remains `/explore` for Explorer.
- Command bar, Explorer rail, graph canvas, layout toolbar, minimap, query panel, preview/inspector rails, and bottom drawer remain in place.
- Search workflow remains unchanged.
- Node selection and selected-neighborhood emphasis remain direct-edge based.
- Pan/zoom controls remain unchanged.
- Optional context-menu focus-subgraph remains explicit and off-default.
- Default learner-facing filtering continues to exclude source/provenance/admin-only records from the render profile.
- Tailwind styling and `vis-network` renderer remain in use.

## Default full-graph contract audit
- API render profile returns 9,880 learner-facing nodes and 13,285 learner-facing edges.
- `VisNetworkHost.loadGraph` builds `visNodes` from all display nodes and `visEdges` from all unique edges.
- No default degree cap, show-more affordance, search-only graph slice, selected-neighborhood-only graph, or bounded visible subgraph is used in the default render path.
- `buildVisibleSubgraph` remains an explicit worker/index helper, not a default renderer input.
- Previous bounded-subgraph recommendation language was identified in `.ai/05_logs/2026-04-30_explorer_performance_optimization_validation.md` and corrected in this phase.

## Impact analysis
GitNexus impact checks were run for the touched symbols before edits:
- `loadGraph`: LOW risk; direct GraphScene process impact.
- `getCachedOrBuildPrecomputedNetworkLayoutPositions`: LOW risk; GraphScene/loadGraph impact.
- `buildPhysicsOptionsForGraph`: LOW risk; GraphScene/loadGraph impact.
- `readCachedNetworkLayoutPositions`: LOW risk; GraphScene/loadGraph impact.

No HIGH or CRITICAL impact warning was reported.
