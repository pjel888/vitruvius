export const MIN_GRAPH_LAYOUT_SPREAD = 0.75;
export const MAX_GRAPH_LAYOUT_SPREAD = 6;
export const DEFAULT_GRAPH_LAYOUT_SPREAD = 2.65;

export function clampGraphLayoutSpread(value: number) {
  if (!Number.isFinite(value)) return DEFAULT_GRAPH_LAYOUT_SPREAD;
  return Math.min(MAX_GRAPH_LAYOUT_SPREAD, Math.max(MIN_GRAPH_LAYOUT_SPREAD, value));
}

export function getClusteredLayoutRadii(groupCount: number, spread: number) {
  const resolvedSpread = clampGraphLayoutSpread(spread);
  return {
    groupRadius: Math.max(420, groupCount * 36) * resolvedSpread,
    memberRadius: 140 * resolvedSpread,
  };
}

export function getCircularLayoutRadius(spread: number) {
  return 300 * clampGraphLayoutSpread(spread);
}

export function getRandomLayoutExtent(spread: number) {
  return 800 * clampGraphLayoutSpread(spread);
}

export interface NetworkLayoutPosition {
  id: string;
  x: number;
  y: number;
}

export function scaleNetworkLayoutPositions(positions: NetworkLayoutPosition[], previousSpread: number, nextSpread: number) {
  if (positions.length === 0) return [];
  const previous = clampGraphLayoutSpread(previousSpread);
  const next = clampGraphLayoutSpread(nextSpread);
  const ratio = next / previous;
  if (!Number.isFinite(ratio) || Math.abs(ratio - 1) < 0.001) return [];

  const center = positions.reduce(
    (acc, position) => ({ x: acc.x + position.x, y: acc.y + position.y }),
    { x: 0, y: 0 },
  );
  center.x /= positions.length;
  center.y /= positions.length;

  return positions.map((position) => ({
    id: position.id,
    x: center.x + (position.x - center.x) * ratio,
    y: center.y + (position.y - center.y) * ratio,
  }));
}
