# Explorer UI Panels Tree Labels Context

Task: improve Explorer UI by widening the left panel, adding draggable/resizable left and right panels, adding expand-all/collapse-all controls for the tree, and adding filter controls to turn node text labels on/off by node type/all nodes.

Desired outcome:
- Left panel defaults to about 256px instead of feeling cramped.
- Left and right panels can be resized by dragging.
- Tree UI has expand all and collapse all buttons.
- Filter tab can toggle graph text labels for node types, so subtopic nodes can remain visible while their labels are hidden.
- Changes are verified with focused Explorer tests, lint, and build.

Constraints:
- Frontend-only Explorer UI change unless discovery proves otherwise.
- Preserve AEC-MEPFS graph data and runtime safety boundaries.
- Keep diffs focused and test-backed.

Likely touchpoints:
- explorer/src/App.tsx
- explorer/src/components/ExplorerRail.tsx
- explorer/src/components/InspectorRail.tsx
- explorer/src/components/explorer-rail/FiltersPanel.tsx
- explorer/src/components/graph/VisNetworkHost.tsx
- explorer/src/stores/useSceneStore.ts
- explorer/src/components/componentInteraction.test.tsx
- explorer/src/app.searchInspector.integration.test.tsx
- explorer/src/components/graph/VisNetworkHost.test.ts
