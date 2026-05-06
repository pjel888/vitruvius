# Phase 8G Validation Report

**Date:** 2026-05-06

## Focused Tests

| Command | Result |
|---|---|
| `bun test api/resourceLayer.test.ts` | PASS, 43 pass |
| `bun test api/resourceEvidencePath.test.ts` | PASS, 21 pass |
| `bun test api/resourceLayerSourceVerification.test.ts` | PASS, 28 pass |
| `bun test api/graphReasoningPaths.test.ts api/graphRelationshipVisibility.test.ts api/canonicalGraphStewardship.test.ts` | PASS, 63 pass |

## Full Validation

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS, resources 10, nodeResourceLinks 12, accepted 8, blockers 0 |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS, admitted 266, base 13670, effective 13936, issues 0 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS, admitted relationships 266, transaction manifests 141, blockers 0 |
| `cd api; bun test` | PASS, 433 pass |
| `cd explorer; bun test` | PASS, 121 pass |
| `cd explorer; bun run build` | PASS with existing Vite chunk-size warning |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 pass |
| `bash ./scripts/refresh_code_intelligence.sh` | PASS_WITH_WARNINGS, GitNexus current; ChunkHound timed out known large files and code-review-graph warned on missing `tree-sitter-yaml` |
| `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` | PASS, 33 files, 1 symbol, 0 affected processes, low risk |

## Counts After Phase 8G

| Metric | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| Accepted Resource Layer links | 8 |
| External metadata candidates | 15 |
| Learner-visible external candidates | 0 |
| Admitted relationships | 266 |
| Base edges | 13670 |
| Effective edges | 13936 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 |

## Safety Verification

- No fake metadata introduced.
- No protected payload stored.
- No learner overexposure occurred.
- No Resource Layer registry mutation occurred.
- No Resource or nodeResourceLink was created.
- No graph node, alias, redirect, tombstone, merge, or canonicalization mutation occurred.
- No P0 Concrete/Reinforced Concrete mutation occurred.
- No high-risk P1 packet mutation occurred.
- No source-truth/current/governing/compliance/AHJ/jurisdiction/numerical/design-adequacy claim was introduced.
