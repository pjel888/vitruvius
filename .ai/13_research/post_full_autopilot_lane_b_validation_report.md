# Post-Full Autopilot Lane B Validation Report

Date: 2026-05-07

## Focused Validation

| Command | Result |
|---|---|
| `bun test api/resourceLayerExternalCandidates.test.ts` | PASS, 46 tests |
| `bun test api/resourceLayerSourceVerification.test.ts` | PASS, 29 tests |
| `bun test api/resourceLayerExternalCandidateReview.test.ts` | PASS, 26 tests |
| `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts` | PASS, 56 tests |

## Full Validation

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS, blockers `[]` |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS, issueCount 0 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS, latest Resource Layer candidate manifest hash matched |
| `cd api && bun test` | PASS, 434 tests |
| `cd explorer && bun test` | PASS, 122 tests |
| `cd explorer && bun run build` | PASS with existing Vite chunk-size warning |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 tests |

## Counts After Apply

| Metric | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| Accepted links | 9 |
| External metadata candidates | 17 |
| Admitted relationships | 266 |
| Base edges | 13,670 |
| Effective edges | 13,936 |
| CROSS_DOMAIN_EQUIVALENT | 0 |
| CROSS_DOMAIN_ALIGNMENT | 22 |
