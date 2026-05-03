# Phase 6L Promotion Apply API Plan

**Date:** 2026-05-03
**Status:** Planning — Routes Designed, NOT Implemented

---

## Route Summary

| Method | Route | Gate | Mutation | Phase |
|---|---|---|---|---|
| POST | `/resources/review/external-candidates/:candidateId/promotion-preview` | `requireLocalDevAdmin` | No | 6K ✅ |
| POST | `/resources/review/external-candidates/:candidateId/promotion-apply-preview` | `requireLocalDevAdmin` | No | Future |
| POST | `/resources/review/external-candidates/:candidateId/promotion-apply` | `requireLocalDevAdmin` | Yes | Future |
| POST | `/resources/review/external-candidates/:candidateId/promotion-rollback-preview` | `requireLocalDevAdmin` | No | Future |
| POST | `/resources/review/external-candidates/:candidateId/promotion-rollback` | `requireLocalDevAdmin` | Yes | Future |

---

## POST /resources/review/external-candidates/:candidateId/promotion-apply-preview

**Purpose:** Read-only preview of what promotion apply would do. May be identical to or extend current promotion-preview.

**Request:**
```json
{
  "applyMode": "resource_only" | "resource_and_links",
  "reviewer": "string",
  "rationale": "string",
  "sourceOfContext": "string"
}
```

**Response:**
```json
{
  "candidateId": "string",
  "eligibleForPromotionApply": true,
  "applyMode": "resource_only",
  "proposedResource": { ...Resource preview... },
  "proposedLinks": [ ...NodeResourceLink preview... ],
  "gates": { "passed": 9, "total": 9 },
  "blockers": [],
  "warnings": [],
  "transactionPreview": {
    "filesTouched": ["resources.json", "node-resource-links.json", "external-metadata-candidates.json"],
    "rollbackCapability": "full"
  },
  "createsResource": false,
  "createsNodeResourceLink": false,
  "noApplyAvailable": true
}
```

**Validation:**
- Candidate must exist
- Candidate must be `ready_for_promotion_review`
- All apply gates must pass
- Request must include reviewer/rationale/sourceOfContext

---

## POST /resources/review/external-candidates/:candidateId/promotion-apply

**Purpose:** Create Resource and optionally nodeResourceLinks from candidate.

**Request:**
```json
{
  "applyMode": "resource_only" | "resource_and_links",
  "reviewer": "string",
  "rationale": "string",
  "sourceOfContext": "string",
  "previewHash": "string"  // Must match current candidate previewHash
}
```

**Response:**
```json
{
  "ok": true,
  "candidateId": "string",
  "resourceId": "string",
  "linkIds": ["string"],
  "decision": { ...ExternalCandidateReviewDecision... },
  "manifest": { "transactionId": "string" }
}
```

**Mutations:**
- `resources.json` — append new Resource
- `node-resource-links.json` — append new links (if mode 2)
- `external-metadata-candidates.json` — update candidate status, append decision
- `transaction-manifests/` — write transaction manifest

**Rejection conditions:**
- Candidate not found → 404
- Candidate not `ready_for_promotion_review` → 400
- Any gate fails → 400 with blockers
- Missing reviewer/rationale/sourceOfContext → 400
- previewHash mismatch → 409 (candidate changed since preview)
- Duplicate resource ID → 409
- Duplicate link (nodeId + resourceId + relationship) → 409

**Transaction behavior:**
- Uses `withResourceLayerTransaction()`
- operationType: `external_candidate_resource_promotion` or `external_candidate_resource_and_link_promotion`
- Records beforeHash/afterHash for all touched files
- Records created resourceIds and linkIds
- Records reviewer/rationale/sourceOfContext
- Records rollback plan

---

## POST /resources/review/external-candidates/:candidateId/promotion-rollback-preview

**Purpose:** Read-only preview of rollback impact.

**Request:**
```json
{
  "promotionDecisionId": "string"
}
```

**Response:**
```json
{
  "promotionDecisionId": "string",
  "rollbackable": true,
  "resourcesToRollback": ["string"],
  "linksToRollback": ["string"],
  "filesToRestore": ["string"],
  "impact": "Resource and links would be marked rolled_back or deleted"
}
```

---

## POST /resources/review/external-candidates/:candidateId/promotion-rollback

**Purpose:** Roll back a promotion apply.

**Request:**
```json
{
  "promotionDecisionId": "string",
  "reviewer": "string",
  "rationale": "string",
  "sourceOfContext": "string"
}
```

**Response:**
```json
{
  "ok": true,
  "rollbackDecisionId": "string",
  "resourcesRolledBack": ["string"],
  "linksRolledBack": ["string"],
  "manifest": { "transactionId": "string" }
}
```

**Rollback behavior:**
- If no other links depend on resource → delete resource
- If other links depend on resource → mark resource `status: 'rolled_back'`
- Delete or mark rolled_back all created links
- Append rollback decision to candidate history
- Write rollback transaction manifest
- Preserve audit history

---

## Safety Invariants (All Routes)

- No graph/canonical mutation
- No external verification
- No learner exposure
- No fake metadata
- No auto-promotion without gates
- No auto-linking without per-link review
