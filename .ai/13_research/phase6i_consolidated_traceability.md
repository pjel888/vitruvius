# Phase 6I Consolidated Traceability Document

**Date:** 2026-05-03
**Status:** Post-Implementation / Post-Audit
**Scope:** External candidate correction, review decision workflow, promotion readiness, history, and UI
**Authority:** Independent audit verdict HIGH confidence, PROCEED to 6K

---

## 1. Review States and Decision Types

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Export:** `ExternalCandidateReviewStatus`, `ExternalCandidateDecisionType`

### Review States (11)
```ts
candidate | needs_review | metadata_correction_needed
| source_custody_review_needed | rights_review_needed
| standards_context_needed | duplicate_candidate
| rejected | deferred | ready_for_promotion_review
| promotion_blocked
```

### Decision Types (11)
```ts
apply_metadata_correction | mark_needs_review | mark_ready_for_promotion_review
| mark_promotion_blocked | mark_rejected | mark_deferred
| mark_duplicate | mark_rights_review_needed | mark_standards_context_needed
| mark_source_custody_review_needed | rollback_decision
```

### Safety Invariants
- `noAutoPromotion: true` on every decision record
- `noAutoLinking: true` on every decision record
- `noLearnerExposure: true` on every decision record
- `auditCaveat` required on every decision record

---

## 2. Correction Preview

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Function:** `previewCorrection(candidate, patch, reviewer, rationale)`

### Behavior
- Pure/read-only — no file writes, no registry mutation
- Re-runs `detectExternalMetadataPlaceholders` on patched values
- Re-runs `validateExternalMetadataCandidate`
- Computes `diff.changedFields`, `blockers`, `warnings`, `missingFields`

### Forbidden Fields
```ts
FORBIDDEN_CORRECTION_FIELDS = [
  'candidateId', 'submittedAt', 'persistedAt', 'previewHash', 'transactionManifestId',
  'resourceId', 'nodeResourceLinkId', 'acceptedAt', 'verifiedAt',
  'reachabilityVerified', 'doiVerified', 'isbnVerified',
  'governingStatus', 'ahjAdoptionStatus', 'complianceStatus',
  'decisions',
];
```

### Rejected Values
- `learnerVisible === true`
- `verificationStatus === 'verified'`
- `displayPolicy` outside `['reviewer_only', 'dev_only']`

### Output Shape
```ts
{
  diff: { changedFields: string[]; before: Record; after: Record };
  blockers: string[];
  warnings: string[];
  missingFields: string[];
  sourceTruthCaveat: string;
}
```

---

## 3. Correction Apply

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Function:** `applyCorrection(repoRoot, candidateId, patch, reviewer, rationale)`

### Behavior
- Gated behind `requireLocalDevAdmin`
- Loads registry, finds candidate
- Re-runs `previewCorrection()` server-side
- **Rejects if preview has blockers**
- Appends decision record with `decisionType: 'apply_metadata_correction'`
- Writes transaction manifest
- **Does NOT create Resource or NodeResourceLink**

### Output
```ts
{
  candidate: ExternalMetadataCandidateRecord;
  decision: ExternalCandidateReviewDecision;
  manifest: { transactionId: string };
}
```

---

## 4. Review Decision Preview

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Function:** `previewReviewDecision(candidate, input)`

### Behavior
- Pure/read-only
- Validates decision type against allowed enum
- Requires `rejectionReasons` for `mark_rejected`
- Requires `duplicateOfCandidateId` for `mark_duplicate`
- Blocks `mark_ready_for_promotion_review` when any promotion readiness gate fails
- Returns `priorStatus`, `proposedNextStatus`, `blockers`, `promotionReadinessChecklist`

---

## 5. Review Decision Apply

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Function:** `applyReviewDecision(repoRoot, candidateId, input)`

### Behavior
- Gated behind `requireLocalDevAdmin`
- Re-runs `previewReviewDecision()` server-side
- Rejects if preview has blockers
- Updates `candidate.status` to `proposedNextStatus`
- Appends decision record
- Writes transaction manifest
- **Does NOT create Resource or NodeResourceLink**

---

## 6. Promotion Readiness Helper

**File:** `api/resourceLayer/externalCandidateReview.ts`  
**Function:** `buildExternalCandidatePromotionReadiness(candidate)`

### 8 Gates
| Gate | Check |
|------|-------|
| Identity | `candidateId` present and valid format |
| Source Metadata | Title, resourceType, proposedUrl present and non-placeholder |
| Rights | `rightsStatus` not `'unknown'` or `'pending'` |
| Verification | `verificationStatus` not `'unverified'` or `'pending'` |
| Standards | `standardContext` present for standard-type candidates |
| Node Link | `nodeResourceLinkId` already exists (optional gate) |
| Display | `displayPolicy` is `'reviewer_only'` or `'dev_only'` |
| Transaction | `transactionManifestId` present (proof of prior review) |

### Safety
- Read-only helper — no mutation
- Called by preview and apply before status transitions to `ready_for_promotion_review`

---

## 7. Source-Custody Queue Integration

**File:** `api/resourceLayer/sourceCustodyQueue.ts`  
**Function:** `enrichExternalCandidateItem(candidate)`

### Behavior
- Maps `candidate.status` → `reviewStatus`
- Maps blocked/placeholder → `custodyStatus: 'blocked'`
- Sets `displayPolicy: 'dev_only'` for all external candidates
- Sets `learnerEligible: false`
- Computes `nextReviewAction` based on status

### nextReviewAction Map
| Status | Action |
|--------|--------|
| blocked | Reject placeholder metadata or supply valid values |
| metadata_correction_needed | Apply metadata correction |
| rights_review_needed | Review rights clearance |
| standards_context_needed | Supply edition, jurisdiction, and citation context |
| source_custody_review_needed | Review source custody chain |
| duplicate_candidate | Review duplicate status |
| rejected | Candidate rejected; no further action unless reopened |
| deferred | Candidate deferred; review postponed |
| ready_for_promotion_review | Candidate ready for promotion review; promotion apply not yet implemented |
| promotion_blocked | Resolve promotion blockers before review |

---

## 8. ResourceReviewAdmin UI

**File:** `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`

### Tabs
1. **Detail** — Read-only candidate metadata, safe badges
2. **Correction** — Structured form, preview diff, blocked-field warnings
3. **Review Decision** — Decision type selector, rationale, context source, promotion readiness checklist
4. **History** — Chronological decision records with full audit trail

### Safe Wording Enforced
- "not learner visible"
- "No resource or link will be created"
- "promotion apply not yet implemented"

### Missing Buttons (by design)
- No "Promote to Resource" button
- No "Create NodeResourceLink" button
- No "Auto-verify" button

---

## 9. Tests

### API Tests
**File:** `api/resourceLayerExternalCandidateReview.test.ts`  
**Count:** 26 tests, all passing

| Category | Count |
|----------|-------|
| Correction preview | 4 |
| Correction apply | 4 |
| Review decision preview | 4 |
| Review decision apply | 4 |
| History | 2 |
| Promotion readiness | 2 |
| Learner safety / integration | 4 |
| Cleanup verification | 2 |

### Explorer Tests
**File:** `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`  
**Count:** 10 tests, all passing

### Integration Tests
- Source-custody queue reflects updated candidate status
- Node resources hide candidates from learners
- Registry empty after test cleanup

---

## 10. Phase 6 Resource Evidence Layer Roadmap

### Completed Phases
| Phase | Deliverable |
|-------|-------------|
| 6A | Resource layer schema and registry |
| 6B | Node resource link validation |
| 6C | Source rights registry |
| 6D | Evidence path and custody queue |
| 6E | Standards context workflow |
| 6F | Canonical duplicate review |
| 6G | External metadata candidate persistence |
| 6H | Promotion preview planning |
| 6I | Correction and review decision workflow |
| 6J | Audit remediation (this cleanup) |

### Future Phases (gated)
| Phase | Deliverable | Authorization Required |
|-------|-------------|------------------------|
| 6K | Promotion preview (read-only candidate-to-resource preview) | Explicit project-owner steward |
| 6L | Promotion apply (create Resource and NodeResourceLink) | Separate explicit authorization |

---

## 11. Quality Metrics

### Test Coverage
- API: 328/328 passing
- Explorer: 118/118 passing
- Python: 118/118 passing (2 pre-existing import errors on Windows, unrelated)

### No-Write Validators
- 0 errors, 0 blockers

### Graph Integrity
- 10,018 nodes
- 13,670 base edges
- 13,934 effective edges
- 264 admitted relationships

---

## 12. Validation Log

| Check | Result | Date |
|-------|--------|------|
| Explorer build | ✅ Success | 2026-05-03 |
| API test suite | ✅ 328/328 | 2026-05-03 |
| Explorer test suite | ✅ 118/118 | 2026-05-03 |
| Python test suite | ✅ 118/118 | 2026-05-03 |
| Registry timestamp dirtiness | ✅ Fixed | 2026-05-03 |
| Test flakiness | ✅ Retry added | 2026-05-03 |
| Audit research gap | ✅ Consolidated doc created | 2026-05-03 |

---

## References

- **Independent Audit:** `.ai/02_audits/2026-05-03_phase_6i_external_candidate_correction_review_decision_independent_audit.md`
- **Implementation:** `api/resourceLayer/externalCandidateReview.ts`
- **Persistence:** `api/resourceLayer/externalCandidateRegistry.ts`
- **UI:** `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- **Routes:** `api/index.ts` (lines ~4600–4700)
