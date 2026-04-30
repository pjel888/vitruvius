# Explorer Full-Graph Rendering Optimization Plan

Date: 2026-04-30

## Goal
Make the default Explorer full learner-facing graph render faster while preserving current UX/UI and keeping all learner-facing nodes and edges in the renderer dataset by default.

## Rejected default strategy
Bounded visible-subgraph rendering is rejected for default Explorer behavior. It may remain as an explicitly named optional feature only. It must not hide ordinary learner-facing nodes by default.

## Implementation plan
1. Add full-graph render metrics around `VisNetworkHost.loadGraph` to measure counts, dataset creation, network creation, layout source, physics state, cache hit state, duplicate loads, and stabilization/skipped-stabilization.
2. Add a renderer graph signature and skip full `DataSet` replacement when the incoming graph is unchanged.
3. Use cached deterministic full-graph startup layout for large default Network Layout (`forceatlas2`) instead of compact centered startup positions.
4. Disable initial physics for the cached full-graph startup layout to avoid expensive full-graph stabilization on warm/default load.
5. Preserve settled-layout cache write behavior when physics is explicitly used and a stabilization event occurs.
6. Skip no-op initial controller updates that were recalculating full node/edge styles immediately after first render.
7. Add tests for full-graph default contract, layout cache invalidation/signature behavior, and no subgraph-default regression.
8. Measure browser/headless before and after.
9. Validate API/Explorer tests, build, lint, safety scans, and Kimi audit.

## Plan critique
- Risk: deterministic full-graph startup positions can alter exact node coordinates compared with physics-settled layout. Mitigation: this is a full-graph layout/stabilization optimization, not a UX redesign; node/edge visual semantics and controls remain unchanged, and the user explicitly allowed precomputed/cached full-graph layout.
- Risk: skipping duplicate loads could hide genuine data changes. Mitigation: signature includes node/edge identities/types/taxonomy paths and edge endpoints/types; changed graph payloads still reload.
- Risk: disabling default startup physics could reduce organic layout motion. Mitigation: this is only for large full-graph startup; explicit layout controls remain available, and the full graph remains rendered.
