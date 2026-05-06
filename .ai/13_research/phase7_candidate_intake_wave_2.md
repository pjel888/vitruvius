# Phase 7 Candidate Intake Wave 2

**Date:** 2026-05-06
**Status:** DELEGATED_REVIEW_PENDING

## Objective

Evaluate a second small reviewer-only intake wave using only repo-local `source-families.json` metadata.

This wave must not promote candidates, create Resources, create nodeResourceLinks, verify sources, fetch URLs, or expose learners.

## Source Scan

Repo-local source-family metadata inspected:

- `006_System-Manifests/resource-layer/source-families.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`

Findings:

- The first source-family intake wave already covers buildingSMART, AISC, and AIA.
- ACI is intentionally skipped because it is too close to Concrete/Reinforced Concrete and standards-context blockers.
- ASCE and FHWA already have dedicated Phase 7 candidates.
- The following five source-family rows have real repo-local labels, source-family ids, organizations, authority context, disciplines, domains, and caveat notes, but no exact reviewed source URL.

## Proposed Reviewer-Only Candidates

| Proposed title | resourceType | sourceType | proposedPublisher | proposedSourceFamilyId | proposedUrl | proposedNodeIds | Recommendation |
|---|---|---|---|---|---|---|---|
| U.S. Access Board Source Family Reference | `source_family_reference` | `government_source_family` | U.S. Access Board | `us_access_board` | none | none | persist reviewer-only candidate if delegated review passes |
| Whole Building Design Guide / NIBS Source Family Reference | `source_family_reference` | `government_guidance_source_family` | National Institute of Building Sciences / Whole Building Design Guide | `wbdg_nibs` | none | none | persist reviewer-only candidate if delegated review passes |
| Institution of Structural Engineers Source Family Reference | `source_family_reference` | `professional_body_source_family` | Institution of Structural Engineers | `istructe` | none | none | persist reviewer-only candidate if delegated review passes |
| Institution of Civil Engineers Source Family Reference | `source_family_reference` | `professional_body_source_family` | Institution of Civil Engineers | `ice` | none | none | persist reviewer-only candidate if delegated review passes |
| Royal Institute of British Architects Source Family Reference | `source_family_reference` | `professional_body_source_family` | Royal Institute of British Architects | `riba` | none | none | persist reviewer-only candidate if delegated review passes |

## Candidate Rationale

These are source-family references only. They seed future curation of real official resources without inventing exact URLs, editions, source truth, compliance claims, AHJ/jurisdiction claims, or learner trust.

Each candidate must persist as:

- `verificationStatus: unverified`
- `displayPolicy: reviewer_only`
- `learnerVisible: false`
- `reviewRequired: true`
- `noAutoVerification: true`
- `noAutoPromotion: true`
- `noAutoLinking: true`
- `noLearnerExposure: true`

## Expected Warnings

- minimal metadata
- no stable identifier
- missing exact URL
- missing DOI/ISBN
- missing authors/publication date
- missing edition/version
- missing jurisdiction/scope

These warnings are acceptable only for reviewer-only source-family reference intake and remain blockers for promotion, learner exposure, source verification completion, and accepted Resource/link creation.

## Blocked Actions

- No Resource creation.
- No nodeResourceLink creation.
- No candidate promotion.
- No learner exposure.
- No graph/canonical mutation.
- No P0 Concrete/Reinforced Concrete work.
- No high-risk P1 work.
- No external URL verification or source fetch.
- No fake URL, DOI, ISBN, edition, publication date, reviewer, source truth, current/governing/compliance, jurisdiction, or AHJ claim.
