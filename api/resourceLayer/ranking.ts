import { basename } from 'node:path';
import type { NodeResourceLink, NodeResourceSummary, Resource, VerificationStatus } from './types';
import {
  isLearnerSidebarEligible,
  isRightsProtectedContent,
  isRightsRestrictedOrProtected,
  isStandardLikeResource,
  standardContextMissingFields,
} from './validation';

export const RESOURCE_RANKING_WEIGHTS = {
  relevance: 0.45,
  authority: 0.25,
  confidence: 0.15,
  verification: 0.10,
  access: 0.05,
} as const;

export const RESOURCE_RANKING_PENALTIES = {
  unverified: 0.20,
  generalWeb: 0.12,
  missingTitle: 0.25,
  needsReview: 0.20,
  candidate: 0.25,
  rejected: 1.00,
  rightsRestricted: 0.30,
  incompleteStandardContext: 0.35,
} as const;

export function verificationScore(status: VerificationStatus) {
  switch (status) {
    case 'human_reviewed': return 1;
    case 'content_verified': return 0.9;
    case 'local_file_verified': return 0.85;
    case 'identifier_verified': return 0.8;
    case 'link_verified': return 0.7;
    case 'metadata_verified': return 0.6;
    case 'unverified': return 0.2;
    case 'rejected': return 0;
  }
}

function accessScore(resource: Resource) {
  if (resource.localFileHash) return 1;
  if (resource.doi || resource.isbn13 || resource.isbn10) return 0.9;
  if (resource.accessType === 'open_access') return 0.85;
  if (resource.accessType === 'public_web') return 0.75;
  if (resource.accessType === 'preview_only') return 0.55;
  if (resource.accessType === 'paywalled') return 0.45;
  if (resource.accessType === 'restricted') return 0.3;
  return 0.2;
}

function penalty(resource: Resource, link: NodeResourceLink) {
  let value = 0;
  if (resource.verificationStatus === 'unverified') value += RESOURCE_RANKING_PENALTIES.unverified;
  if (resource.sourceAuthority === 'general_web') value += RESOURCE_RANKING_PENALTIES.generalWeb;
  if (!resource.title.trim()) value += RESOURCE_RANKING_PENALTIES.missingTitle;
  if (link.reviewStatus === 'needs_review') value += RESOURCE_RANKING_PENALTIES.needsReview;
  if (link.reviewStatus === 'candidate') value += RESOURCE_RANKING_PENALTIES.candidate;
  if (link.reviewStatus === 'rejected' || resource.verificationStatus === 'rejected') value += RESOURCE_RANKING_PENALTIES.rejected;
  if (isRightsRestrictedOrProtected(resource)) value += RESOURCE_RANKING_PENALTIES.rightsRestricted;
  if (isStandardLikeResource(resource)) {
    const missing = standardContextMissingFields(resource, link);
    if (missing.length > 0) value += RESOURCE_RANKING_PENALTIES.incompleteStandardContext;
  }
  return value;
}

export function displayScore(resource: Resource, link: NodeResourceLink) {
  const raw = link.relevanceScore * RESOURCE_RANKING_WEIGHTS.relevance
    + link.authorityScore * RESOURCE_RANKING_WEIGHTS.authority
    + link.confidenceScore * RESOURCE_RANKING_WEIGHTS.confidence
    + verificationScore(resource.verificationStatus) * RESOURCE_RANKING_WEIGHTS.verification
    + accessScore(resource) * RESOURCE_RANKING_WEIGHTS.access
    - penalty(resource, link);
  return Math.max(0, Math.min(1, Number(raw.toFixed(4))));
}

export interface RankOptions {
  includeCandidates?: boolean;
  includeReviewer?: boolean;
  limit?: number;
}

function buildWarning(resource: Resource, link: NodeResourceLink): string | undefined {
  const extended = resource as Resource & {
    sourceTruthCaveat?: string;
    warningFlags?: string[];
    sourceRights?: Resource['sourceRights'];
  };
  if (link.reviewStatus === 'needs_review') return 'Needs review before trusted use.';
  if (link.reviewStatus === 'candidate') return 'Candidate resource; not yet reviewed.';
  if (link.reviewStatus === 'rejected') return 'Rejected resource.';
  if (resource.verificationStatus === 'rejected') return 'Resource verification rejected.';
  if (resource.verificationStatus === 'unverified') return 'Resource not yet verified.';
  if (isRightsProtectedContent(resource)) return 'Rights-protected content; verify clearance before use.';
  if (isRightsRestrictedOrProtected(resource)) return 'Restricted or protected content; access may be limited.';
  if (isStandardLikeResource(resource)) {
    const missing = standardContextMissingFields(resource, link);
    if (missing.length > 0) {
      return `Standard context incomplete: missing ${missing.join(', ')}.`;
    }
  }
  if (resource.jurisdiction) return 'Jurisdiction or scope context applies.';
  if (
    resource.verificationStatus === 'link_verified'
    && (
      extended.sourceRights?.rightsClass === 'public_web_metadata_only'
      || extended.warningFlags?.includes('metadata_only_no_source_truth_claim')
    )
  ) {
    return extended.sourceTruthCaveat || 'Official public locator metadata checked only; not source truth.';
  }
  return undefined;
}

export function summarizeNodeResource(resource: Resource, link: NodeResourceLink): NodeResourceSummary {
  const extended = resource as Resource & {
    sourceTruthCaveat?: string;
    rightsCaveat?: string | null;
    displayPolicy?: string;
    warningFlags?: string[];
  };
  const localFileName = resource.localPath ? basename(resource.localPath.replace(/\\/g, '/')) : undefined;
  return {
    linkId: link.id,
    resourceId: resource.id,
    nodeId: link.nodeId,
    title: resource.title,
    subtitle: resource.subtitle,
    authors: resource.authors,
    organization: resource.organization,
    publisher: resource.publisher,
    year: resource.year,
    resourceType: resource.resourceType,
    sourceAuthority: resource.sourceAuthority,
    sourceFamilyIds: resource.sourceFamilyIds,
    authorityTier: resource.authorityTier,
    accessType: resource.accessType,
    verificationStatus: resource.verificationStatus,
    reviewStatus: link.reviewStatus,
    relationship: link.relationship,
    relevanceScore: link.relevanceScore,
    authorityScore: link.authorityScore,
    confidenceScore: link.confidenceScore,
    displayScore: displayScore(resource, link),
    rationale: link.rationale,
    pageRefs: link.pageRefs,
    chapterRefs: link.chapterRefs,
    sectionRefs: link.sectionRefs,
    jurisdiction: resource.jurisdiction,
    geographicScope: resource.geographicScope,
    url: resource.url,
    canonicalUrl: resource.canonicalUrl,
    doi: resource.doi,
    isbn13: resource.isbn13,
    localFileName,
    localFileType: resource.localFileType,
    licenseNotes: resource.licenseNotes,
    lastCheckedAt: resource.lastCheckedAt,
    warning: buildWarning(resource, link),
    sourceTruthCaveat: extended.sourceTruthCaveat,
    rightsCaveat: extended.rightsCaveat,
    displayPolicy: extended.displayPolicy,
    warningFlags: extended.warningFlags,
  };
}

export function rankNodeResources(resources: Resource[], links: NodeResourceLink[], options: RankOptions = {}) {
  const resourceById = new Map(resources.map((resource) => [resource.id, resource]));
  const reviewerView = options.includeReviewer || options.includeCandidates;
  const summaries = links
    .filter((link) => reviewerView || link.reviewStatus === 'accepted' || link.reviewStatus === 'human_reviewed')
    .map((link) => {
      const resource = resourceById.get(link.resourceId);
      if (!resource) return null;
      if (!reviewerView && (resource.verificationStatus === 'rejected' || resource.verificationStatus === 'unverified')) return null;
      if (!reviewerView && !isLearnerSidebarEligible(link, resource)) return null;
      return summarizeNodeResource(resource, link);
    })
    .filter((summary): summary is NodeResourceSummary => Boolean(summary))
    .sort((a, b) => b.displayScore - a.displayScore || b.relevanceScore - a.relevanceScore || a.title.localeCompare(b.title) || a.resourceId.localeCompare(b.resourceId));
  const hardCap = 8;
  return summaries.slice(0, Math.min(options.limit ?? hardCap, hardCap));
}
