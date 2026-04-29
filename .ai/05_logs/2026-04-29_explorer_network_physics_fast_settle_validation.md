# Explorer Network Layout Fast Settle Physics Validation

## Scope

Further speed up the large-graph `Network Layout` physics formation while
leaving `Saved Backbone Map` and small-graph physics unchanged.

## Repo state

- Branch: `main`
- Starting commit: `530c9ade`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean after `530c9ade`

## Files changed

- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_network_physics_fast_settle_packet.md`
- `.ai/05_logs/2026-04-29_explorer_network_physics_fast_settle_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T004634Z/network-physics-fast-settle-report.json`

## Implementation summary

- Large Network Layout physics now uses:
  - gravitational constant: `-30 * spreadRatio`
  - central gravity: `0.032 / sqrt(spreadRatio)`
  - spring length: `128 * spreadRatio`
  - spring constant: `0.075 / sqrt(spreadRatio)`
  - max velocity: `44`
  - min velocity: `3.4`
  - timestep: `0.34`
  - stabilization iterations: `8`
- Small graph physics remains unchanged.
- `Saved Backbone Map` remains unchanged and selectable.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts
cd explorer && bun test && bun run lint && bun run build
git diff --check
```

## Results

- Focused graph host tests: 33 pass / 0 fail / 108 expect calls.
- Full Explorer tests: 80 pass / 0 fail / 368 expect calls.
- Lint: pass.
- Build: pass with existing `vis-network` chunk-size warning.
- `git diff --check`: pass.

## Safety invariants

- API routes changed: no.
- Taxonomy data changed: no.
- Neo4j/KG mutation changed: no.
- Protected-content handling changed: no.
- Runtime resolver/threshold behavior changed: no.
- `Saved Backbone Map` behavior changed: no.

## Residual risks

- This is an aggressive but still bounded force profile. If the browser visual
  feels too jumpy on a particular machine, the next safe adjustment is to lower
  `maxVelocity` or `timestep` slightly while retaining the default Network
  Layout behavior.
