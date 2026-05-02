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

// Find nodes by exact path code or prefix
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

// Only include L2/L3 nodes (not the leaf 5-char procedure nodes)
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
// A. Mechanical / HVAC
// ==========================================
addIfFound('MEC.AHD.AHU', 'MEC.AHD.DUD', 'COORDINATES_WITH', 'Air handling units coordinate with duct design for sizing, routing, and access; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.AHU', 'MEC.AHD.DTD', 'COORDINATES_WITH', 'Air handling units coordinate with diffusers and terminal devices for coverage and airflow distribution; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.DUD', 'MEC.AHD.DTD', 'CONVEYS', 'Duct design conveys air to diffusers and terminal devices as a general HVAC air-distribution relationship; no airflow rate or duct-sizing claim.');
addIfFound('MEC.AHD.RET', 'MEC.AHD.AHU', 'CONVEYS', 'Return air path conveys return air to air handling units as a general HVAC return-air relationship; no airflow rate or duct-sizing claim.');
addIfFound('MEC.AHD.EXT', 'MEC.AHD.EOT', 'DISCHARGES_TO', 'Exhaust fans discharge to exhaust outlets as a general HVAC exhaust discharge relationship; no airflow rate or fan-sizing claim.');
addIfFound('MEC.COO.CTW', 'MEC.HPS.CWL', 'COORDINATES_WITH', 'Cooling towers coordinate with chilled water loops for piping, access, and make-up water; non-numerical and non-code-specific.');
addIfFound('MEC.HPS.CWL', 'MEC.ACD.CHW', 'CONVEYS', 'Chilled water loops convey chilled water to chilled water systems as a general hydronic cooling relationship; no flow rate or capacity claim.');
addIfFound('MEC.HPS.HWL', 'MEC.HEA', 'CONVEYS', 'Hot water loops convey heating to heating systems as a general hydronic heating relationship; no flow rate or capacity claim.');
addIfFound('MEC.HPS.BOI', 'MEC.HPS.HWL', 'CONVEYS', 'Boilers convey heating to hot water loops as a general boiler-to-distribution relationship; no capacity or temperature claim.');
addIfFound('MEC.ACD.CHW', 'MEC.AHD.AHU', 'CONVEYS', 'Chilled water systems convey chilled water to air handling units as a general hydronic cooling relationship; no flow rate or capacity claim.');
addIfFound('MEC.HEA', 'MEC.HPS.HWL', 'COORDINATES_WITH', 'Heating systems coordinate with hot water loops for piping, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('MEC.ACD', 'MEC.HVA', 'CROSS_DOMAIN_ALIGNMENT', 'Air-conditioning and HVAC systems are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('MEC.HVA', 'MEC.ACD', 'CROSS_DOMAIN_ALIGNMENT', 'HVAC systems and air-conditioning are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.');

// ==========================================
// B. Plumbing / sanitary
// ==========================================
addIfFound('PLS.PWS.WSM', 'PLS.FIX.LAV', 'CONVEYS', 'Water service conveys water to lavatories as a general plumbing supply relationship; no fixture-unit or pressure claim.');
addIfFound('PLS.PWS.WSM', 'PLS.FIX.SHO', 'CONVEYS', 'Water service conveys water to showers as a general plumbing supply relationship; no fixture-unit or pressure claim.');
addIfFound('PLS.PWS.WSM', 'PLS.FIX.WCL', 'CONVEYS', 'Water service conveys water to water closets as a general plumbing supply relationship; no fixture-unit or pressure claim.');
addIfFound('PLS.FIX.LAV', 'PLS.WST', 'DISCHARGES_TO', 'Lavatories discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.');
addIfFound('PLS.FIX.SHO', 'PLS.WST', 'DISCHARGES_TO', 'Showers discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.');
addIfFound('PLS.FIX.WCL', 'PLS.WST', 'DISCHARGES_TO', 'Water closets discharge to wastewater as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.');
addIfFound('PLS.WST', 'CIV.MIS.SEN', 'DISCHARGES_TO', 'Wastewater discharges to sewerage networks as a general building drainage-to-sewer relationship; no capacity or slope claim.');
addIfFound('PLS.WST.RDR', 'CIV.MIS.STN', 'DRAINS_TO', 'Roof drains drain to stormwater networks as a general roof drainage-to-stormwater relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.FDR', 'CIV.DRN', 'DRAINS_TO', 'Floor drains drain to drainage as a general floor drainage relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.SMP', 'CIV.DRN', 'DISCHARGES_TO', 'Sump pumps discharge to drainage as a general sump discharge relationship; no capacity or pump-sizing claim.');
addIfFound('PLS.HOT.WHE', 'PLS.FIX.LAV', 'COORDINATES_WITH', 'Water heating coordinates with lavatories for temperature, pressure, and piping; non-numerical and non-code-specific.');
addIfFound('PLS.HOT.WHE', 'PLS.FIX.SHO', 'COORDINATES_WITH', 'Water heating coordinates with showers for temperature, pressure, and piping; non-numerical and non-code-specific.');
addIfFound('PLS.GAS', 'PLS.HOT.WHE', 'COORDINATES_WITH', 'Fuel gas coordinates with water heating for combustion air, venting, and controls; non-numerical and non-code-specific.');
addIfFound('PLS.PWS.WSM', 'CIV.MIS.WDN', 'CONNECTS_TO', 'Water service connects to water distribution networks as a general building-to-utility water interface; no pressure or sizing claim.');

// ==========================================
// C. Fire / life safety
// ==========================================
addIfFound('FLS.DET.SMK', 'FLS.ALM.DET', 'INFORMS', 'Smoke detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.');
addIfFound('FLS.DET.HEA', 'FLS.ALM.DET', 'INFORMS', 'Heat detection informs detection systems as a general fire-safety sensor-to-system relationship; no device-specification or code-compliance claim.');
addIfFound('FLS.ALM.DET', 'FLS.ALM.NOT', 'INFORMS', 'Detection systems inform notification systems as a general fire-alarm-to-notification relationship; no device-specification or code-compliance claim.');
addIfFound('FLS.ALM.NOT', 'FLS.ALM.MNS', 'COORDINATES_WITH', 'Notification systems coordinate with mass notification for coverage, audibility, and zoning; non-numerical and non-code-specific.');
addIfFound('FLS.SPR', 'FLS.ALM.DET', 'COORDINATES_WITH', 'Sprinkler systems coordinate with detection systems for response timing and zoning; non-numerical and non-code-specific.');
addIfFound('FLS.SPR', 'FLS.ASS', 'COORDINATES_WITH', 'Sprinkler systems coordinate with automatic suppression systems for coverage and design basis; non-numerical and non-code-specific.');
addIfFound('FLS.SPR.FPU', 'FLS.SPR', 'SUPPORTS', 'Fire pumps support sprinkler systems as a general fire-protection equipment relationship; no capacity or pressure claim.');
addIfFound('FLS.EGR.ECA', 'FLS.EGR.EXI', 'CONSTRAINS', 'Egress capacity conceptually constrains exits as a general life-safety capacity relationship; no specific occupant count or code section claim.');
addIfFound('FLS.EGR.EAC', 'ARC.FLO', 'COORDINATES_WITH', 'Exit access coordinates with floor plans for location, width, and door swing; non-numerical and non-code-specific.');
addIfFound('FLS.EGR.ELI', 'FLS.EGR.ERO', 'COORDINATES_WITH', 'Emergency lighting coordinates with egress routes for illumination, placement, and power; non-numerical and non-code-specific.');
addIfFound('FLS.CMP.FBA', 'ARC.FIR.COM', 'COORDINATES_WITH', 'Fire barriers coordinate with compartmentation for continuity and penetration management; non-numerical and non-code-specific.');

// ==========================================
// D. Electrical
// ==========================================
addIfFound('ELE.GRD.GES', 'STR.FND', 'COORDINATES_WITH', 'Grounding electrode systems coordinate with foundations for earth-contact area, embedment, and corrosion protection; non-numerical and non-code-specific.');
addIfFound('ELE.SES', 'ELE.UTI', 'CONNECTS_TO', 'Electrical service connects to utility service as a general building-to-utility electrical interface; no voltage or capacity claim.');
addIfFound('ELE.DIS.PAN', 'ARC.ELE', 'COORDINATES_WITH', 'Panelboards coordinate with electrical rooms for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ELE.CAB', 'ARC.CEL', 'COORDINATES_WITH', 'Cable trays coordinate with ceiling plenums for routing, access, and support; non-numerical and non-code-specific.');
addIfFound('ELE.EPW.GEN', 'ELE.EPW', 'SUPPORTS', 'Generators support emergency power systems as a general emergency power equipment relationship; no capacity or runtime claim.');
addIfFound('ELE.EPW', 'ELE.LOA.LSL', 'SUPPORTS', 'Emergency power supports life-safety loads as a general emergency power-to-load relationship; no capacity or circuit claim.');
addIfFound('ELE.TRA', 'ARC.ELE', 'COORDINATES_WITH', 'Transformers coordinate with electrical rooms for clearances, ventilation, and access; non-numerical and non-code-specific.');
addIfFound('ELE.SWI', 'ARC.ELE', 'COORDINATES_WITH', 'Switchgear coordinates with electrical rooms for clearances, ventilation, and access; non-numerical and non-code-specific.');
addIfFound('ELE.CTL.BMS', 'MEC.CTL', 'COORDINATES_WITH', 'Building management systems coordinate with mechanical controls for integration, protocols, and points; non-numerical and non-code-specific.');
addIfFound('ELE.COM.DNE', 'ELE.COM.VSY', 'COORDINATES_WITH', 'Data networks coordinate with voice systems for infrastructure, pathways, and equipment rooms; non-numerical and non-code-specific.');

// ==========================================
// E. Architecture / structure / MEPFS coordination
// ==========================================
addIfFound('ARC.SHA', 'MEC.AHD.DUD', 'COORDINATES_WITH', 'Shafts coordinate with ductwork for sizing, fire stopping, and access; non-numerical and non-code-specific.');
addIfFound('ARC.SHA', 'PLS.RIS', 'COORDINATES_WITH', 'Shafts coordinate with plumbing risers for sizing, fire stopping, and access; non-numerical and non-code-specific.');
addIfFound('STR.OPE', 'MEC.PEN', 'COORDINATES_WITH', 'Structural openings coordinate with MEP penetrations for sizing, fire stopping, and sealing; non-numerical and non-code-specific.');
addIfFound('STR.SLB.OPE', 'ARC.VSE', 'COORDINATES_WITH', 'Slab openings coordinate with vertical services for sizing, reinforcement, and fire stopping; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.ROF', 'MEC.ROO', 'SUPPORTS', 'Roof structures support rooftop equipment as a general structural-equipment support relationship; no load value or member-sizing claim.');
addIfFound('ARC.ENV.WAL', 'ARC.ENV.LOU', 'COORDINATES_WITH', 'Walls coordinate with louvers for weatherproofing, thermal bridging, and appearance; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'MEC.AHD.EOT', 'COORDINATES_WITH', 'Walls coordinate with exhaust outlets for weatherproofing, thermal bridging, and appearance; non-numerical and non-code-specific.');
addIfFound('ARC.CEL', 'MEC.AHD.DUD', 'COORDINATES_WITH', 'Ceiling plenums coordinate with ductwork for routing, access, and clearance; non-numerical and non-code-specific.');
addIfFound('ARC.MEC.CLR', 'ARC.MEC', 'CONSTRAINS', 'Equipment clearance conceptually constrains mechanical rooms as a general equipment-planning relationship; no specific dimension or code claim.');
addIfFound('ARC.ENV.ROF', 'MEC.COO.CTW', 'SUPPORTS', 'Roof structures support cooling towers as a general structural-equipment support relationship; no load value or member-sizing claim.');

// ==========================================
// F. Civil / site / building interface
// ==========================================
addIfFound('CIV.SIT.GRA', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Site grading coordinates with building pads for drainage, slope, and elevation; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.DRN', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Drainage coordinates with building pads for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.UTI', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Utilities coordinate with building pads for routing, invert elevations, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.FND', 'GEO.EAR', 'COORDINATES_WITH', 'Foundation excavation coordinates with earthworks for cut/fill balance, shoring, and dewatering; non-numerical and non-jurisdiction-specific.');
addIfFound('ARC.ACC.CRA', 'CIV.SID', 'CONNECTS_TO', 'Curb ramps connect to sidewalks as a general accessible route interface; no specific slope or width claim.');
addIfFound('ARC.ACC.PAR', 'ARC.ACC', 'CONNECTS_TO', 'Accessible parking connects to accessible routes as a general accessible parking interface; no specific dimension or code claim.');
addIfFound('ARC.SIT.ACC', 'CIV.SID', 'CONNECTS_TO', 'Site access connects to sidewalks as a general site circulation interface; no specific width or code claim.');
addIfFound('CIV.DRN.CSB', 'CIV.MIS.STN', 'DRAINS_TO', 'Catch basins drain to stormwater networks as a general stormwater collection-to-conveyance relationship; no capacity or pipe-sizing claim.');
addIfFound('CIV.MIS.STN', 'CIV.WAT.STW', 'CONVEYS', 'Stormwater networks convey stormwater to stormwater infrastructure as a general stormwater conveyance relationship; no flow rate or pipe-sizing claim.');
addIfFound('CIV.BRG.DCK', 'CIV.BRG.DCK.DSA', 'COORDINATES_WITH', 'Deck systems coordinate with drainage and service interfaces for runoff and utilities; non-numerical and non-jurisdiction-specific.');

// ==========================================
// G. Additional cross-domain alignments
// ==========================================
addIfFound('MEC.HEA', 'MEC.HPS.HWL', 'CROSS_DOMAIN_ALIGNMENT', 'Heating systems and hot water loops are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('MEC.HPS.HWL', 'MEC.HEA', 'CROSS_DOMAIN_ALIGNMENT', 'Hot water loops and heating systems are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('MEC.VEN', 'MEC.AHD', 'CROSS_DOMAIN_ALIGNMENT', 'Ventilation and air distribution are discipline-scoped views of the same air-moving object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('MEC.AHD', 'MEC.VEN', 'CROSS_DOMAIN_ALIGNMENT', 'Air distribution and ventilation are discipline-scoped views of the same air-moving object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('PLS.PWS', 'PLS.PWS.WSM', 'CROSS_DOMAIN_ALIGNMENT', 'Potable water systems and water service are discipline-scoped views of the same water supply object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('PLS.PWS.WSM', 'PLS.PWS', 'CROSS_DOMAIN_ALIGNMENT', 'Water service and potable water systems are discipline-scoped views of the same water supply object family; alignment only, no equivalence, merge, or identity claim.');

// ==========================================
// H. Structural load paths
// ==========================================
addIfFound('STR.SYS.FRM', 'STR.CON.RCO', 'SUPPORTS', 'Frame systems support reinforced concrete as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('STR.SYS.FRM', 'STR.CON.PRE', 'SUPPORTS', 'Frame systems support precast concrete as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('STR.SYS.WAL', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Wall systems transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.SYS.FRM', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Frame systems transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.CON.RCO', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Reinforced concrete transfers load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.CON.PRE', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Precast concrete transfers load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.FND.DEP', 'GEO.FOE.DEF', 'CROSS_DOMAIN_ALIGNMENT', 'Deep foundations and deep foundations engineering are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.');
addIfFound('GEO.FOE.DEF', 'STR.FND.DEP', 'CROSS_DOMAIN_ALIGNMENT', 'Deep foundations engineering and deep foundations are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.');

// ==========================================
// I. Additional MEPFS coordination
// ==========================================
addIfFound('MEC.AHD.AHU', 'ARC.ENV.ROF', 'COORDINATES_WITH', 'Air handling units coordinate with roof systems for structural openings, weatherproofing, and equipment access; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.AHU', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Air handling units coordinate with walls for intake/discharge openings and thermal bridging; non-numerical and non-code-specific.');
addIfFound('ELE.GRD.GES', 'STR.FND', 'COORDINATES_WITH', 'Grounding electrode systems coordinate with foundations for earth-contact area, corrosion protection, and embedment; non-numerical and non-code-specific.');
addIfFound('PLS.PWS.WSM', 'CIV.MIS.WDN', 'COORDINATES_WITH', 'Water service coordinates with water distribution networks for pressure, sizing, and connection; non-numerical and non-jurisdiction-specific.');
addIfFound('PLS.WST', 'CIV.MIS.SEN', 'COORDINATES_WITH', 'Wastewater coordinates with sewerage networks for capacity, slope, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('ELE.EPW.GEN', 'STR.SYS.FRM', 'SUPPORTS', 'Generators are supported by frame systems as a general structural-equipment support relationship; no equipment-load or member-sizing claim.');
addIfFound('MEC.COO.CTW', 'STR.SYS.FRM', 'SUPPORTS', 'Cooling towers are supported by frame systems as a general structural-equipment support relationship; no equipment-load or member-sizing claim.');

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
