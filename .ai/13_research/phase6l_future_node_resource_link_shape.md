# Phase 6L Future NodeResourceLink Record Shape

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## Base Fields (from existing `NodeResourceLink` interface)

```ts
interface NodeResourceLink {
  id: string;
  nodeId: string;
  resourceId: string;
  relationship: NodeResourceRelationship;
  relevanceScore: number;
  authorityScore: number;
  confidenceScore: number;
  rationale: string;
  pageRefs?: string[];
  chapterRefs?: string[];
  sectionRefs?: string[];
  fragmentRefs?: string[];
  matchedTerms?: string[];
  matchedAliases?: string[];
  matchedTaxonomyContext?: string[];
  evidenceClaimIds?: string[];
  supportsEdgeIds?: string[];
  verifiedBy?: 'codex' | 'kimi' | 'human' | 'script';
  reviewStatus: ReviewStatus;
  reviewNotes?: string;
  standardContext?: StandardContext;
  createdAt: string;
  updatedAt: string;
}
```

## Promotion-Specific Fields

```ts
interface LinkPromotionProvenance {
  createdFromExternalCandidateId: string;   // Original candidate ID
  promotionDecisionId: string;              // Decision ID for this promotion apply
  transactionManifestId: string;            // Transaction manifest backing mutation
  linkReviewer: string;                     // Steward who approved this link
  linkRationale: string;                    // Node-specific relevance rationale
  linkSourceOfContext: string;              // Authority source for link approval
  linkReviewedAt: string;                   // ISO timestamp
  linkPromotionCaveat: string;              // Required audit caveat
}
```

## Recommended Safe Defaults for Promoted Links

| Field | Safe Default | Rationale |
|---|---|---|
| `id` | `nrl-{nodeId}-{resourceId}` | Predictable, traceable |
| `reviewStatus` | `'needs_review'` | Links start unreviewed even if resource passes gates |
| `learnerEligible` | Computed by `isLearnerSidebarEligible()` | Never manually asserted |
| `displayPolicy` | `'reviewer_only'` or inherited from resource | No learner exposure by default |
| `relevanceScore` | `0.5` | Neutral starting score |
| `authorityScore` | `0.5` | Neutral starting score |
| `confidenceScore` | `0.5` | Neutral starting score |
| `verifiedBy` | Undefined | No automatic verification |
| `createdAt` | `new Date().toISOString()` | Promotion apply timestamp |
| `updatedAt` | Same as createdAt | Initial promotion |

## Link Acceptance Gate (Future Phase)

For a promoted link to become `accepted`:

1. Resource must be promoted and valid
2. Link must have node-specific rationale
3. Link relationship must be valid
4. Node must exist
5. Rights must not block learner display
6. Standards context must be complete (if standard-type resource)
7. Explicit link review decision must exist
8. Link reviewer/rationale/sourceOfContext must be recorded

## Multi-Link Creation Rule

- If candidate has `proposedNodeIds` with multiple nodes, each node gets its own `NodeResourceLink`
- Each link MUST have node-specific rationale (generic `candidateRationale` is insufficient)
- No bulk-link creation without per-node review
- No automatic linking to parent/child/descendant nodes

## Forbidden Behaviors

| Behavior | Why Forbidden |
|---|---|
| Auto-accept links at promotion time | Links require separate review |
| Create links to non-existent nodes | Graph integrity violation |
| Create links with invalid relationship | Schema violation |
| Create duplicate (nodeId + resourceId + relationship) | Data integrity violation |
| Set `reviewStatus='accepted'` without link review | Bypasses review workflow |
| Set `learnerEligible=true` manually | Must be computed |
| Create graph edges from link metadata | Graph mutation not allowed |
