import { describe, expect, test } from 'bun:test';
import type { GraphEdge, GraphNode } from '../types';
import { buildGraphIndex, buildVisibleSubgraph, expandNeighborhood, getDirectNeighborhoodIds, resolveAlias, searchGraphIndex, tracePathInIndex } from './graphIndex';

const nodes: GraphNode[] = [
  { id: 'architecture', label: 'Architecture', type: 'taxonomy', aliases: ['ARC'], taxonomy_path: ['ARC'], radius: 14 },
  { id: 'tropical', label: 'Tropical Architecture', type: 'concept', aliases: ['ARC.TAC', 'climate responsive architecture'], taxonomy_path: ['ARC', 'ARC.TAC'], radius: 8 },
  { id: 'bamboo', label: 'Bamboo', type: 'concept', aliases: ['MAT.BAM'], taxonomy_path: ['MAT', 'MAT.BAM'], radius: 8 },
  { id: 'source-meta', label: 'Local raw-source filename metadata for TOA tropical architecture PDF', type: 'source_reference', aliases: ['planning_reference_only'], taxonomy_path: ['SRC'], radius: 6 },
];

const edges: GraphEdge[] = [
  { id: 'e1', source: 'architecture', target: 'tropical', type: 'HAS_CHILD' },
  { id: 'e2', source: 'tropical', target: 'bamboo', type: 'RELATED_TO' },
  { id: 'e3', source: 'source-meta', target: 'tropical', type: 'SOURCE_PROVENANCE' },
];

describe('graphology-backed Explorer graph index', () => {
  test('builds deterministic indexes for search, alias, adjacency, degree, and graphology nodes', () => {
    const index = buildGraphIndex(nodes, edges);

    expect(index.nodeById.size).toBe(4);
    expect(index.edgeById.size).toBe(3);
    expect(index.graph.order).toBe(4);
    expect(index.graph.size).toBe(3);
    expect(index.degreeByNodeId.get('tropical')).toBe(3);
    expect(resolveAlias(index, 'ARC.TAC')?.id).toBe('tropical');
    expect(searchGraphIndex(index, 'climate responsive')[0]).toEqual(expect.objectContaining({ id: 'tropical', matchedField: 'alias' }));
  });

  test('answers neighborhood, path, and visible-subgraph queries without changing learner-facing filters', () => {
    const index = buildGraphIndex(nodes, edges);
    const learnerEdges = edges.filter((edge) => edge.type !== 'SOURCE_PROVENANCE');
    const direct = getDirectNeighborhoodIds(index, 'tropical', learnerEdges);
    const expanded = expandNeighborhood(index, 'architecture', 2, 10);
    const path = tracePathInIndex(index, 'architecture', 'bamboo', 4);
    const visible = buildVisibleSubgraph(index, {
      rootNodeId: 'architecture',
      depth: 2,
      visibleNodeTypes: new Set(['taxonomy', 'concept']),
      visibleEdgeTypes: new Set(['HAS_CHILD', 'RELATED_TO']),
      maxNodes: 10,
      maxEdges: 10,
    });

    expect(direct.nodes).toEqual(new Set(['tropical', 'architecture', 'bamboo']));
    expect(direct.edgeIds).toEqual(new Set(['e1', 'e2']));
    expect(expanded.nodes).toEqual(['architecture', 'tropical', 'bamboo', 'source-meta']);
    expect(path?.nodes).toEqual(['architecture', 'tropical', 'bamboo']);
    expect(visible.nodes.map((node) => node.id)).not.toContain('source-meta');
    expect(visible.edges.map((edge) => edge.id)).toEqual(['e1', 'e2']);
  });

  test('keeps common operations below stable micro-latency budgets on a repeated fixture', () => {
    const repeatedNodes = Array.from({ length: 500 }, (_, index): GraphNode => ({
      id: `node-${index}`,
      label: `Node ${index}`,
      type: index % 2 === 0 ? 'concept' : 'topic',
      aliases: [`ALIAS.${index}`],
      taxonomy_path: ['ROOT', `ROOT.${index}`],
    }));
    const repeatedEdges = Array.from({ length: 499 }, (_, index): GraphEdge => ({
      id: `edge-${index}`,
      source: `node-${index}`,
      target: `node-${index + 1}`,
      type: 'RELATED_TO',
    }));
    const startedAt = performance.now();
    const index = buildGraphIndex(repeatedNodes, repeatedEdges);
    const buildMs = performance.now() - startedAt;
    const searchStartedAt = performance.now();
    const result = searchGraphIndex(index, 'ALIAS.450');
    const searchMs = performance.now() - searchStartedAt;
    const expandStartedAt = performance.now();
    const neighborhood = expandNeighborhood(index, 'node-250', 2, 20);
    const expandMs = performance.now() - expandStartedAt;

    expect(result[0]?.id).toBe('node-450');
    expect(neighborhood.nodes.length).toBeGreaterThan(1);
    expect(buildMs).toBeLessThan(120);
    expect(searchMs).toBeLessThan(15);
    expect(expandMs).toBeLessThan(15);
  });
});
