# Phase 6E External Metadata Validation Rules

**Generated:** 2026-05-03
**Status:** Implemented

---

## Validation Functions

### `validateExternalMetadataCandidate(input)`
Returns `{ ok, errors, warnings }`.

**URL Validation:**
- `canonicalizeUrl()` normalizes URL
- Reject if normalization fails
- Reject placeholder domains
- Reject non-http/https schemes

**DOI Validation:**
- `normalizeDoi()` extracts DOI syntax
- Reject if normalization fails
- Reject placeholder DOI patterns

**ISBN Validation:**
- `normalizeIsbn()` validates check digit
- Reject if normalization fails
- Reject placeholder ISBN patterns

**Standard-Specific:**
- Warn if missing edition/version
- Warn if missing jurisdiction/scope
- Error if placeholder edition/version

**Rights Status:**
- Error if `proposedRightsStatus` is `accepted` or `verified`

---

## Placeholder Detection

### `detectExternalMetadataPlaceholders(input)`
Returns array of flag strings:
- `placeholder_url` — placeholder or test domain
- `placeholder_doi` — placeholder DOI value
- `placeholder_isbn` — placeholder ISBN value
- `placeholder_edition` — placeholder edition string
- `placeholder_version` — placeholder version string
- `placeholder_publisher` — placeholder publisher name
- `placeholder_author` — placeholder author name

**Placeholder values detected:**
- `tbd`, `to be determined`, `unknown`, `generic`, `latest`, `current`, `placeholder`, `sample`, `example`, `varies`, `n/a`
- ISBN patterns: `0000000000`, `1111111111`, `1234567890`, `9876543210`

---

## Classification

### `classifyExternalCandidate(input)`
Returns `{ classification, completenessScore }`.

**Classifications:**
- `url_heavy` — has URL but no DOI/ISBN
- `identifier_heavy` — has DOI/ISBN but no URL
- `metadata_heavy` — score >= 4 with rich metadata
- `minimal` — score < 4

---

## Normalization

### `normalizeExternalCandidateInput(input)`
Applies:
- `canonicalizeUrl()` to `proposedUrl`
- `normalizeDoi()` to `proposedDoi`
- `normalizeIsbn()` to `proposedIsbn`
- Trims all string fields
- Removes empty values

---

## Preview Builder

### `buildExternalCandidatePreview(input)`
Pure function. Returns complete preview object with:
- Normalized input
- Validation results
- Warning flags
- Missing fields list
- Placeholder flags
- Source truth caveat
- Fixed defaults (`unverified`, `reviewer_only`, `false`)

**Does NOT:**
- Write files
- Create resources
- Create nodeResourceLinks
- Create candidates
- Create transaction manifests
- Fetch external URLs
- Call external APIs

---

*Validation rules implemented in `api/resourceLayer/externalMetadataCandidates.ts`.*
