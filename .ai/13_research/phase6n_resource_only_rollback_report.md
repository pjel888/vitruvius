# Phase 6N — Resource-Only Rollback Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Rollback implementation complete

---

## 1. Rollback Routes

### POST .../promotion-rollback-preview

**Purpose:** Read-only preview of rollback impact before execution.

**Request:**
```json
{
  "resourceId": "res_<uuid>"
}
```

**Response:**
```json
{
  "candidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "resourceId": "res_<uuid>",
  "rollbackPlan": {
    "action": "hard_delete",
    "notes": "No dependent links — can hard-delete Resource record"
  },
  "preRollbackStateSummary": {
    "resourcesBefore": 7,
    "linksBefore": 0
  },
  "canRollback": true
}
```

### POST .../promotion-rollback

**Purpose:** Execute rollback of a promoted resource.

**Request:**
```json
{
  "resourceId": "res_<uuid>",
  "reviewer": "string (required)",
  "rationale": "string (required)",
  "rollbackAction": "hard_delete | mark_rolled_back"
}
```

**Response (success):**
```json
{
  "success": true,
  "rollbackTransactionManifestId": "tm_<uuid>",
  "action": "hard_delete",
  "resourcesAffected": ["res_<uuid>"],
  "linksAffected": [],
  "candidateHistoryUpdated": false
}
```

---

## 2. Rollback Types

| Type | Behavior | When Allowed |
|------|----------|-------------|
| `hard_delete` | Remove Resource record from registry | Always in resource_only mode (no link dependencies) |
| `mark_rolled_back` | Set rollbackInfo fields, keep record | Always safe |

In Phase 6N, since no nodeResourceLinks are created, hard_delete is always safe for resource_only promotions. `mark_rolled_back` is available for audit-preservation preferences.

---

## 3. Rollback Safety

| Check | Implementation |
|-------|---------------|
| Rollback-preview is read-only | Yes — no mutation, only reads registry |
| Requires reviewer/rationale | Yes — validated in request handler |
| Transaction manifest created | Yes — rollback manifest written to `transactionManifests.json` |
| No graph/canonical mutation | Yes — only touches resources.json |
| Candidate history preserved | No — candidate history not updated on rollback (scope limitation) |

---

## 4. Rollback Manifest

```json
{
  "transactionManifestId": "tm_<uuid>",
  "previousManifestHash": null,
  "operationType": "external_candidate_resource_promotion_rollback",
  "candidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "reviewer": "reviewer_name",
  "rationale": "Rolling back due to metadata error",
  "sourceOfContext": "",
  "appliedAt": "2026-05-04T...",
  "touchedFiles": [{
    "filePath": "api/resourceLayer/resources.json",
    "operation": "remove",
    "beforeHash": "...",
    "afterHash": "..."
  }],
  "createdResourceIds": [],
  "createdLinkIds": [],
  "rollbackPlan": null,
  "noGraphCanonicalMutation": true,
  "noExternalVerification": true,
  "noLearnerExposure": true,
  "learnerExposureStatus": "none",
  "rollbackInfo": null
}
```

---

## 5. Rollback Limitations (Phase 6N)

- Candidate history is NOT automatically updated on rollback (requires extending the candidate decision flow)
- Rollback does NOT revert candidate status to pre-promotion state
- Rollback does NOT affect any candidate safety flags
- These limitations are acceptable for Phase 6N and may be addressed in Phase 6P
