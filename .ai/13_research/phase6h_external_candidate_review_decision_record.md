# Phase 6H External Candidate Review Decision Record

**Date:** 2026-05-03
**Status:** Planning

## Record Shape

```typescript
interface ExternalCandidateReviewDecision {
  // Identity
  decisionId: string;           // uuid or deterministic hash
  candidateId: string;          // references external-metadata-candidates.json
  priorStatus: string;          // state before this decision
  nextStatus: string;           // state after this decision

  // Decision metadata
  decisionType: 'correction' | 'review_decision' | 'promotion_readiness_review';
  reviewer: string;             // required for all non-trivial decisions
  reviewedAt: string;           // ISO 8601
  rationale: string;            // required, min length enforced

  // Context and provenance
  sourceOfContext: string;      // e.g. "manual_review", "rights_audit", "standards_check"
  correctionPatch?: Partial<ExternalMetadataCandidatePreview>;

  // Assessment fields
  warningFlags?: string[];
  missingFields?: string[];
  rejectionReasons?: string[];
  duplicateOfCandidateId?: string;
  duplicateOfResourceId?: string;

  // Promotion readiness
  promotionReadinessChecklist?: {
    identityGate: boolean;
    sourceMetadataGate: boolean;
    rightsGate: boolean;
    verificationGate: boolean;
    standardsGate: boolean;
    nodeLinkGate: boolean;
    displayGate: boolean;
    transactionGate: boolean;
  };

  // Assessments
  rightsStatusAssessment?: {
    status: string;
    protectedContent: boolean;
    licensedInternalUseOnly: boolean;
    reviewerRationale: string;
  };
  verificationStatusAssessment?: {
    syntaxValid: boolean;
    externalVerified: false;    // always false unless future workflow exists
    reviewerConfidence: 'low' | 'medium' | 'high';
  };
  standardsContextAssessment?: {
    editionPresent: boolean;
    versionPresent: boolean;
    jurisdictionPresent: boolean;
    scopePresent: boolean;
    placeholderDetected: boolean;
    missingContextFields: string[];
  };

  // Safety flags
  noAutoPromotion: true;
  noAutoLinking: true;
  noLearnerExposure: true;

  // Audit
  auditCaveat: string;
}
```

## Rules

### correctionPatch
- CANNOT create `resourceId`.
- CANNOT create `nodeResourceLinkId`.
- CANNOT set `learnerVisible=true`.
- CANNOT set `verificationStatus='verified'`.
- CANNOT use placeholder values for edition/version/scope.
- MUST preserve `candidateId`, `submittedAt`, `previewHash`.

### Reviewer Requirements
- `reviewer` and `rationale` are required for all decisions except trivial self-corrections.
- `sourceOfContext` is required to distinguish manual review from automated checks.

### Rejection
- Rejected candidates keep full history.
- `rejectionReasons` must be explicit (e.g. "placeholder URL", "duplicate of X", "rights unclear").

### Duplicates
- `duplicate_candidate` status does NOT delete the record.
- Links to the canonical candidate or resource via `duplicateOfCandidateId` / `duplicateOfResourceId`.

## Decision History Storage

Decisions are stored in a separate file to preserve candidate immutability:

```
006_System-Manifests/resource-layer/external-candidate-decisions.json
```

Each candidate references its decision history by `candidateId`. The candidate record itself only stores `status` and `transactionManifestId`.
