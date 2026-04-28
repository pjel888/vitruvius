# Explorer Graph Scale Reduction Validation

```yaml
status: VALIDATED
created: 2026-04-28
branch: main
start_commit: 4c9710e0
run_id: 20260428T132000Z
scope: Explorer graph visual scale, spread defaults, and overlap reduction
```

## Task

Respond to the Explorer view looking oversized and cramped: reduce graph visual
scale, widen the default layout spread, and preserve the existing dense-graph
performance controls.

## Changes

- Reduced node body minimum from `10` to `7` screen pixels.
- Reduced node label font from `8` to `6` screen pixels.
- Reduced normal/emphasized/path edge stroke widths from `0.75/1.6/1.8` to
  `0.45/1.05/1.2`.
- Reduced normal/dimmed edge opacity to `0.32/0.14`.
- Reduced confidence/degree size scaling caps from `18` to `14`.
- Increased default graph layout spread from `1.85x` to `2.65x`.
- Increased max spread from `4x` to `6x`; the Spacious preset is now `4x`.
- Node focus no longer zooms in to `1.2x`; it caps focus at `0.85x` to avoid
  blowing up selected-node views.
- Updated graph/store tests for the new scale bounds and helper behavior.

## Files changed

- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/graph/graphVisualEmphasis.ts`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/componentInteraction.test.tsx`

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

- Focused Explorer graph/component tests: `41 pass`, `0 fail`, `169` assertions.
- Full Explorer tests: `67 pass`, `0 fail`, `306` assertions.
- Explorer lint: passed.
- Explorer build: passed.
- `git diff --check`: passed.
- Local Vite `/explore` smoke: HTTP `200 OK`.

Build asset evidence after this change:

- `explorer/dist/assets/index-CGejB4aC.css`: `37,158` bytes.
- `explorer/dist/assets/index-cWsQ6h1K.js`: `366,370` bytes.
- `explorer/dist/assets/vis-network-Pd1GV7-0.js`: `650,427` bytes.

Vite retained the pre-existing large `vis-network` chunk warning; the graph
engine remains code-split into its own chunk.

## Safety invariants

- Explorer-only visual scale change.
- No API behavior changed.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No taxonomy fixture changed.
- No protected content ingest or exposure.
- No runtime resolver behavior changed.

## Residual risks

- Browser-use in-app screenshot automation remains unavailable in this session;
  verification used tests, build, and local HTTP smoke.
- Exact subjective scale should be validated visually by running Explorer, but
  the new defaults are materially smaller and less cramped than the prior view.
