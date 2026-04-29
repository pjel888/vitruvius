---
status: IMPLEMENTED_VERIFIED
scope: explorer-network-layout-fast-settle-physics
baseline_commit: 530c9ade
authority: user-directed-network-layout-speedup
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer Network Layout Fast Settle Physics Packet

## Purpose

The project owner asked whether the default Network Layout physics can be sped
up further. This packet applies a stronger large-graph force profile so the
center-out Network Layout expands and reaches a usable settled state faster,
while keeping `Saved Backbone Map` unchanged.

## Allowed scope

- Explorer frontend-only large-graph physics tuning.
- Preserve `Network Layout` as default.
- Preserve `Saved Backbone Map` as the cached/precomputed alternative.
- Keep small-graph physics unchanged.
- Add/update regression expectations for the faster bounded profile.

## Blocked scope

- No API route changes.
- No taxonomy/source/fixture changes.
- No Neo4j mutation.
- No KG rebuild, reload, reset, or promotion.
- No protected content ingest or exposure.
- No resolver/runtime-threshold behavior changes.

## Implementation

- Increased large-graph repulsion, central gravity, and spring stiffness.
- Increased large-graph max velocity and timestep while keeping them below the
  small-graph ceiling.
- Increased the minimum velocity threshold so the simulation can settle/freeze
  earlier instead of drifting slowly.
- Reduced large-graph stabilization iterations from 16 to 8.
- Updated graph host tests to pin the faster profile.

## Verification plan

- Focused graph host tests.
- Full Explorer tests.
- Explorer lint and production build.
- Diff and safety checks.

## Rollback

Git revert of the implementation commit restores the prior large-graph physics
profile. No server, database, KG, taxonomy, or protected-content state is
mutated.
