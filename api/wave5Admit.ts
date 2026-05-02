import {
  recordCanonicalRelationshipAdmissionDecision,
  approveCanonicalDecision,
} from './graph/canonicalStewardship';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');

// Load shadow graph for nodes/edges
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

// Candidate list from generateWave5CandidatesV2.ts output
const baseCandidates = [
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0003078', type: 'COORDINATES_WITH', rationale: 'Air handling units coordinate with duct design for sizing, routing, and access; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0003081', type: 'COORDINATES_WITH', rationale: 'Air handling units coordinate with diffusers and terminal devices for coverage and airflow distribution; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000345', target: 'VTN-DOM-0003088', type: 'COORDINATES_WITH', rationale: 'Cooling towers coordinate with chilled water loops for piping, access, and make-up water; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003091', target: 'VTN-DOM-0000340', type: 'CONVEYS', rationale: 'Hot water loops convey heating to heating systems as a general hydronic heating relationship; no flow rate or capacity claim.' },
  { source: 'VTN-DOM-0000329', target: 'VTN-DOM-0003075', type: 'CONVEYS', rationale: 'Chilled water systems convey chilled water to air handling units as a general hydronic cooling relationship; no flow rate or capacity claim.' },
  { source: 'VTN-DOM-0000340', target: 'VTN-DOM-0003091', type: 'COORDINATES_WITH', rationale: 'Heating systems coordinate with hot water loops for piping, controls, and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000405', target: 'VTN-DOM-0000054', type: 'DISCHARGES_TO', rationale: 'Lavatories discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.' },
  { source: 'VTN-DOM-0000406', target: 'VTN-DOM-0000054', type: 'DISCHARGES_TO', rationale: 'Showers discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.' },
  { source: 'VTN-DOM-0000404', target: 'VTN-DOM-0000054', type: 'DISCHARGES_TO', rationale: 'Water closets discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.' },
  { source: 'VTN-DOM-0000054', target: 'VTN-DOM-0002896', type: 'DISCHARGES_TO', rationale: 'Wastewater discharges to sewerage networks as a general building drainage-to-sewer relationship; no capacity or slope claim.' },
  { source: 'VTN-DOM-0000411', target: 'VTN-DOM-0000405', type: 'COORDINATES_WITH', rationale: 'Water heating coordinates with lavatories for temperature, pressure, and piping; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000411', target: 'VTN-DOM-0000406', type: 'COORDINATES_WITH', rationale: 'Water heating coordinates with showers for temperature, pressure, and piping; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000414', target: 'VTN-DOM-0000411', type: 'COORDINATES_WITH', rationale: 'Fuel gas coordinates with water heating for combustion air, venting, and controls; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0002893', type: 'CONNECTS_TO', rationale: 'Water service connects to water distribution networks as a general building-to-utility water interface; no pressure or sizing claim.' },
  { source: 'VTN-DOM-0000433', target: 'VTN-DOM-0000434', type: 'INFORMS', rationale: 'Detection systems inform notification systems as a general fire-alarm-to-notification relationship; no device-specification or code-compliance claim.' },
  { source: 'VTN-DOM-0000434', target: 'VTN-DOM-0000435', type: 'COORDINATES_WITH', rationale: 'Notification systems coordinate with mass notification for coverage, audibility, and zoning; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000366', target: 'VTN-DOM-0000046', type: 'SUPPORTS', rationale: 'Generators support emergency power systems as a general emergency power equipment relationship; no capacity or runtime claim.' },
  { source: 'VTN-DOM-0000372', target: 'VTN-DOM-0000356', type: 'COORDINATES_WITH', rationale: 'Building management systems coordinate with mechanical controls for integration, protocols, and points; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000369', target: 'VTN-DOM-0000370', type: 'COORDINATES_WITH', rationale: 'Data networks coordinate with voice systems for infrastructure, pathways, and equipment rooms; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000122', target: 'VTN-DOM-0000345', type: 'SUPPORTS', rationale: 'Roof structures support cooling towers as a general structural-equipment support relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000250', target: 'VTN-DOM-0005741', type: 'COORDINATES_WITH', rationale: 'Deck systems coordinate with drainage and service interfaces for runoff and utilities; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000340', target: 'VTN-DOM-0003091', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Heating systems and hot water loops are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003091', target: 'VTN-DOM-0000340', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Hot water loops and heating systems are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000005', target: 'VTN-DOM-0003074', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Ventilation and air distribution are discipline-scoped views of the same air-moving object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003074', target: 'VTN-DOM-0000005', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Air distribution and ventilation are discipline-scoped views of the same air-moving object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003190', target: 'VTN-DOM-0003191', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Potable water systems and water service are discipline-scoped views of the same water supply object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0003190', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Water service and potable water systems are discipline-scoped views of the same water supply object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000271', type: 'SUPPORTS', rationale: 'Frame systems support reinforced concrete as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000273', type: 'SUPPORTS', rationale: 'Frame systems support precast concrete as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Frame systems transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000271', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Reinforced concrete transfers load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000273', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Precast concrete transfers load to foundations as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000054', target: 'VTN-DOM-0002896', type: 'COORDINATES_WITH', rationale: 'Wastewater coordinates with sewerage networks for capacity, slope, and discharge; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000366', target: 'VTN-DOM-0000255', type: 'SUPPORTS', rationale: 'Generators are supported by frame systems as a general structural-equipment support relationship; no equipment-load or member-sizing claim.' },
  { source: 'VTN-DOM-0000345', target: 'VTN-DOM-0000255', type: 'SUPPORTS', rationale: 'Cooling towers are supported by frame systems as a general structural-equipment support relationship; no equipment-load or member-sizing claim.' },
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

// Step 1: Create decision
const decisionRequest = {
  candidateId: 'wave5-mepfs-coordination-flow-structural-fire-safety',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 5 ACS graph enrichment: MEPFS coordination, flow, structural support, fire safety, civil interfaces, and cross-domain alignment candidates. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts. Includes first CONNECTS_TO admission.',
  notes: 'Wave 5 generated from systematic domain exploration. 35 base candidates. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
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

// Step 2: Approve decision
const approvalRequest = {
  approvedBy: 'project-owner',
  reviewerRole: 'steward',
  approvalRationale: 'Steward-approved batch admission of 35 Wave 5 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: COORDINATES_WITH, CONVEYS, DISCHARGES_TO, CONNECTS_TO, INFORMS, SUPPORTS, CROSS_DOMAIN_ALIGNMENT, TRANSFERS_LOAD_TO. Includes first CONNECTS_TO admission. Non-destructive edge admission only.',
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
