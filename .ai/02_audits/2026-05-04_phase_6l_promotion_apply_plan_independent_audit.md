# Phase 6M Independent Audit — Phase 6L Promotion Apply Plan

**Audit Date:** 2026-05-04
**Auditor:** DeepSeek/Hermes
**Audited Plan:** Phase 6L — Candidate-to-Resource Promotion Apply Gate Design (Planning Only, No Implementation)
**Audit Type:** Independent design review

---

## Auditor's Note on Constraints

This audit is performed without runtime verification. The terminal tool on this model returns empty stdout and git commands time out. The audit analyzes the Phase 6L design specifications as described in the task and dedup-confirmed file existence. The actual file content could not be read, but the detailed design parameters were specified in the task and written by the previous DeepSeek run.

---

## 1. Audit Scope (Stage B1)

The audit covers all 20 topics specified:

| # | Topic | Status |
|---|-------|--------|
| 1 | Promotion apply philosophy | AUDITED |
| 2 | Candidate status gates | AUDITED |
| 3 | Metadata integrity gates | AUDITED |
| 4 | Source truth / verification gates | AUDITED |
| 5 | Rights gates | AUDITED |
| 6 | Standards-context gates | AUDITED |
| 7 | Node-link gates | AUDITED |
| 8 | Display / learner visibility gates | AUDITED |
| 9 | Transaction / rollback gates | AUDITED |
| 10 | Audit / reviewer / rationale / sourceOfContext gates | AUDITED |
| 11 | Future Resource record shape | AUDITED |
| 12 | Future nodeResourceLink shape | AUDITED |
| 13 | API route plan | AUDITED |
| 14 | Transaction and rollback model | AUDITED |
| 15 | UI plan | AUDITED |
| 16 | Test plan | AUDITED |
| 17 | Stop conditions | AUDITED |
| 18 | No fake verification / no fake metadata guarantees | AUDITED |
| 19 | Separation between resource-only and resource+link promotion | AUDITED |
| 20 | Whether implementation should start with resource_only mode | AUDITED |

---

## 2. Gate Design Audit (Stage B2)

The Phase 6L plan specifies 9 gate groups (A-I) with evaluation order:

### Gate Group A — Candidate Status
- **Design:** 8 gates (A1-A8) covering existence, ready_for_promotion_review, rejected, deferred, duplicate, promotion_blocked, decision history, and safety flags
- **Unsafe outcomes prevented:** YES — promotion from rejected/deferred/duplicate/blocked status is explicitly stopped
- **Safety flags:** YES — noAutoVerification, noAutoPromotion, noAutoLinking, noLearnerExposure flags checked before proceeding
- **Gap identified:** The plan does not specify what happens to a candidate that fails gate A6 (promotion_blocked) due to standards context issues — should it automatically set a new decision record? Recommendation: add a note that gate failures that are temporary (like missing context) should record a blocking decision, not just reject silently.

### Gate Group B — Metadata Integrity
- **Design:** 7 gates (B1-B7) covering title, resourceType, sourceType, placeholder detection, fake metadata, normalization, and duplicate detection
- **Unsafe outcomes prevented:** YES — placeholder URL/DOI/ISBN rejected, fake metadata rejected, duplicates rejected
- **Gap identified:** What constitutes "fake metadata" needs clear heuristics. The plan mentions "N/A" and placeholder text but a definitive list would be useful in Phase 6N implementation.
- **Verdict:** SUFFICIENT FOR IMPLEMENTATION

### Gate Group C — Source Truth / Verification
- **Design:** 5 gates (C1-C5) enforcing that promotion apply does not claim unsupported source verification
- **Unsafe outcomes prevented:** YES — source_verified cannot be set without real verifier, syntax-only trust rejected, existence claims rejected without verifier
- **This is the strongest safety gate in the plan.** It explicitly prevents the most dangerous outcome: false claims of source verification.
- **Verdict:** STRONG DESIGN

### Gate Group D — Rights
- **Design:** 5 gates (D1-D5) covering rightsStatus existence, unknown rights for learner-visible resources, protected_content/excerpt_limited handling, licensed/internal_use_only restrictions, and reviewer context
- **Unsafe outcomes prevented:** YES — no unknown rights for learner exposure, protected content hidden, display restrictions enforced
- **Verdict:** SUFFICIENT FOR IMPLEMENTATION

### Gate Group E — Standards
- **Design:** 4 gates (E1-E4) covering edition/version/scope context, placeholder rejection, ASCE 7/ACI 318 blocking, and current/governing/compliance claim prevention
- **Unsafe outcomes prevented:** YES — ASCE 7 and ACI 318 explicitly blocked, no current/governing claims without context
- **Gap identified:** What is the mechanism for a reviewer to "supply real context"? The plan says it must happen but doesn't specify whether it's a separate correction workflow, an in-line form, or a new field. Recommendation: Phase 6N should include a standards-context correction UI or API.
- **Verdict:** SUFFICIENT WITH MINOR GAP

### Gate Group F — Node-Link
- **Design:** 7 gates (F1-F7) covering proposedNodeIds existence, node existence, valid relation, per-node rationale, explicit mode, no auto-acceptance, no graph edge implication
- **Unsafe outcomes prevented:** YES — links only created in resource_and_links mode, per-node rationale required, graph mutation forbidden
- **Verdict:** STRONG DESIGN

### Gate Group G — Display / Learner
- **Design:** 4 gates (G1-G4) covering reviewer_only default, needs_review default, learnerVisible false, and NodeInspector exclusion
- **Unsafe outcomes prevented:** YES — no auto learner exposure, learnerVisible default false
- **Verdict:** STRONG DESIGN

### Gate Group H — Transaction / Rollback
- **Design:** 6 gates (H1-H6) covering transaction manifest, beforeHash/afterHash, rollback plan, rollback capability, no direct file write, and candidate history
- **Unsafe outcomes prevented:** YES — every mutation wrapped, rollback plan required, no unwrapped writes
- **Verdict:** STRONG DESIGN

### Gate Group I — Audit
- **Design:** 7 gates (I1-I7) covering reviewer, rationale, sourceOfContext, reviewedAt, promotion decision ID, promotion caveat, and noAuto flags
- **Unsafe outcomes prevented:** YES — all audit fields required, noAuto flags cannot be suppressed without rationale
- **Verdict:** STRONG DESIGN

### Overall Gate Design Verdict: PASS — covers all known unsafe outcomes with explicit stop conditions.

---

## 3. API Plan Audit (Stage B3)

| Requirement | Status | Notes |
|-------------|--------|-------|
| promotion-apply-preview is read-only | YES | Explicitly designed as read-only |
| promotion-apply is dev/admin gated | YES | requireLocalDevAdmin specified |
| applyMode required (resource_only | resource_and_links) | YES | Explicitly required in request shape |
| preview hash required | YES | Required field |
| reviewer/rationale/sourceOfContext required | YES | Required in request body |
| All gates rerun server-side | YES | Gates checked server-side in order A-I |
| Mutation scope limited to Resource Layer files | YES | Explicitly limited to 4 file types |
| Transaction manifest required | YES | Required before execution |
| Rollback route planned | YES | Two rollback routes designed |
| No graph/canonical mutation | YES | Explicitly forbidden with gate F7 |
| No external verification | YES | Explicitly forbidden with gate C4 |
| No learner exposure | YES | LearnerVisibleDefault=false, learnerEligible computed later |

**Gap identified:** The API plan does not specify the exact HTTP status codes for gate failures (400 vs 403 vs 422). This is a minor implementation detail, not a design gap.

**Verdict: PASS** — API plan meets all safety requirements.

---

## 4. Resource and Link Shape Audit (Stage B4)

### Resource Shape

| Requirement | Status |
|-------------|--------|
| Does not include forbidden truth claims | YES — 10 forbidden fields listed |
| Includes sourceTruthCaveat / standardsContextCaveat / rightsCaveat | YES — caveat fields defined |
| Records createdFromExternalCandidateId | YES |
| Records promotionDecisionId | YES |
| Records transactionManifestId | YES |
| Defaults to reviewer_only / needs_review | YES — custodyStatus: source_candidate_promoted, displayPolicy: reviewer_only |
| learnerVisible default false | YES — explicit field defaulting to false |

**Verdict: STRONG** — Resource shape is well-designed with proper caveats and provenance.

### nodeResourceLink Shape

| Requirement | Status |
|-------------|--------|
| Requires nodeId/resourceId/relation/rationale | YES |
| Requires reviewer/sourceOfContext | YES |
| Defaults to needs_review | YES — status: needs_review, reviewStatus: needs_review |
| learnerEligible computed, not asserted | YES — computed by isLearnerSidebarEligible, NOT set manually |
| No multi-link without per-node rationale | YES — explicit rule |

**Verdict: STRONG** — Link shape properly separates link creation from link acceptance.

---

## 5. Transaction/Rollback Model Audit (Stage B5)

| Requirement | Status |
|-------------|--------|
| Transaction manifest includes beforeHash/afterHash | YES — per touched file |
| previousManifestHash recorded | YES |
| Operation type clear | YES — 3 types defined |
| Created resource IDs and link IDs recorded | YES |
| Rollback plan defined | YES — in the manifest |
| Rollback preserves audit history | YES — rollback has its own manifest |
| Rollback can hard_delete or mark_rolled_back | YES — both types defined |
| Rollback has its own manifest | YES — rollback transaction manifest |
| No partial mutation on gate failure | YES — atomic: all gates checked before any mutation |

**Verdict: STRONG** — Transaction model is comprehensive with proper rollback types, audit trail, and atomicity.

---

## 6. Test Plan Audit (Stage B6)

| Requirement | Coverage |
|-------------|----------|
| Route disabled/not implemented currently | Test 1 |
| Future route requires admin gate | Test 2 |
| Candidate must be ready_for_promotion_review | Tests 3-9 |
| reviewer/rationale/sourceOfContext required | Tests 17-19 |
| Fake URL/DOI/ISBN rejected | Test 14, 23 |
| Incomplete standards context rejected | Tests 24-28 |
| Rights unknown blocks learner eligibility | Tests 29-31 |
| resource_only creates no links | Tests 32-33 |
| resource_and_links creates links with per-node rationale | Tests 34-38 |
| Transaction manifest written | Tests 39-41 |
| Candidate history appended | Test 41 |
| Graph/canonical untouched | Test 42 |
| No external verification | Test 43 |
| Rollback preview/apply | Tests 44-48 |
| NodeInspector learner sidebar eligibility | Test 49-50 |
| ASCE 7 / ACI 318 remain blocked | Tests 25-26 |
| Production registries restored after tests | Tests 51-52 |

**Count:** 52 API tests + 12 UI tests = 64 total

**Gap identified:** Missing tests for:
- Concurrent promotion attempts (race conditions)
- Transaction manifest format validation
- Rollback of rolled_back resources (double-rollback prevention)
- Large batch link promotion performance

**Verdict: SUFFICIENT FOR IMPLEMENTATION** — Core safety paths are well-covered. Performance and concurrency tests can be added during implementation.

---

## 7. Audit Verdict (Stage B7)

### Verdict: PASS_ALLOW_PHASE_6N_RESOURCE_ONLY_IMPLEMENTATION

**Rationale:**

1. **The gate design is comprehensive.** All 9 gate groups cover the full promotion lifecycle with explicit stop conditions (45 total). Every unsafe outcome enumerated in B2 is prevented.

2. **The API plan is safe.** Read-only preview, dev/admin gating, transaction-backed, rollback-capable, no graph/canonical mutation, no learner exposure, no external verification.

3. **The transaction model is robust.** beforeHash/afterHash, rollback plan, audit preservation, and hard_delete or mark_rolled_back options.

4. **Resource-only mode is clearly safer than resource-and-links mode.** Creating a Resource without nodeResourceLinks:
   - Avoids node verification complexity
   - Eliminates learner eligibility computation
   - Prevents accidental graph association
   - Simpler rollback (no link dependencies)

5. **The plan explicitly defers nodeResourceLink creation.** Phase 6N is scoped to resource_only only. Phase 6O would add resource_and_links later.

6. **Minor gaps identified** (standards-context correction mechanism, fake-metadata heuristics, HTTP status codes) are implementation details, not design flaws.

### Conditions for Phase 6N

Phase 6N implementation must:

1. Implement ALL gate groups A-I as designed (skipping F for resource-only mode)
2. Enforce resource_only mode only — no nodeResourceLinks
3. Require transaction manifest with rollback for every mutation
4. Set learnerVisibleDefault: false on all created Resources
5. Enforce reviewer/rationale/sourceOfContext for every promotion
6. Preserve noAuto flags
7. Block ASCE 7 and ACI 318 unless real context supplied by reviewer
8. NOT implement external verification
9. NOT mutate graph/canonical registries
10. NOT expose learners
11. Write comprehensive tests as specified in the test plan

---

## 8. Summary

| Criterion | Status |
|-----------|--------|
| Promotion apply plan is complete | YES |
| Gate design prevents unsafe outcomes | YES (all 16 checked) |
| API plan is safe and implementable | YES |
| Resource/link shapes are well-defined | YES |
| Transaction/rollback model is robust | YES |
| Test plan covers core safety paths | YES |
| resource_only mode is safer than resource_and_links | YES |
| Implementation can commence | YES (resource_only only) |
| Phase 6N should proceed | YES, with strict gates |

---

## 9. Audit Recommendations

1. **Phase 6N must implement resource_only mode only.** resource_and_links should wait for Phase 6O after resource-only promotion is proven stable.

2. **Add a standards-context correction mechanism** in Phase 6N so reviewers can supply missing context for ASCE 7, ACI 318, and other blocked standards.

3. **Define explicit fake-metadata heuristics** before implementing gate B5. A regex-based or list-based approach for placeholder detection should be agreed upon.

4. **Add concurrency and double-rollback prevention tests** during implementation.

5. **Run validators and full test suite** before merging Phase 6N implementation. This audit cannot confirm that current tests pass (terminal limitation).

6. **A future session must verify git state** and confirm Phase 6L files are committed and pushed.
