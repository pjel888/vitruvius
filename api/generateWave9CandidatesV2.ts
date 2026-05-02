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

// Underrepresented relation families: AFFECTS(3), REQUIRES(1), RESISTS(2), MITIGATES(1), COLLECTS(2), DRAINS_TO(1)

// AFFECTS
addIfFound('STR.SEI', 'ARC.ENV.WAL', 'AFFECTS', 'Seismic design affects walls for in-plane forces, out-of-plane demands, and detailing; non-numerical and non-code-specific.');
addIfFound('STR.WIN', 'ARC.ENV.WAL', 'AFFECTS', 'Wind design affects walls for pressure, suction, and fatigue; non-numerical and non-code-specific.');
addIfFound('STR.SEI', 'ARC.ENV.ROF', 'AFFECTS', 'Seismic design affects roof systems for diaphragm action, anchorage, and connections; non-numerical and non-code-specific.');
addIfFound('STR.WIN', 'ARC.ENV.ROF', 'AFFECTS', 'Wind design affects roof systems for uplift, pressure, and fatigue; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.AHU', 'ARC.ACO', 'AFFECTS', 'Air handling units affect acoustics for noise, vibration, and transmission; non-numerical and non-code-specific.');
addIfFound('ELE.LIG', 'ARC.LIG', 'AFFECTS', 'Electrical lighting affects lighting design for power, controls, and dimming; non-numerical and non-code-specific.');
addIfFound('CIV.DRN', 'ARC.SIT', 'AFFECTS', 'Drainage affects site planning for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.');
addIfFound('SUS.THE', 'ARC.ENV.INS', 'AFFECTS', 'Thermal sustainability affects insulation for R-value, condensation, and vapor control; non-numerical and non-code-specific.');

// REQUIRES
addIfFound('FLS.EGR.EXI', 'FLS.EGR.ELI', 'REQUIRES', 'Exits require emergency lighting for illumination, visibility, and safety; non-numerical and non-code-specific.');
addIfFound('FLS.EGR.EXI', 'FLS.EGR.ERO', 'REQUIRES', 'Exits require egress routes for continuity, width, and signage; non-numerical and non-code-specific.');
addIfFound('MEC.AHD.AHU', 'ELE.SES', 'REQUIRES', 'Air handling units require electrical service for power, controls, and protection; non-numerical and non-code-specific.');
addIfFound('MEC.COO.CTW', 'ELE.SES', 'REQUIRES', 'Cooling towers require electrical service for power, controls, and protection; non-numerical and non-code-specific.');
addIfFound('ELE.EPW.GEN', 'ELE.SES', 'REQUIRES', 'Generators require electrical service for paralleling, transfer, and monitoring; non-numerical and non-code-specific.');
addIfFound('PLS.HOT.WHE', 'PLS.GAS', 'REQUIRES', 'Water heating requires fuel gas for combustion, venting, and ignition; non-numerical and non-code-specific.');
addIfFound('FLS.SPR', 'PLS.PWS.WSM', 'REQUIRES', 'Sprinkler systems require water service for supply, pressure, and flow; non-numerical and non-code-specific.');
addIfFound('FLS.SPR.FPU', 'PLS.PWS.WSM', 'REQUIRES', 'Fire pumps require water service for supply, pressure, and flow; non-numerical and non-code-specific.');

// RESISTS
addIfFound('STR.SYS.FRM', 'STR.WIN', 'RESISTS', 'Frame systems resist wind as a general structural lateral-force relationship; no load value or member-sizing claim.');
addIfFound('STR.SYS.WAL', 'STR.WIN', 'RESISTS', 'Wall systems resist wind as a general structural lateral-force relationship; no load value or member-sizing claim.');
addIfFound('STR.SYS.FRM', 'STR.SEI', 'RESISTS', 'Frame systems resist seismic as a general structural lateral-force relationship; no load value or member-sizing claim.');
addIfFound('STR.SYS.WAL', 'STR.SEI', 'RESISTS', 'Wall systems resist seismic as a general structural lateral-force relationship; no load value or member-sizing claim.');
addIfFound('STR.RET', 'GEO.SOI', 'RESISTS', 'Retaining walls resist soil as a general geotechnical lateral-force relationship; no load value or member-sizing claim.');
addIfFound('STR.RET', 'CIV.EAR', 'RESISTS', 'Retaining walls resist earth as a general geotechnical lateral-force relationship; no load value or member-sizing claim.');
addIfFound('ARC.ENV.WAL', 'STR.WIN', 'RESISTS', 'Walls resist wind as a general envelope lateral-force relationship; no load value or member-sizing claim.');
addIfFound('ARC.ENV.ROF', 'STR.WIN', 'RESISTS', 'Roof systems resist wind as a general envelope lateral-force relationship; no load value or member-sizing claim.');

// MITIGATES
addIfFound('FLS.SPR', 'FLS.EGR.OLO', 'MITIGATES', 'Sprinkler systems mitigate occupant load risk as a general fire-safety life-risk relationship; no specific occupancy or hazard claim.');
addIfFound('FLS.ASS.CAS', 'FLS.EGR.OLO', 'MITIGATES', 'Clean agent systems mitigate occupant load risk as a general fire-safety life-risk relationship; no specific occupancy or hazard claim.');
addIfFound('FLS.CMP.FBA', 'FLS.EGR.TDI', 'MITIGATES', 'Fire barriers mitigate travel distance as a general compartmentation life-safety relationship; no specific distance or code claim.');
addIfFound('FLS.EGR.ELI', 'FLS.EGR.TDI', 'MITIGATES', 'Emergency lighting mitigates travel distance as a general egress safety relationship; no specific distance or code claim.');
addIfFound('SUS.WAT', 'PLS.WST', 'MITIGATES', 'Water sustainability mitigates wastewater as a general water-efficiency relationship; no specific flow or capacity claim.');
addIfFound('SUS.ENE', 'MEC.HVA', 'MITIGATES', 'Energy sustainability mitigates HVAC energy as a general energy-efficiency relationship; no specific consumption or savings claim.');
addIfFound('STR.RET', 'GEO.SOI', 'MITIGATES', 'Retaining walls mitigate soil as a general geotechnical risk-mitigation relationship; no specific load or capacity claim.');
addIfFound('CIV.DRN', 'CIV.WAT.STW', 'MITIGATES', 'Drainage mitigates stormwater as a general flood-risk mitigation relationship; no specific capacity or return-period claim.');

// COLLECTS
addIfFound('PLS.WST.FDR', 'PLS.WST', 'COLLECTS', 'Floor drains collect wastewater as a general drainage collection relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.RDR', 'PLS.WST', 'COLLECTS', 'Roof drains collect wastewater as a general drainage collection relationship; no capacity or pipe-sizing claim.');
addIfFound('CIV.DRN.CSB', 'CIV.WAT.STW', 'COLLECTS', 'Catch basins collect stormwater as a general stormwater collection relationship; no capacity or sizing claim.');
addIfFound('PLS.WST.SMP', 'PLS.WST', 'COLLECTS', 'Sump pumps collect wastewater as a general sump collection relationship; no capacity or pump-sizing claim.');
addIfFound('CIV.DRN.CSB', 'CIV.DRN', 'COLLECTS', 'Catch basins collect drainage as a general drainage collection relationship; no capacity or sizing claim.');
addIfFound('PLS.WST.RDR', 'CIV.DRN', 'COLLECTS', 'Roof drains collect drainage as a general roof drainage collection relationship; no capacity or sizing claim.');
addIfFound('PLS.WST.FDR', 'CIV.DRN', 'COLLECTS', 'Floor drains collect drainage as a general floor drainage collection relationship; no capacity or sizing claim.');
addIfFound('PLS.WST.SMP', 'CIV.DRN', 'COLLECTS', 'Sump pumps collect drainage as a general sump collection relationship; no capacity or pump-sizing claim.');

// DRAINS_TO
addIfFound('PLS.WST.RDR', 'CIV.MIS.STN', 'DRAINS_TO', 'Roof drains drain to stormwater networks as a general roof drainage-to-stormwater relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.FDR', 'CIV.MIS.SEN', 'DRAINS_TO', 'Floor drains drain to sewerage networks as a general floor drainage-to-sewer relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.SMP', 'CIV.MIS.SEN', 'DRAINS_TO', 'Sump pumps drain to sewerage networks as a general sump-to-sewer relationship; no capacity or pipe-sizing claim.');
addIfFound('CIV.DRN.CSB', 'PLS.WST', 'DRAINS_TO', 'Catch basins drain to wastewater as a general stormwater-to-drainage relationship; no capacity or pipe-sizing claim.');
addIfFound('CIV.DRN.CSB', 'CIV.MIS.SEN', 'DRAINS_TO', 'Catch basins drain to sewerage networks as a general drainage-to-sewer relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.SMP', 'PLS.WST', 'DRAINS_TO', 'Sump pumps drain to wastewater as a general sump-to-drainage relationship; no capacity or pump-sizing claim.');
addIfFound('PLS.WST.RDR', 'PLS.WST', 'DRAINS_TO', 'Roof drains drain to wastewater as a general roof drainage relationship; no capacity or pipe-sizing claim.');
addIfFound('PLS.WST.FDR', 'PLS.WST', 'DRAINS_TO', 'Floor drains drain to wastewater as a general floor drainage relationship; no capacity or pipe-sizing claim.');

// Additional COORDINATES_WITH
addIfFound('SMS.BIM', 'DIG.BIM', 'CROSS_DOMAIN_ALIGNMENT', 'Smart BIM and BIM are discipline-scoped views of the same digital-modeling object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('DIG.BIM', 'SMS.BIM', 'CROSS_DOMAIN_ALIGNMENT', 'BIM and smart BIM are discipline-scoped views of the same digital-modeling object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('SMS.IOT', 'ELE.CTL.BMS', 'COORDINATES_WITH', 'IoT coordinates with building management for integration, protocols, and sensors; non-numerical and non-code-specific.');
addIfFound('SMS.IOT', 'ELE.COM.DNE', 'COORDINATES_WITH', 'IoT coordinates with data networks for bandwidth, latency, and security; non-numerical and non-code-specific.');
addIfFound('PER.ENE', 'SUS.ENE', 'CROSS_DOMAIN_ALIGNMENT', 'Energy performance and energy sustainability are discipline-scoped views of the same energy object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('SUS.ENE', 'PER.ENE', 'CROSS_DOMAIN_ALIGNMENT', 'Energy sustainability and energy performance are discipline-scoped views of the same energy object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('PER.ACO', 'ARC.ACO', 'CROSS_DOMAIN_ALIGNMENT', 'Acoustic performance and acoustics are discipline-scoped views of the same acoustic object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');
addIfFound('ARC.ACO', 'PER.ACO', 'CROSS_DOMAIN_ALIGNMENT', 'Acoustics and acoustic performance are discipline-scoped views of the same acoustic object family; alignment only, no equivalence, merge, or identity claim.', 'bidirectional');

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
