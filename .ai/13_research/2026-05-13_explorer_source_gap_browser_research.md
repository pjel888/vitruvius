# Explorer Source-Gap Browser Research - 2026-05-13

## Research Inputs

- GitNexus query: `BackbonePreviewPanel ExplorerRail source gap workqueue preview`
- GitNexus impact:
  - `BackbonePreviewPanel`: LOW, 0 upstream dependents reported
  - `ExplorerRail`: LOW, 0 upstream dependents reported
  - `getSourceGapWorkqueue`: not found by symbol index, but route/client tests already cover the helper
- ChunkHound regex search over `explorer/src/components` for existing preview and overlay panel patterns
- Local reads of:
  - `explorer/src/components/ExplorerRail.tsx`
  - `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
  - `explorer/src/components/componentInteraction.test.tsx`
  - `explorer/src/api/graphApi.ts`

## Findings

1. `ExplorerRail` already owns lazy-load state and request-id guards for Backbone summary, taxonomy readiness, placement QA, evidence summary, and improvement overlays.
2. `BackbonePreviewPanel` already accepts preview payloads and load callbacks as props and renders compact section cards.
3. `getSourceGapWorkqueue()` already supports unfiltered graph-wide loading when called with no `nodeId`, plus optional `limit`.
4. The right UX fit is another lazy-load section inside the AEC-MEPFS rail preview, not a new route or page.
5. The section should show high-signal counts, top gap items, top suggested resources, run ID, and safety boundaries.

## Blast Radius

Expected files:

- `ExplorerRail.tsx`: add source-gap preview state, request guard, lazy-load function, and props.
- `BackbonePreviewPanel.tsx`: add props, toolbar button, section rendering.
- `componentInteraction.test.tsx`: add sample preview and UI assertions.

Risk level is LOW because this is read-only UI, route already exists, and changes remain inside Explorer preview components.
