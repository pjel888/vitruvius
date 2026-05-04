# Phase 6 Resource Evidence Layer Roadmap

**Created:** 2026-05-04 (Updated for Phase 6L Planning)
**Phase:** 6L — Planning Only
**Status:** Active roadmap

---

## Completed Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 6A | External metadata candidate schema and intake | DONE |
| 6B | Correction workflow and validation | DONE |
| 6C | Review decision layer | DONE |
| 6D | Duplicate detection and metadata normalization | DONE |
| 6E | External candidate registry and persistence | DONE |
| 6F | Review workflow integration with ResourceReviewAdmin | DONE |
| 6G | Local file indexing and admission | DONE |
| 6H | External candidate promotion gate design | DONE |
| 6I | External candidate correction/review/decision workflow | DONE |
| 6J | Phase 6I acceptance verification | DONE |
| 6K | External candidate promotion preview (read-only) | DONE |
| 6L | Promotion apply gate design (planning only) | DONE |

---

## Current Phase

### Phase 6L: Promotion Apply Gate Design (PLANNING — NO IMPLEMENTATION)

**Scope:** Design the candidate-to-resource promotion apply workflow

**Deliverables:**
- [x] Phase 6L preflight state verification
- [x] Promotion apply philosophy
- [x] Promotion apply gate design (9 gate groups A-I)
- [x] Future resource record shape
- [x] Future nodeResourceLink shape
- [x] Promotion apply API plan (4 routes)
- [x] Transaction and rollback model
- [x] Resource review UI plan
- [x] Test plan for future implementation
- [x] Stop conditions (45 conditions)
- [x] No-mutation validation report
- [x] Roadmap update
- [x] Decision log update

**Non-negotiable constraints:**
- Promotion apply NOT implemented
- No resources created
- No nodeResourceLinks created
- No graph/canonical mutations
- No external verification
- No learner exposure
- No P0/high-risk P1 action

---

## Upcoming Phases

| Phase | Description | Gate |
|-------|-------------|------|
| **6M** | Independent audit of promotion apply plan | Requires Phase 6L completion |
| **6N** | Resource-only promotion implementation | Requires Phase 6M audit pass |
| **6O** | Resource + nodeResourceLink promotion | Requires Phase 6N stability |
| **6P** | Learner sidebar integration | Requires Phase 6O |
| **6Q** | External verification workflow | Requires verification tooling |
| **6R** | Compliance and current-status workflow | Requires Phase 6Q |

---

## Key Metrics (as of Phase 6L)

| Metric | Value |
|--------|-------|
| Active admitted relationships | 264 |
| Base graph edges | 13,670 |
| Effective graph edges | 13,934 |
| CROSS_DOMAIN_EQUIVALENT | 0 |
| CROSS_DOMAIN_ALIGNMENT | 22 |
| Resources | 7 |
| nodeResourceLinks | 9 |
| Existing resource candidates | 4 |
| External metadata candidates | 0 |
| Local files indexed | 25 |
| Local files admitted | 0 |
| Standards missing context | 2 |
| Standards promotion blocked | 3 |
| Promotion apply implemented | NO |
| Resource/link creation unblocked | NO |
| Learner exposure occurred | NO |
| External verification occurred | NO |
