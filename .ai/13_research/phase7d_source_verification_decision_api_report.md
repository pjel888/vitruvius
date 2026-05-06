# Phase 7D Source Verification Decision API Report

**Date:** 2026-05-06
**Status:** IMPLEMENTED

## Routes

- `POST /resources/review/external-candidates/:candidateId/source-verification-decision`
- `POST /resources/review/external-candidates/:candidateId/standards-context-verification-decision`

## Behavior

- Require `requireLocalDevAdmin`.
- Require reviewer, rationale, and sourceOfContext.
- Server-rerun preview before apply; optional preview hash mismatch blocks apply.
- Write transaction manifest through `withResourceLayerTransaction`.
- Update candidate status/history only.
- Keep `verificationStatus: unverified`.
- Keep `displayPolicy: reviewer_only` or `dev_only`.
- Keep `learnerVisible: false`.
- Create no Resource.
- Create no nodeResourceLink.
- Perform no promotion.
- Mutate no graph/canonical registry.

## Added Statuses

- `standards_context_in_review`
- `standards_context_complete`
- `standards_context_rejected`
- `source_custody_in_review`
- `source_custody_verified`
- `source_custody_rejected`

Completion statuses are gated. In Phase 7D, only conservative in-review statuses were applied.
