import { create } from 'zustand';
import type { GraphNode, GraphEdge } from '../types';

interface BottomContent {
  type: 'source' | 'table' | 'query';
  title: string;
  documentId?: string;
  quote?: string;
  deepLink?: string;
}

interface SceneStore {
  // View state
  perspectiveId: string;
  setPerspectiveId: (id: string) => void;

  // Selection
  selectedNodeId: string | null;
  selectedEdgeId: string | null;
  setSelectedNode: (id: string | null) => void;
  setSelectedEdge: (id: string | null) => void;

  // Graph data
  nodes: GraphNode[];
  edges: GraphEdge[];
  setGraphData: (nodes: GraphNode[], edges: GraphEdge[]) => void;

  // UI state
  explorerOpen: boolean;
  inspectorOpen: boolean;
  toggleExplorer: () => void;
  toggleInspector: () => void;

  // Bottom drawer
  bottomOpen: boolean;
  bottomContent: BottomContent | null;
  openBottom: (content: BottomContent) => void;
  closeBottom: () => void;

  // Search
  searchQuery: string;
  setSearchQuery: (q: string) => void;

  // Camera (for Sigma)
  camera: { x: number; y: number; ratio: number };
  setCamera: (c: { x: number; y: number; ratio: number }) => void;

  // Loading
  loading: boolean;
  setLoading: (v: boolean) => void;
}

export const useSceneStore = create<SceneStore>((set) => ({
  perspectiveId: 'default',
  setPerspectiveId: (id) => set({ perspectiveId: id, selectedNodeId: null, selectedEdgeId: null }),

  selectedNodeId: null,
  selectedEdgeId: null,
  setSelectedNode: (id) => set({ selectedNodeId: id, selectedEdgeId: null }),
  setSelectedEdge: (id) => set({ selectedEdgeId: id, selectedNodeId: null }),

  nodes: [],
  edges: [],
  setGraphData: (nodes, edges) => set({ nodes, edges }),

  explorerOpen: true,
  inspectorOpen: false,
  toggleExplorer: () => set(s => ({ explorerOpen: !s.explorerOpen })),
  toggleInspector: () => set(s => ({ inspectorOpen: !s.inspectorOpen })),

  bottomOpen: false,
  bottomContent: null,
  openBottom: (content) => set({ bottomOpen: true, bottomContent: content }),
  closeBottom: () => set({ bottomOpen: false, bottomContent: null }),

  searchQuery: '',
  setSearchQuery: (q) => set({ searchQuery: q }),

  camera: { x: 0, y: 0, ratio: 1 },
  setCamera: (c) => set({ camera: c }),

  loading: false,
  setLoading: (v) => set({ loading: v }),
}));
