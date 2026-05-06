# Phase 7 First Candidate Batch Reviewer Plan

**Date:** 2026-05-06
**Status:** PHASE7_CANDIDATE_INTAKE_WAVE_1_VALIDATION_PASSED
**Reviewer verdict:** Phase 7A `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`; Phase 7B ASCE 7 `REQUEST_STANDARDS_CONTEXT`, Earth Retaining Structures `REQUEST_SOURCE_CUSTODY_REVIEW`; Phase 7D ASCE 7 `MARK_STANDARDS_CONTEXT_IN_REVIEW`, Earth Retaining Structures `MARK_SOURCE_CUSTODY_IN_REVIEW`; Wave 1 source-family intake `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`

This plan records the completed first bounded Phase 7A reviewer-only candidate intake batch, the Phase 7B review decisions for those candidates, the Phase 7C planning-only verification workflow design, and the Phase 7D controlled source-check status decisions. It created external metadata candidates and candidate decision history only; it did not create Resources, nodeResourceLinks, promotions, or learner exposure.

## Batch Boundary

- Batch mode: reviewer-only candidate intake.
- Candidate count target: maximum 5; completed with 2 persisted candidates from repo-local metadata.
- Initial display policy: `reviewer_only`.
- Initial verification status: `unverified` unless the project owner supplies a separate accepted verification record.
- First workflow: preview plus reviewer-only external metadata candidate persistence.
- First promotion mode, if later authorized: `resource_only`.
- Link workflow: blocked until explicit per-node rationale is provided and a separate implementation prompt authorizes it.

## Required Inputs For Each Candidate

- Title.
- Source type.
- Resource type.
- Steward-supplied source identifier, if any.
- Rights status or rights uncertainty.
- Source-of-context note.
- Reviewer identity recorded honestly.
- Rationale for candidate intake.
- Target node family only if known; exact node links require later per-node rationale.

## Reviewer Identity Rule

Delegated AI review may be recorded as one of:

- `project_owner_delegated_ai_reviewer`
- `external_ai_reviewer`
- `kimi_reviewer`

Do not record delegated AI review as `humanReviewed=true`, `humanReviewer`, or equivalent biological-human approval. If a schema cannot represent delegated AI review, keep the safest status such as `needs_human_review` and add the note:

Reviewed by project-owner-delegated external AI reviewer; not a biological human review; not source truth; not approval unless separately recorded by the project owner.

## Completed First Batch

| Candidate ID | Family | Status |
|---|---|---|
| `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` | Structural standards metadata | `standards_context_in_review`, unverified, reviewer-only, learner-hidden |
| `ext-cand-earth-retaining-structures-mosyi54y-jp9m` | Civil/geotechnical guidance metadata | `source_custody_in_review`, unverified, reviewer-only, learner-hidden |

## Candidate Intake Wave 1

Kimi reviewed three repo-local source-family references and approved reviewer-only persistence as source-family metadata seeds only. Codex persisted them through the existing external-candidate API.

| Candidate ID | Family | Status |
|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | buildingSMART International source-family reference | `candidate`, unverified, reviewer-only, learner-hidden |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | AISC source-family reference | `candidate`, unverified, reviewer-only, learner-hidden |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | AIA source-family reference | `candidate`, unverified, reviewer-only, learner-hidden |

These records intentionally omit exact URLs, publication metadata, standards context, proposed nodes, and proposed relations. They are not Resources, not links, not verified sources, and not promotion-ready.

## Phase 7D Controlled Source-Check Result

Phase 7D performed bounded official-source metadata checks under explicit project-owner authorization:

- ASCE 7 official ASCE landing page check reached `https://www.asce.org/publications-and-news/asce-7` with HTTP 200 and no protected content download. The public page did not provide enough complete edition/version/year/scope/jurisdiction/applicability context for completion, so the candidate moved only to `standards_context_in_review`.
- Earth Retaining Structures official FHWA check reached `https://www.fhwa.dot.gov/engineering/geotech/retaining/` with HTTP 200 and no protected content download. Source-family identity moved into review, but rights/access and full custody context remain incomplete, so the candidate moved only to `source_custody_in_review`.

Kimi reviewed the Phase 7D packet as `project_owner_delegated_ai_reviewer`. This was not a biological human review, not source truth, and not production approval by itself.

Deferred:

| Candidate Source | Reason |
|---|---|
| Additional exact source URLs for source families | no exact URL/source record has been reviewed or verified in this wave |

## Candidate Families For Next Planning Batch

| Priority | Family | Planning-only goal | Blocked actions |
|---:|---|---|---|
| 1 | Architecture | identify real steward-supplied general or professional source metadata | no source lookup, no learner exposure |
| 2 | Structural Engineering | identify non-P0 structural reference metadata | no Concrete/Reinforced Concrete work |
| 3 | Civil Engineering | identify real civil/site/infrastructure source metadata | no AHJ or jurisdiction claim unless supplied |
| 4 | MEPFS | identify real system reference metadata | no rights guess, no auto-link |
| 5 | Standards-linked concepts | collect exact edition/version/scope only if supplied | no ASCE 7 or ACI 318 trust change without real context |

## Validation Required Before Any Later Apply

- Resource validator no-write pass.
- Graph relationship validator no-write pass.
- Canonical graph stewardship validator no-write pass.
- Focused Resource/Evidence tests for candidate preview and custody queue.
- Dirty worktree scope check proving no quarantined entries are staged.
- Transaction manifest and rollback plan for any future write-capable operation.

## Current Entry Decision

The first reviewer-only candidate intake batch, its conservative review decisions, the Phase 7C workflow plan, and the Phase 7D controlled source-check status decisions are complete. Candidate intake wave 1 has persisted three additional reviewer-only source-family reference seeds and validation passed. Next work may review/correct those source-family candidates, request real ASCE 7 context from the project owner, complete FHWA rights/source-custody review, or continue reviewer-only candidate intake. Promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, and high-risk P1 work remain blocked unless a separate project-owner prompt authorizes one of those workflows with exact scope and gates.
