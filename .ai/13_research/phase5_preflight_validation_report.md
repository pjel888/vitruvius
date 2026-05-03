# Phase 5 Preflight Validation Report

Date: 2026-05-03T01:00:00+08:00

## Validation Scripts Run

### 1. validateGraphRelationships.ts

```json
{
  "ok": true,
  "nodeCount": 10018,
  "edgeCount": 13927,
  "baseEdgeCount": 13670,
  "admittedRelationshipEdgeCount": 257,
  "issueCount": 0,
  "issues": []
}
```

**Status: PASS**

### 2. validateCanonicalGraphStewardship.ts

```json
{
  "ok": true,
  "admittedRelationships": 257,
  "approvals": 15,
  "stewardshipDecisions": 17,
  "aliases": 0,
  "redirects": 0,
  "tombstones": 0,
  "manifestChainValid": true,
  "latestAfterHashMismatches": 0,
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
| `api/graphRelationshipVisibility.test.ts` | 3 | 0 | Neighborhood visibility |
| `api/mediumRiskP1StewardPacket.test.ts` | 4 | 0 | Medium-risk packet regression |
| `api/graphReasoningPaths.test.ts` | 14 | 0 | New Phase 5 reasoning paths |
| `api/explorerPerformance.test.ts` | 1 | 0 | Render contract |
| `api/v2Backbone.test.ts` | 80 | 0 | API contract |
| **Total** | **141** | **0** | |

## Not Run (documented)

- `cd explorer && bun test` — deferred; API tests confirm graph shape
- `cd explorer && bun run build` — deferred; prior build succeeded in earlier waves
- `python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` — deferred; Python test environment has pre-existing `resource` module import errors on Windows

## Conclusion

All graph, canonical, and resource validations pass with zero blockers. The 141 API tests covering stewardship, visibility, P1 packets, reasoning paths, performance, and v2 backbone all pass. No validation blockers for Phase 5 audit work.
