# Phase 7 Candidate Review Wave 1 Packet

Date: 2026-05-06

Reviewer requested: Kimi delegated external AI reviewer.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Objective

Review the three Phase 7 candidate intake wave 1 source-family reference candidates and choose the safest status decision for each.

No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external source verification, URL fetch, DOI lookup, ISBN lookup, protected content access, or source-truth claim is authorized in this review wave.

## Current Registry Baseline

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 5
- Graph baseline: admitted relationships 264, base edges 13,670, effective edges 13,934, CROSS_DOMAIN_EQUIVALENT 0, CROSS_DOMAIN_ALIGNMENT 22

## Candidates Under Review

| Candidate ID | Title | Type | Current status | Warnings | Missing fields |
|---|---|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | buildingSMART International Source Family Reference | `source_family_reference` | `candidate` | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publicationDate, edition/version, jurisdiction/scope |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | American Institute of Steel Construction Source Family Reference | `source_family_reference` | `candidate` | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publicationDate, edition/version, jurisdiction/scope |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | American Institute of Architects Source Family Reference | `source_family_reference` | `candidate` | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publicationDate, edition/version, jurisdiction/scope |

## Repo-Local Metadata Source

All three candidates come only from `006_System-Manifests/resource-layer/source-families.json`.

The source-family rows contain:

- source-family ID
- label
- domains
- organizations
- authority class
- disciplines
- typical resource types
- jurisdiction caveat
- notes

The candidates intentionally do not include exact source URLs. Domain lists are not exact source URLs and were not converted into URLs.

## Possible Decisions

Use one verdict per candidate:

- `KEEP_CANDIDATE`
- `MARK_NEEDS_REVIEW`
- `REQUEST_METADATA_CORRECTION`
- `REQUEST_SOURCE_CUSTODY_REVIEW`
- `REQUEST_RIGHTS_REVIEW`
- `REJECT_CANDIDATE`
- `BLOCK_UNSAFE_METADATA`

Expected conservative decision:

- `REQUEST_SOURCE_CUSTODY_REVIEW` if these source-family seeds need exact source locator, rights/access, and custody review before any future source verification or promotion readiness.
- `REQUEST_METADATA_CORRECTION` if the lack of exact source identity means metadata correction is required before source-custody review can begin.
- `MARK_NEEDS_REVIEW` if both apply but the safest generic queue state is preferred.

Do not recommend `ready_for_promotion_review`.

## Questions

1. Are the three candidates based only on repo-local metadata?
2. Is any candidate fake, placeholder, or unsafe even as reviewer-only metadata?
3. Is the lack of exact source URL/locator acceptable for a `source_family_reference` candidate?
4. Which status should each candidate move to?
5. Are any Resource, nodeResourceLink, promotion, learner exposure, source-truth, governing/current/compliance/AHJ, or external verification claims implied?
