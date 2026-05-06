# Phase 7 Candidate Intake Wave 1

Date: 2026-05-06

## Objective

Evaluate a small post-Phase7D reviewer-only intake wave using only repo-local source-family metadata.

This wave does not promote candidates, create Resources, create nodeResourceLinks, verify sources, fetch URLs, or expose learners.

## Source Scan

Repo-local candidate sources inspected:

- `006_System-Manifests/resource-layer/resource-candidates.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/source-families.json`
- `.ai/13_research/phase7_first_candidate_batch_reviewer_plan.md`

Findings:

- ASCE 7 resource candidates are already represented by `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu`.
- FHWA Earth Retaining Structures is already represented by `ext-cand-earth-retaining-structures-mosyi54y-jp9m`.
- ACI 318 remains rejected/broad and tied to Concrete/Reinforced Concrete scope, so it is not processed in this task.
- Existing accepted Resources are not re-created as external metadata candidates.
- Source-family rows provide safe reviewer-only metadata seeds, but no exact resource URL, edition, publication metadata, node link, or source truth is asserted.

## Proposed Reviewer-Only Candidates

| Proposed title | resourceType | sourceType | proposedPublisher | proposedSourceFamilyId | proposedUrl | proposedNodeIds | Recommendation |
|---|---|---|---|---|---|---|---|
| buildingSMART International Source Family Reference | `source_family_reference` | `official_source_family` | buildingSMART International | `buildingsmart` | none | none | persist reviewer-only candidate if delegated review passes |
| American Institute of Steel Construction Source Family Reference | `source_family_reference` | `professional_body_source_family` | American Institute of Steel Construction | `aisc` | none | none | persist reviewer-only candidate if delegated review passes |
| American Institute of Architects Source Family Reference | `source_family_reference` | `professional_body_source_family` | American Institute of Architects | `aia` | none | none | persist reviewer-only candidate if delegated review passes |

## Candidate Rationale

These are source-family references only. They are intended to seed future reviewer curation of real official resources without inventing exact URLs, editions, source truth, compliance claims, or learner trust.

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
- missing URL
- missing DOI/ISBN
- missing authors/publication date
- missing jurisdiction/scope

These warnings are acceptable for reviewer-only source-family references only if the delegated reviewer agrees that the records are honest intake seeds and not source/resource assertions.

## Blocked Actions

- No Resource creation.
- No nodeResourceLink creation.
- No candidate promotion.
- No learner exposure.
- No graph/canonical mutation.
- No P0 Concrete/Reinforced Concrete work.
- No high-risk P1 work.
- No external URL verification or source fetch.
- No fake URL, DOI, ISBN, edition, publication date, reviewer, source truth, current/governing/compliance, or AHJ claim.
