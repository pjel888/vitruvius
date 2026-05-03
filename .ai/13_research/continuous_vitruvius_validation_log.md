# Continuous Vitruvius Validation Log

Date: 2026-05-03T01:00:00+08:00

## Validation Run

### Graph Relationships
- **Script**: `api/validateGraphRelationships.ts`
- **Result**: PASS
- **Nodes**: 10,018
- **Edges**: 13,927 (base 13,670 + admitted 257)
- **Issues**: 0

### Canonical Graph Stewardship
- **Script**: `api/validateCanonicalGraphStewardship.ts`
- **Result**: PASS
- **Decisions**: 17
- **Approvals**: 15
- **Admitted**: 257
- **Aliases/Redirects/Tombstones**: 0/0/0
- **Manifest chain**: Valid
- **AfterHash mismatches**: 0
- **Blockers**: []
- **Warnings**: 40 (all P1 packet unsigned/stale — known/expected)

### Resource Layer
- **Script**: `api/validateResourceLayer.ts`
- **Result**: PASS
- **Resources**: 7
- **NodeResourceLinks**: 9
- **Broken links**: 0
- **Blockers**: []
- **Warnings**: 5 (standards missing edition/context — known/expected)

### API Tests
- **Files**: 6 test files
- **Tests**: 141 pass, 0 fail
- **Files run**: canonicalGraphStewardship, graphRelationshipVisibility, mediumRiskP1StewardPacket, graphReasoningPaths, explorerPerformance, v2Backbone

### Explorer Build
- **Status**: Not run (deferred; prior build succeeded)

### Python Tests
- **Status**: Not run (deferred; pre-existing Windows `resource` module import errors)

## Signature

Validator: kimi-phase5-preflight
Run ID: phase5-validation-20260503-010000
