# Strategic Next Move

## Single Best Next Move

**Choose the next shadow slice from fresh evidence, with priority on file-backed classification/placement QA or another read-only `/v2` surface before any runtime cutover.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The first additive shadow-only implementation slice is implemented as a file-backed staging artifact, while primary runtime cutover remains blocked.
- The second bounded read-only consumer/reporting slice is implemented and validates the existing staging artifact without touching Neo4j, Explorer, feature flags, graph rebuilds, or protected source content.
- The first additive `/v2` shadow read route, `GET /v2/backbone`, is implemented as a compact file-backed summary route and does not change v1 behavior or Explorer defaults.
- The non-default Explorer preview is implemented as an opt-in rail panel that reads `/v2/backbone` without replacing the graph, changing perspectives, mutating Neo4j, or enabling runtime cutover.
- The bounded `GET /v2/backbone/taxonomy` detail route is implemented as a sanitized registry-readiness preview over the shadow staging artifact.
- The first admitted `BackboneNode` L1/L2 fixture/model slice is implemented and staged, and the latest generated run `20260426T003710Z` includes a sibling shadow graph artifact with 7 nodes, 4 governed hierarchy edges, 3 roots, and max depth 2.
- The opt-in Explorer preview can show those file-backed shadow nodes and shadow graph counts/edges without routing them into Neo4j or the default graph.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, feature flags, graph rebuilds, or primary Explorer adoption.
- The highest-leverage move is therefore to keep advancing file-backed semantics around the admitted fixture: classification/placement QA and additional read-only `/v2` surfaces, still without protected content ingest, Neo4j writes, graph rebuilds, or default Explorer adoption.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging, read-only reporting, the first compact `/v2` summary route, and the opt-in Explorer preview
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Keep the shadow BackboneNode and sibling shadow graph validation evidence current.
2. Write a separate packet for the next classification/placement QA or read-only `/v2` slice before implementation.
3. Run fresh GitNexus impact/status on the exact files before touching them.
4. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, v1 behavior changes, Explorer default adoption, and default-on feature flags blocked.
