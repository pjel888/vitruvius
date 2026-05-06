# Phase 7B Candidate State Inspection

**Date:** 2026-05-06
**Source:** `006_System-Manifests/resource-layer/external-metadata-candidates.json`
**Verdict:** TWO PHASE 7A CANDIDATES AVAILABLE FOR REVIEW DECISIONS

## Candidate Summary

| Field | ASCE 7 Candidate | Earth Retaining Structures Candidate |
|---|---|---|
| candidateId | `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` | `ext-cand-earth-retaining-structures-mosyi54y-jp9m` |
| title | ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures | Earth Retaining Structures |
| resourceType | `standard_candidate` | `external_url_candidate` |
| sourceType | `professional_body` | `government_guidance` |
| status | `candidate` | `candidate` |
| verificationStatus | `unverified` | `unverified` |
| displayPolicy | `reviewer_only` | `reviewer_only` |
| learnerVisible | false | false |
| reviewRequired | true | true |
| proposedUrl | `https://asce.org/asce-7` | `https://fhwa.dot.gov/engineering/geotech/retaining` |
| proposedDoi | missing | missing |
| proposedIsbn | missing | missing |
| proposedPublisher | `ASCE` | `FHWA` |
| proposedSourceFamilyId | `asce` | `fhwa` |
| proposedRightsStatus | `standard_landing_page_metadata_only` | `public_government_guidance_metadata_only` |
| proposedNodeIds | `VTN-DOM-0012777`, `VTN-DOM-0012778` | `VTN-DOM-0012799` |
| proposedRelation | `is_supplementary_reference_for` | `provides_design_guidance` |
| decisions history | none recorded before Phase 7B | none recorded before Phase 7B |

## ASCE 7 Candidate Inspection

- Metadata source: repo-local Resource Layer ASCE candidate/resource/source-family metadata captured during Phase 7A.
- Warning flags:
  - URL syntax accepted; reachability not verified.
  - Standard candidate missing edition/version.
  - Standard candidate missing jurisdiction or scope.
  - `standard_candidate_not_learner_trusted`.
- Missing fields:
  - DOI.
  - ISBN.
  - Authors.
  - Publication date.
  - Edition/version.
  - Jurisdiction/scope.
- Safety state:
  - No source verification has been performed.
  - No edition/version/scope/jurisdiction context is admitted.
  - No learner trust is claimed.
  - Candidate should remain blocked from `ready_for_promotion_review` until real standards context is supplied and accepted through the normal gates.

## Earth Retaining Structures Candidate Inspection

- Metadata source: repo-local Resource Layer FHWA candidate/resource/source-family metadata captured during Phase 7A.
- Warning flags:
  - URL syntax accepted; reachability not verified.
- Missing fields:
  - DOI.
  - ISBN.
  - Authors.
  - Publication date.
  - Edition/version.
  - Jurisdiction/scope.
- Safety state:
  - No URL reachability or source custody verification has been performed.
  - Rights status is metadata-only and not a source-truth or content-use finding.
  - Candidate remains reviewer-only and unverified.
  - Candidate should remain blocked from `ready_for_promotion_review` until source custody and rights review are complete.

## Registry Safety

No Resource, nodeResourceLink, graph/canonical registry, P0, or high-risk P1 mutation was observed during inspection.
