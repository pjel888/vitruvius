# Phase 7C Verification API Plan

**Date:** 2026-05-06
**Status:** PLANNED_ONLY

## Boundary

This file plans future API routes only. No route was implemented in Phase 7C, no verification occurred, and no Resource Layer registry was mutated.

## Common Route Rules

All planned routes must:

- require `requireLocalDevAdmin`
- accept only existing external metadata candidates
- reject learnerVisible changes
- reject Resource creation, nodeResourceLink creation, promotion, graph/canonical mutation, P0 work, and high-risk P1 work
- require reviewer, rationale, sourceOfContext, and reviewedAt or server-generated reviewedAt
- preserve honest reviewer identity
- write transaction manifests only for decision apply routes
- support rollback of candidate status/history changes without deleting audit history
- leave candidates reviewer-only unless a separate promotion workflow later changes them

## POST /resources/review/external-candidates/:candidateId/source-verification-preview

| Aspect | Plan |
|---|---|
| Gate | `requireLocalDevAdmin` |
| Request | `{ stage, proposedFields, reviewer, rationale, sourceOfContext, reviewedAt?, noExternalFetchConfirmed: true }` |
| Response | `{ ok, candidateId, currentStatus, proposedStatus, warnings, blockers, diff, noWrite: true }` |
| Mutation scope | None |
| Validation | Candidate exists; stage is allowed; required fields present; URL syntax is not verification; external fetch flag must be false/confirmed absent |
| Transaction manifest | None |
| Rollback | Not applicable because preview is no-write |
| Learner exposure | Always false |
| Promotion | Forbidden |

## POST /resources/review/external-candidates/:candidateId/source-verification-decision

| Aspect | Plan |
|---|---|
| Gate | `requireLocalDevAdmin` |
| Request | `{ decisionType, nextStatus, reviewedFields, reviewer, rationale, sourceOfContext, reviewedAt?, previewToken? }` |
| Response | `{ ok, candidateId, priorStatus, nextStatus, decisionId, transactionManifestId, rollbackPlan }` |
| Mutation scope | External metadata candidate status and append-only decision history only |
| Validation | Server reruns preview; no Resource/link/promotion; no learner exposure; no source truth claim from syntax-only URL; rights/source family fields enforced for completion |
| Transaction manifest | Required for apply, listing `external-metadata-candidates.json` only |
| Rollback | Restores prior candidate status while preserving decision/audit history or appending rollback decision |
| Learner exposure | Always false |
| Promotion | Forbidden |

## POST /resources/review/external-candidates/:candidateId/standards-context-preview

| Aspect | Plan |
|---|---|
| Gate | `requireLocalDevAdmin` |
| Request | `{ proposedStandardsContext, reviewer, rationale, sourceOfContext, reviewedAt?, noExternalFetchConfirmed: true }` |
| Response | `{ ok, candidateId, currentStatus, proposedStatus, missingFields, placeholderFindings, warnings, blockers, diff, noWrite: true }` |
| Mutation scope | None |
| Validation | Candidate exists and is standard-like; required fields present for completion; placeholders rejected; jurisdiction/AHJ/current/governing wording blocked without reviewed evidence |
| Transaction manifest | None |
| Rollback | Not applicable because preview is no-write |
| Learner exposure | Always false |
| Promotion | Forbidden |

## POST /resources/review/external-candidates/:candidateId/standards-context-decision

| Aspect | Plan |
|---|---|
| Gate | `requireLocalDevAdmin` |
| Request | `{ decisionType, nextStatus, standardsContext, reviewer, rationale, sourceOfContext, reviewedAt?, previewToken? }` |
| Response | `{ ok, candidateId, priorStatus, nextStatus, decisionId, transactionManifestId, rollbackPlan }` |
| Mutation scope | External metadata candidate status/context fields and append-only decision history only |
| Validation | Server reruns preview; completion requires non-placeholder title, edition, version/year, scope, applicability caveat, sourceOfContext, reviewer, rationale; no compliance/governing/AHJ claim unless reviewed |
| Transaction manifest | Required for apply, listing `external-metadata-candidates.json` only |
| Rollback | Restores prior candidate status/context while preserving decision/audit history or appending rollback decision |
| Learner exposure | Always false |
| Promotion | Forbidden |

## Transaction Manifest Requirements

Apply manifests must record:

- route name and candidate id
- prior status and next status
- decision id
- reviewer identity and AI/human caveat where applicable
- files touched
- no-resource/no-link/no-promotion/no-learner-exposure assertions
- rollback plan

## Future Implementation Sequence

1. Add preview validators with tests before apply routes.
2. Add apply routes using the existing external candidate review-decision transaction pattern.
3. Add rollback preview/apply for status/context decision reversals.
4. Confirm learner endpoints remain no-write and candidate-hidden.
5. Run full Resource/Evidence, API, Explorer, graph, canonical, and Python KG validations before commit.
