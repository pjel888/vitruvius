# Phase 7 Candidate Review Wave 1 Apply Report

Date: 2026-05-06

## Scope

Apply Kimi-supported review decisions for the three Phase 7 source-family reference candidates.

No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical/P0/high-risk P1 mutation, external source verification, URL fetch, DOI lookup, ISBN lookup, protected content access, or source-truth claim occurred.

## Apply Method

Codex used the existing review-decision API routes:

- `POST /resources/review/external-candidates/:candidateId/review-preview`
- `POST /resources/review/external-candidates/:candidateId/review-decision`

Every preview returned no blockers and safety flags:

- `noAutoPromotion: true`
- `noAutoLinking: true`
- `noLearnerExposure: true`

## Decisions Applied

| Candidate ID | Prior status | Decision type | Next status | Manifest |
|---|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | `candidate` | `mark_needs_review` | `needs_review` | `resource-layer-tx-20260506060423-1fa9b68bd0ac` |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | `candidate` | `mark_needs_review` | `needs_review` | `resource-layer-tx-20260506060423-d4fb27616b65` |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | `candidate` | `mark_needs_review` | `needs_review` | `resource-layer-tx-20260506060423-52a3ed2c86bd` |

## Registry Counts

| Registry | Before | After |
|---|---:|---:|
| Resources | 7 | 7 |
| nodeResourceLinks | 9 | 9 |
| External metadata candidates | 5 | 5 |
| Learner-visible external metadata candidates | 0 | 0 |

## Next Safe Action

Run validators and focused Resource/Evidence tests, then commit/push the scoped candidate review wave files. Future work can review source custody or metadata correction for these three candidates, but must not promote, create Resources, create nodeResourceLinks, or expose learners without a separate gated workflow.
