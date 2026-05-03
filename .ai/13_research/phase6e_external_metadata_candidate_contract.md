# Phase 6E External Metadata Candidate Contract

**Generated:** 2026-05-03
**Status:** Implemented

---

## Purpose

Define a candidate-only metadata contract for external URLs, books, PDFs, standards, guides, articles, datasets, and source-family references. All fields are **proposed metadata only**. No field is source truth until reviewed.

---

## Candidate Resource Types

| Type | Description |
|------|-------------|
| `external_url_candidate` | Web-based resource (guide, article, report) |
| `book_candidate` | Published book or textbook |
| `pdf_candidate` | PDF document (online or local) |
| `standard_candidate` | Engineering/building standard or code |
| `guide_candidate` | Professional guidance document |
| `article_candidate` | Academic or technical article |
| `dataset_candidate` | Structured dataset or corpus |
| `source_family_reference` | Reference to a known source family |

---

## Candidate Fields

### Required
- `title` — Resource title (string)
- `resourceType` — One of the candidate types above

### Optional Proposed Metadata
- `sourceType` — Subtype or category
- `proposedUrl` — Proposed URL (http/https only)
- `proposedDoi` — Proposed DOI (syntax check only)
- `proposedIsbn` — Proposed ISBN-10/ISBN-13 (syntax check only)
- `proposedPublisher` — Publisher name
- `proposedAuthors` — Array of author names
- `proposedPublicationDate` — Date or year
- `proposedEdition` — Edition string
- `proposedVersion` — Version string
- `proposedScope` — Geographic or topical scope
- `proposedJurisdiction` — Jurisdiction
- `proposedSourceFamilyId` — Source family association
- `proposedRightsStatus` — Rights status (cannot be pre-accepted)
- `proposedNodeIds` — Proposed node link targets
- `proposedRelation` — Proposed node relationship
- `candidateRationale` — Why this resource is being proposed
- `submittedBy` — Submitter identifier

---

## Output Fields (Preview)

- `candidateId` — Generated ephemeral ID
- `verificationStatus` — Always `unverified`
- `displayPolicy` — Always `reviewer_only` or `dev_only`
- `learnerVisible` — Always `false`
- `reviewRequired` — Always `true`
- `warningFlags` — Array of warning strings
- `missingFields` — Array of missing field names
- `fakePlaceholderFlags` — Array of detected placeholder flags
- `sourceTruthCaveat` — Human-readable disclaimer
- `normalizedUrl` — Canonicalized URL if valid
- `normalizedDoi` — Normalized DOI if valid
- `normalizedIsbn` — Normalized ISBN if valid

---

## Validation Rules

### URL Candidates
- Syntactically valid http/https only
- Reject placeholder domains (example.com, localhost, test, tbd, placeholder, current, latest, unknown)
- Do not claim reachability

### DOI Candidates
- DOI syntax only (`10.xxxx/xxxx`)
- Reject placeholder values
- Do not claim existence

### ISBN Candidates
- ISBN-10/ISBN-13 syntax with valid check digit
- Reject placeholder values
- Do not claim existence

### Book/PDF Candidates
- Require title
- Rights status cannot be pre-accepted or pre-verified
- Default `verificationStatus`: `unverified`
- Default `displayPolicy`: `reviewer_only`
- Default `learnerVisible`: `false`

### Standards Candidates
- Missing edition/version/scope is allowed only as candidate/reviewer-only
- Cannot be learner-trusted
- Cannot be accepted/promoted
- Placeholder context values rejected
- No current/governing/compliance wording

---

## Constraints

| Constraint | Enforcement |
|------------|-------------|
| No auto-verification | `verificationStatus` is always `unverified` |
| No auto-promotion | `reviewRequired` is always `true` |
| No auto-linking | `proposedNodeIds` are suggestions only |
| No learner exposure | `learnerVisible` is always `false` |
| No fake sources | Placeholder detection rejects fake metadata |
| No external fetching | Preview does not call external URLs |

---

*Contract implemented in `api/resourceLayer/externalMetadataCandidates.ts`.*
