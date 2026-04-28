# AEC-MEPFS Explorer Large-Graph Performance Validation

```yaml
status: VALIDATED
created: 2026-04-28
branch: main
start_commit: 925f4963
run_id: 20260428T041000Z
authority_packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_large_graph_performance_packet.md
```

## Scope

Focused Explorer optimization for the 779-node / 760-edge AEC-MEPFS graph after
physics was re-enabled. This slice preserves the full taxonomy and changes only
client-side large-graph rendering guardrails.

## Files changed

- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_large_graph_performance_packet.md`
- `.ai/05_logs/2026-04-28_aec_mepfs_explorer_large_graph_performance_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T041000Z/explorer-large-graph-optimization-report.json`

## Implementation summary

- Moved large-graph thresholds and physics option construction into a pure helper
  module for direct test coverage.
- Classified the expanded AEC-MEPFS graph (`779` nodes, `760` edges) as a large
  graph.
- Reduced large-graph physics cost: stabilization iterations `40 -> 24`, timestep
  `0.25 -> 0.18`, max velocity `20 -> 12`, weaker force/spring constants.
- Auto-freezes physics after large-graph stabilization, keeping physics useful for
  initial layout while preventing continuous post-settle CPU churn.
- Skips expensive all-node hover dimming for graphs at or above 300 nodes/edges.
- Disables vis-network improved layout and hides nodes during drag for large
  graphs.

## Commands run

```bash
cd explorer && bun test src/components/graph/VisNetworkHost.test.ts
cd explorer && bun test src/components/graph/VisNetworkHost.test.ts && bun run lint
cd explorer && bun test && bun run build
RUN_ID=20260428T041000Z bun -e '... large graph optimization evidence ...' > 006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T041000Z/explorer-large-graph-optimization-report.json
```

## Results

- `VisNetworkHost.test.ts`: `8 pass`, `0 fail`
- full Explorer tests: `51 pass`, `0 fail`
- Explorer lint: passed
- Explorer build: passed with the existing Vite chunk-size warning
- performance evidence report: `ok: true`

## Safety invariants

- AEC-MEPFS taxonomy remains 779 nodes / 760 edges.
- No API behavior changed.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No protected content ingest or exposure.
- No new dependency introduced.

## Residual risks

- The evidence is code/test/build plus deterministic option-report evidence, not
  a real browser FPS trace. If jank remains in the browser, the next slice should
  use browser-driven profiling and possibly introduce progressive rendering or a
  root-collapsed initial view.
