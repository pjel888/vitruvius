---
task: aec-mepfs-shadow-parity-fixture-hardening
phase: 05
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Thirty-First Shadow Slice: Parity Fixture Coverage Hardening

## Scope

Harden the file-backed API/Explorer parity runner so the existing
`search_invalid_query` parity fixture case is a required category, not merely an
optional case that could be deleted without failing the coverage gate.

This slice changes only the parity runner gate, its regression test, generated
parity evidence, and governance docs. It does not promote the shadow graph,
write or query Neo4j, rebuild the KG, ingest protected content, change feature
flags, mount `/v2/resolve`, or make Explorer adopt the shadow graph by default.

## Implementation

- Added `search_invalid_query` to `REQUIRED_PARITY_CASE_CATEGORIES` in
  `scripts/vitruvius/kg/backbone_parity_runner.py`.
- Added a regression test proving the parity runner fails if the
  `search_invalid_query` fixture case is removed.
- Generated fresh parity evidence:
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T113000Z/api-explorer-parity-report.json`.

## Audit Findings

- The parity fixture already contained `API-PARITY-002A` for empty/invalid
  `/v2/search` queries.
- The runner required 25 categories but the fixture contained 26 cases; the
  missing required category was `search_invalid_query`.
- GitNexus impact for `_validate_parity_case_coverage` returned LOW risk, with
  impact limited to `run_parity_fixture` and parity-runner tests.
- The fresh parity report passes 6/6 commands and 26/26 cases and now records
  `search_invalid_query` in `required_case_categories`.

## Plan Critique

- [C001] Do not treat this as runtime resolver work; it only strengthens the
  parity fixture coverage gate.
- [C002] Do not refresh downstream boundary/benchmark/evidence reports in the
  same source-dirty code slice. Refresh them after this slice is committed so
  repo-state evidence can remain source-clean.
- [C003] Keep `/v2/search` invalid-query behavior additive, file-backed, and
  fail-closed.

## Execution Checklist

- [x] Inspect parity fixture categories and runner-required categories.
- [x] Run GitNexus impact on the parity coverage validator.
- [x] Require `search_invalid_query` in the parity runner.
- [x] Add a focused regression test.
- [x] Generate fresh parity evidence.
- [x] Run focused and broad Python backbone tests.
- [x] Run Gemini/Kimi advisory review where available.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No downstream boundary/benchmark/evidence refresh in this source-dirty slice.

## Next Safe Slice

After this parity hardening is committed and pushed, refresh boundary audit,
benchmark, and evidence manifest from the clean source tree using the new parity
report. Runtime integration remains blocked.
