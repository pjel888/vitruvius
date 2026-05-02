# Continuous Vitruvius Validation Log

Date: 2026-05-02T11:26:21Z

## Completed validations

- `bun run api/validateGraphRelationships.ts`: pass; nodes=10018, baseEdges=13670, effectiveEdges=13721, admittedRelationshipEdgeCount=51, issueCount=0.
- `bun run api/validateCanonicalGraphStewardship.ts`: pass; approvals=7, admittedRelationships=51, P1 reviewed=20/20, P1 content hash mismatches=0, stale source snapshots=0, transactionManifests=60, latestAfterHashMismatches=0.
- `bun run api/validateResourceLayer.ts`: pass; resources=7, nodeResourceLinks=9; standard-context warnings remain non-blocking and unchanged.
- `cd api && bun test`: pass; 180 tests, 0 failures.
- `cd explorer && bun test`: pass; 112 tests, 0 failures.
- `cd explorer && bun run build`: pass; Vite chunk-size warning only.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: pass; 118 tests.
- Selected-node visibility script: pass for all 25 new Phase 4 Wave 1 edges.
- Strict latest-afterHash validation: pass with `VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true`; latestAfterHashMismatches=0.
- Strict packet-signature smoke: expected non-zero exit because no `VITRUVIUS_PACKET_HMAC_KEY` is configured; blockers were missing-key-only for 20 unsigned packets. Non-strict validation was rerun afterward and passed.

## Tooling notes

- `morph_mcp.codebase_search` returned HTTP 429 during initial exploration.
- `docs/shared/agent-tiers.md` required by the Ultrawork skill was missing.
- ChunkHound regex search hit a Windows cp1252 output encoding issue during one broad search; targeted searches and code-intelligence refresh otherwise ran.
