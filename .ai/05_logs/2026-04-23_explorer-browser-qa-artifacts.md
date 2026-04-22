---
task: explorer-browser-qa-artifacts
phase: meta
created: 2026-04-23
author: Hephaestus
status: COMPLETE
---

# Explorer Browser QA Artifacts — 2026-04-23

These artifacts were captured against the running explorer at `http://localhost:5173` after commit `3b42836` was pushed.

## Search CTA focus proof

```json
{
  "activeId": "command-search-input",
  "activePlaceholder": "Search nodes and taxonomies...",
  "url": "http://localhost:5173/explore"
}
```

## Sample graph preload network proof

```text
[GET] http://localhost:3000/perspective/default/nodes => [200] OK
```

This was captured immediately after clicking `Show sample graph`, supporting the claim that the preloaded graph path issued a single visible request for the default perspective.

## Home-screen console error check

```text
Total messages: 3 (Errors: 0, Warnings: 0)
Returning 0 messages for level "error"
```

## Empty query runtime proof

Observed from the running query panel after executing:

```cypher
MATCH (n) WHERE n.id = "definitely-not-a-real-node" RETURN n LIMIT 5
```

Runtime result object:

```json
{
  "summary": "No rows returned · graph unchanged",
  "emptyState": "This query returned no rows to display."
}
```

## Local screenshot artifacts captured during QA

These files were captured locally during QA and were intentionally left out of the repo commit because they are binary session artifacts rather than durable source records:

- `search-cta-focus.png`
- `sample-graph-view.png`
- `empty-query-result.png`
