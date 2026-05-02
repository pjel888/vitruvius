# Continuous Vitruvius Validation Log

Date: 2026-05-02T14:21:57Z

## Targeted validation already run

- Graph relationships validator: pass; effective edges 13,750; admitted overlays 80.
- Canonical stewardship validator: pass; latest afterHash mismatches 0; transaction manifests 63.
- Resource Layer validator: pass; resources/nodeResourceLinks 7/9.
- Selected-node visibility: pass for 29/29 Wave 2 edges.

## Full validation

Final validation run before commit on 2026-05-02T14:25Z:

- `bun run api/validateGraphRelationships.ts`: pass; nodes 10,018; base edges 13,670; effective edges 13,750; admitted relationship overlays 80; issueCount 0.
- `bun run api/validateCanonicalGraphStewardship.ts`: pass; approvals 8; admittedRelationships 80; transactionManifests 63; latestAfterHashMismatches 0; P1 packets reviewed 20/20; P1 reviews carried forward 20.
- `bun run api/validateResourceLayer.ts`: pass; resources/nodeResourceLinks 7/9; only existing standard-context warnings; blockers 0.
- `cd api && bun test canonicalGraphStewardship.test.ts explorerPerformance.test.ts v2Backbone.test.ts`: pass; 119 tests.
- `cd api && bun test`: pass; 181 tests.
- `cd explorer && bun test`: pass; 112 tests.
- `cd explorer && bun run build`: pass; Vite chunk-size warning only.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: pass; 118 tests.
- Strict latest afterHash validation (`VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true`): pass; latestAfterHashMismatches 0.
- Strict packet-signature smoke (`VITRUVIUS_REQUIRE_PACKET_SIGNATURES=true`): expected fail with exit 1 because no packet HMAC key is configured; blockers are missing-key blockers only.
