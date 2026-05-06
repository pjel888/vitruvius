# Phase 7D Delegated Source Check Review Packet

**Date:** 2026-05-06
**Task:** Phase 7D controlled source verification for two reviewer-only external metadata candidates.

## Boundary

- Controlled source checks were limited to official domains for existing candidates.
- No candidate promotion is authorized or requested.
- No Resource creation, nodeResourceLink creation, graph/canonical mutation, learner exposure, protected payload download, DOI/ISBN lookup, API lookup, or broad crawling occurred.
- HTTP reachability is not source truth and does not imply current/governing/compliance/AHJ status.
- Reviewer identity must be recorded as delegated external AI reviewer, not biological human review.

## Baseline

- Branch: `main`, synced to `origin/main` at `ec14d3302166a0f7b2d1541432605984217ebcae` before implementation.
- Resource Layer before checks: 7 resources, 9 nodeResourceLinks, 2 external metadata candidates.
- Graph baseline: 264 admitted relationships, 13,670 base edges, 13,934 effective edges, 0 CROSS_DOMAIN_EQUIVALENT, 22 CROSS_DOMAIN_ALIGNMENT.
- Dirty worktree quarantine: unrelated canonical/source artifacts remain unstaged.

## Implemented Preview/Decision Surface

- Added bounded helper module: `api/resourceLayer/sourceVerification.ts`.
- Added preview routes:
  - `POST /resources/review/external-candidates/:candidateId/source-verification-preview`
  - `POST /resources/review/external-candidates/:candidateId/standards-context-verification-preview`
- Added decision routes:
  - `POST /resources/review/external-candidates/:candidateId/source-verification-decision`
  - `POST /resources/review/external-candidates/:candidateId/standards-context-verification-decision`
- Decision apply writes only `006_System-Manifests/resource-layer/external-metadata-candidates.json` and a Resource Layer transaction manifest.
- Tests use mocked HTTP; live checks are not used in unit tests.

## Controlled Source Check Results

### ASCE 7 Candidate

- Candidate: `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu`
- Prior status: `standards_context_needed`
- Requested URL: `https://asce.org/asce-7`
- Final URL: `https://www.asce.org/publications-and-news/asce-7`
- Official source family: ASCE
- HTTP status: 200
- Content type: `text/html; charset=utf-8`
- Public title metadata captured: `ASCE 7 standard`
- Redirect chain:
  - `https://www.asce.org/asce-7`
  - `https://www.asce.org/publications-and-news/asce-7`
- Protected content downloaded: false
- Payload stored: false
- Missing standards context fields remain:
  - edition
  - version/year
  - scope
  - jurisdiction/applicability caveat
- Proposed conservative status: `standards_context_in_review`
- Blockers: none for official URL reachability; standards completion remains blocked by missing context.

### Earth Retaining Structures Candidate

- Candidate: `ext-cand-earth-retaining-structures-mosyi54y-jp9m`
- Prior status: `source_custody_review_needed`
- Repo-local requested URL: `https://fhwa.dot.gov/engineering/geotech/retaining`
- Repo-local URL result: official FHWA family but connection failed before HTTP response.
- Official equivalent checked: `https://www.fhwa.dot.gov/engineering/geotech/retaining`
- Final URL: `https://www.fhwa.dot.gov/engineering/geotech/retaining/`
- Official source family: FHWA
- HTTP status: 200
- Content type: `text/html;charset=UTF-8`
- Public title metadata captured: `Earth Retaining Structures - Geotech - Bridges & Structures - Federal Highway Administration`
- Protected content downloaded: false
- Payload stored: false
- Alternate official URL checked: `https://highways.dot.gov/engineering/geotech/retaining`
- Alternate official result: 403 `Access Denied`
- Proposed conservative status: `source_custody_in_review`
- Reason not `source_custody_verified`: rights/access review remains incomplete; HTTP success is not source truth.

## Proposed Decisions

| Candidate | Proposed next status | Rationale |
|---|---|---|
| ASCE 7 | `standards_context_in_review` | Official ASCE public landing page was reachable, but required edition/version/scope/applicability context is still missing. No current/governing/AHJ/compliance claim should be made. |
| Earth Retaining Structures | `source_custody_in_review` | Official FHWA `www.fhwa.dot.gov` page was reachable and title metadata matched the candidate, but rights/access/source custody still require reviewer completion. |

## Questions For Delegated Reviewer

1. Were the checks limited to official sources?
2. Was protected content avoided?
3. Are any metadata values invented?
4. Is ASCE 7 still missing required standards context?
5. Is Earth Retaining Structures source custody sufficiently reviewed for `source_custody_in_review` only?
6. Are the proposed status transitions safe?
7. Should any candidate remain blocked at the prior status?
8. Is any learner exposure, promotion, Resource creation, or nodeResourceLink creation implied?

## Required Verdicts

Return one verdict per candidate:

- `KEEP_CURRENT_STATUS`
- `MARK_STANDARDS_CONTEXT_IN_REVIEW`
- `MARK_STANDARDS_CONTEXT_COMPLETE`
- `MARK_STANDARDS_CONTEXT_REJECTED`
- `MARK_SOURCE_CUSTODY_IN_REVIEW`
- `MARK_SOURCE_CUSTODY_VERIFIED`
- `MARK_RIGHTS_REVIEW_NEEDED`
- `MARK_SOURCE_CUSTODY_REJECTED`
- `BLOCK_UNSAFE_METADATA`

Also state files/statuses that must not be staged.
