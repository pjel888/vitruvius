# Phase 6N — Resource Review UI Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** UI design/specification complete

---

## 1. UI Component: PromotionApplyPanel

### Location
New component: `explorer/src/components/resource-review/PromotionApplyPanel.tsx`

### Purpose
Provide the UI for resource-only promotion apply in the ResourceReviewAdmin component.

### Features

| Feature | Status |
|---------|--------|
| Apply mode selector locked to resource_only | Implemented |
| Resource draft diff | Implemented |
| Gate checklist with pass/fail/skip status | Implemented |
| reviewer/rationale/sourceOfContext fields | Implemented |
| Transaction/rollback preview | Implemented |
| Disabled apply button until all gates pass | Implemented |
| Clear warning text | Implemented |
| Rollback preview after promotion | Implemented |

### Warning Text Displayed

```
Promotion Apply — Resource Only

This operation will:
- Create a Resource record (reviewer-only, not learner-visible)
- Create NO node links
- Perform NO external verification
- Make NO compliance/current/governing/AHJ claims
- Write a transaction manifest
- Support rollback

The promoted Resource will NOT be learner-visible.

Requires explicit steward authorization.
```

---

## 2. UI Safety Controls

| Control | Behavior |
|---------|----------|
| Apply button | Disabled until all gates pass AND all fields filled |
| resource_and_links selector | NOT PRESENT in Phase 6N UI |
| Learner-visible toggle | NOT PRESENT |
| Accept as learner resource | NOT PRESENT |
| External verification button | NOT PRESENT |
| Rollback preview | Available after successful promotion |

---

## 3. Safe vs Unsafe Wording

### Safe Wording (Used)

- "Create reviewer-only Resource record"
- "Resource-only promotion"
- "No node links will be created"
- "Not learner-visible"
- "No external verification performed"
- "Requires separate link review"
- "Transaction-backed"
- "Rollback available"
- "Reviewer-approved metadata"
- "Source-custody reviewed"

### Unsafe Wording (NOT Used)

- "Verified source" — NOT PRESENT
- "Official" — NOT PRESENT
- "Current standard" — NOT PRESENT
- "Governing standard" — NOT PRESENT
- "Compliant" — NOT PRESENT
- "AHJ accepted" — NOT PRESENT
- "Reachable URL" — NOT PRESENT
- "Valid DOI" — NOT PRESENT
- "Valid ISBN" — NOT PRESENT
- "Accepted learner resource" — NOT PRESENT
- "Linked to node" — NOT PRESENT

---

## 4. Gate Checklist Display

The gate checklist renders as a vertical list with status icons:

```
[PASS]  Candidate exists
[PASS]  Candidate ready for promotion review
[PASS]  Title present
[PASS]  Resource type present
[SKIP]  Standards context (not a standard type)
[PASS]  No duplicate resource
[PASS]  Learner visibility safe
[  !  ] Reviewer provided
[  !  ] Rationale provided
[  !  ] Source of context provided
```

---

## 5. Promotion Result Display

After successful resource-only promotion, the UI shows:

```
Promotion Applied Successfully

  Resource ID:    res_<uuid>
  Apply mode:     resource_only
  Links created:  0
  Learner visible: false
  External verification: none
  Transaction ID: tm_<uuid>

  [Rollback Preview]
```

---

## 6. Integration Points

| Component | Change |
|-----------|--------|
| `ResourceReviewAdmin.tsx` | Add PromotionApplyPanel after existing promotion preview section |
| `ResourceReviewAdmin.tsx` | Show promo apply panel conditionally when candidate is `ready_for_promotion_review` |
