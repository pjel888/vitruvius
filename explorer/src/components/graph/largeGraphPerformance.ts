import { DEFAULT_GRAPH_LAYOUT_SPREAD, clampGraphLayoutSpread } from './layoutSpread';

const LARGE_GRAPH_NODE_THRESHOLD = 80;
const EXPENSIVE_HOVER_HIGHLIGHT_NODE_THRESHOLD = 300;
const AUTO_FREEZE_PHYSICS_NODE_THRESHOLD = 300;

export function shouldUseLargeGraphRenderingGuardrails(nodeCount: number, edgeCount: number) {
  return nodeCount >= LARGE_GRAPH_NODE_THRESHOLD || edgeCount >= LARGE_GRAPH_NODE_THRESHOLD;
}

export function shouldSkipExpensiveHoverHighlight(nodeCount: number, edgeCount: number) {
  return nodeCount >= EXPENSIVE_HOVER_HIGHLIGHT_NODE_THRESHOLD || edgeCount >= EXPENSIVE_HOVER_HIGHLIGHT_NODE_THRESHOLD;
}

export function shouldAutoFreezePhysicsAfterStabilization(nodeCount: number, edgeCount: number) {
  return nodeCount >= AUTO_FREEZE_PHYSICS_NODE_THRESHOLD || edgeCount >= AUTO_FREEZE_PHYSICS_NODE_THRESHOLD;
}

export function getNetworkPhysicsSpreadRatio(spread: number) {
  return clampGraphLayoutSpread(spread) / DEFAULT_GRAPH_LAYOUT_SPREAD;
}

export function buildPhysicsOptionsForGraph(nodeCount: number, edgeCount: number, motionPaused: boolean, layoutSpread = DEFAULT_GRAPH_LAYOUT_SPREAD) {
  const largeGraph = shouldUseLargeGraphRenderingGuardrails(nodeCount, edgeCount);
  const spreadRatio = getNetworkPhysicsSpreadRatio(layoutSpread);
  const smallGraphSpreadRatio = Math.min(spreadRatio, 1.8);
  return {
    enabled: !motionPaused,
    forceAtlas2Based: {
      gravitationalConstant: largeGraph ? -18 * spreadRatio : -50 * smallGraphSpreadRatio,
      centralGravity: largeGraph ? 0.025 / Math.sqrt(spreadRatio) : 0.01 / Math.sqrt(smallGraphSpreadRatio),
      springLength: largeGraph ? 120 * spreadRatio : 100 * smallGraphSpreadRatio,
      springConstant: largeGraph ? 0.055 / Math.sqrt(spreadRatio) : 0.08 / Math.sqrt(smallGraphSpreadRatio),
    },
    maxVelocity: largeGraph ? 32 : 50,
    minVelocity: largeGraph ? 2.2 : 0.75,
    solver: 'forceAtlas2Based',
    timestep: largeGraph ? 0.3 : 0.35,
    stabilization: {
      enabled: true,
      iterations: largeGraph ? 16 : 150,
      fit: false,
    },
  };
}


export function shouldPreserveGraphVisibilityDuringDrag() {
  return true;
}
