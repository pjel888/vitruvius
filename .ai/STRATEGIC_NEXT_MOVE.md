# Strategic Next Move

## Single Best Next Move

**Plan the next bounded read-only consumer/reporting slice over the shadow staging artifact.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The first additive shadow-only implementation slice is now implemented as a file-backed staging artifact, while primary runtime cutover remains blocked.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to plan the next bounded read-only consumer/reporting slice over the staging artifact without touching primary KG roots, Neo4j write paths, graph rebuilds, API/Explorer cutover, or protected content ingest.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond the first shadow-only packet
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Review the shadow staging report and artifact under `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/`.
2. Draft a separate next-slice packet for a read-only consumer/reporting lane.
3. Run fresh GitNexus impact/status before touching any consumer surface.
4. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, and default-on feature flags blocked.
