# Audit â€” NodeInspector Source-Gap Detail

## Current State

`NodeInspector` displays source-grounded context and node-specific source-gap workqueue rows. Before this slice, the source-gap panel exposed Resource hints and proposal IDs but did not show proposal rationale, matched terms, or target identifiers.

## Gap

When an operator clicks a node, the selected-node Context tab should be sufficient for inspection. Showing only proposal IDs forces the operator back to JSONL artifacts or the rail detail view.

## Blast Radius

Low:

- `SourceGapWorkqueuePanel` is local to `NodeInspector.tsx`.
- No API route or data schema change is needed.
- Existing component interaction tests already cover the Context tab.

## Safety

The proposed change is display-only. It must not add approve/apply/admit controls.
