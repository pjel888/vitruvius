import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import type {
  LocalFileIndex,
  NodeResourceLink,
  Resource,
  ResourceCandidate,
  ResourceLayerData,
  ReviewDecision,
  ReviewDecisionLog,
  ReviewStatus,
  StandardContext,
  StandardContextConfidence,
  StandardContextStatus,
} from './types';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './types';
import {
  readLocalFileIndex,
  readResourceLayerData,
  readReviewDecisionLog,
  resourceLayerFilePaths,
} from './registry';
import { detectResourceDuplicates } from './deduplication';
import { isPlaceholderStandardContextValue, standardContextMissingFields, validateResourceLayerData } from './validation';
import { withResourceLayerTransaction } from './transactionManifest';

export type LinkReviewDecision = 'accept' | 'reject' | 'needs_review' | 'downgrade' | 'reopen';
export type CandidateReviewDecision =
  | 'accept_as_resource'
  | 'link_to_node'
  | 'reject_candidate'
  | 'needs_more_context'
  | 'mark_duplicate'
  | 'hold';
export type LocalFileReviewDecision = 'admit_as_resource' | 'link_to_node' | 'reject_local_file' | 'needs_review' | 'ignore';
export type StandardsContextDecision =
  | 'keep_needs_review'
  | 'update_context_partial'
  | 'update_context_complete'
  | 'mark_context_not_required'
  | 'reject_context_update'
  | 'defer_context_review'
  | 'promote_if_context_complete'
  | 'demote_to_needs_review';

export interface ReviewFilters {
  status?: string;
  nodeId?: string;
  resourceId?: string;
  sourceFamily?: string;
  authorityTier?: string | number;
  issueType?: string;
  limit?: number;
  offset?: number;
}

export interface ReviewDecisionBody {
  decision: LinkReviewDecision | CandidateReviewDecision | LocalFileReviewDecision;
  reviewer?: string;
  rationale?: string;
  notes?: string;
  dryRun?: boolean;
  statusReason?: string;
  authorityTier?: number;
  authorityScore?: number;
  edition?: string;
  version?: string;
  sectionRefs?: string[];
  chapterRefs?: string[];
  pageRefs?: string[];
  sourceRights?: Resource['sourceRights'];
  admissionProvenance?: Resource['admissionProvenance'];
  standardContextJustification?: string;
  targetNodeId?: string;
  resourceFields?: Partial<Resource>;
  linkFields?: Partial<NodeResourceLink>;
  duplicateOfResourceId?: string;
}

export interface StandardsContextDecisionBody {
  decision: StandardsContextDecision;
  reviewer?: string;
  rationale?: string;
  notes?: string;
  dryRun?: boolean;
  edition?: string;
  version?: string;
  publicationYear?: number;
  amendment?: string;
  errata?: string;
  jurisdiction?: string;
  geographicScope?: string;
  adoptionStatus?: string;
  codeCycle?: string;
  applicabilityNote?: string;
  sourceOfContext?: string;
  sourceUrl?: string;
  sourceNote?: string;
  confidence?: StandardContextConfidence;
  sectionRefs?: string[];
  chapterRefs?: string[];
  pageRefs?: string[];
  fragmentRefs?: string[];
}

export class ResourceReviewError extends Error {
  status: number;
  details: string[];

  constructor(message: string, status = 400, details: string[] = []) {
    super(message);
    this.status = status;
    this.details = details;
  }
}

function nowIso() {
  return new Date().toISOString();
}

function deterministicWrite(path: string, payload: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  const tempPath = `${path}.tmp`;
  writeFileSync(tempPath, `${JSON.stringify(payload, null, 2)}\n`);
  if (existsSync(path)) rmSync(path, { force: true });
  renameSync(tempPath, path);
}

function readJsonObject(path: string): Record<string, unknown> {
  if (!existsSync(path)) return {};
  const value = JSON.parse(readFileSync(path, 'utf-8').replace(/^\uFEFF/, '') || '{}');
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new ResourceReviewError(`${path} must contain a JSON object`, 500);
  }
  return value as Record<string, unknown>;
}

function requireReviewer(body: ReviewDecisionBody) {
  const reviewer = body.reviewer?.trim();
  if (!reviewer) throw new ResourceReviewError('reviewer is required');
  return reviewer;
}

function requireRationale(body: ReviewDecisionBody) {
  const rationale = body.rationale?.trim();
  if (!rationale) throw new ResourceReviewError('rationale is required');
  return rationale;
}

function requireString(value: unknown, label: string) {
  if (typeof value !== 'string' || !value.trim()) throw new ResourceReviewError(`${label} is required`);
  return value.trim();
}

function score(value: unknown, label: string, fallback: number) {
  if (value === undefined || value === null || value === '') return fallback;
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric < 0 || numeric > 1) throw new ResourceReviewError(`${label} must be between 0 and 1`);
  return numeric;
}

function isAccepted(status: string | undefined) {
  return status === 'accepted' || status === 'human_reviewed';
}

function isStandardLike(resource?: Resource) {
  return resource?.resourceType === 'standard' || resource?.resourceType === 'code';
}

function hasContext(link: Partial<NodeResourceLink>) {
  return Boolean(link.sectionRefs?.length || link.chapterRefs?.length || link.pageRefs?.length || link.fragmentRefs?.length);
}

function reviewContextFor(resource?: Resource, link?: Partial<NodeResourceLink>) {
  return link?.standardContext?.reviewContext || resource?.reviewContext;
}

function hasStructuredContextJustification(resource?: Resource, link?: Partial<NodeResourceLink>) {
  const reviewContext = reviewContextFor(resource, link);
  if (!reviewContext) return false;
  if (!['justified_missing', 'not_required'].includes(reviewContext.contextStatus)) return false;
  const reviewedBy = reviewContext.reviewedBy?.trim() || '';
  const rationale = reviewContext.rationale?.trim() || '';
  const sourceOfContext = reviewContext.sourceOfContext?.trim() || '';
  if (!reviewedBy || !rationale || !sourceOfContext) return false;
  if (isPlaceholderStandardContextValue(reviewedBy) || isPlaceholderStandardContextValue(rationale) || isPlaceholderStandardContextValue(sourceOfContext)) return false;
  return true;
}

function appendReviewNotes(existing: string | undefined, body: ReviewDecisionBody) {
  const parts = [existing?.trim()].filter(Boolean) as string[];
  if (body.statusReason?.trim()) parts.push(`Status reason: ${body.statusReason.trim()}`);
  if (body.notes?.trim()) parts.push(`Reviewer notes: ${body.notes.trim()}`);
  if (body.standardContextJustification?.trim()) {
    parts.push(`Explicit standard-context reviewer justification: ${body.standardContextJustification.trim()}`);
  }
  return parts.join('\n');
}

function standardContextMissing(resource: Resource | undefined, link: Partial<NodeResourceLink>) {
  if (!isStandardLike(resource)) return false;
  return standardContextMissingFields(resource, link as NodeResourceLink).length > 0 && !hasStructuredContextJustification(resource, link);
}

function linkWarnings(link: NodeResourceLink, resource?: Resource) {
  const warnings: string[] = [];
  if (!resource) warnings.push('Linked resource is missing from the registry.');
  if (standardContextMissing(resource, link)) {
    warnings.push(`Missing standards context: ${standardContextMissingFields(resource!, link).join(', ')}.`);
  }
  if (link.reviewStatus === 'rejected' && !link.reviewNotes?.trim()) warnings.push('Rejected link lacks preserved rejection rationale.');
  if (resource?.sourceFamilyIds?.includes('wbdg_nibs') && (resource.authorityTier ?? 5) <= 1) {
    warnings.push('WBDG/NIBS must remain contextual guidance unless explicitly reviewed otherwise.');
  }
  return warnings;
}

function standardContextStatus(resource?: Resource, link?: Partial<NodeResourceLink>): StandardContextStatus {
  if (!isStandardLike(resource)) return 'not_required';
  const reviewContext = reviewContextFor(resource, link);
  if (reviewContext?.contextStatus) return reviewContext.contextStatus;
  const missing = standardContextMissingFields(resource, link as NodeResourceLink);
  if (missing.length === 0) return 'complete';
  if (missing.length < 3) return 'partial';
  return 'needs_human_review';
}

function promotionBlockerReasons(resource?: Resource, link?: Partial<NodeResourceLink>) {
  if (!isStandardLike(resource)) return [];
  const missing = standardContextMissingFields(resource, link as NodeResourceLink);
  if (!missing.length || hasStructuredContextJustification(resource, link)) return [];
  return [`Promotion blocked until standards context is complete or explicitly reviewer/source justified: missing ${missing.join(', ')}.`];
}

export function linkItem(link: NodeResourceLink, resource?: Resource) {
  const missingFields = resource ? standardContextMissingFields(resource, link) : [];
  return {
    type: 'node_resource_link' as const,
    id: link.id,
    title: resource?.title || '(missing resource)',
    nodeId: link.nodeId,
    resourceId: link.resourceId,
    sourceFamilyIds: resource?.sourceFamilyIds || [],
    authorityTier: resource?.authorityTier,
    authorityScore: link.authorityScore,
    verificationStatus: resource?.verificationStatus || 'unverified',
    reviewStatus: link.reviewStatus,
    relationship: link.relationship,
    rationale: link.rationale,
    reviewNotes: link.reviewNotes,
    missingStandardContext: standardContextMissing(resource, link),
    missingStandardContextFields: missingFields,
    standardContextStatus: standardContextStatus(resource, link),
    promotionBlocked: promotionBlockerReasons(resource, link).length > 0,
    promotionBlockerReasons: promotionBlockerReasons(resource, link),
    organization: resource?.organization,
    resourceType: resource?.resourceType,
    currentEdition: resource?.edition || resource?.editionContext?.edition || resource?.standardIdentifier?.edition,
    currentVersion: resource?.editionContext?.version || resource?.standardIdentifier?.version,
    currentPublicationYear: resource?.year || resource?.editionContext?.publicationYear || resource?.standardIdentifier?.publicationYear,
    currentJurisdiction: resource?.jurisdiction || resource?.jurisdictionContext?.jurisdiction,
    currentGeographicScope: resource?.geographicScope || resource?.jurisdictionContext?.geographicScope,
    sourceOfContext: reviewContextFor(resource, link)?.sourceOfContext,
    warnings: linkWarnings(link, resource),
    link,
    resource,
  };
}

function candidateTitle(candidate: ResourceCandidate) {
  return candidate.rawTitle || candidate.rawIdentifier || candidate.rawUrl || candidate.id;
}

export function candidateItem(candidate: ResourceCandidate, data: ResourceLayerData) {
  const duplicate = data.resources.find((resource) => (
    candidate.rawIdentifier === resource.id
    || candidate.rawUrl === resource.url
    || candidate.rawUrl === resource.canonicalUrl
    || candidate.duplicateOfResourceId === resource.id
  ));
  const warnings = [
    !candidate.rawTitle?.trim() ? 'Candidate missing title/label.' : '',
    !candidate.rawUrl && !candidate.rawIdentifier ? 'Candidate missing URL or stable identifier.' : '',
    candidate.reviewStatus === 'rejected' && !candidate.rejectionReason?.trim() ? 'Rejected candidate lacks rationale.' : '',
    duplicate ? `Candidate appears related to existing resource ${duplicate.id}.` : '',
  ].filter(Boolean);
  return {
    type: 'candidate' as const,
    id: candidate.id,
    title: candidateTitle(candidate),
    nodeId: candidate.nodeId,
    rawUrl: candidate.rawUrl,
    rawIdentifier: candidate.rawIdentifier,
    preliminaryScore: candidate.preliminaryScore,
    rankingScore: candidate.preliminaryScore,
    reviewStatus: candidate.reviewStatus,
    dedupeKey: candidate.dedupeKey,
    duplicateResourceId: duplicate?.id,
    sourceFamilyIds: duplicate?.sourceFamilyIds || [],
    authorityTier: duplicate?.authorityTier,
    warnings,
    suggestedNodeId: candidate.nodeId,
    suggestedResourceId: candidate.rawIdentifier,
    candidate,
  };
}

export function localFileItem(indexed: Resource, data: ResourceLayerData) {
  const admitted = data.resources.find((resource) => resource.localFileHash && resource.localFileHash === indexed.localFileHash);
  const linkedNodeCount = admitted ? data.nodeResourceLinks.filter((link) => link.resourceId === admitted.id).length : 0;
  return {
    type: 'local_file' as const,
    id: indexed.id,
    fileId: indexed.id,
    title: indexed.title || indexed.localPath || indexed.id,
    localPath: indexed.localPath,
    localFileHash: indexed.localFileHash,
    localFileType: indexed.localFileType,
    localFileSizeBytes: indexed.localFileSizeBytes,
    linkedNodeCount,
    admitted: Boolean(admitted),
    admittedResourceId: admitted?.id,
    reviewStatus: admitted ? 'accepted' : 'candidate',
    sourceFamilyIds: admitted?.sourceFamilyIds || indexed.sourceFamilyIds || [],
    authorityTier: admitted?.authorityTier || indexed.authorityTier,
    warnings: [
      !indexed.localFileHash ? 'Local file index record missing hash.' : '',
      !indexed.localPath ? 'Local file index record missing path.' : '',
      !admitted ? 'Indexed local file is not admitted to the Resource Registry.' : '',
    ].filter(Boolean),
    resource: indexed,
  };
}

function filterItems<T extends { reviewStatus?: string; nodeId?: string; resourceId?: string; sourceFamilyIds?: string[]; authorityTier?: number; warnings?: string[] }>(items: T[], filters: ReviewFilters) {
  let next = items;
  if (filters.status && filters.status !== 'all') next = next.filter((item) => item.reviewStatus === filters.status);
  if (filters.nodeId) next = next.filter((item) => item.nodeId === filters.nodeId);
  if (filters.resourceId) next = next.filter((item) => item.resourceId === filters.resourceId);
  if (filters.sourceFamily) next = next.filter((item) => item.sourceFamilyIds?.includes(filters.sourceFamily!));
  if (filters.authorityTier) next = next.filter((item) => String(item.authorityTier || 'unknown') === String(filters.authorityTier));
  if (filters.issueType === 'standard_context') next = next.filter((item) => item.warnings?.some((warning) => /edition|section|standard/i.test(warning)));
  const offset = Math.max(0, Number(filters.offset || 0));
  const limit = filters.limit == null ? undefined : Math.max(1, Number(filters.limit));
  return limit ? next.slice(offset, offset + limit) : next.slice(offset);
}

function indexedHashes(repoRoot: string) {
  return new Set(readLocalFileIndex(repoRoot).resources.map((resource) => resource.localFileHash).filter(Boolean) as string[]);
}

function validateMutation(repoRoot: string, data: ResourceLayerData) {
  const result = validateResourceLayerData(data, {
    repoRoot,
    localIndexedHashes: indexedHashes(repoRoot),
    fullLocalFileCheck: false,
  });
  if (!result.ok) throw new ResourceReviewError('review decision would break Resource Layer validation', 400, [...result.blockers, ...result.errors]);
  return result;
}

function readMutableData(repoRoot: string): ResourceLayerData {
  return structuredClone(readResourceLayerData(repoRoot));
}

function writeRegistry(repoRoot: string, data: ResourceLayerData, files: { resources?: boolean; links?: boolean; candidates?: boolean }) {
  const paths = resourceLayerFilePaths(repoRoot);
  const generatedAt = nowIso();
  if (files.resources) deterministicWrite(paths.resources, { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, generatedAt, resources: data.resources });
  if (files.links) deterministicWrite(paths.links, { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, generatedAt, nodeResourceLinks: data.nodeResourceLinks });
  if (files.candidates) deterministicWrite(paths.candidates, { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, generatedAt, resourceCandidates: data.resourceCandidates });
}

function decisionId(entry: Omit<ReviewDecision, 'decision_id'>, existing: ReviewDecision[]) {
  const digest = createHash('sha256').update(JSON.stringify(entry)).digest('hex').slice(0, 12);
  const base = `review-${entry.created_at.replace(/\D/g, '').slice(0, 14)}-${digest}`;
  if (!existing.some((item) => item.decision_id === base)) return base;
  let suffix = 2;
  while (existing.some((item) => item.decision_id === `${base}-${suffix}`)) suffix += 1;
  return `${base}-${suffix}`;
}

function appendDecision(repoRoot: string, entry: Omit<ReviewDecision, 'decision_id'>) {
  const paths = resourceLayerFilePaths(repoRoot);
  const log: ReviewDecisionLog = readReviewDecisionLog(repoRoot);
  const decision = { decision_id: decisionId(entry, log.reviewDecisions), ...entry };
  deterministicWrite(paths.reviewDecisions, {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    reviewDecisions: [...log.reviewDecisions, decision],
  });
  return decision;
}

function standardContextTarget(data: ResourceLayerData, id: string) {
  const link = data.nodeResourceLinks.find((item) => item.id === id);
  if (link) {
    const resource = data.resources.find((item) => item.id === link.resourceId);
    if (!resource) throw new ResourceReviewError(`standard context target resource not found for link ${id}`, 404);
    return { link, resource, targetType: 'node_resource_link' as const, targetId: link.id };
  }
  const resource = data.resources.find((item) => item.id === id);
  if (resource) {
    const linked = data.nodeResourceLinks.find((item) => item.resourceId === resource.id);
    return { link: linked, resource, targetType: 'resource' as const, targetId: resource.id };
  }
  throw new ResourceReviewError(`standard context target not found: ${id}`, 404);
}

function validateStandardsContextDecisionBody(body: StandardsContextDecisionBody) {
  const allowedDecisions: StandardsContextDecision[] = [
    'keep_needs_review',
    'update_context_partial',
    'update_context_complete',
    'mark_context_not_required',
    'reject_context_update',
    'defer_context_review',
    'promote_if_context_complete',
    'demote_to_needs_review',
  ];
  if (!allowedDecisions.includes(body.decision)) throw new ResourceReviewError(`unsupported standards context decision: ${String(body.decision)}`);
  const reviewer = requireReviewer(body as ReviewDecisionBody);
  const rationale = requireRationale(body as ReviewDecisionBody);
  for (const [field, value] of Object.entries(body)) {
    if (['notes', 'dryRun', 'decision', 'sectionRefs', 'chapterRefs', 'pageRefs', 'fragmentRefs'].includes(field)) continue;
    if (isPlaceholderStandardContextValue(value)) throw new ResourceReviewError(`${field} contains a placeholder standards-context value`);
  }
  if (body.confidence !== undefined && !['low', 'medium', 'high'].includes(body.confidence)) {
    throw new ResourceReviewError('confidence must be low, medium, or high');
  }
  if (body.publicationYear !== undefined && (!Number.isInteger(Number(body.publicationYear)) || Number(body.publicationYear) < 1500 || Number(body.publicationYear) > 2200)) {
    throw new ResourceReviewError('publicationYear must be a plausible four-digit year');
  }
  if (['update_context_complete', 'mark_context_not_required', 'promote_if_context_complete'].includes(body.decision) && !body.sourceOfContext?.trim()) {
    throw new ResourceReviewError(`${body.decision} requires sourceOfContext`);
  }
  return { reviewer, rationale };
}

function mergeDefined<T extends object>(existing: T | undefined, updates: Partial<T>) {
  const next = { ...(existing || {}) } as T;
  for (const [key, value] of Object.entries(updates)) {
    if (value !== undefined && value !== null && value !== '') (next as Record<string, unknown>)[key] = value;
  }
  return next;
}

function hasContextUpdate(body: StandardsContextDecisionBody) {
  return Boolean(
    body.edition || body.version || body.publicationYear || body.amendment || body.errata
    || body.jurisdiction || body.geographicScope || body.adoptionStatus || body.codeCycle || body.applicabilityNote
    || body.sourceOfContext || body.sourceUrl || body.sourceNote
    || body.sectionRefs?.length || body.chapterRefs?.length || body.pageRefs?.length || body.fragmentRefs?.length
  );
}

function nextContextStatus(body: StandardsContextDecisionBody): StandardContextStatus {
  if (body.decision === 'update_context_complete' || body.decision === 'promote_if_context_complete') return 'complete';
  if (body.decision === 'mark_context_not_required') return 'not_required';
  if (body.decision === 'reject_context_update') return 'rejected';
  if (body.decision === 'update_context_partial') return 'partial';
  return 'needs_human_review';
}

function applyStandardsContextPatch(resource: Resource, link: NodeResourceLink | undefined, body: StandardsContextDecisionBody, timestamp: string) {
  const status = nextContextStatus(body);
  const reviewContext = {
    contextStatus: status,
    reviewedBy: body.reviewer?.trim(),
    reviewedAt: timestamp,
    rationale: body.rationale?.trim(),
    sourceOfContext: body.sourceOfContext?.trim(),
    confidence: body.confidence,
  };
  if (body.decision !== 'reject_context_update' && hasContextUpdate(body)) {
    if (body.edition || body.version) resource.edition = String(body.edition || body.version);
    if (body.publicationYear !== undefined) resource.year = Number(body.publicationYear);
    resource.standardIdentifier = mergeDefined(resource.standardIdentifier, {
      organization: resource.organization,
      title: resource.title,
      edition: body.edition,
      version: body.version,
      publicationYear: body.publicationYear === undefined ? undefined : Number(body.publicationYear),
    });
    resource.editionContext = mergeDefined(resource.editionContext, {
      edition: body.edition,
      version: body.version,
      publicationYear: body.publicationYear === undefined ? undefined : Number(body.publicationYear),
      amendment: body.amendment,
      errata: body.errata,
      sourceUrl: body.sourceUrl,
      sourceNote: body.sourceNote || body.sourceOfContext,
    });
    resource.jurisdictionContext = mergeDefined(resource.jurisdictionContext, {
      jurisdiction: body.jurisdiction,
      geographicScope: body.geographicScope,
      adoptionStatus: body.adoptionStatus,
      codeCycle: body.codeCycle,
      applicabilityNote: body.applicabilityNote,
    });
    if (body.jurisdiction) resource.jurisdiction = body.jurisdiction;
    if (body.geographicScope) resource.geographicScope = body.geographicScope as Resource['geographicScope'];
  }
  resource.reviewContext = mergeDefined(resource.reviewContext, reviewContext);
  resource.updatedAt = timestamp;
  if (link) {
    if (body.sectionRefs?.length) link.sectionRefs = body.sectionRefs;
    if (body.chapterRefs?.length) link.chapterRefs = body.chapterRefs;
    if (body.pageRefs?.length) link.pageRefs = body.pageRefs;
    if (body.fragmentRefs?.length) link.fragmentRefs = body.fragmentRefs;
    link.standardContext = mergeDefined<StandardContext>(link.standardContext, {
      standardIdentifier: resource.standardIdentifier,
      editionContext: resource.editionContext,
      jurisdictionContext: resource.jurisdictionContext,
      reviewContext,
    });
    if (body.decision === 'promote_if_context_complete') {
      link.reviewStatus = 'accepted';
      link.verifiedBy = 'human';
    } else if (['keep_needs_review', 'demote_to_needs_review', 'defer_context_review'].includes(body.decision)) {
      link.reviewStatus = 'needs_review';
    }
    link.reviewNotes = [
      link.reviewNotes,
      `Standards context decision (${body.decision}): ${body.rationale?.trim()}`,
      body.notes?.trim() ? `Reviewer notes: ${body.notes.trim()}` : '',
    ].filter(Boolean).join('\n');
    link.updatedAt = timestamp;
  }
}

function buildStandardsContextResponse(repoRoot: string, data: ResourceLayerData, id: string, before?: { resource: Resource; link?: NodeResourceLink }) {
  const { resource, link } = standardContextTarget(data, id);
  const validation = validateResourceLayerData(data, { repoRoot, localIndexedHashes: indexedHashes(repoRoot), fullLocalFileCheck: false });
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    id,
    resourceId: resource.id,
    linkId: link?.id,
    item: link ? linkItem(link, resource) : {
      type: 'resource',
      id: resource.id,
      title: resource.title,
      resourceId: resource.id,
      sourceFamilyIds: resource.sourceFamilyIds || [],
      reviewStatus: resource.reviewContext?.contextStatus || 'needs_review',
      resource,
      missingStandardContextFields: standardContextMissingFields(resource),
      standardContextStatus: standardContextStatus(resource),
      promotionBlocked: promotionBlockerReasons(resource).length > 0,
      promotionBlockerReasons: promotionBlockerReasons(resource),
      warnings: standardContextMissingFields(resource).map((field) => `Missing standards context: ${field}`),
    },
    currentContext: {
      standardIdentifier: resource.standardIdentifier,
      editionContext: resource.editionContext,
      jurisdictionContext: resource.jurisdictionContext,
      reviewContext: reviewContextFor(resource, link),
      linkStandardContext: link?.standardContext,
      sectionRefs: link?.sectionRefs,
      chapterRefs: link?.chapterRefs,
      pageRefs: link?.pageRefs,
      fragmentRefs: link?.fragmentRefs,
    },
    before,
    validationImpact: {
      ok: validation.ok,
      warnings: validation.warnings,
      blockers: validation.blockers,
      metrics: {
        standardsTotal: validation.standardsTotal,
        standardsMissingEdition: validation.standardsMissingEdition,
        standardsMissingJurisdiction: validation.standardsMissingJurisdiction,
        standardsMissingScope: validation.standardsMissingScope,
        standardsContextComplete: validation.standardsContextComplete,
        standardsContextPartial: validation.standardsContextPartial,
        standardsContextNeedsReview: validation.standardsContextNeedsReview,
        standardsAcceptedMissingContext: validation.standardsAcceptedMissingContext,
        standardsPromotionBlocked: validation.standardsPromotionBlocked,
        standardsContextReviewable: validation.standardsContextReviewable,
      },
    },
  };
}

function previewOrApplyStandardsContext(repoRoot: string, id: string, body: StandardsContextDecisionBody, apply: boolean) {
  const { reviewer, rationale } = validateStandardsContextDecisionBody(body);
  const data = readMutableData(repoRoot);
  const target = standardContextTarget(data, id);
  if (!isStandardLike(target.resource)) throw new ResourceReviewError(`resource is not standard/code-like: ${target.resource.id}`);
  const before = { resource: structuredClone(target.resource), link: target.link ? structuredClone(target.link) : undefined };
  const previousStatus = target.link?.reviewStatus || target.resource.reviewContext?.contextStatus || 'unreviewed';
  const timestamp = nowIso();
  applyStandardsContextPatch(target.resource, target.link, body, timestamp);
  const missingAfter = standardContextMissingFields(target.resource, target.link);
  if (['update_context_complete', 'promote_if_context_complete'].includes(body.decision) && missingAfter.length && !hasStructuredContextJustification(target.resource, target.link)) {
    throw new ResourceReviewError(`${body.decision} requires complete standards context; still missing ${missingAfter.join(', ')}`);
  }
  if (body.decision === 'promote_if_context_complete' && (!target.link || missingAfter.length)) {
    throw new ResourceReviewError('promote_if_context_complete requires a link target and complete context');
  }
  const validation = validateMutation(repoRoot, data);
  const response = {
    dryRun: !apply || Boolean(body.dryRun),
    ...buildStandardsContextResponse(repoRoot, data, id, before),
    diff: {
      resourceBefore: before.resource,
      resourceAfter: structuredClone(target.resource),
      linkBefore: before.link,
      linkAfter: target.link ? structuredClone(target.link) : undefined,
      missingFieldsBefore: standardContextMissingFields(before.resource, before.link),
      missingFieldsAfter: missingAfter,
    },
    transactionManifestPreview: {
      operationType: 'standard_context_update',
      filesTouched: (() => {
        const paths = resourceLayerFilePaths(repoRoot);
        return [paths.resources, paths.reviewDecisions, ...(target.link ? [paths.links] : [])];
      })(),
    },
    validation,
  };
  if (!apply || body.dryRun) return response;
  const paths = resourceLayerFilePaths(repoRoot);
  const filesTouched = [paths.resources, paths.reviewDecisions, ...(target.link ? [paths.links] : [])];
  const { result: reviewDecision, manifest } = withResourceLayerTransaction(repoRoot, 'standard_context_update', filesTouched, () => {
    writeRegistry(repoRoot, data, { resources: true, links: Boolean(target.link) });
    return appendDecision(repoRoot, {
      target_type: 'standard_context',
      target_id: id,
      previous_status: previousStatus,
      new_status: target.link?.reviewStatus || target.resource.reviewContext?.contextStatus,
      decision: body.decision,
      reviewer,
      rationale,
      notes: body.notes,
      created_at: timestamp,
      metadata: {
        resourceId: target.resource.id,
        linkId: target.link?.id,
        before,
        after: { resource: target.resource, link: target.link },
        missingFieldsBefore: standardContextMissingFields(before.resource, before.link),
        missingFieldsAfter: missingAfter,
        sourceOfContext: body.sourceOfContext,
      },
    });
  });
  return { ...response, dryRun: false, reviewDecision, transactionManifest: manifest };
}

export function getStandardsContextReviewDetail(repoRoot: string, id: string) {
  return buildStandardsContextResponse(repoRoot, readResourceLayerData(repoRoot), id);
}

export function previewStandardsContextDecision(repoRoot: string, id: string, body: StandardsContextDecisionBody) {
  return previewOrApplyStandardsContext(repoRoot, id, { ...body, dryRun: true }, false);
}

export function decideStandardsContext(repoRoot: string, id: string, body: StandardsContextDecisionBody) {
  return previewOrApplyStandardsContext(repoRoot, id, body, true);
}

function localIndex(repoRoot: string): LocalFileIndex {
  const path = resourceLayerFilePaths(repoRoot).localFileIndex;
  if (!existsSync(path)) return { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, resources: [] };
  const payload = readJsonObject(path);
  return {
    schemaVersion: String(payload.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION),
    generatedAt: typeof payload.generatedAt === 'string' ? payload.generatedAt : undefined,
    indexedResourceCount: typeof payload.indexedResourceCount === 'number' ? payload.indexedResourceCount : undefined,
    scannedDirectories: Array.isArray(payload.scannedDirectories) ? payload.scannedDirectories.map(String) : [],
    errors: Array.isArray(payload.errors) ? payload.errors.map(String) : [],
    resources: Array.isArray(payload.resources) ? payload.resources as Resource[] : [],
  };
}

export function buildResourceReviewReport(repoRoot: string) {
  const data = readResourceLayerData(repoRoot);
  const local = localIndex(repoRoot);
  const localHashes = new Set(local.resources.map((resource) => resource.localFileHash).filter(Boolean));
  const byId = new Map(data.resources.map((resource) => [resource.id, resource]));
  const standardLinks = data.nodeResourceLinks.filter((link) => link.reviewStatus !== 'rejected' && standardContextMissing(byId.get(link.resourceId), link));
  const validation = validateResourceLayerData(data, { repoRoot, localIndexedHashes: indexedHashes(repoRoot) });
  const countBy = (items: string[]) => items.reduce<Record<string, number>>((acc, item) => {
    acc[item] = (acc[item] || 0) + 1;
    return acc;
  }, {});
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    resourcesTotal: data.resources.length,
    resourcesNonRejected: data.resources.filter((resource) => resource.verificationStatus !== 'rejected').length,
    resourcesWithAcceptedLinks: new Set(data.nodeResourceLinks.filter((link) => isAccepted(link.reviewStatus)).map((link) => link.resourceId)).size,
    acceptedNodeResourceLinks: data.nodeResourceLinks.filter((link) => isAccepted(link.reviewStatus)).length,
    candidateResources: data.resourceCandidates.length,
    rejectedResources: data.resources.filter((resource) => resource.verificationStatus === 'rejected').length,
    needsReviewResources: data.resources.filter((resource) => resource.verificationStatus === 'unverified').length,
    acceptedResources: data.resources.filter((resource) => resource.verificationStatus !== 'rejected').length,
    acceptedLinks: data.nodeResourceLinks.filter((link) => isAccepted(link.reviewStatus)).length,
    needsReviewLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'needs_review').length,
    rejectedLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'rejected').length,
    candidateLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'candidate').length,
    candidates: data.resourceCandidates.length,
    localFilesIndexed: local.resources.length,
    localFilesAdmitted: data.resources.filter((resource) => resource.localFileHash && localHashes.has(resource.localFileHash)).length,
    resourcesMissingEditionVersion: standardLinks.length,
    standardsMissingContext: standardLinks.length,
    standardsTotal: validation.standardsTotal,
    standardsMissingEdition: validation.standardsMissingEdition,
    standardsMissingJurisdiction: validation.standardsMissingJurisdiction,
    standardsMissingScope: validation.standardsMissingScope,
    standardsContextComplete: validation.standardsContextComplete,
    standardsContextPartial: validation.standardsContextPartial,
    standardsContextNeedsReview: validation.standardsContextNeedsReview,
    standardsAcceptedMissingContext: validation.standardsAcceptedMissingContext,
    standardsPromotionBlocked: validation.standardsPromotionBlocked,
    standardsContextReviewable: validation.standardsContextReviewable,
    standardsContextWarnings: validation.standardsContextWarnings,
    duplicateWarnings: detectResourceDuplicates(data.resources).length,
    brokenLinkWarnings: validation.brokenLinkCount,
    validationWarnings: validation.warnings.length,
    validationErrors: validation.errors.length,
    validationBlockers: validation.blockers.length,
    authorityTierDistribution: countBy(data.resources.map((resource) => String(resource.authorityTier ?? 'unknown'))),
    sourceFamilyDistribution: countBy(data.resources.flatMap((resource) => resource.sourceFamilyIds?.length ? resource.sourceFamilyIds : ['unknown'])),
    reviewDecisions: readReviewDecisionLog(repoRoot).reviewDecisions.length,
  };
}

export function buildResourceReviewQueue(repoRoot: string, filters: ReviewFilters = {}) {
  const data = readResourceLayerData(repoRoot);
  const byId = new Map(data.resources.map((resource) => [resource.id, resource]));
  const links = data.nodeResourceLinks.map((link) => linkItem(link, byId.get(link.resourceId)));
  const candidates = data.resourceCandidates.map((candidate) => candidateItem(candidate, data));
  const localFiles = localIndex(repoRoot).resources.map((resource) => localFileItem(resource, data));
  const validation = validateResourceLayerData(data, { repoRoot, localIndexedHashes: indexedHashes(repoRoot) });
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    filters,
    needsReviewLinks: filterItems(links.filter((item) => item.reviewStatus === 'needs_review'), filters),
    rejectedLinks: filterItems(links.filter((item) => item.reviewStatus === 'rejected'), filters),
    acceptedLinks: filterItems(links.filter((item) => isAccepted(item.reviewStatus)), filters),
    candidateLinks: filterItems(links.filter((item) => item.reviewStatus === 'candidate'), filters),
    candidates: filterItems(candidates, filters),
    localFiles: filterItems(localFiles, filters),
    standardsMissingContext: filterItems(links.filter((item) => item.missingStandardContext), filters),
    validationWarnings: validation.warnings,
    validationErrors: validation.errors,
    validationBlockers: validation.blockers,
    reviewDecisions: readReviewDecisionLog(repoRoot).reviewDecisions,
    metrics: buildResourceReviewReport(repoRoot),
  };
}

export function buildResourceReviewCandidates(repoRoot: string, filters: ReviewFilters = {}) {
  const data = readResourceLayerData(repoRoot);
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    candidates: filterItems(data.resourceCandidates.map((candidate) => candidateItem(candidate, data)), filters),
  };
}

export function buildLocalFileReview(repoRoot: string, filters: ReviewFilters = {}) {
  const data = readResourceLayerData(repoRoot);
  const local = localIndex(repoRoot);
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    indexedResourceCount: local.resources.length,
    scannedDirectories: local.scannedDirectories || [],
    errors: local.errors || [],
    localFiles: filterItems(local.resources.map((resource) => localFileItem(resource, data)), filters),
  };
}

export function buildStandardsReview(repoRoot: string, filters: ReviewFilters = {}) {
  const data = readResourceLayerData(repoRoot);
  const byId = new Map(data.resources.map((resource) => [resource.id, resource]));
  const standards = data.nodeResourceLinks
    .map((link) => linkItem(link, byId.get(link.resourceId)))
    .filter((item) => isStandardLike(item.resource) && (item.missingStandardContext || !item.resource?.year || (!item.resource?.jurisdiction && !item.resource?.geographicScope)));
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
    standards: filterItems(standards, filters),
  };
}

export function decideNodeResourceLink(repoRoot: string, linkId: string, body: ReviewDecisionBody) {
  const decision = body.decision as LinkReviewDecision;
  if (!['accept', 'reject', 'needs_review', 'downgrade', 'reopen'].includes(decision)) throw new ResourceReviewError(`unsupported link decision: ${String(body.decision)}`);
  const reviewer = requireReviewer(body);
  const rationale = requireRationale(body);
  const data = readMutableData(repoRoot);
  const link = data.nodeResourceLinks.find((item) => item.id === linkId);
  if (!link) throw new ResourceReviewError(`NodeResourceLink not found: ${linkId}`, 404);
  const resource = data.resources.find((item) => item.id === link.resourceId);
  const previous = structuredClone(link);
  const previousResource = resource ? structuredClone(resource) : undefined;
  const previousStatus = link.reviewStatus;
  const timestamp = nowIso();

  link.reviewStatus = decision === 'accept' ? 'accepted' : decision === 'reject' ? 'rejected' : 'needs_review';
  link.reviewNotes = appendReviewNotes(link.reviewNotes, body) || rationale;
  link.updatedAt = timestamp;
  if (decision === 'accept') link.verifiedBy = 'human';
  if (body.authorityScore !== undefined) link.authorityScore = score(body.authorityScore, 'authorityScore', link.authorityScore);
  if (body.sectionRefs?.length) link.sectionRefs = body.sectionRefs;
  if (body.chapterRefs?.length) link.chapterRefs = body.chapterRefs;
  if (body.pageRefs?.length) link.pageRefs = body.pageRefs;
  if (resource) {
    if (body.edition || body.version) resource.edition = String(body.edition || body.version);
    if (body.authorityTier !== undefined) {
      if (![1, 2, 3, 4, 5].includes(body.authorityTier)) throw new ResourceReviewError('authorityTier must be 1..5');
      resource.authorityTier = body.authorityTier as Resource['authorityTier'];
    }
    if (body.sourceRights) resource.sourceRights = { ...(resource.sourceRights || {}), ...body.sourceRights };
    if (body.admissionProvenance) resource.admissionProvenance = { ...(resource.admissionProvenance || {}), ...body.admissionProvenance };
    resource.updatedAt = timestamp;
  }
  if (decision === 'accept' && standardContextMissing(resource, link)) {
    throw new ResourceReviewError('cannot accept standard/code-like link without edition/version plus page/chapter/section context or explicit reviewer justification', 400, [linkId]);
  }
  const validation = validateMutation(repoRoot, data);
  const response = { dryRun: Boolean(body.dryRun), link: linkItem(link, resource), previous, validation };
  if (body.dryRun) return response;
  const paths = resourceLayerFilePaths(repoRoot);
  const filesTouched = [paths.links, paths.reviewDecisions, ...(resource ? [paths.resources] : [])];
  const { result: reviewDecision, manifest } = withResourceLayerTransaction(repoRoot, 'resource_link_review_decision', filesTouched, () => {
    writeRegistry(repoRoot, data, { resources: Boolean(resource), links: true });
    return appendDecision(repoRoot, {
      target_type: 'node_resource_link',
      target_id: linkId,
      previous_status: previousStatus,
      new_status: link.reviewStatus,
      decision,
      reviewer,
      rationale,
      notes: body.notes,
      created_at: timestamp,
      metadata: {
        nodeId: link.nodeId,
        resourceId: link.resourceId,
        before: previous,
        after: link,
        beforeResource: previousResource,
        afterResource: resource ? structuredClone(resource) : undefined,
      },
    });
  });
  return { ...response, reviewDecision, transactionManifest: manifest };
}

function completeResource(candidate: ResourceCandidate, body: ReviewDecisionBody, timestamp: string): Resource {
  const fields = body.resourceFields || {};
  const sourceFamilyIds = fields.sourceFamilyIds || [];
  if (!sourceFamilyIds.length) throw new ResourceReviewError('candidate promotion requires sourceFamilyIds');
  if (!fields.sourceRights?.declaredUseBoundary && !body.sourceRights?.declaredUseBoundary) {
    throw new ResourceReviewError('candidate promotion requires sourceRights.declaredUseBoundary');
  }
  const provenance = fields.admissionProvenance || body.admissionProvenance;
  if (!provenance?.admittedBy || !provenance.admittedAt) throw new ResourceReviewError('candidate promotion requires admission provenance');
  if (!fields.url && !fields.canonicalUrl && !fields.localPath && !fields.localFileHash && !fields.doi && !fields.isbn13 && !fields.isbn10 && !candidate.rawUrl) {
    throw new ResourceReviewError('candidate promotion requires URL, local file reference, DOI, ISBN, or stable identifier');
  }
  const resourceType = requireString(fields.resourceType, 'resourceType') as Resource['resourceType'];
  if ((resourceType === 'standard' || resourceType === 'code') && !fields.edition) {
    throw new ResourceReviewError('standard/code candidate promotion requires edition/version context');
  }
  if ((resourceType === 'standard' || resourceType === 'code') && !fields.jurisdiction && !fields.geographicScope) {
    throw new ResourceReviewError('standard/code candidate promotion requires jurisdiction or geographicScope');
  }
  return {
    ...fields,
    id: requireString(fields.id || candidate.rawIdentifier, 'resource id'),
    title: requireString(fields.title || candidate.rawTitle, 'resource title'),
    resourceType,
    sourceAuthority: requireString(fields.sourceAuthority, 'sourceAuthority') as Resource['sourceAuthority'],
    sourceFamilyIds,
    url: fields.url || candidate.rawUrl,
    canonicalUrl: fields.canonicalUrl || fields.url || candidate.rawUrl,
    disciplineTags: fields.disciplineTags || [],
    taxonomyTags: fields.taxonomyTags || [],
    accessType: requireString(fields.accessType, 'accessType') as Resource['accessType'],
    sourceRights: fields.sourceRights || body.sourceRights,
    admissionProvenance: provenance,
    verificationStatus: (fields.verificationStatus || 'metadata_verified') as Resource['verificationStatus'],
    createdAt: fields.createdAt || timestamp,
    updatedAt: timestamp,
  } as Resource;
}

function completeLink(candidate: ResourceCandidate, resourceId: string, body: ReviewDecisionBody, timestamp: string): NodeResourceLink {
  const fields = body.linkFields || {};
  const targetNodeId = requireString(body.targetNodeId || candidate.nodeId, 'targetNodeId');
  const id = fields.id || `nrl-${targetNodeId}-${resourceId}`.replace(/[^a-zA-Z0-9_-]+/g, '-').toLowerCase();
  return {
    id,
    nodeId: targetNodeId,
    resourceId,
    relationship: requireString(fields.relationship, 'relationship') as NodeResourceLink['relationship'],
    relevanceScore: score(fields.relevanceScore, 'relevanceScore', 0.5),
    authorityScore: score(fields.authorityScore, 'authorityScore', 0.5),
    confidenceScore: score(fields.confidenceScore, 'confidenceScore', 0.5),
    rationale: requireString(fields.rationale || body.rationale, 'link rationale'),
    pageRefs: fields.pageRefs,
    chapterRefs: fields.chapterRefs,
    sectionRefs: fields.sectionRefs,
    matchedTerms: fields.matchedTerms,
    matchedAliases: fields.matchedAliases,
    verifiedBy: fields.verifiedBy || 'human',
    reviewStatus: (fields.reviewStatus || 'needs_review') as ReviewStatus,
    reviewNotes: appendReviewNotes(fields.reviewNotes, body),
    createdAt: fields.createdAt || timestamp,
    updatedAt: timestamp,
  };
}

function ensureNoDuplicateResource(data: ResourceLayerData, resource: Resource) {
  if (data.resources.some((item) => item.id === resource.id)) throw new ResourceReviewError(`duplicate resource id: ${resource.id}`);
  const duplicates = detectResourceDuplicates([...data.resources, resource]);
  if (duplicates.length) throw new ResourceReviewError('candidate promotion would create duplicate resources', 400, duplicates.map((group) => `${group.kind}:${group.key}`));
}

export function decideResourceCandidate(repoRoot: string, candidateId: string, body: ReviewDecisionBody) {
  const decision = body.decision as CandidateReviewDecision;
  if (!['accept_as_resource', 'link_to_node', 'reject_candidate', 'needs_more_context', 'mark_duplicate', 'hold'].includes(decision)) throw new ResourceReviewError(`unsupported candidate decision: ${String(body.decision)}`);
  const reviewer = requireReviewer(body);
  const rationale = requireRationale(body);
  const data = readMutableData(repoRoot);
  const candidate = data.resourceCandidates.find((item) => item.id === candidateId);
  if (!candidate) throw new ResourceReviewError(`ResourceCandidate not found: ${candidateId}`, 404);
  const previous = structuredClone(candidate);
  const previousStatus = candidate.reviewStatus;
  const timestamp = nowIso();
  let createdResource: Resource | undefined;
  let createdLink: NodeResourceLink | undefined;

  if (decision === 'reject_candidate') {
    candidate.reviewStatus = 'rejected';
    candidate.rejectionReason = rationale;
  } else if (decision === 'mark_duplicate') {
    const duplicateOfResourceId = requireString(body.duplicateOfResourceId, 'duplicateOfResourceId');
    if (!data.resources.some((resource) => resource.id === duplicateOfResourceId)) throw new ResourceReviewError(`duplicate resource not found: ${duplicateOfResourceId}`);
    candidate.reviewStatus = 'rejected';
    candidate.rejectionReason = rationale;
    candidate.duplicateOfResourceId = duplicateOfResourceId;
  } else if (decision === 'needs_more_context' || decision === 'hold') {
    candidate.reviewStatus = 'needs_review';
    if (decision === 'needs_more_context') candidate.rejectionReason = rationale;
  } else {
    createdResource = completeResource(candidate, body, timestamp);
    ensureNoDuplicateResource(data, createdResource);
    data.resources.push(createdResource);
    candidate.reviewStatus = 'accepted';
    if (decision === 'link_to_node') {
      createdLink = completeLink(candidate, createdResource.id, body, timestamp);
      if (data.nodeResourceLinks.some((link) => link.id === createdLink!.id)) throw new ResourceReviewError(`duplicate node-resource link id: ${createdLink.id}`);
      data.nodeResourceLinks.push(createdLink);
    }
  }
  candidate.reviewNotes = appendReviewNotes(candidate.reviewNotes, body) || rationale;
  candidate.reviewedAt = timestamp;
  candidate.updatedAt = timestamp;
  const validation = validateMutation(repoRoot, data);
  const response = { dryRun: Boolean(body.dryRun), candidate: candidateItem(candidate, data), createdResource, createdLink, previous, validation };
  if (body.dryRun) return response;
  const paths = resourceLayerFilePaths(repoRoot);
  const filesTouched = [paths.candidates, paths.reviewDecisions, ...(createdResource ? [paths.resources] : []), ...(createdLink ? [paths.links] : [])];
  const { result: reviewDecision, manifest } = withResourceLayerTransaction(repoRoot, 'resource_candidate_review_decision', filesTouched, () => {
    writeRegistry(repoRoot, data, { resources: Boolean(createdResource), links: Boolean(createdLink), candidates: true });
    return appendDecision(repoRoot, {
      target_type: 'candidate',
      target_id: candidateId,
      previous_status: previousStatus,
      new_status: candidate.reviewStatus,
      decision,
      reviewer,
      rationale,
      notes: body.notes,
      created_at: timestamp,
      metadata: { before: previous, after: candidate, createdResourceId: createdResource?.id, createdLinkId: createdLink?.id, duplicateOfResourceId: body.duplicateOfResourceId },
    });
  });
  return { ...response, reviewDecision, transactionManifest: manifest };
}

export function decideLocalFile(repoRoot: string, fileId: string, body: ReviewDecisionBody) {
  const decision = body.decision as LocalFileReviewDecision;
  if (!['admit_as_resource', 'link_to_node', 'reject_local_file', 'needs_review', 'ignore'].includes(decision)) throw new ResourceReviewError(`unsupported local-file decision: ${String(body.decision)}`);
  const reviewer = requireReviewer(body);
  const rationale = requireRationale(body);
  const data = readMutableData(repoRoot);
  const indexed = localIndex(repoRoot).resources.find((resource) => resource.id === fileId || resource.localFileHash === fileId);
  if (!indexed) throw new ResourceReviewError(`local indexed file not found: ${fileId}`, 404);
  const timestamp = nowIso();
  let createdResource = data.resources.find((resource) => resource.localFileHash && resource.localFileHash === indexed.localFileHash);
  const previouslyAdmitted = Boolean(createdResource);
  let createdLink: NodeResourceLink | undefined;

  if (decision === 'admit_as_resource' || decision === 'link_to_node') {
    if (!indexed.localPath || !existsSync(resolve(repoRoot, indexed.localPath))) {
      throw new ResourceReviewError('local file admission requires the indexed localPath to still exist on disk', 400, [indexed.localPath || indexed.id]);
    }
    if (!createdResource) {
      const fields = body.resourceFields || {};
      createdResource = {
        ...indexed,
        ...fields,
        id: requireString(fields.id || indexed.id, 'resource id'),
        title: requireString(fields.title || indexed.title, 'resource title'),
        sourceRights: fields.sourceRights || body.sourceRights || indexed.sourceRights,
        admissionProvenance: fields.admissionProvenance || body.admissionProvenance || {
          admittedBy: 'human',
          admittedAt: timestamp,
          evidenceRef: indexed.localPath,
          custodyChain: indexed.localPath ? [indexed.localPath] : [],
          reviewSummary: rationale,
        },
        verificationStatus: (fields.verificationStatus || indexed.verificationStatus || 'local_file_verified') as Resource['verificationStatus'],
        createdAt: fields.createdAt || timestamp,
        updatedAt: timestamp,
      } as Resource;
      if (!createdResource.localFileHash) throw new ResourceReviewError('local file admission requires localFileHash');
      ensureNoDuplicateResource(data, createdResource);
      data.resources.push(createdResource);
    }
    if (decision === 'link_to_node') {
      if (!body.targetNodeId) throw new ResourceReviewError('link_to_node requires targetNodeId; local files are never auto-linked');
      createdLink = completeLink({
        id: `local-candidate-${indexed.id}`,
        nodeId: body.targetNodeId,
        adapter: 'local_file_review',
        query: indexed.title,
        rawTitle: indexed.title,
        rawIdentifier: createdResource.id,
        preliminaryScore: 0.5,
        reviewStatus: 'needs_review',
        createdAt: timestamp,
      }, createdResource.id, body, timestamp);
      if (data.nodeResourceLinks.some((link) => link.id === createdLink!.id)) throw new ResourceReviewError(`duplicate node-resource link id: ${createdLink.id}`);
      createdLink.reviewNotes = [
        createdLink.reviewNotes,
        `Local file origin: ${indexed.localPath || indexed.id}`,
        indexed.localFileHash ? `Local file hash: ${indexed.localFileHash}` : '',
      ].filter(Boolean).join('\n');
      data.nodeResourceLinks.push(createdLink);
    }
  }
  const validation = validateMutation(repoRoot, data);
  const response = { dryRun: Boolean(body.dryRun), localFile: localFileItem(indexed, data), createdResource, createdLink, validation };
  if (body.dryRun) return response;
  const paths = resourceLayerFilePaths(repoRoot);
  const resourceCreatedOrUpdated = Boolean(createdResource && (decision === 'admit_as_resource' || decision === 'link_to_node'));
  const filesTouched = [paths.reviewDecisions, ...(resourceCreatedOrUpdated ? [paths.resources] : []), ...(createdLink ? [paths.links] : [])];
  const { result: reviewDecision, manifest } = withResourceLayerTransaction(repoRoot, 'resource_local_file_review_decision', filesTouched, () => {
    writeRegistry(repoRoot, data, { resources: resourceCreatedOrUpdated, links: Boolean(createdLink) });
    return appendDecision(repoRoot, {
      target_type: 'local_file',
      target_id: fileId,
      previous_status: previouslyAdmitted ? 'admitted' : 'indexed',
      new_status: decision === 'ignore' ? 'ignored' : decision === 'reject_local_file' ? 'rejected' : decision === 'needs_review' ? 'needs_review' : 'admitted',
      decision,
      reviewer,
      rationale,
      notes: body.notes,
      created_at: timestamp,
      metadata: { localPath: indexed.localPath, localFileHash: indexed.localFileHash, createdResourceId: createdResource?.id, createdLinkId: createdLink?.id },
    });
  });
  return { ...response, reviewDecision, transactionManifest: manifest };
}
