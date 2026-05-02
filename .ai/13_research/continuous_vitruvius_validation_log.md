# Continuous Vitruvius Validation Log

Date: 2026-05-02T10:58:14Z

## Targeted validation after Phase 3 admission

- `bun run api/validateGraphRelationships.ts`: passed, effective edges 13,696, admitted overlay edges 26.
- `bun run api/validateCanonicalGraphStewardship.ts`: passed, approvals 6, admitted relationships 26, transaction manifests 56, latest afterHash mismatches 0.
- `bun run api/validateResourceLayer.ts`: passed, resources 7, nodeResourceLinks 9.
- API neighborhood visibility script: passed for all 12 new Phase 3 edges.

## Broad validation before checkpoint

- `cd api && bun test`: passed, 179 tests.
- `cd explorer && bun test`: passed, 112 tests.
- `cd explorer && bun run build`: passed; Vite emitted the existing chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: passed, 118 tests.
- Strict latest-afterHash validation: passed, latest afterHash mismatches 0.
- Strict packet-signature smoke: produced expected missing-HMAC-key blockers only (`strict_signature_exit=1`); non-strict canonical validation was rerun and passed.
