# Phase 6G Next Actions

**Generated:** 2026-05-03T01:00:00+08:00
**Status:** Phase 6G CLOSED and ACCEPTED.

---

## Completed

- Preview-to-persist external metadata candidate workflow implemented
- Dedicated external candidate registry created with transaction manifest backing
- API routes: persist (POST), list (GET), detail (GET) — all dev-gated
- Source-custody queue includes `externalCandidates` group
- Source-custody route gated per audit finding
- UI save button and persisted candidates list
- 21 new API tests + updated Explorer tests
- Audit findings reconciled:
  - CROSS_DOMAIN_EQUIVALENT verified as 0 (audit typo)
  - CROSS_DOMAIN_ALIGNMENT confirmed as 22
  - Source-custody route gated

---

## Standing Constraints (Remain in Effect)

- No Wave 10
- No graph topology changes without P1 review
- No production Resource Layer mutation without reviewer workflow
- No auto-linking local files
- No auto-promoting resources, candidates, standards, or local files
- ASCE 7 and ACI 318 remain blocked until real standards context is supplied
- P0 Concrete/Reinforced Concrete remains gated
- No fake metadata

---

## Next Authorized Work (Requires Explicit Authorization)

### Option 1: Independent Audit of Phase 6A–6G
Preferred next step before any promotion work:
- Full review of evidence layer implementation
- Verification of all safety constraints and gating
- Assessment of blast radius for candidate-to-resource promotion

### Option 2: Standards Context Completion
- Supply real edition/version/scope for ASCE 7 and ACI 318
- Requires real source research, not placeholder invention
- Must pass standards-context validation rules

### Option 3: Candidate-to-Resource Promotion Workflow
- Explicit reviewer-only promotion from external candidate to resource
- Must create resource record, not auto-link
- Must maintain no-learner-exposure until accepted
- Requires human review decision, not auto-promotion

---

## Recommended Immediate Action

**WAIT for explicit authorization before beginning any of the above.**

Phase 6A–6G are complete and validated. The external metadata candidate persistence workflow is ready for reviewer use.
