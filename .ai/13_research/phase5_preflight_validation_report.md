# Phase 5 Preflight Validation Report

Date: 2026-05-03T01:40:00+08:00

## Validation Scripts Run

### 1. validateGraphRelationships.ts

```json
{
  "ok": true,
  "nodeCount": 10018,
  "edgeCount": 13934,
  "baseEdgeCount": 13670,
  "admittedRelationshipEdgeCount": 264,
  "issueCount": 0,
  "issues": []
}
```

**Status: PASS**

### 2. validateCanonicalGraphStewardship.ts

```json
{
  "ok": true,
  "admittedRelationships": 264,
  "approvals": 16,
  "stewardshipDecisions": 18,
  "aliases": 0,
  "redirects": 0,
  "tombstones": 0,
  "manifestChainValid": true,
  "latestAfterHashMismatches": 0,
  "staleManifestFiles": 0,
  "blockers": []
}
```

**Status: PASS** (warnings only: unsigned P1 packets and stale source snapshots, both known/expected)

### 3. validateResourceLayer.ts

```json
{
  "ok": true,
  "resources": 7,
  "nodeResourceLinks": 9,
  "brokenLinkCount": 0,
  "duplicateCount": 0,
  "blockers": []
}
```

**Status: PASS**

## Targeted Test Runs

| Test File | Pass | Fail | Notes |
|-----------|------|------|-------|
| `api/canonicalGraphStewardship.test.ts` | 39 | 0 | Full stewardship validation |
| `api/graphRelationshipVisibility.test.ts` | 4 | 0 | Neighborhood visibility |
| `api/mediumRiskP1StewardPacket.test.ts` | 4 | 0 | Medium-risk packet regression |
| `api/graphReasoningPaths.test.ts` | 14 | 0 | All reasoning paths pass |
| `api/explorerPerformance.test.ts` | 5 | 0 | Render contract |
| `api/v2Backbone.test.ts` | 80 | 0 | API contract |
| `explorer/` | 112 | 0 | Explorer component + integration |
| `spatial-daemon/` | 21 | 0 | Spatial geometry tests |
| `scripts/tests/test_kg_aec_relationship_improvement.py` | 118 | 0 | Python KG tests |
| **Total** | **397** | **0** | |

## Explorer Build

- `cd explorer && bun run build` — **PASS** (252ms, no errors)

## Conclusion

All graph, canonical, and resource validations pass with zero blockers. All 397 tests across API, Explorer, spatial-daemon, and Python pass. Manifest chain is valid with zero afterHash mismatches. No validation blockers for Phase 5 work.
