# Context Snapshot - Explorer Full-Graph Rendering Optimization

## Task statement
Optimize the Vitruvius Explorer full learner-facing graph rendering/stabilization path. Correct the prior next-step language that suggested bounded visible subgraph default rendering. The default Explorer must render the full learner-facing graph, not a sliced/subgraph/neighborhood/search-only/degree-capped subset.

## Desired outcome
The Explorer still feels like the same app and renders all learner-facing nodes/edges by default, but full-graph render/stabilization and warm-load behavior are faster and regression-protected.

## Known facts/evidence
- Previous performance commit: 608def8a, `Make Explorer graph interactions fast without changing the interface`.
- Current clean render graph from previous validation: 9,880 nodes / 13,285 edges, render payload 4.72 MiB.
- Previous API/index/search work met query targets; remaining bottleneck is vis-network full-graph rendering/stabilization/layout.
- Worker `loadFromUrl` avoids structured-cloning graph object from React to worker.
- Chrome headless smoke passed previously; Kimi audit passed; Codex Spark not used.

## Constraints
- Full learner-facing graph must remain the default renderer dataset.
- Do not introduce bounded subgraph default, degree caps, show-more, cluster-only default, search-only graph slices, or hidden ordinary learner-facing nodes.
- Preserve current UX/UI, Tailwind styling, Zustand, React Query, vis-network initially.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, destructive graph operations, protected source ingestion, fake benchmarks, fake browser/manual results, or Codex Spark.
- Use Kimi for advisory/final audit.
- Team runtime is unavailable in this native Codex App session because TMUX is unset.

## Unknowns/open questions
- Exact current vis-network full-graph timings and whether layout cache is warm or cold.
- Whether existing layout cache actually avoids stabilization on warm load.
- Whether repeated selection/search causes DataSet full replacement or only incremental updates.
- Whether performance docs currently recommend bounded subgraph default and need correction.

## Likely codebase touchpoints
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/precomputedNetworkLayout.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/graph-engine/*`
- `explorer/src/api/graphApi.ts`
- `api/explorerPerformance.test.ts`
- `.ai/05_logs/2026-04-30_explorer_performance_optimization_validation.md`
- new `.ai` audit/plan/baseline/validation files for full-graph phase
