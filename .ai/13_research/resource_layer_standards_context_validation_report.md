# Resource Layer Standards Context Validation Report

Date: 2026-05-02
Status: passed with honest standards-context warnings

## Resource Layer validation
Command: `bun run api/validateResourceLayer.ts`

Result: passed.

Metrics:
- resources: 7
- nodeResourceLinks: 9
- sourceFamilies: 25
- resourceCandidates: 4
- accepted links: 5
- needs_review links: 3
- rejected links: 1
- local files indexed: 25
- local files admitted: 0
- standards_total: 2
- standards_missing_context: 2
- standards_missing_edition: 2
- standards_missing_jurisdiction: 0
- standards_missing_scope: 3
- standards_context_complete: 0
- standards_context_partial: 1
- standards_context_needs_review: 2
- standards_accepted_missing_context: 0
- standards_promotion_blocked: 3
- standards_context_reviewable: 3
- blockers: 0
- errors: 0

Warnings remain honest:
- `res-asce-7-official-landing`: missing edition/version context.
- `res-aci-318-building-code-portal`: missing edition/version context.
- ASCE wind/seismic links: missing edition/version and citation/scope context.
- ACI structural-column link: missing edition/version and citation/scope context, while still rejected.

## API tests
Command: `cd api && bun test`

Result: passed, 163 tests.

Resource Layer targeted command: `bun test api/resourceLayer.test.ts`

Result: passed, 19 tests.

## Explorer tests and build
Command: `cd explorer && bun test`

Result: passed, 112 tests.

Command: `cd explorer && bun run build`

Result: passed with the known Vite chunk-size warning.

## Graph and canonical validation
Command: `bun run api/validateGraphRelationships.ts`

Result: passed. Nodes 10,018; edges 13,670; issueCount 0.

Command: `bun run api/validateCanonicalGraphStewardship.ts`

Result: passed. Duplicate groups remain 544; unresolved groups remain 544; P0 groups remain 2; approvals/admitted relationships remain 0.

## AEC relationship workflow regression
Command: `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

Result: passed, 104 tests.

## Data mutation status
No production Resource Layer values were added. No ASCE 7 or ACI 318 edition/version/scope values were filled. No links/resources were promoted. No graph edges changed.
