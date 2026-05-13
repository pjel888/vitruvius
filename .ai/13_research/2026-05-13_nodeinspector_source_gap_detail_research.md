# Research Pack â€” NodeInspector Source-Gap Detail

## Evidence Gathered

- GitNexus impact for `NodeInspector` returned LOW risk and no upstream impacted symbols.
- GitNexus query for `NodeInspector source gap workqueue context tab` located:
  - `explorer/src/components/inspector/NodeInspector.tsx`
  - related Resource review and context flows
- Existing `SourceGapWorkqueuePanel` already had:
  - source-gap item list
  - suggested Resource hints
  - `proposalById` lookup
  - proposal ID display

## Inference

The selected-node Context tab could show the same proposal details already available in the bounded API payload without changing backend contracts or adding admission behavior.
