# Continuous Vitruvius Decision Log

**Date:** 2026-05-03

## Decision: Phase 6H Planning Scope

**Context:** Phase 6G is complete. External metadata candidates are persisted in a reviewer-only, unverified, transaction-manifest-backed registry. The next logical step is to design how reviewers can evaluate these candidates.

**Decision:** Phase 6H is scoped to planning and gate-design ONLY. No implementation of promotion, resource creation, or linking.

**Rationale:**
1. Promotion is a high-stakes operation that creates production data.
2. Review-decision workflow is a prerequisite for safe promotion.
3. Planning allows gate design to be reviewed before code is written.

**Consequences:**
- Phase 6H deliverables are design documents, not code changes.
- Implementation requires separate authorization.
- Promotion apply (Phase 6I or later) requires separate authorization after review workflow exists.

## Decision: Test Transaction Manifest Cleanup

**Context:** Tests were leaving transaction manifests that caused canonical validator drift warnings.

**Decision:** Add `cleanTransactionManifests()` to `beforeEach` and `afterAll` in `api/resourceLayerExternalCandidates.test.ts`.

**Rationale:** Test hygiene must not break production validation.

**Consequences:**
- Canonical validator remains clean after test runs.
- Test suite is slightly slower (file system operations).
- No production impact.

## Decision: No Cleanup Manifest for Empty Registry Reset

**Context:** Resetting `external-metadata-candidates.json` to empty required a policy decision on transaction manifests.

**Decision:** No cleanup manifest required for empty-test cleanup.

**Rationale:**
- The registry is explicitly a candidate staging area.
- The intended production state is zero candidates.
- No resource, link, review decision, or graph mutation occurred.

**Consequences:**
- Transaction manifests for test artifacts are ephemeral and deleted.
- Canonical validator does not track drift for empty candidate registries.
