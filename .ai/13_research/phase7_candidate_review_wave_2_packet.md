# Phase 7 Candidate Review Wave 2 Packet

**Date:** 2026-05-06
**Reviewer requested:** Kimi delegated external AI reviewer

## Scope

Review the five Phase 7 candidate intake wave 2 source-family references and recommend conservative review decisions only.

Do not promote. Do not create Resources. Do not create nodeResourceLinks. Do not verify URLs. Do not fetch sources. Do not expose learners.

## Current Baseline

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 10
- Learner-visible external metadata candidates: 0
- Graph/canonical mutation: none

## Candidates

| Candidate ID | Title | Status | Verification | Display | Learner visible | Warnings | Missing fields |
|---|---|---|---|---|---|---|---|
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | U.S. Access Board Source Family Reference | `candidate` | `unverified` | `reviewer_only` | false | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | Whole Building Design Guide / NIBS Source Family Reference | `candidate` | `unverified` | `reviewer_only` | false | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | Institution of Structural Engineers Source Family Reference | `candidate` | `unverified` | `reviewer_only` | false | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | Institution of Civil Engineers Source Family Reference | `candidate` | `unverified` | `reviewer_only` | false | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | Royal Institute of British Architects Source Family Reference | `candidate` | `unverified` | `reviewer_only` | false | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |

## Proposed Conservative Decision

Expected safe decision for each candidate:

- decisionType: `mark_needs_review`
- nextStatus: `needs_review`
- rationale: repo-local source-family metadata is useful as an intake seed, but exact source locator, rights/access context, source custody review, and stable identifier are missing. Candidate remains reviewer-only and unverified.
- sourceOfContext: repo-local `source-families.json` metadata and delegated external AI review only; no external verification performed.
- reviewer: `kimi_reviewer`

## Review Questions

1. Is `mark_needs_review` the correct conservative decision for each candidate?
2. Should any candidate be rejected instead?
3. Should any candidate remain `candidate` instead of `needs_review`?
4. Are any candidates ready for promotion review? Expected answer is no unless all gates pass without invented metadata.
5. Does any decision imply source verification, source truth, compliance, current/governing status, jurisdiction/AHJ applicability, learner trust, Resource creation, link creation, or graph/canonical mutation?

## Required Per-Candidate Verdict

Return one verdict per candidate:

- `MARK_NEEDS_REVIEW`
- `KEEP_CANDIDATE`
- `REQUEST_SOURCE_CUSTODY_REVIEW`
- `REQUEST_RIGHTS_REVIEW`
- `REQUEST_METADATA_CORRECTION`
- `REJECT_CANDIDATE`
- `READY_FOR_PROMOTION_REVIEW`
- `BLOCK_UNSAFE_METADATA`

Required caveat:

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.
