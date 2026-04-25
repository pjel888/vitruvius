# Strategic Next Move

## Single Best Next Move

**Turn the validated AEC-BB-S1/S2 contract spine into a bounded S3 execution packet before opening any runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- `AEC-BB-S1` and `AEC-BB-S2` are the safe foothold: file-backed validators and fixtures that check candidate backbone records, registry rows, QA cases, resolver/API parity cases, and rollback metadata without touching KG schemas, Neo4j, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to define the production registry locations, exact parity/rollback runners, and benchmark evidence packet, not to clean Neo4j, flip feature flags, rebuild the graph, or wire runtime paths.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Draft `AEC-BB-S3` as a bounded execution packet for production registry file locations, exact API/Explorer parity assertions, and rollback-proof commands.
2. Keep the S1/S2 validator as the gate for any future registry or fixture file.
3. Keep `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` as upstream context, not as permission to begin runtime work.
