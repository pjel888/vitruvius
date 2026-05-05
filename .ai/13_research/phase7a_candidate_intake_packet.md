# Phase 7A Candidate Intake Packet For Delegated Reviewer

**Date:** 2026-05-06
**Prepared for:** Project-owner-delegated external AI reviewer

This packet asks for safety review only. It is not source verification, not biological human review, not source truth, and not production approval by itself.

## Baseline Metrics

| Metric | Value |
|---|---:|
| Admitted relationships | 264 |
| Base graph edges | 13,670 |
| Effective graph edges | 13,934 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 |
| Production resources | 7 |
| Production nodeResourceLinks | 9 |
| Resource candidates | 4 |
| External metadata candidates | 0 |
| Local files indexed/admitted | 25 / 0 |
| Standards missing/blocked | 2 / 3 |

## Dirty Worktree Quarantine

- Existing unrelated dirty entries remain quarantined and unstaged.
- No unsafe untracked executable scripts were found.
- No production Resource Layer registry was dirty before candidate persistence.
- No graph-canonical registry was dirty.
- No `003_Canonical-Knowledge-Layer` artifacts are staged.

## Safety Constraints

- Do not create Resources.
- Do not create nodeResourceLinks.
- Do not promote candidates.
- Do not expose candidates to learners.
- Do not verify URLs, DOIs, ISBNs, books, PDFs, standards, source-family references, or local files.
- Do not fetch external sources or call external APIs.
- Do not invent metadata, standards context, jurisdiction, AHJ adoption, compliance status, or source truth.
- Do not mutate graph/canonical registries or admit graph edges.
- Do not process P0 Concrete/Reinforced Concrete or high-risk P1 packets.

## Candidate Proposals

### P1 - ASCE 7 Reviewer-Only Standard Candidate

| Field | Value |
|---|---|
| title | ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures |
| candidateType/resourceType | `standard_candidate` |
| sourceType | `professional_body` |
| proposedUrl | `https://www.asce.org/asce-7` |
| proposedPublisher | `ASCE` |
| proposedSourceFamilyId | `asce` |
| proposedRightsStatus | `standard_landing_page_metadata_only` |
| proposedNodeIds | `VTN-DOM-0012777`, `VTN-DOM-0012778` |
| proposedRelation | `is_supplementary_reference_for` |
| metadata source | `resource-candidates.json`, `resources.json`, `source-families.json` |
| recommendation | `persist_reviewer_only_candidate` |

Rationale: repo-local candidate/resource metadata already names this source for wind-load and seismic-load needs-review records. Persist only as unverified reviewer-only metadata because edition/version/scope/adoption context is missing.

Warnings: standard candidate not learner trusted; edition/version missing; jurisdiction/scope missing; URL syntax only; reachability not verified in this task.

### P2 - FHWA Earth Retaining Structures Reviewer-Only Candidate

| Field | Value |
|---|---|
| title | Earth Retaining Structures |
| candidateType/resourceType | `external_url_candidate` |
| sourceType | `government_guidance` |
| proposedUrl | `https://www.fhwa.dot.gov/engineering/geotech/retaining/` |
| proposedPublisher | `FHWA` |
| proposedSourceFamilyId | `fhwa` |
| proposedRightsStatus | `public_government_guidance_metadata_only` |
| proposedNodeIds | `VTN-DOM-0012799` |
| proposedRelation | `provides_design_guidance` |
| metadata source | `resource-candidates.json`, `resources.json`, `source-families.json` |
| recommendation | `persist_reviewer_only_candidate` |

Rationale: repo-local candidate/resource metadata already identifies this source for the retaining-wall review queue. Persist only as unverified reviewer-only metadata because the scope remains U.S. federal transportation/geotechnical context and no learner trust is claimed.

Warnings: URL syntax only; reachability not verified; node mapping remains review-only.

### D1 - AISC Source Family Reference

| Field | Value |
|---|---|
| title | American Institute of Steel Construction source family reference |
| candidateType/resourceType | `source_family_reference` |
| sourceType | `professional_body` |
| proposedPublisher | `American Institute of Steel Construction` |
| proposedSourceFamilyId | `aisc` |
| metadata source | `source-families.json` |
| recommendation | `defer_missing_metadata` |

Rationale: this source-family metadata is real and repo-local, but it lacks a specific candidate resource URL, DOI, ISBN, publication title, edition, or rights record. Defer until the project owner supplies a specific candidate or authorizes a separate verification/source-discovery workflow.

## Reviewer Questions

1. Are the candidates based only on actual repo-provided metadata?
2. Are any URLs/DOIs/ISBNs fake or placeholder-looking?
3. Are any standard edition/version/scope values invented?
4. Are any candidates unsafe to persist even as reviewer-only?
5. Which candidates may be persisted as unverified reviewer-only external metadata candidates?
6. Which candidates should be deferred or rejected?
7. Does any candidate imply source verification, compliance, current/governing status, AHJ adoption, or learner trust?
8. Is Phase 7A candidate intake safe?

## Required Verdict

Return exactly one verdict:

- `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`
- `PASS_ZERO_CANDIDATES_INTAKE_READY`
- `DEFER_MISSING_METADATA`
- `BLOCK_FAKE_OR_UNSAFE_METADATA`
- `NEEDS_PROJECT_OWNER_METADATA`
