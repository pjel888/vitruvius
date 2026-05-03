# Phase 6K Promotion Preview Contract

**Date:** 2026-05-03
**Status:** Defined

---

## Purpose

Promotion preview is a **read-only analysis** of whether an external metadata candidate could become a Resource and/or NodeResourceLink in a future phase. It creates nothing.

## Request

```http
POST /resources/review/external-candidates/:candidateId/promotion-preview
```

Gate: `requireLocalDevAdmin`

## Response Shape

```ts
interface PromotionPreviewResult {
  candidateId: string;
  candidateStatus: ExternalCandidateReviewStatus;
  eligibleForPromotionPreview: boolean;
  proposedResourceDraft: ProposedResourceDraft | null;
  proposedNodeResourceLinkDrafts: ProposedNodeResourceLinkDraft[];
  promotionReadinessChecklist: PromotionReadinessChecklist;
  blockers: string[];
  warnings: string[];
  missingFields: string[];
  sourceTruthCaveat: string;
  standardsContextCaveat: string;
  rightsCaveat: string;
  verificationCaveat: string;
  noApplyAvailable: true;
  createsResource: false;
  createsNodeResourceLink: false;
  learnerVisibleAfterPreview: false;
  externalVerificationPerformed: false;
  transactionRequiredForFutureApply: true;
  rollbackRequiredForFutureApply: true;
}
```

## Proposed Resource Draft

- `resourceId`: proposed only, prefixed `res-`
- `title`, `resourceType`, `sourceType`: from candidate
- `url`, `doi`, `isbn`: from candidate, unverified
- `verificationStatus`: `'unverified'`
- `displayPolicy`: `'reviewer_only'` or `'dev_only'`
- `learnerVisible`: `false`
- `status`: `'draft_preview'`
- `previewOnly`: `true`
- `noApplyAvailable`: `true`

## Proposed Node-Link Draft

- `linkId`: proposed only
- `nodeId`, `resourceId`, `relationship`: from candidate
- `reviewStatus`: `'preview_only'`
- `learnerVisible`: `false`
- `previewOnly`: `true`

## Eligibility Rules

Blocked if:
- Status is not `ready_for_promotion_review`
- Status is `rejected`, `deferred`, `duplicate_candidate`, or `promotion_blocked`
- `fakePlaceholderFlags` non-empty
- Any promotion readiness gate fails
- Standards context incomplete (for standard/guide candidates)
- `learnerVisible !== false`
- `verificationStatus !== 'unverified'`
- `proposedRelation` invalid when `proposedNodeIds` present

## Safety Guarantees

- No file writes
- No registry mutation
- No resource creation
- No nodeResourceLink creation
- No review decision creation
- No transaction manifest creation
- No external verification
- No graph/canonical mutation
- No learner exposure
