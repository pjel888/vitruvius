import { useRef, useState, useCallback, useEffect } from 'react';
import { ZoomIn, ZoomOut, Maximize, Shrink, Map, LayoutGrid, MousePointerClick } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective, expandNode } from '../api/graphApi';
import SigmaHost, { type GraphController } from './graph/SigmaHost';
import Minimap from './graph/Minimap';

export default function GraphScene() {
  const controllerRef = useRef<GraphController>(null);
  const [layout, setLayout] = useState<'forceatlas2' | 'circular' | 'random'>('forceatlas2');
  const [showMinimap, setShowMinimap] = useState(false);
  const [multiSelect, setMultiSelect] = useState(false);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; nodeId: string } | null>(null);

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setLoading = useSceneStore(s => s.setLoading);
  const setGraphData = useSceneStore(s => s.setGraphData);

  // Load perspective data when it changes
  useEffect(() => {
    async function load() {
      setLoading(true);
      const { nodes, edges } = await getNodesForPerspective(perspectiveId);
      setGraphData(nodes, edges);

      // Wait for Sigma controller to be ready (it initializes in a child useEffect)
      let attempts = 0;
      const tryLoad = () => {
        if (controllerRef.current) {
          controllerRef.current.loadPerspective(nodes, edges);
          setLoading(false);
        } else if (attempts < 50) {
          attempts++;
          setTimeout(tryLoad, 100);
        } else {
          setLoading(false);
          console.error('Graph controller never became ready');
        }
      };
      tryLoad();
    }
    load();
  }, [perspectiveId, setLoading, setGraphData]);

  // Sync selection to graph
  useEffect(() => {
    controllerRef.current?.selectNode(selectedNodeId);
  }, [selectedNodeId]);

  const switchLayout = useCallback((type: 'forceatlas2' | 'circular' | 'random') => {
    setLayout(type);
    controllerRef.current?.setLayout(type);
  }, []);

  const doExpand = useCallback(async (nodeId: string) => {
    setLoading(true);
    const result = await expandNode(nodeId);
    controllerRef.current?.expandNode(nodeId, result);
    setLoading(false);
    setContextMenu(null);
  }, [setLoading]);

  const loading = useSceneStore(s => s.loading);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const [debugInfo, setDebugInfo] = useState({ nodes: 0, edges: 0, controllerReady: false });

  // Debug info polling
  useEffect(() => {
    const interval = setInterval(() => {
      setDebugInfo({
        nodes: nodes.length,
        edges: edges.length,
        controllerReady: !!controllerRef.current,
      });
    }, 500);
    return () => clearInterval(interval);
  }, [nodes, edges]);

  return (
    <div className="flex-1 relative bg-bg overflow-hidden">
      <SigmaHost ref={controllerRef} />

      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 bg-bg/80 flex items-center justify-center z-10">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
            <span className="text-sm text-text-dim">Loading graph...</span>
          </div>
        </div>
      )}

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
        </div>
      </div>

      {/* Debug overlay */}
      <div className="absolute top-4 right-4 z-20 bg-panel/90 border border-border rounded-md px-3 py-2 text-xs font-mono space-y-1">
        <div>Nodes: {debugInfo.nodes}</div>
        <div>Edges: {debugInfo.edges}</div>
        <div>Controller: {debugInfo.controllerReady ? '✓' : '✗'}</div>
        <button
          className="mt-1 px-2 py-1 bg-accent/20 text-accent rounded hover:bg-accent/30 transition-colors"
          onClick={() => {
            console.log('Manual refresh triggered');
            controllerRef.current?.setLayout('circular');
            controllerRef.current?.fitView();
          }}
        >
          Force Render
        </button>
      </div>

      {/* Multi-select toggle */}
      <div className="absolute top-4 left-32 z-20">
        <button onClick={() => setMultiSelect(!multiSelect)} className={`flex items-center gap-1.5 px-2.5 py-1.5 bg-panel border border-border rounded-md text-xs transition-colors ${multiSelect ? 'border-accent text-accent' : 'text-text-dim hover:text-text'}`} title="Toggle multi-select">
          <MousePointerClick size={14} />
          {multiSelect ? 'Multi' : 'Single'}
        </button>
      </div>

      {/* Minimap toggle */}
      <div className="absolute bottom-4 right-4 z-20">
        <button onClick={() => setShowMinimap(!showMinimap)} className={`p-2 bg-panel border border-border rounded-md transition-colors ${showMinimap ? 'border-accent text-accent' : 'text-text-dim hover:text-text'}`} title="Toggle minimap">
          <Map size={16} />
        </button>
      </div>

      {/* Minimap */}
      {showMinimap && <Minimap controllerRef={controllerRef} />}

      {/* Context menu */}
      {contextMenu && (
        <div className="absolute z-30 bg-panel border border-border rounded-lg shadow-xl py-1 w-48" style={{ left: contextMenu.x, top: contextMenu.y }}>
          <button className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors" onClick={() => { setSelectedNode(contextMenu.nodeId); setContextMenu(null); }}>
            Select node
          </button>
          <button className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors" onClick={() => doExpand(contextMenu.nodeId)}>
            Expand neighbors
          </button>
          <button className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors" onClick={() => { controllerRef.current?.fitView(); setContextMenu(null); }}>
            Fit to view
          </button>
          <div className="border-t border-border my-1" />
          <button className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors text-text-dim" onClick={() => setContextMenu(null)}>
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}
