# Phase 6L — Resource Review UI Plan

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** UI design for future implementation

---

## 1. Current State

The ResourceReviewAdmin UI component currently supports:
- External candidate listing
- Candidate detail view
- Correction/review workflow (Phase 6I)
- Promotion preview panel (Phase 6K, read-only)

---

## 2. Future UI Additions

### 2.1 Promotion Apply Preview Panel

A new panel below the existing promotion preview, activated when the candidate is `ready_for_promotion_review`.

**Content:**
- Apply mode selector: radio buttons for "Resource only" vs "Resource + selected links"
- Resource draft diff: shows the future Resource record shape
- Link draft diff: shows future nodeResourceLink records (only in resource_and_links mode)
- Gate checklist: live rendering of all applicable gates with pass/fail/skipped status
- Caveat panels:
  - Standards warning panel (if standard/code type and context incomplete)
  - Rights warning panel (if rightsStatus unknown or restricted)
  - Source verification caveat panel (always: "Not externally verified")
- Transaction/rollback preview: shows files that will be touched and rollback plan
- Required fields:
  - Reviewer handle
  - Rationale
  - Source of context
  - Promotion caveat acknowledgment
- Apply button: disabled until all gates pass AND required fields filled
- Warning banner: "Promotion apply requires explicit steward authorization"

### 2.2 Apply Mode Selector

```html
<radio-group name="applyMode">
  <radio value="resource_only">Resource only
    <help-text>Create a Resource record without node links</help-text>
  </radio>
  <radio value="resource_and_links">Resource + selected links
    <help-text>Create a Resource record and attach to graph nodes</help-text>
  </radio>
</radio-group>
```

The selector is only shown if the candidate has proposedNodeIds. If no nodeIds, mode defaults to `resource_only` and the selector is hidden.

### 2.3 Gate Checklist UI

A vertical checklist showing each gate group:

```
[PASS] A. Candidate Status
[PASS] B. Metadata Integrity
[PASS] C. Source Truth
[PASS] D. Rights
[SKIP] E. Standards (not applicable — not a standard type)
[SKIP] F. Node Link (resource_only mode)
[PASS] G. Display/Learner
[PASS] H. Transaction/Rollback
[  ⚠  ] I. Audit — Missing: reviewer, rationale, sourceOfContext
```

Each gate row shows:
- Pass/fail/skip status icon
- Gate label
- Click to expand details
- If failed: message explaining why

### 2.4 Resource Draft Diff

Shows the Resource record that will be created, with caveats highlighted:

```
Resource Draft:
  resourceId:    (generated)
  title:         "ASCE/SEI 7-22"  ✓
  resourceType:  standard  ✓
  sourceType:    governing-code  ⚠ reviewer-curated
  ⚠ Not externally verified
  ⚠ Not learner-visible
  ⚠ URL syntax-checked only (not verified reachable)
```

### 2.5 Link Draft Diff

Shows each proposed nodeResourceLink:

```
Link Draft:
  node:     n_base_node_structural_design
  relation: evidence_for
  status:   needs_review  ✓
  ⚠ Link not accepted until link gates pass
  ⚠ Not learner-visible
```

### 2.6 Standards Warning Panel

Appears for standard/code/governing-document candidates:

```
⚠ Standards Warning
- Edition: "22"  ✓ (non-placeholder)
- Scope: "Minimum design loads"  ✓ (non-placeholder)
- ASCE 7 is currently incomplete
- No 'current' or 'governing' claim made
- This promotion does not verify current/governing status
```

### 2.7 Rights Warning Panel

```
⚠ Rights Warning
- rightsStatus: open_access  ✓
- No display restriction warnings
- Reviewer rationale for rights assessment: provided
```

If rightsStatus is unknown or restricted:
```
⛔ Rights Issue
- rightsStatus: unknown
- Cannot promote to learner-visible status
- Promotion will set displayPolicy: reviewer_only
```

### 2.8 Apply Button

```html
<button disabled={!canApply}
        title="Promotion apply requires explicit steward authorization">
  Apply Promotion
</button>
```

Disabled until:
- All gates pass
- All required fields filled (reviewer, rationale, sourceOfContext)
- Acknowledge warnings checkbox checked
- previewHash matches latest preview

### 2.9 Rollback Preview Panel

After a successful apply, the UI transitions to show:

```
✓ Promotion applied successfully
  Transaction Manifest: tm_<uuid>
  Promotion Decision: pd_<uuid>
  Created Resource: res_<uuid>
  [Show rollback info]
```

---

## 3. Safe / Unsafe Wording

### Safe Wording (DO use)

| Phrase | Reason |
|--------|--------|
| "Promotion apply preview" | Accurate description |
| "Create Resource record" | Accurate: creates a curated object |
| "Create node-resource link" | Accurate: creates a link |
| "Reviewer-approved metadata" | Accurate: reviewer reviewed metadata |
| "Source-custody reviewed" | Accurate: reviewed for custody purposes |
| "Not external-verified" | Accurate caveat |
| "Not compliance claim" | Honest about limitations |
| "Not governing/current unless context reviewed" | Honest caveat |
| "Learner visibility computed after link acceptance" | Accurate lifecycle |
| "Transaction-backed" | Accurate technical feature |
| "Rollback available" | Accurate technical feature |

### Unsafe Wording (DO NOT use)

| Phrase | Reason |
|--------|--------|
| "Verified source" | Implies trust level not achieved |
| "Official" | Implies endorsement without verification |
| "Current standard" | Implies currency authority |
| "Governing standard" | Implies legal authority |
| "Compliant" | Implies compliance review |
| "AHJ accepted" | Implies AHJ verification |
| "Reachable URL" | Would require URL check (not done) |
| "Valid DOI" | Syntax-only, not DOI resolution |
| "Valid ISBN" | Syntax-only, not ISBN lookup |
| "Accepted resource" (without caveat) | Misleading without limitations |
| "Learner approved" | Visibility not determined by promotion |

---

## 4. Component Design (Future Reference)

Future UI components:
- `explorer/src/components/resource-review/PromotionApplyPanel.tsx` (new)
- `explorer/src/components/resource-review/PromotionGateChecklist.tsx` (new)
- `explorer/src/components/resource-review/PromotionDraftDiff.tsx` (new)
- `explorer/src/components/resource-review/PromotionWarningPanel.tsx` (new)
- `explorer/src/components/resource-review/PromotionRollbackPanel.tsx` (new)

Integration into existing `ResourceReviewAdmin.tsx`:
- Add promotion apply panel after promotion preview panel
- Conditionally render based on candidate status
- Add apply mode selector in candidate detail view (if proposedNodeIds exist)
