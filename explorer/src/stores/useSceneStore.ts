import { create } from 'zustand';
import type { CameraState, GraphNode, GraphEdge, SceneState } from '../types';
import { DEFAULT_EXPLORER_PERSPECTIVE_ID } from '../constants/perspectives';
import { DEFAULT_EXPLORER_PANEL_WIDTH, DEFAULT_INSPECTOR_PANEL_WIDTH, clampSidePanelWidth } from '../utils/resizablePanels';
import { DEFAULT_GRAPH_LAYOUT_SPREAD, clampGraphLayoutSpread } from '../components/graph/layoutSpread';

type LayoutType = 'precomputed' | 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time';
export type GraphInteractionMode = 'select' | 'pan';

interface ChildOrbitRequest {
  nodeId: string;
  strength: number;
  requestId: number;
}

interface BottomTableColumn {
  key: string;
  label: string;
}

interface BottomTableRow {
  id: string;
  values: Record<string, string>;
  deepLink?: string;
}

type BottomContent =
  | {
      type: 'source';
      title: string;
      documentId?: string;
      quote?: string;
      deepLink?: string;
    }
  | {
      type: 'table';
      title: string;
      columns: BottomTableColumn[];
      rows: BottomTableRow[];
    }
  | {
      type: 'query';
      title: string;
      query: string;
      resultSummary?: string;
      columns?: BottomTableColumn[];
      rows?: BottomTableRow[];
    };

interface SceneStore {
  // View state
  perspectiveId: string;
  activeSceneId: string | null;
  activeSceneName: string | null;
  setPerspectiveId: (id: string) => void;
  setActiveScene: (id: string | null, name?: string | null) => void;
  applySceneState: (scene: SceneState) => void;

  // Selection
  selectedNodeId: string | null;
  selectedEdgeId: string | null;
  pendingSelectedNodeId: string | null;
  pinnedNodeIds: string[];
  setSelectedNode: (id: string | null) => void;
  setSelectedEdge: (id: string | null) => void;
  setPendingSelectedNode: (id: string | null) => void;
  togglePinnedNode: (id: string) => void;

  // Graph data
  nodes: GraphNode[];
  edges: GraphEdge[];
  setGraphData: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  mergeGraphData: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  preloadedPerspectiveId: string | null;
  markPreloadedPerspective: (id: string | null) => void;

  // UI state
  explorerOpen: boolean;
  inspectorOpen: boolean;
  toggleExplorer: () => void;
  toggleInspector: () => void;
  openInspector: () => void;
  closeInspector: () => void;
  explorerPanelWidth: number;
  inspectorPanelWidth: number;
  setExplorerPanelWidth: (width: number) => void;
  setInspectorPanelWidth: (width: number) => void;
  graphInteractionMode: GraphInteractionMode;
  setGraphInteractionMode: (mode: GraphInteractionMode) => void;

  // Bottom drawer
  bottomOpen: boolean;
  bottomContent: BottomContent | null;
  openBottom: (content: BottomContent) => void;
  closeBottom: () => void;

  // Search
  searchQuery: string;
  setSearchQuery: (q: string) => void;

  // Context menu
  contextMenuNodeId: string | null;
  contextMenuPos: { x: number; y: number } | null;
  openContextMenu: (nodeId: string, pos: { x: number; y: number }) => void;
  closeContextMenu: () => void;

  // Path tracing
  pathSourceId: string | null;
  pathTargetId: string | null;
  highlightedPath: { nodeIds: string[]; edgeIds: string[] } | null;
  focusSubgraphNodeId: string | null;
  focusedNodeId: string | null;
  showAllRequestId: number;
  setPathSource: (id: string | null) => void;
  setPathTarget: (id: string | null) => void;
  setHighlightedPath: (path: { nodeIds: string[]; edgeIds: string[] } | null) => void;
  requestFocusSubgraph: (id: string) => void;
  clearFocusSubgraphRequest: () => void;
  requestFocusNode: (id: string) => void;
  clearFocusNodeRequest: () => void;
  requestShowAll: () => void;
  childOrbitRequest: ChildOrbitRequest | null;
  requestChildOrbit: (nodeId: string, strength: number) => void;
  clearPath: () => void;

  // Camera (for Sigma)
  camera: CameraState;
  setCamera: (c: CameraState) => void;

  // Loading
  loading: boolean;
  loadError: string | null;
  setLoading: (v: boolean) => void;
  setLoadError: (message: string | null) => void;

  // Filters
  visibleNodeTypes: Set<string>;
  visibleEdgeTypes: Set<string>;
  visibleNodeLabelTypes: Set<string>;
  showScaffoldAnchors: boolean;
  hiddenNodeIds: string[];
  expandedNodeIds: string[];
  setVisibleNodeTypes: (types: Set<string>) => void;
  setVisibleEdgeTypes: (types: Set<string>) => void;
  setVisibleNodeLabelTypes: (types: Set<string>) => void;
  setShowScaffoldAnchors: (show: boolean) => void;
  setHiddenNodeIds: (ids: string[]) => void;
  setExpandedNodeIds: (ids: string[]) => void;
  addExpandedNodeIds: (ids: string[]) => void;

  // Visual settings
  layout: LayoutType;
  setLayout: (layout: LayoutType) => void;
  layoutSpread: number;
  setLayoutSpread: (spread: number) => void;
  colorScheme: string;
  setColorScheme: (scheme: string) => void;
  sizeBy: 'uniform' | 'confidence' | 'degree';
  setSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
}

export const useSceneStore = create<SceneStore>((set) => ({
  perspectiveId: DEFAULT_EXPLORER_PERSPECTIVE_ID,
  activeSceneId: null,
  activeSceneName: null,
  setPerspectiveId: (id) => set({
    perspectiveId: id,
    activeSceneId: null,
    activeSceneName: null,
    selectedNodeId: null,
    selectedEdgeId: null,
  }),
  setActiveScene: (id, name = null) => set({ activeSceneId: id, activeSceneName: name }),
  applySceneState: (scene) => set({
    activeSceneId: scene.id,
    activeSceneName: scene.name,
    perspectiveId: scene.perspectiveId,
    selectedNodeId: scene.selectedNodeIds[0] ?? null,
    selectedEdgeId: scene.selectedEdgeIds[0] ?? null,
    pinnedNodeIds: scene.pinnedNodeIds,
    searchQuery: scene.filters.searchQuery,
    visibleNodeTypes: new Set(scene.filters.nodeTypes),
    visibleEdgeTypes: new Set(scene.filters.edgeTypes),
    showScaffoldAnchors: false,
    hiddenNodeIds: scene.hiddenNodeIds,
    expandedNodeIds: scene.expandedNodeIds,
    camera: scene.camera,
    layout: scene.layout,
    colorScheme: scene.colorScheme,
    sizeBy: scene.sizeBy,
    pathSourceId: null,
    pathTargetId: null,
    highlightedPath: null,
    focusSubgraphNodeId: null,
    focusedNodeId: null,
    showAllRequestId: 0,
    childOrbitRequest: null,
  }),

  selectedNodeId: null,
  selectedEdgeId: null,
  pendingSelectedNodeId: null,
  pinnedNodeIds: [],
  setSelectedNode: (id) => set({ selectedNodeId: id, selectedEdgeId: null }),
  setSelectedEdge: (id) => set({ selectedEdgeId: id, selectedNodeId: null }),
  setPendingSelectedNode: (id) => set({ pendingSelectedNodeId: id }),
  togglePinnedNode: (id) => set((state) => ({
    pinnedNodeIds: state.pinnedNodeIds.includes(id)
      ? state.pinnedNodeIds.filter((nodeId) => nodeId !== id)
      : [...state.pinnedNodeIds, id],
  })),

  nodes: [],
  edges: [],
  preloadedPerspectiveId: null,
  setGraphData: (nodes, edges) => set({ nodes, edges }),
  mergeGraphData: (nodes, edges) => set((state) => {
    const nodeMap = new Map(state.nodes.map((node) => [node.id, node]));
    nodes.forEach((node) => {
      if (!nodeMap.has(node.id)) nodeMap.set(node.id, node);
    });
    const edgeMap = new Map(state.edges.map((edge) => [edge.id, edge]));
    edges.forEach((edge) => {
      if (!edgeMap.has(edge.id)) edgeMap.set(edge.id, edge);
    });
    return {
      nodes: Array.from(nodeMap.values()),
      edges: Array.from(edgeMap.values()),
    };
  }),
  markPreloadedPerspective: (id) => set({ preloadedPerspectiveId: id }),

  explorerOpen: true,
  inspectorOpen: false,
  toggleExplorer: () => set(s => ({ explorerOpen: !s.explorerOpen })),
  toggleInspector: () => set(s => ({ inspectorOpen: !s.inspectorOpen })),
  openInspector: () => set({ inspectorOpen: true }),
  closeInspector: () => set({ inspectorOpen: false }),
  explorerPanelWidth: DEFAULT_EXPLORER_PANEL_WIDTH,
  inspectorPanelWidth: DEFAULT_INSPECTOR_PANEL_WIDTH,
  setExplorerPanelWidth: (width) => set({ explorerPanelWidth: clampSidePanelWidth(width, DEFAULT_EXPLORER_PANEL_WIDTH) }),
  setInspectorPanelWidth: (width) => set({ inspectorPanelWidth: clampSidePanelWidth(width, DEFAULT_INSPECTOR_PANEL_WIDTH) }),
  graphInteractionMode: 'select',
  setGraphInteractionMode: (graphInteractionMode) => set({
    graphInteractionMode,
    contextMenuNodeId: null,
    contextMenuPos: null,
  }),

  bottomOpen: false,
  bottomContent: null,
  openBottom: (content) => set({ bottomOpen: true, bottomContent: content }),
  closeBottom: () => set({ bottomOpen: false, bottomContent: null }),

  searchQuery: '',
  setSearchQuery: (q) => set({ searchQuery: q }),

  contextMenuNodeId: null,
  contextMenuPos: null,
  openContextMenu: (nodeId, pos) => set({ contextMenuNodeId: nodeId, contextMenuPos: pos }),
  closeContextMenu: () => set({ contextMenuNodeId: null, contextMenuPos: null }),

  pathSourceId: null,
  pathTargetId: null,
  highlightedPath: null,
  focusSubgraphNodeId: null,
  focusedNodeId: null,
  showAllRequestId: 0,
  childOrbitRequest: null,
  setPathSource: (id) => set({ pathSourceId: id }),
  setPathTarget: (id) => set({ pathTargetId: id }),
  setHighlightedPath: (path) => set({ highlightedPath: path }),
  requestFocusSubgraph: (id) => set({ focusSubgraphNodeId: id }),
  clearFocusSubgraphRequest: () => set({ focusSubgraphNodeId: null }),
  requestFocusNode: (id) => set({ focusedNodeId: id }),
  clearFocusNodeRequest: () => set({ focusedNodeId: null }),
  requestShowAll: () => set((state) => ({ showAllRequestId: state.showAllRequestId + 1 })),
  requestChildOrbit: (nodeId, strength) => set((state) => ({
    childOrbitRequest: {
      nodeId,
      strength: Number.isFinite(strength) ? Math.min(1, Math.max(0, strength)) : 0,
      requestId: (state.childOrbitRequest?.requestId ?? 0) + 1,
    },
  })),
  clearPath: () => set({ pathSourceId: null, pathTargetId: null, highlightedPath: null }),

  camera: { x: 0, y: 0, ratio: 1 },
  setCamera: (c) => set({ camera: c }),

  loading: false,
  loadError: null,
  setLoading: (v) => set({ loading: v }),
  setLoadError: (message) => set({ loadError: message }),

  visibleNodeTypes: new Set(['taxonomy', 'topic', 'subtopic', 'concept', 'rule', 'definition', 'procedure', 'exception', 'evidence_span']),
  visibleNodeLabelTypes: new Set(['taxonomy', 'topic', 'subtopic', 'concept', 'rule', 'definition', 'procedure', 'exception', 'evidence_span', 'document_version']),
  showScaffoldAnchors: false,
  visibleEdgeTypes: new Set([
    'HAS_CHILD',
    'BELONGS_TO',
    'RELATED_TO',
    'DEPENDS_ON',
    'APPLIES_TO',
    'PART_OF',
    'REQUIRES',
    'EXCLUDES',
    'CONSTRAINS',
    'AFFECTS',
    'INFLUENCES',
    'USED_IN',
    'EXECUTED_IN',
    'REGULATED_BY',
    'DEFINED_BY',
    'SUPPORTED_BY',
    'INFORMS',
    'SUPPORTS',
    'RESISTS',
    'COLLECTS',
    'CONVEYS',
    'MITIGATES',
    'DRAINS_TO',
    'CONNECTS_TO',
    'TRANSFERS_LOAD_TO',
    'DISCHARGES_TO',
    'COORDINATES_WITH',
    'CROSS_DOMAIN_ALIGNMENT',
  ]),
  hiddenNodeIds: [],
  expandedNodeIds: [],
  setVisibleNodeTypes: (types) => set({ visibleNodeTypes: types }),
  setVisibleEdgeTypes: (types) => set({ visibleEdgeTypes: types }),
  setVisibleNodeLabelTypes: (types) => set({ visibleNodeLabelTypes: types }),
  setShowScaffoldAnchors: (showScaffoldAnchors) => set({ showScaffoldAnchors }),
  setHiddenNodeIds: (ids) => set({ hiddenNodeIds: ids }),
  setExpandedNodeIds: (ids) => set({ expandedNodeIds: ids }),
  addExpandedNodeIds: (ids) => set((state) => ({
    expandedNodeIds: Array.from(new Set([...state.expandedNodeIds, ...ids])),
  })),

  layout: 'forceatlas2',
  setLayout: (layout) => set({ layout }),
  layoutSpread: DEFAULT_GRAPH_LAYOUT_SPREAD,
  setLayoutSpread: (layoutSpread) => set({ layoutSpread: clampGraphLayoutSpread(layoutSpread) }),
  colorScheme: 'default',
  setColorScheme: (scheme) => set({ colorScheme: scheme }),
  sizeBy: 'uniform',
  setSizeBy: (metric) => set({ sizeBy: metric }),
}));
