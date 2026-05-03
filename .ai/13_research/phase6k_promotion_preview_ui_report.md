# Phase 6K Promotion Preview UI Report

**Date:** 2026-05-03
**Status:** Implemented
**File:** `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`

---

## Changes

### New Tab: Promotion Preview

Added to `ExternalCandidateReviewPanel` mode selector:
- Detail | Correction | Review Decision | History | **Promotion Preview**

### Auto-Fetch Behavior

When Promotion Preview tab is selected:
1. Calls `previewExternalCandidatePromotion(candidate.candidateId)`
2. Displays loading state
3. Renders preview response

### Display Elements

| Element | Content |
|---|---|
| Eligibility badge | Green "Eligible" or red "Not eligible" |
| Preview-only badge | Yellow "Preview only" |
| Blockers | Rose-colored list if present |
| Warnings | Amber-colored list if present |
| Missing fields | Amber-colored list if present |
| Proposed resource draft | Card with resourceId, title, type, verificationStatus, learnerVisible, status |
| Proposed link drafts | Cards with linkId, nodeId, relationship, reviewStatus |
| Caveats | Source truth, standards context, rights, verification |
| Safety badges | "Promotion apply not implemented", "No resource creation", "No link creation", "No learner exposure" |

### Safe Wording Used

- "Preview only — not created"
- "No resource will be created by this preview"
- "No node link will be created by this preview"
- "Promotion apply not implemented"
- "No resource creation"
- "No link creation"
- "No learner exposure"

### Absent Elements (by design)

- ❌ Create Resource button
- ❌ Create Link button
- ❌ Apply Promotion button
- ❌ Accept Candidate button
- ❌ learner-visible toggle
