# Explorer Network Layout Default and Physics Acceleration Validation

## Scope

Make `Network Layout` the default Explorer layout and speed up its large-graph
center-out physics formation while preserving `Saved Backbone Map`.

## Repo state

- Branch: `main`
- Starting commit: `d7ee7a06`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean after `d7ee7a06`

## Files changed

- `explorer/src/stores/useSceneStore.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_network_default_and_physics_acceleration_packet.md`
- `.ai/05_logs/2026-04-29_explorer_network_default_and_physics_acceleration_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T004331Z/network-default-physics-acceleration-report.json`

## Implementation summary

- `Network Layout` (`forceatlas2`) is now the default scene-store layout and the
  graph host fallback layout.
- `Saved Backbone Map` remains available as the precomputed/cached map option.
- Large graph physics now uses stronger repulsion and spring forces, higher max
  velocity, higher timestep, and fewer stabilization iterations to form faster.
- Small graph physics is unchanged.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
bun --cwd explorer test src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx src/components/graph/VisNetworkHost.test.ts
cd explorer && bun test && bun run lint && bun run build
git diff --check
```

## Results

- Focused graph/default tests: 63 pass / 0 fail / 334 expect calls.
- Full Explorer tests: 80 pass / 0 fail / 366 expect calls.
- Lint: pass.
- Build: pass with existing `vis-network` chunk-size warning.
- `git diff --check`: pass.

## Safety invariants

- API routes changed: no.
- Taxonomy data changed: no.
- Neo4j/KG mutation changed: no.
- Protected-content handling changed: no.
- Runtime resolver/threshold behavior changed: no.
- `Saved Backbone Map` removed: no.

## Residual risks

- The faster physics profile is still browser-rendered and graph-size dependent;
  extremely large graphs may still need additional future tuning if the visual
  formation is too energetic or too slow on a specific machine.
- Existing browser persisted state may keep a user-selected layout until storage
  is reset or the user chooses `Network Layout` manually.
