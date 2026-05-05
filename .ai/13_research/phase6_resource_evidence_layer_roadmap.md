# Phase 6 Resource Evidence Layer Roadmap

**Updated:** 2026-05-05 (Phase 6N/6O Terminal-Validated)

---

## Completed Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 6A-6J | External candidate pipeline, correction, review, decision | DONE |
| 6K | Promotion preview (read-only) | DONE |
| 6L | Promotion apply gate design (planning only) | DONE |
| 6M | Independent audit of promotion apply plan | DONE (PASS_ALLOW_PHASE_6N) |
| 6N | Resource-only promotion apply implementation | DONE (terminal-validated) |
| 6O | Independent audit of Phase 6N implementation | DONE (PASS_RESOURCE_ONLY_BASELINE) |

---

## Current Phase: 6P - Resource-And-Links Planning

`resource_and_links` is intentionally not implemented yet. It remains blocked until a separate plan and audit define:

- link creation eligibility;
- node existence checks;
- per-node rationale requirements;
- valid node-resource relationship constraints;
- accepted vs needs_review defaults;
- learner eligibility computation through `isLearnerSidebarEligible`;
- rights and standards-context restrictions;
- transaction manifest coverage;
- rollback behavior for Resource + nodeResourceLinks.

---

## Completed Phase: 6N - Resource-Only Promotion Apply

**Scope:** Implement resource_only promotion apply infrastructure.

- [x] Resource-only apply contract defined
- [x] Gate implementation (A-I, F blocks resource_and_links)
- [x] Hono API routes mounted: apply-preview, apply, rollback-preview, rollback
- [x] Resource registry integration
- [x] Transaction-backed apply and rollback
- [x] Test suite written
- [x] Validators run
- [x] Tests pass
- [x] Independent audit complete
- [ ] Git committed/pushed (pending scoped staging)

**Key outcomes:**

- Promotion apply infrastructure for resource_only mode is implemented and validated.
- No production resources were created because production external metadata candidate count is 0.
- No production nodeResourceLinks were created.
- `resource_and_links` remains blocked with `F0`.

---

## Upcoming Phases

| Phase | Description | Gate |
|-------|-------------|------|
| 6P | resource_and_links mode planning | Requires scoped Phase 6N commit/push |
| 6P-impl | resource_and_links mode implementation | Requires Phase 6P plan audit pass |
| 6Q | Learner sidebar integration | Requires resource_and_links implementation and audit |
| 6R | External verification workflow | Requires verification tooling |
| 6S | Compliance and current-status workflow | Requires Phase 6R |

---

## Key Metrics

| Metric | Value | Verified? |
|--------|-------|-----------|
| Admitted relationships | 264 | TERMINAL VERIFIED |
| Base graph edges | 13,670 | TERMINAL VERIFIED |
| Effective edges | 13,934 | TERMINAL VERIFIED |
| CROSS_DOMAIN_EQUIVALENT | 0 | TERMINAL VERIFIED |
| CROSS_DOMAIN_ALIGNMENT | 22 | TERMINAL VERIFIED |
| Resources | 7 | TERMINAL VERIFIED |
| nodeResourceLinks | 9 | TERMINAL VERIFIED |
| External metadata candidates | 0 | TERMINAL VERIFIED |
| Promotion apply implemented | YES (resource_only) | TERMINAL VERIFIED |
| resource_and_links implemented | NO | TERMINAL VERIFIED |
| NodeResourceLinks created | 0 | TERMINAL VERIFIED |
| Learner exposure | NO | TERMINAL VERIFIED |
| External verification | NO | TERMINAL VERIFIED |
