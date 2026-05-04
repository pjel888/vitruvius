# Phase 6L — Promotion Apply API Plan

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** API design for future implementation

---

## 1. Current State

- Promotion preview route exists: `POST /resources/review/external-candidates/:candidateId/promotion-preview` (read-only)
- Promotion apply route: DOES NOT EXIST
- Promotion rollback-preview route: DOES NOT EXIST
- Promotion rollback route: DOES NOT EXIST

---

## 2. Future Routes

### Route A: POST .../promotion-apply-preview

May be identical to the existing promotion-preview route, or may extend it with additional fields needed for apply.

| Property | Detail |
|----------|--------|
| Method | POST |
| Path | `/api/resources/review/external-candidates/:candidateId/promotion-apply-preview` |
| Gate | Must have a valid candidateId |
| Read-only | Yes |
| Auth | `requireLocalDevAdmin` |
| Request body | Currently same as promotion-preview; may add `applyMode` for preview purposes |
| Response | Gate checklist, resource draft, optional link drafts, caveats, warnings |
| Mutation | NONE |

**Request shape (future):**
```jsonc
{
  "applyMode": "resource_only" | "resource_and_links"
}
```

**Response shape:**
```jsonc
{
  "candidateId": "ec_<uuid>",
  "applyMode": "resource_only",
  "gates": [
    { "id": "A1", "label": "Candidate exists", "status": "pass" },
    { "id": "A2", "label": "Candidate ready for promotion", "status": "pass" },
    // ... all applicable gates
  ],
  "allGatesPass": true,
  "blockingGates": [],
  "resourceDraft": { /* future Resource record shape */ },
  "linkDrafts": [], // empty for resource_only mode
  "caveats": {
    "sourceTruthCaveat": "Not externally verified",
    "standardsContextCaveat": null,
    "rightsCaveat": null
  },
  "previewHash": "sha256-<hash>",
  "canApply": true
}
```

---

### Route B: POST .../promotion-apply

FUTURE IMPLEMENTATION ONLY. This route does not exist yet.

| Property | Detail |
|----------|--------|
| Method | POST |
| Path | `/api/resources/review/external-candidates/:candidateId/promotion-apply` |
| Gate | All 9 gate groups (A-I) must pass |
| Mutation | Creates Resource, optionally nodeResourceLinks |
| Auth | `requireLocalDevAdmin` |
| Transaction-backed | Yes |
| Graph/canonical mutation | FORBIDDEN |
| External verification | FORBIDDEN |

**Request shape:**
```jsonc
{
  "applyMode": "resource_only" | "resource_and_links",
  "reviewer": "reviewer_handle",
  "rationale": "Why this candidate is being promoted",
  "sourceOfContext": "Where the reviewer obtained context",
  "previewHash": "sha256-<hash-from-preview>",
  "proposedNodeIds": ["n_node1", "n_node2"], // required if resource_and_links
  "proposedRelations": {
    "n_node1": "evidence_for",
    "n_node2": "related_to"
  },
  "nodeRationales": {
    "n_node1": "Specific rationale for this node",
    "n_node2": "Specific rationale for second node"
  },
  "promotionCaveat": "Not externally verified; reviewer-curated metadata only",
  "acknowledgeWarnings": true
}
```

**Response shape (success):**
```jsonc
{
  "success": true,
  "transactionManifestId": "tm_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "createdResource": {
    "resourceId": "res_<uuid>",
    "title": "..."
  },
  "createdLinks": [
    { "linkId": "nl_<uuid>", "nodeId": "n_node1", "status": "needs_review" }
  ],
  "candidateHistoryUpdated": true,
  "learnerExposure": false,
  "externalVerification": false,
  "graphMutation": false
}
```

**Response shape (gate failure):**
```jsonc
{
  "success": false,
  "gate": "C4",
  "message": "Promotion apply must not set source_verified unless real verification workflow exists",
  "severity": "stop",
  "blockingGates": ["C4"]
}
```

---

### Route C: POST .../promotion-rollback-preview

| Property | Detail |
|----------|--------|
| Method | POST |
| Path | `/api/resources/review/external-candidates/:candidateId/promotion-rollback-preview` |
| Gate | Promotion must have occurred |
| Read-only | Yes |
| Auth | `requireLocalDevAdmin` |
| Mutation | NONE |

**Request shape:**
```jsonc
{
  "promotionDecisionId": "pd_<uuid>"
}
```

**Response shape:**
```jsonc
{
  "candidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "rollbackPlan": {
    "resourcesToRemove": ["res_<uuid>"],
    "linksToRemove": ["nl_<uuid>"],
    "candidateHistoryAction": "append_rollback_decision",
    "rollbackType": "hard_delete_or_mark_rolled_back"
  },
  "preRollbackStateSummary": {
    "resourcesBefore": 7,
    "linksBefore": 9
  },
  "canRollback": true
}
```

---

### Route D: POST .../promotion-rollback

| Property | Detail |
|----------|--------|
| Method | POST |
| Path | `/api/resources/review/external-candidates/:candidateId/promotion-rollback` |
| Gate | Promotion must have occurred; rollback preview must exist |
| Mutation | Removes or marks rolled_back resources/links |
| Auth | `requireLocalDevAdmin` |
| Transaction-backed | Yes |

**Request shape:**
```jsonc
{
  "promotionDecisionId": "pd_<uuid>",
  "reviewer": "reviewer_handle",
  "rationale": "Reason for rollback",
  "rollbackAction": "hard_delete" | "mark_rolled_back"
}
```

**Response shape:**
```jsonc
{
  "success": true,
  "rollbackTransactionManifestId": "tm_<uuid>",
  "action": "mark_rolled_back",
  "resourcesAffected": ["res_<uuid>"],
  "linksAffected": ["nl_<uuid>"],
  "candidateHistoryUpdated": true
}
```

---

## 3. Route Implementation Order (Future)

1. promotion-apply-preview (extends existing promotion-preview)
2. promotion-rollback-preview
3. promotion-apply (read-only mode first)
4. promotion-rollback

---

## 4. Code File Location (Future)

Routes should be implemented in:
- `api/resourceLayer/externalCandidatePromotionApply.ts` (new file)
- Registration in `api/index.ts`

---

## 5. Validation Rules (All Routes)

| Rule | Applied To |
|------|-----------|
| candidateId must exist and be retrievable | All routes |
| requireLocalDevAdmin (or future auth) | All mutation routes |
| previewHash must match latest preview | promotion-apply |
| applyMode must be valid enum | promotion-apply, promotion-apply-preview |
| reviewer must be non-empty string | promotion-apply, promotion-rollback |
| rationale must be non-empty | promotion-apply, promotion-rollback |
| sourceOfContext must be non-empty | promotion-apply |
| promotionCaveat must be non-empty | promotion-apply |
| acknowledgeWarnings must be true | promotion-apply |
| proposedNodeIds must exist in graph | promotion-apply (resource_and_links) |
| proposedRelations must be valid vocabulary | promotion-apply (resource_and_links) |
| nodeRationales must be non-empty per node | promotion-apply (resource_and_links) |
| No graph/canonical mutation | promotion-apply |
| No external verification claim | promotion-apply |
| No learner exposure | promotion-apply |
