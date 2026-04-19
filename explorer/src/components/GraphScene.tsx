import { useEffect, useState, useRef, useCallback } from 'react';
import { SigmaContainer, useLoadGraph, useRegisterEvents, useSigma } from '@react-sigma/core';
import { LayoutForceAtlas2Control, useLayoutForceAtlas2 } from '@react-sigma/layout-forceatlas2';
import Graph from 'graphology';
import { circular } from 'graphology-layout';
import { ZoomIn, ZoomOut, Maximize, Shrink, Map, LayoutGrid, MousePointerClick } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective, expandNode } from '../api/graphApi';

const NODE_COLORS: Record<string, string> = {
  taxonomy: '#60a5fa',
  topic: '#818cf8',
  subtopic: '#c084fc',
  concept: '#a78bfa',
  rule: '#f87171',
  definition: '#34d399',
  procedure: '#fbbf24',
  exception: '#f472b6',
};

const EDGE_COLORS: Record<string, string> = {
  HAS_CHILD: '#6b7280',
  BELONGS_TO: '#6b7280',
  RELATED_TO: '#6b7280',
  DEPENDS_ON: '#f59e0b',
  DEFINED_BY: '#10b981',
  REQUIRES: '#8b5cf6',
  SUPPORTED_BY: '#94a3b8',
};

type LayoutType = 'forceatlas2' | 'circular' | 'random';

function GraphRenderer() {
  const loadGraph = useLoadGraph();
  const { assign } = useLayoutForceAtlas2();
  const sigma = useSigma();
  const registerEvents = useRegisterEvents();

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const selectedEdgeId = useSceneStore(s => s.selectedEdgeId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setSelectedEdge = useSceneStore(s => s.setSelectedEdge);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);
  const setCamera = useSceneStore(s => s.setCamera);
  const loading = useSceneStore(s => s.loading);

  const [layout, setLayout] = useState<LayoutType>('forceatlas2');
  const [showMinimap, setShowMinimap] = useState(false);
  const [multiSelect, setMultiSelect] = useState(false);
  const [selectedNodes, setSelectedNodes] = useState<Set<string>>(new Set());
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; nodeId: string } | null>(null);

  const graphRef = useRef<Graph | null>(null);

  const applyLayout = useCallback((g: Graph, type: LayoutType) => {
    if (type === 'circular') {
      circular.assign(g, { scale: 200 });
    } else if (type === 'random') {
      g.forEachNode((node) => {
        g.setNodeAttribute(node, 'x', (Math.random() - 0.5) * 600);
        g.setNodeAttribute(node, 'y', (Math.random() - 0.5) * 600);
      });
    } else if (type === 'forceatlas2') {
      assign();
    }
  }, [assign]);

  const refresh = useCallback(async () => {
    setLoading(true);
    const { nodes, edges } = await getNodesForPerspective(perspectiveId);
    setGraphData(nodes, edges);

    const graph = new Graph();
    nodes.forEach((n, i) => {
      graph.addNode(n.id, {
        label: n.label,
        size: n.radius ?? 8,
        color: NODE_COLORS[n.type] || '#a78bfa',
        type: n.type,
        x: Math.cos((i / nodes.length) * Math.PI * 2) * 200,
        y: Math.sin((i / nodes.length) * Math.PI * 2) * 200,
      });
    });
    edges.forEach((e, i) => {
      if (graph.hasNode(e.source) && graph.hasNode(e.target)) {
        graph.addDirectedEdgeWithKey(e.id || `e${i}`, e.source, e.target, {
          size: 1.5,
          color: EDGE_COLORS[e.type] || '#6b7280',
          type: e.type,
        });
      }
    });

    graphRef.current = graph;
    loadGraph(graph);
    applyLayout(graph, layout);
    setLoading(false);
  }, [perspectiveId, layout, loadGraph, applyLayout, setGraphData, setLoading]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    if (!sigma) return;
    const graph = sigma.getGraph();

    graph.forEachNode((id) => {
      const isSelected = id === selectedNodeId || selectedNodes.has(id);
      graph.setNodeAttribute(id, 'highlighted', isSelected);
    });

    graph.forEachEdge((id) => {
      const isSelected = id === selectedEdgeId;
      graph.setEdgeAttribute(id, 'highlighted', isSelected);
    });

    sigma.refresh();
  }, [selectedNodeId, selectedEdgeId, selectedNodes, sigma]);

  useEffect(() => {
    registerEvents({
      clickNode: (e) => {
        if (e.node) {
          if (multiSelect || (e.event?.original as MouseEvent)?.shiftKey) {
            setSelectedNodes(prev => {
              const next = new Set(prev);
              if (next.has(e.node)) next.delete(e.node);
              else next.add(e.node);
              return next;
            });
          } else {
            setSelectedNode(e.node);
            setSelectedNodes(new Set([e.node]));
          }
        }
        setContextMenu(null);
      },
      clickEdge: (e) => {
        if (e.edge) setSelectedEdge(e.edge);
        setContextMenu(null);
      },
      clickStage: () => {
        setSelectedNode(null);
        setSelectedEdge(null);
        setSelectedNodes(new Set());
        setContextMenu(null);
      },
      rightClickNode: (e) => {
        if (e.node && e.event?.original) {
          (e.event.original as MouseEvent).preventDefault();
          setContextMenu({
            x: (e.event.original as MouseEvent).clientX,
            y: (e.event.original as MouseEvent).clientY,
            nodeId: e.node,
          });
        }
      },
      // Sigma v3 camera events handled differently; skipping for now
    });
  }, [registerEvents, setSelectedNode, setSelectedEdge, setCamera, multiSelect]);

  // Scale-dependent labels
  useEffect(() => {
    if (!sigma) return;
    const interval = setInterval(() => {
      const ratio = sigma.getCamera().ratio;
      const showLabels = ratio < 1.5;
      sigma.getGraph().forEachNode((id) => {
        sigma.getGraph().setNodeAttribute(id, 'forceLabel', showLabels);
      });
      sigma.refresh();
    }, 200);
    return () => clearInterval(interval);
  }, [sigma]);

  // Zoom controls
  const zoomIn = () => {
    const cam = sigma?.getCamera();
    if (cam) cam.animate({ ratio: cam.ratio / 1.5 }, { duration: 200 });
  };
  const zoomOut = () => {
    const cam = sigma?.getCamera();
    if (cam) cam.animate({ ratio: cam.ratio * 1.5 }, { duration: 200 });
  };
  const fitView = () => {
    sigma?.getCamera().animatedReset({ duration: 600 });
  };

  // Local expansion
  const doExpand = async (nodeId: string) => {
    if (!graphRef.current) return;
    setLoading(true);
    const { nodes: newNodes, edges: newEdges } = await expandNode(nodeId);

    const graph = graphRef.current;
    newNodes.forEach(n => {
      if (!graph.hasNode(n.id)) {
        graph.addNode(n.id, {
          label: n.label,
          size: n.radius ?? 8,
          color: NODE_COLORS[n.type] || '#a78bfa',
          type: n.type,
        });
      }
    });
    newEdges.forEach(e => {
      if (graph.hasNode(e.source) && graph.hasNode(e.target) && !graph.hasEdge(e.id)) {
        graph.addDirectedEdgeWithKey(e.id, e.source, e.target, {
          size: 1.5,
          color: EDGE_COLORS[e.type] || '#6b7280',
          type: e.type,
        });
      }
    });

    if (layout === 'forceatlas2') {
      assign();
    }
    setLoading(false);
    setContextMenu(null);
  };

  // Switch layout
  const switchLayout = (newLayout: LayoutType) => {
    setLayout(newLayout);
    if (graphRef.current) {
      applyLayout(graphRef.current, newLayout);
    }
  };

  return (
    <>
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
        <button onClick={zoomIn} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Zoom in">
          <ZoomIn size={16} />
        </button>
        <button onClick={zoomOut} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Zoom out">
          <ZoomOut size={16} />
        </button>
        <button onClick={fitView} className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors" title="Fit to view">
          <Maximize size={16} />
        </button>
      </div>

      {/* Layout switcher */}
      <div className="absolute top-4 left-4 z-20">
        <div className="flex items-center gap-1 bg-panel border border-border rounded-md p-1">
          <button
            onClick={() => switchLayout('forceatlas2')}
            className={`p-1.5 rounded ${layout === 'forceatlas2' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="ForceAtlas2"
          >
            <LayoutGrid size={14} />
          </button>
          <button
            onClick={() => switchLayout('circular')}
            className={`p-1.5 rounded ${layout === 'circular' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="Circular"
          >
            <Shrink size={14} />
          </button>
          <button
            onClick={() => switchLayout('random')}
            className={`p-1.5 rounded ${layout === 'random' ? 'bg-accent/20 text-accent' : 'text-text-dim hover:text-text'}`}
            title="Random"
          >
            <Map size={14} />
          </button>
        </div>
      </div>

      {/* Multi-select toggle */}
      <div className="absolute top-4 left-32 z-20">
        <button
          onClick={() => setMultiSelect(!multiSelect)}
          className={`flex items-center gap-1.5 px-2.5 py-1.5 bg-panel border border-border rounded-md text-xs transition-colors ${
            multiSelect ? 'border-accent text-accent' : 'text-text-dim hover:text-text'
          }`}
          title="Toggle multi-select"
        >
          <MousePointerClick size={14} />
          {multiSelect ? 'Multi' : 'Single'}
        </button>
      </div>

      {/* Minimap toggle */}
      <div className="absolute bottom-4 right-4 z-20">
        <button
          onClick={() => setShowMinimap(!showMinimap)}
          className={`p-2 bg-panel border border-border rounded-md transition-colors ${
            showMinimap ? 'border-accent text-accent' : 'text-text-dim hover:text-text'
          }`}
          title="Toggle minimap"
        >
          <Map size={16} />
        </button>
      </div>

      {/* Minimap */}
      {showMinimap && sigma && (
        <Minimap sigma={sigma} />
      )}

      {/* Context menu */}
      {contextMenu && (
        <div
          className="absolute z-30 bg-panel border border-border rounded-lg shadow-xl py-1 w-48"
          style={{ left: contextMenu.x, top: contextMenu.y }}
        >
          <button
            className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors"
            onClick={() => { setSelectedNode(contextMenu.nodeId); setContextMenu(null); }}
          >
            Select node
          </button>
          <button
            className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors"
            onClick={() => doExpand(contextMenu.nodeId)}
          >
            Expand neighbors
          </button>
          <button
            className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors"
            onClick={() => { fitView(); setContextMenu(null); }}
          >
            Fit to view
          </button>
          <div className="border-t border-border my-1" />
          <button
            className="w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors text-text-dim"
            onClick={() => setContextMenu(null)}
          >
            Cancel
          </button>
        </div>
      )}

      <LayoutForceAtlas2Control />
    </>
  );
}

function Minimap({ sigma }: { sigma: any }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || !sigma) return;

    const canvas = document.createElement('canvas');
    canvas.width = 160;
    canvas.height = 120;
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    function draw() {
      if (!ctx) return;
      ctx.fillStyle = '#16181f';
      ctx.fillRect(0, 0, 160, 120);

      const graph = sigma.getGraph();
      const camera = sigma.getCamera();
      const ratio = camera.ratio;

      graph.forEachNode((_id: string, attr: any) => {
        const x = (attr.x - camera.x) / ratio * 0.05 + 80;
        const y = (attr.y - camera.y) / ratio * 0.05 + 60;
        ctx.beginPath();
        ctx.arc(x, y, 1.5, 0, Math.PI * 2);
        ctx.fillStyle = attr.color || '#a78bfa';
        ctx.fill();
      });

      requestAnimationFrame(draw);
    }

    const raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, [sigma]);

  return (
    <div className="absolute bottom-14 right-4 w-40 h-32 bg-panel border border-border rounded-lg overflow-hidden z-20 shadow-lg">
      <div ref={containerRef} className="w-full h-full" />
    </div>
  );
}

export default function GraphScene() {
  return (
    <div className="flex-1 relative bg-bg overflow-hidden">
      <SigmaContainer
        style={{ position: 'absolute', inset: 0 }}
        settings={{
          defaultEdgeType: 'arrow',
          labelDensity: 0.07,
          labelGridCellSize: 60,
          labelRenderedSizeThreshold: 6,
          labelFont: 'system-ui, sans-serif',
          zIndex: true,
          enableEdgeEvents: true,
          allowInvalidContainer: true,
        }}
      >
        <GraphRenderer />
      </SigmaContainer>
    </div>
  );
}
