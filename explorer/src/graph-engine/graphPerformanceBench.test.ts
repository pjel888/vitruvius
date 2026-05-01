import { describe, expect, test } from 'bun:test';
import { readFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { performance } from 'node:perf_hooks';
import { buildGraphIndex, buildVisibleSubgraph, expandNeighborhood, resolveAlias, searchGraphIndex, tracePathInIndex } from './graphIndex';
import type { GraphEdge, GraphNode } from '../types';

const SHADOW_GRAPH_PATH = resolve(import.meta.dir, '../../../006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T094129Z/shadow-backbone-graph.json');
const SHADOW_STAGING_PATH = resolve(import.meta.dir, '../../../006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T094129Z/shadow-backbone-staging.json');
const BAD_LEARNER_LABEL_PATTERNS = [
  'Local raw-source filename metadata',
  'raw-source filename metadata',
  'TOA tropical architecture PDF',
  'TOA 4 (Tropical Architecture).pdf',
  'protected payload',
  'reviewer candidate',
  'unknown/private',
  'planning_reference_only',
];

interface ShadowGraphPayload {
  nodes: Array<{
    id: string;
    label: string;
    level: number;
    parent_path_code?: string | null;
    path_code: string;
  }>;
  edges: Array<{
    id: string;
    from_id: string;
    from_path_code?: string;
    predicate: string;
    to_id: string;
    to_path_code?: string;
  }>;
}

interface ShadowStagingPayload {
  backbone_nodes?: Array<{
    id: string;
    aliases?: string[];
    path_code?: string;
    review_status?: string;
  }>;
}

function loadShadowGraph() {
  const artifactBytes = statSync(SHADOW_GRAPH_PATH).size;
  const readStartedAt = performance.now();
  const raw = readFileSync(SHADOW_GRAPH_PATH, 'utf8');
  const readMs = performance.now() - readStartedAt;
  const parseStartedAt = performance.now();
  const shadowPayload = JSON.parse(raw) as ShadowGraphPayload;
  const parseMs = performance.now() - parseStartedAt;
  const staging = JSON.parse(readFileSync(SHADOW_STAGING_PATH, 'utf8')) as ShadowStagingPayload;
  const metadataById = new Map((staging.backbone_nodes ?? []).map((row) => [row.id, row]));
  const nodes = shadowPayload.nodes.map((node) => {
    const metadata = metadataById.get(node.id);
    const aliases = [
      node.path_code,
      ...(Array.isArray(metadata?.aliases) ? metadata.aliases : []),
    ]
      .map((alias) => String(alias).trim())
      .filter(Boolean);
    return {
      id: node.id,
      label: node.label,
      displayLabel: node.label,
      type: node.level <= 1 ? 'taxonomy' : node.level === 2 ? 'topic' : node.level === 3 ? 'subtopic' : 'concept',
      kind: 'backbone',
      summary: `AEC-MEPFS BackboneNode ${node.path_code || node.id} · Level ${node.level || 'unknown'}`,
      slug: node.path_code ? node.path_code.toLowerCase().replace(/[^a-z0-9]+/g, '-') : node.id,
      status: metadata?.review_status || 'steward_admitted',
      confidence: 1,
      aliases,
      taxonomy_path: node.path_code.split('.').map((_, index, parts) => parts.slice(0, index + 1).join('.')),
      radius: node.level <= 1 ? 14 : node.level === 2 ? 10 : node.level === 3 ? 9 : 8,
    } satisfies GraphNode;
  });
  const edges = shadowPayload.edges.map((edge) => ({
    id: edge.id,
    source: edge.from_id,
    target: edge.to_id,
    type: edge.predicate === 'broader_than' ? 'HAS_CHILD' : edge.predicate.toUpperCase().replace(/[^A-Z0-9]+/g, '_'),
    reasoning: `AEC-MEPFS Backbone predicate: ${edge.predicate} (${edge.from_path_code || edge.from_id} -> ${edge.to_path_code || edge.to_id})`,
    confidence: 1,
    assertionId: edge.id,
  } satisfies GraphEdge));
  return { artifactBytes, raw, payload: { nodes, edges }, shadowPayload, readMs, parseMs };
}

function percentile(values: number[], quantile: number) {
  const sorted = values.slice().sort((left, right) => left - right);
  return sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * quantile))] ?? 0;
}

function timedRepeated(iterations: number, fn: (index: number) => unknown) {
  const timings: number[] = [];
  for (let index = 0; index < iterations; index += 1) {
    const startedAt = performance.now();
    fn(index);
    timings.push(performance.now() - startedAt);
  }
  return {
    p50: percentile(timings, 0.5),
    p95: percentile(timings, 0.95),
    max: Math.max(...timings),
  };
}

describe('Explorer graph performance contract on current shadow artifact', () => {
  test('keeps graph load, index, search, alias, neighborhood, path, and visible-subgraph operations within stable budgets', () => {
    const { artifactBytes, raw, payload, readMs, parseMs } = loadShadowGraph();
    const indexStartedAt = performance.now();
    const index = buildGraphIndex(payload.nodes, payload.edges);
    const indexMs = performance.now() - indexStartedAt;

    const coldSearchTerms = [
      'tropical', 'concrete', 'architecture', 'bamboo', 'metropolitan', 'locsin', 'fire', 'water',
      'glass', 'tile', 'zaha', 'ando', 'calatrava', 'nipa', 'capiz', 'bahay', 'code', 'permit',
      'steel', 'timber', 'ventilation', 'accessibility', 'sanitation', 'structural', 'materials', 'philippine',
    ];
    const coldSearch = timedRepeated(coldSearchTerms.length, (iteration) => searchGraphIndex(index, coldSearchTerms[iteration], 20));
    const cachedSearch = timedRepeated(200, () => searchGraphIndex(index, 'Tropical Architecture', 20));
    const alias = timedRepeated(200, () => resolveAlias(index, 'ARC.TAC'));
    const oneHop = timedRepeated(200, () => expandNeighborhood(index, 'ARC.TAC', 1, 200));
    const twoHop = timedRepeated(200, () => expandNeighborhood(index, 'ARC.TAC', 2, 500));
    const path = timedRepeated(50, () => tracePathInIndex(index, 'ARC.TAC', 'MAT.TBB.BAS.BCM', 6));
    const visibleSubgraph = timedRepeated(50, () => buildVisibleSubgraph(index, { rootNodeId: 'ARC', depth: 2, maxNodes: 500, maxEdges: 800 }));

    expect(payload.nodes).toHaveLength(9880);
    expect(payload.edges).toHaveLength(13285);
    expect(artifactBytes).toBeLessThan(6_000_000);
    expect(Buffer.byteLength(raw)).toBe(artifactBytes);
    expect(readMs).toBeLessThan(50);
    expect(parseMs).toBeLessThan(50);
    expect(indexMs).toBeLessThan(250);
    expect(index.fingerprint).toMatch(/^9880:13285:/);
    expect(index.searchTokenIndex.get('tropical')?.size).toBeGreaterThan(0);
    expect(index.searchTokenIndex.get('architecture')?.size).toBeGreaterThan(0);
    const tropicalArchitecture = searchGraphIndex(index, 'Tropical Architecture', 5)[0];
    expect(tropicalArchitecture).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0002711',
      label: expect.stringContaining('Tropical Architecture'),
    }));
    expect(resolveAlias(index, 'ARC.TAC')?.id).toBe('VTN-DOM-0002711');
    expect(coldSearch.p95).toBeLessThan(30);
    expect(cachedSearch.p95).toBeLessThan(5);
    expect(alias.p95).toBeLessThan(15);
    expect(oneHop.p95).toBeLessThan(30);
    expect(twoHop.p95).toBeLessThan(75);
    expect(path.p95).toBeLessThan(75);
    expect(visibleSubgraph.p95).toBeLessThan(30);
    expect(buildVisibleSubgraph(index, { rootNodeId: 'ARC', depth: 2, maxNodes: 500, maxEdges: 800 }).nodes.length).toBeLessThanOrEqual(500);
  });

  test('keeps learner-facing performance payload clean of source/provenance labels', () => {
    const { payload, shadowPayload } = loadShadowGraph();
    const labels = payload.nodes.map((node) => node.label);

    for (const pattern of BAD_LEARNER_LABEL_PATTERNS) {
      expect(labels.some((label) => label.toLowerCase().includes(pattern.toLowerCase()))).toBe(false);
    }
    expect(payload.nodes.some((node) => node.id.startsWith('SRC-RAW'))).toBe(false);
    expect(payload.nodes.some((node) => node.label.includes('Tropical Architecture'))).toBe(true);
    expect(shadowPayload.nodes.some((node) => node.id.startsWith('SRC-RAW'))).toBe(false);
  });
});
