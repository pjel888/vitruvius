# Phase 6I Next Actions

**Date:** 2026-05-03
**Status:** Implementation Complete

## What Was Implemented

1. **Review state and decision types** — 11 review states, 11 decision types in `api/resourceLayer/externalCandidateReview.ts`
2. **Correction preview/apply** — `POST .../correction-preview` and `POST .../correction`
3. **Review decision preview/apply** — `POST .../review-preview` and `POST .../review-decision`
4. **Decision history** — `GET .../history`
5. **Promotion readiness helper** — `buildExternalCandidatePromotionReadiness()` with 8 gates
6. **Source-custody queue integration** — Updated `enrichExternalCandidateItem()` to reflect review states
7. **ResourceReviewAdmin UI** — ExternalCandidateReviewPanel with detail, correction, decision, history tabs
8. **Tests** — 26 new API tests in `api/resourceLayerExternalCandidateReview.test.ts`

## What Was NOT Implemented

- Candidate-to-resource promotion apply
- Resource creation from candidates
- NodeResourceLink creation from candidates
- External verification (URL/DOI/ISBN fetching)
- Graph/canonical mutation

## Next Actions

1. **Phase 6J audit** — Independent audit of 6I implementation
2. **Phase 6K (future, needs authorization)** — Promotion preview (read-only candidate-to-resource preview)
3. **Phase 6L (future, needs separate authorization)** — Promotion apply (create Resource and NodeResourceLink)
