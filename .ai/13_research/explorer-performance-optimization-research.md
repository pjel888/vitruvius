---
task: explorer-performance-optimization
phase: 03
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Explorer Performance Optimization Research Pack

## 01 — Discover

GitNexus status was current for `vitruvius` at commit `1e75fd4`. GitNexus queries mapped the relevant Explorer performance paths to:
- `api/index.ts`: `buildAecMepfsExplorerGraph`, `readAecMepfsBackboneGraphArtifacts`, `buildShadowBackboneSearchPreview`, `buildAecMepfsNodeDetail`, `buildAecMepfsExpandResult`, `buildAecMepfsPathResult`, `/perspective/:id/nodes`.
- `explorer/src/App.tsx`: `ExploreView` graph load lifecycle.
- `explorer/src/api/graphApi.ts`: `getNodesForPerspective`, `searchNodes`, `expandNode`, `tracePath`.
- `explorer/src/components/GraphScene.tsx`: graph canvas and toolbar wiring.
- `explorer/src/components/graph/VisNetworkHost.tsx`: vis-network load, layout, selection, hover, filtering, highlight, scene view, minimap snapshot.
- `explorer/src/components/CommandBar.tsx`: search input/result workflow.
- `explorer/src/stores/useSceneStore.ts`: Zustand view/selection/graph data state.

`code-review-graph` MCP was not exposed in this Codex surface; GitNexus CLI was used as the graph-first fallback.

## Current UX preservation checklist

The current Explorer UX/UI to preserve:
- Routes: `/` home and `/explore` graph workspace; URL params preserve `scene`, `perspective`, `node`, and `focus=search` behavior.
- Layout: top command bar, left Explorer rail, central graph canvas, right inspector rail, bottom drawer.
- Graph canvas: vis-network canvas inside `GraphScene`, existing dark KG styling and node/edge visual language.
- Toolbar controls: Select/Pan camera mode, zoom controls, fit, layout menu, physics pause/resume, query panel, spread slider, density presets, legend, minimap.
- Explorer rail: taxonomy tree, filters, visual settings, pinned nodes, AEC-MEPFS/source-clearance preview summaries.
- Search: command-bar input with debounced suggestions, keyboard navigation, result selection, URL update, inspector open, graph focus.
- Preview/inspector: selected node/edge details load in the inspector; source/evidence/query details use the bottom drawer.
- Node click: select node, open inspector; clicking outside clears; selecting outside the current selected direct visible neighborhood clears before selecting.
- Edge click: select edge and open inspector when supported by current graph view.
- Parent selection/highlight: selected node plus direct visible neighbors only; provenance/internal unconnected nodes must not be highlighted.
- Graph reset/clear: Escape and empty canvas clear selection; show-all clears hidden nodes; pan mode preserves selected node emphasis without selecting new nodes.
- Source-clearance display: AEC-MEPFS Backbone preview remains human-readable in the rail.
- Default learner-facing filtering: source/provenance/internal-only records and scaffold anchors remain hidden from ordinary learner-facing graph views unless explicitly supported by existing controls.
- Loading/empty/error states: existing overlays/messages remain unchanged.
- Tailwind styling: keep existing `kg-*` class patterns and no visual redesign.
- Tests: preserve `VisNetworkHost`, graph visual emphasis, command/search, preview panel, and inspector behavior.

Hard UX rule: Any visible behavior change must be explicit, justified, minimized, and tested. The intended changes are engine/data-contract optimizations only.

## Baseline summary

Baseline measured on 2026-04-30 using in-process Hono API fetches plus component helper timing:
- Nodes: 9,880
- Edges: 13,285
- Explorer graph response: 9,032,825 bytes, 8.61 MiB
- Shadow graph artifact: 5,367,411 bytes
- Staging artifact: 15,685,791 bytes
- Fetch `/perspective/aec-mepfs/nodes`: 126.66 ms
- Parse graph response: 17.22 ms
- First searchable graph proxy: 143.89 ms
- Search p50/p95: 14.98 / 28.43 ms
- Alias lookup p50/p95: 15.46 / 19.10 ms
- Selection neighborhood p50/p95: 0.29 / 0.33 ms
- Highlight reason batch p50/p95: 1.08 / 2.08 ms
- One-hop expansion p50/p95: 0.82 / 3.83 ms
- Two-hop expansion p50/p95: 1.10 / 6.07 ms
- Path query p50/p95: 2.77 / 4.30 ms
- Preview panel node detail p50/p95: 24.43 / 27.23 ms
- Heap delta after graph load: 43.07 MiB

Browser FPS/pan/zoom requires post-change browser smoke because the baseline script does not exercise real vis-network rendering.

---

# Follow-up Explorer Performance Optimization Research — 2026-04-30 UTC


## Initial research notes
- This phase is performance-only: preserve current Explorer UX and source-rights behavior.
- Baseline starts from 9,880 nodes / 13,285 relationships and shadow run 20260430T094129Z.
- Rust is a feasibility lane only until TypeScript graph indexing/worker benchmarks prove need.

## Acceptance criteria
- Measured baseline and after metrics.
- UX preservation checklist created.
- At least one real loading/index/search/highlight/render workload optimization.
- Regression assertions for performance/data-source/label/highlight correctness.
- Kimi advisory and final read-only audit.
