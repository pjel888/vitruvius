# Phase 6H External Candidate API Plan

**Date:** 2026-05-03
**Status:** Planning — Routes Designed, NOT Implemented

## Route Summary

| Method | Route | Gate | Mutation | Phase |
|---|---|---|---|---|
| GET | `/resources/review/external-candidates/:candidateId/review` | `requireLocalDevAdmin` | No | 6H |
| POST | `/resources/review/external-candidates/:candidateId/correction-preview` | `requireLocalDevAdmin` | No | 6H |
| POST | `/resources/review/external-candidates/:candidateId/correction` | `requireLocalDevAdmin` | Yes | 6H |
| POST | `/resources/review/external-candidates/:candidateId/review-preview` | `requireLocalDevAdmin` | No | 6H |
| POST | `/resources/review/external-candidates/:candidateId/review-decision` | `requireLocalDevAdmin` | Yes | 6H |
| GET | `/resources/review/external-candidates/:candidateId/history` | `requireLocalDevAdmin` | No | 6H |
| POST | `/resources/review/external-candidates/:candidateId/promotion-preview` | `requireLocalDevAdmin` | No | Future |

---

## GET /resources/review/external-candidates/:candidateId/review

**Purpose:** Return candidate with review context.

**Response:**
```json
{
  "candidate": { ...ExternalMetadataCandidateRecord... },
  "reviewContext": {
    "decisionHistory": [...ExternalCandidateReviewDecision...],
    "promotionReadiness": { ...PromotionReadinessChecklist... },
    "blockers": ["string"],
    "warnings": ["string"],
    "missingFields": ["string"],
    "nextActions": ["string"]
  }
}
```

**Validation:** Candidate must exist.

---

## POST /resources/review/external-candidates/:candidateId/correction-preview

**Purpose:** Preview a metadata correction without applying.

**Request:**
```json
{
  "reviewer": "string",
  "rationale": "string",
  "correctionPatch": {
    "title": "string",
    "proposedUrl": "string",
    "proposedDoi": "string",
    "proposedIsbn": "string",
    "proposedPublisher": "string",
    "proposedAuthors": ["string"],
    "proposedPublicationDate": "string",
    "proposedEdition": "string",
    "proposedVersion": "string",
    "proposedScope": "string",
    "proposedJurisdiction": "string",
    "proposedRightsStatus": "string",
    "candidateRationale": "string"
  }
}
```

**Response:**
```json
{
  "diff": { "before": {...}, "after": {...} },
  "blockers": ["string"],
  "warnings": ["string"],
  "valid": true
}
```

**Validation Rules:**
- `correctionPatch` cannot set `learnerVisible=true`.
- `correctionPatch` cannot set `verificationStatus='verified'`.
- `correctionPatch` cannot set `resourceId` or `nodeResourceLinkId`.
- Placeholder values rejected for edition/version/scope.

---

## POST /resources/review/external-candidates/:candidateId/correction

**Purpose:** Apply a validated metadata correction.

**Request:** Same as correction-preview.

**Response:**
```json
{
  "candidate": { ...updated record... },
  "decision": { ...decision record... },
  "manifest": { "transactionId": "string" }
}
```

**Mutation:**
- Updates `external-metadata-candidates.json`.
- Appends to `external-candidate-decisions.json`.
- Writes transaction manifest.

---

## POST /resources/review/external-candidates/:candidateId/review-preview

**Purpose:** Preview a review decision.

**Request:**
```json
{
  "reviewer": "string",
  "rationale": "string",
  "decisionType": "reject" | "defer" | "needs_more_context" | "ready_for_promotion_review" | "duplicate_candidate",
  "duplicateOfCandidateId": "string",
  "deferUntil": "string"
}
```

**Response:**
```json
{
  "valid": true,
  "blockers": ["string"],
  "nextStatus": "string",
  "promotionReadiness": { ... }
}
```

**Validation:**
- `ready_for_promotion_review` requires all promotion gates to pass.
- `duplicate_candidate` requires `duplicateOfCandidateId` or `duplicateOfResourceId`.
- `reject` requires `rationale`.

---

## POST /resources/review/external-candidates/:candidateId/review-decision

**Purpose:** Apply a review decision.

**Request:** Same as review-preview.

**Response:**
```json
{
  "candidate": { ...updated record... },
  "decision": { ...decision record... },
  "manifest": { "transactionId": "string" }
}
```

**Mutation:**
- Updates candidate `status` in `external-metadata-candidates.json`.
- Appends to `external-candidate-decisions.json`.
- Writes transaction manifest.

---

## GET /resources/review/external-candidates/:candidateId/history

**Purpose:** Return full decision history for a candidate.

**Response:**
```json
{
  "candidateId": "string",
  "decisions": [...ExternalCandidateReviewDecision...],
  "decisionCount": 0
}
```

---

## POST /resources/review/external-candidates/:candidateId/promotion-preview

**Purpose:** Preview candidate-to-resource promotion (FUTURE ONLY).

**Response:**
```json
{
  "ready": true,
  "proposedResource": { ...Resource... },
  "proposedLinks": [ ...NodeResourceLink... ],
  "blockers": ["string"],
  "warnings": ["string"]
}
```

**NOT implemented in Phase 6H.**

## Safety Caveats

- All mutation routes are `requireLocalDevAdmin` gated.
- No route creates `Resource` or `NodeResourceLink`.
- No route sets `learnerVisible=true`.
- No route calls external APIs.
- All mutations write transaction manifests.
