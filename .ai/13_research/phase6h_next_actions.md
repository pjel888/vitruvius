# Phase 6H Next Actions

**Date:** 2026-05-03
**Status:** Planning Complete

## Immediate Next Action

**Do NOT implement promotion.**

Phase 6H planning is complete. The next safe implementation step is:

1. **Await explicit authorization** for Phase 6H review-decision workflow implementation.
2. If authorized, implement:
   - `external-candidate-decisions.json` registry
   - Correction preview + apply routes
   - Review decision preview + apply routes
   - Decision history route
   - ResourceReviewAdmin review panel UI
   - Transaction manifest integration for all mutations

## What is NOT Authorized

- Candidate-to-resource promotion apply
- Resource creation from candidates
- NodeResourceLink creation from candidates
- Auto-linking candidates to nodes
- Auto-promoting candidates to accepted status
- External URL/DOI/ISBN verification calls
- Standards context auto-completion
- Graph edge admission

## What is Authorized When Phase 6H Implementation is Approved

- Reviewer decision workflow for external candidates
- Metadata correction preview/apply
- Status changes: candidate → needs_review → metadata_correction_needed → ready_for_promotion_review
- Status changes: reject, defer, duplicate_candidate
- Promotion readiness gate evaluation (read-only)
- Promotion preview (read-only, no file mutation)
- Decision history tracking

## Phase 6I (Future, Requires Separate Authorization)

- Promotion apply: create Resource from candidate
- Promotion apply: create NodeResourceLink from candidate
- Source-custody queue update after promotion
- Graph/canonical integration after resource creation
