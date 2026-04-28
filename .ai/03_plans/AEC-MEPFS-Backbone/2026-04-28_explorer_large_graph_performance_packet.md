# AEC-MEPFS Explorer Large-Graph Performance Packet

```yaml
status: BOUNDARY_APPROVED
created: 2026-04-28
authority: project-owner-performance-optimization-request
scope: explorer-file-backed-aec-mepfs-large-graph-rendering
baseline_commit: 925f4963
run_id: 20260428T041000Z
node_count: 779
edge_count: 760
neo4j_mutation_authorized: false
kg_rebuild_reload_reset_authorized: false
protected_content_ingest_authorized: false
```

## Purpose

After expanding AEC-MEPFS to 779 nodes and re-enabling physics, the project owner
reported Explorer jank/slowness. This packet authorizes a focused Explorer
rendering optimization that preserves the full taxonomy and keeps physics
available while adding guardrails for large graphs.

## Allowed scope

- Optimize `explorer/src/components/graph/VisNetworkHost.tsx` large-graph
  behavior.
- Add small pure helper functions and tests for large-graph performance
  thresholds/options.
- Generate Explorer performance evidence under
  `006_System-Manifests/aec-mepfs-backbone/explorer-performance/`.
- Run Explorer tests, lint, build, and whitespace checks.

## Blocked scope preserved

- Do not reduce the 779-node / 760-edge taxonomy.
- Do not disable the AEC-MEPFS default graph.
- Do not mutate Neo4j or rebuild/reload/reset KG artifacts.
- Do not ingest or expose protected content.
- Do not introduce new dependencies.

## Implementation

- Add large-graph physics options that reduce continuous simulation cost:
  lower force, lower velocity, lower timestep, and fewer stabilization
  iterations for the 779-node graph.
- Auto-freeze physics after stabilization for large graphs so the graph settles
  but does not keep burning CPU indefinitely.
- Skip all-node hover dimming for large graphs, avoiding per-hover updates over
  779 nodes.
- Disable vis-network `improvedLayout` for large graphs and hide nodes during
  drag to reduce interaction jank.
- Keep small-graph behavior unchanged.

## Completion criteria

- Full Explorer tests pass.
- Explorer lint passes.
- Explorer build passes.
- New large-graph guardrail unit tests pass.
- Performance evidence report exists for run `20260428T041000Z`.
- Working tree is clean after commit and push.
