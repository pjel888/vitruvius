# Strategic Next Move

## Single Best Next Move

**Validate the non-default Explorer preview, then choose any next shadow consumer slice from fresh evidence.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The first additive shadow-only implementation slice is implemented as a file-backed staging artifact, while primary runtime cutover remains blocked.
- The second bounded read-only consumer/reporting slice is implemented and validates the existing staging artifact without touching Neo4j, Explorer, feature flags, graph rebuilds, or protected source content.
- The first additive `/v2` shadow read route, `GET /v2/backbone`, is implemented as a compact file-backed summary route and does not change v1 behavior or Explorer defaults.
- The non-default Explorer preview is implemented as an opt-in rail panel that reads `/v2/backbone` without replacing the graph, changing perspectives, mutating Neo4j, or enabling runtime cutover.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to close validation on the preview slice, then choose any next shadow consumer slice from fresh impact evidence.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging, read-only reporting, the first compact `/v2` summary route, and the opt-in Explorer preview
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Keep the Explorer preview validation evidence current.
2. Decide whether the next bounded slice is a remaining `/v2` detail route or a staging-detail preview.
3. Write a separate packet for only that slice.
4. Run fresh GitNexus impact/status on the exact files before touching them.
5. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, v1 behavior changes, Explorer default adoption, and default-on feature flags blocked.
