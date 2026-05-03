# Phase 6L Promotion Transaction and Rollback Model

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## Transaction Requirements

Promotion apply MUST use the existing `withResourceLayerTransaction()` wrapper.

### Transaction Manifest Fields

```ts
interface PromotionTransactionManifest extends ResourceLayerTransactionManifest {
  operationType:
    | 'external_candidate_resource_promotion'
    | 'external_candidate_link_promotion'
    | 'external_candidate_resource_and_link_promotion';
  subsystem: 'resource_layer';
  actor: string;                    // reviewer identity
  candidateId: string;
  createdResourceIds: string[];
  createdLinkIds: string[];
  promotionDecisionId: string;
  reviewerRationale: string;
  sourceOfContext: string;
  applyMode: 'resource_only' | 'resource_and_links';
  rollbackPlan: RollbackPlan;
  noGraphMutation: true;
  noExternalVerification: true;
  noLearnerExposure: true;
}
```

### Files Touched

| Apply Mode | Files Touched |
|---|---|
| Resource-only | `resources.json`, `external-metadata-candidates.json` |
| Resource + links | `resources.json`, `node-resource-links.json`, `external-metadata-candidates.json` |

### Before/After Hashes

- `beforeHashes` computed for each file BEFORE mutation
- `afterHashes` computed for each file AFTER mutation
- Hash algorithm: SHA-256 of file content
- Stored in manifest for integrity verification

### Manifest Chaining

- `previousManifestHash` points to most recent manifest in `transaction-manifests/`
- Creates auditable chain of mutations
- Enables chronological reconstruction of all changes

---

## Rollback Plan

Every promotion transaction manifest must include a `rollbackPlan`:

```ts
interface RollbackPlan {
  strategy: 'delete_created' | 'mark_rolled_back' | 'manual_intervention_required';
  resourceIds: string[];
  linkIds: string[];
  dependencies: {
    resourceHasOtherLinks: boolean;  // If true, cannot delete resource
    linksHaveDownstreamReferences: boolean;  // If true, cannot delete links
  };
  estimatedComplexity: 'simple' | 'moderate' | 'complex';
  manualSteps?: string[];
}
```

### Rollback Strategy Selection

| Condition | Strategy |
|---|---|
| Resource has no other links | `delete_created` — safe to delete resource and all links |
| Resource has other links | `mark_rolled_back` — keep resource, mark promoted links rolled_back |
| Links have downstream evidence claims | `manual_intervention_required` — requires human review |

### Rollback Execution

1. Load original promotion manifest by `promotionDecisionId`
2. Verify rollback requester identity
3. Compute current file hashes
4. Compare to `afterHashes` from promotion manifest
- If match → no intervening changes, safe to rollback
- If mismatch → warn about drift, require force flag
5. Execute rollback strategy:
   - `delete_created`: Remove resource/link records from JSON arrays
   - `mark_rolled_back`: Update status fields, preserve records for audit
6. Write rollback transaction manifest
7. Append rollback decision to candidate history

### Rollback Transaction Manifest

```ts
interface RollbackTransactionManifest extends ResourceLayerTransactionManifest {
  operationType: 'external_candidate_promotion_rollback';
  rolledBackPromotionDecisionId: string;
  rollbackStrategy: string;
  resourcesAffected: string[];
  linksAffected: string[];
  originalManifestHash: string;
}
```

---

## Audit Preservation

- Rollback does NOT delete candidate history
- Rollback appends a new decision record to candidate history
- Original promotion decision remains visible
- Rollback decision references original decision
- Full audit trail preserved for compliance

---

## No Direct File Mutation Rule

All file writes MUST go through:
1. `withResourceLayerTransaction()` wrapper
2. `deterministicWrite()` helper
3. Transaction manifest generation
4. Hash verification

Never:
- `fs.writeFileSync(path, content)` directly on production files
- `JSON.stringify` + write without transaction wrapper
- Modify files outside the declared `filesTouched` list
