import Graph from 'graphology';
import type { GraphEdge, GraphNode, SearchResult } from '../types';
import { getDisplayLabel } from '../utils/labels';

export interface GraphIndex {
  fingerprint: string;
  graph: Graph;
  nodeById: Map<string, GraphNode>;
  edgeById: Map<string, GraphEdge>;
  outgoingByNodeId: Map<string, GraphEdge[]>;
  incomingByNodeId: Map<string, GraphEdge[]>;
  undirectedByNodeId: Map<string, GraphEdge[]>;
  nodeTypeIndex: Map<string, Set<string>>;
  edgeTypeIndex: Map<string, Set<string>>;
  aliasIndex: Map<string, Set<string>>;
  labelIndex: Map<string, Set<string>>;
  degreeByNodeId: Map<string, number>;
  searchFields: SearchField[];
  searchCache: Map<string, SearchResult[]>;
  neighborhoodCache: Map<string, { nodes: string[]; edges: string[] }>;
}

interface SearchField {
  node: GraphNode;
  field: string;
  text: string;
  normalized: string;
}

export interface VisibleSubgraphOptions {
  rootNodeId?: string | null;
  depth?: number;
  maxNodes?: number;
  maxEdges?: number;
  visibleNodeTypes?: Set<string>;
  visibleEdgeTypes?: Set<string>;
  hiddenNodeIds?: Set<string>;
}

function normalize(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, ' ');
}

function addToSetIndex(index: Map<string, Set<string>>, key: string, value: string) {
  if (!key) return;
  const existing = index.get(key);
  if (existing) existing.add(value);
  else index.set(key, new Set([value]));
}

function addEdgeToIndex(index: Map<string, GraphEdge[]>, nodeId: string, edge: GraphEdge) {
  const existing = index.get(nodeId);
  if (existing) existing.push(edge);
  else index.set(nodeId, [edge]);
}

function addFingerprintPart(hash: number, value: unknown) {
  const text = String(value ?? '');
  let nextHash = hash;
  for (let index = 0; index < text.length; index += 1) {
    nextHash ^= text.charCodeAt(index);
    nextHash = Math.imul(nextHash, 16777619);
  }
  return nextHash >>> 0;
}

export function buildGraphFingerprint(nodes: GraphNode[], edges: GraphEdge[]) {
  let hash = 2166136261;
  hash = addFingerprintPart(hash, nodes.length);
  hash = addFingerprintPart(hash, edges.length);
  for (const node of nodes) {
    hash = addFingerprintPart(hash, node.id);
    hash = addFingerprintPart(hash, node.type);
    hash = addFingerprintPart(hash, node.label);
    hash = addFingerprintPart(hash, Array.isArray(node.aliases) ? node.aliases.join('\u001f') : '');
  }
  for (const edge of edges) {
    hash = addFingerprintPart(hash, edge.id);
    hash = addFingerprintPart(hash, edge.source);
    hash = addFingerprintPart(hash, edge.target);
    hash = addFingerprintPart(hash, edge.type);
  }
  return `${nodes.length}:${edges.length}:${hash.toString(36)}`;
}

export function buildGraphIndex(nodes: GraphNode[], edges: GraphEdge[]): GraphIndex {
  const graph = new Graph({ multi: true, type: 'directed', allowSelfLoops: true });
  const nodeById = new Map<string, GraphNode>();
  const edgeById = new Map<string, GraphEdge>();
  const outgoingByNodeId = new Map<string, GraphEdge[]>();
  const incomingByNodeId = new Map<string, GraphEdge[]>();
  const undirectedByNodeId = new Map<string, GraphEdge[]>();
  const nodeTypeIndex = new Map<string, Set<string>>();
  const edgeTypeIndex = new Map<string, Set<string>>();
  const aliasIndex = new Map<string, Set<string>>();
  const labelIndex = new Map<string, Set<string>>();
  const degreeByNodeId = new Map<string, number>();
  const searchFields: SearchField[] = [];

  for (const node of nodes) {
    if (nodeById.has(node.id)) continue;
    nodeById.set(node.id, node);
    graph.addNode(node.id, node);
    degreeByNodeId.set(node.id, 0);
    addToSetIndex(nodeTypeIndex, node.type, node.id);
    const displayLabel = getDisplayLabel(node);
    const aliases = Array.isArray(node.aliases) ? node.aliases : [];
    const fields = [
      { field: 'label', text: node.label },
      { field: 'displayLabel', text: displayLabel },
      { field: 'id', text: node.id },
      ...aliases.map((text, index) => ({ field: index === 0 ? 'pathCode' : 'alias', text })),
    ];
    for (const field of fields) {
      const normalized = normalize(field.text || '');
      if (!normalized) continue;
      searchFields.push({ node, field: field.field, text: field.text, normalized });
      if (field.field === 'alias' || field.field === 'pathCode') addToSetIndex(aliasIndex, normalized, node.id);
      if (field.field === 'label' || field.field === 'displayLabel') addToSetIndex(labelIndex, normalized, node.id);
    }
  }

  for (const edge of edges) {
    if (edgeById.has(edge.id)) continue;
    edgeById.set(edge.id, edge);
    addToSetIndex(edgeTypeIndex, edge.type, edge.id);
    addEdgeToIndex(outgoingByNodeId, edge.source, edge);
    addEdgeToIndex(incomingByNodeId, edge.target, edge);
    addEdgeToIndex(undirectedByNodeId, edge.source, edge);
    addEdgeToIndex(undirectedByNodeId, edge.target, edge);
    degreeByNodeId.set(edge.source, (degreeByNodeId.get(edge.source) ?? 0) + 1);
    degreeByNodeId.set(edge.target, (degreeByNodeId.get(edge.target) ?? 0) + 1);
    if (nodeById.has(edge.source) && nodeById.has(edge.target)) {
      graph.addDirectedEdgeWithKey(edge.id, edge.source, edge.target, edge);
    }
  }

  return {
    fingerprint: buildGraphFingerprint(nodes, edges),
    graph,
    nodeById,
    edgeById,
    outgoingByNodeId,
    incomingByNodeId,
    undirectedByNodeId,
    nodeTypeIndex,
    edgeTypeIndex,
    aliasIndex,
    labelIndex,
    degreeByNodeId,
    searchFields,
    searchCache: new Map(),
    neighborhoodCache: new Map(),
  };
}

function searchRank(candidate: string, query: string) {
  if (!candidate) return null;
  if (candidate === query) return 100;
  if (candidate.startsWith(query)) return 80;
  if (candidate.includes(query)) return 60;
  return null;
}

export function searchGraphIndex(index: GraphIndex, query: string, limit = 20): SearchResult[] {
  const normalizedQuery = normalize(query);
  if (!normalizedQuery || normalizedQuery.length < 2) return [];
  const boundedLimit = Math.min(Math.max(Math.floor(limit), 1), 100);
  const cacheKey = `${normalizedQuery}:${boundedLimit}`;
  const cached = index.searchCache.get(cacheKey);
  if (cached) return cached;

  const bestByNodeId = new Map<string, { node: GraphNode; field: string; text: string; rank: number }>();
  for (const field of index.searchFields) {
    const rank = searchRank(field.normalized, normalizedQuery);
    if (rank === null) continue;
    const current = bestByNodeId.get(field.node.id);
    if (!current || rank > current.rank || (rank === current.rank && field.field.localeCompare(current.field) < 0)) {
      bestByNodeId.set(field.node.id, { node: field.node, field: field.field, text: field.text, rank });
    }
  }

  const results = Array.from(bestByNodeId.values())
    .sort((left, right) => right.rank - left.rank || getDisplayLabel(left.node).localeCompare(getDisplayLabel(right.node)) || left.node.id.localeCompare(right.node.id))
    .slice(0, boundedLimit)
    .map((match) => ({
      kind: 'node' as const,
      id: match.node.id,
      label: match.node.label,
      displayLabel: match.node.displayLabel,
      type: match.node.type,
      matchType: match.field,
      matchedField: match.field,
    }));
  index.searchCache.set(cacheKey, results);
  return results;
}

export function resolveAlias(index: GraphIndex, alias: string): GraphNode | null {
  const ids = index.aliasIndex.get(normalize(alias));
  const id = ids?.values().next().value;
  return id ? index.nodeById.get(id) ?? null : null;
}

export function getDirectNeighborhoodIds(index: GraphIndex, nodeId: string, visibleEdges?: GraphEdge[]) {
  const nodes = new Set<string>();
  const edgeIds = new Set<string>();
  nodes.add(nodeId);
  const candidateEdges = visibleEdges ?? index.undirectedByNodeId.get(nodeId) ?? [];
  for (const edge of candidateEdges) {
    if (edge.source !== nodeId && edge.target !== nodeId) continue;
    nodes.add(edge.source);
    nodes.add(edge.target);
    edgeIds.add(edge.id);
  }
  return { nodes, edgeIds };
}

export function expandNeighborhood(index: GraphIndex, nodeId: string, depth = 1, maxEdges = 200) {
  const boundedDepth = Math.min(Math.max(Math.floor(depth) || 1, 1), 6);
  const boundedEdges = Math.min(Math.max(Math.floor(maxEdges) || 1, 1), 500);
  const cacheKey = `${nodeId}:${boundedDepth}:${boundedEdges}`;
  const cached = index.neighborhoodCache.get(cacheKey);
  if (cached) return cached;
  const nodes = new Set<string>([nodeId]);
  const edges = new Set<string>();
  let frontier = [nodeId];
  for (let currentDepth = 0; currentDepth < boundedDepth && frontier.length > 0 && edges.size < boundedEdges; currentDepth += 1) {
    const nextFrontier: string[] = [];
    for (const currentNodeId of frontier) {
      for (const edge of index.undirectedByNodeId.get(currentNodeId) ?? []) {
        if (edges.size >= boundedEdges) break;
        if (edges.has(edge.id)) continue;
        edges.add(edge.id);
        const nextNodeId = edge.source === currentNodeId ? edge.target : edge.source;
        if (!nodes.has(nextNodeId)) {
          nodes.add(nextNodeId);
          nextFrontier.push(nextNodeId);
        }
      }
    }
    frontier = nextFrontier;
  }
  const result = { nodes: Array.from(nodes), edges: Array.from(edges) };
  index.neighborhoodCache.set(cacheKey, result);
  return result;
}

export function tracePathInIndex(index: GraphIndex, from: string, to: string, maxHops = 6) {
  if (!index.nodeById.has(from) || !index.nodeById.has(to)) return null;
  const queue: Array<{ nodeId: string; nodes: string[]; edges: string[] }> = [{ nodeId: from, nodes: [from], edges: [] }];
  const visited = new Set<string>([from]);
  while (queue.length) {
    const current = queue.shift()!;
    if (current.nodeId === to) return current;
    if (current.edges.length >= maxHops) continue;
    for (const edge of index.undirectedByNodeId.get(current.nodeId) ?? []) {
      const nextNodeId = edge.source === current.nodeId ? edge.target : edge.source;
      if (visited.has(nextNodeId)) continue;
      visited.add(nextNodeId);
      queue.push({ nodeId: nextNodeId, nodes: [...current.nodes, nextNodeId], edges: [...current.edges, edge.id] });
    }
  }
  return null;
}

export function buildVisibleSubgraph(index: GraphIndex, options: VisibleSubgraphOptions = {}) {
  const visibleNodeTypes = options.visibleNodeTypes;
  const visibleEdgeTypes = options.visibleEdgeTypes;
  const hiddenNodeIds = options.hiddenNodeIds ?? new Set<string>();
  const maxNodes = Math.max(1, options.maxNodes ?? 500);
  const maxEdges = Math.max(1, options.maxEdges ?? 800);
  const seed = options.rootNodeId && index.nodeById.has(options.rootNodeId)
    ? expandNeighborhood(index, options.rootNodeId, options.depth ?? 1, maxEdges).nodes
    : Array.from(index.nodeById.keys());
  const nodeIds = seed
    .filter((id) => !hiddenNodeIds.has(id))
    .filter((id) => {
      const node = index.nodeById.get(id);
      return node && (!visibleNodeTypes || visibleNodeTypes.has(node.type));
    })
    .slice(0, maxNodes);
  const nodeIdSet = new Set(nodeIds);
  const edgeIds: string[] = [];
  for (const edge of index.edgeById.values()) {
    if (edgeIds.length >= maxEdges) break;
    if (visibleEdgeTypes && !visibleEdgeTypes.has(edge.type)) continue;
    if (nodeIdSet.has(edge.source) && nodeIdSet.has(edge.target) && !hiddenNodeIds.has(edge.source) && !hiddenNodeIds.has(edge.target)) {
      edgeIds.push(edge.id);
    }
  }
  return {
    nodes: nodeIds.map((id) => index.nodeById.get(id)).filter((node): node is GraphNode => Boolean(node)),
    edges: edgeIds.map((id) => index.edgeById.get(id)).filter((edge): edge is GraphEdge => Boolean(edge)),
  };
}
