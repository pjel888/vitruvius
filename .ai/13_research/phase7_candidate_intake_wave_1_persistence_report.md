# Phase 7 Candidate Intake Wave 1 Persistence Report

Date: 2026-05-06

## Scope

Persist a small reviewer-only source-family candidate wave after delegated Kimi review.

No Resource was created. No nodeResourceLink was created. No candidate was promoted. No learner exposure occurred. No graph/canonical/P0/high-risk P1 mutation occurred. No external verification, source fetch, DOI lookup, ISBN lookup, or protected-content access occurred.

## Persistence Method

Codex used the existing API route:

- `POST /resources/review/external-candidates/preview`
- `POST /resources/review/external-candidates`

The route reran preview validation, rejected placeholder flags, enforced reviewer-only defaults, wrote the candidate registry, and created Resource Layer transaction manifests.

## Persisted Candidates

| Candidate ID | Title | Type | Status | Verification | Display | Learner visible | Manifest |
|---|---|---|---|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | buildingSMART International Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506055128-643fd391aa1d` |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | American Institute of Steel Construction Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506055128-b6cab5af78f9` |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | American Institute of Architects Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506055128-95555ce555b5` |

## Preview Results

Each preview returned:

- `warningFlags`: `minimal_metadata`, `no_stable_identifier`
- `fakePlaceholderFlags`: none
- `learnerVisible`: false

Each preview intentionally retained missing fields:

- URL
- DOI
- ISBN
- authors
- publication date
- edition/version
- jurisdiction/scope

These missing fields are acceptable only because this wave persisted reviewer-only source-family reference candidates. They are blockers for promotion, learner exposure, source verification, and accepted Resource/link creation.

## Registry Counts

| Registry | Before | After |
|---|---:|---:|
| Resources | 7 | 7 |
| nodeResourceLinks | 9 | 9 |
| External metadata candidates | 2 | 5 |

## Next Safe Action

Run focused Resource Layer validation and full validation. Then review or correct the three new source-family candidates before any promotion, Resource creation, nodeResourceLink creation, or learner exposure can be considered.
