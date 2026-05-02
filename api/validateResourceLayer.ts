import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { readLocalFileIndex, readResourceLayerData } from './resourceLayer/registry';
import { validateResourceLayerData } from './resourceLayer/validation';

function latestShadowGraphPath(repoRoot: string) {
  const stagingRoot = resolve(repoRoot, '006_System-Manifests', 'aec-mepfs-backbone', 'shadow-staging');
  if (!existsSync(stagingRoot)) return null;
  const candidates = readdirSync(stagingRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => join(stagingRoot, entry.name, 'shadow-backbone-graph.json'))
    .filter((path) => existsSync(path))
    .sort();
  return candidates.at(-1) || null;
}

function loadNodeContext(repoRoot: string) {
  const graphPath = latestShadowGraphPath(repoRoot);
  const nodeIds = new Set<string>();
  const nodeTypesById = new Map<string, string>();
  if (!graphPath) return { nodeIds, nodeTypesById, graphPath: null };
  const payload = JSON.parse(readFileSync(graphPath, 'utf-8'));
  for (const node of payload.nodes || []) {
    if (!node?.id) continue;
    nodeIds.add(node.id);
    if (node.type || node.kind) nodeTypesById.set(node.id, String(node.type || node.kind));
  }
  return { nodeIds, nodeTypesById, graphPath };
}

const repoRoot = resolve(import.meta.dir, '..');
const data = readResourceLayerData(repoRoot);
const localFileIndex = readLocalFileIndex(repoRoot);
const { nodeIds, nodeTypesById, graphPath } = loadNodeContext(repoRoot);
const localIndexedHashes = new Set(localFileIndex.resources.map((resource) => resource.localFileHash).filter(Boolean) as string[]);
const result = validateResourceLayerData(data, {
  repoRoot,
  nodeIds: nodeIds.size > 0 ? nodeIds : undefined,
  nodeTypesById: nodeTypesById.size > 0 ? nodeTypesById : undefined,
  localIndexedHashes,
  fullLocalFileCheck: true,
});

const resourceById = new Map(data.resources.map((resource) => [resource.id, resource]));
const isAccepted = (status: string) => status === 'accepted' || status === 'human_reviewed';
const isStandardLike = (resource: any) => resource?.resourceType === 'standard' || resource?.resourceType === 'code';
const hasContext = (link: any) => Boolean(link.sectionRefs?.length || link.chapterRefs?.length || link.pageRefs?.length || link.fragmentRefs?.length);
const standardsMissingContext = data.nodeResourceLinks.filter((link) => {
  const resource = resourceById.get(link.resourceId);
  return resource && isStandardLike(resource) && link.reviewStatus !== 'rejected' && (!resource.edition || !hasContext(link));
});

const summary = {
  ok: result.ok,
  graphPath,
  resources: data.resources.length,
  nodeResourceLinks: data.nodeResourceLinks.length,
  sourceFamilies: data.sourceFamilies.length,
  resourceChecks: data.resourceChecks.length,
  resourceCandidates: data.resourceCandidates.length,
  accepted_count: data.nodeResourceLinks.filter((link) => isAccepted(link.reviewStatus)).length,
  needs_review_count: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'needs_review').length,
  rejected_count: data.nodeResourceLinks.filter((link) => link.reviewStatus === 'rejected').length,
  candidate_count: data.resourceCandidates.length,
  local_files_indexed: localFileIndex.resources.length,
  local_files_admitted: data.resources.filter((resource) => resource.localFileHash && localIndexedHashes.has(resource.localFileHash)).length,
  standards_missing_context: standardsMissingContext.length,
  standards_total: result.standardsTotal,
  standards_missing_edition: result.standardsMissingEdition,
  standards_missing_jurisdiction: result.standardsMissingJurisdiction,
  standards_missing_scope: result.standardsMissingScope,
  standards_context_complete: result.standardsContextComplete,
  standards_context_partial: result.standardsContextPartial,
  standards_context_needs_review: result.standardsContextNeedsReview,
  standards_accepted_missing_context: result.standardsAcceptedMissingContext,
  standards_promotion_blocked: result.standardsPromotionBlocked,
  standards_context_reviewable: result.standardsContextReviewable,
  standards_context_warnings: result.standardsContextWarnings,
  duplicateCount: result.duplicateCount,
  brokenLinkCount: result.brokenLinkCount,
  warnings: result.warnings,
  blockers: result.blockers,
  errors: result.errors,
};

console.log(JSON.stringify(summary, null, 2));
if (!result.ok) process.exit(1);
