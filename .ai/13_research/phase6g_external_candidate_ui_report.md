# Phase 6G External Candidate UI Report

**Generated:** 2026-05-03T01:00:00+08:00

---

## UI Changes

### External Candidates Tab (`ResourceReviewAdmin.tsx`)

**New save button:**
- Appears only after valid preview (no errors, no placeholder flags)
- Label: "Save as reviewer-only candidate"
- Disabled when admin gate is closed
- Disabled while saving

**Save status message:**
- Success: green banner with candidate ID
- Error: red banner with error message

**Ready-to-save indicator:**
- Blue info box: "This candidate passes validation and contains no placeholders. It will be stored as unverified, reviewer-only metadata. No resource or link will be created."

**Persisted candidates list:**
- Appears below the preview form
- Shows count of persisted external candidates
- Each card shows:
  - Title
  - verificationStatus badge (warning)
  - learnerVisible badge (danger: "not learner visible")
  - resourceType · candidateId
  - warning flags as amber chips

### Safe Wording

- "Save as reviewer-only candidate"
- "Reviewer-only candidate"
- "Unverified"
- "Not learner-visible"
- "No external verification performed"
- "Does not create resources, links, or accepted candidates."
- "Requires future source-custody review"

### Unsafe Wording Absent

No "verified", "official", "current", "governing", "accepted", "compliant", "valid DOI", "valid ISBN", "reachable URL".

---

## API Client Updates (`graphApi.ts`)

- `persistExternalMetadataCandidate(body)` — POST /resources/review/external-candidates
- `listExternalMetadataCandidates(status?, resourceType?)` — GET /resources/review/external-candidates
- `getExternalMetadataCandidate(candidateId)` — GET /resources/review/external-candidates/:candidateId

---

## Type Updates (`types/index.ts`)

- `ExternalMetadataCandidateRecord` — persisted record type extending preview
