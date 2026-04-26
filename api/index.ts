import { Hono } from 'hono';
import { serveStatic } from 'hono/bun';
import { cors } from 'hono/cors';
import neo4j from 'neo4j-driver';
import { readFile } from 'node:fs/promises';
import { join, resolve, sep } from 'node:path';
import { createScene, deleteScene, readScenes, sceneCreateSchema, updateScene } from './sceneStore';

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
const SHADOW_BACKBONE_CONSUMER_REPORT_SCHEMA_VERSION = 'aec-bb-shadow-staging-consumer-report/v1';
const SHADOW_BACKBONE_STAGING_SCHEMA_VERSION = 'aec-bb-shadow-staging/v1';
const SHADOW_BACKBONE_REPORT_ROOT = resolve(
  repoRoot,
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'shadow-staging'
);
const DEFAULT_SHADOW_BACKBONE_REPORT_PATH = join(
  SHADOW_BACKBONE_REPORT_ROOT,
  '20260426T000726Z',
  'shadow-staging-consumer-report.json'
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

class ShadowBackboneReportError extends Error {
  code = 'SHADOW_BACKBONE_REPORT_UNAVAILABLE';
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

function resolveShadowBackboneReportPath() {
  const configuredPath = process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
  const resolved = configuredPath
    ? resolve(repoRoot, configuredPath)
    : DEFAULT_SHADOW_BACKBONE_REPORT_PATH;
  const insideReportRoot = resolved === SHADOW_BACKBONE_REPORT_ROOT
    || resolved.startsWith(`${SHADOW_BACKBONE_REPORT_ROOT}${sep}`);
  if (!insideReportRoot) {
    throw new ShadowBackboneReportError(
      'Shadow backbone report path must stay inside the shadow staging report directory'
    );
  }
  return resolved;
}

async function readShadowBackboneConsumerReport() {
  const reportPath = resolveShadowBackboneReportPath();
  try {
    const payload = JSON.parse(await readFile(reportPath, 'utf-8'));
    if (!isRecord(payload)) {
      throw new ShadowBackboneReportError('Shadow backbone consumer report must be a JSON object');
    }
    return payload;
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone consumer report: ${error.message}`);
  }
}

export function resolveShadowBackboneArtifactPath(report: Record<string, any>) {
  const artifactPath = stringField(report.artifact_path);
  if (!artifactPath) {
    throw new ShadowBackboneReportError('Shadow backbone consumer report is missing artifact_path');
  }
  const resolved = resolve(repoRoot, artifactPath);
  const insideReportRoot = resolved === SHADOW_BACKBONE_REPORT_ROOT
    || resolved.startsWith(`${SHADOW_BACKBONE_REPORT_ROOT}${sep}`);
  if (!insideReportRoot) {
    throw new ShadowBackboneReportError(
      'Shadow backbone artifact path must stay inside the shadow staging report directory'
    );
  }
  return resolved;
}

async function readShadowBackboneStagingArtifact(report: Record<string, any>) {
  const artifactPath = resolveShadowBackboneArtifactPath(report);
  try {
    const payload = JSON.parse(await readFile(artifactPath, 'utf-8'));
    if (!isRecord(payload)) {
      throw new ShadowBackboneReportError('Shadow backbone staging artifact must be a JSON object');
    }
    return payload;
  } catch (error: any) {
    if (error instanceof ShadowBackboneReportError) throw error;
    throw new ShadowBackboneReportError(`Unable to read shadow backbone staging artifact: ${error.message}`);
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
      producerReport: stringField(report.producer_report_path),
      consumerReport: stringField(report.report_path),
    },
  };
}

export function buildShadowBackboneTaxonomyPreview(
  report: Record<string, any>,
  artifact: Record<string, any>
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
      previewCompleteness: backboneNodes.length > 0
        ? 'registry_metadata_and_admitted_backbone_nodes'
        : 'registry_metadata_only',
      limitation: backboneNodes.length > 0
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
    sourceFamilies,
    artifactPaths: summary.artifactPaths,
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
  { id: 'default', name: 'All Knowledge', description: 'All canonical and taxonomy nodes currently available' },
  { id: 'concepts', name: 'Concept Map', description: 'Domain concepts connected by semantic relationships' },
  { id: 'taxonomy', name: 'Taxonomy Browser', description: 'Hierarchy, classification, and attached concepts' },
  { id: 'regulatory', name: 'Regulatory Rules', description: 'Rules and directly related concepts' },
  { id: 'evidence', name: 'Evidence Map', description: 'Concept nodes with source evidence links' },
] as const;

async function getPerspectiveNodeCount(id: string): Promise<number> {
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
  try {
    await driver.verifyConnectivity();
    return c.json({ status: 'ok', neo4j: 'connected' });
  } catch (e: any) {
    return c.json({ status: 'error', neo4j: e.message }, 500);
  }
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
    return c.json(buildShadowBackboneTaxonomyPreview(report, artifact));
  } catch (error: any) {
    return c.json({
      error: {
        code: 'SHADOW_BACKBONE_TAXONOMY_UNAVAILABLE',
        message: error?.message || 'Shadow backbone taxonomy preview is unavailable',
      },
    }, 503);
  }
});

// GET /search
app.get('/search', async (c) => {
  const q = c.req.query('q') || '';
  const perspective = c.req.query('perspective');
  const limit = Math.min(parseInt(c.req.query('limit') || '20'), 100);

  if (!q.trim() || q.length < 2) return c.json({ results: [] });

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

// GET /node/:id
app.get('/node/:id', async (c) => {
  const id = c.req.param('id');

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

  return c.json({ node, taxonomyPath, incoming, outgoing, evidence });
});

// GET /edge/:id
app.get('/edge/:id', async (c) => {
  const id = c.req.param('id');

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

  if (!nodeId) return c.json({ error: { code: 'BAD_REQUEST', message: 'nodeId is required' } }, 400);

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
  const perspectives = await Promise.all(
    PERSPECTIVE_METADATA.map(async (perspective) => ({
      ...perspective,
      nodeCount: await getPerspectiveNodeCount(perspective.id),
    }))
  );
  return c.json({ perspectives });
});

// GET /perspective/:id/nodes
app.get('/perspective/:id/nodes', async (c) => {
  const id = c.req.param('id');

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
