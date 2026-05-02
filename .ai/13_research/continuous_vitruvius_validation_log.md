# Continuous Vitruvius Validation Log

Date: 2026-05-02T09:55:00Z

## Commands run

- `bun run api/validateGraphRelationships.ts` - pass; effective edges 13,684, base edges 13,670, admitted overlays 14.
- `bun run api/validateCanonicalGraphStewardship.ts` - pass; P1 reviewed/unreviewed 20/0; stale snapshots 0; stale reviews 0; afterHash mismatches 0.
- `bun run api/validateResourceLayer.ts` - pass with existing standards-context warnings only.
- `bun test api/canonicalGraphStewardship.test.ts` - pass, 36 tests.
- `cd api && bun test` - pass, 178 tests.
- `cd explorer && bun test` - pass, 112 tests.
- `cd explorer && bun run build` - pass; Vite chunk-size warning only.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - pass, 118 tests.
- Strict latest-afterHash validation - pass.
- Strict packet-signature smoke - expected fail/block because no HMAC key is configured; missing-key blockers only.

## Visibility checks covered

- Deep/Shallow Foundation `CROSS_DOMAIN_ALIGNMENT` overlays remain visible through selected-node neighborhoods.
- First ACS `CONSTRAINS` overlays remain visible.
- Second ACS `TRANSFERS_LOAD_TO`, `DISCHARGES_TO`, and `COORDINATES_WITH` overlays are covered by API regression tests.
- Sendai Mediatheque / Toyo Ito `HAS_FACET` regression remains visible.

## Manual selected-node visibility check

- VTN-DOM-0012263 -> VTN-DOM-0012269 TRANSFERS_LOAD_TO: visible.
- VTN-DOM-0012764 -> VTN-DOM-0002899 DISCHARGES_TO: visible.
- VTN-DOM-0012165 -> VTN-DOM-0012261 COORDINATES_WITH: visible.
- Deep Foundations CROSS_DOMAIN_ALIGNMENT: visible.
- Sendai Mediatheque / Toyo Ito HAS_FACET: visible.
- Dynamic graph edge filters include TRANSFERS_LOAD_TO, DISCHARGES_TO, and COORDINATES_WITH; graph edge count returned 13,684.

## Code-intelligence checks

- `bash ./scripts/refresh_code_intelligence.sh`: completed; GitNexus up to date, ChunkHound indexed 38 changed files with 0 file errors, code-review-graph rebuilt. Known warnings: missing `tree-sitter-yaml` for YAML parsing and embedding-provider context-length errors during code-review-graph embedding batches.
- `npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged`: completed; 42 staged files, 16 changed symbols, 5 affected flows, risk level medium.
- `chunkhound search --regex "TRANSFERS_LOAD_TO|DISCHARGES_TO|COORDINATES_WITH"`: completed; semantic/custody report hits found for changed relation vocabulary and reports.
