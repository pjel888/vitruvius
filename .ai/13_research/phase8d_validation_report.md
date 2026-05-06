# Phase 8D Validation Report

Run date: 2026-05-06

## Focused Tests

| Command | Result |
|---|---|
| `bun test api/resourceLayer.test.ts` | PASS, 38 pass |
| `bun test api/resourceEvidencePath.test.ts` | PASS, 21 pass |
| `bun test api/resourceLayerSourceVerification.test.ts` | PASS, 28 pass |
| `bun test api/resourceLayerExternalCandidates.test.ts` | PASS, 46 pass |
| `bun test api/resourceLayerExternalCandidateReview.test.ts` | PASS, 26 pass |
| `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts` | PASS, 56 pass |

## Validators

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS, resources 10, nodeResourceLinks 12, accepted 5, needs_review 6, rejected 1, blockers empty |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS, admitted 264, base 13670, effective 13934, `CROSS_DOMAIN_EQUIVALENT` 0, `CROSS_DOMAIN_ALIGNMENT` 22 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS, latest Resource Layer manifest hashes current, blockers empty |

## Full Suites

| Command | Result |
|---|---|
| `cd api && bun test` | PASS, 426 pass |
| `cd explorer && bun test` | PASS, 121 pass |
| `cd explorer && bun run build` | PASS, existing Vite chunk-size warning only |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 pass |

## Post-Validation Counts

| Metric | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| accepted nodeResourceLinks | 5 |
| needs_review nodeResourceLinks | 6 |
| rejected nodeResourceLinks | 1 |
| External metadata candidates | 15 |
| Admitted relationships | 264 |
| Base edges | 13670 |
| Effective edges | 13934 |
| CROSS_DOMAIN_EQUIVALENT | 0 |
| CROSS_DOMAIN_ALIGNMENT | 22 |

## Safety Checks

- No Resource was created.
- No nodeResourceLink was created.
- No accepted link was created.
- No learner exposure occurred.
- No external candidate appeared in learner mode.
- No protected payload was stored.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- No fake metadata or source-truth claim was introduced.
