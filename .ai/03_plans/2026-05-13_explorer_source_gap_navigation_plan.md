# Explorer Source-Gap Navigation Plan - 2026-05-13

## Goal

Add read-only navigation actions to source-gap workqueue rows in the AEC-MEPFS rail preview.

## Steps

1. Add an optional `onOpenSourceGapNode(nodeId)` prop to `BackbonePreviewPanel`.
2. Render compact action buttons for node gaps and relationship endpoints.
3. Wire `ExplorerRail` to select and route to the clicked node.
4. Add component tests for the buttons and callback payloads.
5. Run focused Explorer tests and build.

## Safety

This changes UI navigation only. It does not add any mutation, admission, Resource Layer, Neo4j, or Postgres write path.
