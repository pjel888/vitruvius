# Phase 6F — Evidence-Path Coverage Report

Date: 2026-05-03

## Coverage Matrix

| Safety Rule | Test File | Test Name | Status |
|-------------|-----------|-----------|--------|
| **Learner sidebar eligibility** | | | |
| accepted/human_reviewed only | `api/resourceEvidencePath.test.ts` | `GET /node/:id/resources returns only accepted/human_reviewed links` | ✅ |
| rejected hidden | `api/resourceEvidencePath.test.ts` | `learner mode never returns rejected, needs_review, candidate, or rights-blocked resources` | ✅ |
| needs_review hidden | `api/resourceEvidencePath.test.ts` | `learner mode never returns rejected, needs_review, candidate, or rights-blocked resources` | ✅ |
| candidate hidden | `api/resourceEvidencePath.test.ts` | `learner mode never returns rejected, needs_review, candidate, or rights-blocked resources` | ✅ |
| rights-blocked hidden | `api/resourceEvidencePath.test.ts` | `learner mode never returns rejected, needs_review, candidate, or rights-blocked resources` | ✅ |
| unverified hidden | `api/resourceLayer.test.ts` | `learner mode filters out rights-protected and incomplete-standards resources` | ✅ |
| incomplete standards hidden | `api/resourceEvidencePath.test.ts` | `ASCE 7 is not learner-visible via endpoint` | ✅ |
| hard cap at 8 | `api/resourceEvidencePath.test.ts` | `learner mode hard-caps at 8 resources` | ✅ |
| empty safe state | `api/resourceEvidencePath.test.ts` | `learner mode returns empty safe state for node with no accepted resources` | ✅ |
| **Reviewer source-custody queue** | | | |
| 9 groups exist | `api/resourceEvidencePath.test.ts` | `GET /resources/review/source-custody returns all 9 groups` | ✅ |
| learnerVisible group | `api/resourceEvidencePath.test.ts` | `source-custody queue marks accepted links as learner-visible` | ✅ |
| needsReview group | `api/resourceEvidencePath.test.ts` | `source-custody queue includes needs_review links` | ✅ |
| blocked group | `api/resourceEvidencePath.test.ts` | `source-custody queue includes rejected/blocked items` | ✅ |
| standardsIncomplete group | `api/resourceEvidencePath.test.ts` | `source-custody queue includes nextReviewAction and missingStandardContextFields` | ✅ |
| localFilesIndexedOnly group | `api/resourceEvidencePath.test.ts` | `source-custody queue includes local files as indexed-only` | ✅ |
| candidates group | `api/resourceEvidencePath.test.ts` | `source-custody queue includes candidates` | ✅ |
| nextReviewAction present | `api/resourceEvidencePath.test.ts` | `source-custody queue includes nextReviewAction and missingStandardContextFields` | ✅ |
| missingFields present | `api/resourceEvidencePath.test.ts` | `source-custody queue includes nextReviewAction and missingStandardContextFields` | ✅ |
| **Standards-context path** | | | |
| ASCE 7 blocked | `api/resourceEvidencePath.test.ts` | `ASCE 7 and ACI 318 remain not learner-trusted in production` | ✅ |
| ACI 318 blocked | `api/resourceEvidencePath.test.ts` | `ASCE 7 and ACI 318 remain not learner-trusted in production` | ✅ |
| Placeholder rejection | `api/resourceLayerStandardsContext.test.ts` | `placeholder standard edition values are rejected` | ✅ |
| Justified missing context | `api/resourceLayerStandardsContext.test.ts` | `justified missing context requires reviewer, rationale, sourceOfContext` | ✅ |
| Complete standard visible | `api/resourceLayerStandardsContext.test.ts` | `human_reviewed complete standard is learner-visible` | ✅ |
| **Local-file path** | | | |
| Indexed-only visible to reviewer | `api/resourceEvidencePath.test.ts` | `source-custody queue includes local files as indexed-only` | ✅ |
| Not learner-visible | `api/resourceEvidencePath.test.ts` | `source-custody queue includes local files as indexed-only` | ✅ |
| Not auto-linked | `api/resourceLayer.test.ts` | `serves the reviewer queue and review metrics without changing learner resources` | ✅ |
| **Rights/protected path** | | | |
| Rights-protected blocked | `api/resourceLayer.test.ts` | `learner mode filters out rights-protected and incomplete-standards resources` | ✅ |
| Warning text | `api/resourceLayer.test.ts` | `reviewer mode includes non-eligible resources with warning text` | ✅ |
| **No-mutation contract** | | | |
| GET /node/:id/resources read-only | `api/resourceEvidencePath.test.ts` | `GET /node/:id/resources does not mutate Resource Layer registries` | ✅ |
| GET /resources/review/source-custody read-only | `api/resourceEvidencePath.test.ts` | `GET /resources/review/source-custody does not mutate Resource Layer registries` | ✅ |
| buildSourceCustodyQueue stable | `api/resourceEvidencePath.test.ts` | `source-custody queue build is read-only and stable across repeated calls` | ✅ |
| Counts stable after routes | `api/resourceEvidencePath.test.ts` | `Resource Layer counts remain 7 resources / 9 links after route calls` | ✅ |
| No-write validators clean | `api/resourceLayerStandardsContext.test.ts` | `Resource Layer no-write validation does not dirty files` | ✅ |
| **Explorer UI** | | | |
| Source Custody tab renders | `ResourceReviewAdmin.test.tsx` | `Source Custody tab renders grouped queue with safe badges` | ✅ |
| Local files indexed-only badge | `ResourceReviewAdmin.test.tsx` | `Source Custody tab shows local files as indexed-only and not admitted` | ✅ |
| Needs review safe wording | `ResourceReviewAdmin.test.tsx` | `Source Custody tab shows needs_review items with safe wording` | ✅ |
| Metrics overview | `ResourceReviewAdmin.test.tsx` | `Source Custody metrics render in overview section` | ✅ |
| **Fixture safety** | | | |
| No placeholder learner-eligible | `api/resourceEvidencePath.test.ts` | `no production placeholder metadata is learner-eligible` | ✅ |

## Summary

- **API tests:** 21 new evidence-path tests + 38 existing Resource Layer tests + 17 standards-context tests = 76 tests
- **Explorer tests:** 8 ResourceReviewAdmin tests (4 new Source Custody tests + 4 existing)
- **Total test coverage:** 256 API tests pass, 100+ Explorer tests pass
- **No production mutation verified:** Yes
- **No-write validators clean:** Yes
