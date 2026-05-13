# Context Snapshot â€” Explorer Source-Gap Detail Expansion

## Task

Continue improving the Explorer AEC-MEPFS source-gap workflow after adding the graph-wide rail browser, node navigation, and node/relationship filters.

## Desired Outcome

Operators should be able to expand a source-gap workqueue row in the Explorer rail and inspect the review-relevant details in place:

- priority, classification, source backing status, and final action
- affected node or relationship endpoint IDs
- resource hints with matched terms and score
- matching source-link proposal metadata and rationale
- explicit pending-only/read-only safety status

## Known Facts

- `GET /v2/backbone/source-gap-workqueue` already returns bounded, sanitized preview data.
- `BackbonePreviewPanel` already renders a graph-wide Source gaps card and can jump to affected node endpoints.
- The preview is read-only and must not create Resource links, admit claims, mutate graph files, or write databases.
- GitNexus scoped impact for `BackbonePreviewPanel` is LOW.

## Constraints

- No active graph mutation.
- No Resource Layer mutation.
- No pending overlay admission.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No API key or `reasoning_content` handling.
- Keep changes scoped to Explorer UI and tests unless validation exposes a defect.

## Likely Touchpoints

- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
