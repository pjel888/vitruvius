# Phase 7D Source Check Helper Report

**Date:** 2026-05-06
**Status:** IMPLEMENTED

## Files

- Added `api/resourceLayer/sourceVerification.ts`.
- Updated candidate status vocabulary in `api/resourceLayer/externalCandidateRegistry.ts`.
- Updated source-custody next-action wording in `api/resourceLayer/sourceCustodyQueue.ts`.

## Helper Scope

Implemented bounded helpers:

- `checkUrlMetadata`
- `checkOfficialSourceCandidate`
- `buildSourceVerificationPreview`
- `buildStandardsContextVerificationPreview`
- `classifySourceVerificationOutcome`
- `classifyStandardsContextOutcome`
- `applySourceVerificationDecision`
- `applyStandardsContextVerificationDecision`

## Enforced Rules

- HTTPS-only source checks.
- Official ASCE/ASCE Library or FHWA/highways domains only for the current candidates.
- HEAD first, GET only for public text/HTML metadata when needed.
- Redirect limit: 5.
- Timeout default: 10 seconds.
- Body read cap: 1 MB.
- No PDF/protected payload extraction.
- No full source payload storage.
- No DOI/ISBN/API lookups.
- No Resource or nodeResourceLink creation.
- No graph/canonical mutation.
- Preview routes are no-write.
- Decision routes append candidate history and touch only the external-candidate registry through transaction manifests.

## Caveats

HTTP success is recorded only as bounded URL metadata evidence. It does not establish source truth, content correctness, governing/current status, AHJ applicability, code compliance, learner trust, DOI existence, ISBN existence, or promotion readiness.
