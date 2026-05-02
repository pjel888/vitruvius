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

function findNodesByPrefix(prefix: string) {
  const results: Array<{id: string; label: string; pathCode: string}> = [];
  for (const [id, pc] of nodePathCodes) {
    if (pc.startsWith(prefix)) {
      results.push({ id, label: nodeLabels.get(id) || '', pathCode: pc });
    }
  }
  return results;
}

function isConceptNode(pathCode: string) {
  const parts = pathCode.split('.');
  return parts.length <= 3;
}

function findConceptsByPrefix(prefix: string) {
  return findNodesByPrefix(prefix).filter(n => isConceptNode(n.pathCode));
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
// A. Materials → Structural / Architecture
// ==========================================
addIfFound('MAT.CON', 'STR.CON.RCO', 'COORDINATES_WITH', 'Concrete materials coordinate with reinforced concrete for mix design, placement, and curing; non-numerical and non-code-specific.');
addIfFound('MAT.STE', 'STR.STL', 'COORDINATES_WITH', 'Steel materials coordinate with steel structures for grades, connections, and corrosion protection; non-numerical and non-code-specific.');
addIfFound('MAT.TIM', 'STR.TIM', 'COORDINATES_WITH', 'Timber materials coordinate with timber structures for species, grades, and moisture; non-numerical and non-code-specific.');
addIfFound('MAT.MAS', 'STR.TMA', 'COORDINATES_WITH', 'Masonry materials coordinate with masonry structures for units, mortar, and reinforcement; non-numerical and non-code-specific.');
addIfFound('MAT.CON', 'STR.CON.PRE', 'COORDINATES_WITH', 'Concrete materials coordinate with precast concrete for mix design, placement, and curing; non-numerical and non-code-specific.');
addIfFound('MAT.GLA', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Glass materials coordinate with windows for performance, safety, and installation; non-numerical and non-code-specific.');
addIfFound('MAT.MET', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Metal materials coordinate with walls for cladding, flashing, and thermal bridging; non-numerical and non-code-specific.');
addIfFound('MAT.WOO', 'ARC.INT', 'COORDINATES_WITH', 'Wood materials coordinate with interiors for finishes, flooring, and millwork; non-numerical and non-code-specific.');
addIfFound('MAT.CER', 'ARC.INT.FLO', 'COORDINATES_WITH', 'Ceramic materials coordinate with flooring for installation, grout, and maintenance; non-numerical and non-code-specific.');
addIfFound('MAT.PLA', 'ARC.INT', 'COORDINATES_WITH', 'Plastic materials coordinate with interiors for finishes, partitions, and casework; non-numerical and non-code-specific.');

// ==========================================
// B. Sustainability / energy / MEPFS
// ==========================================
addIfFound('SUS.ENE', 'MEC.HVA', 'COORDINATES_WITH', 'Energy sustainability coordinates with HVAC for efficiency, controls, and metering; non-numerical and non-code-specific.');
addIfFound('SUS.ENE', 'ELE.SES', 'COORDINATES_WITH', 'Energy sustainability coordinates with electrical service for efficiency, metering, and renewables; non-numerical and non-code-specific.');
addIfFound('SUS.WAT', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Water sustainability coordinates with water service for efficiency, metering, and reuse; non-numerical and non-code-specific.');
addIfFound('SUS.WAT', 'PLS.WST', 'COORDINATES_WITH', 'Water sustainability coordinates with wastewater for efficiency, metering, and reuse; non-numerical and non-code-specific.');
addIfFound('SUS.DAY', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Daylight sustainability coordinates with windows for glazing, shading, and orientation; non-numerical and non-code-specific.');
addIfFound('SUS.THE', 'ARC.ENV.INS', 'COORDINATES_WITH', 'Thermal sustainability coordinates with insulation for R-value, condensation, and vapor control; non-numerical and non-code-specific.');
addIfFound('SUS.ENE', 'ARC.ENV.INS', 'COORDINATES_WITH', 'Energy sustainability coordinates with insulation for thermal performance, air sealing, and condensation; non-numerical and non-code-specific.');
addIfFound('SUS.IND', 'ARC.INT', 'COORDINATES_WITH', 'Indoor environmental quality coordinates with interiors for materials, finishes, and ventilation; non-numerical and non-code-specific.');
addIfFound('SUS.SIT', 'CIV.SIT.GRA', 'COORDINATES_WITH', 'Site sustainability coordinates with site grading for stormwater, permeability, and vegetation; non-numerical and non-jurisdiction-specific.');
addIfFound('SUS.MAT', 'MAT.CON', 'COORDINATES_WITH', 'Material sustainability coordinates with concrete materials for embodied carbon, recycled content, and local sourcing; non-numerical and non-code-specific.');

// ==========================================
// C. Construction / project management
// ==========================================
addIfFound('CON.PMC', 'ARC.PRA', 'COORDINATES_WITH', 'Project management coordinates with architectural practice for scheduling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('CON.PMC', 'STR.PRA', 'COORDINATES_WITH', 'Project management coordinates with structural practice for scheduling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('CON.PMC', 'MEC.PRA', 'COORDINATES_WITH', 'Project management coordinates with mechanical practice for scheduling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('CON.PMC', 'PLS.PRA', 'COORDINATES_WITH', 'Project management coordinates with plumbing practice for scheduling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('CON.PMC', 'ELE.PRA', 'COORDINATES_WITH', 'Project management coordinates with electrical practice for scheduling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('CON.SEQ', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Construction sequencing coordinates with frame systems for erection, bracing, and safety; non-numerical and non-code-specific.');
addIfFound('CON.SEQ', 'STR.CON.RCO', 'COORDINATES_WITH', 'Construction sequencing coordinates with reinforced concrete for formwork, curing, and stripping; non-numerical and non-code-specific.');
addIfFound('CON.QAC', 'STR.FND', 'COORDINATES_WITH', 'Quality assurance coordinates with foundations for inspection, testing, and acceptance; non-numerical and non-code-specific.');
addIfFound('CON.SAF', 'CON.SEQ', 'COORDINATES_WITH', 'Construction safety coordinates with sequencing for hazard control, access, and protection; non-numerical and non-code-specific.');
addIfFound('CON.COS', 'ARC.PRA', 'COORDINATES_WITH', 'Cost management coordinates with architectural practice for budgeting, estimating, and value engineering; non-numerical and non-code-specific.');

// ==========================================
// D. Operations / facilities / MEPFS
// ==========================================
addIfFound('OPS.FAC', 'MEC.HVA', 'COORDINATES_WITH', 'Facilities operations coordinate with HVAC for maintenance, scheduling, and performance; non-numerical and non-code-specific.');
addIfFound('OPS.FAC', 'ELE.SES', 'COORDINATES_WITH', 'Facilities operations coordinate with electrical service for maintenance, scheduling, and performance; non-numerical and non-code-specific.');
addIfFound('OPS.FAC', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Facilities operations coordinate with water service for maintenance, scheduling, and performance; non-numerical and non-code-specific.');
addIfFound('OPS.FAC', 'FLS.SPR', 'COORDINATES_WITH', 'Facilities operations coordinate with sprinkler systems for testing, maintenance, and inspection; non-numerical and non-code-specific.');
addIfFound('OPS.FAC', 'FLS.ALM.DET', 'COORDINATES_WITH', 'Facilities operations coordinate with detection systems for testing, maintenance, and inspection; non-numerical and non-code-specific.');
addIfFound('OPS.PRE', 'MEC.HVA', 'COORDINATES_WITH', 'Preventive maintenance coordinates with HVAC for scheduling, parts, and procedures; non-numerical and non-code-specific.');
addIfFound('OPS.PRE', 'ELE.DIS.PAN', 'COORDINATES_WITH', 'Preventive maintenance coordinates with panelboards for scheduling, testing, and inspection; non-numerical and non-code-specific.');
addIfFound('OPS.ASSET', 'ARC.BLD', 'COORDINATES_WITH', 'Asset management coordinates with building systems for lifecycle, replacement, and budgeting; non-numerical and non-code-specific.');
addIfFound('OPS.EME', 'FLS.EGR.EXI', 'COORDINATES_WITH', 'Emergency operations coordinate with exits for drills, signage, and maintenance; non-numerical and non-code-specific.');
addIfFound('OPS.EME', 'ELE.EPW', 'COORDINATES_WITH', 'Emergency operations coordinate with emergency power for testing, maintenance, and procedures; non-numerical and non-code-specific.');

// ==========================================
// E. Security / communications / electrical
// ==========================================
addIfFound('SEC.PHS', 'ARC.DOO', 'COORDINATES_WITH', 'Physical security coordinates with doors for access control, hardware, and monitoring; non-numerical and non-code-specific.');
addIfFound('SEC.PHS', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Physical security coordinates with windows for glazing, sensors, and monitoring; non-numerical and non-code-specific.');
addIfFound('SEC.ACS', 'ELE.COM.DNE', 'COORDINATES_WITH', 'Access control coordinates with data networks for integration, protocols, and points; non-numerical and non-code-specific.');
addIfFound('SEC.SUR', 'ELE.COM.DNE', 'COORDINATES_WITH', 'Surveillance coordinates with data networks for integration, bandwidth, and storage; non-numerical and non-code-specific.');
addIfFound('SEC.INT', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'Security integration coordinates with building management for protocols, points, and alarms; non-numerical and non-code-specific.');
addIfFound('SEC.FIR', 'FLS.ALM.DET', 'COORDINATES_WITH', 'Fire security coordinates with detection systems for integration, response, and alarms; non-numerical and non-code-specific.');
addIfFound('SEC.CYB', 'ELE.COM.DNE', 'COORDINATES_WITH', 'Cybersecurity coordinates with data networks for segmentation, monitoring, and access; non-numerical and non-code-specific.');
addIfFound('SEC.EME', 'FLS.EGR.ERO', 'COORDINATES_WITH', 'Emergency security coordinates with egress routes for lockdown, access, and monitoring; non-numerical and non-code-specific.');
addIfFound('SEC.PHS', 'ELE.LIG', 'COORDINATES_WITH', 'Physical security coordinates with lighting for illumination, sensors, and deterrence; non-numerical and non-code-specific.');
addIfFound('SEC.ACS', 'ARC.CIR.ELE', 'COORDINATES_WITH', 'Access control coordinates with elevators for integration, protocols, and monitoring; non-numerical and non-code-specific.');

// ==========================================
// F. Digital / BIM / technology
// ==========================================
addIfFound('DIG.BIM', 'ARC.PRA', 'COORDINATES_WITH', 'BIM coordinates with architectural practice for modeling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('DIG.BIM', 'STR.PRA', 'COORDINATES_WITH', 'BIM coordinates with structural practice for modeling, coordination, and deliverables; non-numerical and non-code-specific.');
addIfFound('DIG.BIM', 'MEC.PRA', 'COORDINATES_WITH', 'BIM coordinates with mechanical practice for modeling, coordination, and clash detection; non-numerical and non-code-specific.');
addIfFound('DIG.BIM', 'PLS.PRA', 'COORDINATES_WITH', 'BIM coordinates with plumbing practice for modeling, coordination, and clash detection; non-numerical and non-code-specific.');
addIfFound('DIG.BIM', 'ELE.PRA', 'COORDINATES_WITH', 'BIM coordinates with electrical practice for modeling, coordination, and clash detection; non-numerical and non-code-specific.');
addIfFound('DIG.GIS', 'CIV.SIT.GRA', 'COORDINATES_WITH', 'GIS coordinates with site grading for topography, utilities, and drainage; non-numerical and non-jurisdiction-specific.');
addIfFound('DIG.GIS', 'URB.PLA', 'COORDINATES_WITH', 'GIS coordinates with urban planning for zoning, infrastructure, and analysis; non-numerical and non-jurisdiction-specific.');
addIfFound('DIG.IOT', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'IoT coordinates with building management for integration, protocols, and sensors; non-numerical and non-code-specific.');
addIfFound('DIG.CLO', 'DIG.BIM', 'COORDINATES_WITH', 'Cloud computing coordinates with BIM for hosting, collaboration, and data management; non-numerical and non-code-specific.');
addIfFound('DIG.AI', 'DIG.BIM', 'COORDINATES_WITH', 'AI coordinates with BIM for analysis, optimization, and automation; non-numerical and non-code-specific.');

// ==========================================
// G. Urban / planning / civil
// ==========================================
addIfFound('URB.PLA', 'CIV.SIT.GRA', 'COORDINATES_WITH', 'Urban planning coordinates with site grading for zoning, infrastructure, and drainage; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.PLA', 'ARC.SIT', 'COORDINATES_WITH', 'Urban planning coordinates with site planning for zoning, infrastructure, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.ZON', 'ARC.ABT', 'COORDINATES_WITH', 'Zoning coordinates with building typologies for use, density, and height; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.TRN', 'ARC.ABT.THT', 'COORDINATES_WITH', 'Transportation planning coordinates with transport hubs for access, circulation, and parking; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.INF', 'CIV.UTI', 'COORDINATES_WITH', 'Urban infrastructure coordinates with utilities for routing, capacity, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.HOU', 'ARC.ABT.HEA', 'COORDINATES_WITH', 'Housing planning coordinates with healthcare architecture for accessibility, services, and amenities; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.GRE', 'SUS.SIT', 'COORDINATES_WITH', 'Green infrastructure coordinates with site sustainability for stormwater, vegetation, and permeability; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.RES', 'CIV.DRN', 'COORDINATES_WITH', 'Resilience planning coordinates with drainage for flooding, capacity, and adaptation; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.RES', 'FLS.EGR.EXI', 'COORDINATES_WITH', 'Resilience planning coordinates with exits for emergency access, evacuation, and safety; non-numerical and non-jurisdiction-specific.');
addIfFound('URB.WAT', 'CIV.MIS.WDN', 'COORDINATES_WITH', 'Urban water planning coordinates with water distribution networks for capacity, quality, and access; non-numerical and non-jurisdiction-specific.');

// ==========================================
// H. Additional MEPFS flow connections
// ==========================================
addIfFound('MEC.AHD.AHU', 'MEC.ACD.ZON', 'CONVEYS', 'Air handling units convey air to zoning as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.');
addIfFound('MEC.ACD.ZON', 'MEC.AHD.DTD', 'CONVEYS', 'Zoning conveys air to diffusers and terminal devices as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.');
addIfFound('MEC.HPS.CWL', 'MEC.ACD.CHW', 'CONVEYS', 'Chilled water loops convey chilled water to chilled water systems as a general hydronic cooling relationship; no flow rate or capacity claim.');
addIfFound('MEC.HPS.BOI', 'MEC.HEA', 'CONVEYS', 'Boilers convey heating to heating systems as a general boiler-to-distribution relationship; no capacity or temperature claim.');
addIfFound('PLS.PWS.WSM', 'PLS.HOT.WHE', 'CONVEYS', 'Water service conveys water to water heating as a general plumbing supply relationship; no fixture-unit or pressure claim.');
addIfFound('ELE.SES', 'ELE.TRA', 'CONVEYS', 'Electrical service conveys power to transformers as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('ELE.TRA', 'ELE.DIS.PAN', 'CONVEYS', 'Transformers convey power to panelboards as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('ELE.DIS.PAN', 'ELE.LOA.LSL', 'CONVEYS', 'Panelboards convey power to life-safety loads as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('ELE.DIS.PAN', 'ELE.LOA.GEL', 'CONVEYS', 'Panelboards convey power to general loads as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('FLS.SPR.FPU', 'FLS.SPR', 'CONVEYS', 'Fire pumps convey water to sprinkler systems as a general fire-protection flow relationship; no pressure or capacity claim.');

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
