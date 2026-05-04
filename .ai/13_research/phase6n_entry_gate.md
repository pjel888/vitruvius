# Phase 6N — Entry Gate

**Date:** 2026-05-04
**Status:** OPEN — Resource-only implementation allowed
**Blocked:** No

---

## Prerequisites (All Satisfied)

| Prerequisite | Status |
|-------------|--------|
| Phase 6L closure verified | ✅ |
| Phase 6M audit verified | ✅ |
| Validators pass | ✅ |
| Tests pass | ✅ |
| Git state clean | ✅ |
| No production mutation | ✅ |

---

## Allowed Scope

**resource_only ONLY**

Phase 6N may implement:
- `promotion-apply-preview` route extension (read-only)
- `promotion-apply` route (resource_only mode)
- Gate checks A-I (skipping F for resource_only)
- Transaction manifest and rollback
- Candidate history update

Phase 6N must NOT implement:
- nodeResourceLink creation
- resource_and_links mode
- External verification
- Learner exposure (learnerVisibleDefault must remain false)
- Graph/canonical registry mutation

---

## Mandatory Gates

| Gate | Enforced In |
|------|-------------|
| A — Candidate Status | Server-side |
| B — Metadata Integrity | Server-side |
| C — Source Truth / Verification | Server-side |
| D — Rights | Server-side |
| E — Standards | Server-side |
| F — Node-Link | **SKIPPED in resource_only** |
| G — Display / Learner | Server-side |
| H — Transaction / Rollback | Server-side |
| I — Audit / Reviewer | Server-side |

---

## Stop Conditions

Phase 6N must STOP and surface if:
- Any gate is bypassed or weakened
- Transaction manifest is not written before mutation
- Rollback capability is missing
- learnerVisibleDefault is set to true
- External verification is attempted
- Graph or canonical registry is mutated
- P0 or high-risk P1 nodes are affected

---

## Deferred to Phase 6O

- Node-link gate (F)
- nodeResourceLink creation
- resource_and_links mode
- NodeInspector learner sidebar integration for promoted resources

---

## Authorization

This entry gate is opened by terminal-verified closure of Phase 6L/6M.
Actual Phase 6N implementation requires a **separate steward-authorized task**.
