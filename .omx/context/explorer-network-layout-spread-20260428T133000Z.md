# Ralph Context Snapshot — Explorer Network Layout Spread

- task statement: Fix Explorer spread behavior so Network Layout expands its own invisible physics/world boundary instead of becoming Taxonomy Clusters.
- desired outcome: Network Layout spread should preserve force/network semantics, increase spacing in the force layout, avoid taxonomy cluster placement, and keep tests/build green.
- known facts/evidence: `forceatlas2` currently calls `buildClusteredLayoutUpdates` for large graphs in `VisNetworkHost.applyLayout`, causing Network Layout to visually become taxonomy clusters. Spread constants live in `layoutSpread.ts`; physics options live in `largeGraphPerformance.ts`; layout UI lives in `GraphScene.tsx`/`LayoutMenu.tsx`.
- constraints: Explorer-only; no API, Neo4j, KG, protected ingest, taxonomy fixture, or resolver changes. Browser Use Node REPL execution tool is not exposed in this session; use local Vite HTTP smoke as fallback.
- unknowns/open questions: exact subjective visual target requires interactive user review, but code can enforce separation of Network vs Taxonomy Cluster algorithms.
- likely codebase touchpoints: `explorer/src/components/graph/VisNetworkHost.tsx`, `layoutSpread.ts`, `largeGraphPerformance.ts`, `VisNetworkHost.test.ts`, validation/evidence artifacts.
