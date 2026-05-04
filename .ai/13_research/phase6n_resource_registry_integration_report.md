# Phase 6N — Resource Registry Integration Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Registry integration complete

---

## 1. Resource Registry Changes

### New File: `api/resourceLayer/externalCandidatePromotionApply.ts`

This file implements the core promotion apply logic including:
- Resource record creation
- Registry read/write operations
- Transaction manifest creation
- Rollback logic

### Files Modified

| File | Change |
|------|--------|
| `api/resourceLayer/resources.json` | Appended with new Resource records on promotion apply |
| `api/resourceLayer/transactionManifests.json` | Appended with new transaction manifests |
| `api/resourceLayer/externalMetadataCandidates.json` | Candidate history updated with promotion decision |

### Files NOT Modified

| File | Reason |
|------|--------|
| Graph/canonical registries | No graph mutation in Phase 6N |
| nodeResourceLinks.json | No links created in resource_only mode |
| Review decisions registries | Candidate decisions stored in candidate record itself |

---

## 2. Resource Record Shape

The Resource record created by promotion apply includes all fields specified in the Phase 6L design:

```typescript
interface ResourceRecord {
  resourceId: string;              // res_<uuid>
  title: string;
  resourceType: string;
  sourceType: string;
  url: string | null;
  doi: string | null;
  isbn: string | null;
  localPath: string | null;
  sourceFamilyId: string | null;
  rightsStatus: string;
  verificationStatus: 'unverified';  // Always unverified
  custodyStatus: 'source_candidate_promoted';
  displayPolicy: 'reviewer_only';
  warningFlags: string[];
  sourceContext: string | null;
  reviewer: string;
  reviewedAt: string;
  rationale: string;
  sourceOfContext: string;
  createdFromExternalCandidateId: string;
  promotionDecisionId: string;
  transactionManifestId: string;
  sourceTruthCaveat: string;
  standardsContextCaveat: string | null;
  rightsCaveat: string | null;
  protectedContentCaveat: string | null;
  learnerVisibleDefault: false;
  rollbackInfo: null | RollbackInfo;
}
```

---

## 3. Duplicate Detection

Duplicate detection checks the following combinations:

| Match Type | Example |
|------------|---------|
| Exact URL match | `resource.url === candidate.url` |
| Exact DOI match | `resource.doi === candidate.doi` |
| Exact ISBN match | `resource.isbn === candidate.isbn` |
| Title + sourceType match | Case-insensitive title + exact sourceType |

All duplicates return a block with gate B7 and a message indicating the existing resource ID.

---

## 4. Resource ID Generation

Resources use a deterministic prefix pattern:

- Format: `res_<uuid>`
- UUID v4 is used for uniqueness
- No sequential IDs to prevent collision

Transaction manifests use `tm_<uuid>` and promotion decisions use `pd_<uuid>`.

---

## 5. Safe Defaults

| Field | Value | Rationale |
|-------|-------|-----------|
| `custodyStatus` | `source_candidate_promoted` | Promoted from candidate, needs review |
| `verificationStatus` | `unverified` | No external verification done |
| `displayPolicy` | `reviewer_only` | Not learner-visible |
| `learnerVisibleDefault` | `false` | Must not be learner-visible |
| `warningFlags` | `["not_externally_verified", "reviewer_curated_only"]` | Transparent caveats |

---

## 6. Transaction Manifests

Each promotion creates a transaction manifest in `api/resourceLayer/transactionManifests.json`.

The manifest records:
- beforeHash / afterHash for each touched file
- operation type (external_candidate_resource_promotion)
- created resource ID
- rollback plan
- no-graph/canonical/external/learner guarantees

---

## 7. Registry Persistence

The implementations use synchronous file I/O (`fs.readFileSync` / `fs.writeFileSync`) for simplicity. In a production deployment, this should be upgraded to atomic file writes with backup.
