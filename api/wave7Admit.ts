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
  { source: 'VTN-DOM-0000068', target: 'VTN-DOM-0000271', type: 'COORDINATES_WITH', rationale: 'Concrete materials coordinate with reinforced concrete for mix design, placement, and curing; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000069', target: 'VTN-DOM-0000274', type: 'COORDINATES_WITH', rationale: 'Steel materials coordinate with steel structures for grades, connections, and corrosion protection; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000070', target: 'VTN-DOM-0000278', type: 'COORDINATES_WITH', rationale: 'Timber materials coordinate with timber structures for species, grades, and moisture; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000071', target: 'VTN-DOM-0002983', type: 'COORDINATES_WITH', rationale: 'Masonry materials coordinate with masonry structures for units, mortar, and reinforcement; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000068', target: 'VTN-DOM-0000273', type: 'COORDINATES_WITH', rationale: 'Concrete materials coordinate with precast concrete for mix design, placement, and curing; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000087', target: 'VTN-DOM-0003191', type: 'COORDINATES_WITH', rationale: 'Water sustainability coordinates with water service for efficiency, metering, and reuse; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000087', target: 'VTN-DOM-0000054', type: 'COORDINATES_WITH', rationale: 'Water sustainability coordinates with wastewater for efficiency, metering, and reuse; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000063', target: 'VTN-DOM-0000255', type: 'COORDINATES_WITH', rationale: 'Construction sequencing coordinates with frame systems for erection, bracing, and safety; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000063', target: 'VTN-DOM-0000271', type: 'COORDINATES_WITH', rationale: 'Construction sequencing coordinates with reinforced concrete for formwork, curing, and stripping; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000065', target: 'VTN-DOM-0000032', type: 'COORDINATES_WITH', rationale: 'Quality assurance coordinates with foundations for inspection, testing, and acceptance; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000066', target: 'VTN-DOM-0000063', type: 'COORDINATES_WITH', rationale: 'Construction safety coordinates with sequencing for hazard control, access, and protection; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000102', target: 'VTN-DOM-0003191', type: 'COORDINATES_WITH', rationale: 'Facilities operations coordinate with water service for maintenance, scheduling, and performance; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000102', target: 'VTN-DOM-0000433', type: 'COORDINATES_WITH', rationale: 'Facilities operations coordinate with detection systems for testing, maintenance, and inspection; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000826', target: 'VTN-DOM-0000369', type: 'COORDINATES_WITH', rationale: 'Access control coordinates with data networks for integration, protocols, and points; non-numerical and non-code-specific.' },
  { source: 'VTN-DOM-0000018', target: 'VTN-DOM-0002776', type: 'COORDINATES_WITH', rationale: 'Zoning coordinates with building typologies for use, density, and height; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000204', target: 'VTN-DOM-0002777', type: 'COORDINATES_WITH', rationale: 'Housing planning coordinates with healthcare architecture for accessibility, services, and amenities; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000212', target: 'VTN-DOM-0000025', type: 'COORDINATES_WITH', rationale: 'Resilience planning coordinates with drainage for flooding, capacity, and adaptation; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0000212', target: 'VTN-DOM-0000436', type: 'COORDINATES_WITH', rationale: 'Resilience planning coordinates with exits for emergency access, evacuation, and safety; non-numerical and non-jurisdiction-specific.' },
  { source: 'VTN-DOM-0003075', target: 'VTN-DOM-0000330', type: 'CONVEYS', rationale: 'Air handling units convey air to zoning as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.' },
  { source: 'VTN-DOM-0000330', target: 'VTN-DOM-0003081', type: 'CONVEYS', rationale: 'Zoning conveys air to diffusers and terminal devices as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.' },
  { source: 'VTN-DOM-0003191', target: 'VTN-DOM-0000411', type: 'CONVEYS', rationale: 'Water service conveys water to water heating as a general plumbing supply relationship; no fixture-unit or pressure claim.' },
];

const relationships = baseCandidates.map((c) => ({
  sourceNodeId: c.source,
  targetNodeId: c.target,
  relationType: c.type as any,
  rationale: c.rationale,
  direction: 'outgoing',
  confidence: 'steward_approved',
  weight: 0.5,
  category: 'semantic/aec-mechanism',
}));

const decisionRequest = {
  candidateId: 'wave7-materials-sustainability-construction-urban-mepfs',
  reviewer: 'project-owner',
  rationale: 'Phase 4 Wave 7 ACS graph enrichment: materials-to-systems, sustainability-to-MEPFS, construction sequencing, urban planning, and MEPFS flow connections. All relationships are non-numerical, non-code-specific, and non-jurisdiction-specific. Pre-screened against existing base and admitted edges: 0 duplicates, 0 conflicts.',
  notes: 'Wave 7 generated from systematic domain exploration. 21 base candidates. No Resource Layer mutation, no node merge, no alias/redirect/tombstone.',
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
  approvalRationale: 'Steward-approved batch admission of 21 Wave 7 relationships. All candidates pre-screened against existing edges with 0 duplicates and 0 conflicts. Relation families: COORDINATES_WITH, CONVEYS. Non-destructive edge admission only.',
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
