import { useRef, useEffect } from 'react';
import { Maximize } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective } from '../api/graphApi';
import VisNetworkHost, { type GraphController } from './graph/VisNetworkHost';

export default function GraphScene() {
  const controllerRef = useRef<GraphController>(null);

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setLoading = useSceneStore(s => s.setLoading);
  const setGraphData = useSceneStore(s => s.setGraphData);

  const loading = useSceneStore(s => s.loading);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);

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
    }
  }, [nodes, edges]);

  // Sync selection to graph
  useEffect(() => {
    controllerRef.current?.selectNode(selectedNodeId);
  }, [selectedNodeId]);

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

      {/* Zoom controls */}
      <div className="absolute bottom-4 left-4 flex flex-col gap-1 z-20">
        <button
          onClick={() => controllerRef.current?.fitView()}
          className="p-2 bg-panel border border-border rounded-md hover:border-accent text-text-dim hover:text-text transition-colors"
          title="Fit to view"
        >
          <Maximize size={16} />
        </button>
      </div>
    </div>
  );
}
