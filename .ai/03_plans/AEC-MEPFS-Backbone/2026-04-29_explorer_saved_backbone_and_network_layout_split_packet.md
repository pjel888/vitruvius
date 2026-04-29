---
status: IMPLEMENTED_VERIFIED
scope: explorer-saved-backbone-and-bounded-network-layout-split
authority: user-directed-layout-preservation
baseline_commit: 2f19b0cb
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer Saved Backbone and Network Layout Split Packet

## Purpose

The project owner approved the newly precomputed large-graph map as visually
beautiful and asked to save it, while also preserving the previous invisible
circle bounded Network Layout. This packet splits those behaviors instead of
forcing one layout mode to satisfy both needs.

## Allowed scope

- Explorer frontend-only layout option and default-state changes.
- Preserve the precomputed, cached, wide AEC-MEPFS arrangement as its own saved
  layout mode.
- Restore `Network Layout` to the force-directed invisible-boundary physics
  behavior the user still wants available.
- Update layout labels, type unions, default layout state, and regression tests.
- Keep the change reversible by git revert only.

## Blocked scope

- No API route changes.
- No taxonomy, fixture, or source-data changes.
- No Neo4j mutation.
- No KG rebuild, reload, reset, or promotion.
- No protected-content ingest or exposure.
- No runtime resolver or threshold behavior changes.
- No Explorer graph-source default/cutover changes beyond selecting the new
  saved layout presentation as the default view mode.

## Implementation

- Added `precomputed` as a first-class graph layout key labelled `Saved Backbone
  Map`.
- Kept `forceatlas2` as `Network Layout`, with physics enabled according to the
  existing motion-pause and spread controls.
- Limited the cached precomputed large-graph positions to the `precomputed`
  layout mode.
- Set Explorer scene default layout to `precomputed`, so the approved beautiful
  map opens first.
- Preserved `Network Layout` in the layout menu as the prior bounded physics
  option.
- Updated layout interaction and guardrail tests to prove both modes exist and
  are distinct.

## Verification plan

- Focused graph layout and interaction tests.
- Full Explorer test suite.
- Explorer lint and production build.
- Diff check.
- Safety grep separating documentation mentions from implementation behavior.

## Rollback

Git revert of the implementation commit restores the previous single-mode
precomputed `Network Layout` behavior. No server, database, KG, taxonomy, or
protected-content state is mutated.
