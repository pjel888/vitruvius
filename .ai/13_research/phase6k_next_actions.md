# Phase 6K Next Actions

**Date:** 2026-05-03
**Status:** Implementation Complete

---

## What Was Implemented

1. **Promotion preview helper** — `api/resourceLayer/externalCandidatePromotionPreview.ts`
2. **Promotion preview API route** — `POST /resources/review/external-candidates/:candidateId/promotion-preview`
3. **Promotion preview UI tab** — ResourceReviewAdmin ExternalCandidateReviewPanel
4. **Promotion preview tests** — 14 API tests

## What Was NOT Implemented

- Promotion apply (creating actual Resource)
- Promotion apply (creating actual NodeResourceLink)
- External verification
- Graph/canonical mutation
- Learner exposure

## Next Safe Phase

**Phase 6L — Audit of 6K**

Independent audit of:
- Promotion preview helper correctness
- API route safety
- UI safe wording
- Test coverage completeness
- No-mutation guarantees

## Future Phase (Requires Explicit Authorization)

**Phase 6M — Promotion Apply**

Only with explicit project-owner steward authorization:
- Create Resource from candidate
- Create NodeResourceLink from candidate
- Transaction manifest generation
- Rollback capability
- Canonical admission workflow

## Standing Constraints

- ASCE 7 and ACI 318 remain blocked
- No fake metadata
- No auto-promotion
- No auto-linking
- No learner exposure without explicit verification
