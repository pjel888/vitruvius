# Phase 7D Tests Report

**Date:** 2026-05-06

## New Focused Test

| Command | Result |
|---|---|
| `bun test api/resourceLayerSourceVerification.test.ts` | PASS, 21 pass |

Coverage includes:

- admin gate checks,
- no-write previews,
- official-domain restrictions,
- placeholder/fake URL blocking,
- no protected payload storage,
- HTTP success not treated as source truth,
- no Resource creation,
- no nodeResourceLink creation,
- ASCE missing-context blockers,
- standards placeholder blockers,
- source-custody verified rights/access blockers,
- decision history-only applies,
- transaction manifest creation,
- learner endpoint hiding external candidates,
- source-custody queue status reflection.

## Existing Focused Tests

The external-candidate registry test files must be run sequentially if invoked as separate Bun processes because they share a fixture registry path.

| Command | Result |
|---|---|
| `bun test api/resourceLayerExternalCandidates.test.ts` | PASS, 46 pass when rerun sequentially |
| `bun test api/resourceLayerExternalCandidateReview.test.ts` | PASS, 26 pass when rerun sequentially |

## Fixture Hygiene Note

A manual parallel invocation of two registry-mutating test files caused temporary registry fixture interference. The production registry was restored to the intended Phase 7D state with two candidates and two Phase 7D decision entries before validation continued. This is recorded as a test invocation issue, not a production workflow outcome.
