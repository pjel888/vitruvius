# Phase 8F Validation Report

**Date:** 2026-05-06

## Focused Validation

| Command | Status | Result |
|---|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS | Resources 10, nodeResourceLinks 12, accepted 8, blockers [] |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS | admitted 265, base 13,670, effective 13,935, issues 0 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS | admittedRelationships 265, manifest chain valid, latest afterHash mismatches 0, blockers [] |
| `bun test api/canonicalGraphStewardship.test.ts api/graphRelationshipVisibility.test.ts api/graphReasoningPaths.test.ts api/explorerPerformance.test.ts api/v2Backbone.test.ts` | PASS | 142 pass, 0 fail |

## Focused Fix During Validation

Initial focused tests caught an API exposure wording issue: the first admitted edge provenance contained the guarded phrase `protected content`.

Resolution:

- Rolled back first admission with manifest `canonical-tx-20260506122915-7732219460b9`.
- Re-admitted the same reviewed edge with API-safe wording `protected payload not stored`.
- Focused tests then passed.

## Full Validation

Full validation was run after report updates and final review.

| Command | Status |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS |
| `cd api && bun test` | PASS - 432 pass, 0 fail |
| `cd explorer && bun test` | PASS - 121 pass, 0 fail |
| `cd explorer && bun run build` | PASS_WITH_WARNING |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS - 118 pass |

Additional regression check:

- `bun test api/mediumRiskP1StewardPacket.test.ts`: PASS - 4 pass after narrowing empty-registry assertions to the actual `aliases`, `redirects`, and `tombstones` arrays now present under manifest custody.

## Safety Confirmation

- No fake metadata introduced.
- No protected payload stored.
- No Resource created.
- No nodeResourceLink created.
- No learner Resource/candidate exposure changed.
- No graph node, alias, redirect, tombstone, merge, or canonicalization mutation.
- No P0 Concrete/Reinforced Concrete mutation.
- No high-risk P1 mutation.
- No `CROSS_DOMAIN_EQUIVALENT`.
- No generic `related_to`.
