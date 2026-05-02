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
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000256', type: 'COORDINATES_WITH', rationale: 'Frame systems coordinate with wall systems for lateral stability, expansion joints, and load transfer; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000256', target: 'VTN-DOM-0000255', type: 'COORDINATES_WITH', rationale: 'Wall systems coordinate with frame systems for lateral stability, expansion joints, and load transfer; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000274', type: 'SUPPORTS', rationale: 'Frame systems support steel structures as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000278', type: 'SUPPORTS', rationale: 'Frame systems support timber structures as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0002983', type: 'SUPPORTS', rationale: 'Frame systems support masonry structures as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000274', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Steel structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000278', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Timber structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0002983', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Masonry structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000274', target: 'VTN-DOM-0000255', type: 'COORDINATES_WITH', rationale: 'Steel structures coordinate with frame systems for connections, bracing, and fire protection; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000278', target: 'VTN-DOM-0000255', type: 'COORDINATES_WITH', rationale: 'Timber structures coordinate with frame systems for connections, bracing, and fire protection; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0002983', target: 'VTN-DOM-0000256', type: 'COORDINATES_WITH', rationale: 'Masonry structures coordinate with wall systems for lateral support, expansion joints, and moisture control; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000251', target: 'VTN-DOM-0000025', type: 'COORDINATES_WITH', rationale: 'Pavements coordinate with drainage for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000250', target: 'VTN-DOM-0000255', type: 'SUPPORTS', rationale: 'Deck systems are supported by frame systems as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000248', target: 'VTN-DOM-0000255', type: 'SUPPORTS', rationale: 'Spans are supported by frame systems as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000249', target: 'VTN-DOM-0003009', type: 'COORDINATES_WITH', rationale: 'Abutments coordinate with foundation engineering for bearing, settlement, and drainage; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0002802', target: 'VTN-DOM-0002542', type: 'COORDINATES_WITH', rationale: 'Accessible built environment audits coordinate with accessible routes for compliance, wayfinding, and usability; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000181', target: 'VTN-DOM-0002542', type: 'COORDINATES_WITH', rationale: 'Aging and inclusive use coordinate with accessible routes for wayfinding, rest, and support; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0002812', target: 'VTN-DOM-0000405', type: 'COORDINATES_WITH', rationale: 'Accessible toilet checks coordinate with lavatories for clearances, grab bars, and fixtures; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000122', target: 'VTN-DOM-0000121', type: 'COORDINATES_WITH', rationale: 'Roof systems coordinate with walls for flashing, thermal bridging, and air barrier; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000121', target: 'VTN-DOM-0000122', type: 'COORDINATES_WITH', rationale: 'Walls coordinate with roof systems for flashing, thermal bridging, and air barrier; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000121', target: 'VTN-DOM-0003078', type: 'COORDINATES_WITH', rationale: 'Walls coordinate with ductwork for penetrations, fire stopping, and thermal bridging; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000122', target: 'VTN-DOM-0003078', type: 'COORDINATES_WITH', rationale: 'Roof systems coordinate with ductwork for penetrations, curbs, and weatherproofing; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000369', target: 'VTN-DOM-0000372', type: 'COORDINATES_WITH', rationale: 'Data networks coordinate with building management for integration, protocols, and points; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000370', target: 'VTN-DOM-0000372', type: 'COORDINATES_WITH', rationale: 'Voice systems coordinate with building management for integration, protocols, and points; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003291', target: 'VTN-DOM-0000433', type: 'COORDINATES_WITH', rationale: 'Clean agent systems coordinate with detection systems for response timing and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000434', target: 'VTN-DOM-0000046', type: 'SUPPORTS', rationale: 'Notification systems are supported by emergency power as a general life-safety power relationship; no capacity or circuit claim.' },
  { source: 'VTN-DOM-0000005', target: 'VTN-DOM-0003075', type: 'CONVEYS', rationale: 'Ventilation conveys air to air handling units as a general HVAC air-moving relationship; no airflow rate or duct-sizing claim.' },
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0000005', type: 'COORDINATES_WITH', rationale: 'Air handling units coordinate with ventilation for sizing, controls, and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000041', target: 'VTN-DOM-0003075', type: 'COORDINATES_WITH', rationale: 'Air-conditioning coordinates with air handling units for sizing, controls, and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000344', target: 'VTN-DOM-0003088', type: 'COORDINATES_WITH', rationale: 'Cooling coordinates with chilled water loops for sizing, controls, and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000411', target: 'VTN-DOM-0000414', type: 'COORDINATES_WITH', rationale: 'Water heating coordinates with fuel gas for combustion air, venting, and controls; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000025', target: 'VTN-DOM-0000054', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Drainage and wastewater are discipline-scoped views of the same water-disposal object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000054', target: 'VTN-DOM-0000025', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Wastewater and drainage are discipline-scoped views of the same water-disposal object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
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
  candidateId: 'wave6-structural-civil-accessibility-envelope-mepfs',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 6 ACS graph enrichment: structural systems, civil interfaces, accessibility coordination, building envelope, and MEPFS cross-links. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts.',
  notes: 'Wave 6 generated from systematic domain exploration. 33 base candidates. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
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
  approvalRationale: 'Steward-approved batch admission of 33 Wave 6 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: COORDINATES_WITH, SUPPORTS, TRANSFERS_LOAD_TO, CONVEYS, CROSS_DOMAIN_ALIGNMENT. Non-destructive edge admission only.',
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
