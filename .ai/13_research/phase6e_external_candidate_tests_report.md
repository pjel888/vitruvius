# Phase 6E External Candidate Tests Report

**Generated:** 2026-05-03
**Status:** All passing

---

## API Tests

**File:** `api/resourceLayerExternalCandidates.test.ts`
**Results:** 24 pass, 0 fail

### Validation Tests (20 tests)
1. URL candidate accepts valid HTTPS, marks unverified, learnerVisible=false
2. URL candidate rejects placeholder URLs
3. URL candidate rejects non-http/https schemes
4. DOI candidate accepts syntax, marks unverified
5. DOI candidate rejects placeholder DOI
6. ISBN candidate accepts syntax, marks unverified
7. ISBN candidate rejects placeholder ISBN
8. Book candidate requires title, remains reviewer-only
9. Book candidate missing title is invalid
10. PDF candidate remains reviewer-only, no protected payload
11. Standard candidate missing context remains reviewer-only
12. Standard candidate placeholder edition/version/scope rejected
13. Preview route writes no files
14. Preview route creates no resources/links/candidates/manifests
15. Preview route requires local/dev/admin gate
16. Resource Layer counts unchanged after preview
17. ASCE 7 / ACI 318 remain not learner-trusted
18. No fake metadata becomes learner-eligible
19. detectExternalMetadataPlaceholders flags all placeholder types
20. classifyExternalCandidate categorizes correctly

### API Route Tests (4 tests)
21. GET /resources/review/external-candidates/schema returns schema
22. POST /resources/review/external-candidates/preview returns normalized preview
23. POST preview rejects placeholder URLs
24. POST preview requires local/dev/admin gate

---

## Explorer Tests

**File:** `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`
**Results:** 2 new tests added, all passing

1. External Candidates tab renders preview form with safe wording
2. External Candidates form has all required fields and safe labels

---

## Full Suite Results

| Suite | Tests | Pass | Fail |
|-------|-------|------|------|
| API (full) | 280 | 280 | 0 |
| Explorer | 118 | 118 | 0 |
| Python KG | 118 | 118 | 0 |
| Explorer Build | — | PASS | — |

---

*No production data mutated. No graph changes. No canonical changes.*
