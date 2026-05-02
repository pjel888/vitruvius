# Steward Approval Gate Report

Date: 2026-05-02

## Summary

Implemented a steward approval/admission gate for moving canonical stewardship decisions from proposed review metadata toward approved/admitted state. The gate is intentionally stricter than ordinary proposed decision recording and is required before any P0 non-destructive edge admission.

## Data model

Approval records include:
- approvalId
- decisionId
- groupId
- decisionHash
- approvedBy
- reviewerRole
- approvalSource
- approvedAt
- approvalRationale
- riskAcknowledgment
- mutationScope
- rollbackPlan
- validationSnapshot
- KimiReviewSummary
- transactionManifestId
- status
- admittedBy/admittedAt/admissionTransactionId when relationships are admitted

Statuses supported:
- proposed
- pending_steward_approval
- steward_approved
- admitted
- rejected
- deferred
- rolled_back

Mutation scopes supported:
- metadata_only
- non_destructive_edge_admission
- alias_only
- redirect
- tombstone
- destructive_merge

## API/UI

Added or updated:
- `GET /graph/canonical/approvals`
- `GET /graph/canonical/approvals/:approvalId`
- `POST /graph/canonical/decisions/:decisionId/approval-preview`
- `POST /graph/canonical/decisions/:decisionId/approve`
- `POST /graph/canonical/decisions/:decisionId/reject-approval`
- `/dev/canonical-review` approval/admission panel

## Safety rules

- No admission without approval metadata.
- High-risk approval requires explicit risk acknowledgment.
- `test_fixture` approvals are blocked for production `VTN-DOM-*` nodes and outside test mode.
- `destructive_merge` is blocked in this admission path.
- Disambiguation/admission decision types cannot be directly applied; they must be proposed then approved/admitted.
- Kimi review is advisory only and cannot substitute for steward approval.
- Approval writes use hash-chained transaction manifests.

## Limitation

The repo still does not have a full production identity/authentication system. The API relies on the existing local/dev/admin mutation gate and supplied reviewer fields. Server-derived reviewer identity, two-person approval, and signed imported human records remain deferred.
