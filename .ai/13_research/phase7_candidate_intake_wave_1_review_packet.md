# Phase 7 Candidate Intake Wave 1 Review Packet

Date: 2026-05-06

Reviewer requested: Kimi delegated external AI reviewer.

This is a project-owner-delegated external AI review request, not a biological human review request, not source truth, and not production approval by itself.

## Baseline

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates before wave: 2
- ASCE 7 candidate: `standards_context_in_review`, reviewer-only, unverified, learner-hidden
- Earth Retaining Structures candidate: `source_custody_in_review`, reviewer-only, unverified, learner-hidden
- Graph baseline unchanged: admitted relationships 264, base edges 13,670, effective edges 13,934, CROSS_DOMAIN_EQUIVALENT 0, CROSS_DOMAIN_ALIGNMENT 22

## Review Question

Can the following three source-family references be persisted as reviewer-only external metadata candidates using only repo-local `source-families.json` metadata?

The proposed candidates intentionally omit URLs because no exact source/resource URL is present in the source-family rows. They are not Resources, not links, not verified sources, not learner-visible evidence, and not promotion-ready.

## Proposed Candidates

1. buildingSMART International Source Family Reference
   - resourceType: `source_family_reference`
   - sourceType: `official_source_family`
   - proposedPublisher: buildingSMART International
   - proposedSourceFamilyId: `buildingsmart`
   - metadata source: `006_System-Manifests/resource-layer/source-families.json`

2. American Institute of Steel Construction Source Family Reference
   - resourceType: `source_family_reference`
   - sourceType: `professional_body_source_family`
   - proposedPublisher: American Institute of Steel Construction
   - proposedSourceFamilyId: `aisc`
   - metadata source: `006_System-Manifests/resource-layer/source-families.json`

3. American Institute of Architects Source Family Reference
   - resourceType: `source_family_reference`
   - sourceType: `professional_body_source_family`
   - proposedPublisher: American Institute of Architects
   - proposedSourceFamilyId: `aia`
   - metadata source: `006_System-Manifests/resource-layer/source-families.json`

## Safety Constraints

- Persist only if reviewer-only source-family references are acceptable despite missing stable URL/identifier.
- Do not invent URLs from domain names.
- Do not verify external sources.
- Do not create Resources.
- Do not create nodeResourceLinks.
- Do not promote candidates.
- Do not expose candidates to learners.
- Do not mutate graph/canonical registries.
- Do not touch P0 Concrete/Reinforced Concrete or high-risk P1 packets.

## Requested Verdict

Return one verdict:

- `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`
- `PASS_ZERO_CANDIDATES_INTAKE_READY`
- `DEFER_MISSING_METADATA`
- `BLOCK_FAKE_OR_UNSAFE_METADATA`
- `NEEDS_PROJECT_OWNER_METADATA`

Also identify any candidate that must be removed before persistence.
