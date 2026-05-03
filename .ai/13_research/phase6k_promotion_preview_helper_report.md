# Phase 6K Promotion Preview Helper Report

**Date:** 2026-05-03
**Status:** Implemented
**File:** `api/resourceLayer/externalCandidatePromotionPreview.ts`

---

## Function

```ts
export function buildExternalCandidatePromotionPreview(
  candidate: ExternalMetadataCandidateRecord,
): PromotionPreviewResult
```

## Properties

| Property | Value |
|---|---|
| Pure | ✅ Yes — no side effects |
| File writes | ❌ None |
| Registry mutation | ❌ None |
| Resource creation | ❌ None |
| NodeResourceLink creation | ❌ None |
| External fetch | ❌ None |
| Reuses readiness helper | ✅ `buildExternalCandidatePromotionReadiness()` |

## Behavior

1. **Status validation** — blocks rejected/deferred/duplicate/promotion_blocked and any status other than `ready_for_promotion_review`
2. **Placeholder check** — blocks if `fakePlaceholderFlags` non-empty
3. **Readiness gates** — runs `buildExternalCandidatePromotionReadiness`, propagates blockers/warnings
4. **Standards context** — for standard/guide candidates, requires edition/version + jurisdiction/scope
5. **Rights check** — warns if `proposedRightsStatus` missing
6. **Learner safety** — blocks if `learnerVisible !== false` or `verificationStatus !== 'unverified'`
7. **Draft generation** — builds `proposedResourceDraft` and `proposedNodeResourceLinkDrafts` only if all gates pass
8. **Link validation** — validates `proposedRelation` against `NODE_RESOURCE_RELATIONSHIPS`

## Output

- `eligibleForPromotionPreview`: true only if zero blockers
- `proposedResourceDraft`: null if ineligible; preview-only draft if eligible
- `proposedNodeResourceLinkDrafts`: empty if ineligible; preview-only drafts if eligible
- All caveats included: sourceTruth, standardsContext, rights, verification
