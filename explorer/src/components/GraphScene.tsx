import { useEffect, useCallback } from 'react';
import { SigmaContainer, useLoadGraph, useRegisterEvents, useSigma } from '@react-sigma/core';
import { LayoutForceAtlas2Control, useLayoutForceAtlas2 } from '@react-sigma/layout-forceatlas2';
import Graph from 'graphology';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective } from '../api/graphApi';

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

function GraphLoader() {
  const loadGraph = useLoadGraph();
  const { assign } = useLayoutForceAtlas2();
  const sigma = useSigma();
  const registerEvents = useRegisterEvents();

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);

  const refresh = useCallback(async () => {
    setLoading(true);
    const { nodes, edges } = await getNodesForPerspective(perspectiveId);
    setGraphData(nodes, edges);

    const graph = new Graph();
    nodes.forEach(n => {
      graph.addNode(n.id, {
        label: n.label,
        size: n.radius ?? 8,
        color: NODE_COLORS[n.type] || '#a78bfa',
        type: n.type,
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

    loadGraph(graph);
    assign();
    setLoading(false);
  }, [perspectiveId, loadGraph, assign, setGraphData, setLoading]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    registerEvents({
      clickNode: (e) => {
        if (e.node) setSelectedNode(e.node);
      },
      clickStage: () => {
        setSelectedNode(null);
      },
    });
  }, [registerEvents, setSelectedNode]);

  // Highlight selected node
  useEffect(() => {
    if (!sigma) return;
    const graph = sigma.getGraph();
    graph.forEachNode((id) => {
      graph.setNodeAttribute(id, 'highlighted', id === selectedNodeId);
    });
    sigma.refresh();
  }, [selectedNodeId, sigma]);

  return <LayoutForceAtlas2Control />;
}

export default function GraphScene() {
  const loading = useSceneStore(s => s.loading);

  return (
    <div className="flex-1 relative bg-bg overflow-hidden">
      <SigmaContainer
        style={{ width: '100%', height: '100%' }}
        settings={{
          defaultEdgeType: 'arrow',
          labelDensity: 0.07,
          labelGridCellSize: 60,
          labelRenderedSizeThreshold: 6,
          labelFont: 'system-ui, sans-serif',
          zIndex: true,
        }}
      >
        <GraphLoader />
      </SigmaContainer>

      {loading && (
        <div className="absolute inset-0 bg-bg/80 flex items-center justify-center z-10">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
            <span className="text-sm text-text-dim">Loading graph...</span>
          </div>
        </div>
      )}
    </div>
  );
}
