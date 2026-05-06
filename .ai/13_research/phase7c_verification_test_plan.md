# Phase 7C Verification Test Plan

**Date:** 2026-05-06
**Status:** PLANNED_ONLY

## Boundary

This is a future test plan. Phase 7C did not implement routes or UI behavior, verify sources, create Resources, create nodeResourceLinks, promote candidates, or expose candidates to learners.

## Standards-Context Tests

Future tests must prove:

- standards context rejects placeholder edition/version/scope/sourceOfContext values
- ASCE 7 cannot complete without real edition/version/scope/source context
- "latest", "current", "governing", "compliant", and unsupported AHJ wording are blocked
- reviewer, rationale, sourceOfContext, and reviewedAt are required
- delegated AI reviewer identity is recorded honestly and not as biological-human review
- `standards_context_complete` does not create a Resource or nodeResourceLink
- incomplete standards candidates remain reviewer-only and learner-hidden

## Source-Custody Tests

Future tests must prove:

- source custody cannot complete without reviewer, rationale, and sourceOfContext
- rightsStatus and accessType are required for custody completion
- URL syntax does not count as verification
- HTTP success, if separately authorized later, does not count as source truth by itself
- no external fetch occurs unless explicitly authorized
- protected content is never copied into candidate or Resource records
- source-custody decisions do not create Resources or nodeResourceLinks
- candidates remain reviewer-only and learner-hidden

## API Tests

Future tests must prove:

- preview routes require local/dev/admin gate
- decision routes require local/dev/admin gate
- preview routes are no-write
- decision routes rerun preview server-side
- transaction manifests are written for decision apply
- rollback preview/apply preserves audit history
- apply is rejected when preview has blockers
- invalid candidate ids are blocked
- no graph/canonical registry mutation occurs
- dirty worktree quarantine remains unstaged

## UI Tests

Future tests must prove:

- ResourceReviewAdmin shows Standards Context Review panel for standard-like candidates
- ResourceReviewAdmin shows Source Custody and Rights Review panels for source candidates
- Missing Fields panel lists blockers
- Preview-before-apply diff shows status/context mutations and files touched
- Apply is disabled until preview passes
- unsafe trust wording is absent from incomplete/unverified candidates
- Decision History shows reviewer identity, rationale, sourceOfContext, reviewedAt, and manifest id
- learner node resource views hide external metadata candidates

## Regression Tests To Keep Running

- `bun test api/resourceLayerExternalCandidates.test.ts`
- `bun test api/resourceLayerExternalCandidateReview.test.ts`
- `bun test api/resourceLayerExternalCandidatePromotionPreview.test.ts`
- `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`
- `bun test api/resourceEvidencePath.test.ts`
- `bun test api/resourceLayer.test.ts`
- `bun test api/resourceLayerStandardsContext.test.ts`
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

## Completion Gate

A future implementation is not complete unless resources remain 7, nodeResourceLinks remain 9 unless a separate promotion prompt authorizes otherwise, external candidates remain reviewer-only until explicitly promoted, no external verification occurs without authorization, and the learner endpoints expose no candidates.
