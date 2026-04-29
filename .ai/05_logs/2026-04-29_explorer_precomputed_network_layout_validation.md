# Explorer Precomputed Network Layout Validation

## Scope

Replace the failed hidden-startup workaround with deterministic precomputed and
cached large-graph Network Layout positions.

## Repo state

- Branch: `main`
- Starting commit: `28338ab4`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean

## Files changed

- `explorer/src/components/graph/precomputedNetworkLayout.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_precomputed_network_layout_packet.md`
- `.ai/05_logs/2026-04-29_explorer_precomputed_network_layout_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T001500Z/precomputed-network-layout-report.json`

## Implementation summary

- Added a deterministic wide radial-ring layout for large AEC-MEPFS Network
  Layout graphs.
- Cache key includes graph structure and spread, so graph edits or spread changes
  invalidate stale positions.
- Cache is memory-first and optionally persisted to browser `localStorage`.
- Large Network Layout startup/reload now uses precomputed coordinates and starts
  with physics disabled instead of compact seed + stabilization.
- Removed the hidden stabilization overlay and obsolete compact seed helper.

## Commands run

```bash
git status --short --branch
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx
cd explorer && bun test
cd explorer && bun run lint
cd explorer && bun run build
curl -I http://127.0.0.1:5174/explore
git diff --check
rg -n "buildCenteredNetworkLayoutPositions|shouldHideInitialGraphStabilization|startupStabilizing|Preparing optimized graph layout|stabilizationIterationsDone" explorer/src || true
```

## Results

- Focused graph tests: 31 pass / 0 fail.
- Focused graph + interaction tests: 52 pass / 0 fail.
- Full Explorer tests: 78 pass / 0 fail / 356 expects.
- Lint: pass.
- Build: pass with existing `vis-network` chunk-size warning.
- `/explore` smoke: HTTP 200.
- Obsolete hidden-startup symbols: no matches in `explorer/src`.

## Safety invariants

- API routes changed: no.
- Taxonomy data changed: no.
- Neo4j/KG mutation changed: no.
- Protected-content handling changed: no.
- Runtime threshold/resolver behavior changed: no.

## Residual risks

- Browser visual tuning may still need adjustment if the deterministic spacing is
  too wide or too compressed for a particular screen size, but the compact center
  seed and visible fly-out path are removed.
- Cache is a performance hint only; if browser storage is unavailable, the layout
  is recomputed deterministically in memory.
