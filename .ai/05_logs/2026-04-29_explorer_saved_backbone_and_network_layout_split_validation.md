# Explorer Saved Backbone and Network Layout Split Validation

## Scope

Save the approved precomputed AEC-MEPFS map as a dedicated layout while keeping
the previous invisible-circle physics Network Layout available.

## Repo state

- Branch: `main`
- Starting commit: `2f19b0cb`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean after `2f19b0cb`

## Files changed

- `explorer/src/components/graph/layoutOptions.ts`
- `explorer/src/components/graph/LayoutMenu.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/precomputedNetworkLayout.ts`
- `explorer/src/stores/useSceneStore.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/componentInteraction.test.tsx`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_saved_backbone_and_network_layout_split_packet.md`
- `.ai/05_logs/2026-04-29_explorer_saved_backbone_and_network_layout_split_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T003029Z/layout-split-report.json`

## Implementation summary

- Added `Saved Backbone Map` as the dedicated cached/precomputed layout.
- Made `Saved Backbone Map` the default Explorer layout so the approved visual
  arrangement opens first.
- Restored `Network Layout` to the old force-directed physics/invisible-boundary
  mode instead of using the precomputed cache.
- Updated tests to assert that `precomputed` is the only large cached layout and
  that the layout menu exposes both `Saved Backbone Map` and `Network Layout`.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
omx explore --prompt "Summarize the current uncommitted Explorer layout split changes and flag any obvious missing tests or files. Do not edit."  # timed out/no output; manual diff inspection used
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx
cd explorer && bun test && bun run lint && bun run build
git diff --check
```

## Results

- Focused graph + interaction tests before evidence docs: 52 pass / 0 fail /
  220 expect calls.
- Full Explorer tests before evidence docs: 78 pass / 0 fail / 359 expect calls.
- Lint before evidence docs: pass.
- Build before evidence docs: pass with existing `vis-network` chunk-size
  warning.
- Focused graph + interaction tests after evidence docs: 52 pass / 0 fail / 220 expect calls.
- Full Explorer tests after evidence docs: 78 pass / 0 fail / 359 expect calls.
- Lint after evidence docs: pass.
- Build after evidence docs: pass with existing `vis-network` chunk-size warning.
- `git diff --check`: pass.
- `omx explore`: attempted for read-only summary but produced no output before timeout; manual diff inspection and tests covered the verification.

## Safety invariants

- API routes changed: no.
- Taxonomy data changed: no.
- Neo4j/KG mutation changed: no.
- Protected-content handling changed: no.
- Runtime resolver/threshold behavior changed: no.
- Explorer data-source default changed: no; only layout presentation default
  changes from `forceatlas2` to `precomputed`.

## Residual risks

- Existing user browser state may retain a previously selected layout until the
  scene store is reset or the user selects `Saved Backbone Map` manually.
- The saved layout is deterministic and cache-backed; if localStorage is absent,
  it recomputes in memory.
