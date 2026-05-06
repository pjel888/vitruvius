# Phase 7D Source Verification Preview API Report

**Date:** 2026-05-06
**Status:** IMPLEMENTED

## Routes

- `POST /resources/review/external-candidates/:candidateId/source-verification-preview`
- `POST /resources/review/external-candidates/:candidateId/standards-context-verification-preview`

## Behavior

- Require `requireLocalDevAdmin`.
- Load an existing external metadata candidate only.
- Run bounded official-source metadata checks.
- Return no-write previews with preview hash, source-check result, warnings, blockers, caveats, proposed status, and no-mutation assertions.
- Write no files.
- Create no Resource.
- Create no nodeResourceLink.
- Promote no candidate.
- Expose nothing to learners.

## Test Coverage

`api/resourceLayerSourceVerification.test.ts` verifies:

- preview routes are gated,
- previews write no registry files,
- official-domain restrictions are enforced,
- placeholder/fake URL checks block before fetch,
- HTTP success creates no Resource or nodeResourceLink,
- ASCE 7 cannot complete with missing standards context,
- placeholder standards context values are rejected.
