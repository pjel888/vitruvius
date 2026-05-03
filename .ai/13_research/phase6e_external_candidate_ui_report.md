# Phase 6E External Candidate UI Report

**Generated:** 2026-05-03
**Status:** Implemented

---

## UI Changes

### New Tab: External Candidates

Added to `ResourceReviewAdmin` in `/dev/resource-review`.

**Tab label:** "External Candidates"

**Form fields:**
- Title (required)
- Resource Type dropdown (required)
- URL
- DOI
- ISBN
- Publisher
- Authors (comma-separated)
- Publication Date
- Edition
- Version
- Scope
- Jurisdiction
- Candidate Rationale
- Submitted By

**Safe labels displayed:**
- "Preview only · No auto-verification"
- "Does not create resources, links, or candidates."
- "Unverified candidate"
- "Reviewer-only"
- "Not learner-visible"
- "No external verification performed"

**Unsafe labels avoided:**
- No "verified"
- No "official"
- No "current"
- No "governing"
- No "compliant"
- No "valid DOI" / "valid ISBN"
- No "reachable URL"

**Preview result display:**
- Verification status badge
- Learner visibility badge
- Display policy badge
- Source truth caveat
- Warning flags
- Placeholder flags (if any)
- Missing fields list
- Normalized URL/DOI/ISBN (if valid)
- Full JSON preview

**Behavior:**
- Preview button disabled when admin gate is closed
- Form does not auto-submit
- No apply/admit button
- No resource creation

---

## Component Changes

- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
  - Added `external_candidates` to `ReviewTab` type
  - Added tab to tabs array
  - Added `ExternalCandidatePreviewForm` component
  - Added state for form, preview, and loading
  - Added tab rendering logic

---

## Explorer Test Coverage

- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`
  - External Candidates tab renders with safe wording
  - Form has all required fields
  - No unsafe wording present

---

*No learner exposure. No auto-promotion. No auto-linking.*
