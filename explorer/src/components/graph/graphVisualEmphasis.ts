import type { GraphEdge, GraphNode } from '../../types';

export const NORMAL_EDGE_WIDTH = 0.28;
export const EMPHASIZED_EDGE_WIDTH = 0.68;
export const PATH_EDGE_WIDTH = 0.85;
export const EDGE_ARROW_TYPE = 'vee';
export const EDGE_ARROW_SCALE = 0.22;
export const EDGE_SMOOTH = false;
export const NODE_LABEL_FONT_SIZE = 6;
export const MIN_NODE_BODY_SIZE = 7;
export const SELECTED_NEIGHBORHOOD_ACTIVE_OPACITY = 1;
export const SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY = 0.08;
export const SELECTED_NEIGHBORHOOD_INACTIVE_SIZE_RATIO = 0.42;
export const SELECTED_NEIGHBORHOOD_INACTIVE_MIN_SIZE = 2.5;
export const NORMAL_EDGE_OPACITY = 0.32;
export const DIMMED_EDGE_OPACITY = 0.06;

const CHILD_EDGE_TYPES = new Set(['HAS_CHILD']);
const REVERSE_CHILD_EDGE_TYPES = new Set(['BELONGS_TO', 'PART_OF']);

export function getUniformArrowEdgeStyle(
  color = '#94a3b8',
  opacity = NORMAL_EDGE_OPACITY,
  width = NORMAL_EDGE_WIDTH,
) {
  return {
    color: { color, opacity },
    width,
    smooth: EDGE_SMOOTH,
    dashes: false,
    arrowStrikethrough: false,
    arrows: { to: { enabled: true, type: EDGE_ARROW_TYPE, scaleFactor: EDGE_ARROW_SCALE } },
    chosen: false,
    selectionWidth: 0,
    hoverWidth: 0,
  };
}

export function clampGraphZoomScale(scale: number) {
  if (!Number.isFinite(scale)) return 1;
  return Math.min(4, Math.max(0.08, scale));
}

export function clampUserFacingZoomScale(scale: number) {
  if (!Number.isFinite(scale)) return 1;
  return Math.min(4, Math.max(0.1, scale));
}

export function getSelectedNeighborhoodIds(edges: GraphEdge[], selectedNodeId: string | null) {
  const connected = new Set<string>();
  if (!selectedNodeId) return connected;
  connected.add(selectedNodeId);

  const childrenByParent = new Map<string, Set<string>>();
  function addChild(parentId: string, childId: string) {
    if (parentId === childId) return;
    const children = childrenByParent.get(parentId) ?? new Set<string>();
    children.add(childId);
    childrenByParent.set(parentId, children);
  }

  edges.forEach((edge) => {
    if (edge.source === selectedNodeId) connected.add(edge.target);
    if (edge.target === selectedNodeId) connected.add(edge.source);
    if (CHILD_EDGE_TYPES.has(edge.type)) addChild(edge.source, edge.target);
    if (REVERSE_CHILD_EDGE_TYPES.has(edge.type)) addChild(edge.target, edge.source);
  });

  const visitedForDescendants = new Set([selectedNodeId]);
  const frontier = [selectedNodeId];
  for (let index = 0; index < frontier.length; index += 1) {
    const parentId = frontier[index];
    (childrenByParent.get(parentId) ?? new Set()).forEach((childId) => {
      if (visitedForDescendants.has(childId)) return;
      visitedForDescendants.add(childId);
      connected.add(childId);
      frontier.push(childId);
    });
  }

  return connected;
}

export function isSelectedNeighborhoodEdge(edge: GraphEdge, neighborhoodIds: Set<string>, selectedNodeId: string | null) {
  if (!selectedNodeId) return false;
  return neighborhoodIds.has(edge.source) && neighborhoodIds.has(edge.target);
}

export function getNodeBodySize(node: GraphNode, degree = 0, metric: 'uniform' | 'confidence' | 'degree' = 'uniform') {
  const baseSize = Math.max(MIN_NODE_BODY_SIZE, node.radius ?? MIN_NODE_BODY_SIZE);
  if (metric === 'confidence' && node.confidence != null) {
    return Math.max(MIN_NODE_BODY_SIZE, Math.min(14, node.confidence * 10));
  }
  if (metric === 'degree') {
    return Math.max(MIN_NODE_BODY_SIZE, Math.min(14, baseSize + degree * 0.45));
  }
  return baseSize;
}

export function toRgba(hexColor: string, opacity: number) {
  const normalized = hexColor.replace('#', '').trim();
  if (!/^[0-9a-f]{6}$/i.test(normalized)) return hexColor;
  const value = Number.parseInt(normalized, 16);
  const red = (value >> 16) & 255;
  const green = (value >> 8) & 255;
  const blue = value & 255;
  return `rgba(${red}, ${green}, ${blue}, ${opacity})`;
}
