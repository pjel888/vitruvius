# Phase 6L Promotion Apply UI Plan

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## New UI Components

### Promotion Apply Preview Panel

Extends the existing Promotion Preview tab in `ExternalCandidateReviewPanel`.

### Apply Mode Selector

```tsx
<select>
  <option value="resource_only">Resource only</option>
  <option value="resource_and_links">Resource + node links</option>
</select>
```

- Default: `resource_only` (safer)
- `resource_and_links` only enabled if candidate has valid `proposedNodeIds` and `proposedRelation`

### Required Fields

| Field | Required | Validation |
|---|---|---|
| Reviewer | Yes | Non-empty string |
| Rationale | Yes | Minimum 20 characters |
| sourceOfContext | Yes | Non-empty string |
| Apply mode | Yes | One of allowed values |

### Resource Draft Diff

Display side-by-side:
- Current candidate metadata (left)
- Proposed Resource record (right)
- Highlighted fields: `resourceId`, `status`, `verificationStatus`, `displayPolicy`

### Link Draft Diff (Mode 2 only)

Display table:
| Node ID | Relationship | Rationale | Review Status |
|---|---|---|---|
| VTN-DOM-xxx | `is_primary_reference_for` | Candidate rationale | `needs_review` |

### Gate Checklist

Visual checklist showing all 9 gates:
- ✅ / ❌ for each gate
- Expandable details for failures
- Real-time update as reviewer fills required fields

### Warning Panels

**Standards Warning Panel**
- Shown for standard/guide candidates
- Lists missing context fields
- Shows ASCE 7 / ACI 318 block message if applicable

**Rights Warning Panel**
- Shows rights status
- Warns if `unknown` and learner-eligible path possible
- Shows protected content restrictions

**Source Verification Caveat Panel**
- Explicit statement: "No external verification performed"
- Lists what was NOT checked: URL reachability, DOI resolution, ISBN lookup

### Transaction Preview

Show before apply:
- Files that will be touched
- Estimated rollback complexity
- Transaction manifest ID preview

### Apply Button State

| Condition | Button State |
|---|---|
| Gates failing | Disabled, shows "Resolve blockers first" |
| Required fields missing | Disabled, shows "Fill required fields" |
| Preview hash stale | Disabled, shows "Candidate changed — refresh preview" |
| All gates pass, fields filled | Enabled, shows "Apply promotion (transaction-backed)" |

### Post-Apply State

After successful apply:
- Show success message with transaction manifest ID
- Show created resource ID
- Show created link IDs (if mode 2)
- Show "Rollback available" button
- Auto-refresh candidate list
- Candidate status changes to `promoted` or similar

---

## Safe Wording Requirements

### Required Labels
- "Promotion apply preview"
- "Create Resource record"
- "Create node-resource link"
- "Reviewer-approved metadata"
- "Source-custody reviewed"
- "Not external-verified"
- "Not compliance claim"
- "Not governing/current unless context reviewed"
- "Learner visibility computed after link acceptance"
- "Transaction-backed"
- "Rollback available"

### Forbidden Labels
- "verified source"
- "official"
- "current standard"
- "governing standard"
- "compliant"
- "AHJ accepted"
- "reachable URL"
- "valid DOI"
- "valid ISBN"
- "accepted resource without caveat"
- "learner approved"

---

## Accessibility and Safety

- Apply button requires double-click or confirmation dialog
- Red color for destructive actions (apply, rollback)
- Green color only for successfully completed transactions
- Yellow/amber for warnings and caveats
- All caveats must be visible without scrolling
