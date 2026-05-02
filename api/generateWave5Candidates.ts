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

// Helper to find nodes by path code prefix
function findNodesByPrefix(prefix: string) {
  const results: Array<{id: string; label: string; pathCode: string}> = [];
  for (const [id, pathCode] of nodePathCodes) {
    if (pathCode.startsWith(prefix)) {
      results.push({ id, label: nodeLabels.get(id) || '', pathCode });
    }
  }
  return results;
}

// Build candidates systematically
const candidates: Array<{source: string; target: string; type: string; rationale: string}> = [];

function add(source: string, target: string, type: string, rationale: string) {
  if (!nodeIds.has(source) || !nodeIds.has(target)) return;
  if (source === target) return;
  const key = `${source}|${type}|${target}`;
  if (existingEdgeKeys.has(key)) return;
  candidates.push({ source, target, type, rationale });
  existingEdgeKeys.add(key);
}

// ==========================================
// A. CONNECTS_TO — physical connections
// ==========================================
// Building entrance ↔ site access
const buildingEntrance = findNodesByPrefix('ARC.ACC.ENT');
const siteAccess = findNodesByPrefix('ARC.SIT');
const accessibleRoute = findNodesByPrefix('ARC.ACC');
const sidewalk = findNodesByPrefix('CIV.SID');
const publicWay = findNodesByPrefix('CIV.PUB');
const exitDischarge = findNodesByPrefix('FLS.EGR');
const serviceEntry = findNodesByPrefix('ARC.SER');
const utilityCorridor = findNodesByPrefix('ARC.UTI');
const mechanicalRoom = findNodesByPrefix('ARC.MEC');
const electricalRoom = findNodesByPrefix('ARC.ELE');
const pumpRoom = findNodesByPrefix('ARC.PLS');
const stair = findNodesByPrefix('ARC.CIR');
const elevatorLobby = findNodesByPrefix('ARC.CIR');
const circulationPath = findNodesByPrefix('ARC.CIR');

// Connect entrance to site access if both exist
for (const ent of buildingEntrance.slice(0, 3)) {
  for (const acc of siteAccess.slice(0, 3)) {
    add(ent.id, acc.id, 'CONNECTS_TO', `${ent.label} connects to ${acc.label} as a general building-site physical interface; no jurisdictional standard or specific dimension claim.`);
  }
}

// Accessible route connections
for (const ar of accessibleRoute.filter(n => n.pathCode.includes('ROU') || n.pathCode.includes('ACC')).slice(0, 3)) {
  for (const ent of buildingEntrance.slice(0, 2)) {
    add(ar.id, ent.id, 'CONNECTS_TO', `${ar.label} connects to ${ent.label} as a general accessibility circulation interface; no code-compliance or specific dimension claim.`);
  }
}

// Exit discharge to public way
for (const ed of exitDischarge.filter(n => n.pathCode.includes('EXI') || n.pathCode.includes('DIS')).slice(0, 3)) {
  for (const pw of publicWay.slice(0, 2)) {
    add(ed.id, pw.id, 'CONNECTS_TO', `${ed.label} connects to ${pw.label} as a general egress discharge interface; no specific width or code section claim.`);
  }
}

// Service entry to utility corridor
for (const se of serviceEntry.slice(0, 2)) {
  for (const uc of utilityCorridor.slice(0, 2)) {
    add(se.id, uc.id, 'CONNECTS_TO', `${se.label} connects to ${uc.label} as a general building service distribution interface; no specific routing or capacity claim.`);
  }
}

// Mechanical/electrical/plumbing rooms to service entry
for (const mr of mechanicalRoom.slice(0, 2)) {
  for (const se of serviceEntry.slice(0, 1)) {
    add(mr.id, se.id, 'CONNECTS_TO', `${mr.label} connects to ${se.label} as a general building service access interface; no specific sizing or code claim.`);
  }
}
for (const er of electricalRoom.slice(0, 2)) {
  for (const se of serviceEntry.slice(0, 1)) {
    add(er.id, se.id, 'CONNECTS_TO', `${er.label} connects to ${se.label} as a general electrical service access interface; no specific sizing or code claim.`);
  }
}
for (const pr of pumpRoom.slice(0, 2)) {
  for (const se of serviceEntry.slice(0, 1)) {
    add(pr.id, se.id, 'CONNECTS_TO', `${pr.label} connects to ${se.label} as a general plumbing service access interface; no specific sizing or code claim.`);
  }
}

// ==========================================
// B. Mechanical / HVAC flow and coordination
// ==========================================
const ahu = findNodesByPrefix('MEC.AHD.AHU');
const ductDesign = findNodesByPrefix('MEC.AHD.DUD');
const diffusers = findNodesByPrefix('MEC.AHD.DTD');
const returnAir = findNodesByPrefix('MEC.AHD.RET');
const exhaustFan = findNodesByPrefix('MEC.AHD.EXT');
const exhaustOutlet = findNodesByPrefix('MEC.AHD.EOT');
const coolingTower = findNodesByPrefix('MEC.COO.CTW');
const chilledWater = findNodesByPrefix('MEC.HPS.CWL');
const hotWater = findNodesByPrefix('MEC.HPS.HWL');
const boiler = findNodesByPrefix('MEC.HPS.BOI');
const airDistribution = findNodesByPrefix('MEC.AHD');
const occupiedSpace = findNodesByPrefix('ARC.ENV.OCC');
const ceilingPlenum = findNodesByPrefix('ARC.CEL');

// AHU → air distribution → occupied space
for (const a of ahu.slice(0, 1)) {
  for (const ad of airDistribution.filter(n => n.pathCode.includes('AIR') || n.pathCode.includes('DIS')).slice(0, 2)) {
    add(a.id, ad.id, 'CONVEYS', `${a.label} conveys supply air to ${ad.label} as a general HVAC air distribution relationship; no airflow rate or duct-sizing claim.`);
  }
}

// Return air path
for (const ra of returnAir.slice(0, 1)) {
  for (const a of ahu.slice(0, 1)) {
    add(ra.id, a.id, 'CONVEYS', `${ra.label} conveys return air to ${a.label} as a general HVAC return-air relationship; no airflow rate or duct-sizing claim.`);
  }
}

// Exhaust fan → exhaust outlet
for (const ef of exhaustFan.slice(0, 1)) {
  for (const eo of exhaustOutlet.slice(0, 1)) {
    add(ef.id, eo.id, 'DISCHARGES_TO', `${ef.label} discharges to ${eo.label} as a general HVAC exhaust discharge relationship; no airflow rate or fan-sizing claim.`);
  }
}

// Ductwork coordinates with structural opening / ceiling plenum
for (const dd of ductDesign.slice(0, 1)) {
  for (const cp of ceilingPlenum.slice(0, 2)) {
    add(dd.id, cp.id, 'COORDINATES_WITH', `${dd.label} coordinates with ${cp.label} for routing, access, and clearance; non-numerical and non-code-specific.`);
  }
}

// Cooling tower coordinates with structural support
for (const ct of coolingTower.slice(0, 1)) {
  for (const fs of findNodesByPrefix('STR.SYS.FRM').slice(0, 1)) {
    add(ct.id, fs.id, 'COORDINATES_WITH', `${ct.label} coordinates with ${fs.label} for equipment support, vibration isolation, and roof access; non-numerical and non-code-specific.`);
  }
}

// Chilled water → AHU coil if endpoint exists
for (const cw of chilledWater.slice(0, 1)) {
  for (const a of ahu.slice(0, 1)) {
    add(cw.id, a.id, 'CONVEYS', `${cw.label} conveys chilled water to ${a.label} as a general hydronic cooling relationship; no flow rate or capacity claim.`);
  }
}

// Hot water → terminal unit
for (const hw of hotWater.slice(0, 1)) {
  for (const tu of findNodesByPrefix('MEC.HPS').filter(n => n.pathCode.includes('TER') || n.pathCode.includes('RAD') || n.pathCode.includes('UNIT')).slice(0, 2)) {
    add(hw.id, tu.id, 'CONVEYS', `${hw.label} conveys hot water to ${tu.label} as a general hydronic heating relationship; no flow rate or capacity claim.`);
  }
}

// Boiler → hot water loop
for (const b of boiler.slice(0, 1)) {
  for (const hw of hotWater.slice(0, 1)) {
    add(b.id, hw.id, 'CONVEYS', `${b.label} conveys heating to ${hw.label} as a general boiler-to-distribution relationship; no capacity or temperature claim.`);
  }
}

// ==========================================
// C. Plumbing / sanitary / storm
// ==========================================
const waterServiceEntry = findNodesByPrefix('PLS.PWS');
const domesticWater = findNodesByPrefix('PLS.PWS');
const sanitaryFixture = findNodesByPrefix('PLS.FIX');
const sanitaryDrainage = findNodesByPrefix('PLS.WST');
const roofDrain = findNodesByPrefix('PLS.WST.RDR');
const floorDrain = findNodesByPrefix('PLS.WST.FDR');
const catchBasin = findNodesByPrefix('CIV.DRN.CSB');
const stormSewerPipe = findNodesByPrefix('CIV.MIS.STN');
const sumpPump = findNodesByPrefix('PLS.WST.SMP');
const sewerNetwork = findNodesByPrefix('CIV.MIS.SEN');
const waterMeter = findNodesByPrefix('PLS.PWS.WSM');

// Water service entry → water supply network
for (const wse of waterServiceEntry.slice(0, 1)) {
  for (const wdn of findNodesByPrefix('CIV.MIS.WDN').slice(0, 1)) {
    add(wse.id, wdn.id, 'CONNECTS_TO', `${wse.label} connects to ${wdn.label} as a general building-to-utility water interface; no pressure or sizing claim.`);
  }
}

// Domestic water piping conveys potable water
for (const dw of domesticWater.slice(0, 1)) {
  for (const sf of sanitaryFixture.slice(0, 3)) {
    add(dw.id, sf.id, 'CONVEYS', `${dw.label} conveys potable water to ${sf.label} as a general plumbing supply relationship; no fixture-unit or pressure claim.`);
  }
}

// Sanitary fixture discharges to sanitary drainage
for (const sf of sanitaryFixture.slice(0, 3)) {
  for (const sd of sanitaryDrainage.slice(0, 1)) {
    add(sf.id, sd.id, 'DISCHARGES_TO', `${sf.label} discharges to ${sd.label} as a general fixture-to-drainage relationship; no flow rate or pipe-sizing claim.`);
  }
}

// Sanitary drainage discharges to sewer network
for (const sd of sanitaryDrainage.slice(0, 1)) {
  for (const sn of sewerNetwork.slice(0, 1)) {
    add(sd.id, sn.id, 'DISCHARGES_TO', `${sd.label} discharges to ${sn.label} as a general building drainage-to-sewer relationship; no capacity or slope claim.`);
  }
}

// Roof drain drains to stormwater
for (const rd of roofDrain.slice(0, 1)) {
  for (const stn of findNodesByPrefix('CIV.MIS.STN').slice(0, 1)) {
    add(rd.id, stn.id, 'DRAINS_TO', `${rd.label} drains to ${stn.label} as a general roof drainage-to-stormwater relationship; no capacity or pipe-sizing claim.`);
  }
}

// Floor drain drains to drainage
for (const fd of floorDrain.slice(0, 1)) {
  for (const drn of findNodesByPrefix('CIV.DRN').slice(0, 1)) {
    add(fd.id, drn.id, 'DRAINS_TO', `${fd.label} drains to ${drn.label} as a general floor drainage relationship; no capacity or pipe-sizing claim.`);
  }
}

// Catch basin drains to storm sewer pipe
for (const cb of catchBasin.slice(0, 1)) {
  for (const ssp of stormSewerPipe.slice(0, 1)) {
    add(cb.id, ssp.id, 'DRAINS_TO', `${cb.label} drains to ${ssp.label} as a general stormwater collection-to-conveyance relationship; no capacity or pipe-sizing claim.`);
  }
}

// Storm sewer pipe conveys stormwater
for (const ssp of stormSewerPipe.slice(0, 1)) {
  for (const sw of findNodesByPrefix('CIV.WAT.STW').slice(0, 1)) {
    add(ssp.id, sw.id, 'CONVEYS', `${ssp.label} conveys stormwater to ${sw.label} as a general stormwater conveyance relationship; no flow rate or pipe-sizing claim.`);
  }
}

// Sump pump discharges to drainage
for (const sp of sumpPump.slice(0, 1)) {
  for (const drn of findNodesByPrefix('CIV.DRN').slice(0, 1)) {
    add(sp.id, drn.id, 'DISCHARGES_TO', `${sp.label} discharges to ${drn.label} as a general sump discharge relationship; no capacity or pump-sizing claim.`);
  }
}

// ==========================================
// D. Fire / life safety
// ==========================================
const smokeDetector = findNodesByPrefix('FLS.DET.SMK');
const heatDetector = findNodesByPrefix('FLS.DET.HEA');
const fireAlarmPanel = findNodesByPrefix('FLS.ALM.FAC');
const occupantNotification = findNodesByPrefix('FLS.ALM.NOT');
const sprinklerSystem = findNodesByPrefix('FLS.SPR');
const fireBarrier = findNodesByPrefix('FLS.CMP.FBA');
const compartmentation = findNodesByPrefix('ARC.FIR.COM');
const egressCapacity = findNodesByPrefix('FLS.EGR.ECA');
const exitAccess = findNodesByPrefix('FLS.EGR.EAC');
const emergencyLighting = findNodesByPrefix('FLS.EGR.ELI');
const egressRoute = findNodesByPrefix('FLS.EGR.ERO');
const firePump = findNodesByPrefix('FLS.SPR.FPU');
const detection = findNodesByPrefix('FLS.ALM.DET');

// Smoke detector → fire alarm control panel
for (const sd of smokeDetector.slice(0, 1)) {
  for (const fap of fireAlarmPanel.slice(0, 1)) {
    add(sd.id, fap.id, 'INFORMS', `${sd.label} informs ${fap.label} as a general fire-safety sensor-to-panel relationship; no device-specification or code-compliance claim.`);
  }
}

// Heat detector → fire alarm control panel
for (const hd of heatDetector.slice(0, 1)) {
  for (const fap of fireAlarmPanel.slice(0, 1)) {
    add(hd.id, fap.id, 'INFORMS', `${hd.label} informs ${fap.label} as a general fire-safety sensor-to-panel relationship; no device-specification or code-compliance claim.`);
  }
}

// Fire alarm panel → occupant notification
for (const fap of fireAlarmPanel.slice(0, 1)) {
  for (const on of occupantNotification.slice(0, 1)) {
    add(fap.id, on.id, 'INFORMS', `${fap.label} informs ${on.label} as a general fire-alarm-to-notification relationship; no device-specification or code-compliance claim.`);
  }
}

// Sprinkler system coordinates with ceiling layout
for (const ss of sprinklerSystem.slice(0, 1)) {
  for (const cl of ceilingPlenum.slice(0, 1)) {
    add(ss.id, cl.id, 'COORDINATES_WITH', `${ss.label} coordinates with ${cl.label} for head placement, coverage, and access; non-numerical and non-code-specific.`);
  }
}

// Fire barrier coordinates with compartmentation (already have some, check for more)
for (const fb of fireBarrier.slice(0, 1)) {
  for (const comp of compartmentation.slice(0, 1)) {
    add(fb.id, comp.id, 'COORDINATES_WITH', `${fb.label} coordinates with ${comp.label} for continuity and penetration management; non-numerical and non-code-specific.`);
  }
}

// Exit access coordinates with floor plan
for (const ea of exitAccess.slice(0, 1)) {
  for (const fp of findNodesByPrefix('ARC.FLO').slice(0, 1)) {
    add(ea.id, fp.id, 'COORDINATES_WITH', `${ea.label} coordinates with ${fp.label} for location, width, and door swing; non-numerical and non-code-specific.`);
  }
}

// Emergency lighting coordinates with egress route
for (const el of emergencyLighting.slice(0, 1)) {
  for (const er of egressRoute.slice(0, 1)) {
    add(el.id, er.id, 'COORDINATES_WITH', `${el.label} coordinates with ${er.label} for illumination, placement, and power; non-numerical and non-code-specific.`);
  }
}

// Fire pump supports sprinkler system
for (const fp of firePump.slice(0, 1)) {
  for (const ss of sprinklerSystem.slice(0, 1)) {
    add(fp.id, ss.id, 'SUPPORTS', `${fp.label} supports ${ss.label} as a general fire-protection equipment relationship; no capacity or pressure claim.`);
  }
}

// ==========================================
// E. Electrical
// ==========================================
const groundingElectrode = findNodesByPrefix('ELE.GRD.GES');
const electricalServiceEntry = findNodesByPrefix('ELE.SES');
const panelboard = findNodesByPrefix('ELE.DIS.PAN');
const cableTray = findNodesByPrefix('ELE.CAB');
const standbyGenerator = findNodesByPrefix('ELE.EPW.GEN');
const emergencyPowerSystem = findNodesByPrefix('ELE.EPW');
const lifeSafetyLoads = findNodesByPrefix('ELE.LOA.LSL');
const electricalRoom2 = findNodesByPrefix('ARC.ELE');
const utilityService = findNodesByPrefix('ELE.UTI');
const transformer = findNodesByPrefix('ELE.TRA');
const switchgear = findNodesByPrefix('ELE.SWI');

// Grounding electrode coordinates with foundation
for (const ge of groundingElectrode.slice(0, 1)) {
  for (const fi of findNodesByPrefix('STR.FND').slice(0, 1)) {
    add(ge.id, fi.id, 'COORDINATES_WITH', `${ge.label} coordinates with ${fi.label} for earth-contact area, embedment, and corrosion protection; non-numerical and non-code-specific.`);
  }
}

// Electrical service entry connects to utility service
for (const ese of electricalServiceEntry.slice(0, 1)) {
  for (const us of utilityService.slice(0, 1)) {
    add(ese.id, us.id, 'CONNECTS_TO', `${ese.label} connects to ${us.label} as a general building-to-utility electrical interface; no voltage or capacity claim.`);
  }
}

// Panelboard coordinates with electrical room
for (const pb of panelboard.slice(0, 1)) {
  for (const er2 of electricalRoom2.slice(0, 1)) {
    add(pb.id, er2.id, 'COORDINATES_WITH', `${pb.label} coordinates with ${er2.label} for clearances, access, and ventilation; non-numerical and non-code-specific.`);
  }
}

// Cable tray coordinates with ceiling plenum
for (const ct of cableTray.slice(0, 1)) {
  for (const cp of ceilingPlenum.slice(0, 1)) {
    add(ct.id, cp.id, 'COORDINATES_WITH', `${ct.label} coordinates with ${cp.label} for routing, access, and support; non-numerical and non-code-specific.`);
  }
}

// Standby generator supports emergency power system
for (const sg of standbyGenerator.slice(0, 1)) {
  for (const eps of emergencyPowerSystem.slice(0, 1)) {
    add(sg.id, eps.id, 'SUPPORTS', `${sg.label} supports ${eps.label} as a general emergency power equipment relationship; no capacity or runtime claim.`);
  }
}

// Emergency power system supports life-safety loads
for (const eps of emergencyPowerSystem.slice(0, 1)) {
  for (const lsl of lifeSafetyLoads.slice(0, 1)) {
    add(eps.id, lsl.id, 'SUPPORTS', `${eps.label} supports ${lsl.label} as a general emergency power-to-load relationship; no capacity or circuit claim.`);
  }
}

// Transformer coordinates with electrical room
for (const tr of transformer.slice(0, 1)) {
  for (const er2 of electricalRoom2.slice(0, 1)) {
    add(tr.id, er2.id, 'COORDINATES_WITH', `${tr.label} coordinates with ${er2.label} for clearances, ventilation, and access; non-numerical and non-code-specific.`);
  }
}

// Switchgear coordinates with electrical room
for (const sw of switchgear.slice(0, 1)) {
  for (const er2 of electricalRoom2.slice(0, 1)) {
    add(sw.id, er2.id, 'COORDINATES_WITH', `${sw.label} coordinates with ${er2.label} for clearances, ventilation, and access; non-numerical and non-code-specific.`);
  }
}

// ==========================================
// F. Architecture / structure / MEPFS coordination
// ==========================================
const shaft = findNodesByPrefix('ARC.SHA');
const plumbingRiser = findNodesByPrefix('PLS.RIS');
const structuralOpening = findNodesByPrefix('STR.OPE');
const mepPenetration = findNodesByPrefix('MEC.PEN');
const slabOpening = findNodesByPrefix('STR.SLB.OPE');
const verticalServices = findNodesByPrefix('ARC.VSE');
const roofStructure = findNodesByPrefix('ARC.ENV.ROF');
const rooftopEquipment = findNodesByPrefix('MEC.ROO');
const facade = findNodesByPrefix('ARC.ENV.WAL');
const louvers = findNodesByPrefix('ARC.ENV.LOU');
const exhaustOutlet2 = findNodesByPrefix('MEC.AHD.EOT');
const equipmentClearance = findNodesByPrefix('ARC.MEC.CLR');
const equipmentRoom = findNodesByPrefix('ARC.MEC');

// Shaft coordinates with ductwork
for (const sh of shaft.slice(0, 1)) {
  for (const dd of ductDesign.slice(0, 1)) {
    add(sh.id, dd.id, 'COORDINATES_WITH', `${sh.label} coordinates with ${dd.label} for sizing, fire stopping, and access; non-numerical and non-code-specific.`);
  }
}

// Shaft coordinates with plumbing riser
for (const sh of shaft.slice(0, 1)) {
  for (const pr of plumbingRiser.slice(0, 1)) {
    add(sh.id, pr.id, 'COORDINATES_WITH', `${sh.label} coordinates with ${pr.label} for sizing, fire stopping, and access; non-numerical and non-code-specific.`);
  }
}

// Structural opening coordinates with MEP penetration
for (const so of structuralOpening.slice(0, 1)) {
  for (const mp of mepPenetration.slice(0, 1)) {
    add(so.id, mp.id, 'COORDINATES_WITH', `${so.label} coordinates with ${mp.label} for sizing, fire stopping, and sealing; non-numerical and non-code-specific.`);
  }
}

// Slab opening coordinates with vertical services
for (const so2 of slabOpening.slice(0, 1)) {
  for (const vs of verticalServices.slice(0, 1)) {
    add(so2.id, vs.id, 'COORDINATES_WITH', `${so2.label} coordinates with ${vs.label} for sizing, reinforcement, and fire stopping; non-numerical and non-code-specific.`);
  }
}

// Roof structure supports rooftop equipment
for (const rs of roofStructure.slice(0, 1)) {
  for (const re of rooftopEquipment.slice(0, 1)) {
    add(rs.id, re.id, 'SUPPORTS', `${rs.label} supports ${re.label} as a general structural-equipment support relationship; no load value or member-sizing claim.`);
  }
}

// Facade coordinates with louvers / exhaust outlet
for (const f of facade.slice(0, 1)) {
  for (const l of louvers.slice(0, 1)) {
    add(f.id, l.id, 'COORDINATES_WITH', `${f.label} coordinates with ${l.label} for weatherproofing, thermal bridging, and appearance; non-numerical and non-code-specific.`);
  }
}
for (const f of facade.slice(0, 1)) {
  for (const eo of exhaustOutlet2.slice(0, 1)) {
    add(f.id, eo.id, 'COORDINATES_WITH', `${f.label} coordinates with ${eo.label} for weatherproofing, thermal bridging, and appearance; non-numerical and non-code-specific.`);
  }
}

// Ceiling plenum coordinates with ductwork
for (const cp of ceilingPlenum.slice(0, 1)) {
  for (const dd of ductDesign.slice(0, 1)) {
    add(cp.id, dd.id, 'COORDINATES_WITH', `${cp.label} coordinates with ${dd.label} for routing, access, and clearance; non-numerical and non-code-specific.`);
  }
}

// Equipment clearance constrains equipment room layout
for (const ec of equipmentClearance.slice(0, 1)) {
  for (const er of equipmentRoom.slice(0, 1)) {
    add(ec.id, er.id, 'CONSTRAINS', `${ec.label} conceptually constrains ${er.label} as a general equipment-planning relationship; no specific dimension or code claim.`);
  }
}

// ==========================================
// G. Civil / site / building interface
// ==========================================
const siteGrading = findNodesByPrefix('CIV.SIT.GRA');
const buildingPad = findNodesByPrefix('ARC.SIT.PAD');
const retainingWall = findNodesByPrefix('STR.RET');
const earthworks = findNodesByPrefix('CIV.EAR');
const foundationExcavation = findNodesByPrefix('CIV.FND');
const siteDrainage = findNodesByPrefix('CIV.DRN');
const siteUtilities = findNodesByPrefix('CIV.UTI');
const curbRamp = findNodesByPrefix('ARC.ACC.CRA');
const accessibleParking = findNodesByPrefix('ARC.ACC.PAR');
const sidewalk2 = findNodesByPrefix('CIV.SID');
const siteAccess2 = findNodesByPrefix('ARC.SIT.ACC');

// Site grading coordinates with building pad
for (const sg of siteGrading.slice(0, 1)) {
  for (const bp of buildingPad.slice(0, 1)) {
    add(sg.id, bp.id, 'COORDINATES_WITH', `${sg.label} coordinates with ${bp.label} for drainage, slope, and elevation; non-numerical and non-jurisdiction-specific.`);
  }
}

// Site drainage coordinates with building pad
for (const sd of siteDrainage.slice(0, 1)) {
  for (const bp of buildingPad.slice(0, 1)) {
    add(sd.id, bp.id, 'COORDINATES_WITH', `${sd.label} coordinates with ${bp.label} for runoff, slope, and discharge; non-numerical and non-jurisdiction-specific.`);
  }
}

// Site utilities coordinate with building pad
for (const su of siteUtilities.slice(0, 1)) {
  for (const bp of buildingPad.slice(0, 1)) {
    add(su.id, bp.id, 'COORDINATES_WITH', `${su.label} coordinates with ${bp.label} for routing, invert elevations, and access; non-numerical and non-jurisdiction-specific.`);
  }
}

// Foundation excavation coordinates with earthworks
for (const fe of foundationExcavation.slice(0, 1)) {
  for (const ew of earthworks.slice(0, 1)) {
    add(fe.id, ew.id, 'COORDINATES_WITH', `${fe.label} coordinates with ${ew.label} for cut/fill balance, shoring, and dewatering; non-numerical and non-jurisdiction-specific.`);
  }
}

// Curb ramp connects to sidewalk
for (const cr of curbRamp.slice(0, 1)) {
  for (const sw of sidewalk2.slice(0, 1)) {
    add(cr.id, sw.id, 'CONNECTS_TO', `${cr.label} connects to ${sw.label} as a general accessible route interface; no specific slope or width claim.`);
  }
}

// Accessible parking connects to accessible route
for (const ap of accessibleParking.slice(0, 1)) {
  for (const ar of accessibleRoute.slice(0, 1)) {
    add(ap.id, ar.id, 'CONNECTS_TO', `${ap.label} connects to ${ar.label} as a general accessible parking interface; no specific dimension or code claim.`);
  }
}

// Site access connects to sidewalk
for (const sa of siteAccess2.slice(0, 1)) {
  for (const sw of sidewalk2.slice(0, 1)) {
    add(sa.id, sw.id, 'CONNECTS_TO', `${sa.label} connects to ${sw.label} as a general site circulation interface; no specific width or code claim.`);
  }
}

// ==========================================
// H. Additional cross-domain alignments
// ==========================================
// Look for discipline-scoped pairs that might need alignment
const hvacSystem = findNodesByPrefix('MEC.HVA');
const airConditioning = findNodesByPrefix('MEC.ACD');
const heatingSystem = findNodesByPrefix('MEC.HEA');
const ventilation = findNodesByPrefix('MEC.VEN');

// HVAC system ↔ air conditioning
for (const hv of hvacSystem.slice(0, 1)) {
  for (const ac of airConditioning.slice(0, 1)) {
    add(hv.id, ac.id, 'CROSS_DOMAIN_ALIGNMENT', `${hv.label} and ${ac.label} are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.`);
    add(ac.id, hv.id, 'CROSS_DOMAIN_ALIGNMENT', `${ac.label} and ${hv.label} are discipline-scoped views of the same climate-control object family; alignment only, no equivalence, merge, or identity claim.`);
  }
}

// Heating system ↔ hydronic heating
for (const hs of heatingSystem.slice(0, 1)) {
  for (const hh of findNodesByPrefix('MEC.HPS.HWL').slice(0, 1)) {
    add(hs.id, hh.id, 'CROSS_DOMAIN_ALIGNMENT', `${hs.label} and ${hh.label} are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.`);
    add(hh.id, hs.id, 'CROSS_DOMAIN_ALIGNMENT', `${hh.label} and ${hs.label} are discipline-scoped views of the same heating object family; alignment only, no equivalence, merge, or identity claim.`);
  }
}

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
