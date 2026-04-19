import { useRef, useState, useEffect, useCallback } from 'react';
import { ZoomIn, ZoomOut, Maximize, Shrink, Map, LayoutGrid, FolderTree, Calendar, Terminal } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective } from '../api/graphApi';
import VisNetworkHost, { type GraphController } from './graph/VisNetworkHost';
import NodeSearch from './graph/NodeSearch';
import NodeContextMenu from './graph/NodeContextMenu';
import QueryPanel from './graph/QueryPanel';

export default function GraphScene() {
  const controllerRef = useRef<GraphController>(null);
  const [layout, setLayout] = useState<'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time'>('forceatlas2');
  const [queryOpen, setQueryOpen] = useState(false);

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setLoading = useSceneStore(s => s.setLoading);
  const setGraphData = useSceneStore(s => s.setGraphData);

  const loading = useSceneStore(s => s.loading);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const contextMenuNodeId = useSceneStore(s => s.contextMenuNodeId);
  const highlightedPath = useSceneStore(s => s.highlightedPath);

  // Load perspective data when it changes
  useEffect(() => {
    async function load() {
      setLoading(true);
      const data = await getNodesForPerspective(perspectiveId);
      setGraphData(data.nodes, data.edges);
      setLoading(false);
    }
    load();
  }, [perspectiveId, setLoading, setGraphData]);

  // Sync graph data to vis-network when nodes/edges change
  useEffect(() => {
    if (nodes.length > 0) {
      controllerRef.current?.loadPerspective(nodes, edges);
      // Re-apply current filters after loading new perspective data
      controllerRef.current?.setFilters(visibleNodeTypes, visibleEdgeTypes);
    }
  }, [nodes, edges]);

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
    controllerRef.current?.setLayout(type);
  };

  const handleSearchSelect = useCallback((id: string) => {
    controllerRef.current?.focusNode(id);
    const store = useSceneStore.getState();
    store.setSelectedNode(id);
    store.openInspector();
  }, []);

  return (
    <div className="flex-1 relative bg-bg overflow-hidden">
      <VisNetworkHost ref={controllerRef} />

      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 bg-bg/80 flex items-center justify-center z-10">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
            <span className="text-sm text-text-dim">Loading graph...</span>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20">
        <NodeSearch nodes={nodes} onSelect={handleSearchSelect} />
      </div>

      {/* Zoom controls */}
      <div className="absolute bottom-4 left-4 flex flex-col gap-1 z-20">
        <button onClick={() => controllerRef.current?.zoomIn()} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Zoom in">
          <ZoomIn size={16} />
        </button>
        <button onClick={() => controllerRef.current?.zoomOut()} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Zoom out">
          <ZoomOut size={16} />
        </button>
        <button onClick={() => controllerRef.current?.fitView()} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Fit to view">
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
        <div className="flex items-center gap-1 bg-panel border border-border rounded-md p-1">
          <button onClick={() => switchLayout('forceatlas2')} className={`p-1.5 rounded ${layout === 'forceatlas2' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="ForceAtlas2">
            <LayoutGrid size={14} />
          </button>
          <button onClick={() => switchLayout('circular')} className={`p-1.5 rounded ${layout === 'circular' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Circular">
            <Shrink size={14} />
          </button>
          <button onClick={() => switchLayout('random')} className={`p-1.5 rounded ${layout === 'random' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Random">
            <Map size={14} />
          </button>
          <button onClick={() => switchLayout('clustered')} className={`p-1.5 rounded ${layout === 'clustered' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Clustered by Taxonomy">
            <FolderTree size={14} />
          </button>
          <button onClick={() => switchLayout('time')} className={`p-1.5 rounded ${layout === 'time' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`} title="Timeline by Creation Date">
            <Calendar size={14} />
          </button>
          <div className="w-px h-4 bg-border mx-1" />
          <button
            onClick={() => setQueryOpen(o => !o)}
            className={`p-1.5 rounded ${queryOpen ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="Cypher Query"
          >
            <Terminal size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
