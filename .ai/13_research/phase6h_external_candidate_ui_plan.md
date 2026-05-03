# Phase 6H External Candidate UI Plan

**Date:** 2026-05-03
**Status:** Planning — NOT Implemented

## ResourceReviewAdmin Changes

### New Tab Structure

The "External Candidates" tab gains sub-navigation or accordion sections:

1. **Candidate List** (existing — persisted candidates)
2. **Candidate Detail / Review Panel** (new)
3. **Correction Preview** (new)
4. **Decision History** (new)
5. **Promotion Readiness** (new — read-only checklist)

### Candidate Detail / Review Panel

Displayed when a reviewer selects a candidate from the list.

**Fields shown (read-only):**
- Title, resourceType, sourceType
- URL / DOI / ISBN (with normalized display)
- Authors, publisher, publication date
- Edition, version, scope, jurisdiction
- Rights status
- Submitted by, submitted at
- Verification status (always "unverified")
- Display policy (always "reviewer_only")
- Warning flags
- Missing fields

**Actions:**
- "Preview correction" → opens correction form
- "Review decision" → opens decision panel
- "View history" → opens decision history

### Metadata Correction Preview Form

**Form fields** (pre-populated with current values, editable):
- Title
- URL, DOI, ISBN
- Authors, publisher, date
- Edition, version, scope, jurisdiction
- Rights status
- Candidate rationale

**Validation on change:**
- Real-time placeholder detection
- Cannot set learner visible
- Cannot set verified

**Buttons:**
- "Preview correction" → shows diff + blockers
- "Apply correction" → gated, writes registry

### Review Decision Panel

**Decision types** (radio or dropdown):
- Needs more context
- Metadata correction needed
- Rights review needed
- Standards context needed
- Duplicate candidate
- Deferred
- Rejected
- Ready for promotion review

**Required for all:**
- Reviewer name
- Rationale textarea

**Conditional fields:**
- Duplicate of: candidate ID or resource ID (for duplicate)
- Defer until: date (for deferred)
- Rejection reasons: checklist (for rejected)

**Buttons:**
- "Preview decision" → shows status change + blockers
- "Apply decision" → gated, writes registry

### Decision History

**Display:**
- Chronological list of decisions
- Each item: decision type, reviewer, date, rationale, status change
- Collapsible details for assessments

### Promotion Readiness Checklist

**Display:**
- Visual checklist of 8 gates (A–H)
- Green check / red X per gate
- Gate failures show specific blocker text
- Overall readiness score (0–100%)

**Wording:**
- ✅ "Ready for promotion review" (NOT "Ready for promotion")
- ❌ "Promotion blocked: [reason]"
- "Requires: [gate name]"

## Safe UI Wording Reference

| Use | Avoid |
|---|---|
| "Candidate" | "Accepted" |
| "Reviewer-only" | "Verified" |
| "Unverified" | "Official" |
| "Not learner-visible" | "Governing" |
| "Correction preview" | "Current" |
| "Review decision" | "Compliant" |
| "Ready for promotion review" | "AHJ accepted" |
| "Promotion blocked" | "Resource created" |
| "Requires verification" | "Linked" |
| "Requires rights review" | "Approved source" |

## NodeInspector / Learner Impact

**No changes.** External candidates remain invisible to learners.
