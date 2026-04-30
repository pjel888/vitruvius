import type { GraphEdge, GraphNode } from '../../types';
import { DEFAULT_GRAPH_LAYOUT_SPREAD, clampGraphLayoutSpread, type NetworkLayoutPosition } from './layoutSpread';
import { shouldUseLargeGraphRenderingGuardrails } from './largeGraphPerformance';

const CACHE_VERSION = 'precomputed-network-layout-v1';
const SETTLED_CACHE_VERSION = 'settled-network-layout-v1';
const CACHE_PREFIX = 'vitruvius:explorer:network-layout:';
const TYPE_LEVELS: Record<string, number> = {
  taxonomy: 0,
  topic: 1,
  subtopic: 2,
  concept: 3,
  rule: 4,
  definition: 4,
  procedure: 4,
  exception: 4,
  evidence_span: 5,
  document_version: 5,
};

export interface NetworkLayoutStorage {
  getItem: (key: string) => string | null;
  setItem: (key: string, value: string) => void;
}

interface CachedPositionsPayload {
  version: string;
  positions: NetworkLayoutPosition[];
}

const memoryLayoutCache = new Map<string, NetworkLayoutPosition[]>();

function stableHash(input: string) {
  let hash = 2166136261;
  for (let index = 0; index < input.length; index += 1) {
    hash ^= input.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(36);
}

function nodeSortKey(node: GraphNode) {
  return [node.taxonomy_path?.join('/'), node.type, node.displayLabel ?? node.label, node.id]
    .filter(Boolean)
    .join('|');
}

function getNodeRoot(node: GraphNode) {
  return node.taxonomy_path?.[0] || (node.type === 'taxonomy' ? node.id : 'uncategorized');
}

function getNodeLevel(node: GraphNode) {
  if (node.taxonomy_path && node.taxonomy_path.length > 0) {
    return Math.max(0, node.taxonomy_path.length - 1);
  }
  return TYPE_LEVELS[node.type] ?? 3;
}

function getStorageKey(cacheKey: string) {
  return `${CACHE_PREFIX}${cacheKey}`;
}

function clonePositions(positions: NetworkLayoutPosition[]) {
  return positions.map((position) => ({ ...position }));
}

export function shouldUsePrecomputedNetworkLayout(nodeCount: number, edgeCount: number, layoutType: string) {
  return layoutType === 'precomputed' && shouldUseLargeGraphRenderingGuardrails(nodeCount, edgeCount);
}

export function buildPrecomputedNetworkLayoutCacheKey(nodes: GraphNode[], edges: GraphEdge[], spread: number) {
  const roundedSpread = clampGraphLayoutSpread(spread).toFixed(2);
  const nodeSignature = nodes
    .map((node) => `${node.id}:${node.type}:${node.taxonomy_path?.join('/') ?? ''}`)
    .sort()
    .join(';');
  const edgeSignature = edges
    .map((edge) => `${edge.source}>${edge.type}>${edge.target}`)
    .sort()
    .join(';');

  return `${CACHE_VERSION}:${roundedSpread}:${nodes.length}:${edges.length}:${stableHash(`${nodeSignature}|${edgeSignature}`)}`;
}

export function buildSettledNetworkLayoutCacheKey(
  nodes: GraphNode[],
  edges: GraphEdge[],
  spread: number,
  layoutType: string,
) {
  return `${SETTLED_CACHE_VERSION}:${layoutType}:${buildPrecomputedNetworkLayoutCacheKey(nodes, edges, spread)}`;
}

export function readCachedNetworkLayoutPositions(
  cacheKey: string,
  expectedNodeIds: string[],
  storage?: NetworkLayoutStorage,
) {
  const expectedIds = new Set(expectedNodeIds);
  const memoryHit = memoryLayoutCache.get(cacheKey);
  if (memoryHit && memoryHit.length === expectedIds.size && memoryHit.every((position) => expectedIds.has(position.id))) {
    return clonePositions(memoryHit);
  }

  if (!storage) return null;

  try {
    const raw = storage.getItem(getStorageKey(cacheKey));
    if (!raw) return null;
    const payload = JSON.parse(raw) as CachedPositionsPayload;
    if (payload.version !== CACHE_VERSION) return null;
    if (!Array.isArray(payload.positions) || payload.positions.length !== expectedIds.size) return null;
    if (!payload.positions.every((position) => expectedIds.has(position.id))) return null;
    memoryLayoutCache.set(cacheKey, clonePositions(payload.positions));
    return clonePositions(payload.positions);
  } catch {
    return null;
  }
}

export function writeCachedNetworkLayoutPositions(
  cacheKey: string,
  positions: NetworkLayoutPosition[],
  storage?: NetworkLayoutStorage,
) {
  const cloned = clonePositions(positions);
  memoryLayoutCache.set(cacheKey, cloned);
  if (!storage) return;
  try {
    storage.setItem(getStorageKey(cacheKey), JSON.stringify({ version: CACHE_VERSION, positions: cloned }));
  } catch {
    // Cache writes are a performance hint only; quota/private-mode failures must not block rendering.
  }
}

export function buildPrecomputedNetworkLayoutPositions(
  nodes: GraphNode[],
  edges: GraphEdge[],
  spread = DEFAULT_GRAPH_LAYOUT_SPREAD,
): NetworkLayoutPosition[] {
  if (nodes.length === 0) return [];

  const resolvedSpread = clampGraphLayoutSpread(spread);
  const spreadRatio = resolvedSpread / DEFAULT_GRAPH_LAYOUT_SPREAD;
  const sortedNodes = nodes.slice().sort((a, b) => nodeSortKey(a).localeCompare(nodeSortKey(b)));
  const roots = Array.from(new Set(sortedNodes.map(getNodeRoot))).sort((a, b) => a.localeCompare(b));
  const rootIndex = new Map(roots.map((root, index) => [root, index]));
  const rootCount = Math.max(roots.length, 1);
  const sectorAngle = (Math.PI * 2) / rootCount;
  const sectorPadding = Math.min(0.11, sectorAngle * 0.18);
  const usableSector = Math.max(sectorAngle - sectorPadding * 2, sectorAngle * 0.62);
  const ringSpacing = Math.max(720, Math.sqrt(nodes.length) * 12) * spreadRatio;
  const laneSpacing = ringSpacing * 0.42;
  const desiredArcSpacing = 82 * spreadRatio;
  const buckets = new Map<string, GraphNode[]>();

  sortedNodes.forEach((node) => {
    const root = getNodeRoot(node);
    const level = getNodeLevel(node);
    const key = `${root}\u0000${level}`;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key)!.push(node);
  });

  const positioned = new Map<string, NetworkLayoutPosition>();

  roots.forEach((root) => {
    const taxonomyNode = sortedNodes.find((node) => getNodeRoot(node) === root && getNodeLevel(node) === 0);
    if (!taxonomyNode) return;
    const index = rootIndex.get(root) ?? 0;
    const angle = index * sectorAngle;
    positioned.set(taxonomyNode.id, {
      id: taxonomyNode.id,
      x: Math.cos(angle) * ringSpacing * 0.45,
      y: Math.sin(angle) * ringSpacing * 0.45,
    });
  });

  Array.from(buckets.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([key, bucketNodes]) => {
      const [root, levelText] = key.split('\u0000');
      const level = Number(levelText);
      if (level === 0) return;
      const rootPosition = rootIndex.get(root) ?? 0;
      const sectorStart = rootPosition * sectorAngle - sectorAngle / 2 + sectorPadding;
      const baseRadius = ringSpacing * (level + 0.9);
      const capacity = Math.max(1, Math.floor((usableSector * baseRadius) / desiredArcSpacing));

      bucketNodes.forEach((node, index) => {
        const lane = Math.floor(index / capacity);
        const laneIndex = index % capacity;
        const laneStart = lane * capacity;
        const laneCount = Math.min(capacity, bucketNodes.length - laneStart);
        const angle = sectorStart + ((laneIndex + 0.5) / Math.max(laneCount, 1)) * usableSector;
        const radius = baseRadius + lane * laneSpacing;
        positioned.set(node.id, {
          id: node.id,
          x: Math.cos(angle) * radius,
          y: Math.sin(angle) * radius,
        });
      });
    });

  // Some merged/query nodes may lack taxonomy metadata. Place them in a wide
  // deterministic outer ring instead of falling back to a compact seed.
  const unpositioned = sortedNodes.filter((node) => !positioned.has(node.id));
  const fallbackRadius = ringSpacing * (Math.max(...sortedNodes.map(getNodeLevel), 1) + 2.4);
  unpositioned.forEach((node, index) => {
    const angle = (index / Math.max(unpositioned.length, 1)) * Math.PI * 2;
    positioned.set(node.id, {
      id: node.id,
      x: Math.cos(angle) * fallbackRadius,
      y: Math.sin(angle) * fallbackRadius,
    });
  });

  // Edges are included in the cache key so structural changes invalidate cached
  // output. The layout itself intentionally stays tree/ring deterministic so it
  // can render immediately without a force-solver warmup.
  void edges;

  return nodes.map((node) => positioned.get(node.id) ?? { id: node.id, x: 0, y: 0 });
}

export function getCachedOrBuildPrecomputedNetworkLayoutPositions(
  nodes: GraphNode[],
  edges: GraphEdge[],
  spread: number,
  storage?: NetworkLayoutStorage,
) {
  const cacheKey = buildPrecomputedNetworkLayoutCacheKey(nodes, edges, spread);
  const nodeIds = nodes.map((node) => node.id);
  const cached = readCachedNetworkLayoutPositions(cacheKey, nodeIds, storage);
  if (cached) return { cacheKey, positions: cached, cacheHit: true };
  const positions = buildPrecomputedNetworkLayoutPositions(nodes, edges, spread);
  writeCachedNetworkLayoutPositions(cacheKey, positions, storage);
  return { cacheKey, positions, cacheHit: false };
}
