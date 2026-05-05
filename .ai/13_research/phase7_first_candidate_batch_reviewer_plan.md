# Phase 7 First Candidate Batch Reviewer Plan

**Date:** 2026-05-06
**Status:** PHASE7A_FIRST_BATCH_INTAKE_COMPLETE
**Reviewer verdict:** `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`

This plan now records the completed first bounded Phase 7A reviewer-only candidate intake batch. It created external metadata candidates only; it did not create Resources, nodeResourceLinks, source verification records, promotions, or learner exposure.

## Batch Boundary

- Batch mode: reviewer-only candidate intake.
- Candidate count target: maximum 5; completed with 2 persisted candidates from repo-local metadata.
- Initial display policy: `reviewer_only`.
- Initial verification status: `unverified` unless the project owner supplies a separate accepted verification record.
- First workflow: preview plus reviewer-only external metadata candidate persistence.
- First promotion mode, if later authorized: `resource_only`.
- Link workflow: blocked until explicit per-node rationale is provided and a separate implementation prompt authorizes it.

## Required Inputs For Each Candidate

- Title.
- Source type.
- Resource type.
- Steward-supplied source identifier, if any.
- Rights status or rights uncertainty.
- Source-of-context note.
- Reviewer identity recorded honestly.
- Rationale for candidate intake.
- Target node family only if known; exact node links require later per-node rationale.

## Reviewer Identity Rule

Delegated AI review may be recorded as one of:

- `project_owner_delegated_ai_reviewer`
- `external_ai_reviewer`
- `kimi_reviewer`

Do not record delegated AI review as `humanReviewed=true`, `humanReviewer`, or equivalent biological-human approval. If a schema cannot represent delegated AI review, keep the safest status such as `needs_human_review` and add the note:

Reviewed by project-owner-delegated external AI reviewer; not a biological human review; not source truth; not approval unless separately recorded by the project owner.

## Completed First Batch

| Candidate ID | Family | Status |
|---|---|---|
| `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` | Structural standards metadata | persisted reviewer-only, unverified, learner-hidden |
| `ext-cand-earth-retaining-structures-mosyi54y-jp9m` | Civil/geotechnical guidance metadata | persisted reviewer-only, unverified, learner-hidden |

Deferred:

| Candidate Source | Reason |
|---|---|
| AISC source-family reference | insufficient repo-local stable candidate metadata for reviewer-only persistence |

## Candidate Families For Next Planning Batch

| Priority | Family | Planning-only goal | Blocked actions |
|---:|---|---|---|
| 1 | Architecture | identify real steward-supplied general or professional source metadata | no source lookup, no learner exposure |
| 2 | Structural Engineering | identify non-P0 structural reference metadata | no Concrete/Reinforced Concrete work |
| 3 | Civil Engineering | identify real civil/site/infrastructure source metadata | no AHJ or jurisdiction claim unless supplied |
| 4 | MEPFS | identify real system reference metadata | no rights guess, no auto-link |
| 5 | Standards-linked concepts | collect exact edition/version/scope only if supplied | no ASCE 7 or ACI 318 trust change without real context |

## Validation Required Before Any Later Apply

- Resource validator no-write pass.
- Graph relationship validator no-write pass.
- Canonical graph stewardship validator no-write pass.
- Focused Resource/Evidence tests for candidate preview and custody queue.
- Dirty worktree scope check proving no quarantined entries are staged.
- Transaction manifest and rollback plan for any future write-capable operation.

## Current Entry Decision

The first reviewer-only candidate intake batch is complete. Next implementation remains limited to review/correction decisions for the two persisted candidates unless a separate project-owner prompt authorizes promotion, source verification, Resource creation, nodeResourceLink creation, or a second candidate intake batch.
