# Phase 6L Future Resource Record Shape

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## Base Fields (from existing `Resource` interface)

```ts
interface Resource {
  id: string;                    // e.g. "res-{candidate-derived-id}"
  title: string;
  subtitle?: string;
  authors?: string[];
  organization?: string;
  publisher?: string;
  year?: number;
  edition?: string;
  resourceType: ResourceType;
  sourceAuthority: SourceAuthority;
  sourceFamilyIds?: string[];
  url?: string;
  canonicalUrl?: string;
  landingPageUrl?: string;
  pdfUrl?: string;
  doi?: string;
  isbn10?: string;
  isbn13?: string;
  disciplineTags: string[];
  taxonomyTags: string[];
  keywords?: string[];
  jurisdiction?: string;
  geographicScope?: GeographicScope;
  standardIdentifier?: StandardIdentifier;
  editionContext?: StandardEditionContext;
  jurisdictionContext?: StandardJurisdictionContext;
  reviewContext?: StandardReviewContext;
  accessType: AccessType;
  sourceRights?: { ... };
  licenseNotes?: string;
  copyrightNotes?: string;
  abstractOrSummary?: string;
  verificationStatus: VerificationStatus;
  lastCheckedAt?: string;
  createdAt: string;
  updatedAt: string;
}
```

## Promotion-Specific Fields (new / required for promoted resources)

```ts
interface PromotionProvenance {
  createdFromExternalCandidateId: string;   // Original candidate ID
  promotionDecisionId: string;              // Unique decision ID for this promotion
  transactionManifestId: string;            // Transaction manifest backing this mutation
  reviewer: string;                         // Steward who approved promotion
  rationale: string;                        // Why this resource was promoted
  sourceOfContext: string;                  // Where reviewer authority came from
  reviewedAt: string;                       // ISO timestamp
  promotionCaveat: string;                  // Required audit caveat
  applyMode: 'resource_only' | 'resource_and_links';
}
```

## Recommended Safe Defaults for Promoted Resources

| Field | Safe Default | Rationale |
|---|---|---|
| `id` | `res-{candidate-derived}` | Predictable, traceable |
| `verificationStatus` | `'unverified'` | Syntax checks are not verification |
| `custodyStatus` | `'source_candidate_promoted'` | Indicates origin, not final acceptance |
| `displayPolicy` | `'reviewer_only'` | No learner exposure by default |
| `learnerVisible` | `false` | Must remain false until link acceptance |
| `accessType` | `'restricted'` or `'unknown'` | Safe default; open_access requires verification |
| `authorityTier` | `4` or `5` | Lower tier for unverified sources |
| `createdAt` | `new Date().toISOString()` | Promotion apply timestamp |
| `updatedAt` | Same as createdAt | Initial promotion |

## Forbidden Fields (unless future workflow proves them)

| Field | Why Forbidden |
|---|---|
| `currentStandard=true` | Requires real standards context verification |
| `governing=true` | Requires jurisdiction/AHJ verification |
| `compliant=true` | Requires compliance review workflow |
| `ahjAccepted=true` | Requires AHJ documentation |
| `urlReachable=true` | Requires real reachability check |
| `doiVerified=true` | Requires real DOI resolution |
| `isbnVerified=true` | Requires real ISBN lookup |
| `sourceVerified=true` | Requires source verification workflow |
| `official=true` | Requires authority verification |
| `acceptedForLearner=true` | Requires accepted nodeResourceLink |

## Caveat Fields

Every promoted resource must carry these caveats:

```ts
interface ResourceCaveats {
  sourceTruthCaveat: string;
  standardsContextCaveat?: string;
  rightsCaveat: string;
  verificationCaveat: string;
  protectedContentCaveat?: string;
}
```

Example values:
- `sourceTruthCaveat`: "This resource was promoted from an external metadata candidate. Source truth has not been independently verified."
- `standardsContextCaveat`: "Standards context is derived from candidate input and has not been independently verified."
- `rightsCaveat`: "Rights status is based on candidate-submitted metadata only."
- `verificationCaveat`: "No external verification (URL reachability, DOI resolution, ISBN lookup) has been performed."
