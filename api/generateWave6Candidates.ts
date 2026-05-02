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
// A. Structural systems (steel, timber, masonry)
// ==========================================
addIfFound('STR.SYS.FRM', 'STR.SYS.WAL', 'COORDINATES_WITH', 'Frame systems coordinate with wall systems for lateral stability, expansion joints, and load transfer; non-numerical and non-code-specific.');
addIfFound('STR.SYS.WAL', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Wall systems coordinate with frame systems for lateral stability, expansion joints, and load transfer; non-numerical and non-code-specific.');
addIfFound('STR.SYS.FRM', 'STR.STL', 'SUPPORTS', 'Frame systems support steel structures as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('STR.SYS.FRM', 'STR.TIM', 'SUPPORTS', 'Frame systems support timber structures as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('STR.SYS.FRM', 'STR.TMA', 'SUPPORTS', 'Frame systems support masonry structures as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('STR.STL', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Steel structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.TIM', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Timber structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.TMA', 'STR.FND', 'TRANSFERS_LOAD_TO', 'Masonry structures transfer load to foundations as a general structural load-path relationship; no load value or member-sizing claim.');
addIfFound('STR.STL', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Steel structures coordinate with frame systems for connections, bracing, and fire protection; non-numerical and non-code-specific.');
addIfFound('STR.TIM', 'STR.SYS.FRM', 'COORDINATES_WITH', 'Timber structures coordinate with frame systems for connections, bracing, and fire protection; non-numerical and non-code-specific.');
addIfFound('STR.TMA', 'STR.SYS.WAL', 'COORDINATES_WITH', 'Masonry structures coordinate with wall systems for lateral support, expansion joints, and moisture control; non-numerical and non-code-specific.');

// ==========================================
// B. Civil / site / paving / landscape
// ==========================================
addIfFound('CIV.PAV', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Pavements coordinate with building pads for drainage, slope, and elevation; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.CRB', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Curbs coordinate with building pads for drainage, slope, and grading; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.LAN', 'ARC.SIT.PAD', 'COORDINATES_WITH', 'Landscaping coordinates with building pads for drainage, irrigation, and grading; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.PAV', 'CIV.DRN', 'COORDINATES_WITH', 'Pavements coordinate with drainage for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.CRB', 'CIV.DRN', 'COORDINATES_WITH', 'Curbs coordinate with drainage for runoff, inlets, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.SID', 'CIV.DRN', 'COORDINATES_WITH', 'Sidewalks coordinate with drainage for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.UTI', 'CIV.DRN', 'COORDINATES_WITH', 'Utilities coordinate with drainage for separation, crossings, and access; non-numerical and non-jurisdiction-specific.');
addIfFound('CIV.BRG.DCK', 'STR.SYS.FRM', 'SUPPORTS', 'Deck systems are supported by frame systems as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('CIV.BRG.SPN', 'STR.SYS.FRM', 'SUPPORTS', 'Spans are supported by frame systems as a general structural-system relationship; no member-sizing or capacity claim.');
addIfFound('CIV.BRG.ABT', 'GEO.FOE', 'COORDINATES_WITH', 'Abutments coordinate with foundation engineering for bearing, settlement, and drainage; non-numerical and non-jurisdiction-specific.');

// ==========================================
// C. Accessibility / universal design
// ==========================================
addIfFound('ACC.ABE', 'ARC.ACC', 'COORDINATES_WITH', 'Accessible built environment audits coordinate with accessible routes for compliance, wayfinding, and usability; non-numerical and non-code-specific.');
addIfFound('ACC.AGE', 'ARC.ACC', 'COORDINATES_WITH', 'Aging and inclusive use coordinate with accessible routes for wayfinding, rest, and support; non-numerical and non-code-specific.');
addIfFound('ACC.ABE.ATC', 'PLS.FIX.LAV', 'COORDINATES_WITH', 'Accessible toilet checks coordinate with lavatories for clearances, grab bars, and fixtures; non-numerical and non-code-specific.');
addIfFound('ACC.ABE.DOC', 'ARC.DOO', 'COORDINATES_WITH', 'Doorway and opening checks coordinate with doors for clearances, hardware, and operation; non-numerical and non-code-specific.');
addIfFound('ACC.ABE.RCC', 'ARC.CIR', 'COORDINATES_WITH', 'Route continuity checks coordinate with circulation for width, slope, and surface; non-numerical and non-code-specific.');
addIfFound('ACC.ABE.VAC', 'ARC.CIR.ELE', 'COORDINATES_WITH', 'Vertical access checks coordinate with elevators for cab size, controls, and landing; non-numerical and non-code-specific.');
addIfFound('ACC.ABE.VAC', 'ARC.CIR.STR', 'COORDINATES_WITH', 'Vertical access checks coordinate with stairs for riser, tread, and handrail; non-numerical and non-code-specific.');

// ==========================================
// D. Building envelope / facade / roofing
// ==========================================
addIfFound('ARC.ENV.ROF', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Roof systems coordinate with walls for flashing, thermal bridging, and air barrier; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'ARC.ENV.ROF', 'COORDINATES_WITH', 'Walls coordinate with roof systems for flashing, thermal bridging, and air barrier; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'ARC.ENV.WIN', 'COORDINATES_WITH', 'Walls coordinate with windows for thermal bridging, air barrier, and water intrusion; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'ARC.ENV.DOOR', 'COORDINATES_WITH', 'Walls coordinate with doors for thermal bridging, air barrier, and water intrusion; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'ARC.ENV.INS', 'COORDINATES_WITH', 'Walls coordinate with insulation for thermal performance, condensation, and vapor control; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.ROF', 'ARC.ENV.INS', 'COORDINATES_WITH', 'Roof systems coordinate with insulation for thermal performance, condensation, and vapor control; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'MEC.AHD.DUD', 'COORDINATES_WITH', 'Walls coordinate with ductwork for penetrations, fire stopping, and thermal bridging; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.WAL', 'ELE.CAB', 'COORDINATES_WITH', 'Walls coordinate with cable trays for penetrations, fire stopping, and routing; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.ROF', 'MEC.AHD.DUD', 'COORDINATES_WITH', 'Roof systems coordinate with ductwork for penetrations, curbs, and weatherproofing; non-numerical and non-code-specific.');
addIfFound('ARC.ENV.ROF', 'ELE.CAB', 'COORDINATES_WITH', 'Roof systems coordinate with cable trays for penetrations, curbs, and weatherproofing; non-numerical and non-code-specific.');

// ==========================================
// E. Interior / finishes / partitions
// ==========================================
addIfFound('ARC.INT.PAR', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Interior partitions coordinate with walls for structure, services, and fire rating; non-numerical and non-code-specific.');
addIfFound('ARC.INT.CEL', 'ARC.CEL', 'COORDINATES_WITH', 'Interior ceilings coordinate with ceiling plenums for access, services, and lighting; non-numerical and non-code-specific.');
addIfFound('ARC.INT.FLO', 'ARC.FLO', 'COORDINATES_WITH', 'Interior flooring coordinates with floor systems for structure, services, and finishes; non-numerical and non-code-specific.');
addIfFound('ARC.FIN', 'ARC.INT', 'COORDINATES_WITH', 'Finishes coordinate with interiors for material selection, durability, and maintenance; non-numerical and non-code-specific.');
addIfFound('ARC.FIN.PAI', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Paint finishes coordinate with walls for preparation, application, and durability; non-numerical and non-code-specific.');
addIfFound('ARC.FIN.TIL', 'ARC.ENV.WAL', 'COORDINATES_WITH', 'Tile finishes coordinate with walls for preparation, application, and waterproofing; non-numerical and non-code-specific.');
addIfFound('ARC.FIN.CAR', 'ARC.INT.FLO', 'COORDINATES_WITH', 'Carpet finishes coordinate with flooring for preparation, installation, and maintenance; non-numerical and non-code-specific.');

// ==========================================
// F. MEPFS room / space coordination
// ==========================================
addIfFound('ARC.MEC', 'MEC.AHD.AHU', 'COORDINATES_WITH', 'Mechanical rooms coordinate with air handling units for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.MEC', 'MEC.COO.CTW', 'COORDINATES_WITH', 'Mechanical rooms coordinate with cooling towers for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.ELE', 'ELE.SES', 'COORDINATES_WITH', 'Electrical rooms coordinate with electrical service for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.ELE', 'ELE.EPW.GEN', 'COORDINATES_WITH', 'Electrical rooms coordinate with generators for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.ELE', 'ELE.TRA', 'COORDINATES_WITH', 'Electrical rooms coordinate with transformers for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.PLS', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Plumbing rooms coordinate with water service for clearances, access, and drainage; non-numerical and non-code-specific.');
addIfFound('ARC.PLS', 'PLS.HOT.WHE', 'COORDINATES_WITH', 'Plumbing rooms coordinate with water heating for clearances, access, and ventilation; non-numerical and non-code-specific.');
addIfFound('ARC.FIR', 'FLS.SPR', 'COORDINATES_WITH', 'Fire rooms coordinate with sprinkler systems for clearances, access, and water supply; non-numerical and non-code-specific.');
addIfFound('ARC.FIR', 'FLS.SPR.FPU', 'COORDINATES_WITH', 'Fire rooms coordinate with fire pumps for clearances, access, and water supply; non-numerical and non-code-specific.');

// ==========================================
// G. Additional electrical / low-voltage
// ==========================================
addIfFound('ELE.SES', 'ELE.DIS.PAN', 'CONVEYS', 'Electrical service conveys power to panelboards as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('ELE.DIS.PAN', 'ELE.LOA', 'CONVEYS', 'Panelboards convey power to loads as a general electrical distribution relationship; no voltage or capacity claim.');
addIfFound('ELE.EPW', 'ELE.SES', 'COORDINATES_WITH', 'Emergency power coordinates with electrical service for transfer, isolation, and monitoring; non-numerical and non-code-specific.');
addIfFound('ELE.EPW.GEN', 'ELE.SES', 'COORDINATES_WITH', 'Generators coordinate with electrical service for transfer, isolation, and monitoring; non-numerical and non-code-specific.');
addIfFound('ELE.GRD.GES', 'ELE.SES', 'COORDINATES_WITH', 'Grounding electrode systems coordinate with electrical service for bonding, grounding, and safety; non-numerical and non-code-specific.');
addIfFound('ELE.COM.DNE', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'Data networks coordinate with building management for integration, protocols, and points; non-numerical and non-code-specific.');
addIfFound('ELE.COM.VSY', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'Voice systems coordinate with building management for integration, protocols, and points; non-numerical and non-code-specific.');
addIfFound('ELE.LIG', 'ARC.CEL', 'COORDINATES_WITH', 'Lighting coordinates with ceiling plenums for routing, access, and thermal management; non-numerical and non-code-specific.');
addIfFound('ELE.LIG', 'ARC.INT.CEL', 'COORDINATES_WITH', 'Lighting coordinates with interior ceilings for mounting, access, and thermal management; non-numerical and non-code-specific.');

// ==========================================
// H. Additional fire / life safety
// ==========================================
addIfFound('FLS.SPR', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Sprinkler systems coordinate with water service for supply, pressure, and flow; non-numerical and non-code-specific.');
addIfFound('FLS.SPR.FPU', 'PLS.PWS.WSM', 'COORDINATES_WITH', 'Fire pumps coordinate with water service for supply, pressure, and flow; non-numerical and non-code-specific.');
addIfFound('FLS.ASS.CAS', 'FLS.ALM.DET', 'COORDINATES_WITH', 'Clean agent systems coordinate with detection systems for response timing and zoning; non-numerical and non-code-specific.');
addIfFound('FLS.ASS.CAS', 'FLS.SPR', 'COORDINATES_WITH', 'Clean agent systems coordinate with sprinkler systems for coverage and design basis; non-numerical and non-code-specific.');
addIfFound('FLS.EGR.ELI', 'ELE.EPW', 'SUPPORTS', 'Emergency lighting is supported by emergency power as a general life-safety power relationship; no capacity or circuit claim.');
addIfFound('FLS.ALM.NOT', 'ELE.EPW', 'SUPPORTS', 'Notification systems are supported by emergency power as a general life-safety power relationship; no capacity or circuit claim.');
addIfFound('FLS.EGR.EXI', 'ARC.DOO', 'COORDINATES_WITH', 'Exits coordinate with doors for width, swing, and hardware; non-numerical and non-code-specific.');
addIfFound('FLS.EGR.STA', 'ARC.CIR.STR', 'COORDINATES_WITH', 'Egress stairs coordinate with stairs for width, riser, tread, and handrail; non-numerical and non-code-specific.');

// ==========================================
// I. Additional HVAC / mechanical
// ==========================================
addIfFound('MEC.VEN', 'MEC.AHD.AHU', 'CONVEYS', 'Ventilation conveys air to air handling units as a general HVAC air-moving relationship; no airflow rate or duct-sizing claim.');
addIfFound('MEC.AHD.AHU', 'MEC.VEN', 'COORDINATES_WITH', 'Air handling units coordinate with ventilation for sizing, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('MEC.ACD', 'MEC.AHD.AHU', 'COORDINATES_WITH', 'Air-conditioning coordinates with air handling units for sizing, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('MEC.HEA', 'MEC.HPS.BOI', 'COORDINATES_WITH', 'Heating coordinates with boilers for sizing, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('MEC.COO', 'MEC.HPS.CWL', 'COORDINATES_WITH', 'Cooling coordinates with chilled water loops for sizing, controls, and zoning; non-numerical and non-code-specific.');
addIfFound('MEC.HVA', 'MEC.CTL', 'COORDINATES_WITH', 'HVAC coordinates with mechanical controls for integration, protocols, and points; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.DUD', 'MEC.AHD.RET', 'COORDINATES_WITH', 'Duct design coordinates with return air paths for sizing, routing, and balancing; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.DTD', 'ARC.ENV.OCC', 'COORDINATES_WITH', 'Diffusers coordinate with occupied spaces for coverage, comfort, and noise; non-numerical and non-code-specific.');

// ==========================================
// J. Additional plumbing / sanitary
// ==========================================
addIfFound('PLS.RIS', 'PLS.PWS.WSM', 'CONVEYS', 'Plumbing risers convey water from water service as a general plumbing distribution relationship; no fixture-unit or pressure claim.');
addIfFound('PLS.RIS', 'PLS.WST', 'DISCHARGES_TO', 'Plumbing risers discharge to wastewater as a general drainage collection relationship; no flow rate or pipe-sizing claim.');
addIfFound('PLS.GAS', 'PLS.RIS', 'COORDINATES_WITH', 'Fuel gas coordinates with plumbing risers for routing, venting, and access; non-numerical and non-code-specific.');
addIfFound('PLS.HOT.WHE', 'PLS.GAS', 'COORDINATES_WITH', 'Water heating coordinates with fuel gas for combustion air, venting, and controls; non-numerical and non-code-specific.');
addIfFound('PLS.WST.SMP', 'PLS.WST', 'DISCHARGES_TO', 'Sump pumps discharge to wastewater as a general sump discharge relationship; no capacity or pump-sizing claim.');
addIfFound('PLS.WST.RDR', 'PLS.WST', 'DISCHARGES_TO', 'Roof drains discharge to wastewater as a general roof drainage relationship; no capacity or pipe-sizing claim.');

// ==========================================
// K. Additional cross-domain alignments
// ==========================================
addIfFound('ARC.ENV.WAL', 'ARC.ENV.WAL.FAC', 'CROSS_DOMAIN_ALIGNMENT', 'Walls and facade systems are discipline-scoped views of the same enclosure object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ARC.ENV.WAL.FAC', 'ARC.ENV.WAL', 'CROSS_DOMAIN_ALIGNMENT', 'Facade systems and walls are discipline-scoped views of the same enclosure object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ARC.ENV.ROF', 'ARC.ENV.ROF.RTS', 'CROSS_DOMAIN_ALIGNMENT', 'Roof systems and roof-top systems are discipline-scoped views of the same roof object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ARC.ENV.ROF.RTS', 'ARC.ENV.ROF', 'CROSS_DOMAIN_ALIGNMENT', 'Roof-top systems and roof systems are discipline-scoped views of the same roof object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('STR.FND.SHA', 'GEO.FOE.SHA', 'CROSS_DOMAIN_ALIGNMENT', 'Shallow foundations and shallow foundation engineering are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('GEO.FOE.SHA', 'STR.FND.SHA', 'CROSS_DOMAIN_ALIGNMENT', 'Shallow foundation engineering and shallow foundations are discipline-scoped views of the same foundation object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('CIV.DRN', 'PLS.WST', 'CROSS_DOMAIN_ALIGNMENT', 'Drainage and wastewater are discipline-scoped views of the same water-disposal object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('PLS.WST', 'CIV.DRN', 'CROSS_DOMAIN_ALIGNMENT', 'Wastewater and drainage are discipline-scoped views of the same water-disposal object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('MEC.HVA', 'MEC.HEA', 'CROSS_DOMAIN_ALIGNMENT', 'HVAC and heating are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('MEC.HEA', 'MEC.HVA', 'CROSS_DOMAIN_ALIGNMENT', 'Heating and HVAC are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');

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
