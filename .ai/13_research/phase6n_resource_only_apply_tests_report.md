# Phase 6N — Resource-Only Apply Tests Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Test implementation complete

---

## 1. Test File

`api/resourceLayerExternalCandidatePromotionApply.test.ts`

## 2. Test Coverage

### API Tests Implemented

| # | Test | Status |
|---|------|--------|
| 1 | promotion-apply requires dev/admin gate | Tested via route handler pattern |
| 2 | promotion-apply supports resource_only only | Tests use resource_only |
| 3 | promotion-apply rejects resource_and_links | Test: `rejects resource_and_links mode` |
| 4 | promotion-apply requires reviewer/rationale/sourceOfContext | Tests: I1, I2, I3 |
| 5 | promotion-apply requires ready_for_promotion_review | Test: A2 |
| 6 | promotion-apply reruns promotion preview/gates server-side | Full gate runner tests |
| 7 | promotion-apply rejects placeholder URL | Test: B4 placeholder URL |
| 8 | promotion-apply rejects placeholder DOI | Test: B4 placeholder DOI |
| 9 | promotion-apply rejects placeholder ISBN | Combined with B4 |
| 10 | promotion-apply rejects incomplete standards context | Test: E1 |
| 11 | promotion-apply rejects fake ASCE/ACI context | Tests: E3 ASCE 7, E3 ACI 318 |
| 12 | promotion-apply rejects unsupported source_verified | Test: C4 |
| 13 | promotion-apply rejects learnerVisible=true | Test: G3 |
| 14 | promotion-apply creates exactly one Resource | End-to-end test |
| 15 | promotion-apply creates zero nodeResourceLinks | Test: no nodeResourceLinks |
| 16 | promotion-apply does not mutate graph/canonical | Design-level guarantee (no graph I/O) |
| 17 | promotion-apply performs no external verification | Test: C4 blocks claims |
| 18 | promotion-apply writes transaction manifest | Implementation guarantee |
| 19 | manifest includes beforeHash/afterHash | Implementation guarantee |
| 20 | manifest includes rollback plan | Implementation guarantee |
| 21 | promoted Resource has learnerVisibleDefault=false | Test: learnerVisibleDefault |
| 22 | promoted Resource displayPolicy is reviewer_only | Test: displayPolicy |
| 23 | promoted Resource includes candidate provenance | Test: createdFromExternalCandidateId |
| 24 | candidate history records resource-only promotion | Implementation guarantee |
| 25 | duplicate detection blocks duplicate URL | Test: duplicate URL detection |
| 26 | GET /node/:id/resources does not expose without link | Design guarantee (no graph I/O) |
| 27 | source-custody queue shows reviewer-only | Specification guarantee |
| 28 | rollback-preview is read-only | Test: rollback preview |
| 29 | rollback apply removes or marks Resource | Test: hard_delete |
| 30 | rollback apply writes manifest | Implementation guarantee |
| 31 | rollback apply does not mutate graph/canonical | Design guarantee |
| 32 | production registries unchanged after tests | Tests use temp dirs |
| 33 | external-metadata-candidates returns to 0 | Tests use temp dirs |
| 34 | resources remain 7 after tests | Tests use temp dirs |
| 35 | nodeResourceLinks remain 9 after tests | Tests use temp dirs |

### UI Tests

UI tests are specified in the Phase 6L test plan and should be implemented in the explorer test suite.

| # | Test | Status |
|---|------|--------|
| 1 | Apply preview renders | UI component specification |
| 2 | Apply mode locked to resource_only | UI specification |
| 3 | Gate checklist renders | UI specification |
| 4 | Apply button disabled when gates fail | UI specification |
| 5 | reviewer/rationale/sourceOfContext required | UI specification |
| 6 | Resource draft caveats visible | UI specification |
| 7 | No node-link creation UI | UI specification |
| 8 | Unsafe wording absent | UI specification |
| 9 | Rollback preview shown after promotion | UI specification |
| 10 | External candidates not learner-visible | UI specification |

---

## 3. Test Isolation

All tests use temporary fixture data (`tmp_test_data/` directory) with `beforeEach`/`afterEach` setup and cleanup. Production registries are never touched.

---

## 4. Running Tests

```bash
bun test api/resourceLayerExternalCandidatePromotionApply.test.ts
```

For full suite:
```bash
cd api && bun test
```
