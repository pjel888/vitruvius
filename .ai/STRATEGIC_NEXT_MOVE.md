# Strategic Next Move

## Single Best Next Move

**Build on the validated AEC-BB-S1 contract validator before opening any runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- `AEC-BB-S1` is the safe foothold: a file-backed validator that checks candidate backbone records without touching KG schemas, Neo4j, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to use the validator for authoring/migration QA fixtures and source-rights rows, not to clean Neo4j, flip feature flags, rebuild the graph, or wire runtime paths.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Use `scripts/vitruvius/kg/backbone_contracts.py` as the safe first implementation surface for candidate backbone registry validation.
2. Build authoring/migration QA fixtures and source-rights registry rows that pass the validator.
3. Keep `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` as upstream context, not as permission to begin runtime work.
