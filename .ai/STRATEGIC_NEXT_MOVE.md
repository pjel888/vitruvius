# Strategic Next Move

## Single Best Next Move

**Human-review the S7 decision packets and execute a stopped/isolated Neo4j rollback rehearsal before opening runtime implementation.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The readiness scorecard is still `not ready`, and the 2026-04-23 runtime-roots audit confirmed that AEC runtime roots remain unverified.
- `AEC-BB-S1` through `AEC-BB-S7` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, and runtime-root impact evidence now check readiness without touching KG schemas, Neo4j write paths, API, Explorer, feature flags, or graph rebuilds.
- The highest-leverage move is therefore to review/sign the S7 decision packets and run a stopped/isolated rollback rehearsal, not to clean Neo4j, flip feature flags, rebuild the graph, or wire runtime paths.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime implementation before the readiness scorecard reaches `ready for bounded implementation`
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Review and accept/reject the S7 legal/steward admission record.
2. Record legal/licensing decisions for any source use beyond reference or metadata crosswalk.
3. Resolve the 5 manual source-currentness exception rows.
4. Run a stopped or isolated Neo4j dump/load rehearsal before any graph mutation.
5. Accept/reject the runtime-root implementation packet before editing any HIGH/CRITICAL KG root.
