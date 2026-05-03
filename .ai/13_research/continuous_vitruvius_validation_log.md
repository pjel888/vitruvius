# Continuous Vitruvius Validation Log

Date: 2026-05-03T02:15:00+08:00

## Validation Run

### Graph Relationships
- **Script**: `api/validateGraphRelationships.ts`
- **Result**: PASS
- **Nodes**: 10,018
- **Edges**: 13,934 (base 13,670 + admitted 264)
- **Issues**: 0

### Canonical Graph Stewardship
- **Script**: `api/validateCanonicalGraphStewardship.ts`
- **Result**: PASS
- **Decisions**: 18
- **Approvals**: 16
- **Admitted**: 264
- **Aliases/Redirects/Tombstones**: 0/0/0
- **Manifest chain**: Valid
- **AfterHash mismatches**: 0
- **Stale manifest files**: 0
- **Blockers**: []
- **Warnings**: 41 (P1 packet unsigned/stale — known/expected; one P2 packet mislabeled)

### Resource Layer
- **Script**: `api/validateResourceLayer.ts`
- **Result**: PASS
- **Resources**: 7
- **NodeResourceLinks**: 9
- **Broken links**: 0
- **Blockers**: []
- **Warnings**: 5 (standards missing edition/context — known/expected)

### API Tests
- **Files**: 12 test files
- **Tests**: 202 pass, 0 fail

### Explorer Tests
- **Files**: 12 test files
- **Tests**: 112 pass, 0 fail

### Explorer Build
- **Status**: PASS

### Python Tests
- **File**: `scripts/tests/test_kg_aec_relationship_improvement.py`
- **Tests**: 118 pass, 0 fail

### Graph Reasoning Paths Tests
- **File**: `api/graphReasoningPaths.test.ts`
- **Tests**: 18 pass, 0 fail (4 new tests added in Phase 5 quality gate hardening)

## Summary

All validations pass. Zero failures across all test suites. Graph state is clean and regression-resistant.
