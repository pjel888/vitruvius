# Phase 6F — API Evidence-Path Tests Report

Date: 2026-05-03

## New Test File

`api/resourceEvidencePath.test.ts` — 21 tests covering end-to-end evidence-path safety.

## Test Suites

### evidence-path learner safety (8 tests)

1. `GET /node/:id/resources returns only accepted/human_reviewed links in learner mode`
2. `learner mode never returns rejected, needs_review, candidate, or rights-blocked resources`
3. `learner mode returns empty safe state for node with no accepted resources`
4. `ASCE 7 is not learner-visible via endpoint because standards context is incomplete`
5. `ACI 318 rejected link is not learner-visible via endpoint`
6. `learner mode hard-caps at 8 resources`
7. `reviewer mode returns non-eligible resources with warning text and learnerEligible=false`
8. `node detail endpoint includes learner-safe resources with cap 8`

### evidence-path source-custody queue (7 tests)

1. `GET /resources/review/source-custody returns all 9 groups`
2. `source-custody queue includes needs_review links`
3. `source-custody queue includes nextReviewAction and missingStandardContextFields`
4. `source-custody queue includes rejected/blocked items`
5. `source-custody queue includes local files as indexed-only`
6. `source-custody queue includes candidates`
7. `source-custody queue marks accepted links as learner-visible`

### evidence-path no-mutation safety (4 tests)

1. `GET /node/:id/resources does not mutate Resource Layer registries`
2. `GET /resources/review/source-custody does not mutate Resource Layer registries`
3. `source-custody queue build is read-only and stable across repeated calls`
4. `Resource Layer counts remain 7 resources / 9 links after route calls`

### evidence-path fixture and validation safety (2 tests)

1. `no production placeholder metadata is learner-eligible`
2. `ASCE 7 and ACI 318 remain not learner-trusted in production`

## Existing Supporting Tests

- `api/resourceLayer.test.ts` — 38 tests (ranking, registry, validation, review workflow, source-custody basics)
- `api/resourceLayerStandardsContext.test.ts` — 17 tests (standards-context validation, placeholder rejection, ASCE/ACI production state)

## Results

All 21 new tests pass. Full API suite: 256 pass, 0 fail.
