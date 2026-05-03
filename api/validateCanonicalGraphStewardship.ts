import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import type { GraphEdgeLike, GraphNodeLike } from './graph/relationshipVisibility';
import { buildDuplicateCandidateGroups, readCanonicalDecisions, validateCanonicalStewardship } from './graph/canonicalStewardship';
import { readResourceLayerData } from './resourceLayer/registry';

const repoRoot = resolve(import.meta.dir, '..');
const shadowStagingRoot = resolve(repoRoot, '006_System-Manifests', 'aec-mepfs-backbone', 'shadow-staging');
const validationReportPath = resolve(repoRoot, '.ai', '13_research', 'canonical_graph_stewardship_validation_report.md');
const decisionLogPath = resolve(repoRoot, '.ai', '13_research', 'canonical_graph_stewardship_decision_log.md');

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

function loadGraph() {
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
  const edges: GraphEdgeLike[] = (Array.isArray(raw.edges) ? raw.edges : []).map((edge: any) => ({
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
  return { graphPath, nodes, edges };
}

const { graphPath, nodes, edges } = loadGraph();
const resourceData = readResourceLayerData(repoRoot);
const decisions = readCanonicalDecisions(repoRoot);
const groups = buildDuplicateCandidateGroups(nodes, edges, resourceData, decisions);
const concreteGroups = groups.filter((group) => group.looseNormalizedLabel.includes('concrete'));
const validation = validateCanonicalStewardship(repoRoot, nodes, edges, resourceData);

mkdirSync(dirname(validationReportPath), { recursive: true });
const report = [
  '# Canonical Graph Stewardship Validation Report',
  '',
  `Date: ${new Date().toISOString()}`,
  `Graph artifact: \`${graphPath.replace(repoRoot, '').replace(/^[/\\]/, '')}\``,
  '',
  '## Summary',
  '',
  `- OK: ${validation.ok}`,
  `- Duplicate groups: ${validation.duplicateGroups}`,
  `- Unresolved duplicate groups: ${validation.unresolvedDuplicateGroups}`,
  `- P0 unresolved groups: ${validation.p0UnresolvedGroups}`,
  `- Concrete duplicate groups: ${validation.concreteDuplicateGroups}`,
  `- Groups by risk: \`${JSON.stringify(validation.groupsByRisk || {})}\``,
  `- Groups by priority: \`${JSON.stringify(validation.groupsByPriority || {})}\``,
  `- Batches: ${validation.batchCount || 0}`,
  `- Batch decisions: ${validation.batchDecisionCount || 0}`,
  `- Stewardship decisions: ${validation.stewardshipDecisions}`,
  `- Applied decisions: ${validation.appliedDecisions}`,
  `- Rollbackable decisions: ${validation.rollbackableDecisions || 0}`,
  `- Aliases: ${validation.aliases}`,
  `- Redirects: ${validation.redirects}`,
  `- Tombstones: ${validation.tombstones || 0}`,
  `- Governed disambiguation decisions: ${validation.governedDisambiguationDecisions || 0}`,
  `- Disambiguated keep-separate decisions: ${validation.disambiguatedKeepSeparateDecisions || 0}`,
  `- Related-specialization decisions: ${validation.relatedSpecializationDecisions || 0}`,
  `- Cross-domain equivalence decisions: ${validation.crossDomainEquivalenceDecisions || 0}`,
  `- Stewardship relationship proposals: ${validation.graphStewardshipEdgeProposals || 0}`,
  `- Open remediation manifests: ${validation.openRemediationManifests || 0}`,
  `- P1 decision packets: ${validation.p1DecisionPackets || 0}`,
  `- P1 packets signed: ${validation.p1PacketsSigned || 0}`,
  `- P1 packets unsigned: ${validation.p1PacketsUnsigned || 0}`,
  `- P1 packets invalid signature: ${validation.p1PacketsInvalidSignature || 0}`,
  `- P1 packets missing signature key: ${validation.p1PacketsMissingKey || 0}`,
  `- P1 packet strict signature blockers: ${validation.p1PacketsStrictSignatureBlockers || 0}`,
  `- P1 packets missing source snapshots: ${validation.p1PacketsMissingSourceSnapshot || 0}`,
  `- P1 packets stale source snapshots: ${validation.p1PacketsStaleSourceSnapshot || 0}`,
  `- P1 packets tampered source snapshots: ${validation.p1PacketsTamperedSourceSnapshot || 0}`,
  `- P1 packet content hash mismatches: ${validation.p1PacketsContentHashMismatch || 0}`,
  `- P1 packets with ontology review: ${validation.p1PacketsWithOntologyReview || 0}`,
  `- P1 packets unreviewed: ${validation.p1PacketsUnreviewed || 0}`,
  `- P1 packets Kimi review requested: ${validation.p1PacketsKimiReviewRequested || 0}`,
  `- P1 packets Kimi reviewed: ${validation.p1PacketsKimiReviewed || 0}`,
  `- P1 packets human review needed: ${validation.p1PacketsHumanReviewNeeded || 0}`,
  `- P1 packets human reviewed: ${validation.p1PacketsHumanReviewed || 0}`,
  `- P1 packets rejected: ${validation.p1PacketsRejected || 0}`,
  `- P1 packets deferred: ${validation.p1PacketsDeferred || 0}`,
  `- P1 packet review invalid records: ${validation.p1PacketReviewInvalid || 0}`,
  `- P1 packet review stale/hash mismatches: ${validation.p1PacketReviewStale || 0}`,
  `- P1 packet reviews carried forward: ${validation.p1PacketReviewsCarriedForward || 0}`,
  `- P1 packets carried forward: ${validation.p1PacketsCarriedForward || 0}`,
  `- P1 packets consumed by admission: ${validation.p1PacketsConsumedByAdmission || 0}`,
  `- P1 packets metadata-disambiguation admitted: ${validation.p1PacketsMetadataDisambiguationAdmitted || 0}`,
  `- P1 packet review missing-packet references: ${validation.p1PacketReviewReferencesMissingPacket || 0}`,
  `- P1 packet review transaction manifests: ${validation.p1PacketReviewTransactionManifests || 0}`,
  `- P1 packet review strict mode: ${validation.p1PacketReviewStrictMode ? 'enabled' : 'disabled'}`,
  `- Transaction manifests: ${validation.transactionManifests}`,
  `- Transaction manifests with afterHash: ${validation.transactionManifestsWithAfterHash || 0}`,
  `- Files under manifest custody: ${validation.filesUnderManifestCustody || 0}`,
  `- Latest manifest afterHash matches: ${validation.latestAfterHashMatches || 0}`,
  `- Latest manifest afterHash mismatches: ${validation.latestAfterHashMismatches || 0}`,
  `- Stale manifest-governed files: ${validation.staleManifestFiles || 0}`,
  `- Unmanifested mutated custody files: ${validation.unmanifestedMutatedCustodyFiles || 0}`,
  `- Latest afterHash strict mode: ${validation.latestManifestAfterHashStrictMode ? 'enabled' : 'disabled'}`,
  `- Invalid manifests: ${validation.invalidManifestCount || 0}`,
  `- Broken manifest hash chains: ${validation.brokenHashChainCount || 0}`,
  '',
  '## Concrete duplicate groups',
  '',
  concreteGroups.length
    ? concreteGroups.map((group) => `- \`${group.looseNormalizedLabel}\`: ${group.nodeIds.join(', ')} | risk=${group.riskLevel} | status=${group.status} | suggested=${group.suggestedAction}`).join('\n')
    : '- No concrete duplicate groups detected.',
  '',
  '## Blockers',
  '',
  validation.blockers.length ? validation.blockers.map((blocker) => `- ${blocker}`).join('\n') : '- None.',
  '',
  '## Warnings',
  '',
  validation.warnings.length ? validation.warnings.map((warning) => `- ${warning}`).join('\n') : '- None.',
  '',
].join('\n');

if (!noWrite) {
  writeFileSync(validationReportPath, report, 'utf-8');
}

const decisionLog = [
  '# Canonical Graph Stewardship Decision Log',
  '',
  `Date: ${new Date().toISOString()}`,
  '',
  decisions.length
    ? decisions.map((decision) => (
      `- ${decision.decisionId}: ${decision.decisionType} group=${decision.candidateGroupId} status=${decision.status} reviewer=${decision.reviewer} rationale=${decision.rationale}`
    )).join('\n')
    : '- No stewardship decisions recorded yet.',
  '',
].join('\n');
if (!noWrite) {
  writeFileSync(decisionLogPath, decisionLog, 'utf-8');
}

console.log(JSON.stringify(validation, null, 2));
if (!validation.ok) process.exit(1);
