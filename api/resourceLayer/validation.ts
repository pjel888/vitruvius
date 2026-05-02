import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import type { NodeResourceLink, Resource, ResourceLayerData, StandardContextStatus } from './types';
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
  standardsTotal: number;
  standardsMissingEdition: number;
  standardsMissingJurisdiction: number;
  standardsMissingScope: number;
  standardsContextComplete: number;
  standardsContextPartial: number;
  standardsContextNeedsReview: number;
  standardsAcceptedMissingContext: number;
  standardsPromotionBlocked: number;
  standardsContextReviewable: number;
  standardsContextWarnings: string[];
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

const placeholderContextValues = new Set([
  'tbd',
  'to be determined',
  'unknown',
  'generic',
  'latest',
  'current',
  'placeholder',
  'sample',
  'example',
  'varies',
]);

export function isPlaceholderStandardContextValue(value: unknown) {
  if (value === undefined || value === null) return false;
  if (typeof value === 'number') return false;
  const normalized = String(value).trim().toLowerCase();
  return normalized.length === 0 || placeholderContextValues.has(normalized) || /^n\/?a$/i.test(normalized);
}

function hasUsableValue(value: unknown) {
  if (value === undefined || value === null) return false;
  if (typeof value === 'number') return Number.isFinite(value);
  return String(value).trim().length > 0 && !isPlaceholderStandardContextValue(value);
}

function standardReviewContext(resource: Resource, link?: NodeResourceLink) {
  return link?.standardContext?.reviewContext || resource.reviewContext;
}

function hasStructuredMissingContextJustification(resource: Resource, link?: NodeResourceLink) {
  const reviewContext = standardReviewContext(resource, link);
  if (!reviewContext) return false;
  if (!['justified_missing', 'not_required'].includes(reviewContext.contextStatus)) return false;
  return Boolean(
    hasUsableValue(reviewContext.reviewedBy)
    && hasUsableValue(reviewContext.rationale)
    && hasUsableValue(reviewContext.sourceOfContext)
  );
}

function standardContextStatus(resource: Resource, link?: NodeResourceLink): StandardContextStatus {
  const reviewContext = standardReviewContext(resource, link);
  if (reviewContext?.contextStatus) return reviewContext.contextStatus;
  const missing = standardContextMissingFields(resource, link);
  if (missing.length === 0) return 'complete';
  if (missing.length < 3) return 'partial';
  return 'needs_human_review';
}

export function standardContextMissingFields(resource: Resource, link?: NodeResourceLink) {
  if (!isStandardLikeResource(resource)) return [] as string[];
  const missing: string[] = [];
  const editionContext = link?.standardContext?.editionContext || resource.editionContext;
  const identifier = link?.standardContext?.standardIdentifier || resource.standardIdentifier;
  const jurisdictionContext = link?.standardContext?.jurisdictionContext || resource.jurisdictionContext;
  const hasEdition = hasUsableValue(resource.edition)
    || hasUsableValue(editionContext?.edition)
    || hasUsableValue(editionContext?.version)
    || hasUsableValue(editionContext?.publicationYear)
    || hasUsableValue(identifier?.edition)
    || hasUsableValue(identifier?.version)
    || hasUsableValue(identifier?.publicationYear);
  const hasJurisdiction = hasUsableValue(resource.jurisdiction)
    || hasUsableValue(resource.geographicScope)
    || hasUsableValue(jurisdictionContext?.jurisdiction)
    || hasUsableValue(jurisdictionContext?.geographicScope);
  const hasScope = link ? hasCitationContext(link) || hasUsableValue(jurisdictionContext?.applicabilityNote) : false;
  if (!hasEdition) missing.push('edition/version');
  if (!hasJurisdiction) missing.push('jurisdiction/geographicScope');
  if (link && !hasScope) missing.push('citation/scope');
  return missing;
}

function collectPlaceholderContextWarnings(resource: Resource, link?: NodeResourceLink) {
  const warnings: string[] = [];
  const entries: Array<[string, unknown]> = [
    ['edition', resource.edition],
    ['standardIdentifier.edition', resource.standardIdentifier?.edition],
    ['standardIdentifier.version', resource.standardIdentifier?.version],
    ['editionContext.edition', resource.editionContext?.edition],
    ['editionContext.version', resource.editionContext?.version],
    ['jurisdictionContext.jurisdiction', resource.jurisdictionContext?.jurisdiction],
    ['jurisdictionContext.geographicScope', resource.jurisdictionContext?.geographicScope],
    ['jurisdictionContext.applicabilityNote', resource.jurisdictionContext?.applicabilityNote],
    ['reviewContext.sourceOfContext', resource.reviewContext?.sourceOfContext],
    ['reviewContext.rationale', resource.reviewContext?.rationale],
  ];
  if (link?.standardContext) {
    entries.push(
      ['link.standardContext.editionContext.edition', link.standardContext.editionContext?.edition],
      ['link.standardContext.editionContext.version', link.standardContext.editionContext?.version],
      ['link.standardContext.jurisdictionContext.jurisdiction', link.standardContext.jurisdictionContext?.jurisdiction],
      ['link.standardContext.jurisdictionContext.geographicScope', link.standardContext.jurisdictionContext?.geographicScope],
      ['link.standardContext.jurisdictionContext.applicabilityNote', link.standardContext.jurisdictionContext?.applicabilityNote],
      ['link.standardContext.reviewContext.sourceOfContext', link.standardContext.reviewContext?.sourceOfContext],
      ['link.standardContext.reviewContext.rationale', link.standardContext.reviewContext?.rationale],
    );
  }
  for (const [field, value] of entries) {
    if (isPlaceholderStandardContextValue(value)) warnings.push(`${resource.id}${link ? `/${link.id}` : ''}: placeholder standards context value in ${field}`);
  }
  return warnings;
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
  if (isStandardLikeResource(resource)) {
    const missingFields = standardContextMissingFields(resource);
    if (missingFields.includes('jurisdiction/geographicScope')) warnings.push(`${resource.id}: code/standard resource missing jurisdiction or geographicScope`);
    if (missingFields.includes('edition/version')) warnings.push(`${resource.id}: code/standard resource missing edition/version context`);
    warnings.push(...collectPlaceholderContextWarnings(resource));
  }
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
  if (isStandardLikeResource(resource)) {
    const missingFields = standardContextMissingFields(resource, link);
    if (missingFields.length && !isAcceptedLink(link)) {
      warnings.push(`${link.id}: standard/code-like link missing ${missingFields.join(', ')} context`);
    }
    warnings.push(...collectPlaceholderContextWarnings(resource, link));
    if (isAcceptedLink(link) && missingFields.length && !hasStructuredMissingContextJustification(resource, link)) {
      blockers.push(`${link.id}: accepted standard/code-like link requires edition/version, citation/scope, and jurisdiction/geographicScope context or structured reviewer/source justification; missing ${missingFields.join(', ')}`);
    }
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'asce') && !hasCitationContext(link) && !hasStructuredMissingContextJustification(resource, link)) {
    blockers.push(`${link.id}: ASCE link cannot be promoted without edition/section/adoption context`);
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'aci') && !hasCitationContext(link) && !hasStructuredMissingContextJustification(resource, link)) {
    blockers.push(`${link.id}: ACI link cannot be promoted without edition/section-specific context`);
  }
  if (isAcceptedLink(link) && sourceFamilyIncludes(resource, 'fhwa') && !hasStructuredMissingContextJustification(resource, link) && !/transportation|geotechnical|scope/i.test(link.reviewNotes || resource.jurisdiction || resource.abstractOrSummary || '')) {
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
  const standardsContextWarnings: string[] = [];
  const standardResourceIds = new Set<string>();
  let standardsMissingEdition = 0;
  let standardsMissingJurisdiction = 0;
  let standardsMissingScope = 0;
  let standardsContextComplete = 0;
  let standardsContextPartial = 0;
  let standardsContextNeedsReview = 0;
  let standardsAcceptedMissingContext = 0;
  let standardsPromotionBlocked = 0;
  let standardsContextReviewable = 0;
  const familyIds = approvedSourceFamilyIds(data.sourceFamilies);
  const resourceIds = new Set<string>();
  for (const resource of data.resources) {
    if (resourceIds.has(resource.id)) errors.push(`${resource.id}: duplicate resource id`);
    resourceIds.add(resource.id);
    validateResource(resource, errors, warnings, options);
    if (isStandardLikeResource(resource)) {
      standardResourceIds.add(resource.id);
      const missing = standardContextMissingFields(resource);
      if (missing.includes('edition/version')) standardsMissingEdition += 1;
      if (missing.includes('jurisdiction/geographicScope')) standardsMissingJurisdiction += 1;
      standardsContextWarnings.push(...collectPlaceholderContextWarnings(resource));
    }
    for (const familyId of resource.sourceFamilyIds || []) if (!familyIds.has(familyId)) errors.push(`${resource.id}: sourceFamilyId not registered: ${familyId}`);
  }
  const duplicateGroups = detectResourceDuplicates(data.resources);
  for (const group of duplicateGroups) errors.push(`duplicate ${group.kind}: ${group.key} -> ${group.resourceIds.join(', ')}`);
  const resourceById = new Map(data.resources.map((resource) => [resource.id, resource]));
  for (const link of data.nodeResourceLinks) {
    const resource = resourceById.get(link.resourceId);
    validateLink(link, resourceById, errors, warnings, blockers, options);
    if (resource && isStandardLikeResource(resource)) {
      const missing = standardContextMissingFields(resource, link);
      const status = standardContextStatus(resource, link);
      if (missing.length) standardsContextReviewable += 1;
      if (missing.includes('citation/scope')) standardsMissingScope += 1;
      if (missing.length && !hasStructuredMissingContextJustification(resource, link)) {
        standardsPromotionBlocked += 1;
      }
      if (isAcceptedLink(link) && missing.length && !hasStructuredMissingContextJustification(resource, link)) {
        standardsAcceptedMissingContext += 1;
      }
      if (link.reviewStatus === 'needs_review' && missing.length) standardsContextNeedsReview += 1;
      else if (status === 'complete' && missing.length === 0) standardsContextComplete += 1;
      else if (status === 'partial' || missing.length > 0) standardsContextPartial += 1;
      standardsContextWarnings.push(...collectPlaceholderContextWarnings(resource, link));
    }
  }
  for (const candidate of data.resourceCandidates) {
    if (candidate.reviewStatus === 'rejected' && !candidate.rejectionReason?.trim()) warnings.push(`${candidate.id}: rejected candidate missing rejection rationale`);
  }
  const brokenLinkCount = data.resourceChecks.filter((check) => check.checkType === 'url_health' && check.status === 'fail').length;
  return {
    ok: errors.length === 0 && blockers.length === 0,
    errors,
    warnings,
    blockers,
    duplicateCount: duplicateGroups.length,
    brokenLinkCount,
    standardsTotal: standardResourceIds.size,
    standardsMissingEdition,
    standardsMissingJurisdiction,
    standardsMissingScope,
    standardsContextComplete,
    standardsContextPartial,
    standardsContextNeedsReview,
    standardsAcceptedMissingContext,
    standardsPromotionBlocked,
    standardsContextReviewable,
    standardsContextWarnings: Array.from(new Set(standardsContextWarnings)),
  };
}
