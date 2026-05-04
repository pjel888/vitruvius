# Phase 6N — Source-Custody Queue Integration Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Integration specification

---

## 1. Post-Promotion Candidate State

After a resource-only promotion, the external candidate's state changes as follows:

| Field | Before Promotion | After Promotion |
|-------|-----------------|-----------------|
| `status` | `ready_for_promotion_review` | `ready_for_promotion_review` (unchanged) or `promoted` (if status change implemented) |
| `decisions` | Review history | + Promotion apply decision record |
| `createdResourceId` | Not present | `res_<uuid>` |
| `resourceOnlyPromoted` | Not present | `true` |
| `nodeLinksCreated` | Not present | `0` |

---

## 2. Candidate Decision Record

The promotion decision is appended to `candidate.decisions[]`:

```json
{
  "decisionId": "pd_<uuid>",
  "type": "promotion_apply",
  "applyMode": "resource_only",
  "createdResourceId": "res_<uuid>",
  "reviewer": "reviewer_name",
  "rationale": "Metadata complete, rights clear",
  "sourceOfContext": "Publisher metadata",
  "caveat": "Not externally verified",
  "timestamp": "2026-05-04T12:00:00Z",
  "learnerExposure": false,
  "externalVerification": false,
  "graphMutation": false,
  "canonicalMutation": false
}
```

---

## 3. Source-Custody Queue Display

The promoted resource appears in reviewer/admin queues as:

| Field | Value |
|-------|-------|
| Display policy | `reviewer_only` |
| Custody status | `source_candidate_promoted` |
| Learner-visible | `false` |
| Blocking reason | `resource_promoted_without_accepted_link` |
| Next review action | `review_promoted_resource_metadata` |

---

## 4. Queue Actions

Available actions for a resource-only promoted candidate:

| Action | Behavior |
|--------|----------|
| `review_promoted_resource_metadata` | Review the created Resource metadata |
| `decide_node_linking_separately` | Start the (future) node-linking workflow |
| `rollback_promotion` | Roll back the resource-only promotion |

---

## 5. Learner Visibility

- The promoted Resource is NOT learner-visible (`learnerVisibleDefault: false`)
- The candidate is NOT learner-visible 
- The NodeInspector learner sidebar does NOT show this resource
- Learner visibility requires a future accepted nodeResourceLink

---

## 6. Warning Flags

The promoted resource carries these warning flags:

```json
[
  "not_externally_verified",
  "reviewer_curated_only"
]
```

These flags are visible in the reviewer/admin queue but NOT to learners.

---

## 7. Integration Points

| Component | Integration |
|-----------|-------------|
| `sourceCustodyQueue.ts` | Should detect `candidate.decisions[last].type === 'promotion_apply'` and show promoted state |
| `ResourceReviewAdmin.tsx` | Should show promoted Resource status in candidate detail and queue views |
| `explorer/src/api/graphApi.ts` | Should NOT expose promoted Resources without accepted nodeResourceLinks |
