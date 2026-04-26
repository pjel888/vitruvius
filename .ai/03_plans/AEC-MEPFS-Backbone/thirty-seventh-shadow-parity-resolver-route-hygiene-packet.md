---
task: aec-mepfs-shadow-parity-resolver-route-hygiene
phase: 04
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Thirty-Seventh Shadow Slice: Parity Resolver-Route Hygiene

## Scope

Harden parity fixtures and contract validation so `/v2/resolve` and
`/v2/resolve/trace*` cannot appear as ordinary v2 parity cases while runtime
resolver adoption remains blocked.

This slice is contract/fixture/test/evidence only. It does not mount
`/v2/resolve`, call a runtime resolver, write or query Neo4j, rebuild the KG,
ingest protected content, change feature flags, promote the shadow graph, or
make Explorer adopt the shadow graph by default.

## Audit Findings

- Fresh scan found `API-CASE-003` in `valid_readiness_s2.json` still used
  `POST /v2/resolve` despite all current route inventories, resolver QA,
  boundary audits, benchmarks, and evidence manifests requiring that route to
  remain unmounted.
- The runtime parity cases fixture already avoided `/v2/resolve*`, but the
  contract allowed future parity fixtures to reintroduce the forbidden route.
- GitNexus impact before edits:
  - `_validate_api_explorer_parity_case`: MEDIUM, direct impact through
    `validate_backbone_contract`, no affected processes.
  - `validate_backbone_contract`: CRITICAL root because many tests and shadow
    runners call the public validator; mitigation is a narrow route predicate
    plus the full backbone-focused test suite.

## Implementation Summary

- Added a contract guard rejecting v2 parity routes equal to `/v2/resolve` or
  prefixed by `/v2/resolve/trace`.
- Replaced the stale S2 readiness parity case with implemented
  `GET /v2/backbone/evidence` preview coverage.
- Added contract tests for `/v2/resolve`, `/v2/resolve/trace`, and
  `/v2/resolve/trace/:trace_id`.
- Added parity-runner preflight coverage proving forbidden resolver parity
  routes skip command execution.
- Generated fresh parity report
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T124014Z/api-explorer-parity-report.json`.

## Plan Critique

- [C001] Do not implement or mount runtime resolver routes.
- [C002] Do not weaken the resolver QA route-boundary checks.
- [C003] Treat this as a source-slice parity hardening change; downstream
  boundary, benchmark, and manifest evidence must be refreshed from a clean
  source commit after this slice lands.

## Execution Checklist

- [x] Confirm current repo state is clean and synced before edits.
- [x] Run GitNexus impact for the contract symbols.
- [x] Replace stale S2 `/v2/resolve` parity fixture entry.
- [x] Add contract and parity-runner negative tests.
- [x] Run focused and broad Python tests.
- [x] Generate fresh parity report.
- [x] Run Gemini/Kimi advisory review where available.
- [ ] Commit and push the source-slice evidence.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No live runtime performance threshold claim.

## Next Safe Slice

After this source slice is committed and pushed, regenerate route inventory,
boundary audit, benchmark, and evidence manifest from the clean source tree
using the new parity report.
