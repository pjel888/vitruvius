# Phase 6D Preflight Validation Report

Date: 2026-05-03T05:00:00+08:00

## Git State

- Branch: `main`
- Sync with origin: `main...origin/main` (up to date)
- Last commit: `19fe8a62 Phase 6 planning: Resource / Evidence Layer source-custody readiness and node evidence strategy`
- Modified files (pre-existing):
  - `api/resourceLayer.test.ts` (Phase 6A changes)
  - `api/resourceLayer/validation.ts` (Phase 6A changes)
  - `003_Canonical-Knowledge-Layer/shared/sources/handout-cmo-61-series-2017-bs-architecture-curriculum-standards-7ab380.md` (pre-existing)
- Untracked files: many `003_Canonical-Knowledge-Layer/shared/sources/*.md` (pre-existing extraction artifacts)

## No-Write Validator Results

| Validator | Exit Code | Result |
|-----------|-----------|--------|
| `bun run api/validateResourceLayer.ts -- --no-write` | 0 | ok: true, blockers: [], errors: [] |
| `bun run api/validateGraphRelationships.ts -- --no-write` | 0 | ok: true |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | 0 | ok: true, manifestChainValid: true, latestAfterHashMismatches: 0 |

No files dirtied by no-write validators.

## Resource Layer Tests

- `bun test api/resourceLayer.test.ts`: 24 pass, 0 fail

## Graph Baseline

- Nodes: 10,018
- Effective edges: 13,934
- Base edges: 13,670
- Admitted relationships: 264
- Relation families: 15

## Resource Layer Baseline

- Resources: 7
- Node-resource links: 9
- Accepted links: 5
- Needs-review links: 3
- Rejected links: 1
- Candidates: 4
- Local files indexed: 25
- Local files admitted: 0
- Standards total: 2
- Standards missing context: 2
- Standards promotion blocked: 3

## ASCE 7 / ACI 318 Status

- ASCE 7 (res-asce-7-official-landing): 2 links in `needs_review`, missing edition/version/scope
- ACI 318 (res-aci-318-building-code-portal): 1 link in `rejected`, missing edition/version/scope
- Neither is learner-trusted or promoted

## Discrepancies

None. All expected state matches verified state.
