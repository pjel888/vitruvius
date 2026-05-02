import { describe, expect, test } from 'bun:test';
import {
  buildGraphNeighborhood,
  detectCanonicalDuplicateCandidates,
  validateGraphRelationshipData,
  type GraphEdgeLike,
  type GraphNodeLike,
} from './graph/relationshipVisibility';

function buildIndex(nodes: GraphNodeLike[], edges: GraphEdgeLike[]) {
  const nodeById = new Map(nodes.map((node) => [node.id, node]));
  const edgeById = new Map(edges.map((edge) => [edge.id, edge]));
  const incomingByNodeId = new Map<string, GraphEdgeLike[]>();
  const outgoingByNodeId = new Map<string, GraphEdgeLike[]>();
  const undirectedByNodeId = new Map<string, GraphEdgeLike[]>();
  const add = (map: Map<string, GraphEdgeLike[]>, nodeId: string, edge: GraphEdgeLike) => {
    const current = map.get(nodeId);
    if (current) current.push(edge);
    else map.set(nodeId, [edge]);
  };
  edges.forEach((edge) => {
    add(outgoingByNodeId, edge.source, edge);
    add(incomingByNodeId, edge.target, edge);
    add(undirectedByNodeId, edge.source, edge);
    add(undirectedByNodeId, edge.target, edge);
  });
  return { nodeById, edgeById, incomingByNodeId, outgoingByNodeId, undirectedByNodeId };
}

describe('normalized graph relationship visibility', () => {
  const nodes: GraphNodeLike[] = [
    { id: 'building', label: 'Building', type: 'taxonomy', taxonomy_path: ['ARC'] },
    { id: 'sendai', label: 'Sendai Mediatheque', type: 'concept', taxonomy_path: ['FIG', 'FIG.WRK'] },
    { id: 'toyo', label: 'Toyo Ito', type: 'concept', taxonomy_path: ['FIG', 'FIG.ARD'] },
    { id: 'standard', label: 'Reference Standard', type: 'concept', taxonomy_path: ['COM'] },
  ];
  const edges: GraphEdgeLike[] = [
    { id: 'building--HAS_CHILD--sendai', source: 'building', target: 'sendai', type: 'HAS_CHILD', semanticOverlayCategory: 'hierarchy' },
    { id: 'toyo--HAS_FACET--sendai', source: 'toyo', target: 'sendai', type: 'HAS_FACET', semanticOverlayCategory: 'person_work' },
    { id: 'sendai--MAPS_TO_EXTERNAL_STANDARD--standard', source: 'sendai', target: 'standard', type: 'MAPS_TO_EXTERNAL_STANDARD', semanticOverlayCategory: 'external_standard' },
  ];

  test('returns all direct incoming and outgoing relationships with hydrated endpoint nodes', () => {
    const neighborhood = buildGraphNeighborhood(buildIndex(nodes, edges), 'sendai', { depth: 1 });

    expect(neighborhood.relationshipCounts.totalDirect).toBe(3);
    expect(neighborhood.relationshipCounts.visibleDirect).toBe(3);
    expect(neighborhood.relationshipCounts.semantic).toBe(2);
    expect(neighborhood.relationshipCounts.hierarchy).toBe(1);
    expect(neighborhood.nodes.map((node) => node.id).sort()).toEqual(['building', 'sendai', 'standard', 'toyo']);
    expect(neighborhood.edges.map((edge) => edge.id).sort()).toEqual([
      'building--HAS_CHILD--sendai',
      'sendai--MAPS_TO_EXTERNAL_STANDARD--standard',
      'toyo--HAS_FACET--sendai',
    ]);
    expect(neighborhood.relationships.find((relationship) => relationship.sourceNodeId === 'toyo')?.targetNode?.id).toBe('sendai');
  });

  test('reports hidden direct relationships with explicit reasons when semantic edges are filtered', () => {
    const neighborhood = buildGraphNeighborhood(buildIndex(nodes, edges), 'sendai', {
      depth: 1,
      includeSemanticEdges: false,
    });

    expect(neighborhood.relationshipCounts.visibleDirect).toBe(1);
    expect(neighborhood.relationshipCounts.hiddenDirect).toBe(2);
    expect(neighborhood.hiddenRelationships.map((relationship) => relationship.relationType).sort()).toEqual([
      'HAS_FACET',
      'MAPS_TO_EXTERNAL_STANDARD',
    ]);
    expect(neighborhood.hiddenRelationships[0].hiddenReasons).toContain('semantic_edges_disabled');
  });

  test('validates broken edge references', () => {
    const issues = validateGraphRelationshipData(nodes, [
      ...edges,
      { id: 'broken', source: 'sendai', target: 'missing', type: 'RELATED_TO' },
    ]);

    expect(issues.some((issue) => issue.code === 'missing_edge_target' && issue.edgeId === 'broken')).toBe(true);
  });

  test('detects case/plural duplicate candidates without merging unsafe concept contexts', () => {
    const duplicates = detectCanonicalDuplicateCandidates([
      { id: 'concrete-a', label: 'Concrete', type: 'concept', aliases: ['MAT.CON'], taxonomy_path: ['MAT', 'MAT.CON'] },
      { id: 'concretes-a', label: 'concretes', type: 'concept', aliases: ['MAT.CON.ALIAS'], taxonomy_path: ['MAT', 'MAT.CON'] },
      { id: 'concrete-structural', label: 'Concrete', type: 'concept', aliases: ['STR.CON'], taxonomy_path: ['STR', 'STR.CON'] },
    ]);

    const concrete = duplicates.find((candidate) => candidate.normalizedLabel === 'concrete');
    expect(concrete).toBeTruthy();
    expect(concrete?.nodeIds).toContain('concrete-a');
    expect(concrete?.nodeIds).toContain('concrete-structural');
    expect(concrete?.safeToAutoMerge).toBe(false);
  });
});
