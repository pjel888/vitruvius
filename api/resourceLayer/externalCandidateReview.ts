import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { ExternalMetadataCandidatePreview } from './externalMetadataCandidates';
import {
  detectExternalMetadataPlaceholders,
  validateExternalMetadataCandidate,
} from './externalMetadataCandidates';
import type { ExternalMetadataCandidateRecord } from './externalCandidateRegistry';
import { loadExternalCandidateRegistry, saveRegistry as saveExternalCandidateRegistry } from './externalCandidateRegistry';
import { withResourceLayerTransaction } from './transactionManifest';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ExternalCandidateReviewStatus =
  | 'candidate'
  | 'needs_review'
  | 'metadata_correction_needed'
  | 'source_custody_review_needed'
  | 'rights_review_needed'
  | 'standards_context_needed'
  | 'duplicate_candidate'
  | 'rejected'
  | 'deferred'
  | 'ready_for_promotion_review'
  | 'promotion_blocked';

export type ExternalCandidateDecisionType =
  | 'mark_needs_review'
  | 'request_metadata_correction'
  | 'request_source_custody_review'
  | 'request_rights_review'
  | 'request_standards_context'
  | 'mark_duplicate'
  | 'reject_candidate'
  | 'defer_candidate'
  | 'mark_ready_for_promotion_review'
  | 'block_promotion'
  | 'apply_metadata_correction';

export interface PromotionReadinessChecklist {
  identityGate: boolean;
  sourceMetadataGate: boolean;
  rightsGate: boolean;
  verificationGate: boolean;
  standardsGate: boolean;
  nodeLinkGate: boolean;
  displayGate: boolean;
  transactionGate: boolean;
}

export interface ExternalCandidateReviewDecision {
  decisionId: string;
  candidateId: string;
  decisionType: ExternalCandidateDecisionType;
  priorStatus: ExternalCandidateReviewStatus;
  nextStatus: ExternalCandidateReviewStatus;
  reviewer: string;
  reviewedAt: string;
  rationale: string;
  sourceOfContext: string;
  correctionPatch?: Partial<ExternalMetadataCandidatePreview>;
  warningFlags?: string[];
  missingFields?: string[];
  rejectionReasons?: string[];
  duplicateOfCandidateId?: string;
  duplicateOfResourceId?: string;
  promotionReadinessChecklist?: PromotionReadinessChecklist;
  rightsStatusAssessment?: {
    status: string;
    protectedContent: boolean;
    licensedInternalUseOnly: boolean;
    reviewerRationale: string;
  };
  verificationStatusAssessment?: {
    syntaxValid: boolean;
    externalVerified: false;
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
  noAutoPromotion: true;
  noAutoLinking: true;
  noLearnerExposure: true;
  auditCaveat: string;
}

export interface CorrectionPreviewResult {
  candidateId: string;
  before: ExternalMetadataCandidateRecord;
  afterPreview: ExternalMetadataCandidateRecord;
  diff: { changedFields: string[] };
  blockers: string[];
  warnings: string[];
  missingFields: string[];
  promotionReadinessChecklist: PromotionReadinessChecklist;
  learnerVisible: false;
  verificationStatus: 'unverified';
  displayPolicy: 'reviewer_only' | 'dev_only';
  sourceTruthCaveat: string;
}

export interface ReviewDecisionPreviewResult {
  candidateId: string;
  priorStatus: ExternalCandidateReviewStatus;
  proposedNextStatus: ExternalCandidateReviewStatus;
  requiredFields: string[];
  missingFields: string[];
  blockers: string[];
  warnings: string[];
  promotionReadinessChecklist: PromotionReadinessChecklist;
  sourceTruthCaveat: string;
  safetyFlags: { noAutoPromotion: true; noAutoLinking: true; noLearnerExposure: true };
}

export interface ApplyResult {
  candidate: ExternalMetadataCandidateRecord;
  decision: ExternalCandidateReviewDecision;
  manifest: { transactionId: string };
}

// ---------------------------------------------------------------------------
// Promotion Readiness Helper
// ---------------------------------------------------------------------------

export function buildExternalCandidatePromotionReadiness(
  candidate: ExternalMetadataCandidateRecord,
): { checklist: PromotionReadinessChecklist; blockers: string[]; warnings: string[] } {
  const blockers: string[] = [];
  const warnings: string[] = [];

  // Gate A: Identity
  const identityGate =
    Boolean(candidate.candidateId) &&
    Boolean(candidate.title?.trim()) &&
    candidate.fakePlaceholderFlags.length === 0;
  if (!identityGate) blockers.push('Identity gate failed: missing candidateId, title, or placeholder detected');

  // Gate B: Source Metadata
  const hasUrl = Boolean(candidate.proposedUrl);
  const hasDoi = Boolean(candidate.proposedDoi);
  const hasIsbn = Boolean(candidate.proposedIsbn);
  const sourceMetadataGate = hasUrl || hasDoi || hasIsbn;
  if (!sourceMetadataGate) blockers.push('Source metadata gate failed: no URL, DOI, or ISBN');

  // Gate C: Rights
  const rightsGate = candidate.proposedRightsStatus !== undefined && candidate.proposedRightsStatus !== '';
  if (!rightsGate) warnings.push('Rights gate: rightsStatus not explicitly set');

  // Gate D: Verification
  const verificationGate = candidate.verificationStatus === 'unverified';
  if (!verificationGate) blockers.push('Verification gate failed: verificationStatus must be unverified');

  // Gate E: Standards
  let standardsGate = true;
  if (candidate.resourceType === 'standard_candidate' || candidate.resourceType === 'guide_candidate') {
    const hasEdition = Boolean(candidate.proposedEdition);
    const hasVersion = Boolean(candidate.proposedVersion);
    const hasJurisdiction = Boolean(candidate.proposedJurisdiction);
    const hasScope = Boolean(candidate.proposedScope);
    standardsGate = (hasEdition || hasVersion) && (hasJurisdiction || hasScope);
    if (!standardsGate) {
      blockers.push('Standards gate failed: standard candidate missing edition/version or jurisdiction/scope');
    }
  }

  // Gate F: Node Link
  const nodeLinkGate = true; // Proposed nodes are optional; no links created yet
  if (candidate.proposedNodeIds && candidate.proposedNodeIds.length > 0 && !candidate.proposedRelation) {
    warnings.push('Node-link gate: proposedNodeIds present but proposedRelation missing');
  }

  // Gate G: Display
  const displayGate = candidate.learnerVisible === false && (candidate.displayPolicy === 'reviewer_only' || candidate.displayPolicy === 'dev_only');
  if (!displayGate) blockers.push('Display gate failed: learnerVisible must be false and displayPolicy must be reviewer_only or dev_only');

  // Gate H: Transaction
  const transactionGate = Boolean(candidate.transactionManifestId);
  if (!transactionGate) warnings.push('Transaction gate: candidate persisted before transaction manifest tracking');

  // Status blockers
  if (candidate.status === 'rejected') blockers.push('Candidate status is rejected');
  if (candidate.status === 'duplicate_candidate') blockers.push('Candidate status is duplicate');
  if (candidate.status === 'deferred') blockers.push('Candidate status is deferred');
  if (candidate.status === 'promotion_blocked') blockers.push('Candidate status is promotion_blocked');

  return {
    checklist: {
      identityGate,
      sourceMetadataGate,
      rightsGate,
      verificationGate,
      standardsGate,
      nodeLinkGate,
      displayGate,
      transactionGate,
    },
    blockers,
    warnings,
  };
}

// ---------------------------------------------------------------------------
// Correction Preview
// ---------------------------------------------------------------------------

const FORBIDDEN_CORRECTION_FIELDS = new Set<string>([
  'candidateId',
  'submittedAt',
  'persistedAt',
  'previewHash',
  'transactionManifestId',
  'resourceId',
  'nodeResourceLinkId',
  'acceptedAt',
  'verifiedAt',
  'reachabilityVerified',
  'doiVerified',
  'isbnVerified',
  'governingStatus',
  'ahjAdoptionStatus',
  'complianceStatus',
  'decisions',
]);

function decisionTypeForStatus(status: ExternalCandidateReviewStatus): ExternalCandidateDecisionType {
  const map: Record<string, ExternalCandidateDecisionType> = {
    needs_review: 'mark_needs_review',
    metadata_correction_needed: 'request_metadata_correction',
    source_custody_review_needed: 'request_source_custody_review',
    rights_review_needed: 'request_rights_review',
    standards_context_needed: 'request_standards_context',
    duplicate_candidate: 'mark_duplicate',
    rejected: 'reject_candidate',
    deferred: 'defer_candidate',
    ready_for_promotion_review: 'mark_ready_for_promotion_review',
    promotion_blocked: 'block_promotion',
  };
  return map[status] || 'mark_needs_review';
}

export function previewCorrection(
  candidate: ExternalMetadataCandidateRecord,
  patch: Partial<ExternalMetadataCandidatePreview>,
  reviewer: string,
  rationale: string,
): CorrectionPreviewResult {
  const blockers: string[] = [];
  const warnings: string[] = [];

  // Forbidden field check
  for (const key of Object.keys(patch)) {
    if (FORBIDDEN_CORRECTION_FIELDS.has(key)) {
      blockers.push(`Correction cannot modify forbidden field: ${key}`);
    }
  }

  // Safety checks on patch values
  if ((patch as any).learnerVisible === true) blockers.push('learnerVisible cannot be set to true');
  if ((patch as any).verificationStatus === 'verified') blockers.push('verificationStatus cannot be set to verified');
  if ((patch as any).displayPolicy && !['reviewer_only', 'dev_only'].includes((patch as any).displayPolicy)) {
    blockers.push('displayPolicy must be reviewer_only or dev_only');
  }

  // Placeholder detection on patched values
  const placeholderInput = {
    title: patch.title ?? candidate.title,
    resourceType: patch.resourceType ?? candidate.resourceType,
    proposedUrl: patch.proposedUrl ?? candidate.proposedUrl,
    proposedDoi: patch.proposedDoi ?? candidate.proposedDoi,
    proposedIsbn: patch.proposedIsbn ?? candidate.proposedIsbn,
    proposedEdition: patch.proposedEdition ?? candidate.proposedEdition,
    proposedVersion: patch.proposedVersion ?? candidate.proposedVersion,
    proposedPublisher: patch.proposedPublisher ?? candidate.proposedPublisher,
    proposedAuthors: patch.proposedAuthors ?? candidate.proposedAuthors,
    proposedScope: patch.proposedScope ?? candidate.proposedScope,
    proposedJurisdiction: patch.proposedJurisdiction ?? candidate.proposedJurisdiction,
  };
  const placeholderFlags = detectExternalMetadataPlaceholders(placeholderInput as any);
  if (placeholderFlags.length > 0) {
    blockers.push(`Placeholder values detected: ${placeholderFlags.join(', ')}`);
  }

  // Build preview record
  const afterPreview: ExternalMetadataCandidateRecord = {
    ...candidate,
    ...patch,
    candidateId: candidate.candidateId,
    submittedAt: candidate.submittedAt,
    persistedAt: candidate.persistedAt,
    previewHash: candidate.previewHash,
    transactionManifestId: candidate.transactionManifestId,
    verificationStatus: 'unverified',
    displayPolicy: patch.displayPolicy ?? candidate.displayPolicy,
    learnerVisible: false,
    noAutoVerification: true,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
  };

  // Validate
  const validation = validateExternalMetadataCandidate(placeholderInput as any);
  if (!validation.ok) {
    blockers.push(...validation.errors);
  }
  warnings.push(...validation.warnings);

  // Missing fields
  const missingFields: string[] = [];
  if (!afterPreview.proposedUrl) missingFields.push('url');
  if (!afterPreview.proposedDoi) missingFields.push('doi');
  if (!afterPreview.proposedIsbn) missingFields.push('isbn');
  if (!afterPreview.proposedPublisher) missingFields.push('publisher');
  if (!afterPreview.proposedAuthors?.length) missingFields.push('authors');
  if (!afterPreview.proposedPublicationDate) missingFields.push('publicationDate');
  if (!afterPreview.proposedEdition && !afterPreview.proposedVersion) missingFields.push('edition/version');
  if (!afterPreview.proposedJurisdiction && !afterPreview.proposedScope) missingFields.push('jurisdiction/scope');

  // Promotion readiness
  const { checklist, blockers: readinessBlockers, warnings: readinessWarnings } = buildExternalCandidatePromotionReadiness(afterPreview);
  blockers.push(...readinessBlockers);
  warnings.push(...readinessWarnings);

  const changedFields = Object.keys(patch).filter((k) => {
    const beforeVal = (candidate as any)[k];
    const afterVal = (afterPreview as any)[k];
    return JSON.stringify(beforeVal) !== JSON.stringify(afterVal);
  });

  return {
    candidateId: candidate.candidateId,
    before: candidate,
    afterPreview,
    diff: { changedFields },
    blockers: Array.from(new Set(blockers)),
    warnings: Array.from(new Set(warnings)),
    missingFields,
    promotionReadinessChecklist: checklist,
    learnerVisible: false,
    verificationStatus: 'unverified',
    displayPolicy: afterPreview.displayPolicy,
    sourceTruthCaveat: 'This is unverified candidate metadata. No external verification has been performed.',
  };
}

// ---------------------------------------------------------------------------
// Correction Apply
// ---------------------------------------------------------------------------

export function applyCorrection(
  repoRoot: string,
  candidateId: string,
  patch: Partial<ExternalMetadataCandidatePreview>,
  reviewer: string,
  rationale: string,
): ApplyResult {
  const registry = loadExternalCandidateRegistry(repoRoot);
  const candidate = registry.candidates.find((c) => c.candidateId === candidateId);
  if (!candidate) throw new Error(`Candidate not found: ${candidateId}`);

  const preview = previewCorrection(candidate, patch, reviewer, rationale);
  if (preview.blockers.length > 0) {
    throw new Error(`Correction blocked: ${preview.blockers.join('; ')}`);
  }

  const decision: ExternalCandidateReviewDecision = {
    decisionId: `ext-dec-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    candidateId,
    decisionType: 'apply_metadata_correction',
    priorStatus: candidate.status as ExternalCandidateReviewStatus,
    nextStatus: candidate.status as ExternalCandidateReviewStatus,
    reviewer,
    reviewedAt: new Date().toISOString(),
    rationale,
    sourceOfContext: 'manual_review',
    correctionPatch: patch,
    warningFlags: preview.warnings,
    missingFields: preview.missingFields,
    promotionReadinessChecklist: preview.promotionReadinessChecklist,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
    auditCaveat: 'Correction applied to candidate metadata only. No resource or link created.',
  };

  const updated: ExternalMetadataCandidateRecord = {
    ...preview.afterPreview,
    decisions: [...(candidate.decisions || []), decision],
  };

  const idx = registry.candidates.findIndex((c) => c.candidateId === candidateId);
  registry.candidates[idx] = updated;

  const { manifest } = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_correction',
    [registryPath(repoRoot)],
    () => {
      saveExternalCandidateRegistry(repoRoot, registry);
      return updated;
    },
  );

  updated.transactionManifestId = manifest.transactionId;
  return { candidate: updated, decision, manifest: { transactionId: manifest.transactionId } };
}

// ---------------------------------------------------------------------------
// Review Decision Preview
// ---------------------------------------------------------------------------

export interface ReviewDecisionInput {
  reviewer: string;
  rationale: string;
  sourceOfContext?: string;
  decisionType: ExternalCandidateDecisionType;
  duplicateOfCandidateId?: string;
  duplicateOfResourceId?: string;
  rejectionReasons?: string[];
  deferUntil?: string;
  nextReviewTrigger?: string;
  missingFields?: string[];
}

export function previewReviewDecision(
  candidate: ExternalMetadataCandidateRecord,
  input: ReviewDecisionInput,
): ReviewDecisionPreviewResult {
  const blockers: string[] = [];
  const warnings: string[] = [];
  const requiredFields: string[] = [];
  const missingFields: string[] = [];

  // Validate reviewer/rationale
  if (!input.reviewer?.trim()) blockers.push('reviewer is required');
  if (!input.rationale?.trim()) blockers.push('rationale is required');

  const priorStatus = candidate.status as ExternalCandidateReviewStatus;
  let proposedNextStatus: ExternalCandidateReviewStatus = priorStatus;

  switch (input.decisionType) {
    case 'mark_needs_review':
      proposedNextStatus = 'needs_review';
      break;
    case 'request_metadata_correction':
      proposedNextStatus = 'metadata_correction_needed';
      if (!input.missingFields?.length) warnings.push('No missing fields specified for metadata correction');
      break;
    case 'request_source_custody_review':
      proposedNextStatus = 'source_custody_review_needed';
      break;
    case 'request_rights_review':
      proposedNextStatus = 'rights_review_needed';
      break;
    case 'request_standards_context':
      proposedNextStatus = 'standards_context_needed';
      if (candidate.resourceType !== 'standard_candidate' && candidate.resourceType !== 'guide_candidate') {
        blockers.push('Standards context review only applies to standard_candidate or guide_candidate');
      }
      break;
    case 'mark_duplicate':
      proposedNextStatus = 'duplicate_candidate';
      if (!input.duplicateOfCandidateId && !input.duplicateOfResourceId) {
        blockers.push('duplicate decision requires duplicateOfCandidateId or duplicateOfResourceId');
      }
      break;
    case 'reject_candidate':
      proposedNextStatus = 'rejected';
      if (!input.rejectionReasons?.length) blockers.push('rejection decision requires rejectionReasons');
      break;
    case 'defer_candidate':
      proposedNextStatus = 'deferred';
      break;
    case 'mark_ready_for_promotion_review':
      proposedNextStatus = 'ready_for_promotion_review';
      break;
    case 'block_promotion':
      proposedNextStatus = 'promotion_blocked';
      break;
    default:
      blockers.push(`Unknown decision type: ${input.decisionType}`);
  }

  // Check promotion readiness for ready_for_promotion_review
  if (input.decisionType === 'mark_ready_for_promotion_review') {
    const { blockers: readinessBlockers } = buildExternalCandidatePromotionReadiness(candidate);
    if (readinessBlockers.length > 0) {
      blockers.push(...readinessBlockers);
      blockers.push('Cannot mark ready_for_promotion_review: promotion readiness gates not satisfied');
    }
  }

  const { checklist } = buildExternalCandidatePromotionReadiness(candidate);

  return {
    candidateId: candidate.candidateId,
    priorStatus,
    proposedNextStatus,
    requiredFields,
    missingFields,
    blockers: Array.from(new Set(blockers)),
    warnings: Array.from(new Set(warnings)),
    promotionReadinessChecklist: checklist,
    sourceTruthCaveat: 'This is a review decision preview. No resource or link will be created.',
    safetyFlags: { noAutoPromotion: true, noAutoLinking: true, noLearnerExposure: true },
  };
}

// ---------------------------------------------------------------------------
// Review Decision Apply
// ---------------------------------------------------------------------------

export function applyReviewDecision(
  repoRoot: string,
  candidateId: string,
  input: ReviewDecisionInput,
): ApplyResult {
  const registry = loadExternalCandidateRegistry(repoRoot);
  const candidate = registry.candidates.find((c) => c.candidateId === candidateId);
  if (!candidate) throw new Error(`Candidate not found: ${candidateId}`);

  const preview = previewReviewDecision(candidate, input);
  if (preview.blockers.length > 0) {
    throw new Error(`Review decision blocked: ${preview.blockers.join('; ')}`);
  }

  const decision: ExternalCandidateReviewDecision = {
    decisionId: `ext-dec-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    candidateId,
    decisionType: input.decisionType,
    priorStatus: preview.priorStatus,
    nextStatus: preview.proposedNextStatus,
    reviewer: input.reviewer,
    reviewedAt: new Date().toISOString(),
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext || 'manual_review',
    duplicateOfCandidateId: input.duplicateOfCandidateId,
    duplicateOfResourceId: input.duplicateOfResourceId,
    rejectionReasons: input.rejectionReasons,
    promotionReadinessChecklist: preview.promotionReadinessChecklist,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
    auditCaveat: 'Review decision applied to candidate status only. No resource or link created.',
  };

  const updated: ExternalMetadataCandidateRecord = {
    ...candidate,
    status: preview.proposedNextStatus,
    decisions: [...(candidate.decisions || []), decision],
  };

  const idx = registry.candidates.findIndex((c) => c.candidateId === candidateId);
  registry.candidates[idx] = updated;

  const { manifest } = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_review_decision',
    [registryPath(repoRoot)],
    () => {
      saveExternalCandidateRegistry(repoRoot, registry);
      return updated;
    },
  );

  updated.transactionManifestId = manifest.transactionId;
  return { candidate: updated, decision, manifest: { transactionId: manifest.transactionId } };
}

// ---------------------------------------------------------------------------
// Decision History
// ---------------------------------------------------------------------------

export function getCandidateDecisionHistory(
  repoRoot: string,
  candidateId: string,
): ExternalCandidateReviewDecision[] {
  const registry = loadExternalCandidateRegistry(repoRoot);
  const candidate = registry.candidates.find((c) => c.candidateId === candidateId);
  if (!candidate) return [];
  return candidate.decisions || [];
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function registryPath(repoRoot: string): string {
  return resolve(repoRoot, '006_System-Manifests', 'resource-layer', 'external-metadata-candidates.json');
}

