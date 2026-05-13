# Plan â€” Explorer Source-Gap Detail Expansion

## Objective

Add expandable per-item source-gap details to the Explorer rail Source gaps card.

## Implementation Checklist

1. Add local expanded workqueue item state to `BackbonePreviewPanel`.
2. Build a `proposalById` lookup from `sourceGapPreview.proposals`.
3. Add a compact `Details` button for each rendered workqueue item.
4. When expanded, render:
   - workqueue ID, classification, status, final action, and priority score
   - node or relationship endpoint IDs
   - up to two matched proposals with title, relationship, score, matched terms, and rationale
   - a clear pending-only/read-only safety line
5. Keep layout dense and scoped to the existing rail card.
6. Extend `componentInteraction.test.tsx` to verify the detail panel opens and contains proposal rationale/matched terms.
7. Run focused Explorer test, Explorer build, diff check, code intelligence refresh, and GitNexus change detection.

## Non-Goals

- No graph mutation.
- No Resource Layer mutation.
- No source-link admission.
- No backend schema change.
- No database writes.
