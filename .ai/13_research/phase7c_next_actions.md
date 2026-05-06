# Phase 7C Next Actions

**Date:** 2026-05-06
**Status:** PLANNING_COMPLETE_VALIDATION_PASS

## Phase 7C Result

Phase 7C defines the future standards-context and source-custody verification workflows needed to move the two Phase 7A/7B candidates forward safely. It is planning only.

## Current Candidate Blockers

| Candidate | Current Status | Required Next Evidence |
|---|---|---|
| ASCE 7 | `standards_context_needed` | Real edition/version/scope/source context plus applicability caveat supplied by the steward or a separately authorized verification workflow |
| Earth Retaining Structures | `source_custody_review_needed` | Source custody, rights/access posture, and sourceOfContext reviewed through a separately authorized workflow |

## Allowed Next Implementation

A next implementation prompt may authorize only one bounded workflow at a time:

1. Implement standards-context preview/decision routes and tests.
2. Implement source-custody preview/decision routes and tests.
3. Implement ResourceReviewAdmin panels for the above workflows.
4. Continue reviewer-only candidate intake with repo-local or steward-supplied metadata.

## Still Blocked

- External URL/DOI/ISBN/book/PDF/standards verification unless separately authorized.
- Candidate promotion.
- Resource creation.
- nodeResourceLink creation.
- Learner exposure.
- Graph/canonical mutation.
- P0 Concrete/Reinforced Concrete work.
- High-risk P1 packet work.
- Staging quarantined dirty worktree files.

## Exact Next Action

If the project owner wants to move the current candidates forward, the safest next prompt is: authorize implementation of standards-context and source-custody review preview/decision workflows only, still with no external fetch, no promotion, no Resource creation, no nodeResourceLink creation, and no learner exposure.
