import { basename } from 'node:path';
import type { NodeResourceLink, NodeResourceSummary, Resource, VerificationStatus } from './types';

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
  limit?: number;
}

export function summarizeNodeResource(resource: Resource, link: NodeResourceLink): NodeResourceSummary {
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
    warning: link.reviewStatus === 'needs_review'
      ? 'Needs review before trusted use.'
      : resource.jurisdiction
        ? 'Jurisdiction or scope context applies.'
        : undefined,
  };
}

export function rankNodeResources(resources: Resource[], links: NodeResourceLink[], options: RankOptions = {}) {
  const resourceById = new Map(resources.map((resource) => [resource.id, resource]));
  const summaries = links
    .filter((link) => options.includeCandidates || link.reviewStatus === 'accepted' || link.reviewStatus === 'human_reviewed')
    .map((link) => {
      const resource = resourceById.get(link.resourceId);
      if (!resource) return null;
      if (!options.includeCandidates && (resource.verificationStatus === 'rejected' || resource.verificationStatus === 'unverified')) return null;
      return summarizeNodeResource(resource, link);
    })
    .filter((summary): summary is NodeResourceSummary => Boolean(summary))
    .sort((a, b) => b.displayScore - a.displayScore || b.relevanceScore - a.relevanceScore || a.title.localeCompare(b.title) || a.resourceId.localeCompare(b.resourceId));
  return summaries.slice(0, options.limit ?? 5);
}
