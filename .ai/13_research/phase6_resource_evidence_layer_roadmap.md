# Phase 6 Resource Evidence Layer Roadmap

**Updated:** 2026-05-04 (Phase 6N Implementation Complete)

---

## Completed Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 6A-6J | External candidate pipeline, correction, review, decision | DONE |
| 6K | Promotion preview (read-only) | DONE |
| 6L | Promotion apply gate design (planning only) | DONE |
| 6M | Independent audit of promotion apply plan | DONE (PASS_ALLOW_PHASE_6N) |
| **6N** | **Resource-only promotion apply implementation** | **IMPLEMENTED (code written, pending validation)** |

---

## Current Phase: 6N — Resource-Only Promotion Apply

**Scope:** Implement resource_only promotion apply infrastructure.

- [x] Resource-only apply contract defined
- [x] Gate implementation (A-I, skipping F)
- [x] API routes (preview, apply, rollback-preview, rollback)
- [x] Resource registry integration
- [x] Source-custody queue integration
- [x] Resource review UI specification
- [x] Test suite written
- [ ] Validators run (NOT RUN — terminal limitation)
- [ ] Tests pass (NOT RUN — terminal limitation)
- [ ] Git committed/pushed (NOT CONFIRMED — terminal limitation)

**Key outcomes:**
- Promotion apply infrastructure for resource_only mode is implemented
- No production resources were created (expected, since candidates = 0)
- No nodeResourceLinks created
- resource_and_links remains blocked

---

## Upcoming Phases

| Phase | Description | Gate |
|-------|-------------|------|
| **6O** | Independent audit of Phase 6N implementation | Requires validated Phase 6N |
| **6P** | resource_and_links mode implementation | Requires Phase 6O audit pass |
| **6Q** | Learner sidebar integration | Requires Phase 6P |
| **6R** | External verification workflow | Requires verification tooling |
| **6S** | Compliance and current-status workflow | Requires Phase 6R |

---

## Key Metrics (as of Phase 6N)

| Metric | Value | Verified? |
|--------|-------|-----------|
| Admitted relationships | 264 | ACCEPTED FROM TASK SPEC |
| Base graph edges | 13,670 | ACCEPTED FROM TASK SPEC |
| Effective edges | 13,934 | ACCEPTED FROM TASK SPEC |
| CROSS_DOMAIN_EQUIVALENT | 0 | ACCEPTED |
| CROSS_DOMAIN_ALIGNMENT | 22 | ACCEPTED |
| Resources | 7 | ASSUMED UNCHANGED |
| nodeResourceLinks | 9 | ASSUMED UNCHANGED |
| External metadata candidates | 0 | ASSUMED UNCHANGED |
| Promotion apply implemented | YES (resource_only) | CONFIRMED |
| resource_and_links implemented | NO | CONFIRMED |
| NodeResourceLinks created | 0 | CONFIRMED |
| Learner exposure | NO | CONFIRMED |
| External verification | NO | CONFIRMED |
