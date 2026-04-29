---
status: IMPLEMENTED_VERIFIED
scope: explorer-large-graph-precomputed-network-layout
authority: user-directed-correction
baseline_commit: 28338ab4
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer Precomputed Network Layout Packet

## Purpose

The hidden-stabilization approach was insufficient because the large graph still
started from cramped positions. This packet replaces the compact physics seed
with deterministic, wide, precomputed Network Layout positions and caches those
positions by graph signature and spread.

## Allowed scope

- Explorer frontend-only layout optimization.
- Precompute positions for large force-directed Network Layout graphs.
- Cache computed positions in memory and browser storage.
- Disable automatic startup physics for precomputed large Network Layouts so
  the graph starts in its final spread-out form.
- Preserve spread scaling, minimap/filter behavior, labels, selected-subtree
  focus behavior, small-graph physics, and non-Network layouts.

## Blocked scope

- No API route changes.
- No taxonomy data changes.
- No Neo4j or KG rebuild/reload/reset.
- No protected content ingest/exposure.
- No runtime threshold or resolver changes.

## Implementation

- Added `precomputedNetworkLayout.ts` with:
  - deterministic hierarchy-aware radial ring layout;
  - graph-signature cache keys including node IDs, edge structure, and spread;
  - in-memory cache and optional `localStorage` cache;
  - cache validation against expected node IDs.
- Removed the hidden overlay/startup stabilization path from `VisNetworkHost`.
- Replaced compact centered seed positions with precomputed wide positions for
  large Network Layout graphs.
- Disabled automatic force physics for precomputed large startup/reload paths;
  user-driven motion controls can still alter physics state.
- Removed the obsolete compact centered seed helper.

## Verification plan

- Focused graph layout tests.
- Explorer interaction tests.
- Full Explorer test suite.
- Lint and production build.
- Local `/explore` HTTP smoke.
- Diff and safety checks.

## Rollback

Git revert of the implementation commit restores the prior behavior. No API,
database, KG, taxonomy, or protected-content state is mutated.
