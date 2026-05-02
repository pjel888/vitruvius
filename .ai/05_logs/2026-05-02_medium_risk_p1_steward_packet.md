

## Validation results



## 2026-05-02T05:27:58Z - Medium-risk P1 steward packet validation

Commands run:

- `bun test api/mediumRiskP1StewardPacket.test.ts` - passed, 4 tests.
- `bun test api/canonicalGraphStewardship.test.ts api/mediumRiskP1StewardPacket.test.ts` - passed, 32 tests.
- `cd api && bun test` - passed, 170 tests.
- `cd explorer && bun test` - passed, 112 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed; P1 packets 20, reviewed 8, unreviewed 12, approvals 0, admitted relationships 0, aliases/redirects/tombstones 0/0/0, latest afterHash mismatches 0.
- `bun run api/validateGraphRelationships.ts` - passed; nodes 10,018, edges 13,670, issues 0.
- `bun run api/validateResourceLayer.ts` - passed with known honest standards-context warnings; resources 7, nodeResourceLinks 9, blockers 0.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 104 tests.

Validation conclusion: medium-risk steward packet and admission preview are advisory-only and non-mutating. No graph/resource/canonical mutation registry counts changed.
