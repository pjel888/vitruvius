# Phase 7C Source-Custody Verification Workflow

**Date:** 2026-05-06
**Workflow:** Source-custody and rights review for external source candidates
**Initial target:** Earth Retaining Structures candidate
**Status:** PLANNED_ONLY

## Boundary

This workflow is a future design. Phase 7C did not fetch a URL, check reachability, inspect protected content, verify rights, create a Resource, create a nodeResourceLink, promote a candidate, or expose anything to learners.

## Purpose

External source candidates can move forward only when source identity, rights/access posture, source family, reviewer rationale, and custody evidence are explicitly reviewed. Syntax-valid locators are treated as candidate metadata only, not verification.

## Verification Stages

| Stage | Meaning |
|---|---|
| `metadata_review` | Candidate identity fields are checked against repo-local or steward-supplied metadata. |
| `rights_review` | Rights/access status is reviewed without copying protected content. |
| `reachability_check_pending` | Future reachability check is queued but not performed. |
| `source_custody_verified` | Source identity and custody fields are reviewed with a recorded sourceOfContext. |
| `source_custody_rejected` | Source identity, rights, or custody is unsupported or unsafe. |
| `verification_deferred` | Required verification is not authorized or not available. |

## Required Fields

Every source-custody decision must provide:

| Field | Requirement |
|---|---|
| `title` | Candidate title from repo-local or steward-supplied metadata. |
| `sourceLocator` | URL/source locator if already available; absence must be explicit. |
| `sourceFamily` | Source family or provenance family being reviewed. |
| `rightsStatus` | Explicit rights status or explicit rights uncertainty. |
| `accessType` | Public, restricted, local custody, protected, unknown, or another allowed enum. |
| `sourceOfContext` | Repo-local record, steward-supplied source note, or separately authorized verification artifact. |
| `reviewer` | Honest reviewer identity; delegated AI must not be recorded as biological-human review. |
| `rationale` | Why custody is verified, rejected, deferred, or still incomplete. |
| `reviewedAt` | Timestamp of the review decision. |

## Future Optional Checks

These checks require separate explicit authorization before use:

- URL reachability
- content-type check
- source family match
- title match
- rights/access review

No optional check may claim source truth by itself.

## Hard Rules

- Syntax-valid URL is not verification.
- HTTP success is not source truth by itself.
- A reachable URL does not establish title match, edition match, rights, currentness, compliance, or learner trust.
- Source verification does not imply learner trust.
- Protected content must not be copied into Resource Layer records.
- A candidate must remain reviewer-only until a separate promotion workflow is authorized and passes.

## Earth Retaining Structures Starting State

| Field | Current State |
|---|---|
| Candidate ID | `ext-cand-earth-retaining-structures-mosyi54y-jp9m` |
| Status | `source_custody_review_needed` |
| Verification | `unverified` |
| Display policy | `reviewer_only` |
| Learner visible | false |
| Current blocker | URL/source metadata is candidate-only; reachability, rights, and custody are not verified |

## Output Rules

- Candidate remains reviewer-only.
- Verification remains `unverified` unless a separately authorized workflow records a stronger review result.
- No Resource is created.
- No nodeResourceLink is created.
- No candidate is promoted.
- No learner exposure occurs.
- No graph/canonical registry is mutated.
- No P0 Concrete/Reinforced Concrete or high-risk P1 packet work is allowed.

## Future Acceptance Criteria

A future implementation is acceptable only if tests prove sourceOfContext/reviewer/rationale enforcement, rights/access gating, syntax-only URL non-verification, no external fetch without explicit authorization, transaction-manifest-backed decisions, append-only decision history, rollback behavior, and learner endpoint hiding.
