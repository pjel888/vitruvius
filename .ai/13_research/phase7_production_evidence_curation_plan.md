# Phase 7 Production Evidence Curation Plan

**Date:** 2026-05-06
**Phase:** Production Evidence Curation and Real Resource Growth
**Status:** PHASE7_WAVE2_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT_VALIDATED
**Delegated reviewer verdict:** Phase 7A `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`; Phase 7B ASCE 7 `REQUEST_STANDARDS_CONTEXT`, Earth Retaining Structures `REQUEST_SOURCE_CUSTODY_REVIEW`; Phase 7D ASCE 7 `MARK_STANDARDS_CONTEXT_IN_REVIEW`, Earth Retaining Structures `MARK_SOURCE_CUSTODY_IN_REVIEW`; source-family official-domain support `PASS_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT`; candidate intake wave 2 `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`; candidate review wave 2 `MARK_NEEDS_REVIEW`; wave 2 official-domain support `PASS_WAVE2_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT`

## Goal

Use the Phase 6 Resource/Evidence infrastructure to carefully add real Resources and nodeResourceLinks at scale without fake metadata, unsafe learner exposure, or graph/canonical mutation.

## Non-Negotiable Boundaries

- Delegated AI review may be recorded as `project_owner_delegated_ai_reviewer`, `external_ai_reviewer`, or the exact tool reviewer such as `kimi_reviewer`; it must not be recorded as biological-human review.
- No fake URLs, DOI, ISBN, books, PDFs, standard editions, AHJ claims, reviewer claims, or publication metadata.
- No external URL, DOI, ISBN, book API, PDF, or source verification unless explicitly authorized for a bounded batch.
- No protected content copying.
- No learner exposure unless accepted nodeResourceLink eligibility passes.
- No graph/canonical mutation, edge admission, merge, alias, redirect, or tombstone in this phase unless a separate graph packet authorizes it.
- No P0 Concrete/Reinforced Concrete work or high-risk P1 packet work inside Resource/Evidence curation batches.

## Workstreams

### Entry Gate

Kimi reviewed the post-Phase-6 dirty-worktree quarantine and returned `PASS_PLANNING_ONLY`; the seven-file blocker was later dispositioned with `PASS_COMMIT_SAFE_FILES`. The project owner then authorized a bounded Phase 7A reviewer-only candidate intake batch. Kimi reviewed the Phase 7A candidate packet and returned `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`.

Phase 7A persisted two reviewer-only, unverified external metadata candidates. Phase 7B applied conservative review decisions to those candidates: ASCE 7 needed standards context, and Earth Retaining Structures needed source-custody review. Phase 7C planned the next standards-context/source-custody verification workflows, API route shapes, UI panels, and future tests. Phase 7D implemented controlled source-check preview/decision workflows, performed bounded official-source metadata checks, and moved ASCE 7 to `standards_context_in_review` and Earth Retaining Structures to `source_custody_in_review`. No Resources, nodeResourceLinks, promotions, learner exposure, graph/canonical mutation, P0 work, or high-risk P1 work occurred.

### A. Real External Candidate Seeding

- Seed reviewer-only candidates from real steward-supplied metadata.
- Keep candidates unverified unless a real review record supports another status.
- Do not auto-verify, auto-promote, auto-link, or expose to learners.
- Reject placeholders and incomplete source identity.
- Phase 7A completed the first seed: two repo-local reviewer-only candidates for ASCE 7 and FHWA Earth Retaining Structures.
- Phase 7B reviewed those candidates and marked ASCE 7 `standards_context_needed` and Earth Retaining Structures `source_custody_review_needed`.
- Phase 7C planned the future verification workflow for these blockers without performing verification.
- Phase 7D performed bounded official-source metadata checks and moved the candidates to reviewer-only in-review statuses; both remain unverified and learner-hidden.
- Phase 7 candidate intake wave 1 persisted three repo-local source-family reference candidates for buildingSMART, AISC, and AIA as reviewer-only, unverified, learner-hidden intake seeds only.
- Phase 7 candidate review wave 1 marked those three source-family candidates `needs_review`; they still require metadata correction/source-custody review before verification, promotion readiness, Resource creation, links, or learner exposure.
- Phase 7 candidate intake wave 2 persisted five more repo-local source-family reference candidates for U.S. Access Board, WBDG/NIBS, IStructE, ICE, and RIBA as reviewer-only, unverified, learner-hidden intake seeds only.
- Phase 7 candidate review wave 2 marked those five source-family candidates `needs_review`; they still require metadata correction/source-custody review before verification, promotion readiness, Resource creation, links, or learner exposure.
- ASCE remains incomplete and not learner-trusted.

### B. Source Verification Workflow

- URL reachability checks require explicit authorization.
- DOI/ISBN lookup requires explicit authorization.
- Source truth claims require recorded review evidence.
- Protected content must not be copied into Resource Layer records.
- Phase 7C planned source-custody stages: `metadata_review`, `rights_review`, `reachability_check_pending`, `source_custody_verified`, `source_custody_rejected`, and `verification_deferred`.
- Syntax-valid URL remains candidate metadata only and is not verification.
- Phase 7D added source-verification preview/decision routes and bounded URL metadata helpers with official-domain checks, timeout/redirect/body caps, no payload storage, and transaction-backed candidate status decisions.
- HTTP success must not be treated as source truth by itself.
- Earth Retaining Structures reached `source_custody_in_review`; rights/access and full source-custody review still need completion before `source_custody_verified` or promotion readiness.
- Source-family official-domain support now covers buildingSMART, AISC, and AIA for future reviewer-supplied explicit URL checks. This unit performed no live source verification and made no candidate registry changes.
- Wave 2 source-family official-domain support now covers U.S. Access Board, WBDG/NIBS, IStructE, ICE, and RIBA for future reviewer-supplied explicit URL checks. This unit performed no live source verification and made no candidate registry changes.

### C. Standards Context Completion

- ASCE 7 and ACI 318 require real edition/version/scope/source context before trust changes.
- Do not guess "latest" or "current".
- Do not assert AHJ or jurisdiction applicability unless sourced and reviewed.
- Phase 7C planned standards-context statuses: `standards_context_needed`, `standards_context_in_review`, `standards_context_complete`, `standards_context_justified_missing`, and `standards_context_rejected`.
- Placeholder values such as `latest`, `current`, `TBD`, `unknown`, `n/a`, `sample`, and `assumed` must remain blocked.
- Phase 7D checked the official ASCE public landing page metadata and moved ASCE 7 to `standards_context_in_review`; edition/version/year/scope/jurisdiction/applicability context remains incomplete, so the candidate is still blocked from completion and promotion readiness.

### D. Local File Custody

- Review indexed local files by hash, rights status, source family, and intended use.
- Admission requires a reviewer decision.
- Local files must not be auto-linked to nodes.
- Metadata/hash custody is allowed; content republication remains blocked.

### E. Candidate Promotion

- Use `resource_only` promotion first.
- Use `resource_and_links` only with strong node-specific rationale.
- Every apply requires transaction manifest and rollback plan.
- Learner eligibility is computed, not asserted manually.

### F. Node Sidebar Evidence Growth

Prioritize high-value nodes:

- Architecture
- Structural Engineering
- Civil Engineering
- MEPFS
- standards-linked concepts
- high-traffic nodes

Learner view shows accepted eligible resources only. Reviewer-only and needs-review resources remain hidden or warning-gated.

### G. Quality And Audit Cadence

Every batch must include:

- preview
- review
- apply
- validation
- audit sample
- commit and push

No broad backfill may run without a sampling audit and rollback proof.

## Batch Lifecycle

1. Create a batch plan with exact source metadata supplied by the steward.
2. Run preview only.
3. Review warnings, duplicate keys, rights status, standards context, and learner eligibility.
4. Apply `resource_only` for accepted resource records.
5. Apply `resource_and_links` only after per-node rationale is recorded.
6. Run validators and tests.
7. Audit a sample and any rejected/blocked records.
8. Commit and push scoped files only.

## Current Next Step

Next safe action is commit/push for wave 2 source-family official-domain helper support, then reassess unblocked Phase 7 work. Safe options include metadata correction/source-custody review for source-family candidates using explicit reviewer-supplied official URLs, supplying real ASCE 7 edition/version/year/scope/applicability context, completing FHWA rights/source-custody review, continuing reviewer-only candidate intake only if high-value repo-local metadata remains, or non-mutating Explorer evidence visibility work. Promotion, Resource creation, nodeResourceLink creation, learner exposure, DOI/ISBN lookup, broad crawling, protected content access, graph/canonical mutation, P0 work, and high-risk P1 work remain blocked until separately authorized.

## Phase 7 Completion Criteria

Phase 7 is healthy when Resource Layer growth is real, reviewed, reversible, and learner-safe:

- production Resource count grows only through gated apply
- nodeResourceLinks grow only through explicit node rationale
- external metadata candidate queue remains clean after each batch
- ASCE 7 / ACI 318 trust status changes only with real context
- local file admission remains reviewer-controlled
- validators and focused tests pass after every batch
- dirty worktree quarantine remains enforced
