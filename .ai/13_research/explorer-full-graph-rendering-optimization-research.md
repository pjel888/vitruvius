# Explorer Full-Graph Rendering Optimization Research

Date: 2026-04-30

## Scope
Optimize Explorer full learner-facing graph rendering without changing the default graph into a bounded subgraph. The default renderer dataset must contain every learner-facing node and edge from the render profile.

## Current facts
- Prior performance commit: `608def8a`.
- Runtime graph endpoint: `/perspective/aec-mepfs/nodes?profile=render`.
- Full learner-facing render-profile count observed in API tests and browser metrics: 9,880 nodes and 13,285 edges.
- `buildVisibleSubgraph` exists only as an explicit graph-engine helper/worker query. It is not the default `VisNetworkHost` render path.
- The default `VisNetworkHost` path constructs `vis-network` `DataSet` objects from all render-profile nodes and edges.
- Previous validation language that recommended a future bounded visible-subgraph default conflicts with the new full-graph requirement and must be corrected.

## Renderer bottleneck notes
- Browser metrics added during this phase showed full graph `Network` creation around 545 ms before optimization, but the initial load long task continued past network creation because several initial React/controller effects caused redundant full-node/full-edge updates.
- Duplicate `loadPerspective` calls with the same graph were replacing the full `DataSet` even when the graph fingerprint had not changed.
- Default large-graph `forceatlas2` startup used a compact centered seed and enabled physics. That preserved the renderer but left expensive stabilization/layout work on the main thread.

## Full-graph-safe optimization candidates
1. Keep the full graph in `vis-network` and skip duplicate `DataSet` replacement when the graph signature is unchanged.
2. Seed large default Network Layout with a deterministic full-graph cached layout keyed by graph signature and spread.
3. Disable initial physics for the cached full-graph startup layout; keep user layout controls available.
4. Suppress no-op initial controller updates for unchanged layout, spread, label filters, color scheme, size mode, motion state, and clear-path calls.
5. Keep optional focus-subgraph behavior explicit/off-default only.

## Rust/WebGL note
Rust is not indicated for this phase because the measured bottleneck is browser renderer/update/stabilization behavior, not graph query/index computation. A future Rust insertion point would be a build-time full-graph layout artifact generator if the graph grows beyond the current size or deterministic TypeScript layout generation becomes a measurable bottleneck.
