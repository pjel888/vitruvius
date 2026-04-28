export const MIN_GRAPH_LAYOUT_SPREAD = 0.75;
export const MAX_GRAPH_LAYOUT_SPREAD = 4;
export const DEFAULT_GRAPH_LAYOUT_SPREAD = 1.85;

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
