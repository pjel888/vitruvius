# Phase 7D Source Custody Visibility Check

**Date:** 2026-05-06

## Registry State After Decisions

| Candidate | Status | Verification | Display | Learner visible |
|---|---|---|---|---:|
| ASCE 7 | `standards_context_in_review` | `unverified` | `reviewer_only` | false |
| Earth Retaining Structures | `source_custody_in_review` | `unverified` | `reviewer_only` | false |

## Visibility Assertions

- External metadata candidates remain in reviewer/source-custody workflow only.
- Learner node resource endpoint does not expose external candidates.
- No Resource was created.
- No nodeResourceLink was created.
- No candidate was promoted.
- ASCE 7 remains blocked from standards-context completion and promotion until real edition/version/scope/applicability context exists.
- Earth Retaining Structures remains blocked from source-custody verification/promotion until rights/access/source custody review is complete.

## Notes

`api/resourceLayerSourceVerification.test.ts` includes learner-hidden and source-custody queue assertions for the new statuses.
