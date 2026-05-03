import type {
  ExternalCandidateReviewStatus,
  ExternalMetadataCandidateRecord,
  PromotionReadinessChecklist,
} from './externalCandidateReview';
import { buildExternalCandidatePromotionReadiness } from './externalCandidateReview';
import type { NodeResourceRelationship, ResourceType } from './types';
import { NODE_RESOURCE_RELATIONSHIPS } from './types';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ProposedResourceDraft {
  resourceId: string;
  title: string;
  resourceType: ResourceType;
  sourceType?: string;
  url?: string;
  doi?: string;
  isbn10?: string;
  isbn13?: string;
  publisher?: string;
  authors?: string[];
  year?: number;
  edition?: string;
  version?: string;
  scope?: string;
  jurisdiction?: string;
  standardIdentifier?: string;
  disciplineTags: string[];
  taxonomyTags: string[];
  accessType: 'open_access' | 'restricted' | 'reviewer_only' | 'unknown';
  verificationStatus: 'unverified';
  displayPolicy: 'reviewer_only' | 'dev_only';
  learnerVisible: false;
  status: 'draft_preview';
  previewOnly: true;
  noApplyAvailable: true;
}

export interface ProposedNodeResourceLinkDraft {
  linkId: string;
  nodeId: string;
  resourceId: string;
  relationship: NodeResourceRelationship;
  relevanceScore: number;
  authorityScore: number;
  confidenceScore: number;
  rationale: string;
  reviewStatus: 'preview_only';
  learnerVisible: false;
  previewOnly: true;
}

export interface PromotionPreviewResult {
  candidateId: string;
  candidateStatus: ExternalCandidateReviewStatus;
  eligibleForPromotionPreview: boolean;
  proposedResourceDraft: ProposedResourceDraft | null;
  proposedNodeResourceLinkDrafts: ProposedNodeResourceLinkDraft[];
  promotionReadinessChecklist: PromotionReadinessChecklist;
  blockers: string[];
  warnings: string[];
  missingFields: string[];
  sourceTruthCaveat: string;
  standardsContextCaveat: string;
  rightsCaveat: string;
  verificationCaveat: string;
  noApplyAvailable: true;
  createsResource: false;
  createsNodeResourceLink: false;
  learnerVisibleAfterPreview: false;
  externalVerificationPerformed: false;
  transactionRequiredForFutureApply: true;
  rollbackRequiredForFutureApply: true;
}

// ---------------------------------------------------------------------------
// Pure Helper
// ---------------------------------------------------------------------------

export function buildExternalCandidatePromotionPreview(
  candidate: ExternalMetadataCandidateRecord,
): PromotionPreviewResult {
  const blockers: string[] = [];
  const warnings: string[] = [];
  const missingFields: string[] = [];

  // Status blockers — promotion preview requires ready_for_promotion_review
  if (candidate.status === 'rejected') {
    blockers.push('Candidate status is rejected; promotion preview blocked');
  }
  if (candidate.status === 'deferred') {
    blockers.push('Candidate status is deferred; promotion preview blocked');
  }
  if (candidate.status === 'duplicate_candidate') {
    blockers.push('Candidate status is duplicate; promotion preview blocked');
  }
  if (candidate.status === 'promotion_blocked') {
    blockers.push('Candidate status is promotion_blocked; promotion preview blocked');
  }
  if (candidate.status !== 'ready_for_promotion_review') {
    blockers.push(`Candidate status is ${candidate.status}; must be ready_for_promotion_review to preview promotion`);
  }

  // Placeholder metadata blocker
  if (candidate.fakePlaceholderFlags.length > 0) {
    blockers.push(`Placeholder metadata detected: ${candidate.fakePlaceholderFlags.join(', ')}`);
  }

  // Run readiness gates
  const readiness = buildExternalCandidatePromotionReadiness(candidate);
  blockers.push(...readiness.blockers);
  warnings.push(...readiness.warnings);

  // Standards context check
  if (
    candidate.resourceType === 'standard_candidate' ||
    candidate.resourceType === 'guide_candidate'
  ) {
    if (!candidate.proposedEdition && !candidate.proposedVersion) {
      missingFields.push('proposedEdition or proposedVersion');
      blockers.push('Standards context incomplete: missing edition or version');
    }
    if (!candidate.proposedJurisdiction && !candidate.proposedScope) {
      missingFields.push('proposedJurisdiction or proposedScope');
      blockers.push('Standards context incomplete: missing jurisdiction or scope');
    }
  }

  // Rights check
  if (!candidate.proposedRightsStatus || candidate.proposedRightsStatus === '') {
    missingFields.push('proposedRightsStatus');
    warnings.push('Rights status not explicitly set');
  }

  // Learner visibility safety
  if (candidate.learnerVisible !== false) {
    blockers.push('learnerVisible must be false for promotion preview');
  }

  // Verification safety
  if (candidate.verificationStatus !== 'unverified') {
    blockers.push('verificationStatus must be unverified for promotion preview');
  }

  // Determine eligibility
  const eligibleForPromotionPreview = blockers.length === 0;

  // Build proposed resource draft only if eligible
  let proposedResourceDraft: ProposedResourceDraft | null = null;
  if (eligibleForPromotionPreview) {
    const resourceId = `res-${candidate.candidateId.replace(/^ext-cand-/, '')}`;
    proposedResourceDraft = {
      resourceId,
      title: candidate.title,
      resourceType: candidate.resourceType as ResourceType,
      sourceType: candidate.sourceType,
      url: candidate.proposedUrl,
      doi: candidate.proposedDoi,
      isbn10: candidate.proposedIsbn?.length === 10 ? candidate.proposedIsbn : undefined,
      isbn13: candidate.proposedIsbn?.length === 13 ? candidate.proposedIsbn : undefined,
      publisher: candidate.proposedPublisher,
      authors: candidate.proposedAuthors,
      year: candidate.proposedPublicationDate
        ? new Date(candidate.proposedPublicationDate).getFullYear() || undefined
        : undefined,
      edition: candidate.proposedEdition,
      version: candidate.proposedVersion,
      scope: candidate.proposedScope,
      jurisdiction: candidate.proposedJurisdiction,
      standardIdentifier: candidate.proposedEdition
        ? `${candidate.title} ${candidate.proposedEdition}`
        : undefined,
      disciplineTags: [],
      taxonomyTags: [],
      accessType: 'reviewer_only',
      verificationStatus: 'unverified',
      displayPolicy: candidate.displayPolicy,
      learnerVisible: false,
      status: 'draft_preview',
      previewOnly: true,
      noApplyAvailable: true,
    };
  }

  // Build proposed node-resource link drafts
  const proposedNodeResourceLinkDrafts: ProposedNodeResourceLinkDraft[] = [];
  if (eligibleForPromotionPreview && proposedResourceDraft) {
    if (candidate.proposedNodeIds && candidate.proposedNodeIds.length > 0) {
      if (!candidate.proposedRelation) {
        blockers.push('proposedNodeIds present but proposedRelation missing');
      } else if (
        !NODE_RESOURCE_RELATIONSHIPS.includes(candidate.proposedRelation as NodeResourceRelationship)
      ) {
        blockers.push(`proposedRelation '${candidate.proposedRelation}' is not a valid node-resource relationship`);
      } else {
        for (const nodeId of candidate.proposedNodeIds) {
          proposedNodeResourceLinkDrafts.push({
            linkId: `nrl-${nodeId}-${proposedResourceDraft.resourceId}`,
            nodeId,
            resourceId: proposedResourceDraft.resourceId,
            relationship: candidate.proposedRelation as NodeResourceRelationship,
            relevanceScore: 0.5,
            authorityScore: 0.5,
            confidenceScore: 0.5,
            rationale: candidate.candidateRationale || 'Candidate proposed link (preview only)',
            reviewStatus: 'preview_only',
            learnerVisible: false,
            previewOnly: true,
          });
        }
      }
    }
  }

  // Recompute eligibility after link validation
  const finalEligible = blockers.length === 0;

  return {
    candidateId: candidate.candidateId,
    candidateStatus: candidate.status,
    eligibleForPromotionPreview: finalEligible,
    proposedResourceDraft: finalEligible ? proposedResourceDraft : null,
    proposedNodeResourceLinkDrafts: finalEligible ? proposedNodeResourceLinkDrafts : [],
    promotionReadinessChecklist: readiness.checklist,
    blockers,
    warnings,
    missingFields,
    sourceTruthCaveat:
      'This is a preview-only proposed resource draft derived from unverified candidate metadata. No resource has been created. Source truth must be verified before any future promotion apply.',
    standardsContextCaveat:
      'Standards context (edition, version, jurisdiction, scope) is derived from candidate input and has not been independently verified. Do not treat as governing or current.',
    rightsCaveat:
      'Rights status is based on candidate-submitted metadata only. Independent rights review is required before learner exposure or redistribution.',
    verificationCaveat:
      'No external verification (URL reachability, DOI resolution, ISBN lookup) has been performed. verificationStatus remains unverified.',
    noApplyAvailable: true,
    createsResource: false,
    createsNodeResourceLink: false,
    learnerVisibleAfterPreview: false,
    externalVerificationPerformed: false,
    transactionRequiredForFutureApply: true,
    rollbackRequiredForFutureApply: true,
  };
}
