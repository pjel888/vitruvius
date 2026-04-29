# Explorer Network Layout Center Reset Validation

## Scope

Restore `Network Layout` to the previous center-out physics behavior while
leaving `Saved Backbone Map` unchanged.

## Repo state

- Branch: `main`
- Starting commit: `3dcf25ce`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean after `3dcf25ce`

## Files changed

- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_network_layout_center_reset_packet.md`
- `.ai/05_logs/2026-04-29_explorer_network_layout_center_reset_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T003737Z/network-layout-center-reset-report.json`

## Implementation summary

- `Saved Backbone Map` remains the precomputed/cached map.
- `Network Layout` now resets nodes to compact centered seed positions on normal
  layout selection before enabling force-directed physics.
- `Network Layout` restarts the vis-network simulation when motion is not
  paused, so the graph visibly forms from the middle outward again.
- Spread-slider scaling still uses current positions for non-fit spread updates.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
omx explore --prompt "Find the Explorer Network Layout forceatlas2 applyLayout path and initial centered layout helpers. Summarize where to reset positions when switching from Saved Backbone Map to Network Layout. Do not edit."
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts
cd explorer && bun test && bun run lint && bun run build
git diff --check
```

## Results

- `omx explore`: found `applyLayout('forceatlas2')` as the correct reset point;
  Spark model was unavailable, OMX fell back to `gpt-5.5` and returned a
  read-only summary.
- Focused graph host tests: 32 pass / 0 fail / 101 expect calls.
- Full Explorer tests: 79 pass / 0 fail / 361 expect calls.
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

- This restores the visible center-out physics path. For very large graphs, the
  settling time is still governed by vis-network physics and graph size, but it
  no longer starts from the saved map's wide coordinates when switching modes.
