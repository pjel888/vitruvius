# Phase 6N — Next Actions

**Created:** 2026-05-04
**Phase:** 6N — Implementation Complete

---

## Current Status

- Resource-only promotion apply infrastructure: **IMPLEMENTED** (code written)
- Node links created: **0**
- resource_and_links mode: **NOT IMPLEMENTED**
- Production resources promoted: **0** (expected, since production external candidates = 0)
- No learner exposure: **CONFIRMED**
- No external verification: **CONFIRMED**
- Validators: **NOT RUN** (terminal limitation)
- Tests: **NOT RUN** (terminal limitation)

---

## Priority 1: Run Validators and Tests

A session with working terminal tools must:

1. `bun run api/validateResourceLayer.ts -- --no-write`
2. `bun run api/validateGraphRelationships.ts -- --no-write`
3. `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`
4. `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`
5. `bun test api/resourceLayerExternalCandidatePromotionPreview.test.ts`
6. `bun test api/resourceLayerExternalCandidateReview.test.ts`
7. `bun test api/resourceLayerExternalCandidates.test.ts`
8. `bun test api/resourceEvidencePath.test.ts`
9. `bun test api/resourceLayer.test.ts`
10. `bun test api/resourceLayerStandardsContext.test.ts`
11. `cd api && bun test`
12. `cd explorer && bun test`
13. `cd explorer && bun run build`
14. `.venv/Scripts/python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

---

## Priority 2: Confirm Production Data Integrity

After validation passes:
- Confirm resources remain 7
- Confirm nodeResourceLinks remain 9
- Confirm external metadata candidates remain 0
- Confirm no graph/canonical changes

---

## Priority 3: Git Operations

- Stage Phase 6N files
- Commit
- Push to origin/main

---

## Priority 4: Phase 6O

Phase 6O = Independent audit of Phase 6N implementation.
Only after validators pass and tests pass.

---

## Priority 5: Phase 6P

Phase 6P = resource_and_links mode implementation (future phase, not planned yet).
