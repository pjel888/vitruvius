# Explorer Performance Optimization Context

## Task statement
Dedicated performance optimization phase for Vitruvius Explorer serving the architecture / AEC / LEA-ALE knowledge graph.

## Desired outcome
Make Explorer feel much faster while preserving current React/Vite/Tailwind/Zustand/React Query/vis-network UX, toolbar/search/preview/selection/highlight behavior, learner-facing filtering, and source-rights cleanliness.

## Known baseline
- Graph: 9,880 nodes / 13,285 relationships / 106 source-rights rows / 117 resolver cases.
- UI/API source: file-backed shadow staging run 20260430T094129Z.
- Resolver source: scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json.
- Bad learner-facing label hits: 0 for Local raw-source filename metadata for TOA tropical architecture PDF.
- API + Explorer tests previously passed: 195.
- Non-Rust Python suite previously passed excluding unrelated Rust parity wiring.

## Constraints
- Preserve current UX/UI; no redesign, no renderer migration by default, no wholesale rewrite.
- Use Kimi for advisory/final audit; do not use Codex Spark.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, destructive graph operations, protected source ingestion, or graph-content expansion unrelated to performance.
- Rust only if benchmarked and justified after TypeScript/worker/index optimizations.

## Unknowns/open questions
- Current graph artifact size/parse/index/search/highlight timings.
- Whether actual browser tooling is available from this session.
- Existing hot paths in VisNetworkHost, API graph conversion, Zustand, and React Query.
- Existing Rust/WASM surface and parity-test state.

## Likely touchpoints
- explorer/src/components/graph/VisNetworkHost.tsx and tests.
- explorer/src/api/graphApi.ts and tests.
- explorer/src/stores/sceneStore.ts or equivalent Zustand store.
- explorer/src/App.tsx / route and search components.
- api/index.ts and api/v2Backbone.test.ts for current graph source/data-source assertions.
- scripts/tests/fixtures/aec_mepfs_backbone and shadow-staging artifacts for artifact metrics only.
