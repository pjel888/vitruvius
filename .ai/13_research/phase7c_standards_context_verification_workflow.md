# Phase 7C Standards-Context Verification Workflow

**Date:** 2026-05-06
**Workflow:** Standards context review for external metadata candidates
**Initial target:** ASCE 7 candidate
**Status:** PLANNED_ONLY

## Boundary

This workflow is a future design. Phase 7C did not complete ASCE 7 context, verify an edition, assert a jurisdiction, create a Resource, create a nodeResourceLink, promote a candidate, or expose anything to learners.

## Purpose

Standard-like candidates can move forward only when their edition, version/year, scope, applicability caveat, and source-of-context are explicitly reviewed. The workflow prevents placeholder context such as "latest" or "current" from being treated as source truth.

## Required Fields

Every standards-context decision must provide:

| Field | Requirement |
|---|---|
| `standardTitle` | Exact title being reviewed. |
| `edition` | Explicit edition label from the reviewed source context. |
| `versionYear` | Explicit year/version where applicable. |
| `scope` | Scope of use being claimed by the reviewer. |
| `jurisdictionApplicabilityCaveat` | Caveat that no AHJ/jurisdiction applicability is implied unless directly reviewed. |
| `sourceOfContext` | Repo-local record, steward-supplied source note, or separately authorized verification artifact. |
| `reviewer` | Honest reviewer identity; delegated AI must not be recorded as biological-human review. |
| `rationale` | Why the context is complete, rejected, or still missing. |
| `reviewedAt` | Timestamp of the review decision. |

## Forbidden Placeholder Values

The following values must be rejected case-insensitively in edition, version/year, scope, sourceOfContext, rationale, and applicability fields:

- `latest`
- `current`
- `TBD`
- `unknown`
- `n/a`
- `sample`
- `assumed`

Equivalent filler wording such as "to be determined", "current code", "governing standard", or "assumed jurisdiction" must also be rejected unless represented only as a warning about missing context.

## Review Statuses

| Status | Meaning | Mutation Scope |
|---|---|---|
| `standards_context_needed` | Required context is absent or incomplete. | Candidate status/history only. |
| `standards_context_in_review` | Reviewer is collecting context but has not completed it. | Candidate status/history only. |
| `standards_context_complete` | Required context fields are present and non-placeholder. | Candidate status/history only; not promotion. |
| `standards_context_justified_missing` | Missing context is explicitly justified with source/rationale. | Candidate status/history only; may remain learner-blocked. |
| `standards_context_rejected` | Candidate context is fake, unsupported, contradictory, or unsafe. | Candidate status/history only. |

## Blockers

A standards-context preview must block completion when any of these are true:

- edition is missing or placeholder
- version/year is missing or placeholder when the standard requires one
- scope is missing or placeholder
- `sourceOfContext` is missing or placeholder
- reviewer or rationale is missing
- wording implies "current", "governing", "official", "compliant", or "AHJ accepted" without a real reviewed source
- a jurisdiction/AHJ claim is present without explicit reviewed evidence
- a delegated AI reviewer is represented as a biological human reviewer
- completing the decision would create a Resource, link, promotion, or learner exposure

## ASCE 7 Starting State

| Field | Current State |
|---|---|
| Candidate ID | `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` |
| Status | `standards_context_needed` |
| Verification | `unverified` |
| Display policy | `reviewer_only` |
| Learner visible | false |
| Current blocker | Missing edition/version/scope/jurisdiction/source context |

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

A future implementation is acceptable only if tests prove placeholder rejection, reviewer/rationale/sourceOfContext enforcement, transaction-manifest-backed decisions, append-only decision history, rollback behavior, and learner endpoint hiding for incomplete standard candidates.
