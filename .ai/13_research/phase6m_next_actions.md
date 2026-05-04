# Phase 6M — Next Actions

**Created:** 2026-05-04
**Phase:** 6M — Independent Audit Complete

---

## Audit Verdict

**Verdict:** PASS_ALLOW_PHASE_6N_RESOURCE_ONLY_IMPLEMENTATION

---

## Next Actions

### Priority 1: Phase 6N — Resource-Only Promotion Implementation

**Prerequisites:**
- [ ] Phase 6L closure verified (validators pass, tests pass, git committed) — NOT YET VERIFIED (terminal limitation)
- [ ] Phase 6L planning files committed and pushed — INCONCLUSIVE (exit codes suggest success but stdout empty)
- [ ] Phase 6M audit accepted by steward

**Implementation scope:**
- Implement `promotion-apply-preview` route
- Implement `promotion-apply` route (resource_only mode only)
- Implement gate checks A-I (skipping F for resource_only)
- Implement transaction manifest and rollback
- Implement candidate history update
- No nodeResourceLink creation
- No learner exposure
- No external verification
- No graph mutation

### Priority 2: Run Validators and Tests

A session with working terminal tools must:
1. Run `bun run api/validateResourceLayer.ts -- --no-write`
2. Run `bun run api/validateGraphRelationships.ts -- --no-write`
3. Run `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`
4. Run all bun tests
5. Run explorer tests and build
6. Run Python tests
7. Verify production data integrity

### Priority 3: Finalize Git State

A session with working terminal tools must:
1. Run `git status` to confirm branch and dirty state
2. Stage any remaining Phase 6L/6M files
3. Commit and push
4. Verify branch sync with origin/main

---

## Pending Before Phase 6N

- [ ] Validation suite passes
- [ ] Test suite passes
- [ ] Production data integrity confirmed
- [ ] Git state clean on main
- [ ] Steward authorization for Phase 6N implementation
