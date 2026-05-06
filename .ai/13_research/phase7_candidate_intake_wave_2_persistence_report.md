# Phase 7 Candidate Intake Wave 2 Persistence Report

**Date:** 2026-05-06
**Status:** VALIDATION_PASSED_COMMIT_PENDING

## Scope

Persist a small reviewer-only source-family candidate wave after delegated Kimi review.

No Resource was created. No nodeResourceLink was created. No candidate was promoted. No learner exposure occurred. No graph/canonical/P0/high-risk P1 mutation occurred. No external verification, source fetch, DOI lookup, ISBN lookup, book API, PDF fetch, protected-content access, source-truth claim, current/governing/compliance claim, jurisdiction claim, or AHJ claim occurred.

## Persistence Method

Codex used the existing API routes:

- `POST /resources/review/external-candidates/preview`
- `POST /resources/review/external-candidates`

The route reran preview validation, rejected placeholder flags, enforced reviewer-only defaults, wrote the candidate registry, and created Resource Layer transaction manifests.

## Persisted Candidates

| Candidate ID | Title | Type | Status | Verification | Display | Learner visible | Manifest |
|---|---|---|---|---|---|---|---|
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | U.S. Access Board Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506063353-260dec15d952` |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | Whole Building Design Guide / NIBS Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506063353-57c569c64e89` |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | Institution of Structural Engineers Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506063353-eaf2307d2346` |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | Institution of Civil Engineers Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506063353-f7c656c0d026` |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | Royal Institute of British Architects Source Family Reference | `source_family_reference` | `candidate` | `unverified` | `reviewer_only` | false | `resource-layer-tx-20260506063353-ca1f4473ec6d` |

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

These missing fields are acceptable only because this wave persisted reviewer-only source-family reference candidates. They remain blockers for promotion, learner exposure, source verification completion, accepted Resource creation, and nodeResourceLink creation.

## Registry Counts

| Registry | Before | After |
|---|---:|---:|
| Resources | 7 | 7 |
| nodeResourceLinks | 9 | 9 |
| External metadata candidates | 5 | 10 |
| Learner-visible external metadata candidates | 0 | 0 |

## Next Safe Action

Run candidate review/correction decisions for the five new wave 2 source-family candidates, most likely marking them `needs_review` until exact source locators, rights/access context, and source-custody review exist. Do not promote, create Resources, create nodeResourceLinks, verify URLs, or expose learners.
