import type { GraphEdge, GraphNode } from '../../types';

const CHILD_EDGE_TYPES = new Set(['HAS_CHILD']);
const REVERSE_CHILD_EDGE_TYPES = new Set(['BELONGS_TO', 'PART_OF']);
const BASE_RING_RADIUS = 120;
const DEPTH_RING_RADIUS = 95;
const MIN_NODE_ARC_SPACING = 34;

export interface GraphPosition {
  x: number;
  y: number;
}

export interface ChildOrbitLayoutUpdate {
  id: string;
  x: number;
  y: number;
}

export interface ChildOrbitDescendant {
  id: string;
  depth: number;
}

function clampOrbitStrength(strength: number) {
  if (!Number.isFinite(strength)) return 0;
  return Math.min(1, Math.max(0, strength));
}

function getNodeSortKey(node: GraphNode | undefined, id: string) {
  return [node?.taxonomy_path?.join('/'), node?.type, node?.displayLabel, node?.label, id]
    .filter(Boolean)
    .join('|')
    .toLowerCase();
}

export function getChildOrbitDescendants(nodes: GraphNode[], edges: GraphEdge[], centerId: string) {
  const nodeIds = new Set(nodes.map((node) => node.id));
  const childrenByParent = new Map<string, Set<string>>();

  function addChild(parentId: string, childId: string) {
    if (!nodeIds.has(parentId) || !nodeIds.has(childId) || parentId === childId) return;
    const children = childrenByParent.get(parentId) ?? new Set<string>();
    children.add(childId);
    childrenByParent.set(parentId, children);
  }

  edges.forEach((edge) => {
    if (CHILD_EDGE_TYPES.has(edge.type)) addChild(edge.source, edge.target);
    if (REVERSE_CHILD_EDGE_TYPES.has(edge.type)) addChild(edge.target, edge.source);
  });

  const nodeMap = new Map(nodes.map((node) => [node.id, node]));
  const descendants: ChildOrbitDescendant[] = [];
  const visited = new Set([centerId]);
  let frontier = [{ id: centerId, depth: 0 }];

  while (frontier.length > 0) {
    const nextFrontier: Array<{ id: string; depth: number }> = [];
    frontier.forEach((entry) => {
      const children = [...(childrenByParent.get(entry.id) ?? [])]
        .filter((id) => !visited.has(id))
        .sort((a, b) => getNodeSortKey(nodeMap.get(a), a).localeCompare(getNodeSortKey(nodeMap.get(b), b)));
      children.forEach((id) => {
        visited.add(id);
        const child = { id, depth: entry.depth + 1 };
        descendants.push(child);
        nextFrontier.push(child);
      });
    });
    frontier = nextFrontier;
  }

  return descendants;
}

export function getChildOrbitRingRadius(nodeCount: number, depth: number) {
  const depthRadius = BASE_RING_RADIUS + Math.max(0, depth - 1) * DEPTH_RING_RADIUS;
  const spacingRadius = (Math.max(1, nodeCount) * MIN_NODE_ARC_SPACING) / (Math.PI * 2);
  return Math.max(depthRadius, spacingRadius);
}

export function buildChildOrbitLayoutUpdates(
  nodes: GraphNode[],
  edges: GraphEdge[],
  centerId: string,
  positions: Record<string, GraphPosition | undefined>,
  strength: number,
): ChildOrbitLayoutUpdate[] {
  const resolvedStrength = clampOrbitStrength(strength);
  if (resolvedStrength <= 0) return [];

  const center = positions[centerId] ?? { x: 0, y: 0 };
  const descendants = getChildOrbitDescendants(nodes, edges, centerId);
  if (descendants.length === 0) return [];

  const byDepth = new Map<number, string[]>();
  descendants.forEach((descendant) => {
    const ids = byDepth.get(descendant.depth) ?? [];
    ids.push(descendant.id);
    byDepth.set(descendant.depth, ids);
  });

  const updates: ChildOrbitLayoutUpdate[] = [];
  [...byDepth.entries()].sort(([a], [b]) => a - b).forEach(([depth, ids]) => {
    const radius = getChildOrbitRingRadius(ids.length, depth);
    ids.forEach((id, index) => {
      const angle = (-Math.PI / 2) + (index / Math.max(ids.length, 1)) * Math.PI * 2;
      const target = {
        x: center.x + Math.cos(angle) * radius,
        y: center.y + Math.sin(angle) * radius,
      };
      const current = positions[id] ?? target;
      updates.push({
        id,
        x: current.x + (target.x - current.x) * resolvedStrength,
        y: current.y + (target.y - current.y) * resolvedStrength,
      });
    });
  });

  return updates;
}
