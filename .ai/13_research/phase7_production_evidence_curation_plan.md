# Phase 7 Production Evidence Curation Plan

**Date:** 2026-05-06
**Phase:** Production Evidence Curation and Real Resource Growth
**Status:** PLAN_ONLY

## Goal

Use the Phase 6 Resource/Evidence infrastructure to carefully add real Resources and nodeResourceLinks at scale without fake metadata, unsafe learner exposure, or graph/canonical mutation.

## Non-Negotiable Boundaries

- No fake URLs, DOI, ISBN, books, PDFs, standard editions, AHJ claims, reviewer claims, or publication metadata.
- No external URL, DOI, ISBN, book API, PDF, or source verification unless explicitly authorized for a bounded batch.
- No protected content copying.
- No learner exposure unless accepted nodeResourceLink eligibility passes.
- No graph/canonical mutation, edge admission, merge, alias, redirect, or tombstone in this phase unless a separate graph packet authorizes it.
- No P0 Concrete/Reinforced Concrete work or high-risk P1 packet work inside Resource/Evidence curation batches.

## Workstreams

### A. Real External Candidate Seeding

- Seed reviewer-only candidates from real steward-supplied metadata.
- Keep candidates unverified unless a real review record supports another status.
- Do not auto-verify, auto-promote, auto-link, or expose to learners.
- Reject placeholders and incomplete source identity.

### B. Source Verification Workflow

- URL reachability checks require explicit authorization.
- DOI/ISBN lookup requires explicit authorization.
- Source truth claims require recorded review evidence.
- Protected content must not be copied into Resource Layer records.

### C. Standards Context Completion

- ASCE 7 and ACI 318 require real edition/version/scope/source context before trust changes.
- Do not guess "latest" or "current".
- Do not assert AHJ or jurisdiction applicability unless sourced and reviewed.

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

## Phase 7 Completion Criteria

Phase 7 is healthy when Resource Layer growth is real, reviewed, reversible, and learner-safe:

- production Resource count grows only through gated apply
- nodeResourceLinks grow only through explicit node rationale
- external metadata candidate queue remains clean after each batch
- ASCE 7 / ACI 318 trust status changes only with real context
- local file admission remains reviewer-controlled
- validators and focused tests pass after every batch
- dirty worktree quarantine remains enforced
