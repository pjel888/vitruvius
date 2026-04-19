import { create } from 'zustand';
import type { GraphNode, GraphEdge } from '../types';

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

  searchQuery: '',
  setSearchQuery: (q) => set({ searchQuery: q }),

  camera: { x: 0, y: 0, ratio: 1 },
  setCamera: (c) => set({ camera: c }),

  loading: false,
  setLoading: (v) => set({ loading: v }),
}));
