import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import { Network, DataSet } from 'vis-network/standalone';
import type { GraphNode, GraphEdge } from '../../types';

export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (id: string | null) => void;
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

const VisNetworkHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const nodesRef = useRef<DataSet<any> | null>(null);
  const edgesRef = useRef<DataSet<any> | null>(null);

  useImperativeHandle(ref, () => ({
    loadPerspective(nodes, edges) {
      if (!containerRef.current) return;

      const visNodes = nodes.map((n) => ({
        id: n.id,
        label: n.label,
        color: {
          background: NODE_COLORS[n.type] || '#a78bfa',
          border: '#ffffff',
          highlight: { background: NODE_COLORS[n.type] || '#a78bfa', border: '#ffffff' },
        },
        size: n.radius ?? 8,
        group: n.type,
        title: `<b>${n.label}</b><br/>${n.type}`,
      }));

      const visEdges = edges.map((e) => ({
        from: e.source,
        to: e.target,
        label: e.type,
        arrows: 'to',
        color: { color: '#94a3b8', opacity: 0.6 },
        font: { color: '#7a7f8a', size: 10 },
      }));

      if (networkRef.current && nodesRef.current && edgesRef.current) {
        nodesRef.current.clear();
        nodesRef.current.add(visNodes);
        edgesRef.current.clear();
        edgesRef.current.add(visEdges);
      } else {
        nodesRef.current = new DataSet(visNodes);
        edgesRef.current = new DataSet(visEdges as any);

        networkRef.current = new Network(
          containerRef.current,
          { nodes: nodesRef.current, edges: edgesRef.current },
          {
            nodes: {
              shape: 'dot',
              font: { size: 12, color: '#e2e8f0', face: 'system-ui, sans-serif' },
              borderWidth: 2,
              borderWidthSelected: 3,
              shadow: { enabled: true, color: 'rgba(0,0,0,0.3)', size: 8 },
            },
            edges: {
              width: 1,
              smooth: { enabled: true, type: 'continuous', roundness: 0.5 },
            },
            physics: {
              forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 100,
                springConstant: 0.08,
              },
              maxVelocity: 50,
              solver: 'forceAtlas2Based',
              timestep: 0.35,
              stabilization: { iterations: 150 },
            },
            interaction: {
              hover: true,
              tooltipDelay: 200,
              hideEdgesOnDrag: false,
            },
          }
        );
      }
    },

    selectNode(id) {
      if (id && networkRef.current) {
        networkRef.current.selectNodes([id]);
      } else if (networkRef.current) {
        networkRef.current.unselectAll();
      }
    },

    fitView() {
      networkRef.current?.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
    },
  }));

  useEffect(() => {
    return () => {
      networkRef.current?.destroy();
      networkRef.current = null;
      nodesRef.current = null;
      edgesRef.current = null;
    };
  }, []);

  return <div ref={containerRef} style={{ position: 'absolute', inset: 0 }} />;
});

VisNetworkHost.displayName = 'VisNetworkHost';
export default VisNetworkHost;
