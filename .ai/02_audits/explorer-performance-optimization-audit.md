---
task: explorer-performance-optimization
phase: 04
created: 2026-04-30
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Explorer Performance Optimization Audit

## Current implementation facts

- The Explorer fetches graph data through `explorer/src/api/graphApi.ts::getNodesForPerspective` and loads it in `explorer/src/App.tsx::ExploreView`.
- The default AEC-MEPFS route is `GET /perspective/aec-mepfs/nodes`, backed by `api/index.ts::readAecMepfsBackboneGraphArtifacts` and `buildAecMepfsExplorerGraph`.
- `readAecMepfsBackboneGraphArtifacts` already caches the raw report/artifact/shadow graph and constructed Explorer graph by file size/mtime cache key.
- Hot route operations still repeatedly derive indexes or scan arrays:
  - `/search` calls `buildShadowBackboneSearchPreview`, which validates/builds a preview and scans fields on each request.
  - `/node/:id` rebuilds graph node maps and taxonomy path lookups.
  - `/edge/:id` scans edges.
  - `/expand` scans `graph.edges` for each frontier node.
  - `/path` rebuilds adjacency per request.
- Frontend `VisNetworkHost` keeps the current vis-network renderer and already has large-graph guardrails, precomputed layout cache, hover skip thresholds, and physics auto-freeze.
- Selection/highlight behavior uses direct visible-edge neighborhood semantics; this must not regress.
- The current graph route sends render-irrelevant metadata (`summary`, `kind`, `slug`, `status`, edge `reasoning`, `assertionId`, fixed confidence) to the graph canvas path.

## Baseline bottlenecks

Primary measured bottleneck is graph payload transfer/serialization: 8.61 MiB response and 126.66 ms in-process fetch proxy, with 17.22 ms parse. Search/detail are already near targets but can become safer with cached indexes. Browser pan/zoom bottleneck still needs post-change smoke because the baseline script did not run real vis-network.

## Impact analysis

GitNexus impact results:
- `buildAecMepfsExplorerGraph`: LOW risk, direct callers are node/edge detail, artifact cache, and tests.
- `readAecMepfsBackboneGraphArtifacts`: LOW risk, route-local use plus tests.
- `getNodesForPerspective`: LOW risk, used by `ExploreView` and `HomeScreen` preload.
- `getSelectedNeighborhoodIds`: HIGH risk if edited directly; selection/highlight behavior touches `VisNetworkHost`, `GraphScene`, `QueryPanel`, `NodeContextMenu`, and tests. Plan avoids changing its public semantics and adds indexed helper coverage instead.

## UX preservation audit result

No UI redesign is needed. The safe optimization seam is data/index/cache work below the existing UI. Compact graph payload must preserve fields used for rendering, labels, filters, aliases/search, taxonomy clustering, saved scenes, and visible behavior.

## Risks

- Compact payload could accidentally remove fields used by render modes, saved scenes, or future local search. Mitigation: only use compact profile for Explorer graph load, keep full default API response for tests/contracts, and preserve label/displayLabel/type/aliases/taxonomy_path/radius/confidence.
- Cached search/index could return stale results if file cache key ignores an input. Mitigation: derive index under the existing report/artifact/shadow graph cache key.
- Indexed neighborhood could include hidden/provenance/scaffold nodes if visibility filters are not applied first. Mitigation: index only supplies adjacency; visible node/edge filtering remains authoritative.
- Workerization might add complexity without UI benefit if API/local indexes already meet thresholds. Mitigation: implement worker-safe graph engine contracts and direct tests first; use browser Worker only if integration remains stable.
- Rust currently lacks benchmark justification. Mitigation: defer Rust and document future insertion point unless post-optimization measurements fail targets.
