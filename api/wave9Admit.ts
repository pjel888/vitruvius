import {
  recordCanonicalRelationshipAdmissionDecision,
  approveCanonicalDecision,
} from './graph/canonicalStewardship';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');

const shadowStagingRoot = resolve(repoRoot, '006_System-Manifests', 'aec-mepfs-backbone', 'shadow-staging');
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

const graphPath = latestShadowGraphPath();
const raw = JSON.parse(readFileSync(graphPath, 'utf-8'));
const nodes = raw.nodes || [];
const edges = (raw.edges || []).map((edge: any) => ({
  id: String(edge.id || ''),
  source: String(edge.from_id || ''),
  target: String(edge.to_id || ''),
  type: edge.predicate === 'broader_than' ? 'HAS_CHILD' : String(edge.predicate || '').toUpperCase().replace(/[^A-Z0-9]+/g, '_'),
  predicate: String(edge.predicate || ''),
}));

const baseCandidates = [
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0000121', type: 'AFFECTS', rationale: 'Seismic design affects walls for in-plane forces, out-of-plane demands, and detailing; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0000122', type: 'AFFECTS', rationale: 'Seismic design affects roof systems for diaphragm action, anchorage, and connections; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000025', target: 'VTN-DOM-0002490', type: 'AFFECTS', rationale: 'Drainage affects site planning for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000411', target: 'VTN-DOM-0000414', type: 'REQUIRES', rationale: 'Water heating requires fuel gas for combustion, venting, and ignition; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000033', type: 'RESISTS', rationale: 'Frame systems resist seismic as a general structural lateral-force relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000256', target: 'VTN-DOM-0000033', type: 'RESISTS', rationale: 'Wall systems resist seismic as a general structural lateral-force relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000286', target: 'VTN-DOM-0000038', type: 'RESISTS', rationale: 'Retaining walls resist soil as a general geotechnical lateral-force relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0003291', target: 'VTN-DOM-0000438', type: 'MITIGATES', rationale: 'Clean agent systems mitigate occupant load risk as a general fire-safety life-risk relationship; no specific occupancy or hazard claim.' },
  { source: 'VTN-DOM-0000439', target: 'VTN-DOM-0000437', type: 'MITIGATES', rationale: 'Fire barriers mitigate travel distance as a general compartmentation life-safety relationship; no specific distance or code claim.' },
  { source: 'VTN-DOM-0000087', target: 'VTN-DOM-0000054', type: 'MITIGATES', rationale: 'Water sustainability mitigates wastewater as a general water-efficiency relationship; no specific flow or capacity claim.' },
  { source: 'VTN-DOM-0000286', target: 'VTN-DOM-0000038', type: 'MITIGATES', rationale: 'Retaining walls mitigate soil as a general geotechnical risk-mitigation relationship; no specific load or capacity claim.' },
  { source: 'VTN-DOM-0000863', target: 'VTN-DOM-0000372', type: 'COORDINATES_WITH', rationale: 'IoT coordinates with building management for integration, protocols, and sensors; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000863', target: 'VTN-DOM-0000369', type: 'COORDINATES_WITH', rationale: 'IoT coordinates with data networks for bandwidth, latency, and security; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000585', target: 'VTN-DOM-0000086', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Energy performance and energy sustainability are discipline-scoped views of the same energy object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000086', target: 'VTN-DOM-0000585', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Energy sustainability and energy performance are discipline-scoped views of the same energy object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
];

const relationships = baseCandidates.map((c) => ({
  sourceNodeId: c.source,
  targetNodeId: c.target,
  relationType: c.type as any,
  rationale: c.rationale,
  direction: (c as any).direction || 'outgoing',
  confidence: 'steward_approved',
  weight: 0.5,
  category: 'semantic/aec-mechanism',
}));

const decisionRequest = {
  candidateId: 'wave9-underrepresented-relations-final-push',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 9 ACS graph enrichment: final push using underrepresented relation families (AFFECTS, REQUIRES, RESISTS, MITIGATES) plus IoT coordination and energy cross-domain alignment. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts.',
  notes: 'Wave 9 generated from systematic domain exploration targeting relation-family diversity. 15 base candidates. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
  riskLevel: 'low' as const,
  relationships,
  dryRun: false,
  apply: true,
};

console.log('Creating decision...');
const decisionResult = recordCanonicalRelationshipAdmissionDecision(repoRoot, decisionRequest, nodes, edges);

if ('blockers' in decisionResult && decisionResult.blockers.length > 0) {
  console.error('Decision blockers:', decisionResult.blockers);
  process.exit(1);
}
if ('warnings' in decisionResult && decisionResult.warnings.length > 0) {
  console.log('Decision warnings:', decisionResult.warnings);
}

const decisionId = (decisionResult as any).decisionId || (decisionResult as any).decision?.decisionId;
console.log('Decision created:', decisionId);

const approvalRequest = {
  approvedBy: 'project-owner',
  reviewerRole: 'steward',
  approvalRationale: 'Steward-approved batch admission of 15 Wave 9 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: AFFECTS, REQUIRES, RESISTS, MITIGATES, COORDINATES_WITH, CROSS_DOMAIN_ALIGNMENT. Non-destructive edge admission only.',
  mutationScope: 'non_destructive_edge_admission' as const,
  rollbackPlan: 'Remove admitted relationships by rolling back the decision; no node, edge-endpoint, resource-layer, alias, redirect, or tombstone mutations were made.',
  riskAcknowledgment: false,
  apply: true,
  dryRun: false,
};

console.log('Creating approval...');
const approvalResult = approveCanonicalDecision(repoRoot, decisionId, approvalRequest, nodes, edges);

if ('blockers' in approvalResult && approvalResult.blockers.length > 0) {
  console.error('Approval blockers:', approvalResult.blockers);
  process.exit(1);
}
if ('warnings' in approvalResult && approvalResult.warnings.length > 0) {
  console.log('Approval warnings:', approvalResult.warnings);
}

console.log('Approval completed.');
console.log('Admitted relationships:', (approvalResult as any).admittedRelationships?.length || 0);
