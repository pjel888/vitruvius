# Phase 6E External Candidate Preview API Report

**Generated:** 2026-05-03
**Status:** Implemented

---

## Routes Added

### GET /resources/review/external-candidates/schema
Returns the external metadata candidate schema document.

**Response:**
```json
{
  "schemaVersion": "vitruvius-external-metadata-candidate/v1",
  "resourceTypes": [...],
  "fields": [...],
  "defaults": {
    "verificationStatus": "unverified",
    "displayPolicy": "reviewer_only",
    "learnerVisible": false
  },
  "constraints": {
    "noAutoVerification": true,
    "noAutoPromotion": true,
    "noAutoLinking": true,
    "noLearnerExposure": true,
    "standardsRequireCompleteContext": true
  }
}
```

### POST /resources/review/external-candidates/preview
Returns a normalized, validated preview of an external metadata candidate.

**Request body:** `ExternalMetadataCandidateInput`

**Response:** `ExternalMetadataCandidatePreview`

**Behavior:**
- Requires `local/dev/admin` gate
- Validates request body
- Returns normalized candidate preview
- Returns warning flags
- Returns missing fields
- Returns fake placeholder flags
- Sets `learnerVisible: false`
- Sets `verificationStatus: unverified`
- Sets `displayPolicy: reviewer_only`
- Includes source truth caveat
- Does NOT write files
- Does NOT create resources/candidates/links/manifests
- Does NOT fetch external URLs
- Does NOT call external APIs

---

## Implementation Location

- Route handlers: `api/index.ts` (lines ~4583–4620)
- Validation logic: `api/resourceLayer/externalMetadataCandidates.ts`

---

## Test Coverage

- `api/resourceLayerExternalCandidates.test.ts`
  - 24 tests (all passing)
  - URL/DOI/ISBN syntax validation
  - Placeholder rejection
  - Standard candidate behavior
  - No-mutation safety
  - API route responses

---

*No production Resource Layer data mutated.*
