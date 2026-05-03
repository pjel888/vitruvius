# Phase 6H External Candidate Review States

**Date:** 2026-05-03
**Status:** Planning

## State Machine

```
candidate ──► needs_review ──► metadata_correction_needed ──► candidate
     │              │                    │
     ▼              ▼                    ▼
 rejected    rights_review_needed  standards_context_needed
     │              │                    │
     ▼              ▼                    ▼
 deferred    source_custody_review_needed  duplicate_candidate
     │              │                    │
     └──────────────┴────────────────────┘
                      │
                      ▼
            ready_for_promotion_review
                      │
                      ▼
            promotion_blocked
```

## State Definitions

| State | Meaning | Who Can Set | Required Data |
|---|---|---|---|
| `candidate` | Default state after persistence. Awaiting reviewer attention. | System | None |
| `needs_review` | Reviewer has flagged for attention. Not yet categorized. | Reviewer | `rationale` |
| `metadata_correction_needed` | Title, URL, DOI, ISBN, or basic metadata is wrong or missing. | Reviewer | `rationale`, `correctionPatch` |
| `source_custody_review_needed` | Source provenance, custody chain, or file location needs review. | Reviewer | `rationale` |
| `rights_review_needed` | Rights status unclear or needs reassessment. | Reviewer | `rationale`, `rightsStatusAssessment` |
| `standards_context_needed` | Edition, version, jurisdiction, scope, or citation context missing. | Reviewer | `rationale`, `standardsContextAssessment` |
| `duplicate_candidate` | Same source already exists as another candidate or resource. | System/Reviewer | `duplicateOfCandidateId` or `duplicateOfResourceId` |
| `rejected` | Candidate will not be promoted. History preserved. | Reviewer | `rationale`, `rejectionReasons` |
| `deferred` | Review postponed. Candidate remains in registry. | Reviewer | `rationale`, `deferUntil` (optional) |
| `ready_for_promotion_review` | All readiness gates pass. Awaiting explicit promotion authorization. | Reviewer | `promotionReadinessChecklist` |
| `promotion_blocked` | One or more readiness gates failed. Cannot enter promotion review. | System/Reviewer | `blockers` |

## State Transition Rules

1. **No auto-promotion:** `ready_for_promotion_review` does NOT create resources or links.
2. **No deletion:** `rejected` and `duplicate_candidate` preserve the record.
3. **No learner visibility:** No state may set `learnerVisible=true`.
4. **No verification without workflow:** `verificationStatus` remains `unverified`.
5. **Reversible:** `metadata_correction_needed` → `candidate` → `ready_for_promotion_review` is valid.
6. **Blocked is terminal for promotion:** `promotion_blocked` cannot reach `ready_for_promotion_review` without status change.

## Constraints Carried from Phase 6G

- `noAutoVerification: true`
- `noAutoPromotion: true`
- `noAutoLinking: true`
- `noLearnerExposure: true`
