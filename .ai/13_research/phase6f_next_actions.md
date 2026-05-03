# Phase 6F Next Actions

**Updated:** 2026-05-03T01:00:00+08:00
**Status:** Phase 6F ACCEPTED. Phase 6E authorized to begin.

---

## Completed (6F Closure)

- [x] Fix missing `getResourceReviewSourceCustody` mock in integration test
- [x] Run full Explorer test suite (116/116 pass)
- [x] Run full API test suite (256/256 pass)
- [x] Run Python KG pytest (118/118 pass)
- [x] Run Explorer build (pass)
- [x] Run no-write validators (ResourceLayer, Graph, Canonical — all pass, no file dirtied)
- [x] Verify production Resource Layer data unchanged
- [x] Verify graph/canonical/P0/high-risk P1 unchanged
- [x] Verify ASCE 7 / ACI 318 remain blocked
- [x] Write final acceptance verification report
- [x] Write worktree hygiene report
- [x] Write Python KG validation report
- [x] Update resource/evidence layer roadmap
- [x] Append to continuous validation log
- [x] Append to continuous quality report

---

## Next Authorized Work: Phase 6E

**Phase 6E: External URL/Book/PDF Metadata Candidate Workflow**

### Constraints (Non-Negotiable)
- Must remain **reviewer-only** and **candidate-only**.
- No external URL/book/PDF **auto-verification**.
- No fake **DOI/ISBN/edition/version/jurisdiction/AHJ adoption** metadata.
- No **learner exposure** until reviewer accepted and validated.
- No graph admissions.
- No production Resource Layer mutation without reviewer workflow.
- ASCE 7 and ACI 318 remain blocked until real context supplied.

### Suggested 6E Scope
1. Design candidate ingestion schema for external URLs, books, and PDFs.
2. Add candidate creation API (reviewer-only, no auto-accept).
3. Add candidate review UI tab in ResourceReviewAdmin.
4. Implement metadata validation (URL reachability, ISBN format check, no fake data).
5. Add evidence-path regression tests for candidate workflow.

### Do Not Start Without
- Approved 6E implementation plan.
- Audit of current candidate registry state.
- Impact analysis on ResourceReviewAdmin component.

---

## Standing Maintenance

- [ ] Refresh code intelligence indices before next code edit (`./scripts/refresh_code_intelligence.sh`).
- [ ] Run no-write validators weekly or before any registry-touching change.
- [ ] Keep `.ai/13_research/continuous_vitruvius_validation_log.md` and `continuous_vitruvius_quality_report.md` current.

---

*No further 6F action required.*
