export type GraphRenderMetricPhase =
  | 'loadGraph:start'
  | 'loadGraph:indexed'
  | 'loadGraph:layout'
  | 'loadGraph:visData'
  | 'loadGraph:dataset'
  | 'loadGraph:networkCreated'
  | 'loadGraph:updatedExisting'
  | 'loadGraph:stabilizationSkipped'
  | 'loadGraph:stabilized';

export interface GraphRenderMetricEvent {
  phase: GraphRenderMetricPhase;
  at: number;
  elapsedMs?: number;
  nodeCount?: number;
  edgeCount?: number;
  fullGraph?: boolean;
  layoutType?: string;
  layoutSource?: string;
  layoutCacheHit?: boolean;
  physicsEnabled?: boolean;
  details?: Record<string, unknown>;
}

declare global {
  interface Window {
    __vitruviusGraphRenderMetrics?: GraphRenderMetricEvent[];
  }
}

export function nowForGraphRenderMetric() {
  return typeof performance !== 'undefined' && typeof performance.now === 'function'
    ? performance.now()
    : Date.now();
}

export function recordGraphRenderMetric(event: Omit<GraphRenderMetricEvent, 'at'> & { at?: number }) {
  if (typeof window === 'undefined') return;
  const resolvedEvent: GraphRenderMetricEvent = {
    ...event,
    at: event.at ?? nowForGraphRenderMetric(),
  };
  window.__vitruviusGraphRenderMetrics = window.__vitruviusGraphRenderMetrics ?? [];
  window.__vitruviusGraphRenderMetrics.push(resolvedEvent);
}
