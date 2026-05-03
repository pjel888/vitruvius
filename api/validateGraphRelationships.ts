import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import {
  classifyGraphEdge,
  detectCanonicalDuplicateCandidates,
  validateGraphRelationshipData,
  type GraphEdgeLike,
  type GraphNodeLike,
} from './graph/relationshipVisibility';
import {
  mergeAdmittedRelationshipsIntoEdges,
  readCanonicalAdmittedRelationships,
} from './graph/canonicalStewardship';

const repoRoot = resolve(import.meta.dir, '..');
const shadowStagingRoot = resolve(repoRoot, '006_System-Manifests', 'aec-mepfs-backbone', 'shadow-staging');
const reportPath = resolve(repoRoot, '.ai', '13_research', 'graph_duplicate_canonicalization_report.md');

const noWrite = process.argv.includes('--no-write') || process.env.VITRUVIUS_VALIDATE_NO_WRITE === '1' || process.env.VITRUVIUS_VALIDATE_NO_WRITE === 'true';

function latestShadowGraphPath() {
  const runs = readdirSync(shadowStagingRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d{8}T\d{6}Z$/.test(entry.name))
    .map((entry) => entry.name)
    .sort((left, right) => right.localeCompare(left));
  for (const run of runs) {
    const candidate = join(shadowStagingRoot, run, 'shadow-backbone-graph.json');
    if (existsSync(candidate)) return candidate;
  }
  throw new Error('No shadow-backbone-graph.json artifact found');
}

function edgeType(predicate: string) {
  return predicate === 'broader_than'
    ? 'HAS_CHILD'
    : predicate.toUpperCase().replace(/[^A-Z0-9]+/g, '_');
}

const graphPath = latestShadowGraphPath();
const raw = JSON.parse(readFileSync(graphPath, 'utf-8'));
const nodes: GraphNodeLike[] = (Array.isArray(raw.nodes) ? raw.nodes : []).map((node: any) => ({
  id: String(node.id || ''),
  label: String(node.label || ''),
  displayLabel: String(node.pref_label || node.label || ''),
  type: Number(node.level) <= 1 ? 'taxonomy' : Number(node.level) === 2 ? 'topic' : Number(node.level) === 3 ? 'subtopic' : 'concept',
  aliases: [node.path_code || node.pathCode].filter(Boolean),
  taxonomy_path: String(node.path_code || node.pathCode || '').split('.').map((_, index, parts) => parts.slice(0, index + 1).join('.')),
}));
const baseEdges: GraphEdgeLike[] = (Array.isArray(raw.edges) ? raw.edges : []).map((edge: any) => ({
  id: String(edge.id || ''),
  source: String(edge.from_id || ''),
  target: String(edge.to_id || ''),
  type: edgeType(String(edge.predicate || '')),
  relationType: edge.relation_type,
  relationCategory: edge.relation_category,
  semanticOverlayCategory: edge.semantic_overlay_category,
  reviewStatus: edge.review_status,
  provenanceNote: edge.provenance_note,
  sourceFamilyIds: Array.isArray(edge.source_family_ids) ? edge.source_family_ids : undefined,
}));
const activeAdmittedRelationships = readCanonicalAdmittedRelationships(repoRoot)
  .filter((edge) => edge.reviewStatus !== 'rolled_back');
const edges = mergeAdmittedRelationshipsIntoEdges(baseEdges, activeAdmittedRelationships);
const admittedRelationshipEdges = edges.length - baseEdges.length;

const issues = validateGraphRelationshipData(nodes, edges);
const duplicates = detectCanonicalDuplicateCandidates(nodes);
const semanticEdges = edges.filter((edge) => classifyGraphEdge(edge) === 'semantic');
const hierarchyEdges = edges.filter((edge) => classifyGraphEdge(edge) === 'hierarchy');
const safeCandidates = duplicates.filter((candidate) => candidate.safeToAutoMerge);
const unsafeCandidates = duplicates.filter((candidate) => !candidate.safeToAutoMerge);
const concreteCandidates = duplicates.filter((candidate) => candidate.normalizedLabel.includes('concrete'));

const summary = {
  ok: issues.length === 0,
  graphPath,
  nodeCount: nodes.length,
  edgeCount: edges.length,
  baseEdgeCount: baseEdges.length,
  admittedRelationshipEdgeCount: admittedRelationshipEdges,
  hierarchyEdgeCount: hierarchyEdges.length,
  semanticEdgeCount: semanticEdges.length,
  issueCount: issues.length,
  duplicateCanonicalLabelCount: duplicates.length,
  safeDuplicateReviewCandidates: safeCandidates.length,
  unsafeDuplicateReviewCandidates: unsafeCandidates.length,
  concreteDuplicateCandidates: concreteCandidates.length,
  issues: issues.slice(0, 50),
};

const report = [
  '# Graph Duplicate Canonicalization Report',
  '',
  `Date: ${new Date().toISOString()}`,
  `Graph artifact: \`${graphPath.replace(repoRoot, '').replace(/^[/\\]/, '')}\``,
  '',
  '## Summary',
  '',
  `- Nodes: ${nodes.length}`,
  `- Edges: ${edges.length}`,
  `- Base graph edges: ${baseEdges.length}`,
  `- Admitted stewardship relationship edges overlaid: ${admittedRelationshipEdges}`,
  `- Hierarchy edges: ${hierarchyEdges.length}`,
  `- Semantic edges: ${semanticEdges.length}`,
  `- Broken relationship issues: ${issues.length}`,
  `- Duplicate normalized labels: ${duplicates.length}`,
  `- Safe auto-merge candidates: ${safeCandidates.length}`,
  `- Unsafe/manual-review candidates: ${unsafeCandidates.length}`,
  '',
  'No nodes were auto-merged by this validation. Safe candidates still require reviewer confirmation before any registry mutation.',
  '',
  '## Concrete-related duplicate findings',
  '',
  concreteCandidates.length
    ? concreteCandidates.slice(0, 25).map((candidate) => (
      `- \`${candidate.normalizedLabel}\`: ${candidate.nodeIds.join(', ')} — ${candidate.reason}`
    )).join('\n')
    : '- No exact normalized Concrete duplicate labels were detected; multiple concrete-related nodes are distinct taxonomy-specific concepts.',
  '',
  '## Largest manual-review duplicate candidates',
  '',
  unsafeCandidates.slice(0, 50).map((candidate) => (
    `- \`${candidate.normalizedLabel}\` (${candidate.nodeIds.length} nodes): ${candidate.nodeIds.slice(0, 8).join(', ')} — ${candidate.reason}`
  )).join('\n'),
  '',
].join('\n');

if (!noWrite) {
  writeFileSync(reportPath, report, 'utf-8');
}
console.log(JSON.stringify(summary, null, 2));
if (!summary.ok) process.exit(1);
