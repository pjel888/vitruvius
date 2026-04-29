import { useRef, useState, useEffect, useCallback } from 'react';
import { Code2, Pause, Play, ZoomIn, ZoomOut, Maximize } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import VisNetworkHost, { type GraphController } from './graph/VisNetworkHost';
import NodeContextMenu from './graph/NodeContextMenu';
import QueryPanel from './graph/QueryPanel';
import Minimap from './graph/Minimap';
import { DEFAULT_GRAPH_LAYOUT_SPREAD, MAX_GRAPH_LAYOUT_SPREAD, MIN_GRAPH_LAYOUT_SPREAD, clampGraphLayoutSpread } from './graph/layoutSpread';
import { clampUserFacingZoomScale } from './graph/graphVisualEmphasis';
import LayoutMenu from './graph/LayoutMenu';
import { type GraphLayout } from './graph/layoutOptions';

export default function GraphScene() {
  const controllerRef = useRef<GraphController>(null);
  const [queryOpen, setQueryOpen] = useState(false);
  const [layoutMenuOpen, setLayoutMenuOpen] = useState(false);
  const [motionPaused, setMotionPaused] = useState(false);
  const [zoomScale, setZoomScale] = useState(1);
  const [spreadPauseNotice, setSpreadPauseNotice] = useState(false);
  const appliedSceneRef = useRef<string | null>(null);

  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const focusSubgraphNodeId = useSceneStore(s => s.focusSubgraphNodeId);
  const focusedNodeId = useSceneStore(s => s.focusedNodeId);
  const showAllRequestId = useSceneStore(s => s.showAllRequestId);
  const childOrbitRequest = useSceneStore(s => s.childOrbitRequest);
  const clearFocusSubgraphRequest = useSceneStore(s => s.clearFocusSubgraphRequest);
  const clearFocusNodeRequest = useSceneStore(s => s.clearFocusNodeRequest);
  const hiddenNodeIds = useSceneStore(s => s.hiddenNodeIds);
  const camera = useSceneStore(s => s.camera);
  const layout = useSceneStore(s => s.layout);
  const setLayout = useSceneStore(s => s.setLayout);
  const layoutSpread = useSceneStore(s => s.layoutSpread);
  const setLayoutSpread = useSceneStore(s => s.setLayoutSpread);
  const visibleNodeLabelTypes = useSceneStore(s => s.visibleNodeLabelTypes);
  const showScaffoldAnchors = useSceneStore(s => s.showScaffoldAnchors);

  const loading = useSceneStore(s => s.loading);
  const loadError = useSceneStore(s => s.loadError);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const contextMenuNodeId = useSceneStore(s => s.contextMenuNodeId);
  const highlightedPath = useSceneStore(s => s.highlightedPath);

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
    controllerRef.current?.setLayoutSpread(layoutSpread);
  }, [layoutSpread]);

  useEffect(() => {
    controllerRef.current?.setMotionPaused(motionPaused);
  }, [motionPaused]);

  useEffect(() => {
    controllerRef.current?.setLabelFilters(visibleNodeLabelTypes);
  }, [visibleNodeLabelTypes]);

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

  useEffect(() => {
    if (showAllRequestId === 0) return;
    controllerRef.current?.showAll();
  }, [showAllRequestId]);

  useEffect(() => {
    if (!childOrbitRequest) return;
    controllerRef.current?.arrangeChildOrbit(childOrbitRequest.nodeId, childOrbitRequest.strength);
  }, [childOrbitRequest]);

  // Sync selection to graph
  useEffect(() => {
    controllerRef.current?.selectNode(selectedNodeId);
  }, [selectedNodeId]);

  // Sync filters (when user toggles checkboxes)
  useEffect(() => {
    controllerRef.current?.setFilters(visibleNodeTypes, visibleEdgeTypes, showScaffoldAnchors);
  }, [visibleNodeTypes, visibleEdgeTypes, showScaffoldAnchors]);

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

  const switchLayout = (type: GraphLayout) => {
    setLayout(type);
    setLayoutMenuOpen(false);
  };

  const changeSpreadFromUser = (spread: number) => {
    setMotionPaused(true);
    setSpreadPauseNotice(true);
    setLayoutSpread(clampGraphLayoutSpread(spread));
  };

  const changeZoomFromUser = (scale: number) => {
    const nextScale = clampUserFacingZoomScale(scale);
    setZoomScale(nextScale);
    controllerRef.current?.setZoomScale(nextScale);
  };

  const resetViewControls = () => {
    changeSpreadFromUser(DEFAULT_GRAPH_LAYOUT_SPREAD);
    changeZoomFromUser(1);
  };

  const densityPresets = [
    { label: 'Dense', value: 1 },
    { label: 'Comfort', value: DEFAULT_GRAPH_LAYOUT_SPREAD },
    { label: 'Spacious', value: 4 },
    { label: 'Max', value: MAX_GRAPH_LAYOUT_SPREAD },
  ];

  return (
    <div className="kg-graph-backdrop flex-1 relative bg-bg overflow-hidden">
      <VisNetworkHost ref={controllerRef} onZoomChange={setZoomScale} />

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
      <div className="absolute bottom-4 left-4 z-20">
        <div className="kg-control flex flex-col gap-2 rounded-2xl p-2 text-text-dim">
          <div className="flex items-center gap-1.5">
            <button onClick={() => controllerRef.current?.zoomIn()} className="rounded-xl p-2 transition-colors hover:text-text" title="Zoom in" aria-label="Zoom in">
              <ZoomIn size={16} />
            </button>
            <button onClick={() => controllerRef.current?.zoomOut()} className="rounded-xl p-2 transition-colors hover:text-text" title="Zoom out" aria-label="Zoom out">
              <ZoomOut size={16} />
            </button>
            <button onClick={() => { controllerRef.current?.fitView(); }} className="rounded-xl p-2 transition-colors hover:text-text" title="Fit to view" aria-label="Fit graph to view">
              <Maximize size={16} />
            </button>
          </div>
          <label className="flex min-w-44 items-center gap-2 px-1 text-[10px] uppercase tracking-[0.18em]" title="Zoom the graph viewport">
            <span>Zoom</span>
            <input
              aria-label="Graph zoom"
              className="w-24 accent-cyan-300"
              type="range"
              min={0.1}
              max={4}
              step={0.05}
              value={zoomScale}
              onChange={(event) => changeZoomFromUser(Number(event.currentTarget.value))}
            />
            <span className="tabular-nums text-text">{zoomScale.toFixed(2)}×</span>
          </label>
        </div>
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
        <div className="kg-card flex items-center gap-2 rounded-2xl p-1.5">
          <LayoutMenu
            layout={layout}
            open={layoutMenuOpen}
            onToggle={() => setLayoutMenuOpen((open) => !open)}
            onClose={() => setLayoutMenuOpen(false)}
            onSelect={switchLayout}
          />
          <button
            onClick={() => { setMotionPaused((paused) => !paused); setSpreadPauseNotice(false); }}
            className={`p-2 rounded-xl ${motionPaused ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title={motionPaused ? 'Resume graph motion' : 'Stop graph motion'}
            aria-label={motionPaused ? 'Resume graph motion' : 'Stop graph motion'}
          >
            {motionPaused ? <Play size={14} /> : <Pause size={14} />}
          </button>
          <button
            onClick={() => setQueryOpen(o => !o)}
            className={`flex items-center gap-1.5 rounded-xl px-2 py-2 ${queryOpen ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="Advanced graph query"
            aria-label={queryOpen ? 'Close advanced graph query panel' : 'Open advanced graph query panel'}
          >
            <Code2 size={14} />
            <span className="hidden text-[10px] font-semibold uppercase tracking-[0.14em] sm:inline">Query</span>
          </button>
          <label className="flex min-w-36 items-center gap-2 px-2 text-[10px] uppercase tracking-[0.18em] text-text-dim" title="Expand or compress the graph layout spacing">
            <span>Spread</span>
            <input
              aria-label="Graph layout spread"
              className="w-24 accent-cyan-300"
              type="range"
              min={MIN_GRAPH_LAYOUT_SPREAD}
              max={MAX_GRAPH_LAYOUT_SPREAD}
              step={0.05}
              value={layoutSpread}
              onChange={(event) => changeSpreadFromUser(Number(event.currentTarget.value))}
            />
            <span className="tabular-nums text-text">{layoutSpread.toFixed(2)}×</span>
            <button
              aria-label="Reset graph view controls"
              className="rounded border border-white/10 px-1.5 py-0.5 text-[9px] text-text-dim transition hover:border-cyan-300/40 hover:text-text"
              type="button"
              onClick={resetViewControls}
            >
              Reset
            </button>
          </label>
          <div className="flex items-center gap-1 px-1" aria-label="Graph density presets">
            {densityPresets.map((preset) => (
              <button
                key={preset.label}
                type="button"
                className={`rounded border px-1.5 py-0.5 text-[9px] transition ${Math.abs(layoutSpread - preset.value) < 0.01 ? 'border-cyan-300/60 bg-cyan-300/10 text-cyan-100' : 'border-white/10 text-text-dim hover:border-cyan-300/40 hover:text-text'}`}
                onClick={() => changeSpreadFromUser(preset.value)}
              >
                {preset.label}
              </button>
            ))}
          </div>
          {spreadPauseNotice && motionPaused && (
            <span className="px-2 text-[9px] uppercase tracking-[0.16em] text-cyan-100/80">Physics paused after spread change</span>
          )}
        </div>
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
