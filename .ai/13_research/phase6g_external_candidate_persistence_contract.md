# Phase 6G External Candidate Persistence Contract

**Generated:** 2026-05-03T01:00:00+08:00

---

## Persisted Record Shape

`ExternalMetadataCandidateRecord` extends `ExternalMetadataCandidatePreview` with:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| candidateId | string | ✅ | `ext-cand-{slug}-{timestamp}-{rand}` |
| persistedAt | string (ISO) | ✅ | When saved to registry |
| previewHash | string (sha256) | ✅ | Hash of preview output |
| status | `'candidate' \| 'needs_review' \| 'blocked'` | ✅ | Always starts as `candidate` |
| noAutoVerification | `true` | ✅ | Hardcoded |
| noAutoPromotion | `true` | ✅ | Hardcoded |
| noAutoLinking | `true` | ✅ | Hardcoded |
| noLearnerExposure | `true` | ✅ | Hardcoded |
| transactionManifestId | string | optional | Links to transaction manifest |

## Inherited from Preview

All preview fields are persisted:
- title, resourceType, sourceType
- proposedUrl, proposedDoi, proposedIsbn
- proposedPublisher, proposedAuthors, proposedPublicationDate
- proposedEdition, proposedVersion, proposedScope, proposedJurisdiction
- proposedSourceFamilyId, proposedRightsStatus, proposedNodeIds, proposedRelation
- candidateRationale, submittedBy, submittedAt
- verificationStatus, displayPolicy, learnerVisible, reviewRequired
- warningFlags, missingFields, fakePlaceholderFlags, sourceTruthCaveat
- normalizedUrl, normalizedDoi, normalizedIsbn

## Fields NOT Present

- `verifiedAt` — no external verification performed
- `acceptedAt` — not accepted
- `learnerAccepted` — not learner-facing
- `nodeResourceLinkId` — no node links created
- `resourceId` — not promoted to resource
- `reachabilityVerified` — no URL fetch
- `doiVerified` — no DOI lookup
- `isbnVerified` — no ISBN lookup
- `standardsCurrent` — no governing claim
- `governingStatus` — no compliance claim
- `AHJ/adoption status` — no jurisdiction invention
- `complianceStatus` — no compliance claim

---

## Persistence Rules

1. **Preview-first:** Persist route re-runs preview validation server-side.
2. **Error rejection:** If preview has validation errors, persist returns 400.
3. **Placeholder rejection:** If fakePlaceholderFlags is non-empty, persist returns 400.
4. **Hardcoded safety:** learnerVisible=false, displayPolicy=reviewer_only, verificationStatus=unverified.
5. **Duplicate detection:** Same normalized URL/DOI/ISBN or same title without identifier blocks duplicate.
6. **Transaction manifest:** Every persist write creates a manifest with beforeHash/afterHash.
7. **No registry mutation beyond candidate file:** No resources, links, decisions, or graph changes.
