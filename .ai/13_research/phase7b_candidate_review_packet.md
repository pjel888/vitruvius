# Phase 7B Candidate Review Packet

**Date:** 2026-05-06
**Reviewer Role:** project-owner-delegated external AI reviewer
**Reviewer Caveat:** This review is not biological human review, not source truth, not external source verification, and not production approval by itself.

## Baseline To Preserve

| Metric | Value |
|---|---:|
| Admitted relationships | 264 |
| Base graph edges | 13,670 |
| Effective graph edges | 13,934 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 |
| Resources | 7 |
| nodeResourceLinks | 9 |
| Resource candidates | 4 |
| External metadata candidates | 2 |

## Safety Constraints

- Do not promote candidates.
- Do not create Resources.
- Do not create nodeResourceLinks.
- Do not auto-link candidates to nodes.
- Do not expose candidates to learners.
- Do not verify or fetch URLs, DOIs, ISBNs, PDFs, books, standards, source-family references, or local files.
- Do not call external APIs.
- Do not invent source metadata, publication metadata, edition/version/scope, jurisdiction, AHJ adoption, compliance status, reachability, verification status, or source truth.
- Do not mutate graph/canonical registries.
- Do not admit graph edges.
- Do not process P0 Concrete/Reinforced Concrete.
- Do not touch high-risk P1 packets.

## Candidate A: ASCE 7

| Field | Value |
|---|---|
| candidateId | `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` |
| title | ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures |
| resourceType | `standard_candidate` |
| sourceType | `professional_body` |
| status | `candidate` |
| verificationStatus | `unverified` |
| displayPolicy | `reviewer_only` |
| learnerVisible | false |
| source metadata | repo-local Resource Layer ASCE candidate/resource/source-family metadata only |
| proposedUrl | `https://asce.org/asce-7` |
| warningFlags | URL syntax accepted; reachability not verified; missing edition/version; missing jurisdiction/scope; standard candidate not learner trusted |
| missingFields | DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |

### Reviewer Questions

1. Is this candidate based only on repo-local metadata?
2. Are edition/version/scope/jurisdiction fields missing?
3. Are any standard-context values fake, placeholder, or overclaimed?
4. Should it remain reviewer-only and unverified?
5. Is the safe next state `standards_context_needed`, `needs_review`, or unchanged `candidate`?
6. Should it be blocked from `ready_for_promotion_review` until real standards context exists?

### Proposed Conservative Decision

`REQUEST_STANDARDS_CONTEXT`, implemented as decisionType `request_standards_context` and nextStatus `standards_context_needed`.

Rationale: edition/version/scope/jurisdiction/source context is missing, so promotion readiness and learner trust would require invented context or external verification, both forbidden for Phase 7B.

## Candidate B: Earth Retaining Structures

| Field | Value |
|---|---|
| candidateId | `ext-cand-earth-retaining-structures-mosyi54y-jp9m` |
| title | Earth Retaining Structures |
| resourceType | `external_url_candidate` |
| sourceType | `government_guidance` |
| status | `candidate` |
| verificationStatus | `unverified` |
| displayPolicy | `reviewer_only` |
| learnerVisible | false |
| source metadata | repo-local Resource Layer FHWA candidate/resource/source-family metadata only |
| proposedUrl | `https://fhwa.dot.gov/engineering/geotech/retaining` |
| warningFlags | URL syntax accepted; reachability not verified |
| missingFields | DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |

### Reviewer Questions

1. Is this candidate based only on repo-local metadata?
2. Is the URL only syntax-accepted, not verified?
3. Are rights/source-custody fields missing or metadata-only?
4. Should it remain reviewer-only and unverified?
5. Is the safe next state `source_custody_review_needed`, `rights_review_needed`, `needs_review`, or unchanged `candidate`?
6. Should it be blocked from `ready_for_promotion_review` until source custody and rights are reviewed?

### Proposed Conservative Decision

`REQUEST_SOURCE_CUSTODY_REVIEW`, implemented as decisionType `request_source_custody_review` and nextStatus `source_custody_review_needed`.

Rationale: repo-local URL/source metadata is candidate-only. URL syntax was accepted during intake, but reachability, source custody, and rights suitability have not been verified.

## Required Reviewer Verdicts

For each candidate, return one of:

- `KEEP_CANDIDATE`
- `MARK_NEEDS_REVIEW`
- `REQUEST_STANDARDS_CONTEXT`
- `REQUEST_SOURCE_CUSTODY_REVIEW`
- `REQUEST_RIGHTS_REVIEW`
- `REQUEST_METADATA_CORRECTION`
- `REJECT_CANDIDATE`
- `READY_FOR_PROMOTION_REVIEW`

`READY_FOR_PROMOTION_REVIEW` is allowed only if all gates pass without invented metadata, external verification, or source-truth claims.
