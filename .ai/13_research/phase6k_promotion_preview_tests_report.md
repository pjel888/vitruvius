# Phase 6K Promotion Preview Tests Report

**Date:** 2026-05-03
**Status:** Implemented
**File:** `api/resourceLayerExternalCandidatePromotionPreview.test.ts`

---

## Test Coverage

| # | Test | Status |
|---|---|---|
| 1 | promotion-preview requires dev/admin gate | ✅ pass |
| 2 | promotion-preview is read-only and writes no files | ✅ pass |
| 3 | promotion-preview creates no resource, no nodeResourceLink, no decision, no manifest | ✅ pass |
| 4 | promotion-preview returns blockers for candidate status candidate/needs_review | ✅ pass |
| 5 | promotion-preview returns blockers for rejected/deferred/duplicate/promotion_blocked | ✅ pass |
| 6 | promotion-preview returns blockers if readiness gates fail | ✅ pass |
| 7 | promotion-preview returns blockers for incomplete standards context | ✅ pass |
| 8 | promotion-preview returns preview-only proposed resource draft for ready candidate | ✅ pass |
| 9 | promotion-preview returns preview-only proposed node-link drafts when valid | ✅ pass |
| 10 | promotion-preview returns blockers for invalid proposedRelation | ✅ pass |
| 11 | promotion-preview performs no external verification | ✅ pass |
| 12 | GET /node/:id/resources still hides external candidates | ✅ pass |
| 13 | source-custody queue remains reviewer-only after promotion preview | ✅ pass |
| 14 | registry is empty after test cleanup | ✅ pass |

## API Test Suite Result

- **14/14 pass** in `resourceLayerExternalCandidatePromotionPreview.test.ts`
- **342/342 pass** across full API suite (16 files)
- **118/118 pass** Explorer suite
- **118/118 pass** Python suite

## No-Mutation Confirmations

- Resources remain 7
- nodeResourceLinks remain 9
- External candidate registry empty after tests
- No graph/canonical/registry mutation
- No transaction manifests created by promotion preview
