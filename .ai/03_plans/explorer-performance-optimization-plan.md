---
task: explorer-performance-optimization
phase: 05
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Explorer Performance Optimization Plan

## Goals

[G001] Preserve current Explorer UX/UI, workflow, visual language, and vis-network renderer.
[G002] Reduce graph loading/parsing/render payload workload with no graph semantic changes.
[G003] Add cached graph indexes for search, alias lookup, node/edge detail, expansion, path, and neighborhood operations.
[G004] Add worker-safe/frontend graph index helpers and performance regression assertions.
[G005] Prove learner-facing/source-rights safety remains intact.
[G006] Produce before/after metrics and validation evidence.

## Implementation plan

1. Add API graph index/cache object under `readAecMepfsBackboneGraphArtifacts` cache key:
   - node ID map, edge ID map, path-code map, incoming/outgoing/undirected adjacency, search fields, search-result cache, fingerprint.
   - Use it for `/search`, `/node/:id`, `/edge/:id`, `/expand`, `/path`, and taxonomy tree where safe.
2. Add render-profile graph serialization for `GET /perspective/aec-mepfs/nodes?profile=render`:
   - Preserve render/search fields: `id`, `label`, optional `displayLabel`, `type`, `aliases`, `taxonomy_path`, `radius`, `confidence` for nodes; `id`, `source`, `target`, `type` for edges.
   - Omit canvas-unneeded fields from that profile only: node `summary`, `slug`, `status`, `kind`; edge `reasoning`, `confidence`, `assertionId`.
   - Keep the default route response full for existing contracts.
3. Change Explorer client `getNodesForPerspective` to request the render profile for `aec-mepfs` only.
4. Add frontend graph engine module using graphology-backed/index-equivalent maps:
   - build graph index, normalized search, alias exact/contains lookup, one/two-hop neighborhood, path query, compact visible subgraph builder, source/internal label scanners.
   - Keep it worker-safe and deterministic; introduce an optional Web Worker wrapper only if tests/build stay stable.
5. Update `VisNetworkHost` internally to use an adjacency cache for selected-neighborhood computation while preserving the exported helper behavior and visible filtering as the authority.
6. Add tests/benchmarks:
   - compact payload budget and field preservation
   - API index search/alias/detail/expand/path correctness and timing budget
   - frontend graph index search/alias/neighborhood/path/visible-subgraph timing
   - bad-label/source-provenance/default-filter assertions
   - selected-neighborhood equivalence with existing helper
7. Re-measure baseline script after implementation and write validation log.
8. Run Kimi final read-only audit and record result.

## Plan Critique

[C001] The route-level compact payload is the highest-value low-risk improvement because baseline fetch dominates local parse/query timings.
[C002] A true default bounded visible subgraph would risk visible behavior changes; defer unless browser smoke proves vis-network remains the bottleneck after payload/index work.
[C003] Editing `getSelectedNeighborhoodIds` directly has HIGH GitNexus impact; use an additive indexed helper and equivalence tests instead.
[C004] A browser Worker can improve main-thread graph query isolation but may not affect initial network payload; prioritize shared worker-safe index code and integrate only where it does not destabilize tests.
[C005] Rust has no current benchmark-backed need because TypeScript/API timings already meet most targets; defer Rust unless after metrics fail materially.

## Execution Checklist

- [ ] [G001] Create UX preservation checklist and use it as acceptance criteria.
- [ ] [G002] Measure pre-change baseline and save metrics.
- [ ] [G003] Implement API cached graph indexes and replace repeated scans.
- [ ] [G002] Implement compact render payload profile and client request.
- [ ] [G004] Implement graphology/index-equivalent frontend graph engine helpers with tests.
- [ ] [G001] Preserve `VisNetworkHost`/toolbar/search/preview/selection behavior.
- [ ] [G005] Add source-rights and bad-label safety assertions.
- [ ] [G006] Re-run performance measurements and compare.
- [ ] [G006] Run Explorer/API/KG relevant validation and safety greps.
- [ ] [G006] Run Kimi final read-only audit.
