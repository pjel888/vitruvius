# Phase 6L — Promotion Apply Test Plan

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Test plan design for future implementation

---

## 1. Test Philosophy

- Tests are designed for the FUTURE implementation phase (6N/6O)
- No tests are implemented yet
- Tests must verify gates, transaction behavior, and safety invariants
- Tests must NOT perform external verification, graph mutation, or learner exposure

---

## 2. API Tests

### Route Existence Tests

| # | Test | Expected |
|---|------|----------|
| 1 | Verify promotion-apply route does not exist (planning phase) | 404 or missing route |
| 2 | After implementation, route exists and requires admin auth | 200 for authorized, 401/403 for unauthorized |

### Gate Tests

| # | Test | Expected |
|---|------|----------|
| 3 | Apply route rejects if candidate does not exist | 404 with gate A1 failure |
| 4 | Apply route rejects if candidate not `ready_for_promotion_review` | 400 with gate A2 failure |
| 5 | Apply route rejects if candidate is `rejected` | 400 with gate A3 failure |
| 6 | Apply route rejects if candidate is `deferred` | 400 with gate A4 failure |
| 7 | Apply route rejects if candidate is `duplicate_candidate` | 400 with gate A5 failure |
| 8 | Apply route rejects if candidate is `promotion_blocked` | 400 with gate A6 failure |
| 9 | Apply route rejects if candidate has no decision history | 400 with gate A7 failure |
| 10 | Apply route rejects if safety flags are false | 400 with gate A8 failure |
| 11 | Apply route rejects missing title | 400 with gate B1 failure |
| 12 | Apply route rejects missing resourceType | 400 with gate B2 failure |
| 13 | Apply route rejects missing sourceType | 400 with gate B3 failure |
| 14 | Apply route rejects placeholder URL/DOI/ISBN | 400 with gate B4 failure |
| 15 | Apply route rejects fake publisher/author/date | 400 with gate B5 failure |
| 16 | Apply route rejects duplicate against existing resources | 400 with gate B7 failure |

### Reviewer Requirement Tests

| # | Test | Expected |
|---|------|----------|
| 17 | Apply route requires reviewer field | 400 with gate I1 failure |
| 18 | Apply route requires rationale field | 400 with gate I2 failure |
| 19 | Apply route requires sourceOfContext field | 400 with gate I3 failure |

### Verification Safety Tests

| # | Test | Expected |
|---|------|----------|
| 20 | Apply route rejects `source_verified` verificationStatus | 400 with gate C4 failure |
| 21 | Apply route allows `unverified` verificationStatus | Passes gate C2 |
| 22 | Apply route allows `reviewer_verified_metadata` only with review decision | Conditional pass/fail |
| 23 | Apply route rejects fake URL/DOI/ISBN | 400 with gate B4 or J4 |
| 24 | Apply route rejects incomplete standards context | 400 with gate E1 failure |

### Standards Tests

| # | Test | Expected |
|---|------|----------|
| 25 | Apply route rejects ASCE 7 if context incomplete | 400 with gate E3 failure |
| 26 | Apply route rejects ACI 318 if context incomplete | 400 with gate E3 failure |
| 27 | Apply route rejects placeholder standard edition | 400 with gate E2 failure |
| 28 | Apply route rejects current/governing claim without context | 400 with gate E4 failure |

### Rights Tests

| # | Test | Expected |
|---|------|----------|
| 29 | Apply route rejects missing rightsStatus | 400 with gate D1 failure |
| 30 | Apply route rejects unknown rightsStatus for learner-eligible | 400 with gate D2 failure |
| 31 | Apply route enforces display restrictions for licensed resources | 400 with gate D4 failure |

### Mode Tests

| # | Test | Expected |
|---|------|----------|
| 32 | `resource_only` mode creates Resource only | Resources +1, Links +0 |
| 33 | `resource_only` mode creates no links | Zero links created |
| 34 | `resource_and_links` mode creates Resource + links | Resources +1, Links +N |
| 35 | `resource_and_links` mode requires proposedNodeIds | 400 with gate F1 failure |
| 36 | `resource_and_links` mode requires valid node IDs | 400 with gate F2 failure |
| 37 | `resource_and_links` mode requires valid relations | 400 with gate F3 failure |
| 38 | `resource_and_links` mode requires node-specific rationale | 400 with gate F4 failure |

### Transaction Tests

| # | Test | Expected |
|---|------|----------|
| 39 | Apply writes transaction manifest | Manifest file updated |
| 40 | Apply records beforeHash/afterHash | Hashes present in manifest |
| 41 | Apply appends candidate decision history | History includes promotion decision |
| 42 | Apply does not mutate graph/canonical | Graph registries unchanged |
| 43 | Apply does not verify external data | No external calls made |

### Rollback Tests

| # | Test | Expected |
|---|------|----------|
| 44 | Rollback-preview is read-only | No mutation on preview |
| 45 | Rollback-preview returns rollback plan | Plan with resource/link IDs |
| 46 | Rollback apply removes created resource | Resources count restored |
| 47 | Rollback apply removes or marks links | Links count restored or marked |
| 48 | Rollback preserves audit history | Rollback decision in candidate history |

### Learner Exposure Tests

| # | Test | Expected |
|---|------|----------|
| 49 | NodeInspector learner sidebar excludes unreviewed promoted resources | Not visible in learner sidebar |
| 50 | Promoted resource has learnerVisibleDefault: false | Default is false |

### Production Integrity Tests

| # | Test | Expected |
|---|------|----------|
| 51 | Production registries restored after tests | Clean state |
| 52 | No resource/link duplicate collision | Unique IDs |

---

## 3. UI Tests

| # | Test | Expected |
|---|------|----------|
| 1 | Apply preview renders for ready-for-promotion candidate | Panel visible |
| 2 | Apply button disabled when any gate fails | Button disabled with tooltip |
| 3 | Gate checklist renders blockers with descriptions | Blocker items visible |
| 4 | Resource draft shows caveats (not verified, not learner-visible) | Caveat text visible |
| 5 | Link draft shows caveats (needs_review, not learner-visible) | Caveat text visible |
| 6 | Unsafe wording absent from all UI elements | No "verified source", "official", etc. |
| 7 | Standards warning panel shown for standard types | Warning visible |
| 8 | Rights warning panel shown | Warning visible |
| 9 | Rollback preview shown after successful apply | Rollback info visible |
| 10 | No learner-visible toggle that bypasses eligibility | No toggle present |
| 11 | Apply mode selector renders (when proposedNodeIds exist) | Radio buttons visible |
| 12 | Apply mode selector hidden (when no proposedNodeIds) | No selector, defaults to resource_only |

---

## 4. Test Files (Future)

API tests should go in:
- `api/resourceLayerExternalCandidatePromotionApply.test.ts` (new)
- Extend existing `api/resourceLayerExternalCandidates.test.ts`

UI tests should go in:
- `explorer/src/components/resource-review/__tests__/PromotionApplyPanel.test.tsx` (new)
- Extend existing `ResourceReviewAdmin.test.tsx`

---

## 5. Test Data Setup

Tests should:
- Create a fresh candidate in `ready_for_promotion_review` state
- Ensure no duplicate resources exist
- Set up test graph nodes (for `resource_and_links` tests)
- Clean up all created data after tests
- Verify production registries are restored
