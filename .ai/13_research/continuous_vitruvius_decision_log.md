# Continuous Vitruvius Decision Log — Phase 6N

**Created:** 2026-05-04

---

## Decision: Phase 6N Resource-Only Implementation

**Date:** 2026-05-04
**Decision:** Implement resource_only promotion apply infrastructure

**Rationale:**
- Phase 6M audit verdict: PASS_ALLOW_PHASE_6N_RESOURCE_ONLY_IMPLEMENTATION
- Phase 6L design specified all gates, API routes, transaction model, and rollback
- resource_only mode is safe: no nodeResourceLinks, no learner exposure, no external verification

**Scope:**
- Gate implementation A-I (skipping F for resource_only)
- 4 API routes: preview, apply, rollback-preview, rollback
- Transaction manifest + rollback model
- Test suite for all gate groups

**Consequences:**
- Promotion apply infrastructure exists (resource_only mode)
- resource_and_links remains blocked
- Next phase: 6O independent audit

---

## Decision: Resource ID Prefix

**Date:** 2026-05-04
**Decision:** Use `res_<uuid>` for resource IDs

**Rationale:**
- Clear prefix for identification
- UUID v4 ensures uniqueness
- No sequential IDs to prevent collision

---

## Decision: Manifest-based Rollback

**Date:** 2026-05-04
**Decision:** Rollback writes its own transaction manifest

**Rationale:**
- Audit trail preservation
- Rollback operations are traceable
- Supports both hard_delete and mark_rolled_back

---

## Decision: No Automated Production Promotion

**Date:** 2026-05-04
**Decision:** Phase 6N does not auto-promote any production candidates

**Rationale:**
- Production external candidate count is 0
- Any production promotion requires explicit authorization and passing all gates
- The infrastructure is implemented and tested, but not executed against production data

---

## Decision: Repair Phase 6N Against Runtime API

**Date:** 2026-05-05
**Decision:** Keep Phase 6N scoped to `resource_only` and repair it against the real Hono API, Resource Layer registry paths, and transaction wrapper.

**Rationale:**
- The 2026-05-04 Phase 6N run reported implementation but could not verify terminal output, tests, validators, or git state.
- The mounted runtime API is Hono, not the unmounted Express route file.
- Production external metadata candidates remain 0, so validation must use temp fixtures and keep production resources and links unchanged.

**Scope:**
- Mount resource-only promotion apply and rollback routes in `api/index.ts`.
- Use real Resource Layer registry paths and transaction manifests.
- Preserve `resource_and_links` as explicitly unimplemented pending Phase 6P planning and audit.
- Keep learner visibility false and create zero nodeResourceLinks in resource-only apply.

**Consequences:**
- Phase 6N is terminal-verified and audited as a resource-only infrastructure baseline.
- Production resources remain 7 and production nodeResourceLinks remain 9.
- Next phase is 6P resource_and_links planning, not implementation.
