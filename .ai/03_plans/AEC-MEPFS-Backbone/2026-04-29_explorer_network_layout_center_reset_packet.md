---
status: IMPLEMENTED_VERIFIED
scope: explorer-network-layout-center-reset
baseline_commit: 3dcf25ce
authority: user-directed-network-layout-regression-fix
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer Network Layout Center Reset Packet

## Purpose

The saved precomputed `Saved Backbone Map` is correct, but the separate
`Network Layout` still inherited the saved map's already-wide coordinates when
selected from the menu. That made the invisible-boundary physics mode take too
long to reform into the previous center-out behavior.

This packet restores the previous `Network Layout` feel: when the user selects
`Network Layout`, nodes reset to compact centered seed positions and then
force-directed physics expands them outward inside the invisible boundary.

## Allowed scope

- Explorer frontend-only layout behavior.
- Keep `Saved Backbone Map` unchanged and cache-backed.
- Reset `Network Layout` to compact centered positions on normal layout switch.
- Restart vis-network simulation when motion is not paused.
- Add regression coverage for the compact large-graph center reset.

## Blocked scope

- No API route changes.
- No taxonomy/source/fixture changes.
- No Neo4j mutation.
- No KG rebuild, reload, reset, or promotion.
- No protected content ingest or exposure.
- No resolver/runtime-threshold behavior changes.

## Implementation

- Updated the `forceatlas2` layout branch in `VisNetworkHost` so `fit: true`
  layout switches rebuild compact centered positions with
  `buildCenteredNetworkLayoutPositions(...)` before enabling physics.
- Preserved spread-scaling behavior for `fit: false` updates.
- Added optional `startSimulation()` typing and invoked it after enabling
  physics when motion is not paused.
- Added a regression test proving the large `Network Layout` reset remains
  compact before physics expands it.

## Verification plan

- Focused graph host tests.
- Full Explorer test suite.
- Explorer lint and build.
- Diff and safety checks.

## Rollback

Git revert of the implementation commit restores the previous split behavior.
No server, database, KG, taxonomy, or protected-content state is mutated.
