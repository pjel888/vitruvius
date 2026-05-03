# Phase 6H External Candidate Promotion Gate Design

**Date:** 2026-05-03
**Status:** Planning — Promotion NOT Implemented

## Purpose
Define the gates that must pass before a candidate can even enter a **future** promotion workflow. Promotion readiness ≠ promotion.

---

## Gate A: Identity Gate

| Check | Rule |
|---|---|
| `candidateId` exists | Must be a valid persisted candidate |
| Status allows promotion review | Must be `candidate`, `needs_review`, or `metadata_correction_needed` |
| Not rejected/deferred/duplicate | `rejected`, `deferred`, `duplicate_candidate` block promotion review |
| No placeholder metadata | `fakePlaceholderFlags` must be empty |
| Title present | `title` must be non-empty |
| `resourceType` valid | Must be in `ExternalCandidateResourceType` union |
| `sourceType` valid | If present, must be a known source type |

## Gate B: Source Metadata Gate

| Check | Rule |
|---|---|
| URL syntax valid | If `proposedUrl` present, must pass `canonicalizeUrl` |
| DOI syntax valid | If `proposedDoi` present, must pass `normalizeDoi` |
| ISBN syntax valid | If `proposedIsbn` present, must pass `normalizeIsbn` |
| No fake metadata | `fakePlaceholderFlags` empty |
| Required metadata for type present | Books need author or publisher; standards need edition or version |
| Publication/date not invented | `proposedPublicationDate` must not be future-dated beyond reasonable bounds |
| Source family context complete | If `proposedSourceFamilyId` present, must exist in source-families registry |

## Gate C: Rights Gate

| Check | Rule |
|---|---|
| `rightsStatus` exists | Must be explicitly set, not undefined |
| Protected content hidden | If `protected_content`, must have `displayPolicy='reviewer_only'` or `'dev_only'` |
| Licensed/internal restricted | If `licensed` or `internal_use_only`, must have display restrictions |
| Reviewer rationale exists | `rightsStatusAssessment.reviewerRationale` required |

## Gate D: Verification Gate

| Check | Rule |
|---|---|
| `verificationStatus` remains `unverified` | No automatic verification from syntax checks |
| Future promotion requires explicit reviewer verification | A separate `verification_review` decision type (future phase) |
| Syntax validation is NOT verification | `validateExternalMetadataCandidate` ok=true does not imply verified |

## Gate E: Standards Gate

| Check | Rule |
|---|---|
| Standards candidates require context | `standard_candidate` or `guide_candidate` must have edition/version or justified missing |
| Placeholder context rejected | `isPlaceholderStandardContextValue` must return false for all context fields |
| No current/governing/compliance/AHJ claim | Unless real context exists and is cited |
| ASCE 7 / ACI 318 remain blocked | Existing incomplete standards stay blocked; do not invent context |

## Gate F: Node Link Gate

| Check | Rule |
|---|---|
| `proposedNodeIds` exist | If present, all node IDs must exist in graph |
| `proposedRelation` valid | If present, must be in `NODE_RESOURCE_RELATIONSHIPS` |
| Node-specific relevance rationale | `candidateRationale` must explain relevance to proposed nodes |
| No nodeResourceLink created | Gate check does NOT create links |
| No graph edge implication | Candidate metadata does not imply graph topology changes |

## Gate G: Display Gate

| Check | Rule |
|---|---|
| `learnerVisible` remains `false` | Until accepted resource/link workflow |
| `displayPolicy` remains `reviewer_only` or `dev_only` | No learner exposure |
| Warnings preserved | `warningFlags` must not be silently cleared |

## Gate H: Transaction Gate

| Check | Rule |
|---|---|
| Future promotion must write transaction manifest | Any promotion apply (future) uses `withResourceLayerTransaction` |
| Rollback plan required | Manifest must include `rollbackPlan` |
| Before/after hashes required | `beforeHash` and `afterHash` on affected files |
| No direct file mutation | All writes go through transaction wrapper |

## Promotion Readiness Scoring

All gates must pass (`true`) for `ready_for_promotion_review` status.

```
readinessScore = sum(gate_passes) / total_gates * 100
ready_for_promotion_review requires readinessScore === 100
```

## Explicit Blockers

These conditions permanently block promotion review until resolved:

1. `fakePlaceholderFlags.length > 0`
2. `status === 'rejected'`
3. `status === 'duplicate_candidate'`
4. `status === 'deferred'`
5. `rightsStatusAssessment.protectedContent === true` without clear display restriction
6. Standard candidate with placeholder edition/version/scope and no structured justification
