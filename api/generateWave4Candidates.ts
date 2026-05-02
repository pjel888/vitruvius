import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { readCanonicalAdmittedRelationships } from './graph/canonicalStewardship';

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

function edgeType(predicate: string) {
  return predicate === 'broader_than'
    ? 'HAS_CHILD'
    : predicate.toUpperCase().replace(/[^A-Z0-9]+/g, '_');
}

const graphPath = latestShadowGraphPath();
const raw = JSON.parse(readFileSync(graphPath, 'utf-8'));

const baseEdges: Array<{ id: string; source: string; target: string; type: string }> =
  (Array.isArray(raw.edges) ? raw.edges : []).map((edge: any) => ({
    id: String(edge.id || ''),
    source: String(edge.from_id || ''),
    target: String(edge.to_id || ''),
    type: edgeType(String(edge.predicate || '')),
  }));

const admittedEdges = readCanonicalAdmittedRelationships(repoRoot)
  .filter((edge) => edge.reviewStatus !== 'rolled_back');

const existingEdgeKeys = new Set<string>();
for (const edge of baseEdges) {
  existingEdgeKeys.add(`${edge.source}|${edge.type}|${edge.target}`);
}
for (const edge of admittedEdges) {
  existingEdgeKeys.add(`${edge.source}|${edge.type}|${edge.target}`);
}

// Manually curated Wave 4 candidates
// Format: [sourceId, targetId, relationType, rationale]
const candidates: Array<[string, string, string, string]> = [
  // MEPFS coordination
  ['VTN-DOM-0003075', 'VTN-DOM-0000122', 'COORDINATES_WITH', 'Air handling units coordinate with roof systems for structural openings, weatherproofing, and equipment access; non-numerical and non-code-specific.'],
  ['VTN-DOM-0003075', 'VTN-DOM-0000121', 'COORDINATES_WITH', 'Air handling units coordinate with wall and facade systems for intake/discharge openings and thermal bridging; non-numerical and non-code-specific.'],
  ['VTN-DOM-0000331', 'VTN-DOM-0002471', 'COORDINATES_WITH', 'Passenger lifts coordinate with construction systems for shaft dimensions, structural support, and floor alignments; non-numerical and non-code-specific.'],
  ['VTN-DOM-0000436', 'VTN-DOM-0002556', 'COORDINATES_WITH', 'Exits coordinate with means of egress planning for capacity, location, and travel distance without asserting code compliance or AHJ adoption.'],
  ['VTN-DOM-0000439', 'VTN-DOM-0002559', 'COORDINATES_WITH', 'Fire barriers coordinate with compartmentation and fire resistance for continuity and penetration management; non-numerical and non-code-specific.'],
  ['VTN-DOM-0003191', 'VTN-DOM-0002893', 'COORDINATES_WITH', 'Water service and meters coordinate with water distribution networks for pressure, sizing, and connection interfaces; non-numerical and non-jurisdiction-specific.'],
  ['VTN-DOM-0000243', 'VTN-DOM-0002896', 'COORDINATES_WITH', 'Wastewater infrastructure coordinates with sewerage networks for capacity, slope, and discharge interfaces; non-numerical and non-jurisdiction-specific.'],
  ['VTN-DOM-0003139', 'VTN-DOM-0000032', 'COORDINATES_WITH', 'Grounding electrode systems coordinate with foundations interface for earth-contact area, corrosion protection, and embedment; non-numerical and non-code-specific.'],
  
  // MEP flow
  ['VTN-DOM-0003078', 'VTN-DOM-0003081', 'CONVEYS', 'Duct design conveys air to diffusers and terminal devices as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.'],
  ['VTN-DOM-0003088', 'VTN-DOM-0000329', 'CONVEYS', 'Chilled water loops convey chilled water to air-conditioning systems as a general hydronic cooling relationship; no flow rate or capacity claim.'],
  ['VTN-DOM-0003091', 'VTN-DOM-0000341', 'CONVEYS', 'Hot water loops convey heating to hydronic heating systems as a general hydronic heating relationship; no flow rate or capacity claim.'],
  ['VTN-DOM-0003191', 'VTN-DOM-0000405', 'CONVEYS', 'Water service conveys water to lavatories as a general plumbing supply relationship; no fixture-unit or pressure claim.'],
  ['VTN-DOM-0003191', 'VTN-DOM-0000406', 'CONVEYS', 'Water service conveys water to showers as a general plumbing supply relationship; no fixture-unit or pressure claim.'],
  ['VTN-DOM-0003191', 'VTN-DOM-0000404', 'CONVEYS', 'Water service conveys water to water closets as a general plumbing supply relationship; no fixture-unit or pressure claim.'],
  
  // Fire/life safety
  ['VTN-DOM-0000450', 'VTN-DOM-0000433', 'INFORMS', 'Smoke detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.'],
  ['VTN-DOM-0000451', 'VTN-DOM-0000433', 'INFORMS', 'Heat detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.'],
  ['VTN-DOM-0000438', 'VTN-DOM-0000436', 'CONSTRAINS', 'Occupant load conceptually constrains exit planning as a general life-safety capacity relationship; no specific occupant count or code section claim.'],
  ['VTN-DOM-0000437', 'VTN-DOM-0000436', 'CONSTRAINS', 'Travel distance conceptually constrains exit placement as a general life-safety planning relationship; no specific distance value or code section claim.'],
  
  // Structural support/transfer
  ['VTN-DOM-0000255', 'VTN-DOM-0002945', 'SUPPORTS', 'Frame systems support slabs, beams, and columns as a general structural-system relationship; no member-sizing or capacity claim.'],
  ['VTN-DOM-0002945', 'VTN-DOM-0000032', 'TRANSFERS_LOAD_TO', 'Slabs, beams, and columns transfer load to foundations interface as a general structural load-path relationship; no load value or member-sizing claim.'],
  ['VTN-DOM-0000256', 'VTN-DOM-0000032', 'TRANSFERS_LOAD_TO', 'Wall systems transfer load to foundations interface as a general structural load-path relationship; no load value or member-sizing claim.'],
  ['VTN-DOM-0000255', 'VTN-DOM-0003075', 'SUPPORTS', 'Frame systems support air handling units as a general structural-equipment support relationship; no equipment-load or member-sizing claim.'],
  ['VTN-DOM-0000255', 'VTN-DOM-0000345', 'SUPPORTS', 'Frame systems support cooling towers as a general structural-equipment support relationship; no equipment-load or member-sizing claim.'],
  ['VTN-DOM-0000255', 'VTN-DOM-0000366', 'SUPPORTS', 'Frame systems support generators as a general structural-equipment support relationship; no equipment-load or member-sizing claim.'],
  
  // Civil drainage
  ['VTN-DOM-0002893', 'VTN-DOM-0000239', 'DISCHARGES_TO', 'Water distribution networks discharge to water infrastructure as a general civil water-system relationship; no hydraulic capacity or jurisdiction claim.'],
  ['VTN-DOM-0002896', 'VTN-DOM-0000243', 'DISCHARGES_TO', 'Sewerage networks discharge to wastewater infrastructure as a general civil wastewater relationship; no hydraulic capacity or jurisdiction claim.'],
  ['VTN-DOM-0002899', 'VTN-DOM-0000025', 'DISCHARGES_TO', 'Stormwater networks discharge to drainage as a general civil stormwater relationship; no hydraulic capacity or jurisdiction claim.'],
  
  // MEPFS cross-domain
  ['VTN-DOM-0000329', 'VTN-DOM-0003088', 'CROSS_DOMAIN_ALIGNMENT', 'Chilled water and chilled water loops are discipline-scoped views of the same hydronic cooling object family; alignment only, no equivalence, merge, or identity claim.'],
  ['VTN-DOM-0000341', 'VTN-DOM-0003091', 'CROSS_DOMAIN_ALIGNMENT', 'Hydronic heating and hot water loops are discipline-scoped views of the same hydronic heating object family; alignment only, no equivalence, merge, or identity claim.'],
  ['VTN-DOM-0000411', 'VTN-DOM-0003246', 'CROSS_DOMAIN_ALIGNMENT', 'Water heating and water heaters are discipline-scoped views of the same object family; alignment only, no equivalence, merge, or identity claim.'],
];

const nodeIds = new Set<string>((raw.nodes || []).map((n: any) => String(n.id)));
const nodeLabels = new Map<string, string>();
for (const n of raw.nodes || []) {
  nodeLabels.set(String(n.id), String(n.label || n.pref_label || ''));
}

let kept = 0;
let filtered = 0;
const safeCandidates: typeof candidates = [];

for (const [source, target, type, rationale] of candidates) {
  const key = `${source}|${type}|${target}`;
  if (!nodeIds.has(source)) { filtered++; continue; }
  if (!nodeIds.has(target)) { filtered++; continue; }
  if (existingEdgeKeys.has(key)) { filtered++; continue; }
  if (source === target) { filtered++; continue; }
  safeCandidates.push([source, target, type, rationale]);
  kept++;
}

console.log(JSON.stringify({
  totalCandidates: candidates.length,
  kept,
  filtered,
  safeCandidates: safeCandidates.map(([source, target, type, rationale]) => ({
    source,
    sourceLabel: nodeLabels.get(source),
    target,
    targetLabel: nodeLabels.get(target),
    type,
    rationale,
  })),
}, null, 2));
