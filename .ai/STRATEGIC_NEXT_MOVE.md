# Strategic Next Move

## Single Best Next Move

**Resolve the non-code readiness gates for AEC-BB-S6 candidate rows and rollback proof before opening runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- `AEC-BB-S1` through `AEC-BB-S6` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, and registry/source-admission candidate rows now check candidate backbone records, registry rows, QA cases, resolver/API parity cases, runtime-blocking readiness gates, and current API/Explorer behavior without touching KG schemas, Neo4j write paths, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to get human steward/legal decisions and a stopped/isolated rollback rehearsal, not to clean Neo4j, flip feature flags, rebuild the graph, or wire runtime paths.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Review and accept/reject the S6 predicate and source-rights candidate rows.
2. Record legal/licensing decisions for any source use beyond reference or metadata crosswalk.
3. Run a stopped or isolated Neo4j dump/load rehearsal before any graph mutation.
4. Keep the S1/S2/S3 validator and S4 parity runner as gates for any future registry or fixture file.
5. Keep `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` as upstream context, not as permission to begin runtime work.
