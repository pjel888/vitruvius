export const DEFAULT_EXPLORER_PANEL_WIDTH = 256;
export const DEFAULT_INSPECTOR_PANEL_WIDTH = 360;
export const MIN_SIDE_PANEL_WIDTH = 220;
export const MAX_SIDE_PANEL_WIDTH = 520;

export function clampSidePanelWidth(width: number, fallback = DEFAULT_EXPLORER_PANEL_WIDTH) {
  if (!Number.isFinite(width)) return fallback;
  return Math.min(MAX_SIDE_PANEL_WIDTH, Math.max(MIN_SIDE_PANEL_WIDTH, Math.round(width)));
}
