# Explorer Source-Gap Filtering Plan - 2026-05-13

## Goal

Add read-only local filters to the graph-wide Source gaps rail browser.

## Steps

1. Add local state to `BackbonePreviewPanel` for source-gap filter mode.
2. Render compact filter buttons for all/node/relationship gaps.
3. Filter displayed workqueue rows locally while keeping counts visible.
4. Add component test assertions for filter behavior.
5. Run focused Explorer tests and build.

## Safety

The filter changes display only. It does not mutate graph data, Resource Layer records, source-link proposals, or databases.
