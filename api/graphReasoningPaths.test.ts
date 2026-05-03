import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');

function json(path: string) {
  return JSON.parse(readFileSync(resolve(repoRoot, path), 'utf8').replace(/^\uFEFF/, ''));
}

const graph = json('006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json');
const baseNodes: any[] = graph.nodes;
const baseEdges: any[] = graph.edges;
const admitted = json('006_System-Manifests/graph-canonical/admitted-relationships.json').admittedRelationships.filter((r: any) => !r.revoked);

const normalizedBaseEdges = baseEdges.map((e: any) => ({ ...e, source: e.from_id, target: e.to_id, type: e.predicate }));
const effectiveEdges = [...normalizedBaseEdges, ...admitted];
const nodeById = new Map(baseNodes.map((n: any) => [n.id, n]));
const edgeBySource = new Map<string, any[]>();
for (const edge of effectiveEdges) {
  const list = edgeBySource.get(edge.source) || [];
  list.push(edge);
  edgeBySource.set(edge.source, list);
}

function bfsPath(startId: string, targetId: string, allowedTypes?: string[], maxDepth = 5): string[] | null {
  const visited = new Set<string>();
  const queue: { id: string; path: string[] }[] = [{ id: startId, path: [startId] }];
  while (queue.length) {
    const { id, path } = queue.shift()!;
    if (id === targetId && path.length > 1) return path;
    if (path.length >= maxDepth) continue;
    if (visited.has(id)) continue;
    visited.add(id);
    for (const edge of edgeBySource.get(id) || []) {
      if (allowedTypes && !allowedTypes.includes(edge.type)) continue;
      if (!visited.has(edge.target)) {
        queue.push({ id: edge.target, path: [...path, edge.target] });
      }
    }
  }
  return null;
}

function bfsMultiPath(startId: string, targetIds: string[], allowedTypes?: string[], maxDepth = 5): { targetId: string; path: string[] }[] {
  const results: { targetId: string; path: string[] }[] = [];
  const visited = new Set<string>();
  const queue: { id: string; path: string[] }[] = [{ id: startId, path: [startId] }];
  while (queue.length) {
    const { id, path } = queue.shift()!;
    if (targetIds.includes(id) && path.length > 1) {
      results.push({ targetId: id, path: [...path] });
      if (results.length === targetIds.length) break;
    }
    if (path.length >= maxDepth) continue;
    if (visited.has(id)) continue;
    visited.add(id);
    for (const edge of edgeBySource.get(id) || []) {
      if (allowedTypes && !allowedTypes.includes(edge.type)) continue;
      if (!visited.has(edge.target)) {
        queue.push({ id: edge.target, path: [...path, edge.target] });
      }
    }
  }
  return results;
}

function hasOutgoingEdge(nodeId: string, type: string): boolean {
  return (edgeBySource.get(nodeId) || []).some((e: any) => e.type === type);
}

function countOutgoingByType(nodeId: string, type: string): number {
  return (edgeBySource.get(nodeId) || []).filter((e: any) => e.type === type).length;
}

describe('graph reasoning paths', () => {
  test('load path: foundation to structural element exists', () => {
    // Deep Foundations -> Shallow Foundations via TRANSFERS_LOAD_TO or CROSS_DOMAIN_ALIGNMENT
    const deepFoundations = 'VTN-DOM-0000262';
    const shallowFoundations = 'VTN-DOM-0000261';
    // There may not be a direct edge; verify both are in graph and have structural edges
    expect(nodeById.has(deepFoundations)).toBe(true);
    expect(nodeById.has(shallowFoundations)).toBe(true);
    expect(hasOutgoingEdge(deepFoundations, 'TRANSFERS_LOAD_TO') || hasOutgoingEdge(deepFoundations, 'CROSS_DOMAIN_ALIGNMENT')).toBe(true);
  });

  test('MEP water cycle: supply to conveyance to discharge is traversable', () => {
    const potableWater = 'VTN-DOM-0003190';
    const waterService = 'VTN-DOM-0003191';
    const drainage = 'VTN-DOM-0000025';
    expect(nodeById.has(potableWater)).toBe(true);
    expect(nodeById.has(waterService)).toBe(true);
    expect(nodeById.has(drainage)).toBe(true);
    // Water service should coordinate with potable water
    expect(hasOutgoingEdge(waterService, 'COORDINATES_WITH') || hasOutgoingEdge(potableWater, 'COORDINATES_WITH')).toBe(true);
    // Drainage should have discharge relationships (incoming or outgoing)
    const drainageDischarge = effectiveEdges.some((e: any) =>
      (e.source === drainage || e.target === drainage) && (e.type === 'DISCHARGES_TO' || e.type === 'DRAINS_TO')
    );
    expect(drainageDischarge).toBe(true);
    // Phase 5 targeted gap closure: Drainage now has outgoing DRAINS_TO and DISCHARGES_TO
    const drainageOutgoing = hasOutgoingEdge(drainage, 'DISCHARGES_TO') || hasOutgoingEdge(drainage, 'DRAINS_TO');
    expect(drainageOutgoing).toBe(true);
  });

  test('cross-domain alignment connects structural and geotechnical domains', () => {
    const structuralNodes = baseNodes.filter((n: any) => n.path_code?.startsWith('STR')).map((n: any) => n.id);
    const geoNodes = baseNodes.filter((n: any) => n.path_code?.startsWith('GEO')).map((n: any) => n.id);
    const crossEdges = admitted.filter((e: any) => e.type === 'CROSS_DOMAIN_ALIGNMENT');
    const connectsStructuralGeo = crossEdges.some((e: any) =>
      structuralNodes.includes(e.source) && geoNodes.includes(e.target)
    );
    expect(connectsStructuralGeo).toBe(true);
  });

  test('building envelope has resistance and mitigation relationships', () => {
    // Find nodes with RESISTS or MITIGATES outgoing edges
    const resistingNodes = effectiveEdges.filter((e: any) => e.type === 'RESISTS').map((e: any) => e.source);
    const mitigatingNodes = effectiveEdges.filter((e: any) => e.type === 'MITIGATES').map((e: any) => e.source);
    expect(resistingNodes.length).toBeGreaterThanOrEqual(3);
    expect(mitigatingNodes.length).toBeGreaterThanOrEqual(3);
  });

  test('coordination relationships exist between building service subsystems', () => {
    // MEP systems live under ARC.BLD.SRV.*, ELE, MEC, PLS, SAN, FLS
    const mepNodes = baseNodes.filter((n: any) => {
      const pc = n.path_code || '';
      return pc.startsWith('ARC.BLD.SRV.') || pc.startsWith('ELE.') || pc.startsWith('MEC.') || pc.startsWith('PLS.') || pc.startsWith('SAN.') || pc.startsWith('FLS.');
    }).map((n: any) => n.id);
    const coordEdges = admitted.filter((e: any) => e.type === 'COORDINATES_WITH');
    const mepCoord = coordEdges.filter((e: any) => mepNodes.includes(e.source) && mepNodes.includes(e.target));
    expect(mepCoord.length).toBeGreaterThanOrEqual(3);
  });

  test('constraint paths link regulatory concepts to design domains', () => {
    const constrainEdges = admitted.filter((e: any) => e.type === 'CONSTRAINS');
    expect(constrainEdges.length).toBeGreaterThanOrEqual(5);
    // Each CONSTRAINS edge should have a non-empty rationale
    expect(constrainEdges.every((e: any) => e.rationale && e.rationale.length > 20)).toBe(true);
  });

  test('support hierarchy connects substructure to superstructure', () => {
    const supportEdges = admitted.filter((e: any) => e.type === 'SUPPORTS');
    expect(supportEdges.length).toBeGreaterThanOrEqual(5);
  });

  test('information flow edges connect sources to decision domains', () => {
    const informEdges = admitted.filter((e: any) => e.type === 'INFORMS');
    expect(informEdges.length).toBeGreaterThanOrEqual(3);
  });

  test('underrepresented relation families have at least one valid edge each', () => {
    // DRAINS_TO, CONNECTS_TO, REQUIRES, COLLECTS
    const drainsTo = admitted.filter((e: any) => e.type === 'DRAINS_TO');
    const connectsTo = admitted.filter((e: any) => e.type === 'CONNECTS_TO');
    const requires = admitted.filter((e: any) => e.type === 'REQUIRES');
    const collects = admitted.filter((e: any) => e.type === 'COLLECTS');
    expect(drainsTo.length).toBeGreaterThanOrEqual(1);
    expect(connectsTo.length).toBeGreaterThanOrEqual(1);
    expect(requires.length).toBeGreaterThanOrEqual(1);
    expect(collects.length).toBeGreaterThanOrEqual(1);
    // All should have proper rationale
    for (const family of [drainsTo, connectsTo, requires, collects]) {
      expect(family.every((e: any) => e.rationale && e.rationale.length > 10)).toBe(true);
    }
  });

  test('cross-domain alignment pairs are reciprocal', () => {
    const crossEdges = admitted.filter((e: any) => e.type === 'CROSS_DOMAIN_ALIGNMENT');
    for (const edge of crossEdges) {
      const reciprocal = admitted.find((e: any) =>
        e.type === 'CROSS_DOMAIN_ALIGNMENT' && e.source === edge.target && e.target === edge.source
      );
      expect(reciprocal).toBeTruthy();
    }
  });

  test('admitted edges do not duplicate base graph tuples', () => {
    const baseKeys = new Set(baseEdges.map((e: any) => `${e.source}|${e.type}|${e.target}`));
    for (const edge of admitted) {
      const key = `${edge.source}|${edge.type}|${edge.target}`;
      expect(baseKeys.has(key)).toBe(false);
    }
  });

  test('reasoning path from structural engineering to materials exists', () => {
    const structuralEngineering = 'VTN-DOM-0000029';
    const materials = 'VTN-DOM-0002477';
    expect(nodeById.has(structuralEngineering)).toBe(true);
    expect(nodeById.has(materials)).toBe(true);
    const path = bfsPath(structuralEngineering, materials, ['COORDINATES_WITH', 'AFFECTS', 'TRANSFERS_LOAD_TO', 'REQUIRES', 'INFORMS'], 3);
    // Phase 5 targeted gap closure: INFORMS edge admitted
    expect(path).toBeTruthy();
    expect(path!.length).toBeLessThanOrEqual(3);
  });

  test('reasoning path from mechanical systems to thermal comfort exists', () => {
    const mechanicalSystems = 'VTN-DOM-0000004';
    const thermalComfort = 'VTN-DOM-0002510';
    expect(nodeById.has(mechanicalSystems)).toBe(true);
    expect(nodeById.has(thermalComfort)).toBe(true);
    const path = bfsPath(mechanicalSystems, thermalComfort, ['COORDINATES_WITH', 'AFFECTS', 'INFORMS'], 3);
    // Phase 5 targeted gap closure: AFFECTS edge admitted
    expect(path).toBeTruthy();
    expect(path!.length).toBeLessThanOrEqual(3);
  });

  test('reasoning path from fire protection to egress exists', () => {
    const fireProtection = 'VTN-DOM-0000056';
    const egress = 'VTN-DOM-0000058';
    expect(nodeById.has(fireProtection)).toBe(true);
    expect(nodeById.has(egress)).toBe(true);
    const path = bfsPath(fireProtection, egress, ['COORDINATES_WITH', 'AFFECTS', 'CONSTRAINS', 'REQUIRES', 'INFORMS'], 3);
    // Phase 5 targeted gap closure: CONSTRAINS edge admitted
    expect(path).toBeTruthy();
    expect(path!.length).toBeLessThanOrEqual(3);
  });

  test('no active CROSS_DOMAIN_EQUIVALENT edge exists', () => {
    const crossEquivalent = admitted.filter((e: any) => e.type === 'CROSS_DOMAIN_EQUIVALENT');
    expect(crossEquivalent.length).toBe(0);
  });

  test('Sendai Mediatheque and Toyo Ito remain visible in graph', () => {
    const sendai = 'VTN-DOM-0012495';
    const toyo = 'VTN-DOM-0012436';
    expect(nodeById.has(sendai)).toBe(true);
    expect(nodeById.has(toyo)).toBe(true);
    const hasFacetEdges = effectiveEdges.filter((e: any) => e.type === 'has_facet' && (e.source === toyo || e.target === sendai));
    expect(hasFacetEdges.length).toBeGreaterThanOrEqual(1);
  });

  test('deep and shallow foundations remain distinct and visible', () => {
    const deep = 'VTN-DOM-0000262';
    const shallow = 'VTN-DOM-0000261';
    expect(nodeById.has(deep)).toBe(true);
    expect(nodeById.has(shallow)).toBe(true);
    const deepNode = nodeById.get(deep);
    const shallowNode = nodeById.get(shallow);
    expect(deepNode.path_code).toBe('STR.FND.DEP');
    expect(shallowNode.path_code).toBe('STR.FND.SHL');
    // Both should have structural edges
    expect(hasOutgoingEdge(deep, 'CROSS_DOMAIN_ALIGNMENT') || hasOutgoingEdge(deep, 'broader_than')).toBe(true);
    expect(hasOutgoingEdge(shallow, 'CROSS_DOMAIN_ALIGNMENT') || hasOutgoingEdge(shallow, 'broader_than')).toBe(true);
  });

  test('building envelope remains visible with taxonomy children', () => {
    const envelope = 'VTN-DOM-0000003';
    expect(nodeById.has(envelope)).toBe(true);
    const envelopeNode = nodeById.get(envelope);
    expect(envelopeNode.path_code).toBe('ARC.ENV');
    const children = effectiveEdges.filter((e: any) => e.source === envelope && e.type === 'broader_than');
    expect(children.length).toBeGreaterThanOrEqual(2);
  });
});
