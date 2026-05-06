# Phase 7C Verification UI Plan

**Date:** 2026-05-06
**Surface:** ResourceReviewAdmin
**Status:** PLANNED_ONLY

## Boundary

This file plans future UI additions only. Phase 7C did not implement UI code, verify sources, promote candidates, create Resources, create nodeResourceLinks, or expose candidates to learners.

## Panels

### Standards Context Review

Purpose: let reviewers inspect and preview required standards-context fields for standard-like candidates.

Required controls:

- standard title field
- edition field
- version/year field
- scope field
- jurisdiction/applicability caveat field
- sourceOfContext field
- reviewer identity selector/input
- rationale field
- preview button
- apply decision button disabled until preview passes

### Source Custody Review

Purpose: let reviewers inspect source identity, source family, and custody status for URL/source candidates.

Required controls:

- title display
- source locator display
- source family field
- sourceOfContext field
- reviewer identity selector/input
- rationale field
- stage selector
- preview button
- apply decision button disabled until preview passes

### Rights Review

Purpose: record rights/access posture without copying protected content.

Required controls:

- rightsStatus field
- accessType field
- protected-content warning
- reviewer rationale field
- sourceOfContext field

### Verification Caveat

Purpose: make the safety state visible to reviewers.

Required content:

- candidate metadata only
- not externally verified unless a separately authorized verification record exists
- not learner-visible
- not a compliance claim
- not governing/current unless explicitly reviewed
- delegated AI review is not biological-human review

### Missing Fields

Purpose: show blockers before apply.

Required behavior:

- list missing required fields
- list placeholder/fake values
- list unsafe wording
- show why candidate remains reviewer-only

### Preview-Before-Apply Diff

Purpose: make the exact decision mutation reviewable before apply.

Required behavior:

- display current status and proposed status
- display status/context field diff
- display files that would be touched
- display transaction manifest and rollback summary
- block apply when preview has blockers

### Decision History

Purpose: preserve audit continuity.

Required behavior:

- list decision type, reviewer, reviewedAt, rationale summary, sourceOfContext, and manifest id
- show delegated AI review caveat where applicable
- show rollback decisions without deleting original decisions

## Safe Wording

Allowed UI wording:

- reviewer-only
- candidate metadata
- source custody review
- standards context needed
- not learner-visible
- not verified
- not a compliance claim
- not governing/current unless explicitly reviewed

## Unsafe Wording

Blocked UI wording unless explicitly represented as rejected/unsafe language:

- verified source
- official
- current standard
- governing standard
- compliant
- AHJ accepted
- accepted resource
- learner approved

## Visibility Rules

- Candidate panels are reviewer/admin surfaces only.
- Learner surfaces must not show external metadata candidates.
- ResourceReviewAdmin may show warnings and blocked states; learner node resources must remain accepted-link-only.
- No UI action may bypass server-side preview/apply gates.

## Future Acceptance Criteria

A future UI implementation is acceptable only if tests prove preview blockers are visible, apply remains disabled until preview passes, unsafe wording is absent from candidate trust states, decision history is preserved, and learner endpoints remain candidate-hidden.
