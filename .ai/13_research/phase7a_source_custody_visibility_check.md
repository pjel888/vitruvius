# Phase 7A Source Custody Visibility Check

**Date:** 2026-05-06
**Verdict:** PASS_REVIEWER_ONLY_VISIBLE_LEARNER_HIDDEN

## Commands

- `bun -e` API route check for:
  - `GET /resources/review/external-candidates`
  - `GET /resources/review/source-custody`
  - `GET /node/VTN-DOM-0012777/resources?limit=20`
  - `GET /node/VTN-DOM-0012799/resources?limit=20`

## Results

| Check | Result |
|---|---|
| External candidate reviewer route status | 200 |
| External candidate reviewer route count | 2 |
| Source custody route status | 200 |
| Source custody `externalCandidates` count | 2 |
| ASCE wind-load learner node resource count | 1 |
| FHWA retaining-wall learner node resource count | 0 |
| External candidate leak count in learner responses | 0 |
| Candidate-title leak count in learner responses | 0 |

## Candidate Visibility

Both candidates appear in reviewer-only external candidate and source-custody views:

- `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu`
- `ext-cand-earth-retaining-structures-mosyi54y-jp9m`

Both candidates remain:

- `verificationStatus: unverified`
- `displayPolicy: reviewer_only`
- `learnerVisible: false`
- `reviewRequired: true`
- `noAutoVerification: true`
- `noAutoPromotion: true`
- `noAutoLinking: true`
- `noLearnerExposure: true`

## Registry Safety

- Production resources remain 7.
- Production nodeResourceLinks remain 9.
- No nodeResourceLink was created for either candidate.
- No Resource was created for either candidate.
- No learner-visible node sidebar response includes the new candidate records.
