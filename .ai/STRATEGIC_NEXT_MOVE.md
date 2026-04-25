# Strategic Next Move

## Single Best Next Move

**Turn the validated AEC-BB-S1/S2/S3/S4 readiness spine into a bounded rollback-proof packet before opening any runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- `AEC-BB-S1` through `AEC-BB-S4` are the safe foothold: file-backed validators, fixtures, and parity reports now check candidate backbone records, registry rows, QA cases, resolver/API parity cases, rollback metadata, registry locations, parity-runner plans, rollback-proof plans, benchmark plans, runtime-blocking readiness gates, and current API/Explorer regression behavior without touching KG schemas, Neo4j, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to define and execute a safe rollback proof in an isolated or stopped Neo4j workflow, not to clean Neo4j, flip feature flags, rebuild the graph, or wire runtime paths.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Draft `AEC-BB-S5` as a bounded rollback-proof execution packet.
2. Keep the S1/S2/S3 validator and S4 parity runner as gates for any future registry or fixture file.
3. Keep `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` as upstream context, not as permission to begin runtime work.
