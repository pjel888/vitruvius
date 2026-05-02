# 15 — Backfill Strategy for Graph Nodes

## Why not backfill everything at once

Vitruvius currently has thousands of lower-level nodes. Trying to source-link every node in one pass will create noise. Use prioritized, loopable backfill.

## Priority signals

Rank nodes for backfill by user click frequency, graph centrality, number of edges, safety/importance, Architecture/Civil/Structural focus, missing resource coverage, poor existing description/provenance, node type criticality, local corpus match availability, and Kimi/human review availability.

## Backfill tiers

### Tier A — Critical/high-centrality nodes

Target first 25–100 nodes.

Examples:

- load path,
- foundation,
- beam,
- column,
- slab,
- retaining wall,
- site grading,
- stormwater drainage,
- accessible route,
- egress route,
- fire-rated wall,
- facade,
- roof,
- structural grid,
- soil bearing capacity,
- settlement.

Goal: 3–5 accepted resources each, at least one high-authority source where available, Kimi review for candidate batch.

### Tier B — Frequently clicked nodes

After instrumentation or usage data exists, prioritize actual user needs.

### Tier C — Rule/Procedure/Evidence nodes

As lower types are created, enforce no unsupported rules, no unsupported evidence claims, and procedure sources for Procedure nodes.

### Tier D — Long-tail Concept nodes

Backfill in batches by taxonomy/subtopic.

## Batch workflow

```text
Select batch of 25 nodes
  → build search queries
  → local corpus search
  → curated source search
  → API search
  → candidate normalize/dedupe
  → preliminary ranking
  → Kimi review top candidates
  → accept/reject/needs_review
  → write NodeResourceLinks
  → validate
  → update metrics
```

## Batch size recommendations

- Infrastructure batches: one feature area per loop.
- Source backfill batch: 10–25 nodes if using Kimi review.
- Local corpus matching batch: 25–100 nodes if automated, then review high-confidence only.
- Rule node batch: 5–10 nodes due to high review burden.

## Coverage targets

Initial:

```text
Top 25 eligible nodes: >= 3 accepted resources each
```

Next:

```text
Top 100 Architecture/Civil/Structural Concept nodes: >= 3 accepted resources each
```

Longer term:

```text
80% of user-clicked eligible nodes: >= 3 accepted resources
All Rule nodes: >= 1 primary/high-authority source
All Evidence nodes: >= 1 evidence-bearing source
All Document nodes: complete metadata
```

## When to create Document nodes

Create a Document graph node when a Resource is reused across many nodes, central to a discipline/taxonomy, a standard/guideline/manual/report/textbook, important enough to query as a graph object, and connected to multiple rules/procedures/evidence nodes. Do not create Document nodes for every webpage.

## When to create Definition/Rule/Procedure/Evidence nodes

Only create them when source-backed.

Examples:

- formal definition from a professional source → Definition node,
- design/code/professional constraint → Rule node,
- documented workflow → Procedure node,
- caveat or alternative condition → Exception node,
- research-backed claim → Evidence node.

## Source gaps

If no good source is found, do not force low-quality links. Mark as a source gap and log attempted searches, best rejected candidate, reason, and recommended next action.

## Preventing resource spam

For a normal Concept node, target one primary explanatory source, one professional/design source, one local/book source, one evidence source if relevant, and one classification source if useful.

## Backfill quality report

Each batch should report nodes processed, candidates found, candidates accepted/rejected/needs-review, average resources per node, source type distribution, authority tier distribution, Kimi decisions, validation results, and unresolved gaps.
