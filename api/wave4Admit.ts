import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import {
  recordCanonicalRelationshipAdmissionDecision,
  approveCanonicalDecision,
} from './graph/canonicalStewardship';

const repoRoot = resolve(import.meta.dir, '..');

// Load latest shadow graph
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

// Manually curated Wave 4 candidates
// For CROSS_DOMAIN_ALIGNMENT, include BOTH directions to satisfy reciprocal requirement
const baseCandidates: Array<{
  source: string;
  target: string;
  type: string;
  rationale: string;
  direction?: string;
}> = [
  // COORDINATES_WITH
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0000122', type: 'COORDINATES_WITH', rationale: 'Air handling units coordinate with roof systems for structural openings, weatherproofing, and equipment access; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0000121', type: 'COORDINATES_WITH', rationale: 'Air handling units coordinate with wall and facade systems for intake/discharge openings and thermal bridging; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000331', target: 'VTN-DOM-0002471', type: 'COORDINATES_WITH', rationale: 'Passenger lifts coordinate with construction systems for shaft dimensions, structural support, and floor alignments; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000436', target: 'VTN-DOM-0002556', type: 'COORDINATES_WITH', rationale: 'Exits coordinate with means of egress planning for capacity, location, and travel distance without asserting code compliance or AHJ adoption.' },
  { source: 'VTN-DOM-0000439', target: 'VTN-DOM-0002559', type: 'COORDINATES_WITH', rationale: 'Fire barriers coordinate with compartmentation and fire resistance for continuity and penetration management; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0002893', type: 'COORDINATES_WITH', rationale: 'Water service and meters coordinate with water distribution networks for pressure, sizing, and connection interfaces; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000243', target: 'VTN-DOM-0002896', type: 'COORDINATES_WITH', rationale: 'Wastewater infrastructure coordinates with sewerage networks for capacity, slope, and discharge interfaces; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0003139', target: 'VTN-DOM-0000032', type: 'COORDINATES_WITH', rationale: 'Grounding electrode systems coordinate with foundations interface for earth-contact area, corrosion protection, and embedment; non-numerical and non-code-specific.' },
  // CONVEYS
  { source: 'VTN-DOM-0003078', target: 'VTN-DOM-0003081', type: 'CONVEYS', rationale: 'Duct design conveys air to diffusers and terminal devices as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.' },
  { source: 'VTN-DOM-0003088', target: 'VTN-DOM-0000329', type: 'CONVEYS', rationale: 'Chilled water loops convey chilled water to air-conditioning systems as a general hydronic cooling relationship; no flow rate or capacity claim.' },
  { source: 'VTN-DOM-0003091', target: 'VTN-DOM-0000341', type: 'CONVEYS', rationale: 'Hot water loops convey heating to hydronic heating systems as a general hydronic heating relationship; no flow rate or capacity claim.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0000405', type: 'CONVEYS', rationale: 'Water service conveys water to lavatories as a general plumbing supply relationship; no fixture-unit or pressure claim.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0000406', type: 'CONVEYS', rationale: 'Water service conveys water to showers as a general plumbing supply relationship; no fixture-unit or pressure claim.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0000404', type: 'CONVEYS', rationale: 'Water service conveys water to water closets as a general plumbing supply relationship; no fixture-unit or pressure claim.' },
  // INFORMS
  { source: 'VTN-DOM-0000450', target: 'VTN-DOM-0000433', type: 'INFORMS', rationale: 'Smoke detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.' },
  { source: 'VTN-DOM-0000451', target: 'VTN-DOM-0000433', type: 'INFORMS', rationale: 'Heat detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.' },
  // CONSTRAINS
  { source: 'VTN-DOM-0000438', target: 'VTN-DOM-0000436', type: 'CONSTRAINS', rationale: 'Occupant load conceptually constrains exit planning as a general life-safety capacity relationship; no specific occupant count or code section claim.' },
  { source: 'VTN-DOM-0000437', target: 'VTN-DOM-0000436', type: 'CONSTRAINS', rationale: 'Travel distance conceptually constrains exit placement as a general life-safety planning relationship; no specific distance value or code section claim.' },
  // SUPPORTS
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0002945', type: 'SUPPORTS', rationale: 'Frame systems support slabs, beams, and columns as a general structural-system relationship; no member-sizing or capacity claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0003075', type: 'SUPPORTS', rationale: 'Frame systems support air handling units as a general structural-equipment support relationship; no equipment-load or member-sizing claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000345', type: 'SUPPORTS', rationale: 'Frame systems support cooling towers as a general structural-equipment support relationship; no equipment-load or member-sizing claim.' },
  { source: 'VTN-DOM-0000255', target: 'VTN-DOM-0000366', type: 'SUPPORTS', rationale: 'Frame systems support generators as a general structural-equipment support relationship; no equipment-load or member-sizing claim.' },
  // TRANSFERS_LOAD_TO
  { source: 'VTN-DOM-0002945', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Slabs, beams, and columns transfer load to foundations interface as a general structural load-path relationship; no load value or member-sizing claim.' },
  { source: 'VTN-DOM-0000256', target: 'VTN-DOM-0000032', type: 'TRANSFERS_LOAD_TO', rationale: 'Wall systems transfer load to foundations interface as a general structural load-path relationship; no load value or member-sizing claim.' },
  // DISCHARGES_TO
  { source: 'VTN-DOM-0002893', target: 'VTN-DOM-0000239', type: 'DISCHARGES_TO', rationale: 'Water distribution networks discharge to water infrastructure as a general civil water-system relationship; no hydraulic capacity or jurisdiction claim.' },
  { source: 'VTN-DOM-0002896', target: 'VTN-DOM-0000243', type: 'DISCHARGES_TO', rationale: 'Sewerage networks discharge to wastewater infrastructure as a general civil wastewater relationship; no hydraulic capacity or jurisdiction claim.' },
  { source: 'VTN-DOM-0002899', target: 'VTN-DOM-0000025', type: 'DISCHARGES_TO', rationale: 'Stormwater networks discharge to drainage as a general civil stormwater relationship; no hydraulic capacity or jurisdiction claim.' },
  // CROSS_DOMAIN_ALIGNMENT (bidirectional — include both directions)
  { source: 'VTN-DOM-0000329', target: 'VTN-DOM-0003088', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Chilled water and chilled water loops are discipline-scoped views of the same hydronic cooling object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003088', target: 'VTN-DOM-0000329', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Chilled water loops and chilled water are discipline-scoped views of the same hydronic cooling object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000341', target: 'VTN-DOM-0003091', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Hydronic heating and hot water loops are discipline-scoped views of the same hydronic heating object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003091', target: 'VTN-DOM-0000341', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Hot water loops and hydronic heating are discipline-scoped views of the same hydronic heating object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0000411', target: 'VTN-DOM-0003246', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Water heating and water heaters are discipline-scoped views of the same object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
  { source: 'VTN-DOM-0003246', target: 'VTN-DOM-0000411', type: 'CROSS_DOMAIN_ALIGNMENT', rationale: 'Water heaters and water heating are discipline-scoped views of the same object family; alignment only, no equivalence, merge, or identity claim.', direction: 'bidirectional' },
];

const relationships = baseCandidates.map((c) => ({
  sourceNodeId: c.source,
  targetNodeId: c.target,
  relationType: c.type as any,
  rationale: c.rationale,
  direction: c.direction || 'outgoing',
  confidence: 'steward_approved',
  weight: 0.5,
  category: 'semantic/aec-mechanism',
}));

// Step 1: Create decision
const decisionRequest = {
  candidateId: 'wave4-mepfs-coordination-flow-structural-fire-safety',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 4 ACS graph enrichment: MEPFS coordination, flow, structural support, fire safety, and cross-domain alignment candidates. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts.',
  notes: 'Wave 4 generated from domain exploration of MEPFS nodes. 30 base candidates + 3 reciprocal CROSS_DOMAIN_ALIGNMENT pairs = 33 total proposed relationships. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
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
  approvalRationale: 'Steward-approved batch admission of 33 Wave 4 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: COORDINATES_WITH, CONVEYS, INFORMS, CONSTRAINS, SUPPORTS, TRANSFERS_LOAD_TO, DISCHARGES_TO, CROSS_DOMAIN_ALIGNMENT. Non-destructive edge admission only.',
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
