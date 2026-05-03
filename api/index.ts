import { Hono } from 'hono';
import { serveStatic } from 'hono/bun';
import { cors } from 'hono/cors';
import neo4j from 'neo4j-driver';
import { createHash, timingSafeEqual } from 'node:crypto';
import { existsSync, readdirSync, statSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { basename, join, relative, resolve, sep } from 'node:path';
import { createScene, deleteScene, readScenes, sceneCreateSchema, updateScene } from './sceneStore';
import { getNodeResources, getResource, readResourceLayerData, resourceLayerMetrics } from './resourceLayer/registry';
import {
  ResourceReviewError,
  buildLocalFileReview,
  buildResourceReviewCandidates,
  buildResourceReviewQueue,
  buildResourceReviewReport,
  buildStandardsReview,
  decideStandardsContext,
  decideLocalFile,
  decideNodeResourceLink,
  decideResourceCandidate,
  getStandardsContextReviewDetail,
  previewStandardsContextDecision,
  type ReviewFilters,
} from './resourceLayer/reviewWorkflow';
import { buildSourceCustodyQueue } from './resourceLayer/sourceCustodyQueue';
import {
  buildExternalCandidatePreview,
  type ExternalMetadataCandidateInput,
} from './resourceLayer/externalMetadataCandidates';
import {
  getExternalCandidate,
  listExternalCandidates,
  loadExternalCandidateRegistry,
  persistExternalCandidate,
} from './resourceLayer/externalCandidateRegistry';
import {
  applyCorrection,
  applyReviewDecision,
  getCandidateDecisionHistory,
  previewCorrection,
  previewReviewDecision,
} from './resourceLayer/externalCandidateReview';
import { buildExternalCandidatePromotionPreview } from './resourceLayer/externalCandidatePromotionPreview';
import {
  buildGraphNeighborhood,
  classifyGraphEdge,
  normalizeGraphRelationship,
} from './graph/relationshipVisibility';
import {
  buildDuplicateCandidateGroups,
  applyPriorityOverrides,
  canonicalStewardshipPaths,
  createCanonicalBatch,
  findCanonicalBatch,
  canonicalNodeStatus,
  canonicalPreferredSearch,
  listCanonicalBatches,
  listCanonicalRemediationManifests,
  findCanonicalRemediationManifest,
  findDuplicateGroup,
  generateCanonicalP1DecisionPackets,
  getCanonicalP1PacketDetail,
  listCanonicalP1DecisionPackets,
  listCanonicalP1PacketsWithReviews,
  mergeAdmittedRelationshipsIntoEdges,
  previewCanonicalApproval,
  previewCanonicalBatchDecision,
  previewCanonicalP1PacketReview,
  previewCanonicalRollback,
  readCanonicalAdmittedRelationships,
  readCanonicalPriorityOverrides,
  readCanonicalAliases,
  readCanonicalApprovals,
  readCanonicalDecisions,
  readCanonicalRedirects,
  approveCanonicalDecision,
  rebaseCanonicalP1DecisionPackets,
  recordCanonicalDecision,
  recordCanonicalBatchDecision,
  recordCanonicalP1PacketReview,
  rejectCanonicalApproval,
  rollbackCanonicalDecision,
  setCanonicalGroupPriority,
  updateCanonicalRemediationStatus,
  validateCanonicalStewardship,
  type CanonicalPriorityBand,
  type DuplicateFilters,
} from './graph/canonicalStewardship';

// ---------------------------------------------------------------------------
// Neo4j connection
// ---------------------------------------------------------------------------
const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASS || 'password'
  )
);

async function runQuery<T = any>(query: string, params?: Record<string, any>): Promise<T[]> {
  const session = driver.session();
  try {
    const result = await session.run(query, params);
    return result.records.map(r => {
      const obj: any = {};
      r.keys.forEach(k => {
        const v = r.get(k);
        if (v && typeof v === 'object' && 'properties' in v) {
          const props = { ...v.properties };
          // Neo4j Relationship has `type` metadata (not a property); Node has `labels`
          if ('type' in v && !('labels' in v)) {
            props.type = v.type;
          }
          obj[k] = props;
        } else {
          obj[k] = v;
        }
      });
      return obj;
    });
  } finally {
    await session.close();
  }
}

const scenesFilePath = join(import.meta.dir, '.data', 'scenes.json');
const repoRoot = resolve(import.meta.dir, '..');

export const SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-summary/v1';
export const SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-taxonomy-preview/v1';
export const SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-node-preview/v1';
export const SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-search-preview/v1';
export const SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-source-preview/v1';
export const SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-placement-qa-preview/v1';
export const SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-evidence-preview/v1';
export const AEC_MEPFS_RESOLVER_RESPONSE_SCHEMA_VERSION = 'aec-mepfs-resolver-response/v1';
export const AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION = 'aec-mepfs-resolver-trace/v1';
export const AEC_MEPFS_RESOLVER_RUNTIME_FLAG = 'VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME';
export const AEC_MEPFS_RESOLVER_RUNTIME_DEFAULT = 'on';
export const AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID = 'aec-mepfs';
export const AEC_MEPFS_LEGACY_PERSPECTIVE_ID = 'default';
export const AEC_MEPFS_EXPLORER_GRAPH_SCHEMA_VERSION = 'aec-mepfs-explorer-graph/v1';
const AEC_MEPFS_RESOLVER_FIXTURE_FLAG = 'VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH';
const SHADOW_BACKBONE_CONSUMER_REPORT_SCHEMA_VERSION = 'aec-bb-shadow-staging-consumer-report/v1';
const SHADOW_BACKBONE_STAGING_SCHEMA_VERSION = 'aec-bb-shadow-staging/v1';
const SHADOW_BACKBONE_GRAPH_SCHEMA_VERSION = 'aec-bb-shadow-graph/v1';
const SHADOW_BACKBONE_PLACEMENT_QA_REPORT_SCHEMA_VERSION = 'aec-bb-placement-qa-report/v1';
const SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_SCHEMA_VERSION = 'aec-bb-shadow-evidence-manifest-report/v1';
const SHADOW_BACKBONE_REPORT_ROOT = resolve(
  repoRoot,
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'shadow-staging'
);
const SHADOW_BACKBONE_PLACEMENT_QA_REPORT_ROOT = resolve(
  repoRoot,
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'placement-qa'
);
const DEFAULT_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH = join(
  SHADOW_BACKBONE_PLACEMENT_QA_REPORT_ROOT,
  '20260426T015915Z',
  'placement-qa-report.json'
);
const SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_ROOT = resolve(
  repoRoot,
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'evidence-manifest'
);
const SHADOW_BACKBONE_CONSUMER_REPORT_FILENAME = 'shadow-staging-consumer-report.json';
const SHADOW_BACKBONE_STAGING_ARTIFACT_FILENAME = 'shadow-backbone-staging.json';
const SHADOW_BACKBONE_GRAPH_ARTIFACT_FILENAME = 'shadow-backbone-graph.json';
const SHADOW_BACKBONE_PLACEMENT_QA_REPORT_FILENAME = 'placement-qa-report.json';
const SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_FILENAME = 'shadow-evidence-manifest-report.json';
const DEFAULT_AEC_MEPFS_RESOLVER_FIXTURE_PATH = resolve(
  repoRoot,
  'scripts',
  'tests',
  'fixtures',
  'aec_mepfs_backbone',
  'valid_readiness_s2.json'
);
const REQUIRED_TRUE_SHADOW_BOUNDARIES = [
  'shadow_only',
  'file_backed_only',
] as const;
const REQUIRED_FALSE_SHADOW_BOUNDARIES = [
  'live_neo4j_writes',
  'graph_rebuild',
  'feature_flag_cutover',
  'api_explorer_cutover',
  'canonical_content_admission',
  'protected_content_ingest',
] as const;
const REQUIRED_TRUE_PLACEMENT_QA_BOUNDARIES = [
  'shadow_only',
  'file_backed_only',
] as const;
const REQUIRED_FALSE_PLACEMENT_QA_BOUNDARIES = [
  'live_neo4j_writes',
  'kg_rebuild',
  'feature_flag_cutover',
  'explorer_default_adoption',
  'protected_content_ingest',
  'canonical_content_admission',
] as const;
const REQUIRED_PLACEMENT_QA_COVERAGE_KEYS = [
  'l1_l2_human_review',
  'l3_l4_ld8_auto_accept',
  'legacy_label_alias',
] as const;
const REQUIRED_TRUE_EVIDENCE_INVARIANTS = [
  'all_artifacts_ok',
  'benchmark_shadow_file_backed_only',
  'boundary_audit_safety_green',
  'no_runtime_promotion',
  'route_inventory_preview_routes_complete',
  'runtime_thresholds_not_evaluated',
] as const;

class ShadowBackboneReportError extends Error {
  code = 'SHADOW_BACKBONE_REPORT_UNAVAILABLE';
}

class ShadowBackboneNodeNotFoundError extends Error {
  code = 'SHADOW_BACKBONE_NODE_NOT_FOUND';
}

class ShadowBackboneEdgeNotFoundError extends Error {
  code = 'SHADOW_BACKBONE_EDGE_NOT_FOUND';
}

class ShadowBackboneSearchQueryError extends Error {
  code = 'SHADOW_BACKBONE_SEARCH_QUERY_INVALID';
}

class ShadowBackboneSourceIdError extends Error {
  code = 'SHADOW_BACKBONE_SOURCE_ID_INVALID';
}

class ShadowBackboneSourceNotFoundError extends Error {
  code = 'SHADOW_BACKBONE_SOURCE_NOT_FOUND';
}

class AecMepfsResolverInputError extends Error {
  code: string;
  status: number;

  constructor(code: string, message: string, status = 400) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

class AecMepfsResolverArtifactError extends Error {
  code = 'AEC_MEPFS_RESOLVER_FIXTURE_UNAVAILABLE';
  status = 503;
}

class AecMepfsResolverTraceNotFoundError extends Error {
  code = 'AEC_MEPFS_RESOLVER_TRACE_NOT_FOUND';
  status = 404;
}

function isRecord(value: unknown): value is Record<string, any> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function requireRecord(value: unknown, path: string, errors: string[]) {
  if (!isRecord(value)) {
    errors.push(`${path}: expected object`);
    return {};
  }
  return value;
}

function requireArray(value: unknown, path: string, errors: string[]) {
  if (!Array.isArray(value)) {
    errors.push(`${path}: expected array`);
    return [];
  }
  return value;
}

function numericField(value: unknown, path: string, errors: string[]) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    errors.push(`${path}: expected number`);
    return 0;
  }
  return numeric;
}

function optionalNumericField(value: unknown, path: string, errors: string[]) {
  if (value === undefined) return 0;
  return numericField(value, path, errors);
}

function nullableNumericField(value: unknown, path: string, errors: string[]) {
  if (value === undefined) return null;
  return numericField(value, path, errors);
}

function nullableBooleanField(value: unknown, path: string, errors: string[]) {
  if (value === undefined) return null;
  if (typeof value !== 'boolean') {
    errors.push(`${path}: expected boolean`);
    return null;
  }
  return value;
}

function stringField(value: unknown) {
  return typeof value === 'string' ? value : '';
}

function requiredStringField(value: unknown, path: string, errors: string[]) {
  const text = stringField(value).trim();
  if (!text) errors.push(`${path}: expected non-empty string`);
  return text;
}

function stringArrayField(value: unknown, path: string, errors: string[]) {
  const values = requireArray(value, path, errors);
  const strings = values
    .map((item) => stringField(item).trim())
    .filter(Boolean);
  if (strings.length !== values.length) {
    errors.push(`${path}: expected string array`);
  }
  return strings;
}

function optionalStringArrayField(value: unknown, path: string, errors: string[]) {
  if (value === undefined) return [];
  return stringArrayField(value, path, errors);
}

const SHADOW_BACKBONE_EDGE_METADATA_FIELDS = [
  'relationType',
  'relationCategory',
  'relationNature',
  'direction',
  'weight',
  'confidenceScore',
  'discipline',
  'lifecyclePhase',
  'sourceFamilyIds',
  'rationale',
  'provenanceNote',
  'generationMethod',
  'reviewStatus',
  'semanticOverlayCategory',
  'applicabilityBasis',
  'jurisdictionContext',
  'designBasisStatus',
] as const;

function optionalFiniteNumericField(value: unknown, path: string, errors: string[]) {
  if (value === undefined || value === null || value === '') return undefined;
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    errors.push(`${path}: expected number`);
    return undefined;
  }
  return numeric;
}

function addOptionalStringMetadata(
  target: Record<string, any>,
  key: string,
  value: unknown,
) {
  const text = stringField(value).trim();
  if (text) target[key] = text;
}

function addOptionalArrayMetadata(
  target: Record<string, any>,
  key: string,
  value: unknown,
  path: string,
  errors: string[],
) {
  const values = optionalStringArrayField(value, path, errors);
  if (values.length) target[key] = values;
}

function shadowBackboneEdgeMetadataFromRow(
  row: Record<string, any>,
  index: number,
  errors: string[],
) {
  const metadata: Record<string, any> = {};
  addOptionalStringMetadata(metadata, 'relationType', row.relation_type);
  addOptionalStringMetadata(metadata, 'relationCategory', row.relation_category);
  addOptionalArrayMetadata(metadata, 'relationNature', row.relation_nature, `shadow_graph.edges[${index}].relation_nature`, errors);
  addOptionalStringMetadata(metadata, 'direction', row.direction);

  const weight = optionalFiniteNumericField(row.weight, `shadow_graph.edges[${index}].weight`, errors);
  if (weight !== undefined) metadata.weight = weight;
  const confidenceScore = optionalFiniteNumericField(
    row.confidence_score,
    `shadow_graph.edges[${index}].confidence_score`,
    errors
  );
  if (confidenceScore !== undefined) metadata.confidenceScore = confidenceScore;

  addOptionalArrayMetadata(metadata, 'discipline', row.discipline, `shadow_graph.edges[${index}].discipline`, errors);
  addOptionalArrayMetadata(metadata, 'lifecyclePhase', row.lifecycle_phase, `shadow_graph.edges[${index}].lifecycle_phase`, errors);
  addOptionalArrayMetadata(metadata, 'sourceFamilyIds', row.source_family_ids, `shadow_graph.edges[${index}].source_family_ids`, errors);
  addOptionalStringMetadata(metadata, 'rationale', row.rationale);
  addOptionalStringMetadata(metadata, 'provenanceNote', row.provenance_note);
  addOptionalStringMetadata(metadata, 'generationMethod', row.generation_method);
  addOptionalStringMetadata(metadata, 'reviewStatus', row.review_status);
  addOptionalStringMetadata(metadata, 'semanticOverlayCategory', row.semantic_overlay_category);
  addOptionalStringMetadata(metadata, 'applicabilityBasis', row.applicability_basis);
  addOptionalStringMetadata(metadata, 'jurisdictionContext', row.jurisdiction_context);
  addOptionalStringMetadata(metadata, 'designBasisStatus', row.design_basis_status);
  return metadata;
}

function shadowBackboneEdgeMetadataFromPreview(
  edge: Record<string, any>,
  options: { directionKey?: 'direction' | 'edgeDirection' } = {},
) {
  const directionKey = options.directionKey || 'direction';
  const metadata: Record<string, any> = {};
  for (const field of SHADOW_BACKBONE_EDGE_METADATA_FIELDS) {
    const value = field === 'direction' && directionKey === 'edgeDirection' && edge.edgeDirection !== undefined
      ? edge.edgeDirection
      : edge[field];
    if (value === undefined || value === null) continue;
    const outputField = field === 'direction' ? directionKey : field;
    if (Array.isArray(value)) {
      if (value.length) metadata[outputField] = [...value];
      continue;
    }
    if (typeof value === 'string') {
      const text = value.trim();
      if (text) metadata[outputField] = text;
      continue;
    }
    if (typeof value === 'number') {
      if (Number.isFinite(value)) metadata[outputField] = value;
      continue;
    }
    metadata[outputField] = value;
  }
  return metadata;
}

function confidenceFromEdgeMetadata(edge: Record<string, any>) {
  return typeof edge.confidenceScore === 'number' && Number.isFinite(edge.confidenceScore)
    ? edge.confidenceScore
    : 1;
}

function edgeReasoningFromMetadata(edge: Record<string, any>, fallback: string) {
  return stringField(edge.rationale).trim() || fallback;
}

function groupCounts(values: string[]) {
  const counts = new Map<string, number>();
  values.forEach((value) => {
    const key = value.trim();
    if (!key) return;
    counts.set(key, (counts.get(key) ?? 0) + 1);
  });
  return [...counts.entries()]
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => a.value.localeCompare(b.value));
}

function validateShadowBoundaries(boundaries: Record<string, any>, errors: string[]) {
  for (const key of REQUIRED_TRUE_SHADOW_BOUNDARIES) {
    if (boundaries[key] !== true) errors.push(`boundaries.${key}: expected true`);
  }
  for (const key of REQUIRED_FALSE_SHADOW_BOUNDARIES) {
    if (boundaries[key] !== false) errors.push(`boundaries.${key}: expected false`);
  }
}

function validatePlacementQaBoundaries(boundaries: Record<string, any>, errors: string[]) {
  for (const key of REQUIRED_TRUE_PLACEMENT_QA_BOUNDARIES) {
    if (boundaries[key] !== true) errors.push(`safety_boundaries.${key}: expected true`);
  }
  for (const key of REQUIRED_FALSE_PLACEMENT_QA_BOUNDARIES) {
    if (boundaries[key] !== false) errors.push(`safety_boundaries.${key}: expected false`);
  }
}

function repoRelativePath(path: string) {
  const relativePath = relative(repoRoot, path);
  return relativePath && relativePath !== '..' && !relativePath.startsWith(`..${sep}`)
    ? relativePath
    : path;
}

function resolveShadowPathInsideRoot(options: {
  value?: string | null;
  defaultPath?: string;
  root: string;
  expectedFilename: string;
  rootError: string;
  filenameError: string;
}) {
  const candidate = options.value
    ? resolve(repoRoot, options.value)
    : options.defaultPath;
  if (!candidate) {
    throw new ShadowBackboneReportError(options.filenameError);
  }
  const resolved = resolve(candidate);
  const insideReportRoot = resolved === options.root
    || resolved.startsWith(`${options.root}${sep}`);
  if (!insideReportRoot) {
    throw new ShadowBackboneReportError(options.rootError);
  }
  if (basename(resolved) !== options.expectedFilename) {
    throw new ShadowBackboneReportError(options.filenameError);
  }
  return resolved;
}

function resolveLatestShadowReportPath(root: string, filename: string, label: string) {
  let runIds: string[];
  try {
    runIds = readdirSync(root, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .filter((runId) => /^\d{8}T\d{6}Z$/.test(runId))
      .sort((a, b) => b.localeCompare(a));
  } catch {
    throw new ShadowBackboneReportError(`${label} report directory is unavailable`);
  }
  if (runIds.length === 0) {
    throw new ShadowBackboneReportError(`${label} report is unavailable`);
  }
  const latest = join(root, runIds[0], filename);
  if (!existsSync(latest)) {
    throw new ShadowBackboneReportError(`${label} report is unavailable for latest run ${runIds[0]}`);
  }
  return latest;
}

async function readShadowJsonObject(path: string, label: string) {
  const text = await readFile(path, 'utf-8');
  let payload: unknown;
  try {
    payload = JSON.parse(text);
  } catch {
    throw new ShadowBackboneReportError(
      `Invalid JSON in ${label} at ${repoRelativePath(path)}`
    );
  }
  if (!isRecord(payload)) {
    throw new ShadowBackboneReportError(`${label} must be a JSON object`);
  }
  return payload;
}

export function resolveShadowBackboneReportPath() {
  const configuredPath = process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
  return resolveShadowPathInsideRoot({
    value: configuredPath,
    defaultPath: configuredPath ? undefined : resolveLatestShadowReportPath(
      SHADOW_BACKBONE_REPORT_ROOT,
      SHADOW_BACKBONE_CONSUMER_REPORT_FILENAME,
      'Shadow backbone consumer'
    ),
    root: SHADOW_BACKBONE_REPORT_ROOT,
    expectedFilename: SHADOW_BACKBONE_CONSUMER_REPORT_FILENAME,
    rootError: 'Shadow backbone report path must stay inside the shadow staging report directory',
    filenameError: `Shadow backbone report filename must be ${SHADOW_BACKBONE_CONSUMER_REPORT_FILENAME}`,
  });
}

export function resolveShadowBackbonePlacementQaReportPath() {
  return resolveShadowPathInsideRoot({
    value: process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH,
    defaultPath: DEFAULT_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH,
    root: SHADOW_BACKBONE_PLACEMENT_QA_REPORT_ROOT,
    expectedFilename: SHADOW_BACKBONE_PLACEMENT_QA_REPORT_FILENAME,
    rootError: 'Shadow backbone placement QA report path must stay inside the placement QA report directory',
    filenameError: `Shadow backbone placement QA report filename must be ${SHADOW_BACKBONE_PLACEMENT_QA_REPORT_FILENAME}`,
  });
}

export function resolveShadowBackboneEvidenceManifestPath() {
  const configuredPath = process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH;
  return resolveShadowPathInsideRoot({
    value: configuredPath,
    defaultPath: configuredPath ? undefined : resolveLatestShadowReportPath(
      SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_ROOT,
      SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_FILENAME,
      'Shadow backbone evidence manifest'
    ),
    root: SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_ROOT,
    expectedFilename: SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_FILENAME,
    rootError: 'Shadow backbone evidence manifest path must stay inside the evidence manifest report directory',
    filenameError: `Shadow backbone evidence manifest filename must be ${SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_FILENAME}`,
  });
}

async function readShadowBackboneConsumerReport() {
  const reportPath = resolveShadowBackboneReportPath();
  try {
    return await readShadowJsonObject(reportPath, 'shadow backbone consumer report');
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone consumer report: ${error.message}`);
  }
}

async function readShadowBackbonePlacementQaReport() {
  const reportPath = resolveShadowBackbonePlacementQaReportPath();
  try {
    return await readShadowJsonObject(reportPath, 'shadow backbone placement QA report');
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone placement QA report: ${error.message}`);
  }
}

async function readShadowBackboneEvidenceManifestReport() {
  const reportPath = resolveShadowBackboneEvidenceManifestPath();
  try {
    return await readShadowJsonObject(reportPath, 'shadow backbone evidence manifest report');
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone evidence manifest report: ${error.message}`);
  }
}

export function resolveShadowBackboneArtifactPath(report: Record<string, any>) {
  const artifactPath = stringField(report.artifact_path);
  if (!artifactPath) {
    throw new ShadowBackboneReportError('Shadow backbone consumer report is missing artifact_path');
  }
  return resolveShadowPathInsideRoot({
    value: artifactPath,
    root: SHADOW_BACKBONE_REPORT_ROOT,
    expectedFilename: SHADOW_BACKBONE_STAGING_ARTIFACT_FILENAME,
    rootError: 'Shadow backbone artifact path must stay inside the shadow staging report directory',
    filenameError: `Shadow backbone artifact filename must be ${SHADOW_BACKBONE_STAGING_ARTIFACT_FILENAME}`,
  });
}

async function readShadowBackboneStagingArtifact(report: Record<string, any>) {
  const artifactPath = resolveShadowBackboneArtifactPath(report);
  try {
    return await readShadowJsonObject(artifactPath, 'shadow backbone staging artifact');
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone staging artifact: ${error.message}`);
  }
}

export function resolveShadowBackboneGraphPath(report: Record<string, any>) {
  const graphPath = stringField(report.shadow_graph_path);
  if (!graphPath) return null;
  return resolveShadowPathInsideRoot({
    value: graphPath,
    root: SHADOW_BACKBONE_REPORT_ROOT,
    expectedFilename: SHADOW_BACKBONE_GRAPH_ARTIFACT_FILENAME,
    rootError: 'Shadow backbone graph path must stay inside the shadow staging report directory',
    filenameError: `Shadow backbone graph filename must be ${SHADOW_BACKBONE_GRAPH_ARTIFACT_FILENAME}`,
  });
}

async function readShadowBackboneGraphArtifact(report: Record<string, any>) {
  const graphPath = resolveShadowBackboneGraphPath(report);
  if (!graphPath) return null;
  try {
    return await readShadowJsonObject(graphPath, 'shadow backbone graph artifact');
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone graph artifact: ${error.message}`);
  }
}

export function buildShadowBackboneSummary(report: Record<string, any>) {
  const errors: string[] = [];
  if (report.schema_version !== SHADOW_BACKBONE_CONSUMER_REPORT_SCHEMA_VERSION) {
    errors.push(
      `schema_version: expected ${SHADOW_BACKBONE_CONSUMER_REPORT_SCHEMA_VERSION}`
    );
  }
  if (report.ok !== true) {
    errors.push('shadow consumer report is not passing');
  }

  const counts = requireRecord(report.counts, 'counts', errors);
  const boundaries = requireRecord(report.boundaries, 'boundaries', errors);
  const boundaryCoverage = requireRecord(report.boundary_coverage, 'boundary_coverage', errors);
  const noIngestCoverage = requireRecord(
    report.no_ingest_boundary_coverage,
    'no_ingest_boundary_coverage',
    errors
  );

  validateShadowBoundaries(boundaries, errors);
  if (boundaryCoverage.safe_for_read_only_consumer !== true) {
    errors.push('boundary_coverage.safe_for_read_only_consumer: expected true');
  }
  if (Number(noIngestCoverage.content_ingest_source_count) !== 0) {
    errors.push('no_ingest_boundary_coverage.content_ingest_source_count: expected 0');
  }
  if (Number(noIngestCoverage.missing_explicit_block_count) !== 0) {
    errors.push('no_ingest_boundary_coverage.missing_explicit_block_count: expected 0');
  }

  const predicateRegistryCount = numericField(
    counts.predicate_registry,
    'counts.predicate_registry',
    errors
  );
  const sourceRightsRegistryCount = numericField(
    counts.source_rights_registry,
    'counts.source_rights_registry',
    errors
  );
  const backboneNodeCount = optionalNumericField(
    counts.backbone_nodes,
    'counts.backbone_nodes',
    errors
  );
  const sourcesTotal = numericField(
    noIngestCoverage.sources_total,
    'no_ingest_boundary_coverage.sources_total',
    errors
  );
  const explicitNoIngestSourceCount = numericField(
    noIngestCoverage.explicit_no_ingest_source_count,
    'no_ingest_boundary_coverage.explicit_no_ingest_source_count',
    errors
  );
  const missingExplicitBlockCount = numericField(
    noIngestCoverage.missing_explicit_block_count,
    'no_ingest_boundary_coverage.missing_explicit_block_count',
    errors
  );
  const contentIngestSourceCount = numericField(
    noIngestCoverage.content_ingest_source_count,
    'no_ingest_boundary_coverage.content_ingest_source_count',
    errors
  );

  if (errors.length) {
    throw new ShadowBackboneReportError(
      `Shadow backbone consumer report failed validation: ${errors.join('; ')}`
    );
  }

  const liveMutationBoundariesClear = REQUIRED_FALSE_SHADOW_BOUNDARIES.every(
    (key) => boundaries[key] === false
  );

  return {
    schemaVersion: SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION,
    source: 'file-backed-shadow-staging-consumer-report',
    status: 'shadow_ready',
    reportOk: true,
    runId: stringField(report.run_id),
    counts: {
      predicateRegistry: predicateRegistryCount,
      sourceRightsRegistry: sourceRightsRegistryCount,
      backboneNodes: backboneNodeCount,
    },
    boundaries: {
      shadowOnly: boundaries.shadow_only === true,
      fileBackedOnly: boundaries.file_backed_only === true,
      liveNeo4jWrites: boundaries.live_neo4j_writes === true,
      graphRebuild: boundaries.graph_rebuild === true,
      featureFlagCutover: boundaries.feature_flag_cutover === true,
      apiExplorerCutover: boundaries.api_explorer_cutover === true,
      canonicalContentAdmission: boundaries.canonical_content_admission === true,
      protectedContentIngest: boundaries.protected_content_ingest === true,
      liveMutationBoundariesClear,
      safeForReadOnlyConsumer: boundaryCoverage.safe_for_read_only_consumer === true,
    },
    noIngestBoundaryCoverage: {
      sourcesTotal,
      explicitNoIngestSourceCount,
      missingExplicitBlockCount,
      contentIngestSourceCount,
    },
    artifactPaths: {
      artifact: stringField(report.artifact_path),
      shadowGraph: stringField(report.shadow_graph_path),
      producerReport: stringField(report.producer_report_path),
      consumerReport: stringField(report.report_path),
    },
  };
}

export function buildShadowBackboneTaxonomyPreview(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null = null
) {
  const summary = buildShadowBackboneSummary(report);
  const errors: string[] = [];

  if (artifact.schema_version !== SHADOW_BACKBONE_STAGING_SCHEMA_VERSION) {
    errors.push(`schema_version: expected ${SHADOW_BACKBONE_STAGING_SCHEMA_VERSION}`);
  }
  if (artifact.status !== 'shadow_staged') {
    errors.push('status: expected shadow_staged');
  }
  if (stringField(artifact.run_id) !== summary.runId) {
    errors.push('run_id: expected to match consumer report run_id');
  }

  const counts = requireRecord(artifact.counts, 'counts', errors);
  const boundaries = requireRecord(artifact.boundaries, 'boundaries', errors);
  const predicateValues = requireArray(artifact.predicate_registry, 'predicate_registry', errors);
  const sourceValues = requireArray(artifact.source_rights_registry, 'source_rights_registry', errors);
  const backboneNodeValues = 'backbone_nodes' in artifact
    ? requireArray(artifact.backbone_nodes, 'backbone_nodes', errors)
    : [];
  validateShadowBoundaries(boundaries, errors);

  const predicateRegistryCount = numericField(
    counts.predicate_registry,
    'counts.predicate_registry',
    errors
  );
  const sourceRightsRegistryCount = numericField(
    counts.source_rights_registry,
    'counts.source_rights_registry',
    errors
  );
  const backboneNodeCount = 'backbone_nodes' in counts
    ? numericField(counts.backbone_nodes, 'counts.backbone_nodes', errors)
    : 0;
  if (predicateRegistryCount !== predicateValues.length) {
    errors.push('counts.predicate_registry: expected to match predicate_registry length');
  }
  if (sourceRightsRegistryCount !== sourceValues.length) {
    errors.push('counts.source_rights_registry: expected to match source_rights_registry length');
  }
  if (backboneNodeValues.length > 0 && !('backbone_nodes' in counts)) {
    errors.push('counts.backbone_nodes: required when backbone_nodes are present');
  }
  if (backboneNodeCount !== backboneNodeValues.length) {
    errors.push('counts.backbone_nodes: expected to match backbone_nodes length');
  }

  const predicateRows = predicateValues.map((value, index) => (
    requireRecord(value, `predicate_registry[${index}]`, errors)
  ));
  const sourceRows = sourceValues.map((value, index) => (
    requireRecord(value, `source_rights_registry[${index}]`, errors)
  ));
  const backboneNodeRows = backboneNodeValues.map((value, index) => (
    requireRecord(value, `backbone_nodes[${index}]`, errors)
  ));
  const shadowGraphRecord = shadowGraphArtifact;

  const predicates = predicateRows.map((row, index) => ({
    predicate: requiredStringField(row.predicate, `predicate_registry[${index}].predicate`, errors),
    category: requiredStringField(row.category, `predicate_registry[${index}].category`, errors),
    direction: stringField(row.direction),
    domainClasses: stringArrayField(row.domain_classes, `predicate_registry[${index}].domain_classes`, errors),
    rangeClasses: stringArrayField(row.range_classes, `predicate_registry[${index}].range_classes`, errors),
    allowedStrengthClasses: stringArrayField(
      row.allowed_strength_classes,
      `predicate_registry[${index}].allowed_strength_classes`,
      errors
    ),
    evidenceRequiredFields: stringArrayField(
      row.evidence_required_fields,
      `predicate_registry[${index}].evidence_required_fields`,
      errors
    ),
    owner: stringField(row.owner),
  }));

  const sourceFamilies = sourceRows.map((row, index) => ({
    sourceId: requiredStringField(row.source_id, `source_rights_registry[${index}].source_id`, errors),
    sourceFamily: requiredStringField(row.source_family, `source_rights_registry[${index}].source_family`, errors),
    publisherAuthority: stringField(row.publisher_authority),
    sourceRightsClass: requiredStringField(
      row.source_rights_class,
      `source_rights_registry[${index}].source_rights_class`,
      errors
    ),
    clearanceState: requiredStringField(
      row.clearance_state,
      `source_rights_registry[${index}].clearance_state`,
      errors
    ),
    declaredUseBoundary: stringField(row.declared_use_boundary),
    currentnessCheckDate: stringField(row.currentness_check_date),
    stewardOwner: stringField(row.steward_owner),
    updateCadence: stringField(row.update_cadence),
  }));

  const backboneNodes = backboneNodeRows.map((row, index) => ({
    id: requiredStringField(row.id, `backbone_nodes[${index}].id`, errors),
    canonicalId: requiredStringField(row.canonical_id, `backbone_nodes[${index}].canonical_id`, errors),
    label: requiredStringField(row.label, `backbone_nodes[${index}].label`, errors),
    prefLabel: requiredStringField(row.pref_label, `backbone_nodes[${index}].pref_label`, errors),
    pathCode: requiredStringField(row.path_code, `backbone_nodes[${index}].path_code`, errors),
    level: numericField(row.level, `backbone_nodes[${index}].level`, errors),
    parentPathCode: stringField(row.parent_path_code),
    reviewStatus: stringField(row.review_status),
    steward: stringField(row.steward),
    releaseVersion: stringField(row.release_version),
  }));
  const shadowGraphNodeValues = shadowGraphRecord
    ? requireArray(shadowGraphRecord.nodes, 'shadow_graph.nodes', errors)
    : [];
  const shadowGraphEdgeValues = shadowGraphRecord
    ? requireArray(shadowGraphRecord.edges, 'shadow_graph.edges', errors)
    : [];
  const shadowGraphCounts = shadowGraphRecord
    ? requireRecord(shadowGraphRecord.counts, 'shadow_graph.counts', errors)
    : {};
  if (shadowGraphRecord && shadowGraphRecord.schema_version !== SHADOW_BACKBONE_GRAPH_SCHEMA_VERSION) {
    errors.push(`shadow_graph.schema_version: expected ${SHADOW_BACKBONE_GRAPH_SCHEMA_VERSION}`);
  }
  if (shadowGraphRecord && stringField(shadowGraphRecord.run_id) !== summary.runId) {
    errors.push('shadow_graph.run_id: expected to match consumer report run_id');
  }
  if (shadowGraphRecord && shadowGraphRecord.status !== 'shadow_graph_staged') {
    errors.push('shadow_graph.status: expected shadow_graph_staged');
  }
  if (
    shadowGraphRecord
    && stringField(shadowGraphRecord.source_artifact_path) !== summary.artifactPaths.artifact
  ) {
    errors.push('shadow_graph.source_artifact_path: expected to match consumer report artifact_path');
  }
  const shadowGraphNodes = shadowGraphNodeValues.map((value, index) => {
    const row = requireRecord(value, `shadow_graph.nodes[${index}]`, errors);
    return {
      id: requiredStringField(row.id, `shadow_graph.nodes[${index}].id`, errors),
      label: requiredStringField(row.label, `shadow_graph.nodes[${index}].label`, errors),
      pathCode: requiredStringField(row.path_code, `shadow_graph.nodes[${index}].path_code`, errors),
      level: numericField(row.level, `shadow_graph.nodes[${index}].level`, errors),
      parentPathCode: stringField(row.parent_path_code),
    };
  });
  const shadowGraphNodeIds = new Set(shadowGraphNodes.map((node) => node.id));
  const shadowGraphEdges = shadowGraphEdgeValues.map((value, index) => {
    const row = requireRecord(value, `shadow_graph.edges[${index}]`, errors);
    const fromId = requiredStringField(row.from_id, `shadow_graph.edges[${index}].from_id`, errors);
    const toId = requiredStringField(row.to_id, `shadow_graph.edges[${index}].to_id`, errors);
    if (fromId && !shadowGraphNodeIds.has(fromId)) {
      errors.push(`shadow_graph.edges[${index}].from_id: unresolved node`);
    }
    if (toId && !shadowGraphNodeIds.has(toId)) {
      errors.push(`shadow_graph.edges[${index}].to_id: unresolved node`);
    }
    return {
      id: requiredStringField(row.id, `shadow_graph.edges[${index}].id`, errors),
      fromId,
      toId,
      predicate: requiredStringField(row.predicate, `shadow_graph.edges[${index}].predicate`, errors),
      fromPathCode: stringField(row.from_path_code),
      toPathCode: stringField(row.to_path_code),
      ...shadowBackboneEdgeMetadataFromRow(row, index, errors),
    };
  });
  const shadowGraph = {
    available: shadowGraphRecord !== null,
    counts: {
      nodes: shadowGraphRecord ? numericField(shadowGraphCounts.nodes, 'shadow_graph.counts.nodes', errors) : 0,
      edges: shadowGraphRecord ? numericField(shadowGraphCounts.edges, 'shadow_graph.counts.edges', errors) : 0,
      roots: shadowGraphRecord ? numericField(shadowGraphCounts.roots, 'shadow_graph.counts.roots', errors) : 0,
      maxDepth: shadowGraphRecord ? numericField(shadowGraphCounts.max_depth, 'shadow_graph.counts.max_depth', errors) : 0,
    },
    nodes: shadowGraphNodes,
    edges: shadowGraphEdges,
  };
  if (shadowGraph.available) {
    if (shadowGraph.counts.nodes !== shadowGraph.nodes.length) {
      errors.push('shadow_graph.counts.nodes: expected to match shadow_graph.nodes length');
    }
    if (shadowGraph.counts.edges !== shadowGraph.edges.length) {
      errors.push('shadow_graph.counts.edges: expected to match shadow_graph.edges length');
    }
    const reportShadowGraphCounts = requireRecord(
      report.shadow_graph_counts,
      'shadow_graph_counts',
      errors
    );
    const countPairs = [
      ['nodes', shadowGraph.counts.nodes],
      ['edges', shadowGraph.counts.edges],
      ['roots', shadowGraph.counts.roots],
      ['max_depth', shadowGraph.counts.maxDepth],
    ] as const;
    for (const [key, actual] of countPairs) {
      if (numericField(reportShadowGraphCounts[key], `shadow_graph_counts.${key}`, errors) !== actual) {
        errors.push(`shadow_graph_counts.${key}: expected to match shadow_graph.counts`);
      }
    }
  }

  if (errors.length) {
    throw new ShadowBackboneReportError(
      `Shadow backbone staging artifact failed validation: ${errors.join('; ')}`
    );
  }

  return {
    schemaVersion: SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-shadow-staging-artifact',
    status: 'shadow_ready',
    reportOk: true,
    runId: summary.runId,
    counts: summary.counts,
    boundaries: summary.boundaries,
    noIngestBoundaryCoverage: summary.noIngestBoundaryCoverage,
    readiness: {
      registryMetadataAvailable: true,
      canonicalTaxonomyTreeAvailable: backboneNodes.length > 0,
      backboneNodesAvailable: backboneNodes.length > 0,
      shadowGraphAvailable: shadowGraph.available,
      previewCompleteness: shadowGraph.available
        ? 'registry_metadata_admitted_nodes_and_shadow_graph'
        : backboneNodes.length > 0
        ? 'registry_metadata_and_admitted_backbone_nodes'
        : 'registry_metadata_only',
      limitation: shadowGraph.available
        ? 'Shadow graph records are exposed for parity preview only; v1 graph, Neo4j, and Explorer defaults are unchanged.'
        : backboneNodes.length > 0
        ? 'Admitted BackboneNode records are exposed for shadow preview only; v1 graph, Neo4j, and Explorer defaults are unchanged.'
        : 'Shadow staging contains predicate and source-rights registry metadata only; admitted BackboneNode taxonomy records are not exposed yet.',
    },
    predicateCategories: groupCounts(predicates.map((row) => row.category)).map((group) => ({
      category: group.value,
      count: group.count,
      predicates: predicates
        .filter((row) => row.category === group.value)
        .map((row) => row.predicate)
        .sort((a, b) => a.localeCompare(b)),
    })),
    predicates,
    sourceRightsClasses: groupCounts(sourceFamilies.map((row) => row.sourceRightsClass)).map((group) => ({
      sourceRightsClass: group.value,
      count: group.count,
    })),
    clearanceStates: groupCounts(sourceFamilies.map((row) => row.clearanceState)).map((group) => ({
      clearanceState: group.value,
      count: group.count,
    })),
    backboneNodes,
    shadowGraph,
    sourceFamilies,
    artifactPaths: summary.artifactPaths,
  };
}

export function buildShadowBackboneNodePreview(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null,
  nodeId: string
) {
  if (!shadowGraphArtifact) {
    throw new ShadowBackboneReportError('Shadow backbone node preview requires a shadow graph artifact');
  }
  const preview = buildShadowBackboneTaxonomyPreview(report, artifact, shadowGraphArtifact);
  const requestedId = nodeId.trim();
  if (!requestedId) {
    throw new ShadowBackboneNodeNotFoundError('Shadow backbone node id is required');
  }

  const node = preview.backboneNodes.find((entry: any) => (
    entry.id === requestedId
    || entry.canonicalId === requestedId
    || entry.pathCode === requestedId
  ));
  if (!node) {
    throw new ShadowBackboneNodeNotFoundError(`Shadow backbone node not found: ${requestedId}`);
  }

  const nodeById = new Map(preview.backboneNodes.map((entry: any) => [entry.id, entry]));
  const graphNodeById = new Map(preview.shadowGraph.nodes.map((entry: any) => [entry.id, entry]));
  const relationships = preview.shadowGraph.edges
    .filter((edge: any) => edge.fromId === node.id || edge.toId === node.id)
    .map((edge: any) => {
      const direction = edge.fromId === node.id ? 'outgoing' : 'incoming';
      const fromNode: any = graphNodeById.get(edge.fromId) || nodeById.get(edge.fromId) || {};
      const toNode: any = graphNodeById.get(edge.toId) || nodeById.get(edge.toId) || {};
      return {
        id: edge.id,
        predicate: edge.predicate,
        direction,
        ...shadowBackboneEdgeMetadataFromPreview(edge, { directionKey: 'edgeDirection' }),
        from: {
          id: edge.fromId,
          label: stringField(fromNode.label),
          pathCode: stringField(edge.fromPathCode || fromNode.pathCode),
        },
        to: {
          id: edge.toId,
          label: stringField(toNode.label),
          pathCode: stringField(edge.toPathCode || toNode.pathCode),
        },
        provenance: {
          source: 'file-backed-shadow-backbone-graph',
          artifactPath: preview.artifactPaths.shadowGraph,
          consumerReportPath: preview.artifactPaths.consumerReport,
        },
      };
    })
    .sort((a: any, b: any) => (
      `${a.direction}:${a.predicate}:${a.from.id}:${a.to.id}`
        .localeCompare(`${b.direction}:${b.predicate}:${b.from.id}:${b.to.id}`)
    ));

  return {
    schemaVersion: SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-shadow-backbone-node-preview',
    status: 'shadow_ready',
    reportOk: true,
    runId: preview.runId,
    node: {
      id: node.id,
      canonicalId: node.canonicalId,
      label: node.label,
      displayLabel: node.prefLabel || node.label,
      prefLabel: node.prefLabel,
      pathCode: node.pathCode,
      level: node.level,
      parentPathCode: node.parentPathCode,
      reviewStatus: node.reviewStatus,
      steward: node.steward,
      releaseVersion: node.releaseVersion,
    },
    relationships,
    relationshipCounts: {
      incoming: relationships.filter((edge: any) => edge.direction === 'incoming').length,
      outgoing: relationships.filter((edge: any) => edge.direction === 'outgoing').length,
      total: relationships.length,
    },
    boundaries: preview.boundaries,
    noIngestBoundaryCoverage: preview.noIngestBoundaryCoverage,
    artifactPaths: preview.artifactPaths,
  };
}


function aecMepfsNodeType(level: number, pathCode = '') {
  if (level <= 1) return 'taxonomy';
  if (level === 2) return 'topic';
  if (level === 3) return 'subtopic';
  const leafSegment = pathCode.split('.').at(-1);
  if (leafSegment === 'RUL') return 'rule';
  return 'concept';
}

function aecMepfsTaxonomyPath(pathCode: string) {
  const parts = pathCode.split('.').map((part) => part.trim()).filter(Boolean);
  return parts.map((_, index) => parts.slice(0, index + 1).join('.'));
}

function aecMepfsEdgeType(predicate: string) {
  return predicate === 'broader_than' ? 'HAS_CHILD' : predicate.toUpperCase().replace(/[^A-Z0-9]+/g, '_');
}

function isLikelyAecMepfsBackboneNodeId(value: string) {
  return value.startsWith('VTN-') || /^[A-Z]{2,5}(\.[A-Z0-9]{2,8})*$/.test(value);
}

function isLikelyAecMepfsBackboneEdgeId(value: string) {
  return value.includes('--') && value.includes('VTN-');
}

function aecGraphNodeFromPreview(node: any, metadataById: Map<string, any>) {
  const pathCode = stringField(node.pathCode);
  const level = Number(node.level) || 0;
  const metadata = metadataById.get(node.id) || {};
  const aliases = [pathCode, ...(Array.isArray(metadata.aliases) ? metadata.aliases : [])]
    .map((alias) => String(alias).trim())
    .filter(Boolean);
  return {
    id: node.id,
    label: node.label,
    displayLabel: node.label,
    type: aecMepfsNodeType(level, pathCode),
    kind: 'backbone',
    summary: `AEC-MEPFS BackboneNode ${pathCode || node.id} · Level ${level || 'unknown'}`,
    slug: pathCode ? pathCode.toLowerCase().replace(/[^a-z0-9]+/g, '-') : node.id,
    status: metadata.reviewStatus || 'steward_admitted',
    confidence: 1,
    aliases,
    taxonomy_path: aecMepfsTaxonomyPath(pathCode),
    radius: level <= 1 ? 14 : level === 2 ? 10 : level === 3 ? 9 : 8,
  };
}

function aecGraphEdgeFromPreview(edge: any) {
  const fallbackReasoning = `AEC-MEPFS Backbone predicate: ${edge.predicate} (${edge.fromPathCode || edge.fromId} -> ${edge.toPathCode || edge.toId})`;
  return {
    id: edge.id,
    source: edge.fromId,
    target: edge.toId,
    type: aecMepfsEdgeType(edge.predicate),
    reasoning: edgeReasoningFromMetadata(edge, fallbackReasoning),
    confidence: confidenceFromEdgeMetadata(edge),
    assertionId: edge.id,
    ...shadowBackboneEdgeMetadataFromPreview(edge),
  };
}

export function buildAecMepfsExplorerGraph(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null
) {
  const preview = buildShadowBackboneTaxonomyPreview(report, artifact, shadowGraphArtifact);
  if (!preview.shadowGraph.available) {
    throw new ShadowBackboneReportError('AEC-MEPFS Explorer graph requires a shadow graph artifact');
  }
  const rawBackboneRows = Array.isArray(artifact.backbone_nodes) ? artifact.backbone_nodes : [];
  const metadataById = new Map<string, any>();
  for (const row of rawBackboneRows) {
    if (!row || typeof row !== 'object') continue;
    const id = stringField((row as any).id);
    if (!id) continue;
    metadataById.set(id, {
      aliases: Array.isArray((row as any).aliases)
        ? (row as any).aliases.filter((alias: unknown): alias is string => typeof alias === 'string')
        : [],
      reviewStatus: stringField((row as any).review_status),
    });
  }
  const nodes = preview.shadowGraph.nodes.map((node: any) => aecGraphNodeFromPreview(node, metadataById));
  const baseEdges = preview.shadowGraph.edges.map((edge: any) => aecGraphEdgeFromPreview(edge));
  const nodeIds = new Set(nodes.map((node: any) => node.id));
  const admittedStewardshipEdges = readCanonicalAdmittedRelationships(repoRoot)
    .filter((edge) => edge.reviewStatus !== 'rolled_back' && nodeIds.has(edge.source) && nodeIds.has(edge.target));
  const edges = mergeAdmittedRelationshipsIntoEdges(baseEdges, admittedStewardshipEdges);
  return {
    schemaVersion: AEC_MEPFS_EXPLORER_GRAPH_SCHEMA_VERSION,
    source: 'file-backed-aec-mepfs-backbone-graph',
    status: 'aec_mepfs_first_default_ready',
    runId: preview.runId,
    nodes,
    edges,
    boundaries: {
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      kgRebuild: false,
      protectedContentIngest: false,
      explorerDefaultAdoption: true,
      broadLiveRuntimeAuthorization: false,
    },
    artifactPaths: preview.artifactPaths,
  };
}

function buildAecMepfsTaxonomyTreeFromGraph(graph: ReturnType<typeof buildAecMepfsExplorerGraph>) {
  const nodeByPathCode = new Map<string, any>();
  const childrenByParent = new Map<string, any[]>();
  for (const node of graph.nodes) {
    const pathCode = node.aliases?.[0] || '';
    nodeByPathCode.set(pathCode, node);
    const parts = pathCode.split('.');
    const parentPathCode = parts.length > 1 ? parts.slice(0, -1).join('.') : '';
    if (!childrenByParent.has(parentPathCode)) childrenByParent.set(parentPathCode, []);
    childrenByParent.get(parentPathCode)!.push(node);
  }
  function buildTree(node: any): any {
    const pathCode = node.aliases?.[0] || '';
    const children = (childrenByParent.get(pathCode) || [])
      .sort((left, right) => left.displayLabel.localeCompare(right.displayLabel))
      .map((child) => buildTree(child));
    return {
      id: node.id,
      label: node.label,
      displayLabel: node.displayLabel,
      kind: node.type,
      conceptCount: 0,
      children,
    };
  }
  return (childrenByParent.get('') || [])
    .sort((left, right) => left.displayLabel.localeCompare(right.displayLabel))
    .map((node) => buildTree(node));
}

export function buildAecMepfsNodeDetail(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null,
  nodeId: string
) {
  const preview = buildShadowBackboneNodePreview(report, artifact, shadowGraphArtifact, nodeId);
  const graph = buildAecMepfsExplorerGraph(report, artifact, shadowGraphArtifact);
  const graphNodeById = new Map(graph.nodes.map((node: any) => [node.id, node]));
  const currentNode = graphNodeById.get(preview.node.id);
  if (!currentNode) {
    throw new ShadowBackboneNodeNotFoundError(`Shadow backbone node not found: ${nodeId}`);
  }
  const taxonomyPath = (currentNode.taxonomy_path || [])
    .map((pathCode: string) => graph.nodes.find((candidate: any) => candidate.aliases?.[0] === pathCode))
    .filter(Boolean)
    .map((node: any) => ({
      id: node.id,
      label: node.label,
      displayLabel: node.displayLabel,
      kind: node.type,
      conceptCount: 0,
      children: [],
    }));
  const incoming = preview.relationships
    .filter((relationship: any) => relationship.direction === 'incoming')
    .map((relationship: any) => {
      const fallbackReasoning = `AEC-MEPFS Backbone predicate: ${relationship.predicate}`;
      return {
        relType: aecMepfsEdgeType(relationship.predicate),
        other: graphNodeById.get(relationship.from.id),
        reasoning: edgeReasoningFromMetadata(relationship, fallbackReasoning),
        confidence: confidenceFromEdgeMetadata(relationship),
        assertionId: relationship.id,
        ...shadowBackboneEdgeMetadataFromPreview(relationship, { directionKey: 'edgeDirection' }),
      };
    })
    .filter((relationship: any) => relationship.other);
  const outgoing = preview.relationships
    .filter((relationship: any) => relationship.direction === 'outgoing')
    .map((relationship: any) => {
      const fallbackReasoning = `AEC-MEPFS Backbone predicate: ${relationship.predicate}`;
      return {
        relType: aecMepfsEdgeType(relationship.predicate),
        other: graphNodeById.get(relationship.to.id),
        reasoning: edgeReasoningFromMetadata(relationship, fallbackReasoning),
        confidence: confidenceFromEdgeMetadata(relationship),
        assertionId: relationship.id,
        ...shadowBackboneEdgeMetadataFromPreview(relationship, { directionKey: 'edgeDirection' }),
      };
    })
    .filter((relationship: any) => relationship.other);
  const resourceData = readResourceLayerData(repoRoot);
  const canonicalGroups = buildDuplicateCandidateGroups(graph.nodes, graph.edges, resourceData, readCanonicalDecisions(repoRoot));
  return {
    node: currentNode,
    taxonomyPath,
    incoming,
    outgoing,
    evidence: [],
    resources: getNodeResources(repoRoot, nodeId, { limit: 8 }),
    canonical: canonicalNodeStatus(repoRoot, nodeId, canonicalGroups),
  };
}

export function buildAecMepfsEdgeDetail(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null,
  edgeId: string
) {
  const graph = buildAecMepfsExplorerGraph(report, artifact, shadowGraphArtifact);
  const edge = graph.edges.find((candidate: any) => candidate.id === edgeId);
  if (!edge) {
    throw new ShadowBackboneEdgeNotFoundError(`Shadow backbone edge not found: ${edgeId}`);
  }
  const nodeById = new Map(graph.nodes.map((node: any) => [node.id, node]));
  return {
    edge,
    source: nodeById.get(edge.source),
    target: nodeById.get(edge.target),
    evidence: [],
  };
}

function buildAecMepfsNodeDetailFromIndex(index: AecMepfsExplorerGraphIndex, nodeId: string) {
  const currentNode = index.nodeById.get(nodeId);
  if (!currentNode) {
    throw new ShadowBackboneNodeNotFoundError(`Shadow backbone node not found: ${nodeId}`);
  }
  const taxonomyPath = (currentNode.taxonomy_path || [])
    .map((pathCode: string) => index.nodeByPathCode.get(pathCode))
    .filter(Boolean)
    .map((node: any) => ({
      id: node.id,
      label: node.label,
      displayLabel: node.displayLabel,
      kind: node.type,
      conceptCount: 0,
      children: [],
    }));
  const incoming = (index.incomingByNodeId.get(nodeId) || [])
    .map((edge: any) => relationDetailFromEdge(index, edge, nodeId))
    .filter((relationship: any) => relationship.other);
  const outgoing = (index.outgoingByNodeId.get(nodeId) || [])
    .map((edge: any) => relationDetailFromEdge(index, edge, nodeId))
    .filter((relationship: any) => relationship.other);
  const resourceData = readResourceLayerData(repoRoot);
  const canonicalGroups = buildDuplicateCandidateGroups(
    Array.from(index.nodeById.values()),
    Array.from(index.edgeById.values()),
    resourceData,
    readCanonicalDecisions(repoRoot),
  );
  return {
    node: currentNode,
    taxonomyPath,
    incoming,
    outgoing,
    evidence: [],
    resources: getNodeResources(repoRoot, nodeId, { limit: 8 }),
    canonical: canonicalNodeStatus(repoRoot, nodeId, canonicalGroups),
  };
}

function buildAecMepfsEdgeDetailFromIndex(index: AecMepfsExplorerGraphIndex, edgeId: string) {
  const edge = index.edgeById.get(edgeId);
  if (!edge) {
    throw new ShadowBackboneEdgeNotFoundError(`Shadow backbone edge not found: ${edgeId}`);
  }
  return {
    edge,
    source: index.nodeById.get(edge.source),
    target: index.nodeById.get(edge.target),
    evidence: [],
  };
}

function relationDetailFromEdge(
  index: AecMepfsExplorerGraphIndex,
  edge: AecMepfsExplorerEdge,
  focusNodeId: string,
) {
  const normalized = normalizeGraphRelationship(edge, index.nodeById, focusNodeId);
  const otherNodeId = edge.source === focusNodeId ? edge.target : edge.source;
  return {
    relType: edge.type,
    other: index.nodeById.get(otherNodeId),
    reasoning: edge.reasoning,
    confidence: edge.confidence,
    assertionId: edge.assertionId,
    relationshipId: edge.id,
    sourceNodeId: edge.source,
    targetNodeId: edge.target,
    category: normalized.category,
    isHierarchyEdge: normalized.isHierarchyEdge,
    isSemanticEdge: normalized.isSemanticEdge,
    visibility: {
      canvasEdgeType: edge.type,
      defaultVisible: true,
      hiddenReasons: [],
    },
    ...shadowBackboneEdgeMetadataFromPreview(edge, { directionKey: 'edgeDirection' }),
  };
}

function buildAecMepfsExpandResult(
  graph: ReturnType<typeof buildAecMepfsExplorerGraph>,
  nodeId: string,
  relTypes: string[] | undefined,
  direction: string,
  depth = 1,
  limit = 200,
) {
  const allowedTypes = relTypes && relTypes.length ? new Set(relTypes) : null;
  const nodeById = new Map(graph.nodes.map((node: any) => [node.id, node]));
  const maxDepth = Math.min(Math.max(Math.floor(depth) || 1, 1), 6);
  const maxEdges = Math.min(Math.max(Math.floor(limit) || 50, 1), 500);
  const matches = (edge: any, currentNodeId: string) => {
    if (allowedTypes && !allowedTypes.has(edge.type)) return false;
    if (direction === 'out') return edge.source === currentNodeId;
    if (direction === 'in') return edge.target === currentNodeId;
    return edge.source === currentNodeId || edge.target === currentNodeId;
  };
  const otherNode = (edge: any, currentNodeId: string) => edge.source === currentNodeId ? edge.target : edge.source;
  const incidentEdges: any[] = [];
  const seenEdges = new Set<string>();
  const visitedNodes = new Set<string>([nodeId]);
  let frontier = [nodeId];
  for (let currentDepth = 0; currentDepth < maxDepth && frontier.length > 0 && incidentEdges.length < maxEdges; currentDepth += 1) {
    const nextFrontier: string[] = [];
    for (const currentNodeId of frontier) {
      for (const edge of graph.edges) {
        if (incidentEdges.length >= maxEdges) break;
        if (!matches(edge, currentNodeId)) continue;
        const edgeId = edge.id || `${edge.source}-${edge.type}-${edge.target}`;
        if (seenEdges.has(edgeId)) continue;
        seenEdges.add(edgeId);
        incidentEdges.push(edge);
        const nextNodeId = otherNode(edge, currentNodeId);
        if (!visitedNodes.has(nextNodeId)) {
          visitedNodes.add(nextNodeId);
          nextFrontier.push(nextNodeId);
        }
      }
    }
    frontier = nextFrontier;
  }
  const nodeIds = new Set<string>([nodeId]);
  for (const edge of incidentEdges) {
    nodeIds.add(edge.source);
    nodeIds.add(edge.target);
  }
  return {
    nodeId,
    neighbors: incidentEdges.filter((edge: any) => edge.source === nodeId || edge.target === nodeId).map((edge: any) => {
      const otherId = edge.source === nodeId ? edge.target : edge.source;
      return {
        node: nodeById.get(otherId),
        relType: edge.type,
        direction: edge.source === nodeId ? 'out' : 'in',
      };
    }).filter((neighbor: any) => neighbor.node),
    nodes: Array.from(nodeIds).map((id) => nodeById.get(id)).filter(Boolean),
    edges: incidentEdges,
  };
}

function buildAecMepfsExpandResultFromIndex(
  index: AecMepfsExplorerGraphIndex,
  nodeId: string,
  relTypes: string[] | undefined,
  direction: string,
  depth = 1,
  limit = 200,
) {
  const allowedTypes = relTypes && relTypes.length ? new Set(relTypes) : null;
  const maxDepth = Math.min(Math.max(Math.floor(depth) || 1, 1), 6);
  const maxEdges = Math.min(Math.max(Math.floor(limit) || 50, 1), 500);
  const incidentEdges: AecMepfsExplorerEdge[] = [];
  const seenEdges = new Set<string>();
  const visitedNodes = new Set<string>([nodeId]);
  let frontier = [nodeId];

  const candidateEdges = (currentNodeId: string) => {
    if (direction === 'out') return index.outgoingByNodeId.get(currentNodeId) || [];
    if (direction === 'in') return index.incomingByNodeId.get(currentNodeId) || [];
    return index.undirectedByNodeId.get(currentNodeId) || [];
  };
  const otherNode = (edge: AecMepfsExplorerEdge, currentNodeId: string) => edge.source === currentNodeId ? edge.target : edge.source;

  for (let currentDepth = 0; currentDepth < maxDepth && frontier.length > 0 && incidentEdges.length < maxEdges; currentDepth += 1) {
    const nextFrontier: string[] = [];
    for (const currentNodeId of frontier) {
      for (const edge of candidateEdges(currentNodeId)) {
        if (incidentEdges.length >= maxEdges) break;
        if (allowedTypes && !allowedTypes.has(edge.type)) continue;
        if (seenEdges.has(edge.id)) continue;
        seenEdges.add(edge.id);
        incidentEdges.push(edge);
        const nextNodeId = otherNode(edge, currentNodeId);
        if (!visitedNodes.has(nextNodeId)) {
          visitedNodes.add(nextNodeId);
          nextFrontier.push(nextNodeId);
        }
      }
    }
    frontier = nextFrontier;
  }

  const nodeIds = new Set<string>([nodeId]);
  for (const edge of incidentEdges) {
    nodeIds.add(edge.source);
    nodeIds.add(edge.target);
  }
  return {
    nodeId,
    neighbors: incidentEdges.filter((edge: any) => edge.source === nodeId || edge.target === nodeId).map((edge: any) => {
      const otherId = edge.source === nodeId ? edge.target : edge.source;
      return {
        node: index.nodeById.get(otherId),
        relType: edge.type,
        direction: edge.source === nodeId ? 'out' : 'in',
      };
    }).filter((neighbor: any) => neighbor.node),
    nodes: Array.from(nodeIds).map((id) => index.nodeById.get(id)).filter(Boolean),
    edges: incidentEdges,
  };
}

function buildAecMepfsNeighborhoodResultFromIndex(
  index: AecMepfsExplorerGraphIndex,
  nodeId: string,
  options: {
    relTypes?: string[];
    direction?: 'in' | 'out' | 'both';
    depth?: number;
    limit?: number;
    includeHierarchyEdges?: boolean;
    includeSemanticEdges?: boolean;
  } = {},
) {
  return {
    schemaVersion: 'aec-mepfs-graph-neighborhood/v1',
    source: 'file-backed-aec-mepfs-normalized-neighborhood',
    ...buildGraphNeighborhood(index, nodeId, options),
  };
}

function buildAecMepfsPathResult(graph: ReturnType<typeof buildAecMepfsExplorerGraph>, from: string, to: string, maxHops: number) {
  const nodeById = new Map(graph.nodes.map((node: any) => [node.id, node]));
  if (!nodeById.has(from) || !nodeById.has(to)) return [];
  const adjacency = new Map<string, Array<{ next: string; edge: any }>>();
  for (const edge of graph.edges) {
    if (!adjacency.has(edge.source)) adjacency.set(edge.source, []);
    if (!adjacency.has(edge.target)) adjacency.set(edge.target, []);
    adjacency.get(edge.source)!.push({ next: edge.target, edge });
    adjacency.get(edge.target)!.push({ next: edge.source, edge });
  }
  const queue: Array<{ nodeId: string; nodes: string[]; edges: any[] }> = [{ nodeId: from, nodes: [from], edges: [] }];
  const visited = new Set<string>([from]);
  while (queue.length) {
    const current = queue.shift()!;
    if (current.nodeId === to) {
      return [{
        length: current.edges.length,
        nodes: current.nodes.map((id) => nodeById.get(id)).filter(Boolean),
        edges: current.edges,
      }];
    }
    if (current.edges.length >= maxHops) continue;
    for (const next of adjacency.get(current.nodeId) || []) {
      if (visited.has(next.next)) continue;
      visited.add(next.next);
      queue.push({ nodeId: next.next, nodes: [...current.nodes, next.next], edges: [...current.edges, next.edge] });
    }
  }
  return [];
}

function buildAecMepfsPathResultFromIndex(index: AecMepfsExplorerGraphIndex, from: string, to: string, maxHops: number) {
  if (!index.nodeById.has(from) || !index.nodeById.has(to)) return [];
  const queue: Array<{ nodeId: string; nodes: string[]; edges: AecMepfsExplorerEdge[] }> = [{ nodeId: from, nodes: [from], edges: [] }];
  const visited = new Set<string>([from]);
  while (queue.length) {
    const current = queue.shift()!;
    if (current.nodeId === to) {
      return [{
        length: current.edges.length,
        nodes: current.nodes.map((id) => index.nodeById.get(id)).filter(Boolean),
        edges: current.edges,
      }];
    }
    if (current.edges.length >= maxHops) continue;
    for (const edge of index.undirectedByNodeId.get(current.nodeId) || []) {
      const nextNodeId = edge.source === current.nodeId ? edge.target : edge.source;
      if (visited.has(nextNodeId)) continue;
      visited.add(nextNodeId);
      queue.push({ nodeId: nextNodeId, nodes: [...current.nodes, nextNodeId], edges: [...current.edges, edge] });
    }
  }
  return [];
}

function normalizeSearchTerm(value: string) {
  return value.trim().toLowerCase();
}

function compareAscii(left: string, right: string) {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function searchRank(candidate: string, query: string) {
  const normalized = normalizeSearchTerm(candidate);
  if (!normalized) return null;
  if (normalized === query) return 100;
  if (normalized.startsWith(query)) return 80;
  if (normalized.includes(query)) return 60;
  return null;
}

function parseSearchLimit(value: unknown) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric <= 0) return 10;
  return Math.min(Math.floor(numeric), 25);
}

export function buildShadowBackboneSearchPreview(
  report: Record<string, any>,
  artifact: Record<string, any>,
  shadowGraphArtifact: Record<string, any> | null,
  query: string,
  limit = 10
) {
  if (!shadowGraphArtifact) {
    throw new ShadowBackboneReportError('Shadow backbone search preview requires a shadow graph artifact');
  }

  const normalizedQuery = normalizeSearchTerm(query);
  if (!normalizedQuery) {
    throw new ShadowBackboneSearchQueryError('Shadow backbone search query is required');
  }

  const preview = buildShadowBackboneTaxonomyPreview(report, artifact, shadowGraphArtifact);
  const errors: string[] = [];
  const rawRows = requireArray(artifact.backbone_nodes, 'backbone_nodes', errors);
  const metadataById = new Map<string, { aliases: string[] }>();
  rawRows.forEach((value, index) => {
    const row = requireRecord(value, `backbone_nodes[${index}]`, errors);
    const id = requiredStringField(row.id, `backbone_nodes[${index}].id`, errors);
    metadataById.set(id, {
      aliases: optionalStringArrayField(row.aliases, `backbone_nodes[${index}].aliases`, errors),
    });
  });
  if (errors.length) {
    throw new ShadowBackboneReportError(
      `Shadow backbone search metadata failed validation: ${errors.join('; ')}`
    );
  }

  const results = preview.backboneNodes
    .map((node: any) => {
      const metadata = metadataById.get(node.id) || { aliases: [] };
      const fields = [
        { field: 'label', text: stringField(node.label) },
        { field: 'prefLabel', text: stringField(node.prefLabel) },
        { field: 'pathCode', text: stringField(node.pathCode) },
        ...metadata.aliases.map((text) => ({ field: 'alias', text })),
      ];
      const best = fields
        .map((field) => ({ ...field, rank: searchRank(field.text, normalizedQuery) }))
        .filter((field): field is { field: string; text: string; rank: number } => field.rank !== null)
        .sort((a, b) => b.rank - a.rank || compareAscii(a.field, b.field) || compareAscii(a.text, b.text))[0];
      if (!best) return null;
      return {
        id: node.id,
        canonicalId: node.canonicalId,
        label: node.label,
        displayLabel: node.prefLabel || node.label,
        pathCode: node.pathCode,
        level: node.level,
        parentPathCode: node.parentPathCode,
        matchedField: best.field,
        matchedText: best.text,
        score: best.rank,
        detailRoute: `/v2/backbone/node/${encodeURIComponent(node.id)}`,
      };
    })
    .filter(Boolean)
    .sort((a: any, b: any) => (
      b.score - a.score
      || a.level - b.level
      || compareAscii(a.pathCode, b.pathCode)
      || compareAscii(a.id, b.id)
    ));

  const boundedLimit = Math.min(Math.max(Math.floor(limit), 1), 25);
  return {
    schemaVersion: SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-shadow-backbone-search-preview',
    status: 'shadow_ready',
    reportOk: true,
    runId: preview.runId,
    query,
    normalizedQuery,
    total: results.length,
    returned: Math.min(results.length, boundedLimit),
    results: results.slice(0, boundedLimit),
    boundaries: preview.boundaries,
    noIngestBoundaryCoverage: preview.noIngestBoundaryCoverage,
    artifactPaths: preview.artifactPaths,
  };
}

export function buildShadowBackboneSourcePreview(
  report: Record<string, any>,
  artifact: Record<string, any>,
  sourceId: string
) {
  const requestedId = sourceId.trim();
  if (!requestedId) {
    throw new ShadowBackboneSourceIdError('Shadow backbone source id is required');
  }

  const preview = buildShadowBackboneTaxonomyPreview(report, artifact);
  const sourceRecord = preview.sourceFamilies.find((entry: any) => (
    entry.sourceId === requestedId
    || entry.sourceFamily === requestedId
  ));
  if (!sourceRecord) {
    throw new ShadowBackboneSourceNotFoundError(`Shadow backbone source not found: ${requestedId}`);
  }

  const sourceLabels = [
    sourceRecord.sourceFamily,
    sourceRecord.publisherAuthority,
  ].filter((value) => typeof value === 'string' && value.length > 0);

  return {
    schemaVersion: SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-shadow-source-preview',
    status: 'shadow_ready',
    reportOk: true,
    runId: preview.runId,
    sourceRecord: {
      sourceId: sourceRecord.sourceId,
      sourceFamily: sourceRecord.sourceFamily,
      sourceLabels,
      evidenceTitle: sourceRecord.sourceFamily,
      publisherAuthority: sourceRecord.publisherAuthority,
      sourceRightsClass: sourceRecord.sourceRightsClass,
      clearanceState: sourceRecord.clearanceState,
      declaredUseBoundary: sourceRecord.declaredUseBoundary,
      currentnessCheckDate: sourceRecord.currentnessCheckDate,
      stewardOwner: sourceRecord.stewardOwner,
      updateCadence: sourceRecord.updateCadence,
    },
    boundaries: preview.boundaries,
    noIngestBoundaryCoverage: preview.noIngestBoundaryCoverage,
    artifactPaths: preview.artifactPaths,
  };
}

type AecMepfsResolverEnv = Record<string, string | undefined>;

type AecMepfsResolverRequest = {
  text: string;
  conceptId: string;
  assetContext: string;
  jurisdiction: string;
  effectiveDate: string;
  contextIds: string[];
  jurisdictionFilters: string[];
  disciplineFilters: string[];
  traceRequested: boolean;
};

type AecMepfsResolverCase = {
  caseId: string;
  query: Record<string, any>;
  jurisdiction: string;
  effectiveDate: string;
  resultType: string;
  confidence: string;
  rationale: string;
  sourceEvidenceRefs: string[];
  canonicalNodeRefs: Array<{ nodeId: string; role: string }>;
  fallbackReason: string;
  traceSafeRationale: string;
};

export function isAecMepfsResolverRuntimeEnabled(
  env: AecMepfsResolverEnv = process.env
) {
  const value = stringField(env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG]).trim().toLowerCase();
  if (!value) return true;
  return !['0', 'false', 'no', 'off', 'disabled'].includes(value);
}

function relativeRepoPath(path: string) {
  const resolved = resolve(path);
  const rel = relative(repoRoot, resolved);
  if (!rel || (!rel.startsWith('..') && !rel.startsWith(sep))) return rel || '.';
  return resolved;
}

function resolveAecMepfsResolverFixturePath(
  env: AecMepfsResolverEnv = process.env
) {
  const configuredPath = stringField(env[AEC_MEPFS_RESOLVER_FIXTURE_FLAG]).trim();
  const fixturePath = configuredPath
    ? resolve(repoRoot, configuredPath)
    : DEFAULT_AEC_MEPFS_RESOLVER_FIXTURE_PATH;
  const rel = relative(repoRoot, fixturePath);
  if (rel.startsWith('..') || rel.startsWith(sep)) {
    throw new AecMepfsResolverArtifactError(
      'AEC-MEPFS resolver fixture path must stay inside the repository'
    );
  }
  return fixturePath;
}

function normalizeAecMepfsResolverRequest(value: unknown): AecMepfsResolverRequest {
  const errors: string[] = [];
  const body = requireRecord(value, 'request', errors);
  const query = isRecord(body.query) ? body.query : body;
  const text = requiredStringField(query.text, 'query.text', errors);
  const contextIds = optionalStringArrayField(
    query.context_ids ?? query.contextIds,
    'query.context_ids',
    errors
  );
  const jurisdictionFilters = optionalStringArrayField(
    query.jurisdiction_filters ?? query.jurisdictionFilters,
    'query.jurisdiction_filters',
    errors
  );
  const disciplineFilters = optionalStringArrayField(
    query.discipline_filters ?? query.disciplineFilters,
    'query.discipline_filters',
    errors
  );
  const traceRequested = Boolean(
    query.trace_requested ?? query.traceRequested ?? body.include_trace ?? body.includeTrace
  );
  const conceptId = stringField(query.concept_id ?? query.conceptId).trim();
  const assetContext = stringField(query.asset_context ?? query.assetContext ?? body.asset_context).trim();
  const jurisdiction = stringField(body.jurisdiction ?? jurisdictionFilters[0]).trim();
  const effectiveDate = stringField(body.effective_date ?? query.effective_date ?? body.effectiveDate).trim();

  if (errors.some((error) => error.includes('expected string array') || error.includes('expected array'))) {
    throw new AecMepfsResolverInputError(
      'AEC_MEPFS_RESOLVER_MALFORMED_REQUEST',
      errors.join('; ')
    );
  }
  if (errors.length) {
    throw new AecMepfsResolverInputError(
      'AEC_MEPFS_RESOLVER_INVALID_INPUT',
      errors.join('; ')
    );
  }

  return {
    text,
    conceptId,
    assetContext,
    jurisdiction,
    effectiveDate,
    contextIds,
    jurisdictionFilters,
    disciplineFilters,
    traceRequested,
  };
}

function stringArrayFromRecord(value: unknown, path: string, errors: string[]) {
  return stringArrayField(value, path, errors);
}

function parseAecMepfsResolverCase(value: unknown, index: number, errors: string[]) {
  const row = requireRecord(value, `resolver_golden_cases[${index}]`, errors);
  const query = requireRecord(row.query, `resolver_golden_cases[${index}].query`, errors);
  const nodeRefs = requireArray(
    row.expected_node_refs,
    `resolver_golden_cases[${index}].expected_node_refs`,
    errors
  ).map((item, refIndex) => {
    const ref = requireRecord(
      item,
      `resolver_golden_cases[${index}].expected_node_refs[${refIndex}]`,
      errors
    );
    return {
      nodeId: requiredStringField(
        ref.node_id,
        `resolver_golden_cases[${index}].expected_node_refs[${refIndex}].node_id`,
        errors
      ),
      role: requiredStringField(
        ref.role,
        `resolver_golden_cases[${index}].expected_node_refs[${refIndex}].role`,
        errors
      ),
    };
  });
  return {
    caseId: requiredStringField(row.case_id, `resolver_golden_cases[${index}].case_id`, errors),
    query,
    jurisdiction: requiredStringField(row.jurisdiction, `resolver_golden_cases[${index}].jurisdiction`, errors),
    effectiveDate: requiredStringField(
      row.effective_date,
      `resolver_golden_cases[${index}].effective_date`,
      errors
    ),
    resultType: requiredStringField(
      row.expected_result_type,
      `resolver_golden_cases[${index}].expected_result_type`,
      errors
    ),
    confidence: requiredStringField(
      row.expected_confidence,
      `resolver_golden_cases[${index}].expected_confidence`,
      errors
    ),
    rationale: requiredStringField(row.rationale, `resolver_golden_cases[${index}].rationale`, errors),
    sourceEvidenceRefs: stringArrayFromRecord(
      row.source_evidence,
      `resolver_golden_cases[${index}].source_evidence`,
      errors
    ),
    canonicalNodeRefs: nodeRefs,
    fallbackReason: requiredStringField(
      row.fallback_reason,
      `resolver_golden_cases[${index}].fallback_reason`,
      errors
    ),
    traceSafeRationale: requiredStringField(
      row.trace_safe_rationale,
      `resolver_golden_cases[${index}].trace_safe_rationale`,
      errors
    ),
  };
}

async function readAecMepfsResolverCases(env: AecMepfsResolverEnv = process.env) {
  const fixturePath = resolveAecMepfsResolverFixturePath(env);
  if (!existsSync(fixturePath)) {
    throw new AecMepfsResolverArtifactError(
      `AEC-MEPFS resolver fixture is unavailable: ${relativeRepoPath(fixturePath)}`
    );
  }
  let payload: Record<string, any>;
  try {
    payload = JSON.parse(await readFile(fixturePath, 'utf-8'));
  } catch (error: any) {
    throw new AecMepfsResolverArtifactError(
      `AEC-MEPFS resolver fixture could not be parsed: ${error?.message || 'invalid JSON'}`
    );
  }

  const errors: string[] = [];
  const caseValues = requireArray(payload.resolver_golden_cases, 'resolver_golden_cases', errors);
  const cases = caseValues.map((value, index) => parseAecMepfsResolverCase(value, index, errors));
  if (errors.length) {
    throw new AecMepfsResolverArtifactError(
      `AEC-MEPFS resolver fixture failed validation: ${errors.join('; ')}`
    );
  }
  return { fixturePath, cases };
}

function normalizedResolverText(value: string) {
  return value.replace(/\s+/g, ' ').trim().toLowerCase();
}

function fixtureCaseTraceId(row: Pick<AecMepfsResolverCase, 'caseId'>) {
  return `aec-trace-${createHash('sha256').update(row.caseId).digest('hex').slice(0, 16)}`;
}

function matchAecMepfsResolverCase(
  cases: AecMepfsResolverCase[],
  request: AecMepfsResolverRequest
) {
  const normalizedText = normalizedResolverText(request.text);
  const textMatch = cases.find((row) => normalizedResolverText(stringField(row.query.text)) === normalizedText);
  if (textMatch) return textMatch;

  return cases.find((row) => {
    const query = row.query;
    const conceptMatches = request.conceptId && stringField(query.concept_id) === request.conceptId;
    const assetMatches = request.assetContext && stringField(query.asset_context) === request.assetContext;
    const jurisdictionMatches = !request.jurisdiction || row.jurisdiction === request.jurisdiction;
    return conceptMatches && assetMatches && jurisdictionMatches;
  }) || null;
}

function buildAecMepfsResolverTrace(
  row: AecMepfsResolverCase | null,
  request: AecMepfsResolverRequest,
  fixturePath: string
) {
  const traceId = row ? fixtureCaseTraceId(row) : `aec-trace-${createHash('sha256').update(request.text).digest('hex').slice(0, 16)}`;
  const resultType = row?.resultType || 'none';
  const confidence = row?.confidence || 'insufficient';
  const fallbackReason = row?.fallbackReason || 'no_static_fixture_case_match';
  const traceSafeRationale = row?.traceSafeRationale || 'No admitted fixture case matched; no source claim was generated.';

  return {
    schemaVersion: AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION,
    traceId,
    caseId: row?.caseId || null,
    resultType,
    confidence,
    fallbackReason,
    traceSafeRationale,
    steps: [
      {
        step: 'validate_request',
        status: 'passed',
        detail: 'Request shape was validated without LLM or database access.',
      },
      {
        step: 'read_file_backed_fixture',
        status: 'passed',
        detail: `Read non-protected resolver fixture ${relativeRepoPath(fixturePath)}.`,
      },
      {
        step: 'deterministic_case_match',
        status: row ? 'matched' : 'none',
        detail: row
          ? `Matched governed resolver fixture case ${row.caseId}.`
          : 'No governed resolver fixture case matched the request.',
      },
      {
        step: 'return_safe_result',
        status: 'passed',
        detail: 'Returned canonical IDs, source IDs, and safe rationale only.',
      },
    ],
  };
}

export async function buildAecMepfsResolverRuntimeResponse(
  rawRequest: unknown,
  env: AecMepfsResolverEnv = process.env
) {
  const request = normalizeAecMepfsResolverRequest(rawRequest);
  const { fixturePath, cases } = await readAecMepfsResolverCases(env);
  const matchedCase = matchAecMepfsResolverCase(cases, request);
  const trace = buildAecMepfsResolverTrace(matchedCase, request, fixturePath);

  return {
    schemaVersion: AEC_MEPFS_RESOLVER_RESPONSE_SCHEMA_VERSION,
    status: 'resolved',
    runtimeMode: 'file_backed_default_on_runtime',
    resultType: matchedCase?.resultType || 'none',
    confidence: matchedCase?.confidence || 'insufficient',
    query: {
      text: request.text,
      conceptId: request.conceptId || null,
      assetContext: request.assetContext || null,
      contextIds: request.contextIds,
      jurisdiction: request.jurisdiction || null,
      jurisdictionFilters: request.jurisdictionFilters,
      disciplineFilters: request.disciplineFilters,
      effectiveDate: request.effectiveDate || null,
      traceRequested: request.traceRequested,
    },
    canonicalNodeRefs: matchedCase?.canonicalNodeRefs || [],
    sourceEvidenceRefs: matchedCase?.sourceEvidenceRefs || [],
    fallbackReason: matchedCase?.fallbackReason || 'no_static_fixture_case_match',
    traceId: trace.traceId,
    traceSafeRationale: trace.traceSafeRationale,
    trace: request.traceRequested ? trace : null,
    conflictSet: matchedCase?.resultType === 'conflict'
      ? {
          candidateNodeRefs: matchedCase.canonicalNodeRefs,
          resolution: 'human_review_required',
          reason: matchedCase.fallbackReason,
        }
      : null,
    boundaries: {
      defaultOffRuntimeRoute: false,
      defaultOnRuntimeRoute: true,
      rollbackDisableFlag: AEC_MEPFS_RESOLVER_RUNTIME_FLAG,
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      kgRebuild: false,
      protectedContentIngest: false,
      llmHotPath: false,
      explorerDefaultAdoption: false,
      runtimeThresholdClaim: false,
    },
    artifactPaths: {
      fixture: relativeRepoPath(fixturePath),
    },
  };
}

export async function buildAecMepfsResolverTraceResponse(
  traceId: string,
  env: AecMepfsResolverEnv = process.env
) {
  const requestedTraceId = traceId.trim();
  if (!requestedTraceId) {
    throw new AecMepfsResolverInputError(
      'AEC_MEPFS_RESOLVER_TRACE_INVALID',
      'Trace id is required',
      400
    );
  }
  const { fixturePath, cases } = await readAecMepfsResolverCases(env);
  const row = cases.find((candidate) => fixtureCaseTraceId(candidate) === requestedTraceId);
  if (!row) {
    throw new AecMepfsResolverTraceNotFoundError(`Resolver trace not found: ${requestedTraceId}`);
  }
  const request = normalizeAecMepfsResolverRequest({
    query: row.query,
    jurisdiction: row.jurisdiction,
    effective_date: row.effectiveDate,
  });
  return buildAecMepfsResolverTrace(row, request, fixturePath);
}

function resolverErrorPayload(error: any, fallbackCode: string, fallbackMessage: string) {
  return {
    error: {
      code: stringField(error?.code) || fallbackCode,
      message: error?.message || fallbackMessage,
    },
  };
}

export async function handleAecMepfsResolverRequest(c: any) {
  let body: unknown;
  try {
    body = await c.req.json();
  } catch {
    return c.json({
      error: {
        code: 'AEC_MEPFS_RESOLVER_MALFORMED_REQUEST',
        message: 'Request body must be valid JSON',
      },
    }, 400);
  }

  try {
    return c.json(await buildAecMepfsResolverRuntimeResponse(body));
  } catch (error: any) {
    if (error instanceof AecMepfsResolverInputError || error instanceof AecMepfsResolverArtifactError) {
      return c.json(
        resolverErrorPayload(error, 'AEC_MEPFS_RESOLVER_ERROR', 'Resolver request failed'),
        error.status as any
      );
    }
    return c.json({
      error: {
        code: 'AEC_MEPFS_RESOLVER_UNAVAILABLE',
        message: error?.message || 'AEC-MEPFS resolver is unavailable',
      },
    }, 503);
  }
}

export async function handleAecMepfsResolverTraceRequest(c: any) {
  let traceId = '';
  try {
    traceId = decodeURIComponent(c.req.param('trace_id') || '');
  } catch {
    return c.json({
      error: {
        code: 'AEC_MEPFS_RESOLVER_TRACE_INVALID',
        message: 'Trace id is not valid URI encoding',
      },
    }, 400);
  }

  try {
    return c.json(await buildAecMepfsResolverTraceResponse(traceId));
  } catch (error: any) {
    if (
      error instanceof AecMepfsResolverInputError
      || error instanceof AecMepfsResolverArtifactError
      || error instanceof AecMepfsResolverTraceNotFoundError
    ) {
      return c.json(
        resolverErrorPayload(error, 'AEC_MEPFS_RESOLVER_TRACE_ERROR', 'Resolver trace failed'),
        error.status as any
      );
    }
    return c.json({
      error: {
        code: 'AEC_MEPFS_RESOLVER_TRACE_UNAVAILABLE',
        message: error?.message || 'AEC-MEPFS resolver trace is unavailable',
      },
    }, 503);
  }
}

export function buildShadowBackbonePlacementQaPreview(report: Record<string, any>) {
  const errors: string[] = [];
  if (report.schema_version !== SHADOW_BACKBONE_PLACEMENT_QA_REPORT_SCHEMA_VERSION) {
    errors.push(
      `schema_version: expected ${SHADOW_BACKBONE_PLACEMENT_QA_REPORT_SCHEMA_VERSION}`
    );
  }
  if (report.ok !== true) {
    errors.push('placement QA report is not passing');
  }

  const summary = requireRecord(report.summary, 'summary', errors);
  const requiredCoverage = requireRecord(
    summary.required_coverage,
    'summary.required_coverage',
    errors
  );
  const safetyBoundaries = requireRecord(report.safety_boundaries, 'safety_boundaries', errors);
  const contractValidation = requireRecord(report.contract_validation, 'contract_validation', errors);
  validatePlacementQaBoundaries(safetyBoundaries, errors);
  if (contractValidation.ok !== true) {
    errors.push('contract_validation.ok: expected true');
  }
  for (const key of REQUIRED_PLACEMENT_QA_COVERAGE_KEYS) {
    if (requiredCoverage[key] !== true) {
      errors.push(`summary.required_coverage.${key}: expected true`);
    }
  }

  const casesTotal = numericField(summary.cases_total, 'summary.cases_total', errors);
  const casesPassed = numericField(summary.cases_passed, 'summary.cases_passed', errors);
  const casesFailed = numericField(summary.cases_failed, 'summary.cases_failed', errors);
  const autoAcceptCases = numericField(summary.auto_accept_cases, 'summary.auto_accept_cases', errors);
  if (casesTotal <= 0) {
    errors.push('summary.cases_total: expected at least one case');
  }
  if (casesFailed !== 0) {
    errors.push('summary.cases_failed: expected 0');
  }
  if (casesPassed !== casesTotal) {
    errors.push('summary.cases_passed: expected to equal cases_total');
  }

  if (errors.length) {
    throw new ShadowBackboneReportError(
      `Shadow backbone placement QA report failed validation: ${errors.join('; ')}`
    );
  }

  const liveMutationBoundariesClear = REQUIRED_FALSE_PLACEMENT_QA_BOUNDARIES.every(
    (key) => safetyBoundaries[key] === false
  );

  return {
    schemaVersion: SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-placement-qa-report',
    status: 'shadow_ready',
    reportOk: true,
    runId: stringField(report.run_id),
    fixturePath: stringField(report.fixture_path),
    reportPath: stringField(report.report_path),
    summary: {
      casesTotal,
      casesPassed,
      casesFailed,
      autoAcceptCases,
      proposalLevelCounts: isRecord(summary.proposal_level_counts)
        ? summary.proposal_level_counts
        : {},
      reviewQueueCounts: isRecord(summary.review_queue_counts)
        ? summary.review_queue_counts
        : {},
    },
    requiredCoverage: Object.fromEntries(
      REQUIRED_PLACEMENT_QA_COVERAGE_KEYS.map((key) => [key, requiredCoverage[key] === true])
    ),
    contractValidation: {
      ok: contractValidation.ok === true,
      warnings: Array.isArray(contractValidation.warnings)
        ? contractValidation.warnings.map((warning) => String(warning))
        : [],
    },
    boundaries: {
      shadowOnly: safetyBoundaries.shadow_only === true,
      fileBackedOnly: safetyBoundaries.file_backed_only === true,
      liveNeo4jWrites: safetyBoundaries.live_neo4j_writes === true,
      kgRebuild: safetyBoundaries.kg_rebuild === true,
      featureFlagCutover: safetyBoundaries.feature_flag_cutover === true,
      explorerDefaultAdoption: safetyBoundaries.explorer_default_adoption === true,
      protectedContentIngest: safetyBoundaries.protected_content_ingest === true,
      canonicalContentAdmission: safetyBoundaries.canonical_content_admission === true,
      liveMutationBoundariesClear,
    },
    warnings: Array.isArray(report.warnings)
      ? report.warnings.map((warning) => String(warning))
      : [],
  };
}

export function buildShadowBackboneEvidencePreview(report: Record<string, any>) {
  const errors: string[] = [];
  if (report.schema_version !== SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_SCHEMA_VERSION) {
    errors.push(
      `schema_version: expected ${SHADOW_BACKBONE_EVIDENCE_MANIFEST_REPORT_SCHEMA_VERSION}`
    );
  }
  if (report.ok !== true) {
    errors.push('evidence manifest report is not passing');
  }

  const summary = requireRecord(report.summary, 'summary', errors);
  const safetyInvariants = requireRecord(report.safety_invariants, 'safety_invariants', errors);
  const artifactResults = requireArray(report.artifact_results, 'artifact_results', errors);
  const inputHashes = requireRecord(
    report.input_file_hashes_sha256,
    'input_file_hashes_sha256',
    errors
  );
  const repoState = requireRecord(report.repo_state, 'repo_state', errors);
  for (const key of REQUIRED_TRUE_EVIDENCE_INVARIANTS) {
    if (safetyInvariants[key] !== true) {
      errors.push(`safety_invariants.${key}: expected true`);
    }
  }
  const resolverRouteEvidenceClear =
    safetyInvariants.resolver_routes_absent_or_default_off === true;
  if (!resolverRouteEvidenceClear) {
    errors.push(
      'safety_invariants.resolver_routes_absent_or_default_off: expected true'
    );
  }

  const artifactCount = numericField(summary.artifact_count, 'summary.artifact_count', errors);
  if (artifactCount !== artifactResults.length) {
    errors.push('summary.artifact_count: expected to match artifact_results length');
  }
  const evidenceFiles = artifactResults.map((value, index) => {
    const row = requireRecord(value, `artifact_results[${index}]`, errors);
    if (row.ok !== true) {
      errors.push(`artifact_results[${index}].ok: expected true`);
    }
    return {
      label: requiredStringField(row.label, `artifact_results[${index}].label`, errors),
      path: requiredStringField(row.path, `artifact_results[${index}].path`, errors),
      schemaVersion: requiredStringField(
        row.schema_version,
        `artifact_results[${index}].schema_version`,
        errors
      ),
      ok: row.ok === true,
    };
  });
  const hashEntries = Object.entries(inputHashes).filter(
    ([, value]) => typeof value === 'string' && value.length === 64
  );
  if (hashEntries.length !== Object.keys(inputHashes).length) {
    errors.push('input_file_hashes_sha256: expected SHA-256 hashes for all inputs');
  }
  const shadowGraphCounts = requireRecord(summary.shadow_graph_counts, 'summary.shadow_graph_counts', errors);
  const boundaryChecksPassed = numericField(
    summary.boundary_checks_passed,
    'summary.boundary_checks_passed',
    errors
  );
  const boundaryChecksTotal = numericField(
    summary.boundary_checks_total,
    'summary.boundary_checks_total',
    errors
  );
  const benchmarkOperationsPassed = numericField(
    summary.benchmark_operations_passed,
    'summary.benchmark_operations_passed',
    errors
  );
  const benchmarkOperationsTotal = numericField(
    summary.benchmark_operations_total,
    'summary.benchmark_operations_total',
    errors
  );
  const previewRoutesPresent = numericField(
    summary.preview_routes_present,
    'summary.preview_routes_present',
    errors
  );
  const previewRoutesRequired = numericField(
    summary.preview_routes_required,
    'summary.preview_routes_required',
    errors
  );
  const shadowGraphNodeCount = numericField(
    shadowGraphCounts.nodes,
    'summary.shadow_graph_counts.nodes',
    errors
  );
  const shadowGraphEdgeCount = numericField(
    shadowGraphCounts.edges,
    'summary.shadow_graph_counts.edges',
    errors
  );
  const shadowGraphRootCount = numericField(
    shadowGraphCounts.roots,
    'summary.shadow_graph_counts.roots',
    errors
  );
  const shadowGraphMaxDepth = numericField(
    shadowGraphCounts.max_depth,
    'summary.shadow_graph_counts.max_depth',
    errors
  );
  const routeCount = numericField(summary.route_count, 'summary.route_count', errors);
  const resolverRoutePolicy = requiredStringField(
    summary.resolver_route_policy,
    'summary.resolver_route_policy',
    errors
  );
  const benchmarkRuntimeThresholdDisposition = requiredStringField(
    summary.benchmark_runtime_threshold_disposition,
    'summary.benchmark_runtime_threshold_disposition',
    errors
  );
  if (boundaryChecksPassed !== boundaryChecksTotal) {
    errors.push('summary.boundary checks: expected all boundary checks to pass');
  }
  if (benchmarkOperationsPassed !== benchmarkOperationsTotal) {
    errors.push('summary.benchmark operations: expected all benchmark operations to pass');
  }
  if (previewRoutesPresent !== previewRoutesRequired) {
    errors.push('summary.preview routes: expected all required preview routes to be present');
  }

  const sourceWorkingTreeDirtyAtGeneration = nullableBooleanField(
    repoState.source_working_tree_dirty,
    'repo_state.source_working_tree_dirty',
    errors
  );
  const generatedEvidenceDirtyAtGeneration = nullableBooleanField(
    repoState.generated_evidence_dirty,
    'repo_state.generated_evidence_dirty',
    errors
  );
  const sourceDirtyPathCount = nullableNumericField(
    repoState.source_dirty_path_count,
    'repo_state.source_dirty_path_count',
    errors
  );
  const generatedEvidenceDirtyPathCount = nullableNumericField(
    repoState.generated_evidence_dirty_path_count,
    'repo_state.generated_evidence_dirty_path_count',
    errors
  );
  const freshnessAvailable = sourceWorkingTreeDirtyAtGeneration !== null
    && generatedEvidenceDirtyAtGeneration !== null
    && sourceDirtyPathCount !== null
    && generatedEvidenceDirtyPathCount !== null;
  if (sourceWorkingTreeDirtyAtGeneration === true) {
    errors.push('repo_state.source_working_tree_dirty: expected false');
  }
  if (sourceDirtyPathCount !== null && sourceDirtyPathCount > 0) {
    errors.push('repo_state.source_dirty_path_count: expected 0');
  }

  if (errors.length) {
    throw new ShadowBackboneReportError(
      `Shadow backbone evidence manifest failed validation: ${errors.join('; ')}`
    );
  }

  const allInvariantsClear = REQUIRED_TRUE_EVIDENCE_INVARIANTS.every(
    (key) => safetyInvariants[key] === true
  ) && resolverRouteEvidenceClear;

  return {
    schemaVersion: SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION,
    source: 'file-backed-shadow-evidence-manifest',
    status: 'shadow_ready',
    reportOk: true,
    runId: stringField(report.run_id),
    summary: {
      artifactCount,
      shadowGraphCounts: {
        nodes: shadowGraphNodeCount,
        edges: shadowGraphEdgeCount,
        roots: shadowGraphRootCount,
        maxDepth: shadowGraphMaxDepth,
      },
      boundaryChecksPassed,
      boundaryChecksTotal,
      benchmarkOperationsPassed,
      benchmarkOperationsTotal,
      routeCount,
      previewRoutesPresent,
      previewRoutesRequired,
      inputHashCount: hashEntries.length,
      resolverRoutePolicy,
      benchmarkRuntimeThresholdDisposition,
    },
    safetyInvariants: {
      allArtifactsOk: safetyInvariants.all_artifacts_ok === true,
      benchmarkShadowFileBackedOnly: safetyInvariants.benchmark_shadow_file_backed_only === true,
      boundaryAuditSafetyGreen: safetyInvariants.boundary_audit_safety_green === true,
      noRuntimePromotion: safetyInvariants.no_runtime_promotion === true,
      resolverRoutesAbsentOrDefaultOff: resolverRouteEvidenceClear,
      routeInventoryPreviewRoutesComplete: safetyInvariants.route_inventory_preview_routes_complete === true,
      runtimeThresholdsNotEvaluated: safetyInvariants.runtime_thresholds_not_evaluated === true,
      allInvariantsClear,
    },
    evidenceFiles,
    repoState: {
      gitHeadCommit: stringField(repoState.git_head_commit),
      workingTreeDirtyAtGeneration: repoState.working_tree_dirty === true,
      freshnessAvailable,
      sourceWorkingTreeDirtyAtGeneration,
      generatedEvidenceDirtyAtGeneration,
      sourceDirtyPathCount,
      generatedEvidenceDirtyPathCount,
    },
    reportPath: stringField(report.report_path),
  };
}

const DISPLAY_LABEL_LIMIT = 64;
const RULE_DISPLAY_LABEL_LIMIT = 56;
export const CONCEPT_SEMANTIC_EDGE_TYPES = [
  'RELATED_TO',
  'DEPENDS_ON',
  'APPLIES_TO',
  'PART_OF',
  'REQUIRES',
  'EXCLUDES',
  'CONSTRAINS',
  'AFFECTS',
  'INFLUENCES',
  'USED_IN',
  'EXECUTED_IN',
  'REGULATED_BY',
] as const;
export const DEFAULT_TRAVERSAL_EDGE_TYPES = [
  'HAS_CHILD',
  'BELONGS_TO',
  ...CONCEPT_SEMANTIC_EDGE_TYPES,
  'DEFINED_BY',
  'SUPPORTED_BY',
] as const;

function cypherStringList(values: readonly string[]) {
  return values.map((value) => `'${value}'`).join(', ');
}

function compactText(value: string, maxLength = DISPLAY_LABEL_LIMIT) {
  const normalized = value.replace(/\s+/g, ' ').trim();
  if (normalized.length <= maxLength) return normalized;
  return `${normalized.slice(0, maxLength - 1).trimEnd()}…`;
}

export function buildDisplayLabel(label: string, type?: string) {
  const normalized = label.replace(/\s+/g, ' ').trim();
  if (!normalized) return 'Untitled node';
  if (normalized.length <= DISPLAY_LABEL_LIMIT) return normalized;

  if (type === 'rule') {
    return `Rule · ${compactText(normalized, DISPLAY_LABEL_LIMIT - 'Rule · '.length)}`;
  }

  if (type === 'evidence_span') {
    return `Evidence · ${compactText(normalized, DISPLAY_LABEL_LIMIT - 'Evidence · '.length)}`;
  }

  return compactText(normalized);
}

export function compactRuleDisplayLabel(value: string) {
  const normalized = value
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (!normalized) return '';

  const withoutSourceRef = normalized.replace(/\s+\[[^\]]+\]$/g, '').trim();
  const parts = withoutSourceRef.split(/\s+—\s+/).map((part) => part.trim()).filter(Boolean);
  const semanticHead = parts[0] || withoutSourceRef;
  const sectionSuffix = buildRuleSectionSuffix(parts.slice(1));
  if (!sectionSuffix && semanticHead.length <= RULE_DISPLAY_LABEL_LIMIT) return semanticHead;

  const suffix = sectionSuffix ? ` · ${sectionSuffix}` : '';
  const headLimit = Math.max(16, RULE_DISPLAY_LABEL_LIMIT - suffix.length);
  if (semanticHead.length <= headLimit) return `${semanticHead}${suffix}`;

  let compact = '';
  for (const word of semanticHead.split(' ')) {
    const next = compact ? `${compact} ${word}` : word;
    if (next.length > headLimit) break;
    compact = next;
  }
  return `${compact || semanticHead.slice(0, headLimit).trim()}${suffix}`;
}

function buildRuleSectionSuffix(parts: string[]) {
  for (const part of parts) {
    const section = part.match(/^Section\s+([A-Za-z0-9.-]+)/i);
    if (section) return `Sec. ${section[1]}`;
    const article = part.match(/^Article\s+([IVXLCDM0-9.-]+)/i);
    if (article) return `Art. ${article[1]}`;
  }
  return '';
}

function appendRuleDisplaySuffix(label: string, suffix: string, maxLength = 72) {
  const suffixText = ` · ${suffix}`;
  if (`${label}${suffixText}`.length <= maxLength) return `${label}${suffixText}`;

  const headLimit = Math.max(16, maxLength - suffixText.length);
  let compact = '';
  for (const word of label.split(' ')) {
    const next = compact ? `${compact} ${word}` : word;
    if (next.length > headLimit) break;
    compact = next;
  }
  return `${compact || label.slice(0, headLimit).trim()}${suffixText}`;
}

function buildRuleDuplicateHint(id: string) {
  const sourcePart = id
    .replace(/^rule-/, '')
    .replace(/-section-.+$/i, '')
    .replace(/-\d+$/g, '');

  if (sourcePart.includes('national-building-code')) return 'NBC';
  if (sourcePart.includes('fire-code')) return 'Fire Code';
  if (sourcePart.includes('water-code')) return 'Water Code';

  const stopWords = new Set([
    'source', 'law', 'irr', 'implementing', 'rules', 'regulations', 'revised',
    'comprehensive', 'zoning', 'ordinance', 'city', 'municipality', 'of', 'the',
    'for', 'and', 'volume', 'vol', 'final', 'approved', 'version', 'printing',
    'clup', 'plan', 'use', 'land',
  ]);
  const tokens = sourcePart
    .split(/[-_]+/)
    .filter((token) => token && !stopWords.has(token.toLowerCase()));

  const hintTokens = tokens.slice(-2);
  if (hintTokens.length > 0) {
    return hintTokens.map((token) => token.replace(/\b\w/g, (char) => char.toUpperCase())).join(' ');
  }

  const ordinal = id.match(/-(\d{3})$/)?.[1];
  return ordinal ? String(Number(ordinal) + 1).padStart(2, '0') : '';
}

export function dedupeRuleDisplayLabels<T extends { id?: string; type?: string; displayLabel?: string }>(nodes: T[]) {
  const groups = new Map<string, T[]>();
  nodes.forEach((node) => {
    if (node.type !== 'rule' || !node.displayLabel) return;
    const key = node.displayLabel;
    groups.set(key, [...(groups.get(key) || []), node]);
  });

  const replacements = new Map<T, string>();
  groups.forEach((group, label) => {
    if (group.length < 2) return;

    const sortedGroup = [...group].sort((a, b) => String(a.id || '').localeCompare(String(b.id || '')));
    const hintCounts = new Map<string, number>();
    sortedGroup.forEach((node) => {
      const hint = buildRuleDuplicateHint(String(node.id || ''));
      if (hint) hintCounts.set(hint, (hintCounts.get(hint) || 0) + 1);
    });

    sortedGroup.forEach((node, index) => {
      const hint = buildRuleDuplicateHint(String(node.id || ''));
      const suffix = hint && hintCounts.get(hint) === 1
        ? hint
        : String(index + 1).padStart(2, '0');
      replacements.set(node, appendRuleDisplaySuffix(label, suffix));
    });
  });

  if (replacements.size === 0) return nodes;
  return nodes.map((node) => {
    const displayLabel = replacements.get(node);
    return displayLabel ? { ...node, displayLabel } : node;
  });
}

function humanizeIdentifier(value: string) {
  let normalized = value.replace(/\s+/g, ' ').trim();
  for (const prefix of ['concept-', 'taxonomy-', 'topic-', 'subtopic-', 'rule-', 'definition-', 'procedure-', 'exception-', 'constraint-', 'example-', 'section-', 'sec-']) {
    if (normalized.startsWith(prefix)) {
      normalized = normalized.slice(prefix.length);
      break;
    }
  }
  normalized = normalized.replace(/[-_]+/g, ' ').trim();
  if (!normalized) return '';
  return normalized.replace(/\b\w/g, (char) => char.toUpperCase());
}

export function buildRuleDisplayLabel(props: Record<string, any>, label: string) {
  const existing = props.displayLabel || props.display_label;
  if (typeof existing === 'string' && existing.trim()) {
    const compactExisting = compactRuleDisplayLabel(existing);
    if (compactExisting) return compactExisting;
  }

  const taxonomyPath = Array.isArray(props.taxonomy_path) ? props.taxonomy_path : [];
  const semanticAnchor = taxonomyPath.length > 0
    ? String(taxonomyPath[taxonomyPath.length - 1])
    : String(props.slug || props.id || '');
  const anchorLabel = humanizeIdentifier(semanticAnchor);

  if (anchorLabel) {
    return compactRuleDisplayLabel(anchorLabel.toLowerCase().endsWith('rule') ? anchorLabel : `${anchorLabel} Rule`);
  }

  return buildDisplayLabel(label, 'rule');
}

export function buildNodeDetailQuery() {
  return `
    MATCH (c) WHERE c.id = $id
    OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(e:EvidenceSpan)
    OPTIONAL MATCH (c)-[outgoingRel]->(outgoingNode)
    OPTIONAL MATCH (incomingNode)-[incomingRel]->(c)
    RETURN c,
           collect(DISTINCT e) AS evidence,
           collect(DISTINCT {rel: type(outgoingRel), other: outgoingNode, reasoning: outgoingRel.reasoning_summary, confidence: outgoingRel.confidence, assertionId: outgoingRel.assertion_id}) AS outgoing,
           collect(DISTINCT {rel: type(incomingRel), other: incomingNode, reasoning: incomingRel.reasoning_summary, confidence: incomingRel.confidence, assertionId: incomingRel.assertion_id}) AS incoming
  `;
}

export function normalizeEvidenceSpan(e: any) {
  const props = e.properties ? e.properties : e;
  return {
    id: props.id,
    quote: props.quote || props.normalized_text || props.label || 'No quote',
    document_id: props.document_id,
    document_title: props.document_title || props.source_title || props.document_name || props.document_id,
    deep_link: props.deep_link,
    confidence: props.confidence != null ? Number(props.confidence) : undefined,
  };
}

export function normalizeNode(node: any) {
  if (!node) return null;
  const props = node.properties ? node.properties : node;
  const inferredType = props.type
    || props.kind
    || (props.quote || props.normalized_text ? 'evidence_span' : null)
    || (props.source_uri && props.document_id ? 'document_version' : null)
    || 'unknown';
  const label = props.label || props.title || props.quote || props.normalized_text || props.document_title || props.document_id || props.id;
  const displayLabel = inferredType === 'rule'
    ? buildRuleDisplayLabel(props, label)
    : props.displayLabel || props.display_label || buildDisplayLabel(label, inferredType);
  return {
    id: props.id,
    label,
    displayLabel,
    type: inferredType,
    kind: props.kind,
    summary: props.summary,
    slug: props.slug,
    status: props.status,
    confidence: props.confidence != null ? Number(props.confidence) : undefined,
    aliases: props.aliases,
    taxonomy_path: props.taxonomy_path,
    createdAt: props.created_at,
    updatedAt: props.updated_at,
    radius: inferredType === 'taxonomy' ? 12 : inferredType === 'topic' ? 10 : inferredType === 'subtopic' ? 9 : inferredType === 'rule' ? 9 : inferredType === 'evidence_span' ? 6 : inferredType === 'document_version' ? 7 : 8,
  };
}

export function normalizeTaxonomyNode(node: any) {
  if (!node) return null;
  const label = String(node.label || node.id || 'Untitled taxonomy node');
  const kind = node.kind || 'taxonomy';
  return {
    id: node.id,
    label,
    displayLabel: node.displayLabel || node.display_label || buildDisplayLabel(label, kind),
    kind,
    conceptCount: Number(node.conceptCount) || 0,
  };
}

function normalizeEdge(rel: any, sourceId: string, targetId: string) {
  return {
    id: rel.assertion_id || `${sourceId}|${rel.type}|${targetId}`,
    source: sourceId,
    target: targetId,
    type: rel.type,
    reasoning: rel.reasoning_summary,
    confidence: rel.confidence != null ? Number(rel.confidence) : undefined,
    assertionId: rel.assertion_id,
  };
}

function isPresent<T>(value: T | null | undefined): value is T {
  return value != null;
}

function summarizeValue(value: any): string {
  if (value == null) return '—';
  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }
  if (neo4j.isNode(value)) {
    try {
      return JSON.stringify(value.properties);
    } catch {
      return value.properties.label || value.properties.id || '[node]';
    }
  }
  if (neo4j.isRelationship(value)) {
    try {
      return JSON.stringify({ type: value.type, properties: value.properties });
    } catch {
      return `[${value.type}]`;
    }
  }
  if (neo4j.isPath(value)) {
    try {
      return JSON.stringify({
        segments: value.segments.map((segment: any) => ({
          start: segment.start.properties,
          relationship: { type: segment.relationship.type, properties: segment.relationship.properties },
          end: segment.end.properties,
        })),
      });
    } catch {
      return `path(${value.segments.length} hops)`;
    }
  }
  if (Array.isArray(value)) {
    return value.map((item) => summarizeValue(item)).join(', ');
  }
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value);
    } catch {
      return '[object]';
    }
  }
  return String(value);
}

export function buildSearchTypeFilter(perspective?: string) {
  if (perspective === 'concepts') {
    return 'AND c.type = "concept"';
  }
  if (perspective === 'taxonomy') {
    return 'AND (c:Taxonomy OR c:Topic OR c:Subtopic OR c.type = "concept")';
  }
  if (perspective === 'evidence') {
    return 'AND (c:EvidenceSpan OR c:DocumentVersion OR c.type = "concept" OR c.type = "evidence_span" OR c.type = "document_version")';
  }
  if (perspective === 'regulatory') {
    return 'AND c.type IN ["rule", "concept"]';
  }
  return '';
}

export function buildPerspectiveQueries(id: string) {
  if (id === 'concepts') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode)
      WHERE c.type = 'concept'
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type = 'concept'
        AND b.type = 'concept'
        AND type(r) IN [${cypherStringList(CONCEPT_SEMANTIC_EDGE_TYPES)}]
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'taxonomy') {
    return {
      nodeQuery: `
      MATCH (n) WHERE n:Taxonomy OR n:Topic OR n:Subtopic OR (n:CanonicalNode AND n.type = 'taxonomy')
      RETURN n
      UNION
      MATCH (c:CanonicalNode) WHERE c.type = 'concept'
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a)-[r:HAS_CHILD|BELONGS_TO]->(b)
      WHERE (a:Taxonomy OR a:Topic OR a:Subtopic OR (a:CanonicalNode AND a.type = 'concept'))
        AND (b:Taxonomy OR b:Topic OR b:Subtopic OR (b:CanonicalNode AND b.type = 'concept'))
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'regulatory') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode) WHERE c.type IN ['rule', 'concept']
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type IN ['rule', 'concept'] AND b.type IN ['rule', 'concept']
        AND type(r) IN [${cypherStringList([...CONCEPT_SEMANTIC_EDGE_TYPES, 'DEFINED_BY'])}]
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'evidence') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode)-[:SUPPORTED_BY]->(e)
      WHERE c.type = 'concept' AND (e:EvidenceSpan OR e:DocumentVersion)
      RETURN c AS n
      UNION
      MATCH (e:EvidenceSpan)
      RETURN e AS n
      UNION
      MATCH (d:DocumentVersion)
      RETURN d AS n
      LIMIT 150
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r:SUPPORTED_BY]->(b)
      WHERE a.type = 'concept' AND (b:EvidenceSpan OR b:DocumentVersion)
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  return {
    nodeQuery: `
      MATCH (n) WHERE n:CanonicalNode OR n:Taxonomy OR n:Topic OR n:Subtopic
      RETURN n
    `,
    edgeQuery: `
      MATCH (a)-[r]->(b)
      WHERE type(r) IN [${cypherStringList(DEFAULT_TRAVERSAL_EDGE_TYPES)}]
      RETURN r, a.id AS source, b.id AS target
    `,
  };
}

const PERSPECTIVE_METADATA = [
  { id: AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID, name: 'AEC-MEPFS Backbone', description: 'File-backed taxonomy-first AEC / MEPFS backbone graph' },
  { id: AEC_MEPFS_LEGACY_PERSPECTIVE_ID, name: 'Legacy All Knowledge', description: 'Pre-cutover canonical and taxonomy graph snapshot' },
  { id: 'concepts', name: 'Concept Map', description: 'Domain concepts connected by semantic relationships' },
  { id: 'taxonomy', name: 'Taxonomy Browser', description: 'Hierarchy, classification, and attached concepts' },
  { id: 'regulatory', name: 'Regulatory Rules', description: 'Rules and directly related concepts' },
  { id: 'evidence', name: 'Evidence Map', description: 'Concept nodes with source evidence links' },
] as const;

type AecMepfsBackboneGraphArtifacts = {
  report: Record<string, any>;
  artifact: Record<string, any>;
  shadowGraph: Record<string, any> | null;
  explorerGraph: ReturnType<typeof buildAecMepfsExplorerGraph>;
  explorerIndex: AecMepfsExplorerGraphIndex | null;
  cacheKey: string;
};

let cachedAecMepfsBackboneGraphArtifacts: AecMepfsBackboneGraphArtifacts | null = null;

type AecMepfsExplorerGraph = ReturnType<typeof buildAecMepfsExplorerGraph>;
type AecMepfsExplorerNode = AecMepfsExplorerGraph['nodes'][number];
type AecMepfsExplorerEdge = AecMepfsExplorerGraph['edges'][number];

type AecMepfsSearchField = {
  node: AecMepfsExplorerNode;
  field: string;
  text: string;
  normalized: string;
};

type AecMepfsExplorerGraphIndex = {
  nodeById: Map<string, AecMepfsExplorerNode>;
  edgeById: Map<string, AecMepfsExplorerEdge>;
  nodeByPathCode: Map<string, AecMepfsExplorerNode>;
  incomingByNodeId: Map<string, AecMepfsExplorerEdge[]>;
  outgoingByNodeId: Map<string, AecMepfsExplorerEdge[]>;
  undirectedByNodeId: Map<string, AecMepfsExplorerEdge[]>;
  searchFields: AecMepfsSearchField[];
  searchCache: Map<string, ReturnType<typeof searchAecMepfsExplorerIndex>>;
};

function addEdgeToIndex(map: Map<string, AecMepfsExplorerEdge[]>, nodeId: string, edge: AecMepfsExplorerEdge) {
  const existing = map.get(nodeId);
  if (existing) {
    existing.push(edge);
  } else {
    map.set(nodeId, [edge]);
  }
}

function buildAecMepfsExplorerGraphIndex(graph: AecMepfsExplorerGraph): AecMepfsExplorerGraphIndex {
  const nodeById = new Map<string, AecMepfsExplorerNode>();
  const edgeById = new Map<string, AecMepfsExplorerEdge>();
  const nodeByPathCode = new Map<string, AecMepfsExplorerNode>();
  const incomingByNodeId = new Map<string, AecMepfsExplorerEdge[]>();
  const outgoingByNodeId = new Map<string, AecMepfsExplorerEdge[]>();
  const undirectedByNodeId = new Map<string, AecMepfsExplorerEdge[]>();
  const searchFields: AecMepfsSearchField[] = [];

  for (const node of graph.nodes) {
    nodeById.set(node.id, node);
    const aliases = Array.isArray(node.aliases) ? node.aliases : [];
    const pathCode = aliases[0] || '';
    if (pathCode) nodeByPathCode.set(pathCode, node);
    const fields = [
      { field: 'label', text: stringField(node.label) },
      { field: 'displayLabel', text: stringField(node.displayLabel) },
      { field: 'pathCode', text: pathCode },
      { field: 'id', text: node.id },
      ...aliases.map((text: string, index: number) => ({ field: index === 0 ? 'pathCode' : 'alias', text })),
    ];
    for (const field of fields) {
      const normalized = normalizeSearchTerm(field.text);
      if (!normalized) continue;
      searchFields.push({ node, field: field.field, text: field.text, normalized });
    }
  }

  for (const edge of graph.edges) {
    edgeById.set(edge.id, edge);
    addEdgeToIndex(outgoingByNodeId, edge.source, edge);
    addEdgeToIndex(incomingByNodeId, edge.target, edge);
    addEdgeToIndex(undirectedByNodeId, edge.source, edge);
    addEdgeToIndex(undirectedByNodeId, edge.target, edge);
  }

  return {
    nodeById,
    edgeById,
    nodeByPathCode,
    incomingByNodeId,
    outgoingByNodeId,
    undirectedByNodeId,
    searchFields,
    searchCache: new Map(),
  };
}

function searchAecMepfsExplorerIndex(index: AecMepfsExplorerGraphIndex, query: string, limit = 20) {
  const normalizedQuery = normalizeSearchTerm(query);
  if (!normalizedQuery) {
    throw new ShadowBackboneSearchQueryError('Shadow backbone search query is required');
  }
  const boundedLimit = Math.min(Math.max(Math.floor(limit), 1), 25);
  const cacheKey = `${normalizedQuery}:${boundedLimit}`;
  const cached = index.searchCache.get(cacheKey);
  if (cached) return cached;

  const bestByNodeId = new Map<string, {
    node: AecMepfsExplorerNode;
    field: string;
    text: string;
    rank: number;
  }>();
  for (const field of index.searchFields) {
    const rank = searchRank(field.normalized, normalizedQuery);
    if (rank === null) continue;
    const current = bestByNodeId.get(field.node.id);
    if (
      !current
      || rank > current.rank
      || (rank === current.rank && (
        compareAscii(field.field, current.field) < 0
        || (field.field === current.field && compareAscii(field.text, current.text) < 0)
      ))
    ) {
      bestByNodeId.set(field.node.id, {
        node: field.node,
        field: field.field === 'displayLabel' ? 'prefLabel' : field.field,
        text: field.text,
        rank,
      });
    }
  }

  const allResults = Array.from(bestByNodeId.values())
    .sort((a, b) => (
      b.rank - a.rank
      || (a.node.taxonomy_path?.length ?? 0) - (b.node.taxonomy_path?.length ?? 0)
      || compareAscii(a.node.aliases?.[0] || '', b.node.aliases?.[0] || '')
      || compareAscii(a.node.id, b.node.id)
    ))
    .map((match) => ({
      id: match.node.id,
      label: match.node.label,
      displayLabel: match.node.displayLabel || match.node.label,
      type: match.node.type,
      pathCode: match.node.aliases?.[0] || '',
      level: match.node.taxonomy_path?.length || 0,
      matchedField: match.field,
      matchedText: match.text,
      score: match.rank,
    }));

  const result = {
    total: allResults.length,
    returned: Math.min(allResults.length, boundedLimit),
    results: allResults.slice(0, boundedLimit),
  };
  index.searchCache.set(cacheKey, result);
  return result;
}

function compactAecMepfsExplorerGraphForRender(graph: AecMepfsExplorerGraph) {
  return {
    nodes: graph.nodes.map((node: AecMepfsExplorerNode) => ({
      id: node.id,
      label: node.label,
      ...(node.displayLabel && node.displayLabel !== node.label ? { displayLabel: node.displayLabel } : {}),
      type: node.type,
      confidence: node.confidence,
      aliases: node.aliases,
      taxonomy_path: node.taxonomy_path,
      radius: node.radius,
    })),
    edges: graph.edges.map((edge: AecMepfsExplorerEdge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: edge.type,
    })),
  };
}

function shadowBackboneFileCacheKey(paths: Array<string | null>) {
  return paths.map((path) => {
    if (!path) return 'none';
    if (!existsSync(path)) return `${path}:missing`;
    const stat = statSync(path);
    return `${path}:${stat.size}:${stat.mtimeMs}`;
  }).join('|');
}

async function readAecMepfsBackboneGraphArtifacts(): Promise<AecMepfsBackboneGraphArtifacts> {
  const reportPath = resolveShadowBackboneReportPath();
  const report = await readShadowJsonObject(reportPath, 'shadow backbone consumer report');
  const artifactPath = resolveShadowBackboneArtifactPath(report);
  const shadowGraphPath = resolveShadowBackboneGraphPath(report);
  const admittedRelationshipsPath = canonicalStewardshipPaths(process.cwd()).admittedRelationships;
  const cacheKey = shadowBackboneFileCacheKey([reportPath, artifactPath, shadowGraphPath, admittedRelationshipsPath]);

  if (cachedAecMepfsBackboneGraphArtifacts?.cacheKey === cacheKey) {
    return cachedAecMepfsBackboneGraphArtifacts;
  }

  const artifact = await readShadowJsonObject(artifactPath, 'shadow backbone staging artifact');
  const shadowGraph = shadowGraphPath
    ? await readShadowJsonObject(shadowGraphPath, 'shadow backbone graph artifact')
    : null;
  const explorerGraph = buildAecMepfsExplorerGraph(report, artifact, shadowGraph);
  cachedAecMepfsBackboneGraphArtifacts = {
    report,
    artifact,
    shadowGraph,
    explorerGraph,
    explorerIndex: null,
    cacheKey,
  };
  return cachedAecMepfsBackboneGraphArtifacts;
}

function getAecMepfsExplorerGraphIndex(artifacts: AecMepfsBackboneGraphArtifacts) {
  if (!artifacts.explorerIndex) {
    artifacts.explorerIndex = buildAecMepfsExplorerGraphIndex(artifacts.explorerGraph);
  }
  return artifacts.explorerIndex;
}

async function getPerspectiveNodeCount(id: string): Promise<number | undefined> {
  if (id === AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID) {
    const report = await readShadowBackboneConsumerReport();
    const shadowGraphCounts = isRecord(report.shadow_graph_counts) ? report.shadow_graph_counts : {};
    const reportCounts = isRecord(report.counts) ? report.counts : {};
    return Number(shadowGraphCounts.nodes ?? reportCounts.backbone_nodes ?? 0);
  }
  const { nodeQuery } = buildPerspectiveQueries(id);
  const records = await runQuery<{ nodeCount: number }>(`
    CALL {
      ${nodeQuery}
    }
    WITH n AS node
    WHERE node IS NOT NULL AND node.id IS NOT NULL
    RETURN count(DISTINCT node.id) AS nodeCount
  `);
  return Number(records[0]?.nodeCount ?? 0);
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------
const app = new Hono();

app.use(cors({ origin: '*' }));

// Health check
app.get('/health', async (c) => {
  let neo4jStatus = 'not checked';
  let aecMepfsStatus = 'unavailable';
  const shouldCheckNeo4j = c.req.query('neo4j') === '1';

  try {
    const report = await readShadowBackboneConsumerReport();
    const graphCounts = isRecord(report.shadow_graph_counts) ? report.shadow_graph_counts : {};
    aecMepfsStatus = report.ok === true && Number(graphCounts.nodes ?? 0) > 0
      ? 'ready'
      : 'unavailable';
  } catch (e: any) {
    aecMepfsStatus = e?.message || 'unavailable';
  }

  if (shouldCheckNeo4j) {
    try {
      await driver.verifyConnectivity();
      neo4jStatus = 'connected';
    } catch (e: any) {
      neo4jStatus = e?.message || 'unavailable';
    }
  }

  if (aecMepfsStatus === 'ready' || neo4jStatus === 'connected') {
    return c.json({ status: 'ok', neo4j: neo4jStatus, aecMepfs: aecMepfsStatus });
  }

  return c.json({ status: 'error', neo4j: neo4jStatus, aecMepfs: aecMepfsStatus }, 500);
});

// GET /v2/backbone
app.get('/v2/backbone', async (c) => {
  try {
    const report = await readShadowBackboneConsumerReport();
    return c.json(buildShadowBackboneSummary(report));
  } catch (error: any) {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_REPORT_UNAVAILABLE',
        message: error?.message || 'Shadow backbone report is unavailable',
      },
    }, 503);
  }
});

// GET /v2/backbone/taxonomy
app.get('/v2/backbone/taxonomy', async (c) => {
  try {
    const report = await readShadowBackboneConsumerReport();
    const artifact = await readShadowBackboneStagingArtifact(report);
    const shadowGraph = await readShadowBackboneGraphArtifact(report);
    return c.json(buildShadowBackboneTaxonomyPreview(report, artifact, shadowGraph));
  } catch (error: any) {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_TAXONOMY_UNAVAILABLE',
        message: error?.message || 'Shadow backbone taxonomy preview is unavailable',
      },
    }, 503);
  }
});

// GET /v2/backbone/node/:id
app.get('/v2/backbone/node/:id', async (c) => {
  let nodeId: string;
  try {
    nodeId = decodeURIComponent(c.req.param('id'));
  } catch {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_NODE_ID_INVALID',
        message: 'Shadow backbone node id is malformed',
      },
    }, 400);
  }

  try {
    const report = await readShadowBackboneConsumerReport();
    const artifact = await readShadowBackboneStagingArtifact(report);
    const shadowGraph = await readShadowBackboneGraphArtifact(report);
    return c.json(buildShadowBackboneNodePreview(report, artifact, shadowGraph, nodeId));
  } catch (error: any) {
    if (error instanceof ShadowBackboneNodeNotFoundError) {
      return c.json({
        error: {
          code: error.code,
          message: error.message,
        },
      }, 404);
    }
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_NODE_UNAVAILABLE',
        message: error?.message || 'Shadow backbone node preview is unavailable',
      },
    }, 503);
  }
});

// GET /v2/search
app.get('/v2/search', async (c) => {
  try {
    const report = await readShadowBackboneConsumerReport();
    const artifact = await readShadowBackboneStagingArtifact(report);
    const shadowGraph = await readShadowBackboneGraphArtifact(report);
    return c.json(buildShadowBackboneSearchPreview(
      report,
      artifact,
      shadowGraph,
      c.req.query('q') || '',
      parseSearchLimit(c.req.query('limit'))
    ));
  } catch (error: any) {
    if (error instanceof ShadowBackboneSearchQueryError) {
      return c.json({
        error: {
          code: error.code,
          message: error.message,
        },
      }, 400);
    }
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_SEARCH_UNAVAILABLE',
        message: error?.message || 'Shadow backbone search preview is unavailable',
      },
    }, 503);
  }
});

// GET /v2/sources/:source_id
app.get('/v2/sources/:source_id', async (c) => {
  let sourceId = '';
  try {
    sourceId = decodeURIComponent(c.req.param('source_id') || '');
  } catch {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_SOURCE_ID_INVALID',
        message: 'Shadow backbone source id is not valid URI encoding',
      },
    }, 400);
  }

  try {
    const report = await readShadowBackboneConsumerReport();
    const artifact = await readShadowBackboneStagingArtifact(report);
    return c.json(buildShadowBackboneSourcePreview(report, artifact, sourceId));
  } catch (error: any) {
    if (error instanceof ShadowBackboneSourceIdError) {
      return c.json({
        error: {
          code: error.code,
          message: error.message,
        },
      }, 400);
    }
    if (error instanceof ShadowBackboneSourceNotFoundError) {
      return c.json({
        error: {
          code: error.code,
          message: error.message,
        },
      }, 404);
    }
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_SOURCE_UNAVAILABLE',
        message: error?.message || 'Shadow backbone source preview is unavailable',
      },
    }, 503);
  }
});

// GET /v2/backbone/placement-qa
app.get('/v2/backbone/placement-qa', async (c) => {
  try {
    const report = await readShadowBackbonePlacementQaReport();
    return c.json(buildShadowBackbonePlacementQaPreview(report));
  } catch (error: any) {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_PLACEMENT_QA_UNAVAILABLE',
        message: error?.message || 'Shadow backbone placement QA report is unavailable',
      },
    }, 503);
  }
});

// GET /v2/backbone/evidence
app.get('/v2/backbone/evidence', async (c) => {
  try {
    const report = await readShadowBackboneEvidenceManifestReport();
    return c.json(buildShadowBackboneEvidencePreview(report));
  } catch (error: any) {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_EVIDENCE_UNAVAILABLE',
        message: error?.message || 'Shadow backbone evidence manifest is unavailable',
      },
    }, 503);
  }
});

// POST /v2/resolve and GET /v2/resolve/trace/:trace_id are enabled by
// default for the prelaunch file-backed AEC-MEPFS runtime. Set
// VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME=0, false, no, off, or disabled to
// roll back the route surface without Neo4j/KG/protected payload changes.
if (isAecMepfsResolverRuntimeEnabled()) {
  app.post('/v2/resolve', handleAecMepfsResolverRequest);
  app.get('/v2/resolve/trace/:trace_id', handleAecMepfsResolverTraceRequest);
}

// GET /search
app.get('/search', async (c) => {
  const q = c.req.query('q') || '';
  const perspective = c.req.query('perspective');
  const limit = Math.min(parseInt(c.req.query('limit') || '20'), 100);

  if (!q.trim() || q.length < 2) return c.json({ results: [] });

  if (perspective === AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID) {
    try {
      const artifacts = await readAecMepfsBackboneGraphArtifacts();
      const explorerIndex = getAecMepfsExplorerGraphIndex(artifacts);
      const preview = searchAecMepfsExplorerIndex(explorerIndex, q, limit);
      const baseResults = preview.results.map((row: any) => ({
        kind: 'node',
        id: row.id,
        label: row.label,
        displayLabel: row.displayLabel,
        type: aecMepfsNodeType(row.level, row.pathCode),
        matchType: row.matchedField,
        matchedField: row.matchedField,
      }));
      const canonicalAliasRecords = readCanonicalAliases(repoRoot);
      const canonicalRedirectRecords = readCanonicalRedirects(repoRoot);
      const canonicalDecisionRecords = readCanonicalDecisions(repoRoot);
      const hasCanonicalStewardship = canonicalAliasRecords.length > 0 || canonicalRedirectRecords.length > 0 || canonicalDecisionRecords.length > 0;
      const canonicalCandidates = hasCanonicalStewardship
        ? canonicalPreferredSearch(
          repoRoot,
          artifacts.explorerGraph.nodes,
          q,
          buildDuplicateCandidateGroups(artifacts.explorerGraph.nodes, artifacts.explorerGraph.edges, readResourceLayerData(repoRoot), canonicalDecisionRecords),
          limit,
        )
        : [];
      const canonicalResults = canonicalCandidates.filter((result: any) => {
        const canonicalStatus = String(result.canonicalStatus ?? '');
        return Boolean(
          result.reviewState
          || result.ambiguity
          || (Array.isArray(result.duplicateGroupIds) && result.duplicateGroupIds.length > 0)
          || canonicalStatus === 'merged_into'
          || canonicalStatus === 'alias_of'
          || canonicalStatus === 'deprecated'
          || (canonicalAliasRecords.length > 0 && result.matchType === 'canonical_alias')
        );
      });
      const seen = new Set<string>();
      const results = [...canonicalResults, ...baseResults].filter((result: any) => {
        if (seen.has(result.id)) return false;
        seen.add(result.id);
        return true;
      }).slice(0, limit);
      return c.json({
        results,
      });
    } catch (error: any) {
      if (error instanceof ShadowBackboneSearchQueryError) {
        return c.json({ error: { code: error.code, message: error.message } }, 400);
      }
      return c.json({
        error: {
          code: 'AEC_MEPFS_SEARCH_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS search is unavailable',
        },
      }, 503);
    }
  }

  const typeFilter = buildSearchTypeFilter(perspective);

  const records = await runQuery(`
    MATCH (c)
    WHERE (c:CanonicalNode OR c:Taxonomy OR c:Topic OR c:Subtopic OR c:EvidenceSpan OR c:DocumentVersion)
      AND (
        toLower(coalesce(c.label, c.title, c.quote, c.normalized_text, c.id)) CONTAINS $q
        OR toLower(c.id) CONTAINS $q
        OR toLower(coalesce(c.slug, '')) CONTAINS $q
        OR any(alias IN coalesce(c.aliases, []) WHERE toLower(alias) CONTAINS $q)
      )
      ${typeFilter}
    RETURN c.id AS id,
           coalesce(c.label, c.title, c.quote, c.normalized_text, c.id) AS label,
           c.display_label AS display_label,
           c.taxonomy_path AS taxonomy_path,
           coalesce(c.type, c.kind, CASE WHEN c:EvidenceSpan THEN 'evidence_span' WHEN c:DocumentVersion THEN 'document_version' ELSE null END) AS type,
           c.kind AS kind,
           c.slug AS slug,
           c.aliases AS aliases
    LIMIT $limit
  `, { q: q.toLowerCase(), limit: neo4j.int(limit) });

  const results = dedupeRuleDisplayLabels(records.map((r) => {
    const label = String(r.label ?? r.id ?? 'Unknown node');
    const normalizedQuery = q.toLowerCase();
    const aliases = Array.isArray(r.aliases)
      ? r.aliases.map((alias: any) => String(alias).toLowerCase())
      : [];
    const slug = typeof r.slug === 'string' ? r.slug.toLowerCase() : '';
    const matchedField = label.toLowerCase().includes(normalizedQuery)
      ? 'label'
      : aliases.some((alias: string) => alias.includes(normalizedQuery))
        ? 'alias'
        : slug.includes(normalizedQuery)
          ? 'slug'
          : 'id';

    return {
      kind: 'node' as const,
      id: r.id,
      label,
      displayLabel: r.type === 'rule'
        ? buildRuleDisplayLabel(r, label)
        : r.display_label || buildDisplayLabel(label, r.type || r.kind || 'unknown'),
      type: r.type || r.kind || 'unknown',
      matchType: matchedField,
      matchedField,
    };
  }));

  return c.json({ results });
});

const RESOURCE_ELIGIBLE_NODE_TYPES = new Set([
  'concept',
  'rule',
  'definition',
  'procedure',
  'exception',
  'evidence',
  'evidence_span',
  'document',
  'document_version',
]);

function parseResourceLimit(value: string | undefined) {
  const parsed = Number.parseInt(value || '8', 10);
  if (!Number.isFinite(parsed)) return 8;
  return Math.max(1, Math.min(8, parsed));
}

function isTruthyQuery(value: string | undefined) {
  return value === '1' || value === 'true' || value === 'yes';
}

function parseReviewFilters(query: (name: string) => string | undefined): ReviewFilters {
  const limit = query('limit');
  const offset = query('offset');
  return {
    status: query('status'),
    nodeId: query('nodeId'),
    resourceId: query('resourceId'),
    sourceFamily: query('sourceFamily'),
    authorityTier: query('authorityTier'),
    issueType: query('issueType'),
    limit: limit === undefined ? undefined : Number.parseInt(limit, 10),
    offset: offset === undefined ? undefined : Number.parseInt(offset, 10),
  };
}

function parseCanonicalFilters(query: (name: string) => string | undefined): DuplicateFilters {
  const limit = query('limit');
  const offset = query('offset');
  const bool = (value: string | undefined) => value === '1' || value === 'true' || value === 'yes';
  return {
    status: query('status'),
    riskLevel: query('riskLevel'),
    query: query('query') || query('q') || query('label'),
    taxonomy: query('taxonomy'),
    nodeType: query('nodeType'),
    hasResourceLinks: bool(query('hasResourceLinks')),
    hasHighEdgeCount: bool(query('hasHighEdgeCount')),
    concreteOnly: bool(query('concreteOnly')),
    safeCandidatesOnly: bool(query('safeCandidatesOnly')),
    manualReviewOnly: bool(query('manualReviewOnly')),
    priorityBand: query('priorityBand') as CanonicalPriorityBand | undefined,
    limit: limit === undefined ? undefined : Number.parseInt(limit, 10),
    offset: offset === undefined ? undefined : Number.parseInt(offset, 10),
  };
}

async function parseReviewDecisionBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Review decision request body must be a JSON object');
    }
    if (typeof body.decision !== 'string' || !body.decision.trim()) {
      throw new ResourceReviewError('review decision body requires a decision string');
    }
    const allowedDecisions = new Set([
      'accept', 'reject', 'needs_review', 'downgrade', 'reopen',
      'accept_as_resource', 'link_to_node', 'reject_candidate', 'needs_more_context', 'mark_duplicate', 'hold',
      'admit_as_resource', 'reject_local_file', 'ignore',
    ]);
    if (!allowedDecisions.has(body.decision)) throw new ResourceReviewError(`unsupported review decision: ${body.decision}`);
    if (body.reviewer !== undefined && typeof body.reviewer !== 'string') throw new ResourceReviewError('reviewer must be a string');
    if (body.rationale !== undefined && typeof body.rationale !== 'string') throw new ResourceReviewError('rationale must be a string');
    if (body.notes !== undefined && typeof body.notes !== 'string') throw new ResourceReviewError('notes must be a string');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    for (const refField of ['sectionRefs', 'chapterRefs', 'pageRefs']) {
      if (body[refField] !== undefined && (!Array.isArray(body[refField]) || body[refField].some((value: unknown) => typeof value !== 'string'))) {
        throw new ResourceReviewError(`${refField} must be an array of strings`);
      }
    }
    if (body.authorityTier !== undefined && ![1, 2, 3, 4, 5].includes(Number(body.authorityTier))) throw new ResourceReviewError('authorityTier must be 1..5');
    if (body.authorityScore !== undefined && (typeof body.authorityScore !== 'number' || body.authorityScore < 0 || body.authorityScore > 1)) throw new ResourceReviewError('authorityScore must be a number between 0 and 1');
    for (const objectField of ['resourceFields', 'linkFields', 'sourceRights', 'admissionProvenance']) {
      if (body[objectField] !== undefined && (!body[objectField] || typeof body[objectField] !== 'object' || Array.isArray(body[objectField]))) {
        throw new ResourceReviewError(`${objectField} must be an object`);
      }
    }
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Review decision request body must be valid JSON');
  }
}

async function parseStandardsContextDecisionBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Standards context request body must be a JSON object');
    }
    const allowedDecisions = new Set([
      'keep_needs_review',
      'update_context_partial',
      'update_context_complete',
      'mark_context_not_required',
      'reject_context_update',
      'defer_context_review',
      'promote_if_context_complete',
      'demote_to_needs_review',
    ]);
    if (typeof body.decision !== 'string' || !allowedDecisions.has(body.decision)) {
      throw new ResourceReviewError(`unsupported standards context decision: ${String(body.decision)}`);
    }
    for (const textField of ['reviewer', 'rationale', 'notes', 'edition', 'version', 'amendment', 'errata', 'jurisdiction', 'geographicScope', 'adoptionStatus', 'codeCycle', 'applicabilityNote', 'sourceOfContext', 'sourceUrl', 'sourceNote']) {
      if (body[textField] !== undefined && typeof body[textField] !== 'string') throw new ResourceReviewError(`${textField} must be a string`);
    }
    for (const refField of ['sectionRefs', 'chapterRefs', 'pageRefs', 'fragmentRefs']) {
      if (body[refField] !== undefined && (!Array.isArray(body[refField]) || body[refField].some((value: unknown) => typeof value !== 'string'))) {
        throw new ResourceReviewError(`${refField} must be an array of strings`);
      }
    }
    if (body.publicationYear !== undefined && typeof body.publicationYear !== 'number') throw new ResourceReviewError('publicationYear must be a number');
    if (body.confidence !== undefined && !['low', 'medium', 'high'].includes(body.confidence)) throw new ResourceReviewError('confidence must be low, medium, or high');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Standards context request body must be valid JSON');
  }
}

async function parseCanonicalDecisionBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical decision request body must be a JSON object');
    }
    if (typeof body.decisionType !== 'string' || !body.decisionType.trim()) {
      throw new ResourceReviewError('canonical decision body requires decisionType');
    }
    const allowedDecisionTypes = new Set([
      'MERGE_INTO_CANONICAL',
      'ALIAS_TO_CANONICAL',
      'KEEP_SEPARATE',
      'NEEDS_HUMAN_REVIEW',
      'REJECT_DUPLICATE_CANDIDATE',
      'SPLIT_OR_RETYPE_NEEDED',
      'GOVERNED_DISAMBIGUATION',
      'RELATED_SPECIALIZATION',
      'CROSS_DOMAIN_EQUIVALENCE',
      'CANONICAL_LABEL_CLARIFICATION',
      'DISAMBIGUATED_KEEP_SEPARATE',
    ]);
    if (!allowedDecisionTypes.has(body.decisionType)) throw new ResourceReviewError(`unsupported canonical decisionType: ${body.decisionType}`);
    if (body.reviewer !== undefined && typeof body.reviewer !== 'string') throw new ResourceReviewError('reviewer must be a string');
    if (body.rationale !== undefined && typeof body.rationale !== 'string') throw new ResourceReviewError('rationale must be a string');
    if (body.notes !== undefined && typeof body.notes !== 'string') throw new ResourceReviewError('notes must be a string');
    if (body.canonicalNodeId !== undefined && typeof body.canonicalNodeId !== 'string') throw new ResourceReviewError('canonicalNodeId must be a string');
    if (body.highRiskAcknowledged !== undefined && typeof body.highRiskAcknowledged !== 'boolean') throw new ResourceReviewError('highRiskAcknowledged must be a boolean');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    if (body.sourceNodeIds !== undefined && (!Array.isArray(body.sourceNodeIds) || body.sourceNodeIds.some((value: unknown) => typeof value !== 'string'))) {
      throw new ResourceReviewError('sourceNodeIds must be an array of strings');
    }
    if (body.searchDisambiguationText !== undefined && typeof body.searchDisambiguationText !== 'string') throw new ResourceReviewError('searchDisambiguationText must be a string');
    if (body.proposedRelationshipAdds !== undefined && (!Array.isArray(body.proposedRelationshipAdds) || body.proposedRelationshipAdds.some((value: unknown) => !value || typeof value !== 'object' || Array.isArray(value)))) {
      throw new ResourceReviewError('proposedRelationshipAdds must be an array of objects');
    }
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical decision request body must be valid JSON');
  }
}

async function parseCanonicalRemediationBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical remediation request body must be a JSON object');
    }
    if (body.status !== undefined && !['open', 'in_progress', 'resolved', 'waived'].includes(body.status)) throw new ResourceReviewError('status must be open, in_progress, resolved, or waived');
    if (body.reviewer !== undefined && typeof body.reviewer !== 'string') throw new ResourceReviewError('reviewer must be a string');
    if (body.resolutionNotes !== undefined && typeof body.resolutionNotes !== 'string') throw new ResourceReviewError('resolutionNotes must be a string');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical remediation request body must be valid JSON');
  }
}

async function parseCanonicalApprovalBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical approval request body must be a JSON object');
    }
    if (body.approvedBy !== undefined && typeof body.approvedBy !== 'string') throw new ResourceReviewError('approvedBy must be a string');
    if (body.reviewerRole !== undefined && typeof body.reviewerRole !== 'string') throw new ResourceReviewError('reviewerRole must be a string');
    if (body.approvalSource !== undefined && !['dev_admin_ui', 'api', 'test_fixture', 'imported_decision_record', 'human_record', 'user_supplied_standing_steward_approval'].includes(body.approvalSource)) {
      throw new ResourceReviewError('approvalSource is not supported');
    }
    if (body.approvalRationale !== undefined && typeof body.approvalRationale !== 'string') throw new ResourceReviewError('approvalRationale must be a string');
    if (body.rollbackPlan !== undefined && typeof body.rollbackPlan !== 'string') throw new ResourceReviewError('rollbackPlan must be a string');
    if (body.kimiReviewSummary !== undefined && typeof body.kimiReviewSummary !== 'string') throw new ResourceReviewError('kimiReviewSummary must be a string');
    if (body.riskAcknowledgment !== undefined && typeof body.riskAcknowledgment !== 'boolean') throw new ResourceReviewError('riskAcknowledgment must be a boolean');
    if (body.mutationScope !== undefined && !['metadata_only', 'non_destructive_edge_admission', 'alias_only', 'redirect', 'tombstone', 'destructive_merge'].includes(body.mutationScope)) {
      throw new ResourceReviewError('mutationScope is not supported');
    }
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical approval request body must be valid JSON');
  }
}

async function parseCanonicalApprovalRejectionBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical approval rejection request body must be a JSON object');
    }
    if (body.approvedBy !== undefined && typeof body.approvedBy !== 'string') throw new ResourceReviewError('approvedBy must be a string');
    if (body.reviewerRole !== undefined && typeof body.reviewerRole !== 'string') throw new ResourceReviewError('reviewerRole must be a string');
    if (body.rejectionRationale !== undefined && typeof body.rejectionRationale !== 'string') throw new ResourceReviewError('rejectionRationale must be a string');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical approval rejection request body must be valid JSON');
  }
}

async function parseCanonicalP1PacketBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical P1 packet request body must be a JSON object');
    }
    if (body.limit !== undefined && typeof body.limit !== 'number') throw new ResourceReviewError('limit must be a number');
    if (body.reviewer !== undefined && typeof body.reviewer !== 'string') throw new ResourceReviewError('reviewer must be a string');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical P1 packet request body must be valid JSON');
  }
}

async function parseCanonicalP1PacketReviewBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical P1 packet review request body must be a JSON object');
    }
    const allowedStatuses = new Set(['unreviewed', 'kimi_review_requested', 'kimi_reviewed', 'human_review_needed', 'human_reviewed', 'rejected', 'deferred']);
    const allowedReviewerTypes = new Set(['kimi', 'human', 'codex', 'system']);
    const allowedSources = new Set(['kimi', 'manual_entry', 'imported_review', 'test_fixture']);
    const allowedRiskLevels = new Set(['low', 'medium', 'high', 'blocked']);
    if (body.ontologyReviewStatus !== undefined && (typeof body.ontologyReviewStatus !== 'string' || !allowedStatuses.has(body.ontologyReviewStatus))) {
      throw new ResourceReviewError(`unsupported ontologyReviewStatus: ${String(body.ontologyReviewStatus)}`);
    }
    if (body.reviewerType !== undefined && (typeof body.reviewerType !== 'string' || !allowedReviewerTypes.has(body.reviewerType))) {
      throw new ResourceReviewError(`unsupported reviewerType: ${String(body.reviewerType)}`);
    }
    if (body.source !== undefined && (typeof body.source !== 'string' || !allowedSources.has(body.source))) {
      throw new ResourceReviewError(`unsupported review source: ${String(body.source)}`);
    }
    if (body.reviewRiskLevel !== undefined && (typeof body.reviewRiskLevel !== 'string' || !allowedRiskLevels.has(body.reviewRiskLevel))) {
      throw new ResourceReviewError(`unsupported reviewRiskLevel: ${String(body.reviewRiskLevel)}`);
    }
    for (const textField of ['reviewedBy', 'reviewSummary', 'recommendedAction', 'nextAction', 'notes']) {
      if (body[textField] !== undefined && typeof body[textField] !== 'string') throw new ResourceReviewError(`${textField} must be a string`);
    }
    for (const listField of ['acceptedSuggestions', 'rejectedSuggestions', 'deferredSuggestions']) {
      if (body[listField] !== undefined) {
        const value = body[listField];
        if (typeof value !== 'string' && (!Array.isArray(value) || value.some((entry: unknown) => typeof entry !== 'string'))) {
          throw new ResourceReviewError(`${listField} must be a string or an array of strings`);
        }
      }
    }
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical P1 packet review request body must be valid JSON');
  }
}

async function parseCanonicalBatchBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new ResourceReviewError('Canonical batch request body must be a JSON object');
    }
    if (body.name !== undefined && typeof body.name !== 'string') throw new ResourceReviewError('name must be a string');
    if (body.reviewer !== undefined && typeof body.reviewer !== 'string') throw new ResourceReviewError('reviewer must be a string');
    if (body.rationale !== undefined && typeof body.rationale !== 'string') throw new ResourceReviewError('rationale must be a string');
    if (body.notes !== undefined && typeof body.notes !== 'string') throw new ResourceReviewError('notes must be a string');
    if (body.action !== undefined && typeof body.action !== 'string') throw new ResourceReviewError('action must be a string');
    if (body.priorityBand !== undefined && !['P0', 'P1', 'P2', 'P3', 'BLOCKED'].includes(body.priorityBand)) throw new ResourceReviewError('priorityBand must be P0, P1, P2, P3, or BLOCKED');
    if (body.tags !== undefined && (!Array.isArray(body.tags) || body.tags.some((value: unknown) => typeof value !== 'string'))) {
      throw new ResourceReviewError('tags must be an array of strings');
    }
    if (body.filters !== undefined && (!body.filters || typeof body.filters !== 'object' || Array.isArray(body.filters))) {
      throw new ResourceReviewError('filters must be an object');
    }
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical batch request body must be valid JSON');
  }
}

async function parseCanonicalRollbackBody(c: any) {
  try {
    const body = await c.req.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) throw new ResourceReviewError('Canonical rollback request body must be a JSON object');
    if (typeof body.reviewer !== 'string' || !body.reviewer.trim()) throw new ResourceReviewError('rollback reviewer is required');
    if (typeof body.rationale !== 'string' || !body.rationale.trim()) throw new ResourceReviewError('rollback rationale is required');
    if (body.dryRun !== undefined && typeof body.dryRun !== 'boolean') throw new ResourceReviewError('dryRun must be a boolean');
    if (body.apply !== undefined && typeof body.apply !== 'boolean') throw new ResourceReviewError('apply must be a boolean');
    return body;
  } catch (error) {
    if (error instanceof ResourceReviewError) throw error;
    throw new ResourceReviewError('Canonical rollback request body must be valid JSON');
  }
}

function isLocalDevAdminRequest(c: any) {
  const requestUrl = new URL(c.req.url);
  const hostname = requestUrl.hostname.toLowerCase();
  const configuredToken = process.env.VITRUVIUS_ADMIN_TOKEN;
  const suppliedToken = c.req.header('x-vitruvius-admin-token') || c.req.header('authorization')?.replace(/^Bearer\s+/i, '');
  if (configuredToken && suppliedToken) {
    const configured = Buffer.from(configuredToken);
    const supplied = Buffer.from(suppliedToken);
    if (configured.length === supplied.length && timingSafeEqual(configured, supplied)) return true;
  }
  const isLocal = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
  if (process.env.NODE_ENV === 'production') {
    return process.env.VITRUVIUS_ENABLE_DEV_ADMIN === 'true' && isLocal;
  }
  return process.env.NODE_ENV === 'test' || process.env.VITRUVIUS_ENABLE_DEV_ADMIN === 'true' || isLocal;
}

function requireLocalDevAdmin(c: any) {
  if (!isLocalDevAdminRequest(c)) {
    throw new ResourceReviewError('admin mutation route is disabled: use local/dev mode or configure VITRUVIUS_ADMIN_TOKEN', 403);
  }
}

function reviewErrorResponse(c: any, error: any) {
  if (error instanceof ResourceReviewError) {
    return c.json({
      error: {
        code: 'RESOURCE_REVIEW_DECISION_INVALID',
        message: error.message,
        details: error.details,
      },
    }, error.status);
  }
  return c.json({
    error: {
      code: 'RESOURCE_REVIEW_UNAVAILABLE',
      message: error?.message || 'Resource review workflow is unavailable',
    },
  }, 500);
}

// GET /node/:id/resources
app.get('/node/:id/resources', async (c) => {
  const id = c.req.param('id');
  const includeCandidates = isTruthyQuery(c.req.query('includeCandidates'));
  const limit = parseResourceLimit(c.req.query('limit'));
  const mode = c.req.query('mode') || 'learner';

  if (mode === 'reviewer') {
    requireLocalDevAdmin(c);
  }

  if (isLikelyAecMepfsBackboneNodeId(id)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      if (!explorerIndex.nodeById.has(id)) {
        return c.json({ error: { code: 'NODE_NOT_FOUND', message: `Node '${id}' not found` } }, 404);
      }
    } catch (error: any) {
      if (error instanceof ShadowBackboneNodeNotFoundError) {
        return c.json({ error: { code: error.code, message: error.message } }, 404);
      }
      return c.json({
        error: {
          code: 'AEC_MEPFS_NODE_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS node resources are unavailable',
        },
      }, 503);
    }
  }

  return c.json({
    nodeId: id,
    resources: getNodeResources(repoRoot, id, { includeCandidates, includeReviewer: mode === 'reviewer', limit }),
    displayPolicy: {
      mode,
      limit,
      learnerEligibleOnly: mode !== 'reviewer',
    },
  });
});

// GET /node/:id/neighborhood
app.get('/node/:id/neighborhood', async (c) => {
  const id = c.req.param('id');
  const relTypes = c.req.query('relTypes')?.split(',').map((value) => value.trim()).filter(Boolean);
  const directionQuery = c.req.query('direction');
  const direction = directionQuery === 'in' || directionQuery === 'out' || directionQuery === 'both'
    ? directionQuery
    : 'both';
  const depth = Math.min(Math.max(parseInt(c.req.query('depth') || '1', 10) || 1, 1), 3);
  const limit = Math.min(Math.max(parseInt(c.req.query('limit') || '500', 10) || 500, 1), 1000);
  const includeHierarchyEdges = c.req.query('includeHierarchyEdges') !== 'false';
  const includeSemanticEdges = c.req.query('includeSemanticEdges') !== 'false';

  if (isLikelyAecMepfsBackboneNodeId(id)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      return c.json(buildAecMepfsNeighborhoodResultFromIndex(explorerIndex, id, {
        relTypes,
        direction,
        depth,
        limit,
        includeHierarchyEdges,
        includeSemanticEdges,
      }));
    } catch (error: any) {
      if (error instanceof ShadowBackboneNodeNotFoundError) {
        return c.json({ error: { code: error.code, message: error.message } }, 404);
      }
      return c.json({
        error: {
          code: 'AEC_MEPFS_NEIGHBORHOOD_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS normalized neighborhood is unavailable',
        },
      }, 503);
    }
  }

  return c.json({
    error: {
      code: 'GRAPH_NEIGHBORHOOD_UNSUPPORTED',
      message: 'Normalized graph neighborhoods are currently implemented for file-backed AEC-MEPFS nodes.',
    },
  }, 400);
});

async function canonicalGraphContext(filters: DuplicateFilters = {}) {
  const { explorerGraph } = await readAecMepfsBackboneGraphArtifacts();
  const resourceData = readResourceLayerData(repoRoot);
  const decisions = readCanonicalDecisions(repoRoot);
  const unfilteredGroups = applyPriorityOverrides(repoRoot, buildDuplicateCandidateGroups(explorerGraph.nodes, explorerGraph.edges, resourceData, decisions));
  const groups = applyPriorityOverrides(repoRoot, buildDuplicateCandidateGroups(explorerGraph.nodes, explorerGraph.edges, resourceData, decisions, filters));
  return { explorerGraph, resourceData, decisions, groups, unfilteredGroups };
}

// GET /graph/canonical/duplicates
app.get('/graph/canonical/duplicates', async (c) => {
  try {
    const filters = parseCanonicalFilters(c.req.query.bind(c.req));
    const { groups } = await canonicalGraphContext(filters);
    return c.json({
      schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
      generatedAt: new Date().toISOString(),
      filters,
      groups,
      total: groups.length,
    });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/duplicates/:groupId
app.get('/graph/canonical/duplicates/:groupId', async (c) => {
  try {
    const { groups } = await canonicalGraphContext({});
    const group = findDuplicateGroup(groups, c.req.param('groupId'));
    if (!group) return c.json({ error: { code: 'CANONICAL_DUPLICATE_GROUP_NOT_FOUND', message: 'duplicate group not found' } }, 404);
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), group });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/duplicates/:groupId/preview
app.post('/graph/canonical/duplicates/:groupId/preview', async (c) => {
  try {
    const body = await parseCanonicalDecisionBody(c);
    const { explorerGraph, resourceData, groups } = await canonicalGraphContext({});
    const group = findDuplicateGroup(groups, c.req.param('groupId'));
    if (!group) return c.json({ error: { code: 'CANONICAL_DUPLICATE_GROUP_NOT_FOUND', message: 'duplicate group not found' } }, 404);
    return c.json(recordCanonicalDecision(repoRoot, group, { ...body, dryRun: true, apply: false }, explorerGraph.edges, resourceData.nodeResourceLinks));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/duplicates/:groupId/decision
app.post('/graph/canonical/duplicates/:groupId/decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalDecisionBody(c);
    const { explorerGraph, resourceData, groups } = await canonicalGraphContext({});
    const group = findDuplicateGroup(groups, c.req.param('groupId'));
    if (!group) return c.json({ error: { code: 'CANONICAL_DUPLICATE_GROUP_NOT_FOUND', message: 'duplicate group not found' } }, 404);
    return c.json(recordCanonicalDecision(repoRoot, group, body, explorerGraph.edges, resourceData.nodeResourceLinks));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/decisions
app.get('/graph/canonical/decisions', (c) => {
  try {
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), decisions: readCanonicalDecisions(repoRoot) });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/approvals
app.get('/graph/canonical/approvals', (c) => {
  try {
    const approvals = readCanonicalApprovals(repoRoot);
    const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot).filter((edge) => edge.reviewStatus !== 'rolled_back');
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), approvals, admittedRelationships, total: approvals.length });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/approvals/:approvalId
app.get('/graph/canonical/approvals/:approvalId', (c) => {
  try {
    const approval = readCanonicalApprovals(repoRoot).find((entry) => entry.approvalId === c.req.param('approvalId'));
    if (!approval) return c.json({ error: { code: 'CANONICAL_APPROVAL_NOT_FOUND', message: 'canonical approval not found' } }, 404);
    const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot).filter((edge) => edge.approvalId === approval.approvalId && edge.reviewStatus !== 'rolled_back');
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), approval, admittedRelationships });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/decisions/:decisionId/approval-preview
app.post('/graph/canonical/decisions/:decisionId/approval-preview', async (c) => {
  try {
    const body = await parseCanonicalApprovalBody(c);
    const { explorerGraph, resourceData } = await canonicalGraphContext({});
    return c.json(previewCanonicalApproval(repoRoot, c.req.param('decisionId'), { ...body, dryRun: true, apply: false }, explorerGraph.nodes, explorerGraph.edges, resourceData));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/decisions/:decisionId/approve
app.post('/graph/canonical/decisions/:decisionId/approve', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalApprovalBody(c);
    const { explorerGraph, resourceData } = await canonicalGraphContext({});
    return c.json(approveCanonicalDecision(repoRoot, c.req.param('decisionId'), body, explorerGraph.nodes, explorerGraph.edges, resourceData));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/decisions/:decisionId/reject-approval
app.post('/graph/canonical/decisions/:decisionId/reject-approval', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalApprovalRejectionBody(c);
    return c.json(rejectCanonicalApproval(repoRoot, c.req.param('decisionId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/node/:nodeId
app.get('/graph/canonical/node/:nodeId', async (c) => {
  try {
    const { groups } = await canonicalGraphContext({});
    return c.json({
      schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
      generatedAt: new Date().toISOString(),
      nodeId: c.req.param('nodeId'),
      canonical: canonicalNodeStatus(repoRoot, c.req.param('nodeId'), groups),
    });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/search?q=
app.get('/graph/canonical/search', async (c) => {
  try {
    const query = c.req.query('q') || '';
    if (!query.trim()) return c.json({ error: { code: 'CANONICAL_SEARCH_QUERY_REQUIRED', message: 'q is required' } }, 400);
    const limit = Math.max(1, Math.min(50, Number.parseInt(c.req.query('limit') || '20', 10) || 20));
    const { explorerGraph, groups } = await canonicalGraphContext({});
    return c.json({
      schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
      generatedAt: new Date().toISOString(),
      query,
      results: canonicalPreferredSearch(repoRoot, explorerGraph.nodes, query, groups, limit),
    });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/validation
app.get('/graph/canonical/validation', async (c) => {
  try {
    const { explorerGraph, resourceData } = await canonicalGraphContext({});
    return c.json(validateCanonicalStewardship(repoRoot, explorerGraph.nodes, explorerGraph.edges, resourceData));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/priorities
app.get('/graph/canonical/priorities', async (c) => {
  try {
    const filters = parseCanonicalFilters(c.req.query.bind(c.req));
    const { groups } = await canonicalGraphContext(filters);
    return c.json({
      schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
      generatedAt: new Date().toISOString(),
      priorities: groups,
      overrides: readCanonicalPriorityOverrides(repoRoot),
      total: groups.length,
    });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/groups/:groupId/priority
app.post('/graph/canonical/groups/:groupId/priority', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalBatchBody(c);
    if (!body.priorityBand) throw new ResourceReviewError('priorityBand is required');
    const { unfilteredGroups } = await canonicalGraphContext({});
    if (!findDuplicateGroup(unfilteredGroups, c.req.param('groupId'))) return c.json({ error: { code: 'CANONICAL_DUPLICATE_GROUP_NOT_FOUND', message: 'duplicate group not found' } }, 404);
    return c.json(setCanonicalGroupPriority(repoRoot, c.req.param('groupId'), {
      priorityBand: body.priorityBand,
      reviewer: body.reviewer,
      owner: body.owner,
      notes: body.notes,
      tags: body.tags,
    }));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/batches
app.get('/graph/canonical/batches', async (c) => {
  try {
    const { unfilteredGroups } = await canonicalGraphContext({});
    const batches = listCanonicalBatches(repoRoot, unfilteredGroups);
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), batches, total: batches.length });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/batches
app.post('/graph/canonical/batches', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalBatchBody(c);
    const filters = { ...(body.filters || {}) } as DuplicateFilters;
    const { groups } = await canonicalGraphContext(filters);
    return c.json(createCanonicalBatch(repoRoot, groups, {
      name: body.name,
      filters,
      reviewer: body.reviewer,
      priorityBand: body.priorityBand,
      tags: body.tags,
      notes: body.notes,
    }));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/batches/:batchId
app.get('/graph/canonical/batches/:batchId', async (c) => {
  try {
    const { unfilteredGroups } = await canonicalGraphContext({});
    const batch = findCanonicalBatch(repoRoot, c.req.param('batchId'), unfilteredGroups);
    if (!batch) return c.json({ error: { code: 'CANONICAL_BATCH_NOT_FOUND', message: 'canonical batch not found' } }, 404);
    const groupIds = new Set(batch.groupIds);
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), batch, groups: unfilteredGroups.filter((group) => groupIds.has(group.groupId)) });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/batches/:batchId/preview
app.post('/graph/canonical/batches/:batchId/preview', async (c) => {
  try {
    const body = await parseCanonicalBatchBody(c);
    const { unfilteredGroups } = await canonicalGraphContext({});
    const batch = findCanonicalBatch(repoRoot, c.req.param('batchId'), unfilteredGroups);
    if (!batch) return c.json({ error: { code: 'CANONICAL_BATCH_NOT_FOUND', message: 'canonical batch not found' } }, 404);
    const groupIds = new Set(batch.groupIds);
    return c.json({ preview: previewCanonicalBatchDecision(batch, unfilteredGroups.filter((group) => groupIds.has(group.groupId)), { ...body, dryRun: true, apply: false }) });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/batches/:batchId/decision
app.post('/graph/canonical/batches/:batchId/decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalBatchBody(c);
    const { unfilteredGroups } = await canonicalGraphContext({});
    return c.json(recordCanonicalBatchDecision(repoRoot, c.req.param('batchId'), unfilteredGroups, body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/p1-decision-packets
app.get('/graph/canonical/p1-decision-packets', (c) => {
  try {
    const packets = listCanonicalP1PacketsWithReviews(repoRoot, {
      ontologyReviewStatus: c.req.query('ontologyReviewStatus'),
      reviewRiskLevel: c.req.query('reviewRiskLevel'),
      groupId: c.req.query('groupId'),
      query: c.req.query('query') || c.req.query('q'),
      needsKimiReview: isTruthyQuery(c.req.query('needsKimiReview')),
      needsHumanReview: isTruthyQuery(c.req.query('needsHumanReview')),
      reviewed: isTruthyQuery(c.req.query('reviewed')),
      unreviewed: isTruthyQuery(c.req.query('unreviewed')),
    });
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), packets, total: packets.length });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/p1-packets
app.get('/graph/canonical/p1-packets', (c) => {
  try {
    const packets = listCanonicalP1PacketsWithReviews(repoRoot, {
      ontologyReviewStatus: c.req.query('ontologyReviewStatus'),
      reviewRiskLevel: c.req.query('reviewRiskLevel'),
      groupId: c.req.query('groupId'),
      query: c.req.query('query') || c.req.query('q'),
      needsKimiReview: isTruthyQuery(c.req.query('needsKimiReview')),
      needsHumanReview: isTruthyQuery(c.req.query('needsHumanReview')),
      reviewed: isTruthyQuery(c.req.query('reviewed')),
      unreviewed: isTruthyQuery(c.req.query('unreviewed')),
    });
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), packets, total: packets.length });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/p1-packets/:packetId
app.get('/graph/canonical/p1-packets/:packetId', (c) => {
  try {
    const detail = getCanonicalP1PacketDetail(repoRoot, c.req.param('packetId'));
    if (!detail) return c.json({ error: { code: 'CANONICAL_P1_PACKET_NOT_FOUND', message: 'P1 decision packet not found' } }, 404);
    return c.json(detail);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/p1-packets/:packetId/review-preview
app.post('/graph/canonical/p1-packets/:packetId/review-preview', async (c) => {
  try {
    const body = await parseCanonicalP1PacketReviewBody(c);
    return c.json(previewCanonicalP1PacketReview(repoRoot, c.req.param('packetId'), { ...body, dryRun: true, apply: false }));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/p1-packets/:packetId/review-decision
app.post('/graph/canonical/p1-packets/:packetId/review-decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalP1PacketReviewBody(c);
    return c.json(recordCanonicalP1PacketReview(repoRoot, c.req.param('packetId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/p1-decision-packets/generate
app.post('/graph/canonical/p1-decision-packets/generate', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalP1PacketBody(c);
    const { explorerGraph, resourceData, unfilteredGroups } = await canonicalGraphContext({});
    return c.json(generateCanonicalP1DecisionPackets(repoRoot, unfilteredGroups, explorerGraph.edges, body, {
      nodes: explorerGraph.nodes,
      resourceData,
    }));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/p1-decision-packets/rebase
app.post('/graph/canonical/p1-decision-packets/rebase', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalP1PacketBody(c);
    const { explorerGraph, resourceData, unfilteredGroups } = await canonicalGraphContext({});
    return c.json(rebaseCanonicalP1DecisionPackets(repoRoot, unfilteredGroups, explorerGraph.edges, body, {
      nodes: explorerGraph.nodes,
      resourceData,
    }));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/decisions/:decisionId/rollback-preview
app.get('/graph/canonical/decisions/:decisionId/rollback-preview', (c) => {
  try {
    return c.json(previewCanonicalRollback(repoRoot, c.req.param('decisionId')));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/decisions/:decisionId/rollback
app.post('/graph/canonical/decisions/:decisionId/rollback', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalRollbackBody(c);
    return c.json(rollbackCanonicalDecision(repoRoot, c.req.param('decisionId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/remediation
app.get('/graph/canonical/remediation', (c) => {
  try {
    return c.json({
      schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
      generatedAt: new Date().toISOString(),
      remediationManifests: listCanonicalRemediationManifests(repoRoot),
    });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /graph/canonical/remediation/:id
app.get('/graph/canonical/remediation/:id', (c) => {
  try {
    const remediation = findCanonicalRemediationManifest(repoRoot, c.req.param('id'));
    if (!remediation) return c.json({ error: { code: 'CANONICAL_REMEDIATION_NOT_FOUND', message: 'canonical remediation manifest not found' } }, 404);
    return c.json({ schemaVersion: 'vitruvius-graph-canonical-stewardship/v1', generatedAt: new Date().toISOString(), remediation });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /graph/canonical/remediation/:id/status
app.post('/graph/canonical/remediation/:id/status', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseCanonicalRemediationBody(c);
    return c.json(updateCanonicalRemediationStatus(repoRoot, c.req.param('id'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/metrics
app.get('/resources/metrics', async (c) => {
  let eligibleNodeIds = new Set<string>();
  try {
    const { explorerGraph } = await readAecMepfsBackboneGraphArtifacts();
    eligibleNodeIds = new Set(
      explorerGraph.nodes
        .filter((node: any) => RESOURCE_ELIGIBLE_NODE_TYPES.has(String(node.type || '').toLowerCase()))
        .map((node: any) => node.id)
        .filter(Boolean)
    );
  } catch {
    eligibleNodeIds = new Set();
  }
  return c.json(resourceLayerMetrics(repoRoot, eligibleNodeIds));
});

// GET /resources/review/queue
app.get('/resources/review/queue', (c) => {
  try {
    return c.json(buildResourceReviewQueue(repoRoot, parseReviewFilters(c.req.query.bind(c.req))));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/candidates
app.get('/resources/review/candidates', (c) => {
  try {
    return c.json(buildResourceReviewCandidates(repoRoot, parseReviewFilters(c.req.query.bind(c.req))));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/local-files
app.get('/resources/review/local-files', (c) => {
  try {
    return c.json(buildLocalFileReview(repoRoot, parseReviewFilters(c.req.query.bind(c.req))));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/standards
app.get('/resources/review/standards', (c) => {
  try {
    return c.json(buildStandardsReview(repoRoot, parseReviewFilters(c.req.query.bind(c.req))));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/standards/:id
app.get('/resources/review/standards/:id', (c) => {
  try {
    return c.json(getStandardsContextReviewDetail(repoRoot, c.req.param('id')));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/standards/:id/context-preview
app.post('/resources/review/standards/:id/context-preview', async (c) => {
  try {
    const body = await parseStandardsContextDecisionBody(c);
    return c.json(previewStandardsContextDecision(repoRoot, c.req.param('id'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/standards/:id/context-decision
app.post('/resources/review/standards/:id/context-decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseStandardsContextDecisionBody(c);
    return c.json(decideStandardsContext(repoRoot, c.req.param('id'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/report
app.get('/resources/review/report', (c) => {
  try {
    return c.json(buildResourceReviewReport(repoRoot));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/source-custody
app.get('/resources/review/source-custody', (c) => {
  try {
    requireLocalDevAdmin(c);
    return c.json(buildSourceCustodyQueue(repoRoot));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/external-candidates/schema
app.get('/resources/review/external-candidates/schema', (c) => {
  return c.json({
    schemaVersion: 'vitruvius-external-metadata-candidate/v1',
    resourceTypes: [
      'external_url_candidate',
      'book_candidate',
      'pdf_candidate',
      'standard_candidate',
      'guide_candidate',
      'article_candidate',
      'dataset_candidate',
      'source_family_reference',
    ],
    fields: [
      { name: 'title', required: true, type: 'string' },
      { name: 'resourceType', required: true, type: 'enum' },
      { name: 'sourceType', required: false, type: 'string' },
      { name: 'proposedUrl', required: false, type: 'url' },
      { name: 'proposedDoi', required: false, type: 'doi' },
      { name: 'proposedIsbn', required: false, type: 'isbn' },
      { name: 'proposedPublisher', required: false, type: 'string' },
      { name: 'proposedAuthors', required: false, type: 'string[]' },
      { name: 'proposedPublicationDate', required: false, type: 'string' },
      { name: 'proposedEdition', required: false, type: 'string' },
      { name: 'proposedVersion', required: false, type: 'string' },
      { name: 'proposedScope', required: false, type: 'string' },
      { name: 'proposedJurisdiction', required: false, type: 'string' },
      { name: 'proposedSourceFamilyId', required: false, type: 'string' },
      { name: 'proposedRightsStatus', required: false, type: 'string' },
      { name: 'proposedNodeIds', required: false, type: 'string[]' },
      { name: 'proposedRelation', required: false, type: 'string' },
      { name: 'candidateRationale', required: false, type: 'string' },
      { name: 'submittedBy', required: false, type: 'string' },
    ],
    defaults: {
      verificationStatus: 'unverified',
      displayPolicy: 'reviewer_only',
      learnerVisible: false,
      reviewRequired: true,
    },
    constraints: {
      noAutoVerification: true,
      noAutoPromotion: true,
      noAutoLinking: true,
      noLearnerExposure: true,
      standardsRequireCompleteContext: true,
    },
  });
});

// POST /resources/review/external-candidates/preview
app.post('/resources/review/external-candidates/preview', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await c.req.json<ExternalMetadataCandidateInput>();
    if (!body || typeof body !== 'object') {
      return c.json({ error: { message: 'Request body must be an object' } }, 400);
    }
    const preview = buildExternalCandidatePreview(body);
    return c.json(preview);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates
// Persist a validated external metadata candidate to the registry.
app.post('/resources/review/external-candidates', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await c.req.json<ExternalMetadataCandidateInput>();
    if (!body || typeof body !== 'object') {
      return c.json({ error: { message: 'Request body must be an object' } }, 400);
    }
    const result = persistExternalCandidate(repoRoot, body);
    if (!result.ok) {
      return c.json({ error: { message: result.error || 'Persist failed' }, duplicateOf: result.duplicateOf }, 400);
    }
    return c.json({ ok: true, candidate: result.candidate, manifest: result.manifest }, 201);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/external-candidates
app.get('/resources/review/external-candidates', (c) => {
  try {
    requireLocalDevAdmin(c);
    const status = c.req.query('status');
    const resourceType = c.req.query('resourceType');
    const candidates = listExternalCandidates(repoRoot, { status: status || undefined, resourceType: resourceType || undefined });
    return c.json({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', count: candidates.length, candidates });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/external-candidates/:candidateId
app.get('/resources/review/external-candidates/:candidateId', (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidate = getExternalCandidate(repoRoot, c.req.param('candidateId'));
    if (!candidate) {
      return c.json({ error: { message: 'Candidate not found' } }, 404);
    }
    return c.json(candidate);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates/:candidateId/correction-preview
app.post('/resources/review/external-candidates/:candidateId/correction-preview', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const body = await c.req.json<{ patch: Record<string, unknown>; reviewer: string; rationale: string }>();
    const candidate = getExternalCandidate(repoRoot, candidateId);
    if (!candidate) return c.json({ error: { message: 'Candidate not found' } }, 404);
    const result = previewCorrection(candidate, body.patch as any, body.reviewer, body.rationale);
    return c.json(result);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates/:candidateId/correction
app.post('/resources/review/external-candidates/:candidateId/correction', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const body = await c.req.json<{ patch: Record<string, unknown>; reviewer: string; rationale: string }>();
    const result = applyCorrection(repoRoot, candidateId, body.patch as any, body.reviewer, body.rationale);
    return c.json(result);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates/:candidateId/review-preview
app.post('/resources/review/external-candidates/:candidateId/review-preview', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const body = await c.req.json<any>();
    const candidate = getExternalCandidate(repoRoot, candidateId);
    if (!candidate) return c.json({ error: { message: 'Candidate not found' } }, 404);
    const result = previewReviewDecision(candidate, body);
    return c.json(result);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates/:candidateId/review-decision
app.post('/resources/review/external-candidates/:candidateId/review-decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const body = await c.req.json<any>();
    const result = applyReviewDecision(repoRoot, candidateId, body);
    return c.json(result);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/review/external-candidates/:candidateId/history
app.get('/resources/review/external-candidates/:candidateId/history', (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const history = getCandidateDecisionHistory(repoRoot, candidateId);
    return c.json({ candidateId, decisions: history, decisionCount: history.length });
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/external-candidates/:candidateId/promotion-preview
app.post('/resources/review/external-candidates/:candidateId/promotion-preview', (c) => {
  try {
    requireLocalDevAdmin(c);
    const candidateId = c.req.param('candidateId');
    const registry = loadExternalCandidateRegistry(repoRoot);
    const candidate = registry.candidates.find((cand) => cand.candidateId === candidateId);
    if (!candidate) {
      return c.json({ error: { message: `Candidate not found: ${candidateId}` } }, 404);
    }
    const preview = buildExternalCandidatePromotionPreview(candidate);
    return c.json(preview);
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/link/:linkId/decision
app.post('/resources/review/link/:linkId/decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseReviewDecisionBody(c);
    return c.json(decideNodeResourceLink(repoRoot, c.req.param('linkId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/candidate/:candidateId/decision
app.post('/resources/review/candidate/:candidateId/decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseReviewDecisionBody(c);
    return c.json(decideResourceCandidate(repoRoot, c.req.param('candidateId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// POST /resources/review/local-file/:fileId/decision
app.post('/resources/review/local-file/:fileId/decision', async (c) => {
  try {
    requireLocalDevAdmin(c);
    const body = await parseReviewDecisionBody(c);
    return c.json(decideLocalFile(repoRoot, c.req.param('fileId'), body));
  } catch (error: any) {
    return reviewErrorResponse(c, error);
  }
});

// GET /resources/:id
app.get('/resources/:id', (c) => {
  const id = c.req.param('id');
  const resource = getResource(repoRoot, id);
  if (!resource) return c.json({ error: { code: 'RESOURCE_NOT_FOUND', message: `Resource '${id}' not found` } }, 404);
  return c.json({ resource });
});

// GET /node/:id
app.get('/node/:id', async (c) => {
  const id = c.req.param('id');

  if (isLikelyAecMepfsBackboneNodeId(id)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      return c.json(buildAecMepfsNodeDetailFromIndex(explorerIndex, id));
    } catch (error: any) {
      if (error instanceof ShadowBackboneNodeNotFoundError) {
        return c.json({ error: { code: error.code, message: error.message } }, 404);
      }
      return c.json({
        error: {
          code: 'AEC_MEPFS_NODE_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS node detail is unavailable',
        },
      }, 503);
    }
  }

  const nodes = await runQuery(buildNodeDetailQuery(), { id });

  if (!nodes.length) return c.json({ error: { code: 'NODE_NOT_FOUND', message: `Node '${id}' not found` } }, 404);

  const n = nodes[0];
  const node = normalizeNode(n.c);

  // Build taxonomy path
  const taxonomyPath: any[] = [];
  if (node?.taxonomy_path && Array.isArray(node.taxonomy_path)) {
    const taxonomyNodes = await runQuery(
      'MATCH (t) WHERE t.id IN $ids RETURN t.id AS id, t.label AS label, t.kind AS kind',
      { ids: node.taxonomy_path }
    );
    const taxonomyById = new Map(taxonomyNodes.map((taxo: any) => [taxo.id, taxo]));
    for (const taxoId of node.taxonomy_path) {
      const taxo = taxonomyById.get(taxoId);
      if (taxo) taxonomyPath.push(normalizeTaxonomyNode(taxo));
    }
  }

  const evidence = (n.evidence || []).filter(Boolean).map((e: any) => normalizeEvidenceSpan(e));
  if (node?.type === 'evidence_span' && evidence.length === 0) {
    evidence.push(normalizeEvidenceSpan(n.c));
  }

  const incoming = (n.incoming || []).filter((r: any) => r.rel && r.other).map((r: any) => ({
    relType: r.rel,
    other: normalizeNode(r.other),
    reasoning: r.reasoning,
    confidence: r.confidence != null ? Number(r.confidence) : undefined,
    assertionId: r.assertionId,
  }));

  const outgoing = (n.outgoing || []).filter((r: any) => r.rel && r.other).map((r: any) => ({
    relType: r.rel,
    other: normalizeNode(r.other),
    reasoning: r.reasoning,
    confidence: r.confidence != null ? Number(r.confidence) : undefined,
    assertionId: r.assertionId,
  }));

  return c.json({ node, taxonomyPath, incoming, outgoing, evidence, resources: getNodeResources(repoRoot, id) });
});

// GET /edge/:id
app.get('/edge/:id', async (c) => {
  const id = c.req.param('id');

  if (isLikelyAecMepfsBackboneEdgeId(id)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      return c.json(buildAecMepfsEdgeDetailFromIndex(explorerIndex, id));
    } catch (error: any) {
      if (error instanceof ShadowBackboneEdgeNotFoundError) {
        return c.json({ error: { code: error.code, message: error.message } }, 404);
      }
      return c.json({
        error: {
          code: 'AEC_MEPFS_EDGE_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS edge detail is unavailable',
        },
      }, 503);
    }
  }

  // Try assertion_id first
  let records = await runQuery(`
    MATCH (a)-[r]->(b)
    WHERE r.assertion_id = $id
    RETURN r, a, b
  `, { id });

  // Fallback: parse as source|type|target
  if (!records.length && id.includes('|')) {
    const [sourceId, type, targetId] = id.split('|');
    records = await runQuery(`
      MATCH (a)-[r]->(b)
      WHERE a.id = $sourceId AND type(r) = $type AND b.id = $targetId
      RETURN r, a, b
    `, { sourceId, type, targetId });
  }

  if (!records.length) {
    return c.json({ error: { code: 'EDGE_NOT_FOUND', message: `Edge '${id}' not found` } }, 404);
  }

  const rec = records[0];
  const edge = normalizeEdge(rec.r, rec.a.id, rec.b.id);
  const edgeEvidence = edge.type === 'SUPPORTED_BY'
    ? [rec.a, rec.b]
        .map((node: any) => normalizeNode(node))
        .filter((node: any) => node?.type === 'evidence_span')
        .map((node: any) => ({
          id: node.id,
          quote: node.label,
          document_id: node.id,
          document_title: node.label,
          deep_link: undefined,
          confidence: undefined,
        }))
    : [];
  return c.json({
    edge,
    source: normalizeNode(rec.a),
    target: normalizeNode(rec.b),
    evidence: edgeEvidence,
  });
});

// POST /query
app.post('/query', async (c) => {
  const body = await c.req.json();
  const cypher = (body.cypher || '').trim();

  if (!cypher) {
    return c.json({ error: { code: 'BAD_REQUEST', message: 'cypher query is required' } }, 400);
  }

  function extractValue(value: any, nodeMap: Map<string, any>, edgeMap: Map<string, any>) {
    if (neo4j.isNode(value)) {
      const n = normalizeNode(value.properties);
      if (n) nodeMap.set(n.id, n);
    } else if (neo4j.isPath(value)) {
      value.segments.forEach((seg: any) => {
        const start = normalizeNode(seg.start.properties);
        const end = normalizeNode(seg.end.properties);
        if (start) nodeMap.set(start.id, start);
        if (end) nodeMap.set(end.id, end);
        if (start && end) {
          const rel = normalizeEdge(
            { ...seg.relationship.properties, type: seg.relationship.type },
            start.id,
            end.id
          );
          edgeMap.set(rel.id, rel);
        }
      });
    } else if (Array.isArray(value)) {
      value.forEach(v => extractValue(v, nodeMap, edgeMap));
    }
  }

  const session = driver.session({ defaultAccessMode: neo4j.session.READ });
  try {
    const result = await session.run(cypher);
    const nodeMap = new Map<string, any>();
    const edgeMap = new Map<string, any>();
    const rows = result.records.map((record: any, index: number) => {
      const values: Record<string, string> = {};
      record.keys.forEach((key: string) => {
        values[key] = summarizeValue(record.get(key));
      });
      return { id: `row-${index}`, values };
    });

    result.records.forEach((record: any) => {
      record.keys.forEach((key: string) => {
        extractValue(record.get(key), nodeMap, edgeMap);
      });
    });

      return c.json({
        nodes: dedupeRuleDisplayLabels(Array.from(nodeMap.values())),
        edges: Array.from(edgeMap.values()),
        recordCount: result.records.length,
        rows,
      });
  } catch (err: any) {
    return c.json({ error: { code: 'QUERY_ERROR', message: err.message } }, 400);
  } finally {
    await session.close();
  }
});

// GET /expand
app.get('/expand', async (c) => {
  const nodeId = c.req.query('nodeId');
  const relTypes = c.req.query('relTypes')?.split(',').filter(Boolean);
  const direction = c.req.query('direction') || 'both';
  const limit = Math.min(parseInt(c.req.query('limit') || '50'), 200);
  const depth = Math.min(parseInt(c.req.query('depth') || '1'), 6);

  if (!nodeId) return c.json({ error: { code: 'BAD_REQUEST', message: 'nodeId is required' } }, 400);

  if (isLikelyAecMepfsBackboneNodeId(nodeId)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      return c.json(buildAecMepfsExpandResultFromIndex(explorerIndex, nodeId, relTypes, direction, depth, limit));
    } catch (error: any) {
      return c.json({
        error: {
          code: 'AEC_MEPFS_EXPAND_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS expansion is unavailable',
        },
      }, 503);
    }
  }

  let relFilter = '';
  if (relTypes && relTypes.length) {
    relFilter = 'AND type(r) IN $relTypes';
  }

  let query = '';
  if (direction === 'out') {
    query = `
      MATCH (c)-[r]->(other)
      WHERE c.id = $nodeId ${relFilter}
      RETURN c.id AS source, other, r
      LIMIT $limit
    `;
  } else if (direction === 'in') {
    query = `
      MATCH (other)-[r]->(c)
      WHERE c.id = $nodeId ${relFilter}
      RETURN other AS source, c AS other, r
      LIMIT $limit
    `;
  } else {
    query = `
      MATCH (c)-[r]-(other)
      WHERE c.id = $nodeId ${relFilter}
      RETURN c.id AS source, other, r
      LIMIT $limit
    `;
  }

  const records = await runQuery(query, { nodeId, relTypes: relTypes || [], limit: neo4j.int(limit) });

  const nodeIds = new Set([nodeId]);
  const edgeSet = new Map<string, any>();

  records.forEach((rec: any) => {
    const other = normalizeNode(rec.other);
    if (other) nodeIds.add(other.id);

    const sourceId = rec.source || nodeId;
    const targetId = rec.other?.id || rec.other?.properties?.id;
    if (targetId) {
      const edge = normalizeEdge(rec.r, sourceId, targetId);
      edgeSet.set(edge.id, edge);
    }
  });

  // Fetch all nodes
  const allNodes = await runQuery(`
    MATCH (n) WHERE n.id IN $ids
    RETURN n
  `, { ids: Array.from(nodeIds) });

  return c.json({
    nodeId,
    neighbors: records.map((rec: any) => ({
      node: normalizeNode(rec.other),
      relType: rec.r?.type,
      direction: direction,
    })).filter((n: any) => n.node),
    nodes: dedupeRuleDisplayLabels(allNodes.map((r: any) => normalizeNode(r.n)).filter(isPresent)),
    edges: Array.from(edgeSet.values()),
  });
});

// GET /path
app.get('/path', async (c) => {
  const from = c.req.query('from');
  const to = c.req.query('to');
  const maxHops = Math.min(parseInt(c.req.query('maxHops') || '6'), 12);
  const limit = Math.min(parseInt(c.req.query('limit') || '5'), 20);

  if (!from || !to) return c.json({ error: { code: 'BAD_REQUEST', message: 'from and to are required' } }, 400);

  if (isLikelyAecMepfsBackboneNodeId(from) && isLikelyAecMepfsBackboneNodeId(to)) {
    try {
      const explorerIndex = getAecMepfsExplorerGraphIndex(await readAecMepfsBackboneGraphArtifacts());
      const paths = buildAecMepfsPathResultFromIndex(explorerIndex, from, to, maxHops).slice(0, limit);
      if (!paths.length) {
        return c.json({ error: { code: 'PATH_NOT_FOUND', message: `No AEC-MEPFS path found between '${from}' and '${to}' within ${maxHops} hops` } }, 404);
      }
      return c.json({ paths });
    } catch (error: any) {
      return c.json({
        error: {
          code: 'AEC_MEPFS_PATH_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS path tracing is unavailable',
        },
      }, 503);
    }
  }

  const records = await runQuery(`
    MATCH path = shortestPath((a)-[*1..${maxHops}]-(b))
    WHERE a.id = $from AND b.id = $to
    RETURN path
    LIMIT $limit
  `, { from, to, limit: neo4j.int(limit) });

  if (!records.length) {
    return c.json({ error: { code: 'PATH_NOT_FOUND', message: `No path found between '${from}' and '${to}' within ${maxHops} hops` } }, 404);
  }

  const paths = records.map((rec: any) => {
    const path = rec.path;
    const nodes = path.segments.map((s: any) => normalizeNode(s.start.properties)).filter(Boolean);
    nodes.push(normalizeNode(path.end.properties));
    const edges = path.segments.map((s: any) => normalizeEdge(
      { ...s.relationship.properties, type: s.relationship.type },
      s.start.properties.id,
      s.end.properties.id
    ));
    return { length: edges.length, nodes, edges };
  });

  return c.json({ paths });
});

// GET /taxonomy
app.get('/taxonomy', async (c) => {
  try {
    const { explorerGraph } = await readAecMepfsBackboneGraphArtifacts();
    return c.json({ roots: buildAecMepfsTaxonomyTreeFromGraph(explorerGraph) });
  } catch {
    // Fall through to the legacy Neo4j taxonomy only when the file-backed AEC-MEPFS
    // surface is unavailable, preserving a degraded-but-usable prelaunch fallback.
  }

  const allNodes = await runQuery(`
    MATCH (n)
    WHERE n:Taxonomy OR n:Topic OR n:Subtopic
    RETURN n.id AS id, n.label AS label, n.kind AS kind
    ORDER BY label
  `);

  const edges = await runQuery(`
    MATCH (parent)-[:HAS_CHILD]->(child)
    WHERE parent:Taxonomy OR parent:Topic OR parent:Subtopic
    RETURN parent.id AS parentId, child.id AS childId
  `);

  const conceptCounts = await runQuery(`
    MATCH (c:CanonicalNode)-[:BELONGS_TO]->(node)
    WHERE c.type = 'concept' AND (node:Taxonomy OR node:Topic OR node:Subtopic)
    RETURN node.id AS id, count(DISTINCT c) AS conceptCount
  `);

  const countById = new Map(conceptCounts.map((row: any) => [row.id, Number(row.conceptCount) || 0]));
  const childrenByParent = new Map<string, string[]>();
  const childIds = new Set<string>();

  for (const edge of edges) {
    childIds.add(edge.childId);
    if (!childrenByParent.has(edge.parentId)) childrenByParent.set(edge.parentId, []);
    childrenByParent.get(edge.parentId)!.push(edge.childId);
  }

  const nodeById = new Map(
    allNodes.map((node: any) => [
      node.id,
      normalizeTaxonomyNode({ ...node, conceptCount: countById.get(node.id) || 0 }),
    ])
  );

  function buildTree(nodeId: string): any {
    const node = nodeById.get(nodeId);
    if (!node) return null;
    const children = (childrenByParent.get(nodeId) || [])
      .map((childId) => buildTree(childId))
      .filter(Boolean)
      .sort((a: any, b: any) => a.label.localeCompare(b.label));
    return { ...node, children };
  }

  const roots = allNodes
    .filter((node: any) => !childIds.has(node.id))
    .map((node: any) => buildTree(node.id))
    .filter(Boolean)
    .sort((a: any, b: any) => a.label.localeCompare(b.label));

  return c.json({ roots });
});

// GET /perspectives
app.get('/perspectives', async (c) => {
  const includeLegacyCounts = c.req.query('includeCounts') === '1';
  const perspectives = await Promise.all(
    PERSPECTIVE_METADATA.map(async (perspective) => {
      try {
        if (perspective.id !== AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID && !includeLegacyCounts) {
          return { ...perspective };
        }
        return {
          ...perspective,
          nodeCount: await getPerspectiveNodeCount(perspective.id),
        };
      } catch {
        return { ...perspective };
      }
    })
  );
  return c.json({ perspectives });
});

// GET /perspective/:id/nodes
app.get('/perspective/:id/nodes', async (c) => {
  const id = c.req.param('id');
  const profile = c.req.query('profile');

  if (id === AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID) {
    try {
      const { explorerGraph } = await readAecMepfsBackboneGraphArtifacts();
      if (profile === 'render') {
        return c.json(compactAecMepfsExplorerGraphForRender(explorerGraph));
      }
      return c.json({ nodes: explorerGraph.nodes, edges: explorerGraph.edges });
    } catch (error: any) {
      return c.json({
        error: {
          code: 'AEC_MEPFS_GRAPH_UNAVAILABLE',
          message: error?.message || 'AEC-MEPFS Explorer graph is unavailable',
        },
      }, 503);
    }
  }

  const { nodeQuery, edgeQuery } = buildPerspectiveQueries(id);

  const nodes = await runQuery(nodeQuery);
  const edges = await runQuery(edgeQuery);

  return c.json({
    nodes: dedupeRuleDisplayLabels(nodes.map((r: any) => normalizeNode(r.n || r.c)).filter(isPresent)),
    edges: edges.map((r: any) => normalizeEdge(r.r, r.source, r.target)),
  });
});

// Scene storage (file-backed)
app.get('/scenes', async (c) => {
  const scenes = await readScenes(scenesFilePath);
  return c.json({
    scenes: scenes
      .map((scene) => ({
        id: scene.id,
        name: scene.name,
        savedAt: scene.savedAt,
        perspectiveId: scene.perspectiveId,
      }))
      .sort((a, b) => (b.savedAt || '').localeCompare(a.savedAt || '')),
  });
});

// POST /scene/save
app.post('/scene/save', async (c) => {
  const body = sceneCreateSchema.parse(await c.req.json());
  const scene = await createScene(scenesFilePath, body);
  return c.json({ sceneId: scene.id, url: `/explore?scene=${scene.id}`, scene });
});

app.put('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const body = sceneCreateSchema.parse(await c.req.json());
  const scene = await updateScene(scenesFilePath, id, body);
  if (!scene) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json({ scene });
});

app.delete('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const deleted = await deleteScene(scenesFilePath, id);
  if (!deleted) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json({ ok: true, id });
});

// GET /scene/:id
app.get('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const scenes = await readScenes(scenesFilePath);
  const scene = scenes.find((entry) => entry.id === id);
  if (!scene) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json(scene);
});

// Serve static frontend build
app.use('/*', serveStatic({ root: '../explorer/dist' }));

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
const port = parseInt(process.env.PORT || '3000');
if (import.meta.main) {
  console.log(`Vitruvius Graph API starting on http://localhost:${port}`);
}

export default {
  port,
  fetch: app.fetch,
};
