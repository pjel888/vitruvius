import type { GraphEdge, GraphNode } from '../../types';

export const NORMAL_EDGE_WIDTH = 0.75;
export const EMPHASIZED_EDGE_WIDTH = 1.6;
export const PATH_EDGE_WIDTH = 1.8;
export const NODE_LABEL_FONT_SIZE = 8;
export const MIN_NODE_BODY_SIZE = 10;
export const SELECTED_NEIGHBORHOOD_ACTIVE_OPACITY = 1;
export const SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY = 0.5;
export const NORMAL_EDGE_OPACITY = 0.42;
export const DIMMED_EDGE_OPACITY = 0.18;

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
  edges.forEach((edge) => {
    if (edge.source === selectedNodeId) connected.add(edge.target);
    if (edge.target === selectedNodeId) connected.add(edge.source);
  });
  return connected;
}

export function isSelectedNeighborhoodEdge(edge: GraphEdge, neighborhoodIds: Set<string>, selectedNodeId: string | null) {
  if (!selectedNodeId) return false;
  return (
    (edge.source === selectedNodeId && neighborhoodIds.has(edge.target))
    || (edge.target === selectedNodeId && neighborhoodIds.has(edge.source))
  );
}

export function getNodeBodySize(node: GraphNode, degree = 0, metric: 'uniform' | 'confidence' | 'degree' = 'uniform') {
  const baseSize = Math.max(MIN_NODE_BODY_SIZE, node.radius ?? MIN_NODE_BODY_SIZE);
  if (metric === 'confidence' && node.confidence != null) {
    return Math.max(MIN_NODE_BODY_SIZE, Math.min(18, node.confidence * 14));
  }
  if (metric === 'degree') {
    return Math.max(MIN_NODE_BODY_SIZE, Math.min(18, baseSize + degree * 0.8));
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
