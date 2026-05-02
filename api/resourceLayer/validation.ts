import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import type { NodeResourceLink, Resource, ResourceLayerData } from './types';
import { ACCESS_TYPES, NODE_RESOURCE_RELATIONSHIPS, RESOURCE_TYPES, REVIEW_STATUSES, SOURCE_AUTHORITIES, VERIFICATION_STATUSES } from './types';
import { canonicalizeUrl, normalizeDoi, normalizeIsbn } from './normalization';
import { detectResourceDuplicates } from './deduplication';
import { approvedSourceFamilyIds } from './sourceFamilies';

export interface ValidationResult {
  ok: boolean;
  errors: string[];
  warnings: string[];
  blockers: string[];
  duplicateCount: number;
  brokenLinkCount: number;
}

export interface ValidationOptions {
  repoRoot: string;
  nodeIds?: Set<string>;
  nodeTypesById?: Map<string, string>;
  localIndexedHashes?: Set<string>;
  fullLocalFileCheck?: boolean;
  allowUnverifiedAccepted?: boolean;
}

const resourceTypes = new Set<string>(RESOURCE_TYPES);
const authorities = new Set<string>(SOURCE_AUTHORITIES);
const accessTypes = new Set<string>(ACCESS_TYPES);
const verificationStatuses = new Set<string>(VERIFICATION_STATUSES);
const relationships = new Set<string>(NODE_RESOURCE_RELATIONSHIPS);
const reviewStatuses = new Set<string>(REVIEW_STATUSES);

function isAcceptedLink(link: NodeResourceLink) {
  return link.reviewStatus === 'accepted' || link.reviewStatus === 'human_reviewed';
}

function isLocalResource(resource: Resource) {
  return Boolean(resource.localPath || resource.localFileHash || resource.resourceType.startsWith('local_') || resource.accessType === 'local_only');
}

function isStandardLikeResource(resource: Resource) {
  return resource.resourceType === 'code' || resource.resourceType === 'standard';
}

function hasCitationContext(link: NodeResourceLink) {
  return Boolean(link.sectionRefs?.length || link.chapterRefs?.length || link.pageRefs?.length || link.fragmentRefs?.length);
}

function hasExplicitStandardContextJustification(link: NodeResourceLink) {
  return /explicit standard-context reviewer justification/i.test(link.reviewNotes || '');
}

function sourceFamilyIncludes(resource: Resource, familyId: string) {
  return Boolean(resource.sourceFamilyIds?.includes(familyId));
}

function hasExternalIdentifier(resource: Resource) {
  return Boolean(resource.url || resource.canonicalUrl || resource.doi || resource.isbn13 || resource.isbn10 || resource.internetArchiveIdentifier || resource.openAlexId || resource.semanticScholarId);
}

function validateResource(resource: Resource, errors: string[], warnings: string[], options: ValidationOptions) {
  if (!resource.id) errors.push('resource missing id');
  if (!resource.title?.trim()) errors.push(`${resource.id}: missing title`);
  if (!resourceTypes.has(resource.resourceType)) errors.push(`${resource.id}: unsupported resourceType ${resource.resourceType}`);
  if (!authorities.has(resource.sourceAuthority)) errors.push(`${resource.id}: unsupported sourceAuthority ${resource.sourceAuthority}`);
  if (!accessTypes.has(resource.accessType)) errors.push(`${resource.id}: unsupported accessType ${resource.accessType}`);
  if (!verificationStatuses.has(resource.verificationStatus)) errors.push(`${resource.id}: unsupported verificationStatus ${resource.verificationStatus}`);
  if ((resource.url || resource.canonicalUrl) && !canonicalizeUrl(resource.canonicalUrl || resource.url)) errors.push(`${resource.id}: invalid URL`);
  if (resource.doi && !normalizeDoi(resource.doi)) errors.push(`${resource.id}: invalid DOI`);
  if (resource.isbn10 && !normalizeIsbn(resource.isbn10)) errors.push(`${resource.id}: invalid ISBN10`);
  if (resource.isbn13 && !normalizeIsbn(resource.isbn13)) errors.push(`${resource.id}: invalid ISBN13`);
  if ((resource.authorityTier ?? 5) <= 2 && (!resource.sourceFamilyIds || resource.sourceFamilyIds.length === 0)) warnings.push(`${resource.id}: high-authority resource missing sourceFamilyIds`);
  if (!resource.sourceRights?.declaredUseBoundary) warnings.push(`${resource.id}: missing sourceRights.declaredUseBoundary`);
  if (!resource.admissionProvenance?.admittedBy || !resource.admissionProvenance?.admittedAt) warnings.push(`${resource.id}: missing admission provenance`);
  if (isLocalResource(resource)) {
    if (!resource.localPath) errors.push(`${resource.id}: local resource missing localPath`);
    if (!resource.localFileHash) errors.push(`${resource.id}: local resource missing localFileHash`);
    if (resource.localFileHash && options.localIndexedHashes && !options.localIndexedHashes.has(resource.localFileHash)) {
      errors.push(`${resource.id}: local resource hash is not present in local-file-index.json`);
    }
    if (options.fullLocalFileCheck && resource.localPath && !existsSync(resolve(options.repoRoot, resource.localPath))) errors.push(`${resource.id}: localPath does not exist`);
  } else if (!hasExternalIdentifier(resource)) {
    errors.push(`${resource.id}: online resource missing URL, DOI, ISBN, or stable identifier`);
  }
  if (isStandardLikeResource(resource) && !resource.jurisdiction && !resource.geographicScope) warnings.push(`${resource.id}: code/standard resource missing jurisdiction or geographicScope`);
  if (isStandardLikeResource(resource) && !resource.edition) warnings.push(`${resource.id}: code/standard resource missing edition/version context`);
}

function validateLink(link: NodeResourceLink, resourceById: Map<string, Resource>, errors: string[], warnings: string[], blockers: string[], options: ValidationOptions) {
  if (!link.id) errors.push('nodeResourceLink missing id');
  if (!link.nodeId) errors.push(`${link.id}: missing nodeId`);
  if (!link.resourceId) errors.push(`${link.id}: missing resourceId`);
  if (options.nodeIds && !options.nodeIds.has(link.nodeId)) errors.push(`${link.id}: nodeId does not exist: ${link.nodeId}`);
  if (!resourceById.has(link.resourceId)) errors.push(`${link.id}: resourceId does not exist: ${link.resourceId}`);
  if (!relationships.has(link.relationship)) errors.push(`${link.id}: unsupported relationship ${link.relationship}`);
  if (!reviewStatuses.has(link.reviewStatus)) errors.push(`${link.id}: unsupported reviewStatus ${link.reviewStatus}`);
  for (const [name, value] of [['relevanceScore', link.relevanceScore], ['authorityScore', link.authorityScore], ['confidenceScore', link.confidenceScore]] as const) {
    if (typeof value !== 'number' || value < 0 || value > 1) errors.push(`${link.id}: ${name} outside 0..1`);
  }
  if (isAcceptedLink(link) && !link.rationale?.trim()) errors.push(`${link.id}: accepted link missing rationale`);
  const resource = resourceById.get(link.resourceId);
  if (!resource) return;
  if (isAcceptedLink(link) && resource.verificationStatus === 'rejected') errors.push(`${link.id}: accepted link points to rejected resource`);
  if (isAcceptedLink(link) && resource.verificationStatus === 'unverified' && !options.allowUnverifiedAccepted) errors.push(`${link.id}: accepted link points to unverified resource`);
  if (isAcceptedLink(link) && !isLocalResource(resource) && !resource.lastCheckedAt) errors.push(`${link.id}: accepted external resource missing lastCheckedAt`);
  if (isAcceptedLink(link) && !resource.admissionProvenance?.admittedBy) warnings.push(`${link.id}: accepted link resource missing admission provenance`);
  if (isAcceptedLink(link) && (!resource.sourceRights?.declaredUseBoundary || !resource.admissionProvenance?.admittedBy)) {
    blockers.push(`${link.id}: accepted link requires source-rights and admission provenance context`);
  }
  if (isAcceptedLink(link) && isStandardLikeResource(resource) && !resource.edition && !hasCitationContext(link) && !hasExplicitStandardContextJustification(link)) {
    blockers.push(`${link.id}: accepted standard/code-like link requires edition/version plus page/chapter/section context or explicit reviewer justification`);
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'asce') && !hasCitationContext(link) && !hasExplicitStandardContextJustification(link)) {
    blockers.push(`${link.id}: ASCE link cannot be promoted without edition/section/adoption context`);
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'aci') && !hasCitationContext(link) && !hasExplicitStandardContextJustification(link)) {
    blockers.push(`${link.id}: ACI link cannot be promoted without edition/section-specific context`);
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'fhwa') && !hasExplicitStandardContextJustification(link) && !/transportation|geotechnical|scope/i.test(link.reviewNotes || resource.jurisdiction || resource.abstractOrSummary || '')) {
    blockers.push(`${link.id}: FHWA link cannot be promoted without explicit U.S. transportation/geotechnical scope review`);
  }
  if (link.reviewStatus === 'rejected' && !link.reviewNotes?.trim()) warnings.push(`${link.id}: rejected link missing preserved rejection rationale`);
  if (sourceFamilyIncludes(resource, 'wbdg_nibs')) {
    if ((resource.authorityTier ?? 5) <= 1) blockers.push(`${link.id}: WBDG/NIBS must remain contextual guidance unless explicitly reviewed otherwise`);
    if (isAcceptedLink(link) && ['governs', 'is_primary_reference_for'].includes(link.relationship)) {
      blockers.push(`${link.id}: WBDG/NIBS accepted link must not be primary/governing without explicit review`);
    }
  }
  const nodeType = options.nodeTypesById?.get(link.nodeId)?.toLowerCase();
  if (isAcceptedLink(link) && nodeType === 'rule') {
    if (link.authorityScore < 0.75) errors.push(`${link.id}: Rule link authorityScore below 0.75`);
    if (!['governs', 'is_primary_reference_for'].includes(link.relationship)) warnings.push(`${link.id}: Rule link is not a primary/governing relationship`);
    if (!resource.jurisdiction && !resource.geographicScope) errors.push(`${link.id}: Rule link resource missing jurisdiction/geographicScope`);
  }
}

export function validateResourceLayerData(data: ResourceLayerData, options: ValidationOptions): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  const blockers: string[] = [];
  const familyIds = approvedSourceFamilyIds(data.sourceFamilies);
  const resourceIds = new Set<string>();
  for (const resource of data.resources) {
    if (resourceIds.has(resource.id)) errors.push(`${resource.id}: duplicate resource id`);
    resourceIds.add(resource.id);
    validateResource(resource, errors, warnings, options);
    for (const familyId of resource.sourceFamilyIds || []) if (!familyIds.has(familyId)) errors.push(`${resource.id}: sourceFamilyId not registered: ${familyId}`);
  }
  const duplicateGroups = detectResourceDuplicates(data.resources);
  for (const group of duplicateGroups) errors.push(`duplicate ${group.kind}: ${group.key} -> ${group.resourceIds.join(', ')}`);
  const resourceById = new Map(data.resources.map((resource) => [resource.id, resource]));
  for (const link of data.nodeResourceLinks) validateLink(link, resourceById, errors, warnings, blockers, options);
  for (const candidate of data.resourceCandidates) {
    if (candidate.reviewStatus === 'rejected' && !candidate.rejectionReason?.trim()) warnings.push(`${candidate.id}: rejected candidate missing rejection rationale`);
  }
  const brokenLinkCount = data.resourceChecks.filter((check) => check.checkType === 'url_health' && check.status === 'fail').length;
  return { ok: errors.length === 0 && blockers.length === 0, errors, warnings, blockers, duplicateCount: duplicateGroups.length, brokenLinkCount };
}
