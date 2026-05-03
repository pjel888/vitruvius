# Phase 6G External Candidate Tests Report

**Generated:** 2026-05-03T01:00:00+08:00

---

## API Tests (`api/resourceLayerExternalCandidates.test.ts`)

**Total tests:** 45 (24 from 6E + 21 new)

### New Persistence Tests (21)

1. Persist route requires dev/admin gate
2. Persist route re-runs preview validation
3. Persist route rejects placeholder URL
4. Persist route rejects placeholder DOI
5. Persist route rejects placeholder ISBN
6. Persist route rejects placeholder standard context
7. Persist route creates external candidate only
8. Persisted candidate has learnerVisible=false
9. Persisted candidate has displayPolicy=reviewer_only
10. Persisted candidate has verificationStatus=unverified
11. Persisted candidate has reviewRequired=true
12. Persisted candidate has noAutoVerification/noAutoPromotion/noAutoLinking/noLearnerExposure
13. Persisted standard candidate with missing edition/scope remains reviewer-only
14. Duplicate candidate detection catches same URL
15. Transaction manifest is written for candidate registry changes
16. GET list route is gated
17. GET list route returns persisted candidates
18. GET detail route is gated
19. Source-custody queue route is gated
20. Persisted candidate does not appear in learner node resources
21. No graph/canonical registry mutation occurs on persist

### Test Setup

- `beforeEach` resets `external-metadata-candidates.json` to empty array
- Prevents cross-test contamination

---

## Explorer Tests

### ResourceReviewAdmin.test.tsx

Existing tests updated:
- Text assertion updated to match new safe wording ("accepted candidates")
- Optional chaining fix for `warningFlags`

---

## Integration Test Mocks

`app.searchInspector.integration.test.tsx`:
- Added `persistExternalMetadataCandidate`
- Added `listExternalMetadataCandidates`
- Added `getExternalMetadataCandidate`

---

## Full Suite Results

| Suite | Tests | Pass | Fail |
|-------|-------|------|------|
| API (full) | 301 | 301 | 0 |
| Explorer | 118 | 118 | 0 |
| Explorer build | — | PASS | — |
| Python KG | 118 | 118 | 0 |
| ResourceLayer no-write | — | PASS | — |
| Graph no-write | — | PASS | — |
| Canonical no-write | — | PASS | — |
