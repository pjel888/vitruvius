import { forwardRef, useImperativeHandle, useRef, useEffect, useState } from 'react';
import { useSceneStore, type GraphInteractionMode } from '../../stores/useSceneStore';
import type { GraphNode, GraphEdge } from '../../types';
import { getDisplayLabel } from '../../utils/labels';
import {
  buildCenteredNetworkLayoutPositions,
  clampGraphLayoutSpread,
  getCircularLayoutRadius,
  getClusteredLayoutRadii,
  getRandomLayoutExtent,
  scaleNetworkLayoutPositions,
} from './layoutSpread';
import { getNodeGraphLabel } from './nodeLabelVisibility';
import { buildPhysicsOptionsForGraph, shouldAutoFreezePhysicsAfterStabilization, shouldPreserveGraphVisibilityDuringDrag, shouldSkipExpensiveHoverHighlight, shouldUseLargeGraphRenderingGuardrails } from './largeGraphPerformance';
import { getOverviewVisibleNodes } from './overviewSnapshot';
import { buildNodeTooltip, deriveRuleDisplayLabelsFromConceptEdges } from './visNetworkDisplay';
import { buildChildOrbitLayoutUpdates } from './childOrbitLayout';
import {
  buildSettledNetworkLayoutCacheKey,
  getCachedOrBuildPrecomputedNetworkLayoutPositions,
  writeCachedNetworkLayoutPositions,
} from './precomputedNetworkLayout';
import { isGenericBackboneScaffoldNode } from './scaffoldAnchors';
import { buildGraphIndex, type GraphIndex } from '../../graph-engine/graphIndex';
import { assertFullGraphRenderContract, buildFullGraphRenderSignature } from './fullGraphRenderContract';
import { nowForGraphRenderMetric, recordGraphRenderMetric } from './graphRenderMetrics';
import {
  DIMMED_EDGE_OPACITY,
  EMPHASIZED_EDGE_WIDTH,
  MIN_NODE_BODY_SIZE,
  NODE_LABEL_FONT_SIZE,
  NORMAL_EDGE_WIDTH,
  PATH_EDGE_WIDTH,
  SELECTED_NEIGHBORHOOD_INACTIVE_MIN_SIZE,
  SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY,
  SELECTED_NEIGHBORHOOD_INACTIVE_SIZE_RATIO,
  clampGraphZoomScale,
  clampUserFacingZoomScale,
  getNodeBodySize,
  getSelectedNeighborhoodIds,
  getUniformArrowEdgeStyle,
  isSelectedNeighborhoodEdge,
  toRgba,
} from './graphVisualEmphasis';

// ---------------------------------------------------------------------------
// Dynamic vis-network import — code-splits the ~900 KB library into its own
// chunk so the main bundle stays lean.
// ---------------------------------------------------------------------------
let visModule: typeof import('vis-network/standalone') | null = null;
let visPromise: Promise<typeof import('vis-network/standalone')> | null = null;

function loadVisNetwork() {
  if (visModule) return Promise.resolve(visModule);
  if (visPromise) return visPromise;
  visPromise = import('vis-network/standalone').then((mod) => {
    visModule = mod;
    return mod;
  });
  return visPromise;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  applySceneView: (state: { camera: { x: number; y: number; ratio: number }; hiddenNodeIds: string[] }) => void;
  getSceneView: () => { camera: { x: number; y: number; ratio: number }; hiddenNodeIds: string[] };
  getOverviewSnapshot: () => {
    nodes: Array<{ id: string; x: number; y: number; type: string }>;
    camera: { x: number; y: number; ratio: number };
    viewport: { width: number; height: number };
    visibleNodeCount: number;
    version: number;
  };
  getOverviewVersion: () => number;
  centerOnPosition: (x: number, y: number) => void;
  selectNode: (id: string | null) => void;
  focusNode: (id: string) => void;
  fitView: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
  setZoomScale: (scale: number) => void;
  setLayout: (type: 'precomputed' | 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time') => void;
  setLayoutSpread: (spread: number) => void;
  arrangeChildOrbit: (centerId: string, strength: number) => void;
  setFilters: (nodeTypes: Set<string>, edgeTypes: Set<string>, showScaffoldAnchors?: boolean) => void;
  setLabelFilters: (nodeLabelTypes: Set<string>) => void;
  setColorScheme: (scheme: string) => void;
  setSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
  setMotionPaused: (paused: boolean) => void;
  hideNode: (id: string) => void;
  showAll: () => void;
  focusSubgraph: (centerId: string) => void;
  mergeNodesEdges: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  highlightPath: (nodeIds: string[], edgeIds: string[]) => void;
  clearPathHighlight: () => void;
}

type LayoutType = Parameters<GraphController['setLayout']>[0];
type InitialLayoutResult = {
  positions: Map<string, { id: string; x: number; y: number }>;
  source: string;
  cacheHit: boolean;
  staticFullGraphStartup: boolean;
};

interface VisNodeColor {
  background: string;
  border: string;
  highlight: {
    background: string;
    border: string;
  };
}

interface VisNodeItem {
  id: string;
  label: string;
  color: VisNodeColor;
  size: number;
  group: string;
  title: string;
  font?: { size: number; color: string; face?: string };
  hidden?: boolean;
  x?: number;
  y?: number;
}

interface VisEdgeItem {
  id: string;
  from: string;
  to: string;
  label: string;
  title: string;
  color: { color: string; opacity?: number };
  width?: number;
  smooth?: boolean;
  dashes?: boolean;
  arrowStrikethrough?: boolean;
  arrows?: { to: { enabled: boolean; type: string; scaleFactor: number } };
  chosen?: boolean;
  selectionWidth?: number;
  hoverWidth?: number;
  hidden?: boolean;
}

type VisNodeUpdate = Partial<VisNodeItem> & { id: string };
type VisEdgeUpdate = Partial<VisEdgeItem> & { id: string };

interface VisDataSet<T extends { id: string }, U extends { id: string } = Partial<T> & { id: string }> {
  clear: () => void;
  add: (items: T[]) => void;
  update: (items: U[] | U) => void;
}

interface VisNetworkInstance {
  destroy: () => void;
  getScale: () => number;
  getViewPosition: () => { x: number; y: number };
  getPositions: (ids: string[]) => Record<string, { x: number; y: number }>;
  moveTo: (options: {
    position: { x: number; y: number };
    scale?: number;
    animation?: false | { duration: number; easingFunction: string };
  }) => void;
  fit: (options?: { animation?: { duration: number; easingFunction: string } }) => void;
  selectNodes: (ids: string[]) => void;
  unselectAll: () => void;
  focus: (id: string, options: { scale: number; animation: { duration: number; easingFunction: string } }) => void;
  setOptions: (options: Record<string, unknown>) => void;
  getConnectedNodes: (id: string) => Array<string | number>;
  DOMtoCanvas: (point: { x: number; y: number }) => { x: number; y: number };
  getNodeAt: (point: { x: number; y: number }) => string | number | undefined;
  on: (event: string, handler: (params: unknown) => void) => void;
  startSimulation?: () => void;
}

interface ZoomEvent {
  scale?: number;
}

interface NodeEvent {
  node?: string | number;
}

interface DragEvent {
  nodes?: Array<string | number>;
}

interface ClickEvent {
  nodes?: Array<string | number>;
  edges?: Array<string | number>;
}

interface ContextEvent {
  event: { preventDefault: () => void };
  pointer: { DOM: { x: number; y: number } };
}

const COLOR_SCHEMES: Record<string, Record<string, string>> = {
  default: {
    taxonomy: '#60a5fa', topic: '#818cf8', subtopic: '#c084fc', concept: '#a78bfa',
    rule: '#f87171', definition: '#34d399', procedure: '#fbbf24', exception: '#f472b6', evidence_span: '#38bdf8', document_version: '#22d3ee',
  },
  pastel: {
    taxonomy: '#93c5fd', topic: '#a5b4fc', subtopic: '#d8b4fe', concept: '#c4b5fd',
    rule: '#fca5a5', definition: '#6ee7b7', procedure: '#fcd34d', exception: '#f9a8d4', evidence_span: '#7dd3fc', document_version: '#67e8f9',
  },
  vibrant: {
    taxonomy: '#3b82f6', topic: '#6366f1', subtopic: '#a855f7', concept: '#8b5cf6',
    rule: '#ef4444', definition: '#10b981', procedure: '#f59e0b', exception: '#ec4899', evidence_span: '#0ea5e9', document_version: '#06b6d4',
  },
  monochrome: {
    taxonomy: '#e2e8f0', topic: '#cbd5e1', subtopic: '#94a3b8', concept: '#64748b',
    rule: '#475569', definition: '#334155', procedure: '#1e293b', exception: '#0f172a', evidence_span: '#38bdf8', document_version: '#67e8f9',
  },
};

function buildClusteredLayoutUpdates(nodes: GraphNode[], spread: number): VisNodeUpdate[] {
  const groups = new Map<string, GraphNode[]>();
  nodes.forEach((node) => {
    const root = node.taxonomy_path?.[0] || 'uncategorized';
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root)!.push(node);
  });

  const groupKeys = [...groups.keys()].sort();
  const { groupRadius, memberRadius } = getClusteredLayoutRadii(groupKeys.length, spread);
  const updates: VisNodeUpdate[] = [];
  groupKeys.forEach((groupKey, groupIndex) => {
    const members = groups.get(groupKey)!;
    const centerAngle = (groupIndex / Math.max(groupKeys.length, 1)) * Math.PI * 2;
    const cx = Math.cos(centerAngle) * groupRadius;
    const cy = Math.sin(centerAngle) * groupRadius;
    members
      .slice()
      .sort((a, b) => getDisplayLabel(a).localeCompare(getDisplayLabel(b)))
      .forEach((node, memberIndex) => {
        const memberAngle = (memberIndex / Math.max(members.length, 1)) * Math.PI * 2;
        updates.push({
          id: node.id,
          x: cx + Math.cos(memberAngle) * memberRadius,
          y: cy + Math.sin(memberAngle) * memberRadius,
        });
      });
  });
  return updates;
}

function getNodeColor(schemeName: string, nodeType: string) {
  const scheme = COLOR_SCHEMES[schemeName] || COLOR_SCHEMES.default;
  return scheme[nodeType] || '#a78bfa';
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
interface VisNetworkHostProps {
  onZoomChange?: (scale: number) => void;
}

const VisNetworkHost = forwardRef<GraphController, VisNetworkHostProps>(({ onZoomChange }, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const setCamera = useSceneStore((s) => s.setCamera);
  const setHiddenNodeIds = useSceneStore((s) => s.setHiddenNodeIds);
  const graphInteractionMode = useSceneStore((s) => s.graphInteractionMode);

  const networkRef = useRef<VisNetworkInstance | null>(null);
  const nodesRef = useRef<VisDataSet<VisNodeItem, VisNodeUpdate> | null>(null);
  const edgesRef = useRef<VisDataSet<VisEdgeItem, VisEdgeUpdate> | null>(null);

  const rawNodesRef = useRef<GraphNode[]>([]);
  const rawEdgesRef = useRef<GraphEdge[]>([]);
  const graphIndexRef = useRef<GraphIndex | null>(null);
  const scaleRef = useRef(1);
  const colorSchemeRef = useRef('default');
  const activeLayoutRef = useRef<LayoutType>('forceatlas2');
  const layoutSpreadRef = useRef(2.65);
  const motionPausedRef = useRef(false);
  const sizeByRef = useRef<'uniform' | 'confidence' | 'degree'>('uniform');
  const degreeMapRef = useRef<Map<string, number>>(new Map());
  const hoveredNodeRef = useRef<string | null>(null);
  const selectedNodeIdRef = useRef<string | null>(null);
  const pathHighlightActiveRef = useRef(false);
  const lastNodeTypesRef = useRef<Set<string>>(new Set());
  const visibleNodeLabelTypesRef = useRef<Set<string>>(new Set(['taxonomy', 'topic', 'subtopic', 'concept', 'rule', 'definition', 'procedure', 'exception', 'evidence_span', 'document_version']));
  const showScaffoldAnchorsRef = useRef(false);
  const lastEdgeTypesRef = useRef<Set<string>>(new Set());
  const filtersInitializedRef = useRef(false);
  const hiddenNodeIdsRef = useRef<Set<string>>(new Set());
  const interactionModeRef = useRef<GraphInteractionMode>('select');
  const cameraSyncFrameRef = useRef<number | null>(null);
  const overviewVersionRef = useRef(0);
  const blockedDragRestoreRef = useRef<Array<{ id: string; x: number; y: number }> | null>(null);
  const childOrbitBaselineRef = useRef<{
    centerId: string;
    graphSignature: string;
    positions: Record<string, { x: number; y: number }>;
  } | null>(null);
  const lastRenderGraphSignatureRef = useRef<string | null>(null);

  function markOverviewDirty() {
    overviewVersionRef.current += 1;
  }

  function notifyZoomChange(scale = getLiveScale()) {
    onZoomChange?.(clampUserFacingZoomScale(scale));
  }

  function setGraphCursor(cursor: string) {
    if (!containerRef.current) return;
    containerRef.current.style.cursor = cursor;
    const canvas = containerRef.current.querySelector('canvas') as HTMLCanvasElement | null;
    if (canvas) canvas.style.cursor = cursor;
  }

  function getLiveScale() {
    const nextScale = networkRef.current?.getScale?.();
    if (typeof nextScale === 'number' && Number.isFinite(nextScale)) {
      scaleRef.current = nextScale;
    }
    return scaleRef.current;
  }

  function getLivePosition() {
    return networkRef.current?.getViewPosition?.() ?? { x: 0, y: 0 };
  }

  function getViewportWorldSize() {
    const scale = Math.max(getLiveScale(), 0.01);
    const rect = containerRef.current?.getBoundingClientRect();
    return {
      width: (rect?.width ?? 0) / scale,
      height: (rect?.height ?? 0) / scale,
    };
  }

  function moveToScale(scale: number, options: { animated?: boolean } = {}) {
    if (!networkRef.current) return;
    const { animated = true } = options;
    const nextScale = clampGraphZoomScale(scale);
    scaleRef.current = nextScale;
    networkRef.current.moveTo({
      position: getLivePosition(),
      scale: nextScale,
      animation: animated ? { duration: 180, easingFunction: 'easeInOutQuad' } : false,
    });
    syncCameraFromNetwork();
    markOverviewDirty();
  }

  function applyGraphInteractionMode(mode: GraphInteractionMode) {
    interactionModeRef.current = mode;
    setGraphCursor(mode === 'pan' ? 'grab' : '');

    const network = networkRef.current;
    if (!network) return;

    network.setOptions({
      interaction: {
        dragNodes: mode === 'select',
        dragView: true,
        hover: mode === 'select',
        selectable: mode === 'select',
        tooltipDelay: 200,
      },
    });

    if (mode === 'pan') {
      hoveredNodeRef.current = null;
      const store = useSceneStore.getState();
      const selectedNodeId = store.selectedNodeId;
      selectedNodeIdRef.current = selectedNodeId;
      if (selectedNodeId) network.selectNodes([selectedNodeId]);
      store.closeContextMenu();
      if (selectedNodeId) applySelectedNeighborhoodEmphasis();
      applyHover();
      return;
    }

    const selectedNodeId = useSceneStore.getState().selectedNodeId;
    selectedNodeIdRef.current = selectedNodeId;
    if (selectedNodeId) {
      network.selectNodes([selectedNodeId]);
      applySelectedNeighborhoodEmphasis();
    }
  }

  useEffect(() => {
    applyGraphInteractionMode(graphInteractionMode);
    // applyGraphInteractionMode intentionally closes over ref-backed vis-network state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graphInteractionMode]);


  // Load vis-network on mount
  useEffect(() => {
    let cancelled = false;
    loadVisNetwork()
      .then(() => {
        if (!cancelled) setReady(true);
      })
      .catch((error) => {
        if (!cancelled) {
          setLoadError(error instanceof Error ? error.message : 'Unable to load graph engine');
        }
      });
    return () => {
      cancelled = true;
      if (cameraSyncFrameRef.current !== null) cancelAnimationFrame(cameraSyncFrameRef.current);
      networkRef.current?.destroy();
      networkRef.current = null;
      nodesRef.current = null;
      edgesRef.current = null;
    };
  }, []);

  function buildVisNode(n: GraphNode) {
    const color = getNodeColor(colorSchemeRef.current, n.type);
    const displayLabel = getNodeGraphLabel(n, visibleNodeLabelTypesRef.current);
    let size = MIN_NODE_BODY_SIZE;
    if (sizeByRef.current === 'confidence' && n.confidence != null) {
      size = getNodeBodySize(n, degreeMapRef.current.get(n.id) ?? 0, 'confidence');
    } else if (sizeByRef.current === 'degree') {
      size = getNodeBodySize(n, degreeMapRef.current.get(n.id) ?? 0, 'degree');
    } else {
      size = getNodeBodySize(n);
    }
    return {
      id: n.id,
      label: displayLabel,
      color: {
        background: color,
        border: color,
        highlight: { background: color, border: '#e2e8f0' },
      },
      size,
      group: n.type,
      title: buildNodeTooltip(n),
      font: { size: NODE_LABEL_FONT_SIZE, color: '#dbeafe', face: 'system-ui, sans-serif' },
    };
  }

  function applyLayout(type: LayoutType, options: { fit?: boolean; previousSpread?: number } = {}) {
    if (!networkRef.current || !nodesRef.current) return;
    const net = networkRef.current;
    const ds = nodesRef.current;
    const nodes = rawNodesRef.current;
    const fit = options.fit ?? true;

    if (type === 'precomputed') {
      const updates = getCachedOrBuildPrecomputedNetworkLayoutPositions(
        nodes,
        rawEdgesRef.current,
        layoutSpreadRef.current,
        typeof window === 'undefined' ? undefined : window.localStorage,
      ).positions;
      if (updates.length > 0) ds.update(updates);
      net.setOptions({ physics: { enabled: false } });
      if (fit) net.fit({ animation: { duration: 350, easingFunction: 'easeInOutQuad' } });
      syncCameraFromNetwork();
      markOverviewDirty();
      return;
    }

    if (type === 'forceatlas2') {
      const previousSpread = options.previousSpread ?? layoutSpreadRef.current;
      let usingStaticFullGraphLayout = false;
      if (fit) {
        const initialLayout = buildInitialNetworkLayoutPositions(nodes, rawEdgesRef.current);
        usingStaticFullGraphLayout = initialLayout.staticFullGraphStartup;
        const updates = Array.from(initialLayout.positions.values());
        if (updates.length > 0) ds.update(updates);
      } else {
        const positions = net.getPositions(nodes.map((node) => node.id));
        const positionList = nodes
          .map((node) => {
            const position = positions[node.id];
            return position && Number.isFinite(position.x) && Number.isFinite(position.y)
              ? { id: node.id, x: position.x, y: position.y }
              : null;
          })
          .filter(Boolean) as Array<{ id: string; x: number; y: number }>;
        const updates = scaleNetworkLayoutPositions(positionList, previousSpread, layoutSpreadRef.current);
        if (updates.length > 0) ds.update(updates);
      }
      net.setOptions({ physics: buildPhysicsOptionsForGraph(nodes.length, rawEdgesRef.current.length, motionPausedRef.current || usingStaticFullGraphLayout, layoutSpreadRef.current) });
      if (!motionPausedRef.current && !usingStaticFullGraphLayout) net.startSimulation?.();
      if (fit) net.fit({ animation: { duration: 350, easingFunction: 'easeInOutQuad' } });
      syncCameraFromNetwork();
      markOverviewDirty();
      return;
    }

    net.setOptions({ physics: { enabled: false } });
    const updates: VisNodeUpdate[] = [];

    if (type === 'circular') {
      const radius = getCircularLayoutRadius(layoutSpreadRef.current);
      nodes.forEach((n, i) => {
        const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2;
        updates.push({ id: n.id, x: Math.cos(angle) * radius, y: Math.sin(angle) * radius });
      });
    } else if (type === 'random') {
      const extent = getRandomLayoutExtent(layoutSpreadRef.current);
      nodes.forEach((n) => {
        updates.push({ id: n.id, x: (Math.random() - 0.5) * extent, y: (Math.random() - 0.5) * extent });
      });
    } else if (type === 'clustered') {
      updates.push(...buildClusteredLayoutUpdates(nodes, layoutSpreadRef.current));
    } else if (type === 'time') {
      const nodesWithDate: { id: string; date: number }[] = [];
      nodes.forEach((n) => {
        if (n.createdAt) nodesWithDate.push({ id: n.id, date: new Date(n.createdAt).getTime() });
      });
      if (nodesWithDate.length > 1) {
        nodesWithDate.sort((a, b) => a.date - b.date);
        const min = nodesWithDate[0].date;
        const max = nodesWithDate[nodesWithDate.length - 1].date;
        const range = Math.max(max - min, 1);
        const dayMap = new Map<number, number>();
        nodesWithDate.forEach(({ id, date }) => {
          const x = ((date - min) / range) * 1400 - 700;
          const day = Math.floor(date / 86400000);
          const yOffset = (dayMap.get(day) || 0) * 40;
          dayMap.set(day, (dayMap.get(day) || 0) + 1);
          updates.push({ id, x, y: yOffset - 200 });
        });
      }
      let noDateY = 0;
      nodes.forEach((n) => {
        if (!n.createdAt) {
          updates.push({ id: n.id, x: 0, y: noDateY });
          noDateY += 40;
        }
      });
    }

    if (updates.length > 0) {
      ds.update(updates);
      if (fit) net.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
      syncCameraFromNetwork();
      markOverviewDirty();
    }
  }

  function applyMotionPaused(paused: boolean) {
    if (motionPausedRef.current === paused) return;
    motionPausedRef.current = paused;
    if (!networkRef.current) return;
    const enabled = activeLayoutRef.current === 'forceatlas2' && !paused;
    networkRef.current.setOptions({ physics: { enabled } });
    markOverviewDirty();
  }

  function getNetworkLayoutStorage() {
    return typeof window === 'undefined' ? undefined : window.localStorage;
  }

  function isSettledLayoutCacheEligible() {
    return activeLayoutRef.current === 'forceatlas2'
      && shouldUseLargeGraphRenderingGuardrails(rawNodesRef.current.length, rawEdgesRef.current.length);
  }

  function getSettledLayoutCacheKey() {
    if (!isSettledLayoutCacheEligible()) return null;
    return buildSettledNetworkLayoutCacheKey(
      rawNodesRef.current,
      rawEdgesRef.current,
      layoutSpreadRef.current,
      activeLayoutRef.current,
    );
  }

  function writeSettledNetworkLayoutPositions() {
    if (!networkRef.current) return;
    const cacheKey = getSettledLayoutCacheKey();
    if (!cacheKey) return;
    const nodeIds = rawNodesRef.current.map((node) => node.id);
    const positionsById = networkRef.current.getPositions(nodeIds);
    const positions = nodeIds
      .map((id) => {
        const position = positionsById[id];
        return position && Number.isFinite(position.x) && Number.isFinite(position.y)
          ? { id, x: position.x, y: position.y }
          : null;
      })
      .filter(Boolean) as Array<{ id: string; x: number; y: number }>;
    if (positions.length !== nodeIds.length) return;
    writeCachedNetworkLayoutPositions(cacheKey, positions, getNetworkLayoutStorage());
  }

  function buildInitialNetworkLayoutPositions(nodes: GraphNode[], edges: GraphEdge[]): InitialLayoutResult {
    if (activeLayoutRef.current === 'precomputed') {
      const cachedOrBuilt = getCachedOrBuildPrecomputedNetworkLayoutPositions(
        nodes,
        edges,
        layoutSpreadRef.current,
        typeof window === 'undefined' ? undefined : window.localStorage,
      );
      return {
        positions: new Map(cachedOrBuilt.positions.map((position) => [position.id, position])),
        source: 'precomputed-cache-or-build',
        cacheHit: cachedOrBuilt.cacheHit,
        staticFullGraphStartup: true,
      };
    }

    if (activeLayoutRef.current === 'forceatlas2') {
      const centered = buildCenteredNetworkLayoutPositions(
        nodes.map((node) => node.id),
        layoutSpreadRef.current,
      );
      return {
        positions: new Map(centered.map((position) => [position.id, position])),
        source: 'centered-physics-seed',
        cacheHit: false,
        staticFullGraphStartup: false,
      };
    }

    return {
      positions: new Map<string, { id: string; x: number; y: number }>(),
      source: 'layout-specific',
      cacheHit: false,
      staticFullGraphStartup: false,
    };
  }

  function arrangeChildOrbit(centerId: string, strength: number) {
    if (!networkRef.current || !nodesRef.current) return;
    const nodeIds = rawNodesRef.current.map((node) => node.id);
    const graphSignature = `${nodeIds.length}:${rawEdgesRef.current.length}`;
    if (
      childOrbitBaselineRef.current?.centerId !== centerId
      || childOrbitBaselineRef.current?.graphSignature !== graphSignature
    ) {
      childOrbitBaselineRef.current = {
        centerId,
        graphSignature,
        positions: networkRef.current.getPositions(nodeIds),
      };
    }
    const baseline = childOrbitBaselineRef.current.positions;
    const updates = buildChildOrbitLayoutUpdates(rawNodesRef.current, rawEdgesRef.current, centerId, baseline, strength);
    if (updates.length === 0) return;
    motionPausedRef.current = true;
    networkRef.current.setOptions({ physics: { enabled: false } });
    nodesRef.current.update(updates);
    applySelectedNeighborhoodEmphasis();
    syncCameraFromNetwork();
    markOverviewDirty();
  }

  function applyHover() {
    if (!nodesRef.current) return;
    if (selectedNodeIdRef.current || shouldSkipExpensiveHoverHighlight(rawNodesRef.current.length, rawEdgesRef.current.length)) {
      hoveredNodeRef.current = null;
      return;
    }
    const hovered = hoveredNodeRef.current;
    const net = networkRef.current;
    if (!hovered || !net) {
      const updates = rawNodesRef.current.map((n) => {
        const c = getNodeColor(colorSchemeRef.current, n.type);
        return {
          id: n.id,
          color: {
            background: c,
            border: c,
            highlight: { background: c, border: '#e2e8f0' },
          },
        };
      });
      nodesRef.current.update(updates);
      return;
    }
    const connected = new Set(net.getConnectedNodes(hovered).map(String));
    connected.add(hovered);
    const updates = rawNodesRef.current.map((n) => {
      const isActive = connected.has(n.id);
      const baseColor = getNodeColor(colorSchemeRef.current, n.type);
      return {
        id: n.id,
        color: {
          background: isActive ? baseColor : '#334155',
          border: isActive ? baseColor : '#475569',
          highlight: { background: baseColor, border: '#e2e8f0' },
        },
      };
    });
    nodesRef.current.update(updates);
  }

  function buildNodeColorUpdate(node: GraphNode, active = true): VisNodeUpdate {
    const color = getNodeColor(colorSchemeRef.current, node.type);
    const displayColor = active ? color : toRgba(color, SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY);
    const bodySize = getNodeBodySize(node, degreeMapRef.current.get(node.id) ?? 0, sizeByRef.current);
    return {
      id: node.id,
      size: active
        ? bodySize
        : Math.max(SELECTED_NEIGHBORHOOD_INACTIVE_MIN_SIZE, bodySize * SELECTED_NEIGHBORHOOD_INACTIVE_SIZE_RATIO),
      color: {
        background: displayColor,
        border: displayColor,
        highlight: { background: color, border: '#e2e8f0' },
      },
    };
  }

  function applyNodeColors() {
    if (!nodesRef.current) return;
    const updates = rawNodesRef.current.map((node) => buildNodeColorUpdate(node));
    nodesRef.current.update(updates);
  }

  function getVisibleNodeIdsForSelectionEmphasis() {
    const filterInitialized = filtersInitializedRef.current || lastNodeTypesRef.current.size > 0;
    return new Set(
      rawNodesRef.current
        .filter((node) => !filterInitialized || lastNodeTypesRef.current.has(node.type))
        .filter((node) => showScaffoldAnchorsRef.current || !isGenericBackboneScaffoldNode(node))
        .filter((node) => !hiddenNodeIdsRef.current.has(node.id))
        .map((node) => node.id)
    );
  }

  function getVisibleEdgesForSelectionEmphasis(selectedNodeId?: string | null) {
    const visibleNodeIds = getVisibleNodeIdsForSelectionEmphasis();
    const filterInitialized = filtersInitializedRef.current || lastEdgeTypesRef.current.size > 0;
    const candidateEdges = selectedNodeId && graphIndexRef.current
      ? graphIndexRef.current.undirectedByNodeId.get(selectedNodeId) || []
      : rawEdgesRef.current;
    return candidateEdges.filter((edge) => (
      (!filterInitialized || lastEdgeTypesRef.current.has(edge.type))
      && visibleNodeIds.has(edge.source)
      && visibleNodeIds.has(edge.target)
    ));
  }

  function applyNodeLabels() {
    if (!nodesRef.current) return;
    const selectedNodeId = selectedNodeIdRef.current;
    const selectedNeighborhood = getSelectedNeighborhoodIds(getVisibleEdgesForSelectionEmphasis(selectedNodeId), selectedNodeId);
    const updates = rawNodesRef.current.map((node) => ({
      id: node.id,
      label: selectedNodeId
        ? (selectedNeighborhood.has(node.id) ? getDisplayLabel(node) : '')
        : getNodeGraphLabel(node, visibleNodeLabelTypesRef.current),
    }));
    nodesRef.current.update(updates);
    markOverviewDirty();
  }

  function applyEdgeColors() {
    if (!edgesRef.current) return;
    const updates = rawEdgesRef.current.map((edge) => ({
      id: edge.id,
      ...getUniformArrowEdgeStyle(),
    }));
    edgesRef.current.update(updates);
  }

  function applySelectedNeighborhoodEmphasis() {
    if (!nodesRef.current || !edgesRef.current) return;
    const selectedNodeId = selectedNodeIdRef.current;
    const neighborhood = getSelectedNeighborhoodIds(getVisibleEdgesForSelectionEmphasis(selectedNodeId), selectedNodeId);
    if (!selectedNodeId) {
      applyNodeColors();
      applyNodeLabels();
      applyEdgeColors();
      markOverviewDirty();
      return;
    }

    nodesRef.current.update(rawNodesRef.current.map((node) => ({
      ...buildNodeColorUpdate(node, neighborhood.has(node.id)),
      label: neighborhood.has(node.id) ? getDisplayLabel(node) : '',
    })));

    edgesRef.current.update(rawEdgesRef.current.map((edge) => {
      const active = isSelectedNeighborhoodEdge(edge, neighborhood, selectedNodeId);
      return {
        id: edge.id,
        ...getUniformArrowEdgeStyle(
          active ? '#cbd5e1' : '#64748b',
          active ? 1 : DIMMED_EDGE_OPACITY,
          active ? EMPHASIZED_EDGE_WIDTH : NORMAL_EDGE_WIDTH,
        ),
      };
    }));
    markOverviewDirty();
  }

  function applyFilters(nodeTypes: Set<string>, edgeTypes: Set<string>, showScaffoldAnchors = showScaffoldAnchorsRef.current) {
    if (!nodesRef.current || !edgesRef.current || !networkRef.current) return;

    const visibleNodeIds = new Set(
      rawNodesRef.current
        .filter((n) => nodeTypes.has(n.type))
        .filter((n) => showScaffoldAnchors || !isGenericBackboneScaffoldNode(n))
        .map((n) => n.id)
    );

    const nodeUpdates = rawNodesRef.current.map((n) => ({
      id: n.id,
      hidden: !visibleNodeIds.has(n.id) || hiddenNodeIdsRef.current.has(n.id),
    }));
    nodesRef.current.update(nodeUpdates);

    const edgeUpdates = rawEdgesRef.current.map((e) => ({
      id: e.id,
      hidden: !(edgeTypes.has(e.type) && visibleNodeIds.has(e.source) && visibleNodeIds.has(e.target))
        || hiddenNodeIdsRef.current.has(e.source)
        || hiddenNodeIdsRef.current.has(e.target),
    }));
    edgesRef.current.update(edgeUpdates);

    applyHover();
    applySelectedNeighborhoodEmphasis();
    markOverviewDirty();
  }

  function syncCameraFromNetwork() {
    if (!networkRef.current) return;
    if (cameraSyncFrameRef.current !== null) return;
    cameraSyncFrameRef.current = requestAnimationFrame(() => {
      cameraSyncFrameRef.current = null;
      if (!networkRef.current) return;
      const position = getLivePosition();
      const scale = getLiveScale();
      setCamera({ x: position.x, y: position.y, ratio: scale });
      notifyZoomChange(scale);
      markOverviewDirty();
    });
  }

  function loadGraph(nodes: GraphNode[], edges: GraphEdge[]) {
    const loadStartedAt = nowForGraphRenderMetric();
    recordGraphRenderMetric({
      phase: 'loadGraph:start',
      nodeCount: nodes.length,
      edgeCount: edges.length,
      fullGraph: true,
      layoutType: activeLayoutRef.current,
    });
    const nodeMap = new Map<string, GraphNode>();
    nodes.forEach((n) => {
      if (!nodeMap.has(n.id)) nodeMap.set(n.id, n);
    });
    const uniqueNodes = Array.from(nodeMap.values());

    const edgeMap = new Map<string, GraphEdge>();
    edges.forEach((e) => {
      const key = e.id || `${e.source}-${e.type}-${e.target}`;
      if (!edgeMap.has(key)) edgeMap.set(key, e);
    });
    const uniqueEdges = Array.from(edgeMap.values());
    const renderGraphSignature = buildFullGraphRenderSignature(uniqueNodes, uniqueEdges);
    const fullGraphContractHeld = assertFullGraphRenderContract(
      uniqueNodes.length,
      uniqueEdges.length,
      uniqueNodes.length,
      uniqueEdges.length,
    );

    if (
      ready
      && containerRef.current
      && visModule
      && networkRef.current
      && nodesRef.current
      && edgesRef.current
      && lastRenderGraphSignatureRef.current === renderGraphSignature
    ) {
      recordGraphRenderMetric({
        phase: 'loadGraph:updatedExisting',
        elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
        nodeCount: uniqueNodes.length,
        edgeCount: uniqueEdges.length,
        fullGraph: fullGraphContractHeld,
        layoutType: activeLayoutRef.current,
        details: { skippedFullDatasetReplacement: true },
      });
      applyGraphInteractionMode(interactionModeRef.current);
      syncCameraFromNetwork();
      markOverviewDirty();
      return;
    }

    rawEdgesRef.current = uniqueEdges;
    const displayNodes = deriveRuleDisplayLabelsFromConceptEdges(uniqueNodes, uniqueEdges);
    rawNodesRef.current = displayNodes;
    graphIndexRef.current = buildGraphIndex(displayNodes, uniqueEdges);
    lastRenderGraphSignatureRef.current = renderGraphSignature;
    markOverviewDirty();
    recordGraphRenderMetric({
      phase: 'loadGraph:indexed',
      elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
      nodeCount: displayNodes.length,
      edgeCount: uniqueEdges.length,
      fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, displayNodes.length, uniqueEdges.length),
      layoutType: activeLayoutRef.current,
    });

    if (!ready || !containerRef.current || !visModule) {
      return;
    }

    const { Network, DataSet } = visModule;

    hiddenNodeIdsRef.current.clear();

    const degMap = new Map<string, number>();
    displayNodes.forEach((n) => degMap.set(n.id, 0));
    uniqueEdges.forEach((e) => {
      degMap.set(e.source, (degMap.get(e.source) ?? 0) + 1);
      degMap.set(e.target, (degMap.get(e.target) ?? 0) + 1);
    });
    degreeMapRef.current = degMap;

    const largeGraph = shouldUseLargeGraphRenderingGuardrails(displayNodes.length, uniqueEdges.length);
    const initialLayout = buildInitialNetworkLayoutPositions(displayNodes, uniqueEdges);
    const initialNetworkPositions = initialLayout.positions;
    recordGraphRenderMetric({
      phase: 'loadGraph:layout',
      elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
      nodeCount: displayNodes.length,
      edgeCount: uniqueEdges.length,
      fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, displayNodes.length, uniqueEdges.length),
      layoutType: activeLayoutRef.current,
      layoutSource: initialLayout.source,
      layoutCacheHit: initialLayout.cacheHit,
    });
    const visNodes = displayNodes.map((node) => ({
      ...buildVisNode(node),
      ...initialNetworkPositions.get(node.id),
    }));
    const physicsOptions = buildPhysicsOptionsForGraph(
      displayNodes.length,
      uniqueEdges.length,
      motionPausedRef.current
        || activeLayoutRef.current === 'precomputed'
        || initialLayout.staticFullGraphStartup,
      layoutSpreadRef.current,
    );

    const visEdges = uniqueEdges.map((e) => ({
      id: e.id,
      from: e.source,
      to: e.target,
      label: '',
      title: e.type,
      ...getUniformArrowEdgeStyle(),
    }));
    recordGraphRenderMetric({
      phase: 'loadGraph:visData',
      elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
      nodeCount: visNodes.length,
      edgeCount: visEdges.length,
      fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, visNodes.length, visEdges.length),
      layoutType: activeLayoutRef.current,
      layoutSource: initialLayout.source,
      layoutCacheHit: initialLayout.cacheHit,
      physicsEnabled: Boolean(physicsOptions.enabled),
    });

    if (networkRef.current && nodesRef.current && edgesRef.current) {
      nodesRef.current.clear();
      nodesRef.current.add(visNodes);
      edgesRef.current.clear();
      edgesRef.current.add(visEdges);
      recordGraphRenderMetric({
        phase: 'loadGraph:updatedExisting',
        elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
        nodeCount: visNodes.length,
        edgeCount: visEdges.length,
        fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, visNodes.length, visEdges.length),
        layoutType: activeLayoutRef.current,
        layoutSource: initialLayout.source,
        layoutCacheHit: initialLayout.cacheHit,
        physicsEnabled: Boolean(physicsOptions.enabled),
      });
      if (lastNodeTypesRef.current.size > 0 || lastEdgeTypesRef.current.size > 0) {
        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
      }
      applyLayout(activeLayoutRef.current, { fit: true });
      applyGraphInteractionMode(interactionModeRef.current);
      syncCameraFromNetwork();
      markOverviewDirty();
      return;
    }

    nodesRef.current = new DataSet(visNodes) as VisDataSet<VisNodeItem, VisNodeUpdate>;
    edgesRef.current = new DataSet(visEdges) as VisDataSet<VisEdgeItem, VisEdgeUpdate>;
    recordGraphRenderMetric({
      phase: 'loadGraph:dataset',
      elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
      nodeCount: visNodes.length,
      edgeCount: visEdges.length,
      fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, visNodes.length, visEdges.length),
      layoutType: activeLayoutRef.current,
      layoutSource: initialLayout.source,
      layoutCacheHit: initialLayout.cacheHit,
      physicsEnabled: Boolean(physicsOptions.enabled),
    });

    const networkData = {
      nodes: nodesRef.current,
      edges: edgesRef.current,
    } as unknown as ConstructorParameters<typeof Network>[1];

    networkRef.current = new Network(
      containerRef.current,
      networkData,
      {
        nodes: {
          shape: 'dot',
          font: { size: NODE_LABEL_FONT_SIZE, color: '#dbeafe', face: 'system-ui, sans-serif' },
          borderWidth: 1,
          borderWidthSelected: 2,
          shadow: largeGraph ? false : { enabled: true, color: 'rgba(0,0,0,0.3)', size: 8 },
        },
        edges: {
          ...getUniformArrowEdgeStyle(),
          font: { size: 5, color: '#7a7f8a', strokeWidth: 0, face: 'system-ui, sans-serif' },
        },
        physics: {
          ...physicsOptions,
        },
        layout: {
          improvedLayout: !largeGraph,
        },
        interaction: {
          dragNodes: interactionModeRef.current === 'select',
          dragView: true,
          hover: true,
          selectable: interactionModeRef.current === 'select',
          tooltipDelay: 200,
          hideEdgesOnDrag: !shouldPreserveGraphVisibilityDuringDrag(),
          hideNodesOnDrag: false,
        },
      }
    ) as unknown as VisNetworkInstance;
    recordGraphRenderMetric({
      phase: 'loadGraph:networkCreated',
      elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
      nodeCount: visNodes.length,
      edgeCount: visEdges.length,
      fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, visNodes.length, visEdges.length),
      layoutType: activeLayoutRef.current,
      layoutSource: initialLayout.source,
      layoutCacheHit: initialLayout.cacheHit,
      physicsEnabled: Boolean(physicsOptions.enabled),
    });
    if (!physicsOptions.enabled) {
      recordGraphRenderMetric({
        phase: 'loadGraph:stabilizationSkipped',
        elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
        nodeCount: visNodes.length,
        edgeCount: visEdges.length,
        fullGraph: assertFullGraphRenderContract(uniqueNodes.length, uniqueEdges.length, visNodes.length, visEdges.length),
        layoutType: activeLayoutRef.current,
        layoutSource: initialLayout.source,
        layoutCacheHit: initialLayout.cacheHit,
        physicsEnabled: false,
        details: {
          reason: initialLayout.staticFullGraphStartup
            ? 'static-full-graph-startup-layout'
            : 'motion-paused-or-precomputed-layout',
        },
      });
    }

    networkRef.current.on('zoom', (params) => {
      const event = params as ZoomEvent;
      if (typeof event.scale === 'number') scaleRef.current = clampGraphZoomScale(event.scale);
      notifyZoomChange(scaleRef.current);
      syncCameraFromNetwork();
    });

    networkRef.current.on('dragEnd', () => {
      if (blockedDragRestoreRef.current && nodesRef.current) {
        nodesRef.current.update(blockedDragRestoreRef.current);
        blockedDragRestoreRef.current = null;
      }
      setGraphCursor(interactionModeRef.current === 'pan' ? 'grab' : '');
      syncCameraFromNetwork();
    });

    networkRef.current.on('dragStart', (params) => {
      const event = params as DragEvent;
      const draggedNodeIds = (event.nodes ?? []).map(String);
      if (interactionModeRef.current === 'pan') {
        setGraphCursor('grabbing');
        return;
      }
      const selectedNodeId = selectedNodeIdRef.current;
      if (!selectedNodeId || draggedNodeIds.length === 0 || !networkRef.current) return;
      const movableNeighborhood = getSelectedNeighborhoodIds(getVisibleEdgesForSelectionEmphasis(selectedNodeId), selectedNodeId);
      const outsideSelection = draggedNodeIds.some((nodeId) => !movableNeighborhood.has(nodeId));
      if (!outsideSelection) return;
      const positions = networkRef.current.getPositions(draggedNodeIds);
      blockedDragRestoreRef.current = draggedNodeIds
        .map((id) => {
          const position = positions[id];
          return position ? { id, x: position.x, y: position.y } : null;
        })
        .filter(Boolean) as Array<{ id: string; x: number; y: number }>;
      nodesRef.current?.update(blockedDragRestoreRef.current);
      networkRef.current.setOptions({ interaction: { dragNodes: false } });
      window.requestAnimationFrame(() => {
        networkRef.current?.setOptions({ interaction: { dragNodes: interactionModeRef.current === 'select' } });
      });
      const store = useSceneStore.getState();
      selectedNodeIdRef.current = null;
      networkRef.current.unselectAll();
      store.setSelectedNode(null);
      store.setSelectedEdge(null);
      applySelectedNeighborhoodEmphasis();
    });

    networkRef.current.on('animationFinished', () => {
      syncCameraFromNetwork();
      markOverviewDirty();
    });

    networkRef.current.on('stabilized', () => {
      writeSettledNetworkLayoutPositions();
      recordGraphRenderMetric({
        phase: 'loadGraph:stabilized',
        elapsedMs: nowForGraphRenderMetric() - loadStartedAt,
        nodeCount: rawNodesRef.current.length,
        edgeCount: rawEdgesRef.current.length,
        fullGraph: true,
        layoutType: activeLayoutRef.current,
      });
      if (
        shouldAutoFreezePhysicsAfterStabilization(rawNodesRef.current.length, rawEdgesRef.current.length)
        && activeLayoutRef.current === 'forceatlas2'
      ) {
        networkRef.current?.setOptions({ physics: { enabled: false } });
      }
      syncCameraFromNetwork();
      markOverviewDirty();
    });

    networkRef.current.on('hoverNode', (params) => {
      const event = params as NodeEvent;
      hoveredNodeRef.current = event.node == null ? null : String(event.node);
      applyHover();
    });

    networkRef.current.on('blurNode', () => {
      hoveredNodeRef.current = null;
      applyHover();
    });

    networkRef.current.on('click', (params) => {
      const event = params as ClickEvent;
      const store = useSceneStore.getState();
      store.closeContextMenu();
      if (interactionModeRef.current === 'pan') {
        return;
      }
      if (event.nodes && event.nodes.length > 0) {
        const clickedNodeId = String(event.nodes[0]);
        const selectedNodeId = selectedNodeIdRef.current;
        if (selectedNodeId && clickedNodeId !== selectedNodeId) {
          const selectedNeighborhood = getSelectedNeighborhoodIds(getVisibleEdgesForSelectionEmphasis(selectedNodeId), selectedNodeId);
          if (!selectedNeighborhood.has(clickedNodeId)) {
            selectedNodeIdRef.current = null;
            networkRef.current?.unselectAll();
            store.setSelectedNode(null);
            store.setSelectedEdge(null);
            applySelectedNeighborhoodEmphasis();
            return;
          }
        }
        store.setSelectedNode(clickedNodeId);
        store.openInspector();
      } else if (event.edges && event.edges.length > 0) {
        store.setSelectedNode(null);
        store.setSelectedEdge(String(event.edges[0]));
        store.openInspector();
      } else {
        store.setSelectedNode(null);
        store.setSelectedEdge(null);
      }
    });

    networkRef.current.on('oncontext', (params) => {
      const event = params as ContextEvent;
      event.event.preventDefault();
      if (interactionModeRef.current === 'pan') {
        useSceneStore.getState().closeContextMenu();
        return;
      }
      if (!networkRef.current) return;
      const canvasPos = networkRef.current.DOMtoCanvas(event.pointer.DOM);
      const nodeId = networkRef.current.getNodeAt(canvasPos);
      const store = useSceneStore.getState();
      if (nodeId) {
        store.openContextMenu(String(nodeId), {
          x: event.pointer.DOM.x + (containerRef.current?.getBoundingClientRect().left ?? 0),
          y: event.pointer.DOM.y + (containerRef.current?.getBoundingClientRect().top ?? 0),
        });
      } else {
        store.closeContextMenu();
      }
    });

    if (lastNodeTypesRef.current.size > 0 || lastEdgeTypesRef.current.size > 0) {
      applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
    }
    if (activeLayoutRef.current === 'forceatlas2' || activeLayoutRef.current === 'precomputed') {
      networkRef.current.fit({ animation: { duration: 350, easingFunction: 'easeInOutQuad' } });
      syncCameraFromNetwork();
      markOverviewDirty();
    } else {
      applyLayout(activeLayoutRef.current, { fit: true });
    }
    applyGraphInteractionMode(interactionModeRef.current);
    syncCameraFromNetwork();
  }

  useEffect(() => {
    if (!ready || networkRef.current || rawNodesRef.current.length === 0) return;
    loadGraph(rawNodesRef.current, rawEdgesRef.current);
    // loadGraph reads ref-backed vis-network state; ready is the only React trigger needed here.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready]);

  useImperativeHandle(
    ref,
    () => ({
      loadPerspective(nodes, edges) {
        loadGraph(nodes, edges);
      },

      applySceneView(state) {
        hiddenNodeIdsRef.current = new Set(state.hiddenNodeIds);
        setHiddenNodeIds(state.hiddenNodeIds);
        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
        if (networkRef.current) {
          scaleRef.current = state.camera.ratio;
          networkRef.current.moveTo({
            position: { x: state.camera.x, y: state.camera.y },
            scale: state.camera.ratio,
            animation: false,
          });
          syncCameraFromNetwork();
        }
      },

      getSceneView() {
        syncCameraFromNetwork();
        const position = getLivePosition();
        return {
          camera: { x: position.x, y: position.y, ratio: getLiveScale() },
          hiddenNodeIds: Array.from(hiddenNodeIdsRef.current),
        };
      },

      getOverviewSnapshot() {
        const overviewNodes = getOverviewVisibleNodes(
          rawNodesRef.current,
          hiddenNodeIdsRef.current,
          lastNodeTypesRef.current,
          filtersInitializedRef.current,
        ).filter((node) => showScaffoldAnchorsRef.current || !isGenericBackboneScaffoldNode(node));
        const positions = networkRef.current?.getPositions?.(overviewNodes.map((node) => node.id)) || {};
        return {
          nodes: overviewNodes
            .map((node) => {
              const position = positions[node.id];
              if (!position) return null;
              return { id: node.id, x: position.x, y: position.y, type: node.type };
            })
            .filter(Boolean) as Array<{ id: string; x: number; y: number; type: string }>,
          camera: { ...getLivePosition(), ratio: getLiveScale() },
          viewport: getViewportWorldSize(),
          visibleNodeCount: overviewNodes.length,
          version: overviewVersionRef.current,
        };
      },

      getOverviewVersion() {
        return overviewVersionRef.current;
      },

      centerOnPosition(x, y) {
        if (!networkRef.current) return;
        networkRef.current.moveTo({
          position: { x, y },
          scale: getLiveScale(),
          animation: { duration: 250, easingFunction: 'easeInOutQuad' },
        });
        syncCameraFromNetwork();
        markOverviewDirty();
      },

      selectNode(id) {
        selectedNodeIdRef.current = id;
        if (id && networkRef.current) {
          networkRef.current.selectNodes([id]);
        } else if (networkRef.current) {
          networkRef.current.unselectAll();
        }
        applySelectedNeighborhoodEmphasis();
      },

      focusNode(id) {
        if (!networkRef.current) return;
        networkRef.current.selectNodes([id]);
        networkRef.current.focus(id, {
          scale: Math.min(getLiveScale(), 0.85),
          animation: { duration: 500, easingFunction: 'easeInOutQuad' },
        });
        selectedNodeIdRef.current = id;
        applySelectedNeighborhoodEmphasis();
        markOverviewDirty();
      },

      fitView() {
        const selectedNodeId = selectedNodeIdRef.current;
        if (selectedNodeId && networkRef.current) {
          networkRef.current.focus(selectedNodeId, {
            scale: 1.1,
            animation: { duration: 500, easingFunction: 'easeInOutQuad' },
          });
        } else {
          networkRef.current?.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
        }
        syncCameraFromNetwork();
        markOverviewDirty();
      },

      zoomIn() {
        moveToScale(getLiveScale() * 1.22);
      },

      zoomOut() {
        moveToScale(getLiveScale() / 1.22);
      },

      setZoomScale(scale) {
        moveToScale(scale, { animated: false });
      },

      setLayout(type) {
        if (activeLayoutRef.current === type) return;
        activeLayoutRef.current = type;
        applyLayout(type, { fit: true });
      },

      setLayoutSpread(spread) {
        const previousSpread = layoutSpreadRef.current;
        const nextSpread = clampGraphLayoutSpread(spread);
        if (nextSpread === previousSpread) return;
        layoutSpreadRef.current = nextSpread;
        applyLayout(activeLayoutRef.current, { fit: false, previousSpread });
      },

      arrangeChildOrbit(centerId, strength) {
        arrangeChildOrbit(centerId, strength);
      },

      setFilters(nodeTypes, edgeTypes, showScaffoldAnchors = showScaffoldAnchorsRef.current) {
        lastNodeTypesRef.current = nodeTypes;
        lastEdgeTypesRef.current = edgeTypes;
        showScaffoldAnchorsRef.current = showScaffoldAnchors;
        filtersInitializedRef.current = true;
        applyFilters(nodeTypes, edgeTypes, showScaffoldAnchors);
      },

      setLabelFilters(nodeLabelTypes) {
        if (
          nodeLabelTypes.size === visibleNodeLabelTypesRef.current.size
          && [...nodeLabelTypes].every((nodeType) => visibleNodeLabelTypesRef.current.has(nodeType))
        ) {
          return;
        }
        visibleNodeLabelTypesRef.current = nodeLabelTypes;
        applyNodeLabels();
        markOverviewDirty();
      },

      setColorScheme(scheme) {
        if (colorSchemeRef.current === scheme) return;
        colorSchemeRef.current = scheme;
        applyNodeColors();
        applySelectedNeighborhoodEmphasis();
      },

      setSizeBy(metric) {
        if (sizeByRef.current === metric) return;
        sizeByRef.current = metric;
        if (!nodesRef.current) return;
        const updates = rawNodesRef.current.map((n) => {
          return { id: n.id, size: getNodeBodySize(n, degreeMapRef.current.get(n.id) ?? 0, metric) };
        });
        nodesRef.current.update(updates);
        applySelectedNeighborhoodEmphasis();
      },

      setMotionPaused(paused) {
        applyMotionPaused(paused);
      },

      hideNode(id) {
        hiddenNodeIdsRef.current.add(id);
        setHiddenNodeIds(Array.from(hiddenNodeIdsRef.current));
        if (!nodesRef.current || !edgesRef.current) return;
        nodesRef.current.update({ id, hidden: true });
        const edgeUpdates = rawEdgesRef.current
          .filter((e) => e.source === id || e.target === id)
          .map((e) => ({ id: e.id, hidden: true }));
        if (edgeUpdates.length) edgesRef.current.update(edgeUpdates);
        markOverviewDirty();
      },

      showAll() {
        hiddenNodeIdsRef.current.clear();
        setHiddenNodeIds([]);
        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
        markOverviewDirty();
      },

      focusSubgraph(centerId) {
        if (!networkRef.current || !nodesRef.current || !edgesRef.current) return;
        const connected = new Set(networkRef.current.getConnectedNodes(centerId).map(String));
        connected.add(centerId);
        const nodeUpdates = rawNodesRef.current.map((n) => ({
          id: n.id,
          hidden: !connected.has(n.id),
        }));
        hiddenNodeIdsRef.current = new Set(rawNodesRef.current.filter((n) => !connected.has(n.id)).map((n) => n.id));
        setHiddenNodeIds(Array.from(hiddenNodeIdsRef.current));
        nodesRef.current.update(nodeUpdates);
        const edgeUpdates = rawEdgesRef.current.map((e) => ({
          id: e.id,
          hidden: !(connected.has(e.source) && connected.has(e.target)),
        }));
        edgesRef.current.update(edgeUpdates);
        markOverviewDirty();
      },

      mergeNodesEdges(newNodes, newEdges) {
        if (!nodesRef.current || !edgesRef.current || !networkRef.current) return;

        const existingNodeIds = new Set(rawNodesRef.current.map((n) => n.id));
        const existingEdgeIds = new Set(rawEdgesRef.current.map((e) => e.id));
        const nodesToAdd = newNodes.filter((n) => !existingNodeIds.has(n.id));
        const edgesToAdd = newEdges.filter((e) => !existingEdgeIds.has(e.id));

        if (!nodesToAdd.length && !edgesToAdd.length) return;

        rawNodesRef.current = [...rawNodesRef.current, ...nodesToAdd];
        rawEdgesRef.current = [...rawEdgesRef.current, ...edgesToAdd];
        graphIndexRef.current = buildGraphIndex(rawNodesRef.current, rawEdgesRef.current);

        edgesToAdd.forEach((e) => {
          degreeMapRef.current.set(e.source, (degreeMapRef.current.get(e.source) ?? 0) + 1);
          degreeMapRef.current.set(e.target, (degreeMapRef.current.get(e.target) ?? 0) + 1);
        });

        const visNodes = nodesToAdd.map(buildVisNode);
        const visEdges = edgesToAdd.map((e) => ({
          id: e.id,
          from: e.source,
          to: e.target,
          label: '',
          title: e.type,
          ...getUniformArrowEdgeStyle(),
        }));

        nodesRef.current.update(visNodes);
        edgesRef.current.update(visEdges);

        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);

        const sizeUpdates = nodesToAdd.map((n) => {
          return { id: n.id, size: getNodeBodySize(n, degreeMapRef.current.get(n.id) ?? 0, sizeByRef.current) };
        });
        nodesRef.current.update(sizeUpdates);
        applySelectedNeighborhoodEmphasis();
        applyHover();
      },

      highlightPath(nodeIds, edgeIds) {
        if (!nodesRef.current || !edgesRef.current) return;
        pathHighlightActiveRef.current = true;
        const pathNodeSet = new Set(nodeIds);
        const pathEdgeSet = new Set(edgeIds);

        const nodeUpdates = rawNodesRef.current.map((n) => {
          const isPath = pathNodeSet.has(n.id);
          return {
            id: n.id,
            color: {
              background: isPath ? '#fbbf24' : getNodeColor(colorSchemeRef.current, n.type),
              border: isPath ? '#f59e0b' : getNodeColor(colorSchemeRef.current, n.type),
              highlight: { background: '#fbbf24', border: '#e2e8f0' },
            },
          };
        });
        nodesRef.current.update(nodeUpdates);

        const edgeUpdates = rawEdgesRef.current.map((e) => ({
          id: e.id,
          ...getUniformArrowEdgeStyle(
            pathEdgeSet.has(e.id) ? '#fbbf24' : '#334155',
            pathEdgeSet.has(e.id) ? 1 : 0.2,
            pathEdgeSet.has(e.id) ? PATH_EDGE_WIDTH : NORMAL_EDGE_WIDTH,
          ),
        }));
        edgesRef.current.update(edgeUpdates);
        markOverviewDirty();
      },

      clearPathHighlight() {
        if (!pathHighlightActiveRef.current && !selectedNodeIdRef.current) return;
        pathHighlightActiveRef.current = false;
        applySelectedNeighborhoodEmphasis();
        applyHover();
      },
    }),
    // GraphController methods intentionally close over ref-backed vis-network state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [ready]
  );

  // While vis-network is loading, show a subtle loading indicator
  if (loadError) {
    return (
      <div className="absolute inset-0 flex items-center justify-center px-6">
        <div className="max-w-md rounded-lg border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-100 shadow-lg">
          Unable to load graph engine: {loadError}
        </div>
      </div>
    );
  }

  if (!ready) {
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
          <span className="text-sm text-text-dim">Loading graph engine...</span>
        </div>
      </div>
    );
  }

  return (
    <>
      <div
        ref={containerRef}
        style={{
          position: 'absolute',
          inset: 0,
        }}
      />
    </>
  );
});

VisNetworkHost.displayName = 'VisNetworkHost';
export default VisNetworkHost;
