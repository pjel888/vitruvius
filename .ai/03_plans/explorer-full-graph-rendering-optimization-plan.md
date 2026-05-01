# Explorer Full-Graph Rendering Optimization Plan

Date: 2026-04-30

## Goal
Make the default Explorer full learner-facing graph render faster while preserving current UX/UI and keeping all learner-facing nodes and edges in the renderer dataset by default.

## Rejected default strategy
Bounded visible-subgraph rendering is rejected for default Explorer behavior. It may remain as an explicitly named optional feature only. It must not hide ordinary learner-facing nodes by default.

## Implementation plan
1. Add full-graph render metrics around `VisNetworkHost.loadGraph` to measure counts, dataset creation, network creation, layout source, physics state, cache hit state, duplicate loads, and stabilization/skipped-stabilization.
2. Add a renderer graph signature and skip full `DataSet` replacement when the incoming graph is unchanged.
3. Preserve default Network Layout (`forceatlas2`) as the physics-driven full-graph layout with compact centered startup positions.
4. Keep cached deterministic full-graph positions only for the explicit Precomputed Layout option, not the default Network Layout.
5. Preserve settled-layout cache write behavior for future analysis, while preventing cached/precomputed positions from replacing default Network Layout physics startup.
6. Skip no-op initial controller updates that were recalculating full node/edge styles immediately after first render.
7. Add tests for full-graph default contract, layout cache invalidation/signature behavior, and no subgraph-default regression.
8. Measure browser/headless before and after.
9. Validate API/Explorer tests, build, lint, safety scans, and Kimi audit.

## Plan critique
- Risk: deterministic full-graph startup positions can alter exact node coordinates compared with physics-settled layout. Mitigation: do not apply deterministic precomputed positions to the default Network Layout; keep them scoped to explicit Precomputed Layout only.
- Risk: skipping duplicate loads could hide genuine data changes. Mitigation: signature includes node/edge identities/types/taxonomy paths and edge endpoints/types; changed graph payloads still reload.
- Risk: disabling default startup physics reduces the organic Network Layout behavior the user expects. Mitigation: default Network Layout keeps physics enabled; static/no-physics startup is restricted to explicit Precomputed Layout.

## 2026-05-01 correction
The previous no-redesign optimization that reused the deterministic precomputed backbone-style startup for default `forceatlas2` changed the expected visual semantics. The corrected plan is: default Network Layout remains full graph + physics; explicit Precomputed Layout owns saved deterministic positions; full-graph performance guardrails continue through stable datasets, duplicate-load skipping, and bounded physics settings rather than replacing the default layout with a saved map.
