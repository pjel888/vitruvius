import { existsSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import type { LocalFileIndex, NodeResourceSummary, Resource, ResourceCandidate, ResourceCheck, ResourceLayerData, ReviewDecisionLog, SourceFamily } from './types';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './types';
import { rankNodeResources } from './ranking';
import { detectResourceDuplicates } from './deduplication';
import { validateResourceLayerData } from './validation';

const RESOURCE_LAYER_DIR = join('006_System-Manifests', 'resource-layer');
const REGISTRY_FILES = {
  resources: 'resources.json',
  links: 'node-resource-links.json',
  sourceFamilies: 'source-families.json',
  checks: 'resource-checks.json',
  candidates: 'resource-candidates.json',
  localFileIndex: 'local-file-index.json',
  reviewDecisions: 'review-decisions.json',
} as const;

type JsonRecord = Record<string, unknown>;

function readJsonObject(path: string): JsonRecord {
  const text = readFileSync(path, 'utf-8').replace(/^\uFEFF/, '');
  const value = JSON.parse(text);
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${path} must contain a JSON object`);
  return value as JsonRecord;
}

function readArray<T>(path: string, key: string): T[] {
  if (!existsSync(path)) return [];
  const payload = readJsonObject(path);
  const value = payload[key];
  if (!Array.isArray(value)) throw new Error(`${path}.${key} must be an array`);
  return value as T[];
}

function fileKey(path: string) {
  if (!existsSync(path)) return `${path}:missing`;
  const stat = statSync(path);
  return `${path}:${stat.size}:${stat.mtimeMs}`;
}

let cached: { key: string; data: ResourceLayerData } | null = null;

export function resourceLayerDirectory(repoRoot: string) {
  return resolve(repoRoot, RESOURCE_LAYER_DIR);
}

export function resourceLayerFilePaths(repoRoot: string) {
  const dir = resourceLayerDirectory(repoRoot);
  return {
    dir,
    resources: join(dir, REGISTRY_FILES.resources),
    links: join(dir, REGISTRY_FILES.links),
    sourceFamilies: join(dir, REGISTRY_FILES.sourceFamilies),
    checks: join(dir, REGISTRY_FILES.checks),
    candidates: join(dir, REGISTRY_FILES.candidates),
    localFileIndex: join(dir, REGISTRY_FILES.localFileIndex),
    reviewDecisions: join(dir, REGISTRY_FILES.reviewDecisions),
  };
}

export function readResourceLayerData(repoRoot: string): ResourceLayerData {
  const paths = resourceLayerFilePaths(repoRoot);
  const key = [paths.resources, paths.links, paths.sourceFamilies, paths.checks, paths.candidates].map(fileKey).join('|');
  if (cached?.key === key) return cached.data;
  const data: ResourceLayerData = {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    resources: readArray<Resource>(paths.resources, 'resources'),
    nodeResourceLinks: readArray(paths.links, 'nodeResourceLinks'),
    sourceFamilies: readArray<SourceFamily>(paths.sourceFamilies, 'sourceFamilies'),
    resourceChecks: readArray<ResourceCheck>(paths.checks, 'resourceChecks'),
    resourceCandidates: readArray<ResourceCandidate>(paths.candidates, 'resourceCandidates'),
  };
  cached = { key, data };
  return data;
}

export interface NodeResourceOptions {
  includeCandidates?: boolean;
  includeReviewer?: boolean;
  limit?: number;
}

export function getNodeResources(repoRoot: string, nodeId: string, options: NodeResourceOptions = {}): NodeResourceSummary[] {
  const data = readResourceLayerData(repoRoot);
  const links = data.nodeResourceLinks.filter((link) => link.nodeId === nodeId);
  return rankNodeResources(data.resources, links, options);
}

export function getResource(repoRoot: string, resourceId: string): Resource | null {
  const data = readResourceLayerData(repoRoot);
  return data.resources.find((resource) => resource.id === resourceId) || null;
}

export function readLocalFileIndex(repoRoot: string): LocalFileIndex {
  const path = resourceLayerFilePaths(repoRoot).localFileIndex;
  if (!existsSync(path)) {
    return { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, resources: [], indexedResourceCount: 0, errors: [] };
  }
  const payload = readJsonObject(path);
  const resources = Array.isArray(payload.resources) ? payload.resources as Resource[] : [];
  return {
    schemaVersion: String(payload.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION),
    generatedAt: typeof payload.generatedAt === 'string' ? payload.generatedAt : undefined,
    indexedResourceCount: typeof payload.indexedResourceCount === 'number' ? payload.indexedResourceCount : resources.length,
    scannedDirectories: Array.isArray(payload.scannedDirectories) ? payload.scannedDirectories.map(String) : [],
    errors: Array.isArray(payload.errors) ? payload.errors.map(String) : [],
    resources,
  };
}

export function readReviewDecisionLog(repoRoot: string): ReviewDecisionLog {
  const path = resourceLayerFilePaths(repoRoot).reviewDecisions;
  if (!existsSync(path)) {
    return { schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION, reviewDecisions: [] };
  }
  const payload = readJsonObject(path);
  return {
    schemaVersion: String(payload.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION),
    generatedAt: typeof payload.generatedAt === 'string' ? payload.generatedAt : undefined,
    reviewDecisions: Array.isArray(payload.reviewDecisions) ? payload.reviewDecisions as ReviewDecisionLog['reviewDecisions'] : [],
  };
}

function isAcceptedLinkStatus(status: string) {
  return status === 'accepted' || status === 'human_reviewed';
}

function isStandardLike(resource: Resource) {
  return resource.resourceType === 'standard' || resource.resourceType === 'code';
}

function linkHasSectionContext(link: { sectionRefs?: string[]; chapterRefs?: string[]; pageRefs?: string[] }) {
  return Boolean(link.sectionRefs?.length || link.chapterRefs?.length || link.pageRefs?.length);
}

export function resourceLayerMetrics(repoRoot: string, eligibleNodeIds: Set<string> = new Set()) {
  const data = readResourceLayerData(repoRoot);
  const acceptedLinks = data.nodeResourceLinks.filter((link) => isAcceptedLinkStatus(link.reviewStatus));
  const acceptedNodeIds = new Set(acceptedLinks.map((link) => link.nodeId));
  const resourcesWithAcceptedLinks = new Set(acceptedLinks.map((link) => link.resourceId));
  const localFileIndex = readLocalFileIndex(repoRoot);
  const localIndexedHashes = new Set(localFileIndex.resources.map((resource) => resource.localFileHash).filter(Boolean));
  const localAdmitted = data.resources.filter((resource) => resource.localFileHash && localIndexedHashes.has(resource.localFileHash));
  const resourceById = new Map(data.resources.map((resource) => [resource.id, resource]));
  const standardsMissingContext = data.nodeResourceLinks.filter((link) => {
    const resource = resourceById.get(link.resourceId);
    return resource
      && isStandardLike(resource)
      && (!resource.edition || !linkHasSectionContext(link))
      && link.reviewStatus !== 'rejected';
  });
  const validation = validateResourceLayerData(data, {
    repoRoot,
    localIndexedHashes,
  });
  const countBy = <T extends string>(items: T[]) => items.reduce<Record<string, number>>((acc, item) => {
    acc[item] = (acc[item] || 0) + 1;
    return acc;
  }, {});
  return {
    resourcesTotal: data.resources.length,
    resourcesNonRejected: data.resources.filter((resource) => resource.verificationStatus !== 'rejected').length,
    resourcesWithAcceptedLinks: resourcesWithAcceptedLinks.size,
    acceptedNodeResourceLinks: acceptedLinks.length,
    candidateResources: data.resourceCandidates.length,
    rejectedResources: data.resources.filter((resource) => resource.verificationStatus === 'rejected').length,
    needsReviewResources: data.resources.filter((resource) => resource.verificationStatus === 'unverified').length,
    totalResources: data.resources.length,
    resourcesByType: countBy(data.resources.map((resource) => resource.resourceType)),
    resourcesByAuthority: countBy(data.resources.map((resource) => resource.sourceAuthority)),
    resourcesByVerificationStatus: countBy(data.resources.map((resource) => resource.verificationStatus)),
    acceptedResources: data.resources.filter((resource) => resource.verificationStatus !== 'rejected').length,
    totalNodeResourceLinks: data.nodeResourceLinks.length,
    acceptedLinks: acceptedLinks.length,
    candidateLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'candidate').length,
    needsReviewLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'needs_review').length,
    rejectedLinks: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'rejected').length,
    eligibleNodesWithAcceptedResource: Array.from(acceptedNodeIds).filter((id) => eligibleNodeIds.size === 0 || eligibleNodeIds.has(id)).length,
    resourceCandidates: data.resourceCandidates.length,
    resourceChecks: data.resourceChecks.length,
    localFilesIndexed: localFileIndex.resources.length,
    localFilesAdmitted: localAdmitted.length,
    standardsMissingContext: standardsMissingContext.length,
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
    reviewDecisions: readReviewDecisionLog(repoRoot).reviewDecisions.length,
    authorityTierDistribution: countBy(data.resources.map((resource) => String(resource.authorityTier ?? 'unknown'))),
    sourceFamilyDistribution: countBy(data.resources.flatMap((resource) => resource.sourceFamilyIds?.length ? resource.sourceFamilyIds : ['unknown'])),
  };
}
