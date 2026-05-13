# Context Snapshot â€” NodeInspector Source-Gap Detail

## Task

Continue the Explorer source-grounding UX by bringing detailed source-gap proposal inspection into the selected-node Context tab.

## Desired Outcome

When a user opens a node and switches to Context, the Source Gap Workqueue panel should expose proposal rationale, matched terms, target identifiers, and safety status for source-link suggestions that touch that node.

## Evidence

- `NodeInspector` already renders `SourceGapWorkqueuePanel`.
- The panel currently shows Resource hints and proposal IDs, but not proposal details.
- GitNexus impact for `NodeInspector` is LOW.

## Constraints

- No graph mutation.
- No Resource Layer mutation.
- No source-link admission.
- No Neo4j/Postgres writes.
- No protected source text, API keys, or `reasoning_content`.
