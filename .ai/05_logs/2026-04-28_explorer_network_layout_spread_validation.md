# Explorer Network Layout Spread Validation

```yaml
status: VALIDATED
created: 2026-04-28
branch: main
start_commit: 0ed6602d
run_id: 20260428T133600Z
scope: Explorer Network Layout spread behavior and layout separation
```

## Task

Fix the spread control so **Network Layout** expands the invisible network/physics
space instead of visually turning into **Taxonomy Clusters**.

## Root cause

`VisNetworkHost.applyLayout('forceatlas2')` previously used
`buildClusteredLayoutUpdates(...)` for large graphs. That made the default
Network Layout reuse the taxonomy-cluster placement algorithm, so increasing
spread looked like cluster expansion rather than a larger network-layout world.

## Changes

- Removed taxonomy-cluster placement from the `forceatlas2` / Network Layout path.
- Network Layout spread now updates force/physics parameters:
  - larger spring length;
  - stronger repulsion;
  - lower central gravity;
  - lower spring constant as spread increases.
- Network Layout spread now scales existing node positions around their current
  center when the slider changes, which behaves like expanding the current
  invisible network boundary.
- Taxonomy Clusters remains the only layout that calls `buildClusteredLayoutUpdates`.
- Added tests proving Network Layout spread expands physics and scales positions
  without taxonomy-cluster placement.

## Files changed

- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/05_logs/2026-04-28_explorer_network_layout_spread_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T133600Z/explorer-network-layout-spread-report.json`

## Commands run

```bash
git status --short --branch
omx explore --prompt "Map the Explorer graph scale defaults..."
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx
(cd explorer && bun test && bun run lint && bun run build)
git diff --check
cd explorer && bun run dev:vite --host 127.0.0.1
curl -I --max-time 5 http://127.0.0.1:5174/explore
pkill -f "vite --host 127.0.0.1" || true
```

## Results

- Focused Explorer graph/component tests: `43 pass`, `0 fail`, `174` assertions.
- Full Explorer tests: `69 pass`, `0 fail`, `311` assertions.
- Explorer lint: passed.
- Explorer build: passed.
- `git diff --check`: passed.
- Local Vite `/explore` smoke: HTTP `200 OK`.

Build asset evidence after this change:

- `explorer/dist/assets/index-CGejB4aC.css`: `37.15 kB`.
- `explorer/dist/assets/index-pq809ald.js`: `367.00 kB`.
- `explorer/dist/assets/vis-network-Pd1GV7-0.js`: `650.42 kB`.

## Browser-use status

The Browser Use skill was read, but tool discovery did not expose the required
Node REPL `js` execution tool. In-app browser automation could not be bootstrapped
in this session, so verification used local Vite HTTP smoke plus tests/lint/build.

## Safety invariants

- Explorer-only graph layout behavior change.
- No API behavior changed.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No taxonomy fixture changed.
- No protected content ingest or exposure.
- No runtime resolver behavior changed.

## Residual risks

- Exact visual feel still needs user review in the running Explorer, but Network
  Layout no longer calls the taxonomy-cluster placement algorithm.

## Architect verification

Ralph verifier verdict: APPROVED. The verifier confirmed that `forceatlas2` /
Network Layout now scales current positions and adjusts physics, while only the
`clustered` branch calls `buildClusteredLayoutUpdates`.
