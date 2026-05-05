# Phase 7 First Candidate Batch Reviewer Plan

**Date:** 2026-05-06
**Status:** PLANNING_ONLY_AFTER_DELEGATED_AI_REVIEW
**Reviewer verdict:** `PASS_PLANNING_ONLY`

This plan refines the first-batch queue after Kimi's delegated AI review. It does not create candidates, Resources, nodeResourceLinks, source verification records, or learner exposure.

## Batch Boundary

- Batch mode: reviewer-only intake planning.
- Candidate count target: 3 to 8 steward-supplied real metadata records.
- Initial display policy: `reviewer_only`.
- Initial verification status: `unverified` unless the project owner supplies a separate accepted verification record.
- First workflow: preview only.
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

## Candidate Families For First Planning Batch

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

Planning is allowed. Implementation is not allowed by this task.
