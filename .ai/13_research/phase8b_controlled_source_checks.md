# Phase 8B Controlled Source Checks

Checked at: 2026-05-06T17:10:32.7077958+08:00

Checks used the existing local API preview routes, which perform bounded official-source checks and write no registry files.

## ASCE 7

Command/API route:

- `POST /resources/review/external-candidates/ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu/standards-context-verification-preview`
- Body: `{ "requestedUrl": "https://asce.org/asce-7" }`

Result:

- HTTP status from route: 200
- requestedUrl: `https://asce.org/asce-7`
- finalUrl: `https://www.asce.org/publications-and-news/asce-7`
- source HTTP status: 200
- contentType: `text/html; charset=utf-8`
- title: `ASCE 7 standard`
- officialSourceFamilyMatch: true
- sourceFamily: `asce`
- protectedContentDownloaded: false
- contentPayloadStored: false
- proposedNextStatus: `standards_context_in_review`
- missingFields:
  - edition
  - version/year
  - scope
  - jurisdiction/applicability caveat
- caveats:
  - HTTP success is not source truth.
  - This check does not establish current/governing/compliance/AHJ status or learner trust.

Forced completion probe:

- `nextStatus: standards_context_complete` returned blockers:
  - `standards_context_complete requires: edition, version/year, scope, jurisdiction/applicability caveat`
  - `standards_context_complete requires sourceOfContext`
  - `standards_context_complete requires reviewer`
  - `standards_context_complete requires rationale`

Conclusion: ASCE 7 remains blocked for standards-context completion and promotion. Do not promote or create links.

## FHWA Earth Retaining Structures

Command/API route:

- `POST /resources/review/external-candidates/ext-cand-earth-retaining-structures-mosyi54y-jp9m/source-verification-preview`
- Body: `{ "requestedUrl": "https://www.fhwa.dot.gov/engineering/geotech/retaining/" }`

Result:

- HTTP status from route: 200
- requestedUrl: `https://www.fhwa.dot.gov/engineering/geotech/retaining/`
- finalUrl: `https://www.fhwa.dot.gov/engineering/geotech/retaining/`
- source HTTP status: 200
- contentType: `text/html;charset=UTF-8`
- title: `Earth Retaining Structures - Geotech - Bridges &amp; Structures - Federal Highway Administration`
- officialSourceFamilyMatch: true
- sourceFamily: `fhwa`
- protectedContentDownloaded: false
- contentPayloadStored: false
- proposedNextStatus: `source_custody_in_review`
- blockers: none
- caveats:
  - HTTP success is not source truth.
  - This check does not establish current/governing/compliance/AHJ status or learner trust.

Verified-with-repo-rights no-write probe:

- Body included:
  - `nextStatus: source_custody_verified`
  - `rightsStatus: public_government_guidance`
  - `accessType: public_web`
  - `rightsAssessmentRationale`: repo-local Resource `res-fhwa-earth-retaining-structures` states public government page metadata/rationale only, no copied payload text.
- Result:
  - proposedNextStatus: `source_custody_verified`
  - blockers: none

Conclusion: Source custody could be advanced on rights/access grounds, but the candidate duplicates existing Resource `res-fhwa-earth-retaining-structures`. The safer disposition is duplicate-candidate status rather than creating a second Resource.

## Source-Family Reference Candidates

The 10 source-family reference candidates have source-family domains but no exact candidate URL/source locator. Per Phase 8B rule, source-family candidates require an official source-family locator; a domain alone is insufficient for Resource creation or source custody verification.

Conclusion: Mark as blocked for missing exact locator/stable identifier/source custody metadata; do not fetch homepage guesses, create Resources, create links, or promote.
