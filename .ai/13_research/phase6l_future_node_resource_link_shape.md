# Phase 6L — Future NodeResourceLink Shape

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Design specification for future implementation

---

## 1. Purpose

This document defines the shape and creation gates for nodeResourceLinks that a future promotion apply (Phase 6N or 6O) may create alongside a Resource record. nodeResourceLinks connect a promoted Resource to specific graph nodes in the Resource Layer.

---

## 2. Allowed Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `linkId` | string (UUID) | Yes | Generated at creation time |
| `nodeId` | string | Yes | The graph node this link attaches to |
| `resourceId` | string (UUID) | Yes | The promoted Resource |
| `relation` | enum | Yes | Valid Resource Layer link relation (e.g., evidence_for, related_to) |
| `status` | enum | Yes | Default: `needs_review` |
| `reviewStatus` | enum | Yes | Default: `needs_review` |
| `relevance` | string | No | Node-specific relevance statement |
| `rationale` | string | Yes | Node-specific rationale |
| `reviewer` | string | Yes | Who reviewed this link |
| `reviewedAt` | ISO timestamp | Yes | When the link was reviewed |
| `sourceOfContext` | string | Yes | Where context came from |
| `createdFromExternalCandidateId` | string (UUID) | Yes | Link back to source candidate |
| `promotionDecisionId` | string (UUID) | Yes | Link to promotion decision |
| `transactionManifestId` | string (UUID) | Yes | Link to transaction manifest |
| `warningFlags` | string[] | No | Link-specific warnings |
| `displayPolicy` | enum | Yes | Default: `reviewer_only` |
| `learnerEligible` | boolean | Yes | Computed by `isLearnerSidebarEligible`, NOT manually asserted |
| `standardsContextStatus` | string | No | If standards-related link |
| `rightsStatusSummary` | string | No | Summary of rights for this link context |
| `rollbackInfo` | object | No | Populated if rolled back |

---

## 3. Validation Rules

| Rule | Enforcement |
|------|-------------|
| `nodeId` must exist in graph | Gate F2 — reject if node not found |
| `resourceId` must be the newly created Resource | Auto-set by the promotion |
| `relation` must be in valid Resource Layer link relation vocabulary | Gate F3 — reject if invalid |
| `rationale` must be node-specific (not generic) | Gate F4 — reject if missing or generic |
| `learnerEligible` must be computed, never set manually | Gate G3 — reject if manually set true |
| `status` must NOT be `accepted` unless all acceptance gates pass | Gate F6 — reject if auto-accepted |
| No graph edge may be created from link | Gate F7 — enforce no graph mutation |

---

## 4. Safe Defaults

| Field | Default | Condition for Override |
|-------|---------|----------------------|
| `status` | `needs_review` | Only `accepted` if all link acceptance gates pass and reviewer explicitly approves |
| `reviewStatus` | `needs_review` | Only `accepted` with explicit approval |
| `learnerEligible` | `false` | Computed by `isLearnerSidebarEligible` — never manual |
| `displayPolicy` | `reviewer_only` | Only changed downstream after eligibility check |

---

## 5. No Auto-Multi-Link Creation

Design rule: Do NOT design automatic multi-link creation unless every link has node-specific rationale.

- Each proposed link must have its own `rationale` field
- Each proposed link must have its own `relevance` statement
- Batch link creation is allowed IF every link in the batch meets the above criteria
- A single candidate may have 0-N proposed nodeLinks

---

## 6. JSON Skeleton (Future Implementation Reference)

```jsonc
{
  "linkId": "nl_<uuid>",
  "nodeId": "n_<graph_node_id>",
  "resourceId": "res_<uuid>",
  "relation": "evidence_for",
  "status": "needs_review",
  "reviewStatus": "needs_review",
  "relevance": "This standard is directly relevant to the node's domain",
  "rationale": "Standard X directly governs the design requirements for this node",
  "reviewer": "reviewer_handle",
  "reviewedAt": "2026-05-04T12:00:00Z",
  "sourceOfContext": "Reviewer knowledge of code adoption",
  "createdFromExternalCandidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "transactionManifestId": "tm_<uuid>",
  "warningFlags": ["not_externally_verified"],
  "displayPolicy": "reviewer_only",
  "learnerEligible": false,
  "standardsContextStatus": "needs_review",
  "rightsStatusSummary": "open_access",
  "rollbackInfo": null
}
```

---

## 7. Learner Visibility Flow

1. Promotion apply creates Resource (learnerVisibleDefault: false)
2. Promotion apply creates nodeResourceLink (learnerEligible: false, status: needs_review)
3. Future link acceptance workflow reviews link status
4. If accepted, `isLearnerSidebarEligible()` computes final eligibility
5. Only then can the resource appear in NodeInspector learner sidebar

**Promotion apply must NOT shortcut this flow.** A candidate being promoted does not mean it becomes learner-visible.

---

## 8. Registry Placement

Future nodeResourceLink records should be added to:
- A new or existing nodeResourceLinks registry (e.g., `api/resourceLayer/nodeResourceLinks.json`)
- Managed alongside the Resource registry

They must NOT be placed in graph edge registries or canonical knowledge layer.
