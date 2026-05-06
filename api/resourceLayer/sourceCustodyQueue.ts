import type { NodeResourceLink, Resource, ResourceCandidate, ResourceLayerData } from './types';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './types';
import { readLocalFileIndex, readResourceLayerData } from './registry';
import {
  isLearnerSidebarEligible,
  isRightsProtectedContent,
  isRightsRestrictedOrProtected,
  isStandardLikeResource,
  standardContextMissingFields,
  hasStructuredMissingContextJustification,
} from './validation';
import { candidateItem, linkItem, localFileItem } from './reviewWorkflow';
import { loadExternalCandidateRegistry, type ExternalMetadataCandidateRecord } from './externalCandidateRegistry';

export type CustodyStatus =
  | 'learner_visible'
  | 'reviewer_only'
  | 'blocked'
  | 'needs_review'
  | 'candidate'
  | 'indexed_only'
  | 'standards_incomplete'
  | 'rights_limited';

export type DisplayPolicy = 'show_to_user' | 'show_warning' | 'dev_only' | 'hidden' | 'blocked';

export interface SourceCustodyItem {
  itemType: 'resource_link' | 'candidate' | 'local_file' | 'external_candidate';
  id: string;
  title: string;
  resourceId?: string;
  nodeId?: string;
  resourceType?: string;
  sourceAuthority?: string;
  reviewStatus: string;
  verificationStatus?: string;
  custodyStatus: CustodyStatus;
  displayPolicy: DisplayPolicy;
  learnerEligible: boolean;
  reviewerOnlyReason?: string;
  hiddenReason?: string;
  warningFlags: string[];
  rightsStatus?: string;
  standardsContextStatus?: string;
  missingStandardContextFields?: string[];
  promotionBlocked?: boolean;
  nextReviewAction?: string;
  // Pass-through of existing review-workflow fields
  authorityTier?: number;
  authorityScore?: number;
  relationship?: string;
  rationale?: string;
  reviewNotes?: string;
  sourceFamilyIds?: string[];
  organization?: string;
  currentEdition?: string;
  currentVersion?: string;
  currentPublicationYear?: number | string;
  currentJurisdiction?: string;
  currentGeographicScope?: string;
  sourceOfContext?: string;
  warnings?: string[];
  rawUrl?: string;
  rawIdentifier?: string;
  preliminaryScore?: number;
  rankingScore?: number;
  dedupeKey?: string;
  duplicateResourceId?: string;
  localPath?: string;
  localFileHash?: string;
  localFileType?: string;
  localFileSizeBytes?: number;
  linkedNodeCount?: number;
  admitted?: boolean;
  admittedResourceId?: string;
  // Underlying objects for advanced use
  resource?: Resource;
  link?: NodeResourceLink;
  candidate?: ResourceCandidate;
}

export interface SourceCustodyQueue {
  schemaVersion: string;
  generatedAt: string;
  groups: {
    learnerVisible: SourceCustodyItem[];
    reviewerOnly: SourceCustodyItem[];
    needsReview: SourceCustodyItem[];
    candidates: SourceCustodyItem[];
    externalCandidates: SourceCustodyItem[];
    localFilesIndexedOnly: SourceCustodyItem[];
    standardsContextIncomplete: SourceCustodyItem[];
    rightsLimited: SourceCustodyItem[];
    rejected: SourceCustodyItem[];
    blocked: SourceCustodyItem[];
  };
  metrics: {
    total: number;
    learnerVisible: number;
    reviewerOnly: number;
    needsReview: number;
    candidates: number;
    externalCandidates: number;
    localFilesIndexedOnly: number;
    standardsContextIncomplete: number;
    rightsLimited: number;
    rejected: number;
    blocked: number;
  };
}

function buildWarningFlags(resource?: Resource, link?: NodeResourceLink, baseWarnings: string[] = []): string[] {
  const flags = [...baseWarnings];
  if (link) {
    if (link.reviewStatus === 'needs_review') flags.push('needs_review');
    if (link.reviewStatus === 'candidate') flags.push('candidate');
    if (link.reviewStatus === 'rejected') flags.push('rejected');
  }
  if (resource) {
    const resourceWarningFlags = (resource as Resource & { warningFlags?: string[] }).warningFlags;
    if (Array.isArray(resourceWarningFlags)) flags.push(...resourceWarningFlags);
    if (resource.verificationStatus === 'unverified') flags.push('unverified');
    if (resource.verificationStatus === 'rejected') flags.push('verification_rejected');
    if (isRightsProtectedContent(resource)) flags.push('rights_protected');
    else if (isRightsRestrictedOrProtected(resource)) flags.push('rights_restricted');
    if (isStandardLikeResource(resource)) {
      const missing = standardContextMissingFields(resource, link);
      if (missing.length > 0 && !hasStructuredMissingContextJustification(resource, link)) {
        flags.push('standards_context_incomplete');
      }
    }
  }
  return [...new Set(flags)];
}

function rightsStatusLabel(resource?: Resource): string | undefined {
  if (!resource) return undefined;
  if (isRightsProtectedContent(resource)) return 'protected_content';
  if (isRightsRestrictedOrProtected(resource)) return 'restricted';
  if (resource.accessType === 'open_access') return 'open_access';
  if (resource.accessType === 'public_web') return 'public_web';
  if (resource.accessType === 'local_only') return 'local_only';
  return resource.accessType;
}

function nextReviewAction(item: SourceCustodyItem): string | undefined {
  if (item.custodyStatus === 'candidate') return 'Review candidate for acceptance or rejection';
  if (item.custodyStatus === 'indexed_only') return 'Review local file for admission to Resource Registry';
  if (item.custodyStatus === 'needs_review') return 'Review link for accept, reject, or context completion';
  if (item.custodyStatus === 'standards_incomplete') return 'Supply edition, jurisdiction, and citation context or structured justification';
  if (item.custodyStatus === 'rights_limited') return 'Review rights clearance before learner exposure';
  if (item.custodyStatus === 'blocked') return 'Item is rejected; no further action unless reopened';
  if (item.custodyStatus === 'reviewer_only') return 'Review for promotion to learner-visible';
  return undefined;
}

function classifyLinkCustody(link: NodeResourceLink, resource?: Resource): { custodyStatus: CustodyStatus; displayPolicy: DisplayPolicy; learnerEligible: boolean; reviewerOnlyReason?: string; hiddenReason?: string } {
  const learnerEligible = resource ? isLearnerSidebarEligible(link, resource) : false;

  if (link.reviewStatus === 'rejected') {
    return { custodyStatus: 'blocked', displayPolicy: 'blocked', learnerEligible: false, hiddenReason: 'Link status is rejected.' };
  }

  if (resource && isRightsProtectedContent(resource)) {
    return { custodyStatus: 'rights_limited', displayPolicy: 'hidden', learnerEligible: false, reviewerOnlyReason: 'Resource is rights-protected content.', hiddenReason: 'Rights-protected content is blocked from learner view.' };
  }

  if (resource && isStandardLikeResource(resource)) {
    const missing = standardContextMissingFields(resource, link);
    if (missing.length > 0 && !hasStructuredMissingContextJustification(resource, link)) {
      if (link.reviewStatus === 'accepted' || link.reviewStatus === 'human_reviewed') {
        // This shouldn't happen because validation blocks it, but handle gracefully
        return { custodyStatus: 'standards_incomplete', displayPolicy: 'show_warning', learnerEligible: false, reviewerOnlyReason: `Standard context incomplete: missing ${missing.join(', ')}.`, hiddenReason: 'Incomplete standard context without structured justification.' };
      }
      return { custodyStatus: 'standards_incomplete', displayPolicy: 'dev_only', learnerEligible: false, reviewerOnlyReason: `Standard context incomplete: missing ${missing.join(', ')}.`, hiddenReason: 'Incomplete standard context without structured justification.' };
    }
  }

  if (learnerEligible) {
    return { custodyStatus: 'learner_visible', displayPolicy: 'show_to_user', learnerEligible: true };
  }

  if (link.reviewStatus === 'needs_review') {
    return { custodyStatus: 'needs_review', displayPolicy: 'dev_only', learnerEligible: false, reviewerOnlyReason: 'Link status is needs_review.', hiddenReason: 'Pending review before trusted use.' };
  }

  if (link.reviewStatus === 'candidate') {
    return { custodyStatus: 'candidate', displayPolicy: 'dev_only', learnerEligible: false, reviewerOnlyReason: 'Link status is candidate.', hiddenReason: 'Candidate link not yet reviewed.' };
  }

  if (resource && resource.verificationStatus === 'unverified') {
    return { custodyStatus: 'reviewer_only', displayPolicy: 'dev_only', learnerEligible: false, reviewerOnlyReason: 'Resource verification status is unverified.', hiddenReason: 'Resource not yet verified.' };
  }

  if (resource && isRightsRestrictedOrProtected(resource)) {
    return { custodyStatus: 'rights_limited', displayPolicy: 'hidden', learnerEligible: false, reviewerOnlyReason: 'Resource has restricted or protected rights.', hiddenReason: 'Rights-restricted content.' };
  }

  return { custodyStatus: 'reviewer_only', displayPolicy: 'dev_only', learnerEligible: false, reviewerOnlyReason: 'Not eligible for learner sidebar.', hiddenReason: 'Hidden from learner view.' };
}

function enrichLinkItem(base: ReturnType<typeof linkItem>): SourceCustodyItem {
  const classification = classifyLinkCustody(base.link as NodeResourceLink, base.resource as Resource);
  const warningFlags = buildWarningFlags(base.resource as Resource, base.link as NodeResourceLink, base.warnings);
  return {
    itemType: 'resource_link',
    id: base.id,
    title: base.title,
    resourceId: base.resourceId,
    nodeId: base.nodeId,
    resourceType: base.resourceType,
    sourceAuthority: base.resource?.sourceAuthority,
    reviewStatus: base.reviewStatus,
    verificationStatus: base.verificationStatus,
    custodyStatus: classification.custodyStatus,
    displayPolicy: classification.displayPolicy,
    learnerEligible: classification.learnerEligible,
    reviewerOnlyReason: classification.reviewerOnlyReason,
    hiddenReason: classification.hiddenReason,
    warningFlags,
    rightsStatus: rightsStatusLabel(base.resource as Resource),
    standardsContextStatus: base.standardContextStatus,
    missingStandardContextFields: base.missingStandardContextFields,
    promotionBlocked: base.promotionBlocked,
    nextReviewAction: undefined, // set after full item built
    authorityTier: base.authorityTier,
    authorityScore: base.authorityScore,
    relationship: base.relationship,
    rationale: base.rationale,
    reviewNotes: base.reviewNotes,
    sourceFamilyIds: base.sourceFamilyIds,
    organization: base.organization,
    currentEdition: base.currentEdition,
    currentVersion: base.currentVersion,
    currentPublicationYear: base.currentPublicationYear,
    currentJurisdiction: base.currentJurisdiction,
    currentGeographicScope: base.currentGeographicScope,
    sourceOfContext: base.sourceOfContext,
    warnings: base.warnings,
    resource: base.resource as Resource,
    link: base.link as NodeResourceLink,
  };
}

function enrichExternalCandidateItem(candidate: ExternalMetadataCandidateRecord): SourceCustodyItem {
  const isBlocked = candidate.fakePlaceholderFlags.length > 0 || candidate.status === 'blocked';
  const status = candidate.status;
  let nextReviewAction = 'Review candidate metadata';
  if (isBlocked) nextReviewAction = 'Reject placeholder metadata or supply valid values';
  else if (status === 'metadata_correction_needed') nextReviewAction = 'Apply metadata correction';
  else if (status === 'rights_review_needed') nextReviewAction = 'Review rights clearance';
  else if (status === 'standards_context_needed') nextReviewAction = 'Supply edition, jurisdiction, and citation context';
  else if (status === 'standards_context_in_review') nextReviewAction = 'Complete standards context review';
  else if (status === 'standards_context_complete') nextReviewAction = 'Review promotion readiness gates; no auto-promotion';
  else if (status === 'standards_context_rejected') nextReviewAction = 'Candidate standards context rejected; reopen only with real context';
  else if (status === 'source_custody_review_needed') nextReviewAction = 'Review source custody chain';
  else if (status === 'source_custody_in_review') nextReviewAction = 'Complete source custody and rights review';
  else if (status === 'source_custody_verified') nextReviewAction = 'Review promotion readiness gates; no auto-promotion';
  else if (status === 'source_custody_rejected') nextReviewAction = 'Candidate source custody rejected; reopen only with new evidence';
  else if (status === 'duplicate_candidate') nextReviewAction = 'Review duplicate status';
  else if (status === 'rejected') nextReviewAction = 'Candidate rejected; no further action unless reopened';
  else if (status === 'deferred') nextReviewAction = 'Candidate deferred; review postponed';
  else if (status === 'ready_for_promotion_review') nextReviewAction = 'Candidate ready for promotion review; promotion apply not yet implemented';
  else if (status === 'promotion_blocked') nextReviewAction = 'Resolve promotion blockers before review';

  return {
    itemType: 'external_candidate',
    id: candidate.candidateId,
    title: candidate.title,
    resourceType: candidate.resourceType,
    sourceAuthority: undefined,
    reviewStatus: candidate.status,
    verificationStatus: candidate.verificationStatus,
    custodyStatus: isBlocked ? 'blocked' : 'candidate',
    displayPolicy: isBlocked ? 'blocked' : 'dev_only',
    learnerEligible: false,
    reviewerOnlyReason: isBlocked
      ? 'External candidate contains placeholder or invalid metadata.'
      : `External candidate is ${candidate.status.replace(/_/g, ' ')} and not reviewed.`,
    hiddenReason: 'External candidates are not learner-visible until reviewed and accepted.',
    warningFlags: candidate.warningFlags,
    rightsStatus: candidate.proposedRightsStatus,
    standardsContextStatus: undefined,
    missingStandardContextFields: undefined,
    promotionBlocked: status !== 'ready_for_promotion_review',
    nextReviewAction,
    rawUrl: candidate.proposedUrl,
    rawIdentifier: candidate.proposedDoi || candidate.proposedIsbn,
    sourceFamilyIds: candidate.proposedSourceFamilyId ? [candidate.proposedSourceFamilyId] : undefined,
    warnings: candidate.warningFlags,
  };
}

function enrichCandidateItem(base: ReturnType<typeof candidateItem>): SourceCustodyItem {
  return {
    itemType: 'candidate',
    id: base.id,
    title: base.title,
    nodeId: base.nodeId,
    resourceType: undefined,
    sourceAuthority: undefined,
    reviewStatus: base.reviewStatus,
    verificationStatus: undefined,
    custodyStatus: 'candidate',
    displayPolicy: 'dev_only',
    learnerEligible: false,
    reviewerOnlyReason: 'Candidate resource has not been reviewed or accepted.',
    hiddenReason: 'Candidate resources are hidden from learners.',
    warningFlags: ['candidate'],
    rightsStatus: undefined,
    standardsContextStatus: undefined,
    missingStandardContextFields: undefined,
    promotionBlocked: undefined,
    nextReviewAction: 'Review candidate for acceptance or rejection',
    rawUrl: base.rawUrl,
    rawIdentifier: base.rawIdentifier,
    preliminaryScore: base.preliminaryScore,
    rankingScore: base.rankingScore,
    dedupeKey: base.dedupeKey,
    duplicateResourceId: base.duplicateResourceId,
    sourceFamilyIds: base.sourceFamilyIds,
    authorityTier: base.authorityTier,
    warnings: base.warnings,
    candidate: base.candidate as ResourceCandidate,
  };
}

function enrichLocalFileItem(base: ReturnType<typeof localFileItem>): SourceCustodyItem {
  const custodyStatus: CustodyStatus = base.admitted ? 'reviewer_only' : 'indexed_only';
  const displayPolicy: DisplayPolicy = base.admitted ? 'dev_only' : 'dev_only';
  return {
    itemType: 'local_file',
    id: base.id,
    title: base.title,
    resourceId: base.admittedResourceId,
    reviewStatus: base.reviewStatus,
    verificationStatus: undefined,
    custodyStatus,
    displayPolicy,
    learnerEligible: false,
    reviewerOnlyReason: base.admitted
      ? 'Local file admitted but not linked to learner-eligible resource.'
      : 'Local file is indexed but not admitted to Resource Registry.',
    hiddenReason: base.admitted
      ? 'Admitted local file requires explicit linkage review.'
      : 'Indexed-only local files are not learner-visible.',
    warningFlags: base.admitted ? ['local_file_admitted'] : ['local_file_indexed_only'],
    rightsStatus: undefined,
    standardsContextStatus: undefined,
    missingStandardContextFields: undefined,
    promotionBlocked: undefined,
    nextReviewAction: base.admitted ? 'Review linkage to nodes' : 'Review local file for admission',
    localPath: base.localPath,
    localFileHash: base.localFileHash,
    localFileType: base.localFileType,
    localFileSizeBytes: base.localFileSizeBytes,
    linkedNodeCount: base.linkedNodeCount,
    admitted: base.admitted,
    admittedResourceId: base.admittedResourceId,
    sourceFamilyIds: base.sourceFamilyIds,
    authorityTier: base.authorityTier,
    warnings: base.warnings,
    resource: base.resource as Resource,
  };
}

export function buildSourceCustodyQueue(repoRoot: string): SourceCustodyQueue {
  const data = readResourceLayerData(repoRoot);
  const localIndex = readLocalFileIndex(repoRoot);
  const resourceById = new Map(data.resources.map((resource) => [resource.id, resource]));

  const allItems: SourceCustodyItem[] = [];

  // Links
  for (const link of data.nodeResourceLinks) {
    const resource = resourceById.get(link.resourceId);
    const base = linkItem(link, resource);
    const enriched = enrichLinkItem(base);
    enriched.nextReviewAction = nextReviewAction(enriched);
    allItems.push(enriched);
  }

  // Candidates
  for (const candidate of data.resourceCandidates) {
    const base = candidateItem(candidate, data);
    const enriched = enrichCandidateItem(base);
    enriched.nextReviewAction = nextReviewAction(enriched);
    allItems.push(enriched);
  }

  // Local files
  for (const indexed of localIndex.resources) {
    const base = localFileItem(indexed, data);
    const enriched = enrichLocalFileItem(base);
    enriched.nextReviewAction = nextReviewAction(enriched);
    allItems.push(enriched);
  }

  // External metadata candidates
  const externalRegistry = loadExternalCandidateRegistry(repoRoot);
  for (const extCandidate of externalRegistry.candidates) {
    const enriched = enrichExternalCandidateItem(extCandidate);
    allItems.push(enriched);
  }

  const groups = {
    learnerVisible: allItems.filter((item) => item.custodyStatus === 'learner_visible'),
    reviewerOnly: allItems.filter((item) => item.custodyStatus === 'reviewer_only'),
    needsReview: allItems.filter((item) => item.custodyStatus === 'needs_review'),
    candidates: allItems.filter((item) => item.itemType === 'candidate'),
    externalCandidates: allItems.filter((item) => item.itemType === 'external_candidate'),
    localFilesIndexedOnly: allItems.filter((item) => item.custodyStatus === 'indexed_only'),
    standardsContextIncomplete: allItems.filter((item) => item.custodyStatus === 'standards_incomplete'),
    rightsLimited: allItems.filter((item) => item.custodyStatus === 'rights_limited'),
    rejected: allItems.filter((item) => item.custodyStatus === 'blocked'),
    blocked: allItems.filter((item) => item.custodyStatus === 'blocked'),
  };

  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: new Date().toISOString(),
    groups,
    metrics: {
      total: allItems.length,
      learnerVisible: groups.learnerVisible.length,
      reviewerOnly: groups.reviewerOnly.length,
      needsReview: groups.needsReview.length,
      candidates: groups.candidates.length,
      externalCandidates: groups.externalCandidates.length,
      localFilesIndexedOnly: groups.localFilesIndexedOnly.length,
      standardsContextIncomplete: groups.standardsContextIncomplete.length,
      rightsLimited: groups.rightsLimited.length,
      rejected: groups.rejected.length,
      blocked: groups.blocked.length,
    },
  };
}
