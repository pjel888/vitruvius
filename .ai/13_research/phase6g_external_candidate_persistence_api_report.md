# Phase 6G External Candidate Persistence API Report

**Generated:** 2026-05-03T01:00:00+08:00

---

## Routes Added

### POST /resources/review/external-candidates

**Purpose:** Persist a validated external metadata candidate.

**Gate:** `requireLocalDevAdmin`

**Request:** `ExternalMetadataCandidateInput` JSON body

**Behavior:**
- Re-runs preview validation
- Rejects if validation errors exist
- Rejects if placeholder flags exist
- Forces learnerVisible=false, displayPolicy=reviewer_only
- Detects duplicates
- Creates transaction manifest
- Writes to `external-metadata-candidates.json`

**Response (201):**
```json
{
  "ok": true,
  "candidate": { /* ExternalMetadataCandidateRecord */ },
  "manifest": { "transactionId": "...", "manifestHash": "..." }
}
```

**Response (400):**
```json
{
  "error": { "message": "..." },
  "duplicateOf": { /* existing record */ }
}
```

### GET /resources/review/external-candidates

**Purpose:** List persisted external candidates.

**Gate:** `requireLocalDevAdmin`

**Query params:** `status`, `resourceType`

**Response:**
```json
{
  "schemaVersion": "vitruvius-external-metadata-candidate/v1",
  "count": 0,
  "candidates": []
}
```

### GET /resources/review/external-candidates/:candidateId

**Purpose:** Get single candidate detail.

**Gate:** `requireLocalDevAdmin`

**Response:** `ExternalMetadataCandidateRecord` or 404.

### Source-Custody Route Hardening

**GET /resources/review/source-custody** now requires `requireLocalDevAdmin`.

Rationale: Exposes reviewer-only metadata (needs_review links, standards context, local files, rejected items).

---

## Safety Checklist

| Check | Status |
|-------|--------|
| Dev/admin gate on persist | ✅ |
| Dev/admin gate on list | ✅ |
| Dev/admin gate on detail | ✅ |
| Dev/admin gate on source-custody | ✅ |
| Preview validation re-run | ✅ |
| Placeholder rejection | ✅ |
| learnerVisible=false forced | ✅ |
| displayPolicy=reviewer_only forced | ✅ |
| Transaction manifest written | ✅ |
| No resource created | ✅ |
| No nodeResourceLink created | ✅ |
| No external fetch | ✅ |
