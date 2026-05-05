# Phase 7 Entry Gate

**Date:** 2026-05-06
**Phase:** Production Evidence Curation and Real Resource Growth
**Gate status:** OPEN_FOR_PLANNING_ONLY

## Entry Evidence

| Requirement | Status |
|---|---|
| Phase 6 Resource/Evidence infrastructure closed | PASS |
| Resource-only promotion apply implemented | PASS |
| Resource-only rollback implemented | PASS |
| Resource-and-links plan and implementation audited | PASS |
| Resource validator | PASS |
| Graph validator | PASS |
| Canonical validator | PASS |
| API tests | PASS, 398 |
| Explorer tests | PASS, 118 |
| Explorer build | PASS |
| Python KG regression | PASS, 118 |
| Production resources unchanged | PASS, 7 |
| Production nodeResourceLinks unchanged | PASS, 9 |
| Production external metadata candidates | PASS, 0 |
| Dirty worktree quarantined | PASS_WITH_CAVEAT, 818 unrelated entries |

## Allowed Next Work

- Plan the first small real candidate batch.
- Accept steward-supplied real metadata into reviewer-only preview workflows.
- Use no-write previews to inspect source identity, duplicates, rights, standards context, and learner eligibility.
- Prepare batch-specific audit and rollback requirements.

## Blocked Until Separate Authorization

- External URL, DOI, ISBN, book API, or PDF verification.
- Protected content copying.
- ASCE 7 or ACI 318 trust changes without real edition/version/scope/source context.
- Production Resource creation outside gated apply.
- Production nodeResourceLink creation outside gated `resource_and_links` apply.
- Graph/canonical mutation, edge admission, merge, alias, redirect, or tombstone.
- P0 Concrete/Reinforced Concrete work.
- High-risk P1 packet work.
- Staging quarantined dirty canonical/source artifacts.

## Entry Conditions For First Implementation Batch

Before Phase 7 implementation begins, the batch must provide:

- exact candidate metadata supplied by the steward
- source type and rights status
- reviewer identity and rationale
- source-of-context statement
- duplicate check result
- learner exposure decision computed by the system
- transaction manifest and rollback plan
- explicit list of files allowed to be staged

## Exact Next Action

Prepare a small steward-supplied candidate batch for preview only. Do not seed, promote, verify, or link any production candidate until a batch-specific prompt authorizes the work.
