# Phase 6N — Resource-Only Promotion Apply Contract

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Implementation contract

---

## 1. Definition

Resource-only promotion apply creates exactly one Resource record from one external metadata candidate. It creates zero nodeResourceLinks, zero graph edges, zero canonical mutations, zero learner exposure, and performs zero external verification. It writes a transaction manifest and appends candidate history.

---

## 2. Contract

### Input

```typescript
interface ResourceOnlyApplyInput {
  candidateId: string;
  applyMode: 'resource_only';
  reviewer: string;
  rationale: string;
  sourceOfContext: string;
  previewHash: string;
  acknowledgeWarnings: boolean;
  promotionCaveat: string;
}
```

### Output (Success)

```typescript
interface ResourceOnlyApplyResult {
  success: true;
  candidateId: string;
  applyMode: 'resource_only';
  createdResourceId: string;
  createdNodeResourceLinkIds: [];
  learnerVisible: false;
  externalVerificationPerformed: false;
  graphMutationApplied: false;
  canonicalMutationApplied: false;
  nodeLinksCreated: 0;
  transactionManifestId: string;
  rollbackPlan: {
    resourcesToRemove: string[];
    linksToRemove: string[];
    rollbackType: 'hard_delete' | 'mark_rolled_back';
  };
  sourceTruthCaveat: string;
  standardsContextCaveat: string | null;
  rightsCaveat: string | null;
  verificationCaveat: string;
}
```

### Output (Failure)

```typescript
interface ResourceOnlyApplyFailure {
  success: false;
  gate: string; // e.g., 'B4'
  message: string;
  severity: 'stop';
  blockingGates: string[];
}
```

---

## 3. Safe Defaults for Created Resource

| Field | Value | Rationale |
|-------|-------|-----------|
| `resourceId` | Generated UUID (`res_<uuid>`) | Unique identifier |
| `custodyStatus` | `source_candidate_promoted` | Promoted from candidate, not yet fully reviewed |
| `verificationStatus` | `unverified` | No external verification performed |
| `displayPolicy` | `reviewer_only` | Not learner-visible |
| `learnerVisibleDefault` | `false` | Must not be learner-visible |
| `warningFlags` | `["not_externally_verified", "reviewer_curated_only"]` | Transparency about limitations |
| `sourceTruthCaveat` | `"Source metadata curated by reviewer; not externally verified"` | Honest caveat |
| `verificationCaveat` | `"No external verification performed; URL/DOI/ISBN not verified for reachability or existence"` | Honest caveat |

---

## 4. Forbidden Output Claims

- `currentStandard: true` — Not allowed
- `governing: true` — Not allowed
- `compliant: true` — Not allowed
- `ahjAccepted: true` — Not allowed
- `urlReachable: true` — Not allowed
- `doiVerified: true` — Not allowed
- `isbnVerified: true` — Not allowed
- `sourceVerified: true` — Not allowed
- `official: true` — Not allowed
- `acceptedForLearner: true` — Not allowed

---

## 5. Rollback Contract

### Rollback Preview (Read-Only)

```typescript
interface RollbackPreviewResult {
  candidateId: string;
  promotionDecisionId: string;
  resourceId: string;
  rollbackPlan: {
    action: 'hard_delete' | 'mark_rolled_back';
    notes: string;
  };
  preRollbackStateSummary: {
    resourcesBefore: number;
    linksBefore: number;
  };
  canRollback: true;
}
```

### Rollback Apply

```typescript
interface RollbackApplyInput {
  promotionDecisionId: string;
  reviewer: string;
  rationale: string;
  rollbackAction: 'hard_delete' | 'mark_rolled_back';
}

interface RollbackApplyResult {
  success: true;
  rollbackTransactionManifestId: string;
  action: 'hard_delete' | 'mark_rolled_back';
  resourcesAffected: string[];
  linksAffected: [];
  candidateHistoryUpdated: true;
}
```

---

## 6. Non-Negotiable Safety Guarantees

1. Resource-only promotion NEVER creates nodeResourceLinks
2. Resource-only promotion NEVER sets learnerVisible to true
3. Resource-only promotion NEVER claims source verification
4. Resource-only promotion NEVER mutates graph/canonical registries
5. Resource-only promotion ALWAYS writes a transaction manifest
6. Resource-only promotion ALWAYS records a rollback plan
7. Resource-only promotion ALWAYS requires reviewer/rationale/sourceOfContext
8. Resource-only promotion ALWAYS fails closed on any gate failure
9. Resource-only promotion NEVER auto-promotes a candidate
10. Resource-only promotion blocks ASCE 7 and ACI 318 without real context
