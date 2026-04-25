# Strategic Next Move

## Single Best Next Move

**Prepare the first additive `/v2` shadow read-route implementation packet.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The first additive shadow-only implementation slice is implemented as a file-backed staging artifact, while primary runtime cutover remains blocked.
- The second bounded read-only consumer/reporting slice is implemented and validates the existing staging artifact without touching Neo4j, API, Explorer, feature flags, graph rebuilds, or protected source content.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to prepare, but not yet execute, the first additive `/v2` shadow read-route implementation packet with fresh API impact review and route-shape tests.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging and read-only reporting
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Review `shadow-v2-api-read-route-planning-packet.md`.
2. Run fresh GitNexus impact/status on the exact API route files before touching them.
3. Write route-shape tests for the smallest additive `/v2` read route.
4. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, v1 behavior changes, Explorer default adoption, and default-on feature flags blocked.
