import { existsSync, readFileSync, readdirSync } from 'node:fs';
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

const baseEdges = (Array.isArray(raw.edges) ? raw.edges : []).map((edge: any) => ({
  id: String(edge.id || ''),
  source: String(edge.from_id || ''),
  target: String(edge.to_id || ''),
  type: edgeType(String(edge.predicate || '')),
}));

const admittedEdges = readCanonicalAdmittedRelationships(repoRoot)
  .filter((edge) => edge.reviewStatus !== 'rolled_back');

const existingEdgeKeys = new Set<string>();
for (const edge of baseEdges) existingEdgeKeys.add(`${edge.source}|${edge.type}|${edge.target}`);
for (const edge of admittedEdges) existingEdgeKeys.add(`${edge.source}|${edge.type}|${edge.target}`);

const nodeIds = new Set<string>((raw.nodes || []).map((n: any) => String(n.id)));
const nodeLabels = new Map<string, string>();
const nodePathCodes = new Map<string, string>();
for (const n of raw.nodes || []) {
  nodeLabels.set(String(n.id), String(n.label || n.pref_label || ''));
  nodePathCodes.set(String(n.id), String(n.path_code || ''));
}

function findNode(pathCode: string): {id: string; label: string; pathCode: string} | undefined {
  for (const [id, pc] of nodePathCodes) {
    if (pc === pathCode) return { id, label: nodeLabels.get(id) || '', pathCode: pc };
  }
  return undefined;
}

const candidates: Array<{source: string; target: string; type: string; rationale: string}> = [];

function add(source: string, target: string, type: string, rationale: string) {
  if (!nodeIds.has(source) || !nodeIds.has(target)) return;
  if (source === target) return;
  const key = `${source}|${type}|${target}`;
  if (existingEdgeKeys.has(key)) return;
  candidates.push({ source, target, type, rationale });
  existingEdgeKeys.add(key);
}

function addIfFound(sourcePath: string, targetPath: string, type: string, rationale: string) {
  const s = findNode(sourcePath);
  const t = findNode(targetPath);
  if (s && t) add(s.id, t.id, type, rationale);
}

// ==========================================
// A. Acoustics / lighting / MEPFS
// ==========================================
addIfFound('ARC.ACO', 'ARC.CEL', 'COORDINATES_WITH', 'Acoustics coordinate with ceiling plenums for absorption, isolation, and HVAC noise; non-numerical and non-code-specific.');
addIfFound('ARC.ACO', 'MEC.AHD.AHU', 'COORDINATES_WITH', 'Acoustics coordinate with air handling units for noise, vibration, and isolation; non-numerical and non-code-specific.');
addIfFound('ARC.LIG', 'ELE.LIG', 'COORDINATES_WITH', 'Lighting design coordinates with electrical lighting for power, controls, and dimming; non-numerical and non-code-specific.');
addIfFound('ARC.LIG', 'ARC.CEL', 'COORDINATES_WITH', 'Lighting design coordinates with ceiling plenums for mounting, access, and thermal management; non-numerical and non-code-specific.');
addIfFound('ARC.LIG', 'ARC.INT.CEL', 'COORDINATES_WITH', 'Lighting design coordinates with interior ceilings for mounting, access, and thermal management; non-numerical and non-code-specific.');
addIfFound('ARC.LIG', 'SUS.DAY', 'COORDINATES_WITH', 'Lighting design coordinates with daylight sustainability for integration, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('ARC.ACO', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Acoustics coordinate with walls for insulation, mass, and isolation; non-numerical and non-code-specific.');
addIfFound('ARC.ACO', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Acoustics coordinate with windows for glazing, mass, and isolation; non-numerical and non-code-specific.');
addIfFound('ELE.LIG', 'ELE.SES', 'COORDINATES_WITH', 'Electrical lighting coordinates with electrical service for power, circuits, and controls; non-numerical and non-code-specific.');
addIfFound('ELE.LIG', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'Electrical lighting coordinates with building management for integration, protocols, and sensors; non-numerical and non-code-specific.');

// ==========================================
// B. Seismic / wind / structural
// ==========================================
addIfFound('STR.SEI', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Seismic design coordinates with frame systems for lateral loads, ductility, and connections; non-numerical and non-code-specific.');
addIfFound('STR.WIN', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Wind design coordinates with frame systems for lateral loads, pressure, and connections; non-numerical and non-code-specific.');
addIfFound('STR.SEI', 'STR.FND', 'COORDINATES_WITH', 'Seismic design coordinates with foundations for bearing, settlement, and liquefaction; non-numerical and non-code-specific.');
addIfFound('STR.WIN', 'ARC.ENV.ROF', 'COORDINATES_WITH', 'Wind design coordinates with roof systems for uplift, pressure, and connections; non-numerical and non-code-specific.');
addIfFound('STR.SEI', 'GEO.FOE', 'COORDINATES_WITH', 'Seismic design coordinates with foundation engineering for soil response, liquefaction, and settlement; non-numerical and non-jurisdiction-specific.');
addIfFound('STR.WIN', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Wind design coordinates with walls for pressure, suction, and connections; non-numerical and non-code-specific.');
addIfFound('STR.SEI', 'STR.CON.RCO', 'COORDINATES_WITH', 'Seismic design coordinates with reinforced concrete for ductility, detailing, and connections; non-numerical and non-code-specific.');
addIfFound('STR.WIN', 'STR.STL', 'COORDINATES_WITH', 'Wind design coordinates with steel structures for connections, bracing, and fatigue; non-numerical and non-code-specific.');

// ==========================================
// C. Geotechnical / excavation / civil
// ==========================================
addIfFound('GEO.FOE', 'STR.FND', 'COORDINATES_WITH', 'Foundation engineering coordinates with foundations for design, settlement, and bearing; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.FOE.SHA', 'STR.FND.SHA', 'CROSS_DOMAIN_ALIGNMENT', 'Shallow foundation engineering and shallow foundations are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('STR.FND.SHA', 'GEO.FOE.SHA', 'CROSS_DOMAIN_ALIGNMENT', 'Shallow foundations and shallow foundation engineering are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('GEO.EXC', 'CIV.FND', 'COORDINATES_WITH', 'Excavation support coordinates with foundation excavation for shoring, dewatering, and sequencing; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.EXC.SHR', 'CIV.FND', 'COORDINATES_WITH', 'Shoring coordinates with foundation excavation for earth retention, dewatering, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.EXC.DWT', 'CIV.DRN', 'COORDINATES_WITH', 'Dewatering coordinates with drainage for discharge, treatment, and monitoring; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.SOI', 'STR.FND', 'COORDINATES_WITH', 'Soil mechanics coordinates with foundations for bearing, settlement, and liquefaction; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.SOI', 'CIV.SIT.GRA', 'COORDINATES_WITH', 'Soil mechanics coordinates with site grading for compaction, drainage, and stabilization; non-numerical and non-jurisdiction-specific.');
addIfFound('GEO.RET', 'STR.RET', 'COORDINATES_WITH', 'Retaining wall engineering coordinates with retaining walls for design, drainage, and settlement; non-numerical and non-jurisdiction-specific.');

// ==========================================
// D. Commissioning / testing / MEPFS
// ==========================================
addIfFound('MEC.COM', 'MEC.AHD.AHU', 'COORDINATES_WITH', 'Commissioning coordinates with air handling units for testing, balancing, and acceptance; non-numerical and non-code-specific.');
addIfFound('MEC.COM', 'MEC.HPS.BOI', 'COORDINATES_WITH', 'Commissioning coordinates with boilers for testing, tuning, and acceptance; non-numerical and non-code-specific.');
addIfFound('MEC.COM', 'MEC.COO.CTW', 'COORDINATES_WITH', 'Commissioning coordinates with cooling towers for testing, balancing, and acceptance; non-numerical and non-code-specific.');
addIfFound('ELE.COM2', 'ELE.SES', 'COORDINATES_WITH', 'Electrical commissioning coordinates with electrical service for testing, protection, and acceptance; non-numerical and non-code-specific.');
addIfFound('ELE.COM2', 'ELE.EPW.GEN', 'COORDINATES_WITH', 'Electrical commissioning coordinates with generators for testing, transfer, and acceptance; non-numerical and non-code-specific.');
addIfFound('PLS.COM', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Plumbing commissioning coordinates with water service for testing, flushing, and acceptance; non-numerical and non-code-specific.');
addIfFound('PLS.COM', 'PLS.HOT.WHE', 'COORDINATES_WITH', 'Plumbing commissioning coordinates with water heating for testing, tuning, and acceptance; non-numerical and non-code-specific.');
addIfFound('FLS.COM', 'FLS.SPR', 'COORDINATES_WITH', 'Fire commissioning coordinates with sprinkler systems for testing, flow, and acceptance; non-numerical and non-code-specific.');
addIfFound('FLS.COM', 'FLS.ALM.DET', 'COORDINATES_WITH', 'Fire commissioning coordinates with detection systems for testing, sensitivity, and acceptance; non-numerical and non-code-specific.');
addIfFound('MEC.COM', 'MEC.CTL', 'COORDINATES_WITH', 'Commissioning coordinates with mechanical controls for testing, calibration, and acceptance; non-numerical and non-code-specific.');

// ==========================================
// E. Landscape / irrigation / civil
// ==========================================
addIfFound('ARC.LAN', 'CIV.SIT.GRA', 'COORDINATES_WITH', 'Landscape architecture coordinates with site grading for drainage, irrigation, and planting; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'CIV.DRN', 'COORDINATES_WITH', 'Landscape architecture coordinates with drainage for runoff, infiltration, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Landscape architecture coordinates with water service for irrigation, metering, and backflow; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'SUS.SIT', 'COORDINATES_WITH', 'Landscape architecture coordinates with site sustainability for native plants, permeability, and habitat; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'CIV.UTI', 'COORDINATES_WITH', 'Landscape architecture coordinates with utilities for routing, protection, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Landscape architecture coordinates with building pads for grading, drainage, and irrigation; non-numerical and non-jurisdiction-specific.');
addIfFound('PLS.IRR', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Irrigation coordinates with water service for supply, pressure, and backflow; non-numerical and non-jurisdiction-specific.');
addIfFound('PLS.IRR', 'CIV.DRN', 'COORDINATES_WITH', 'Irrigation coordinates with drainage for runoff, infiltration, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.LAN', 'ARC.ACC', 'COORDINATES_WITH', 'Landscape architecture coordinates with accessible routes for paths, seating, and wayfinding; non-numerical and non-code-specific.');

// ==========================================
// F. Energy modeling / performance / MEPFS
// ==========================================
addIfFound('MEC.LOA', 'MEC.AHD.AHU', 'COORDINATES_WITH', 'Load calculations coordinate with air handling units for sizing, zoning, and diversity; non-numerical and non-code-specific.');
addIfFound('MEC.LOA', 'MEC.HPS.BOI', 'COORDINATES_WITH', 'Load calculations coordinate with boilers for sizing, zoning, and diversity; non-numerical and non-code-specific.');
addIfFound('MEC.LOA', 'MEC.COO.CTW', 'COORDINATES_WITH', 'Load calculations coordinate with cooling towers for sizing, zoning, and diversity; non-numerical and non-code-specific.');
addIfFound('MEC.LOA', 'MEC.ACD', 'COORDINATES_WITH', 'Load calculations coordinate with air-conditioning for sizing, zoning, and diversity; non-numerical and non-code-specific.');
addIfFound('MEC.LOA', 'MEC.HEA', 'COORDINATES_WITH', 'Load calculations coordinate with heating for sizing, zoning, and diversity; non-numerical and non-code-specific.');
addIfFound('ELE.LOA', 'ELE.SES', 'COORDINATES_WITH', 'Electrical load calculations coordinate with electrical service for sizing, diversity, and demand; non-numerical and non-code-specific.');
addIfFound('ELE.LOA', 'ELE.EPW', 'COORDINATES_WITH', 'Electrical load calculations coordinate with emergency power for sizing, diversity, and demand; non-numerical and non-code-specific.');
addIfFound('SUS.ENE', 'MEC.LOA', 'COORDINATES_WITH', 'Energy sustainability coordinates with load calculations for efficiency, diversity, and demand; non-numerical and non-code-specific.');
addIfFound('SUS.ENE', 'ELE.LOA', 'COORDINATES_WITH', 'Energy sustainability coordinates with electrical load calculations for efficiency, diversity, and demand; non-numerical and non-code-specific.');
addIfFound('SUS.ENE', 'ARC.ENV.INS', 'COORDINATES_WITH', 'Energy sustainability coordinates with insulation for thermal performance, air sealing, and condensation; non-numerical and non-code-specific.');

// ==========================================
// G. Historic / preservation / architecture
// ==========================================
addIfFound('HRC.HIS', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Historic preservation coordinates with walls for material repair, replacement, and documentation; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'ARC.ENV.ROF', 'COORDINATES_WITH', 'Historic preservation coordinates with roof systems for material repair, replacement, and documentation; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Historic preservation coordinates with windows for glazing repair, replacement, and documentation; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'ARC.FIN', 'COORDINATES_WITH', 'Historic preservation coordinates with finishes for material repair, replacement, and documentation; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'MAT.CON', 'COORDINATES_WITH', 'Historic preservation coordinates with concrete materials for repair, replacement, and compatibility; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'MAT.STE', 'COORDINATES_WITH', 'Historic preservation coordinates with steel materials for repair, replacement, and compatibility; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'MAT.TIM', 'COORDINATES_WITH', 'Historic preservation coordinates with timber materials for repair, replacement, and compatibility; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'MAT.MAS', 'COORDINATES_WITH', 'Historic preservation coordinates with masonry materials for repair, replacement, and compatibility; non-numerical and non-code-specific.');
addIfFound('HRC.HIS', 'STR.TMA', 'COORDINATES_WITH', 'Historic preservation coordinates with masonry structures for structural assessment, repair, and stabilization; non-numerical and non-code-specific.');

// ==========================================
// H. Additional cross-domain alignments
// ==========================================
addIfFound('ARC.ENV.WAL', 'ARC.ENV.WAL.FAC', 'CROSS_DOMAIN_ALIGNMENT', 'Walls and facade systems are discipline-scoped views of the same enclosure object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ARC.ENV.WAL.FAC', 'ARC.ENV.WAL', 'CROSS_DOMAIN_ALIGNMENT', 'Facade systems and walls are discipline-scoped views of the same enclosure object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('MEC.HPS.CWL', 'MEC.ACD.CHW', 'CROSS_DOMAIN_ALIGNMENT', 'Chilled water loops and chilled water are discipline-scoped views of the same hydronic cooling object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('MEC.ACD.CHW', 'MEC.HPS.CWL', 'CROSS_DOMAIN_ALIGNMENT', 'Chilled water and chilled water loops are discipline-scoped views of the same hydronic cooling object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ELE.SES', 'ELE.UTI', 'CROSS_DOMAIN_ALIGNMENT', 'Electrical service and utility service are discipline-scoped views of the same electrical supply object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ELE.UTI', 'ELE.SES', 'CROSS_DOMAIN_ALIGNMENT', 'Utility service and electrical service are discipline-scoped views of the same electrical supply object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('PLS.WST', 'PLS.WST.SAN', 'CROSS_DOMAIN_ALIGNMENT', 'Wastewater and sanitary drainage are discipline-scoped views of the same drainage object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('PLS.WST.SAN', 'PLS.WST', 'CROSS_DOMAIN_ALIGNMENT', 'Sanitary drainage and wastewater are discipline-scoped views of the same drainage object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('MEC.CTL', 'ELE.CTL.BMS', 'CROSS_DOMAIN_ALIGNMENT', 'Mechanical controls and building management are discipline-scoped views of the same control-system object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ELE.CTL.BMS', 'MEC.CTL', 'CROSS_DOMAIN_ALIGNMENT', 'Building management and mechanical controls are discipline-scoped views of the same control-system object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');

// ==========================================
// Output
// ==========================================
console.log(JSON.stringify({
  totalCandidates: candidates.length,
  byType: candidates.reduce((acc, c) => {
    acc[c.type] = (acc[c.type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>),
  candidates: candidates.map(c => ({
    source: c.source,
    sourceLabel: nodeLabels.get(c.source),
    target: c.target,
    targetLabel: nodeLabels.get(c.target),
    type: c.type,
    rationale: c.rationale,
  })),
}, null, 2));
