import { useRef, useState, useEffect, useCallback, useMemo } from 'react';
import { ZoomIn, ZoomOut, Maximize, Shrink, Map, LayoutGrid, FolderTree, Calendar, Terminal } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import VisNetworkHost, { type GraphController } from './graph/VisNetworkHost';
import NodeContextMenu from './graph/NodeContextMenu';
import QueryPanel from './graph/QueryPanel';
import Minimap from './graph/Minimap';

export default function GraphScene() {
  const controllerRef = useRef<GraphController>(null);
  const [queryOpen, setQueryOpen] = useState(false);
  const appliedSceneRef = useRef<string | null>(null);

  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const focusSubgraphNodeId = useSceneStore(s => s.focusSubgraphNodeId);
  const focusedNodeId = useSceneStore(s => s.focusedNodeId);
  const clearFocusSubgraphRequest = useSceneStore(s => s.clearFocusSubgraphRequest);
  const clearFocusNodeRequest = useSceneStore(s => s.clearFocusNodeRequest);
  const hiddenNodeIds = useSceneStore(s => s.hiddenNodeIds);
  const camera = useSceneStore(s => s.camera);
  const layout = useSceneStore(s => s.layout);
  const setLayout = useSceneStore(s => s.setLayout);

  const loading = useSceneStore(s => s.loading);
  const loadError = useSceneStore(s => s.loadError);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const contextMenuNodeId = useSceneStore(s => s.contextMenuNodeId);
  const highlightedPath = useSceneStore(s => s.highlightedPath);
  const hiddenCount = hiddenNodeIds.length;
  const visibleTypeCount = useMemo(() => {
    const nodeTypes = new Set(nodes.map((node) => node.type));
    const edgeTypes = new Set(edges.map((edge) => edge.type));
    return [...visibleNodeTypes].filter((type) => nodeTypes.has(type)).length
      + [...visibleEdgeTypes].filter((type) => edgeTypes.has(type)).length;
  }, [edges, nodes, visibleEdgeTypes, visibleNodeTypes]);
  const layoutLabel = layout === 'forceatlas2' ? 'Force' : layout === 'clustered' ? 'Clustered' : layout === 'time' ? 'Timeline' : layout[0].toUpperCase() + layout.slice(1);

  const loadGraphToHost = useCallback(() => {
    if (nodes.length === 0 || !controllerRef.current) return false;
    controllerRef.current.loadPerspective(nodes, edges);
    return true;
  }, [nodes, edges]);

  // Sync graph data to vis-network when nodes/edges change
  useEffect(() => {
    if (loadGraphToHost()) return;
    if (nodes.length === 0) return;

    const frame = requestAnimationFrame(() => {
      loadGraphToHost();
    });

    return () => cancelAnimationFrame(frame);
  }, [loadGraphToHost, nodes.length]);

  useEffect(() => {
    controllerRef.current?.setLayout(layout);
  }, [layout]);

  useEffect(() => {
    if (!activeSceneId || nodes.length === 0 || !controllerRef.current) return;
    if (appliedSceneRef.current === activeSceneId) return;

    controllerRef.current.applySceneView({ camera, hiddenNodeIds });
    appliedSceneRef.current = activeSceneId;
  }, [activeSceneId, camera, hiddenNodeIds, nodes.length]);

  useEffect(() => {
    if (!activeSceneId) {
      appliedSceneRef.current = null;
    }
  }, [activeSceneId]);

  useEffect(() => {
    if (!focusSubgraphNodeId) return;
    controllerRef.current?.focusSubgraph(focusSubgraphNodeId);
    clearFocusSubgraphRequest();
  }, [focusSubgraphNodeId, clearFocusSubgraphRequest]);

  useEffect(() => {
    if (!focusedNodeId) return;
    controllerRef.current?.focusNode(focusedNodeId);
    clearFocusNodeRequest();
  }, [focusedNodeId, clearFocusNodeRequest]);

  // Sync selection to graph
  useEffect(() => {
    controllerRef.current?.selectNode(selectedNodeId);
  }, [selectedNodeId]);

  // Sync filters (when user toggles checkboxes)
  useEffect(() => {
    controllerRef.current?.setFilters(visibleNodeTypes, visibleEdgeTypes);
  }, [visibleNodeTypes, visibleEdgeTypes]);

  // Sync color scheme
  const colorScheme = useSceneStore(s => s.colorScheme);
  useEffect(() => {
    controllerRef.current?.setColorScheme(colorScheme);
  }, [colorScheme]);

  // Sync size metric
  const sizeBy = useSceneStore(s => s.sizeBy);
  useEffect(() => {
    controllerRef.current?.setSizeBy(sizeBy);
  }, [sizeBy]);

  // Sync path highlighting
  useEffect(() => {
    if (highlightedPath) {
      controllerRef.current?.highlightPath(highlightedPath.nodeIds, highlightedPath.edgeIds);
    } else {
      controllerRef.current?.clearPathHighlight();
    }
  }, [highlightedPath]);

  const switchLayout = (type: 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time') => {
    setLayout(type);
  };

  return (
    <div className="kg-graph-backdrop flex-1 relative bg-bg overflow-hidden">
      <VisNetworkHost ref={controllerRef} />

      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 bg-bg/80 flex items-center justify-center z-30">
          <div className="kg-card flex flex-col items-center gap-3 rounded-2xl px-8 py-6">
            <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
            <span className="text-sm text-text">Loading graph perspective</span>
            <span className="max-w-xs text-center text-xs text-text-dim">Fetching nodes, relationships, and layout context for the selected perspective.</span>
          </div>
        </div>
      )}

      {!loading && loadError && (
        <div className="absolute inset-x-4 top-4 z-20 rounded-lg border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-100 shadow-lg">
          Unable to load this graph view: {loadError}
        </div>
      )}

      {/* Zoom controls */}
      <div className="absolute bottom-4 left-4 flex flex-col gap-1.5 z-20">
        <button onClick={() => controllerRef.current?.zoomIn()} className="kg-control p-2.5 rounded-xl text-text-dim hover:text-text transition-colors" title="Zoom in" aria-label="Zoom in">
          <ZoomIn size={16} />
        </button>
        <button onClick={() => controllerRef.current?.zoomOut()} className="kg-control p-2.5 rounded-xl text-text-dim hover:text-text transition-colors" title="Zoom out" aria-label="Zoom out">
          <ZoomOut size={16} />
        </button>
        <button onClick={() => controllerRef.current?.fitView()} className="kg-control p-2.5 rounded-xl text-text-dim hover:text-text transition-colors" title="Fit to view" aria-label="Fit graph to view">
          <Maximize size={16} />
        </button>
      </div>

      {/* Context menu */}
      {contextMenuNodeId && (
        <NodeContextMenu controllerRef={controllerRef} />
      )}

      {/* Query panel */}
      {queryOpen && (
        <QueryPanel controllerRef={controllerRef} onClose={() => setQueryOpen(false)} />
      )}

      {/* Layout switcher */}
      <div className="absolute top-4 left-4 z-20">
        <div className="kg-card flex items-center gap-1 rounded-2xl p-1.5">
          <button onClick={() => switchLayout('forceatlas2')} className={`p-2 rounded-xl ${layout === 'forceatlas2' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="ForceAtlas2" aria-label="Use force layout">
            <LayoutGrid size={14} />
          </button>
          <button onClick={() => switchLayout('circular')} className={`p-2 rounded-xl ${layout === 'circular' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Circular" aria-label="Use circular layout">
            <Shrink size={14} />
          </button>
          <button onClick={() => switchLayout('random')} className={`p-2 rounded-xl ${layout === 'random' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Random" aria-label="Use random layout">
            <Map size={14} />
          </button>
          <button onClick={() => switchLayout('clustered')} className={`p-2 rounded-xl ${layout === 'clustered' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Clustered by Taxonomy" aria-label="Use taxonomy clustered layout">
            <FolderTree size={14} />
          </button>
          <button onClick={() => switchLayout('time')} className={`p-2 rounded-xl ${layout === 'time' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Timeline by Creation Date" aria-label="Use timeline layout">
            <Calendar size={14} />
          </button>
          <div className="w-px h-4 bg-border mx-1" />
          <button
            onClick={() => setQueryOpen(o => !o)}
            className={`p-2 rounded-xl ${queryOpen ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="Cypher Query"
            aria-label="Toggle Cypher query panel"
          >
            <Terminal size={14} />
          </button>
        </div>
      </div>

      <div className="kg-card absolute right-4 top-4 z-20 rounded-2xl px-4 py-3 text-xs">
        <div className="text-[10px] uppercase tracking-[0.24em] text-text-dim">Scene</div>
        <div className="mt-1 flex items-center gap-3 text-text">
          <span>{nodes.length.toLocaleString()} nodes</span>
          <span>{edges.length.toLocaleString()} edges</span>
          <span>{layoutLabel}</span>
        </div>
        <div className="mt-1 text-text-dim">{hiddenCount > 0 ? `${hiddenCount} hidden · ` : ''}{visibleTypeCount} active filters</div>
      </div>

      <div className="absolute bottom-4 right-4 z-20 flex items-end gap-3">
        <div className="kg-card hidden rounded-2xl px-4 py-3 text-xs md:block">
          <div className="text-[10px] uppercase tracking-[0.24em] text-text-dim">Legend</div>
          <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1.5">
            <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-node-concept" />Concept</span>
            <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-node-rule" />Rule</span>
            <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-node-definition" />Definition</span>
            <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-sky-500" />Evidence</span>
          </div>
        </div>
        <Minimap controllerRef={controllerRef} />
      </div>
    </div>
  );
}
