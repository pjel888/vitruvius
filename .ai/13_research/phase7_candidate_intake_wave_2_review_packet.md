# Phase 7 Candidate Intake Wave 2 Review Packet

**Date:** 2026-05-06
**Reviewer requested:** Kimi delegated external AI reviewer

## Current Baseline

- Admitted relationships: 264
- Base graph edges: 13,670
- Effective graph edges: 13,934
- CROSS_DOMAIN_EQUIVALENT: 0
- CROSS_DOMAIN_ALIGNMENT: 22
- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 5
- Learner-visible external candidates: 0

## Proposed Candidates

| Title | Source-family id | Publisher/organization from repo | Authority from repo | Domains from repo | Caveat |
|---|---|---|---|---|---|
| U.S. Access Board Source Family Reference | `us_access_board` | U.S. Access Board | government | `access-board.gov` | Accessibility guidance/standards landing pages; no universal compliance claim without adopted-code context |
| Whole Building Design Guide / NIBS Source Family Reference | `wbdg_nibs` | National Institute of Building Sciences; Whole Building Design Guide | government | `wbdg.org`, `nibs.org` | Contextual interdisciplinary building performance guidance, not a primary standard by itself |
| Institution of Structural Engineers Source Family Reference | `istructe` | Institution of Structural Engineers | professional_body | `istructe.org` | UK professional-body context; no universal governance claim |
| Institution of Civil Engineers Source Family Reference | `ice` | Institution of Civil Engineers | professional_body | `ice.org.uk`, `knowledgehub.ice.org.uk` | UK professional education/guidance context; not universal code authority |
| Royal Institute of British Architects Source Family Reference | `riba` | Royal Institute of British Architects | professional_body | `architecture.com` | UK architectural professional context |

## Metadata Source

All candidate metadata comes from `006_System-Manifests/resource-layer/source-families.json`.

No external source was fetched. No URL was checked. No DOI/ISBN/book/PDF/standards API was called. No exact source URL is asserted.

## Proposed Persistence Defaults

- status: `candidate`
- verificationStatus: `unverified`
- displayPolicy: `reviewer_only`
- learnerVisible: false
- reviewRequired: true
- noAutoVerification: true
- noAutoPromotion: true
- noAutoLinking: true
- noLearnerExposure: true

## Review Questions

1. Are these candidates based only on actual repo-local metadata?
2. Are any URLs, DOIs, ISBNs, editions, publication dates, compliance claims, source-truth claims, or AHJ/jurisdiction claims invented?
3. Are any candidates unsafe to persist even as reviewer-only source-family references?
4. Which candidates may be persisted as unverified reviewer-only external metadata candidates?
5. Which candidates should be deferred or rejected?
6. Is Phase 7 candidate intake wave 2 safe?

## Required Verdict

Return one of:

- `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`
- `PASS_ZERO_CANDIDATES_INTAKE_READY`
- `DEFER_MISSING_METADATA`
- `BLOCK_FAKE_OR_UNSAFE_METADATA`
- `NEEDS_PROJECT_OWNER_METADATA`

Required caveat:

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.
