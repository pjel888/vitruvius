---
status: IMPLEMENTED_VERIFIED
scope: explorer-network-layout-default-and-physics-acceleration
baseline_commit: d7ee7a06
authority: user-directed-default-and-speed-tuning
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer Network Layout Default and Physics Acceleration Packet

## Purpose

The project owner requested that `Network Layout` be the default Explorer view
instead of `Saved Backbone Map`, then asked whether the center-out physics can
be faster. This packet makes `Network Layout` the default and tunes large-graph
force physics to form faster while remaining bounded and while preserving the
saved precomputed map as an explicit menu option.

## Allowed scope

- Explorer frontend-only default layout state.
- Explorer large-graph force physics tuning for `Network Layout`.
- Regression tests for accelerated bounded physics.
- Preserve `Saved Backbone Map` as a selectable cached/precomputed option.

## Blocked scope

- No API route changes.
- No taxonomy/source/fixture changes.
- No Neo4j mutation.
- No KG rebuild, reload, reset, or promotion.
- No protected content ingest or exposure.
- No resolver/runtime-threshold behavior changes.

## Implementation

- Changed the persisted scene-store default layout from `precomputed` to
  `forceatlas2`.
- Changed the graph host active-layout fallback from `precomputed` to
  `forceatlas2`.
- Accelerated large `Network Layout` physics by increasing force, spring
  stiffness, max velocity, timestep, and stabilization cutoff while keeping
  large-graph values below small-graph physics ceilings.
- Added regression coverage proving the large graph physics profile is faster
  but still bounded.

## Verification plan

- Focused Explorer graph/default integration tests.
- Full Explorer tests.
- Explorer lint and production build.
- Diff and safety checks.

## Rollback

Git revert of the implementation commit restores `Saved Backbone Map` as the
default and the previous slower large-graph physics profile. No server,
database, KG, taxonomy, or protected-content state is mutated.
