# Strategic Next Move

## Single Best Next Move

**Close the AEC-MEPFS Backbone readiness gates before opening any runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- The highest-leverage move is therefore to close readiness gates, not to implement code, clean Neo4j, flip feature flags, rebuild the graph, or run backup tests.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Use `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md` as the next AEC gate.
2. Keep `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` as upstream context, not as permission to begin runtime work.
3. Close the source-rights, first-slice model, code-intel, shadow graph, API/Explorer parity, verification, and rollback gates before any execution handoff.
