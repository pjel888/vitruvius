import { create } from 'zustand';
import type { CameraState, GraphNode, GraphEdge, SceneState } from '../types';
import { DEFAULT_EXPLORER_PERSPECTIVE_ID } from '../constants/perspectives';

type LayoutType = 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time';

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
  preloadedPerspectiveId: string | null;
  markPreloadedPerspective: (id: string | null) => void;

  // UI state
  explorerOpen: boolean;
  inspectorOpen: boolean;
  toggleExplorer: () => void;
  toggleInspector: () => void;
  openInspector: () => void;
  closeInspector: () => void;

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
  hiddenNodeIds: string[];
  expandedNodeIds: string[];
  setVisibleNodeTypes: (types: Set<string>) => void;
  setVisibleEdgeTypes: (types: Set<string>) => void;
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
  markPreloadedPerspective: (id) => set({ preloadedPerspectiveId: id }),

  explorerOpen: true,
  inspectorOpen: false,
  toggleExplorer: () => set(s => ({ explorerOpen: !s.explorerOpen })),
  toggleInspector: () => set(s => ({ inspectorOpen: !s.inspectorOpen })),
  openInspector: () => set({ inspectorOpen: true }),
  closeInspector: () => set({ inspectorOpen: false }),

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
  setPathSource: (id) => set({ pathSourceId: id }),
  setPathTarget: (id) => set({ pathTargetId: id }),
  setHighlightedPath: (path) => set({ highlightedPath: path }),
  requestFocusSubgraph: (id) => set({ focusSubgraphNodeId: id }),
  clearFocusSubgraphRequest: () => set({ focusSubgraphNodeId: null }),
  requestFocusNode: (id) => set({ focusedNodeId: id }),
  clearFocusNodeRequest: () => set({ focusedNodeId: null }),
  requestShowAll: () => set((state) => ({ showAllRequestId: state.showAllRequestId + 1 })),
  clearPath: () => set({ pathSourceId: null, pathTargetId: null, highlightedPath: null }),

  camera: { x: 0, y: 0, ratio: 1 },
  setCamera: (c) => set({ camera: c }),

  loading: false,
  loadError: null,
  setLoading: (v) => set({ loading: v }),
  setLoadError: (message) => set({ loadError: message }),

  visibleNodeTypes: new Set(['taxonomy', 'topic', 'subtopic', 'concept', 'rule', 'definition', 'procedure', 'exception', 'evidence_span']),
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
  ]),
  hiddenNodeIds: [],
  expandedNodeIds: [],
  setVisibleNodeTypes: (types) => set({ visibleNodeTypes: types }),
  setVisibleEdgeTypes: (types) => set({ visibleEdgeTypes: types }),
  setHiddenNodeIds: (ids) => set({ hiddenNodeIds: ids }),
  setExpandedNodeIds: (ids) => set({ expandedNodeIds: ids }),
  addExpandedNodeIds: (ids) => set((state) => ({
    expandedNodeIds: Array.from(new Set([...state.expandedNodeIds, ...ids])),
  })),

  layout: 'forceatlas2',
  setLayout: (layout) => set({ layout }),
  layoutSpread: 1.45,
  setLayoutSpread: (layoutSpread) => set({ layoutSpread }),
  colorScheme: 'default',
  setColorScheme: (scheme) => set({ colorScheme: scheme }),
  sizeBy: 'uniform',
  setSizeBy: (metric) => set({ sizeBy: metric }),
}));
