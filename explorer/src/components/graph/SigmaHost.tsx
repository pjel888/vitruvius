import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import { SigmaContainer, useLoadGraph, useRegisterEvents, useSigma } from '@react-sigma/core';
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

function SigmaInner({ controllerRef }: { controllerRef: React.RefObject<GraphController | null> }) {
  const loadGraph = useLoadGraph();
  const sigma = useSigma();
  const registerEvents = useRegisterEvents();

  const graphRef = useRef<Graph | null>(null);
  const selectedNodeRef = useRef<string | null>(null);
  const layoutTypeRef = useRef<'forceatlas2' | 'circular' | 'random'>('forceatlas2');
  const sigmaRef = useRef(sigma);
  sigmaRef.current = sigma;

  // Initialize graph once
  useEffect(() => {
    const graph = new Graph({ multi: true });
    graphRef.current = graph;
    loadGraph(graph);
    console.log('[SigmaHost] loadGraph called, graph nodes:', graph.nodes().length);
    // Force Sigma to recognize the graph
    setTimeout(() => {
      sigmaRef.current?.refresh();
      console.log('[SigmaHost] Initial refresh done, sigma exists:', !!sigmaRef.current);
    }, 50);

    // Expose controller API
    const controller: GraphController = {
      loadPerspective(nodes, edges) {
        if (!graphRef.current) return;
        const g = graphRef.current;

        // Build sets for diff
        const newNodeIds = new Set(nodes.map(n => n.id));
        const newEdgeIds = new Set(edges.map(e => e.id || `${e.source}-${e.type}-${e.target}`));

        // Remove old nodes not in new set
        g.forEachNode((id) => {
          if (!newNodeIds.has(id)) {
            g.dropNode(id);
          }
        });

        // Remove old edges not in new set
        g.forEachEdge((_id, attr, source, target) => {
          const edgeId = attr.id || `${source}-${attr.type}-${target}`;
          if (!newEdgeIds.has(edgeId)) {
            g.dropEdge(_id);
          }
        });

        // Add/update nodes
        nodes.forEach((n, i) => {
          if (g.hasNode(n.id)) {
            g.setNodeAttribute(n.id, 'label', n.label);
            g.setNodeAttribute(n.id, 'size', n.radius ?? 8);
            g.setNodeAttribute(n.id, 'color', NODE_COLORS[n.type] || '#a78bfa');
            g.setNodeAttribute(n.id, 'type', n.type);
          } else {
            g.addNode(n.id, {
              label: n.label,
              size: n.radius ?? 8,
              color: NODE_COLORS[n.type] || '#a78bfa',
              type: n.type,
              x: Math.cos((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
              y: Math.sin((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
            });
          }
        });

        // Add/update edges
        edges.forEach((e) => {
          if (!g.hasNode(e.source) || !g.hasNode(e.target)) return;
          const edgeId = e.id || `${e.source}-${e.type}-${e.target}`;
          if (g.hasEdge(edgeId)) {
            g.setEdgeAttribute(edgeId, 'size', 1.5);
            g.setEdgeAttribute(edgeId, 'color', EDGE_COLORS[e.type] || '#6b7280');
            g.setEdgeAttribute(edgeId, 'type', e.type);
          } else {
            g.addDirectedEdgeWithKey(edgeId, e.source, e.target, {
              size: 1.5,
              color: EDGE_COLORS[e.type] || '#6b7280',
              type: e.type,
            });
          }
        });

        // Apply layout
        controller.setLayout(layoutTypeRef.current);
        sigmaRef.current?.refresh();
        console.log('[SigmaHost] expandNode done, nodes:', graphRef.current?.nodes().length);
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
              type: n.type,
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
              type: e.type,
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
    };

    // Assign to ref
    if (controllerRef) {
      (controllerRef as React.MutableRefObject<GraphController>).current = controller;
    }

    // Register events
    registerEvents({
      clickNode: (e) => {
        if (e.node) controller.selectNode(e.node);
      },
      clickStage: () => {
        controller.selectNode(null);
      },
    });

    console.log('[SigmaHost] Controller initialized, graph ready');

    return () => {
      if (controllerRef) {
        (controllerRef as React.MutableRefObject<GraphController | null>).current = null;
      }
    };
  }, [loadGraph, registerEvents, controllerRef]);

  return null;
}

const SigmaHost = forwardRef<GraphController>((_, ref) => {
  const controllerRef = useRef<GraphController | null>(null);
  useImperativeHandle(ref, () => controllerRef.current!);

  return (
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
      <SigmaInner controllerRef={controllerRef} />
    </SigmaContainer>
  );
});

SigmaHost.displayName = 'SigmaHost';
export default SigmaHost;
