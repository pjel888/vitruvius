# AEC-MEPFS Explorer Physics Validation

```yaml
status: VALIDATED
date: 2026-04-28
branch: main
start_commit: 0fd255d1
scope: explorer-physics-reenabled-for-expanded-aec-graph
```

## Scope

Re-enable force-atlas physics for the expanded AEC-MEPFS Explorer graph after
the taxonomy expansion to 114 nodes and 95 edges. This keeps the large-graph
rendering guardrails that reduce visual cost, but no longer freezes the default
force-atlas layout for graphs above the 80-node guardrail threshold.

## Files changed

- `explorer/src/components/graph/VisNetworkHost.tsx`

## Implementation summary

- Renamed the large-graph helper to describe rendering guardrails instead of
  reduced motion.
- Kept deterministic clustered seeding for large graphs so the first layout does
  not start from an arbitrary tangle.
- Re-enabled force-atlas physics for large graphs unless the user has explicitly
  paused motion.
- Preserved large-graph render-cost reductions:
  - no node shadows,
  - no smooth edges,
  - lower large-graph velocity/timestep parameters,
  - hidden edges while dragging.

## Verification

```bash
cd explorer && bun test src/components/graph/VisNetworkHost.test.ts src/app.searchInspector.integration.test.tsx
cd explorer && bun run lint
cd explorer && bun run build
git diff --check
git diff -U0 -- explorer/src/components/graph/VisNetworkHost.tsx | rg -n "^\\+.*(LIVE_RUNTIME_AUTHORIZED|Neo4j|KG rebuild|KG reload|KG reset|protected ingest|protected content|MATCH \\(n\\) DETACH DELETE|DETACH DELETE|DROP DATABASE|CREATE OR REPLACE|run-kg-pipeline|--reset|--reload)" || true
```

Results:

- Focused Explorer tests: `14 pass`, `0 fail`.
- Explorer lint: passed.
- Explorer build: passed with the existing Vite chunk-size warning for the
  dynamically loaded `vis-network` bundle.
- `git diff --check`: passed.
- Safety diff grep: no unauthorized runtime, Neo4j, KG, or protected-ingest
  changes.

## Residual risk

This restores physics for the 114-node graph, which should feel more organic and
interactive. If subjective browser behavior becomes janky on lower-powered
machines, tune force-atlas constants rather than disabling physics globally.
