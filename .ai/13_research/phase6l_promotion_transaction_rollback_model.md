# Phase 6L — Promotion Transaction and Rollback Model

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Transaction model design for future implementation

---

## 1. Transaction Requirements

Every promotion apply operation MUST wrap its mutations in a transaction manifest. The manifest ensures:

- Atomicity: All mutations succeed together or can be rolled back
- Auditability: Every mutation is recorded with before/after state
- Recovery: Rollback can restore prior state
- Traceability: Every mutation links back to the candidate and decision

---

## 2. Transaction Manifest Structure

```jsonc
{
  "transactionManifestId": "tm_<uuid>",
  "previousManifestHash": "sha256-<hash-of-previous-manifest>",
  "operationType": "external_candidate_resource_promotion" |
                    "external_candidate_link_promotion" |
                    "external_candidate_resource_and_link_promotion",
  "candidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "reviewer": "reviewer_handle",
  "rationale": "Why this promotion was performed",
  "sourceOfContext": "Reviewer's context source",
  "appliedAt": "2026-05-04T12:00:00Z",
  "touchedFiles": [
    {
      "filePath": "api/resourceLayer/resources.json",
      "operation": "append",
      "beforeHash": "sha256-<before>",
      "afterHash": "sha256-<after>"
    },
    {
      "filePath": "api/resourceLayer/nodeResourceLinks.json",
      "operation": "append",
      "beforeHash": "sha256-<before>",
      "afterHash": "sha256-<after>"
    },
    {
      "filePath": "api/resourceLayer/externalMetadataCandidates.json",
      "operation": "update_candidate_history",
      "beforeHash": "sha256-<before>",
      "afterHash": "sha256-<after>"
    }
  ],
  "createdResourceIds": ["res_<uuid>"],
  "createdLinkIds": ["nl_<uuid>"] || [],
  "rollbackPlan": {
    "resourcesToRemove": ["res_<uuid>"],
    "linksToRemove": ["nl_<uuid>"],
    "candidateAction": "append_rollback_decision",
    "rollbackType": "hard_delete_or_mark_rolled_back"
  },
  "noGraphCanonicalMutation": true,
  "noExternalVerification": true,
  "noLearnerExposure": true,
  "learnerExposureStatus": "none",
  "rollbackInfo": null
}
```

---

## 3. Operation Types

| operationType | Mutations | When Used |
|---------------|-----------|-----------|
| `external_candidate_resource_promotion` | Resource registry only | resource_only mode |
| `external_candidate_link_promotion` | Resource + link registries | resource_and_links mode (standalone link promotion from existing resource) |
| `external_candidate_resource_and_link_promotion` | Resource + link registries | resource_and_links mode (both created together) |

---

## 4. Rollback Behavior

### Rollback Types

| Type | Behavior | When Allowed |
|------|----------|-------------|
| `hard_delete` | Delete Resource and nodeResourceLink records entirely | Only when no other resources/links depend on the deleted records |
| `mark_rolled_back` | Set `rollbackInfo.rolledBackAt`, `rollbackInfo.rolledBackBy`, `rollbackInfo.rationale`; keep record for audit | Always safe |

### Rollback Steps

1. Load the original transaction manifest
2. For each created resource:
   - If `hard_delete`: remove resource record from registry
   - If `mark_rolled_back`: set `rollbackInfo` fields on resource record
3. For each created link:
   - If `hard_delete`: remove link record from registry
   - If `mark_rolled_back`: set `rollbackInfo` fields on link record
4. Append rollback decision to external candidate history:
   - Decision type: `promotion_rolled_back`
   - Links to original promotionDecisionId
   - Records rollback reviewer/rationale/timestamp
5. Write rollback transaction manifest:
   - Records all changes made during rollback
   - Links back to the original promotion manifest
6. Restore file hashes if applicable

### Rollback Safety

- Rollback MUST NOT delete a Resource if any other Resource or nodeResourceLink depends on it
- If deletion is unsafe, rollback MUST use `mark_rolled_back` instead
- Rollback MUST preserve audit history (even deleted records should leave audit trail)
- Rollback MUST produce its own transaction manifest

---

## 5. Transaction File Scope

Promotion apply transaction MUST touch ONLY the following files:

| File | Operation | Notes |
|------|-----------|-------|
| Resource registry | Append resource record | e.g., `api/resourceLayer/resources.json` |
| nodeResourceLink registry | Append link records | Only if `resource_and_links` mode |
| External candidate registry | Append decision to candidate history | e.g., `externalMetadataCandidates.json` |
| Transaction manifest registry | Append manifest | e.g., `api/resourceLayer/transactionManifests.json` |

Forbidden touched files:
- Graph registries (003-Canonical-Knowledge-Layer)
- Graph edge stores
- Any learner-facing data store
- Source markdown artifacts
- P0/high-risk P1 registries

---

## 6. Transaction Lifecycle

```
1. PREPARE
   - Load candidate
   - Check all gates A-I
   - Compute beforeHashes for all touched files
   - Generate resourceId, linkIds, promotionDecisionId, manifestId
   - Build rollback plan

2. EXECUTE (if all gates pass)
   - Create Resource record
   - Create nodeResourceLink records (if mode == resource_and_links)
   - Append promotion decision to candidate history
   - Compute afterHashes for all touched files
   - Write transaction manifest
   - Confirm learnerExposure = false
   - Confirm no graph mutation

3. POST-EXECUTION
   - Verify file state
   - Return success with transaction details

4. ROLLBACK (if needed)
   - Load transaction manifest
   - Execute rollback plan
   - Write rollback manifest
   - Verify restored state
```
