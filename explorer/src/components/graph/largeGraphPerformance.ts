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

export function buildPhysicsOptionsForGraph(nodeCount: number, edgeCount: number, motionPaused: boolean) {
  const largeGraph = shouldUseLargeGraphRenderingGuardrails(nodeCount, edgeCount);
  return {
    enabled: !motionPaused,
    forceAtlas2Based: {
      gravitationalConstant: largeGraph ? -12 : -50,
      centralGravity: largeGraph ? 0.02 : 0.01,
      springLength: largeGraph ? 120 : 100,
      springConstant: largeGraph ? 0.04 : 0.08,
    },
    maxVelocity: largeGraph ? 12 : 50,
    minVelocity: largeGraph ? 1.5 : 0.75,
    solver: 'forceAtlas2Based',
    timestep: largeGraph ? 0.18 : 0.35,
    stabilization: {
      enabled: true,
      iterations: largeGraph ? 24 : 150,
      fit: false,
    },
  };
}
