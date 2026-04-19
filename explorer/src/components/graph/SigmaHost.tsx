import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import Sigma from 'sigma';
import Graph from 'graphology';
import { circular } from 'graphology-layout';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import type { GraphNode, GraphEdge } from '../../types';

export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (id: string | null) => void;
  expandNode: (id: string, neighbors: { nodes: GraphNode[]; edges: GraphEdge[] }) => void;
  setLayout: (type: 'forceatlas2' | 'circular' | 'random') => void;
  zoomIn: () => void;
  zoomOut: () => void;
  fitView: () => void;
  getDebugInfo: () => Record<string, any>;
}

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

const SigmaHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<Graph | null>(null);
  const controllerRef = useRef<GraphController | null>(null);
  const selectedNodeRef = useRef<string | null>(null);
  const layoutTypeRef = useRef<'forceatlas2' | 'circular' | 'random'>('forceatlas2');

  useImperativeHandle(ref, () => controllerRef.current!);

  useEffect(() => {
    if (!containerRef.current) {
      console.error('[SigmaHost] Container ref is null');
      return;
    }

    const rect = containerRef.current.getBoundingClientRect();
    console.log('[SigmaHost] Container dimensions:', rect.width, 'x', rect.height);

    if (rect.width === 0 || rect.height === 0) {
      console.error('[SigmaHost] Container has zero dimensions!');
    }

    const graph = new Graph({ multi: true });
    graphRef.current = graph;

    const sigma = new Sigma(graph, containerRef.current, {
      defaultEdgeType: 'arrow',
      labelDensity: 0.07,
      labelGridCellSize: 60,
      labelRenderedSizeThreshold: 6,
      labelFont: 'system-ui, sans-serif',
      zIndex: true,
      enableEdgeEvents: true,
      allowInvalidContainer: true,
    });
    sigmaRef.current = sigma;

    console.log('[SigmaHost] Sigma created, canvas count:', sigma.getCanvases ? Object.keys(sigma.getCanvases()).length : 'N/A');

    // Register click events
    sigma.on('clickNode', (e) => {
      if (e.node) {
        controller.selectNode(e.node);
      }
    });
    sigma.on('clickStage', () => {
      controller.selectNode(null);
    });
    sigma.on('clickEdge', (e) => {
      const edge = graph.getEdgeAttributes(e.edge);
      console.log('Edge clicked:', edge);
    });

    // Expose controller API
    const controller: GraphController = {
      loadPerspective(nodes, edges) {
        if (!graphRef.current) return;
        const g = graphRef.current;

        console.log('[SigmaHost] loadPerspective called with', nodes.length, 'nodes,', edges.length, 'edges');

        // Clear existing
        g.clear();

        // Add nodes
        nodes.forEach((n, i) => {
          if (g.hasNode(n.id)) return;
          g.addNode(n.id, {
            label: n.label,
            size: n.radius ?? 8,
            color: NODE_COLORS[n.type] || '#a78bfa',
            nodeType: n.type,
            x: Math.cos((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
            y: Math.sin((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
          });
        });

        // Add edges
        edges.forEach((e) => {
          if (!g.hasNode(e.source) || !g.hasNode(e.target)) return;
          const edgeId = e.id || `${e.source}-${e.type}-${e.target}`;
          g.addDirectedEdgeWithKey(edgeId, e.source, e.target, {
            size: 1.5,
            color: EDGE_COLORS[e.type] || '#6b7280',
            edgeType: e.type,
          });
        });

        console.log('[SigmaHost] Graph now has', g.nodes().length, 'nodes,', g.edges().length, 'edges');

        // Apply layout
        controller.setLayout(layoutTypeRef.current);
        sigmaRef.current?.refresh();
        setTimeout(() => controller.fitView(), 100);
      },

      selectNode(id) {
        selectedNodeRef.current = id;
        if (!graphRef.current || !sigmaRef.current) return;
        graphRef.current.forEachNode((nodeId) => {
          graphRef.current!.setNodeAttribute(nodeId, 'highlighted', nodeId === id);
        });
        sigmaRef.current.refresh();
      },

      expandNode(_id, { nodes: newNodes, edges: newEdges }) {
        if (!graphRef.current) return;
        const g = graphRef.current;
        newNodes.forEach((n) => {
          if (!g.hasNode(n.id)) {
            g.addNode(n.id, {
              label: n.label,
              size: n.radius ?? 8,
              color: NODE_COLORS[n.type] || '#a78bfa',
              nodeType: n.type,
            });
          }
        });
        newEdges.forEach((e) => {
          if (!g.hasNode(e.source) || !g.hasNode(e.target)) return;
          const edgeId = e.id || `${e.source}-${e.type}-${e.target}`;
          if (!g.hasEdge(edgeId)) {
            g.addDirectedEdgeWithKey(edgeId, e.source, e.target, {
              size: 1.5,
              color: EDGE_COLORS[e.type] || '#6b7280',
              edgeType: e.type,
            });
          }
        });
        controller.setLayout(layoutTypeRef.current);
        sigmaRef.current?.refresh();
      },

      setLayout(type) {
        layoutTypeRef.current = type;
        if (!graphRef.current) return;
        const g = graphRef.current;
        if (type === 'circular') {
          circular.assign(g, { scale: 200 });
        } else if (type === 'random') {
          g.forEachNode((node) => {
            g.setNodeAttribute(node, 'x', (Math.random() - 0.5) * 600);
            g.setNodeAttribute(node, 'y', (Math.random() - 0.5) * 600);
          });
        } else if (type === 'forceatlas2') {
          try {
            forceAtlas2.assign(g, { iterations: 100 });
          } catch (e) {
            console.error('ForceAtlas2 failed:', e);
          }
        }
        sigmaRef.current?.refresh();
      },

      zoomIn() {
        const cam = sigmaRef.current?.getCamera();
        if (cam) cam.animate({ ratio: cam.ratio / 1.5 }, { duration: 200 });
      },

      zoomOut() {
        const cam = sigmaRef.current?.getCamera();
        if (cam) cam.animate({ ratio: cam.ratio * 1.5 }, { duration: 200 });
      },

      fitView() {
        sigmaRef.current?.getCamera().animatedReset({ duration: 600 });
      },

      getDebugInfo() {
        const canvas = containerRef.current?.querySelector('canvas');
        return {
          graphNodes: graphRef.current?.nodes().length ?? 0,
          graphEdges: graphRef.current?.edges().length ?? 0,
          sigmaExists: !!sigmaRef.current,
          containerExists: !!containerRef.current,
          canvasExists: !!canvas,
          canvasWidth: canvas?.width ?? 0,
          canvasHeight: canvas?.height ?? 0,
          containerWidth: containerRef.current?.clientWidth ?? 0,
          containerHeight: containerRef.current?.clientHeight ?? 0,
        };
      },
    };

    controllerRef.current = controller;

    console.log('[SigmaHost] Raw Sigma initialized');

    return () => {
      sigma.kill();
      sigmaRef.current = null;
      controllerRef.current = null;
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
    />
  );
});

SigmaHost.displayName = 'SigmaHost';
export default SigmaHost;
