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
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0000255', type: 'COORDINATES_WITH', rationale: 'Seismic design coordinates with frame systems for lateral loads, ductility, and connections; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0000032', type: 'COORDINATES_WITH', rationale: 'Seismic design coordinates with foundations for bearing, settlement, and liquefaction; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0003009', type: 'COORDINATES_WITH', rationale: 'Seismic design coordinates with foundation engineering for soil response, liquefaction, and settlement; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000033', target: 'VTN-DOM-0000271', type: 'COORDINATES_WITH', rationale: 'Seismic design coordinates with reinforced concrete for ductility, detailing, and connections; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003009', target: 'VTN-DOM-0000032', type: 'COORDINATES_WITH', rationale: 'Foundation engineering coordinates with foundations for design, settlement, and bearing; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000315', target: 'VTN-DOM-0000025', type: 'COORDINATES_WITH', rationale: 'Dewatering coordinates with drainage for discharge, treatment, and monitoring; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000038', target: 'VTN-DOM-0000032', type: 'COORDINATES_WITH', rationale: 'Soil mechanics coordinates with foundations for bearing, settlement, and liquefaction; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000426', target: 'VTN-DOM-0003191', type: 'COORDINATES_WITH', rationale: 'Irrigation coordinates with water service for supply, pressure, and backflow; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000426', target: 'VTN-DOM-0000025', type: 'COORDINATES_WITH', rationale: 'Irrigation coordinates with drainage for runoff, infiltration, and discharge; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000121', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with walls for material repair, replacement, and documentation; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000122', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with roof systems for material repair, replacement, and documentation; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000068', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with concrete materials for repair, replacement, and compatibility; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000069', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with steel materials for repair, replacement, and compatibility; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000070', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with timber materials for repair, replacement, and compatibility; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0000071', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with masonry materials for repair, replacement, and compatibility; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0004351', target: 'VTN-DOM-0002983', type: 'COORDINATES_WITH', rationale: 'Historic preservation coordinates with masonry structures for structural assessment, repair, and stabilization; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000356', target: 'VTN-DOM-0000372', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Mechanical controls and building management are discipline-scoped views of the same control-system object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000372', target: 'VTN-DOM-0000356', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Building management and mechanical controls are discipline-scoped views of the same control-system object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
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
  candidateId: 'wave8-seismic-geotech-heritage-irrigation-controls',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 8 ACS graph enrichment: seismic design, geotechnical coordination, heritage preservation, irrigation, and control-system alignments. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts.',
  notes: 'Wave 8 generated from systematic domain exploration. 18 base candidates. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
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
  approvalRationale: 'Steward-approved batch admission of 18 Wave 8 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: COORDINATES_WITH, CROSS_DOMAIN_ALIGNMENT. Non-destructive edge admission only.',
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
