# Explorer Source-Gap Browser Plan - 2026-05-13

## Goal

Add a graph-wide Explorer rail browser for source-grounding gaps and source-link proposals, using the existing read-only `GET /v2/backbone/source-gap-workqueue` API preview.

## Acceptance Criteria

- Explorer rail has a lazy-load source-gap preview control.
- The preview renders:
  - total workqueue items;
  - returned workqueue items;
  - node resource gaps;
  - relationship source gaps;
  - source-link proposals;
  - latest run ID;
  - top ranked workqueue items;
  - top suggested resources.
- UI explicitly says the surface is review-only and does not mutate graph/Resource Layer/databases.
- Existing selected-node source-gap panel remains unchanged.
- Tests assert the new rail section renders counts, top item/resource labels, and safety copy.

## Implementation Steps

1. Extend `ExplorerRail` with source-gap preview state, request id, lazy-load function, reset on backbone refresh, and `BackbonePreviewPanel` props.
2. Extend `BackbonePreviewPanel` props and toolbar with a source-gap control.
3. Add a compact "Source gaps" card that reuses existing count/card styling and renders up to a few top rows/resources.
4. Add or update component interaction tests.
5. Run focused Explorer tests and build.

## Non-Goals

- No Resource Layer link creation.
- No active graph mutation.
- No source-link admission workflow.
- No new API route.
- No database writes.
