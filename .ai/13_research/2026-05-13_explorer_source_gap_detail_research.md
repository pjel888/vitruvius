# Research Pack â€” Explorer Source-Gap Detail Expansion

## Evidence Gathered

- GitNexus query for `BackbonePreviewPanel source gap workqueue Explorer rail` identified:
  - `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
  - `explorer/src/components/ExplorerRail.tsx`
  - `explorer/src/components/inspector/NodeInspector.tsx`
- GitNexus impact for `BackbonePreviewPanel`:
  - upstream impacted count: `0`
  - risk: `LOW`
- ChunkHound regex search confirmed the source-gap UI is currently concentrated in:
  - `ExplorerRail.tsx`
  - `BackbonePreviewPanel.tsx`
  - `NodeInspector.tsx`

## Existing Data Available In The Preview

`SourceGapWorkqueueItem` includes:

- `workqueueId`
- `itemType`
- `sourceBackingStatus`
- `classification`
- node or relationship endpoint IDs and labels
- `degree`
- `priorityRank`
- `priorityScore`
- `proposalIds`
- `suggestedResources`
- pending-only safety booleans

`SourceLinkProposal` includes:

- `proposalId`
- target node/edge identifiers
- `resourceId`
- `title`
- `score`
- `matchedTerms`
- `suggestedRelationship`
- `rationale`
- review/safety booleans

## Inference

The UI can become more operationally useful without new backend or graph behavior by joining `item.proposalIds` against `sourceGapPreview.proposals` in the component and rendering a collapsible detail block.
