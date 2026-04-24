import { useEffect, useState } from 'react';
import { PanelRightClose, PanelRightOpen } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getEdgeDetail, getNode, tracePath } from '../api/graphApi';
import type { EdgeDetail, NodeDetail } from '../types';
import NodeInspector from './inspector/NodeInspector';
import EdgeInspector from './inspector/EdgeInspector';
import { getDisplayLabel } from '../utils/labels';

export default function InspectorRail() {
  const selectedNodeId = useSceneStore((s) => s.selectedNodeId);
  const selectedEdgeId = useSceneStore((s) => s.selectedEdgeId);
  const edges = useSceneStore((s) => s.edges);
  const inspectorOpen = useSceneStore((s) => s.inspectorOpen);
  const openInspector = useSceneStore((s) => s.openInspector);
  const closeInspector = useSceneStore((s) => s.closeInspector);
  const pathSourceId = useSceneStore((s) => s.pathSourceId);
  const pathTargetId = useSceneStore((s) => s.pathTargetId);
  const highlightedPath = useSceneStore((s) => s.highlightedPath);
  const setHighlightedPath = useSceneStore((s) => s.setHighlightedPath);

  const [nodeDetail, setNodeDetail] = useState<NodeDetail | null>(null);
  const [edgeDetail, setEdgeDetail] = useState<EdgeDetail | null>(null);
  const [nodeLoading, setNodeLoading] = useState(false);
  const [edgeLoading, setEdgeLoading] = useState(false);
  const [nodeError, setNodeError] = useState<string | null>(null);
  const [edgeError, setEdgeError] = useState<string | null>(null);
  const [pathError, setPathError] = useState<string | null>(null);

  useEffect(() => {
    if ((selectedNodeId || selectedEdgeId) && !inspectorOpen) {
      openInspector();
    }
  }, [selectedNodeId, selectedEdgeId, inspectorOpen, openInspector]);

  useEffect(() => {
    let cancelled = false;

    if (selectedNodeId) {
      setNodeLoading(true);
      setNodeError(null);
      setNodeDetail(null);
      getNode(selectedNodeId)
        .then((detail) => {
          if (!cancelled) setNodeDetail(detail);
        })
        .catch((error) => {
          if (!cancelled) setNodeError(error instanceof Error ? error.message : 'Failed to load node');
        })
        .finally(() => {
          if (!cancelled) setNodeLoading(false);
        });
    } else {
      setNodeDetail(null);
      setNodeError(null);
      setNodeLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, [selectedNodeId]);

  useEffect(() => {
    let cancelled = false;

    if (selectedEdgeId) {
      if (!edges.some((edge) => edge.id === selectedEdgeId)) {
        setEdgeLoading(false);
        setEdgeDetail(null);
        setEdgeError('Edge is not present in the current graph view.');
        return () => {
          cancelled = true;
        };
      }

      setEdgeLoading(true);
      setEdgeError(null);
      setEdgeDetail(null);
      getEdgeDetail(selectedEdgeId)
        .then((detail) => {
          if (!cancelled) setEdgeDetail(detail);
        })
        .catch((error) => {
          if (!cancelled) setEdgeError(error instanceof Error ? error.message : 'Failed to load edge');
        })
        .finally(() => {
          if (!cancelled) setEdgeLoading(false);
        });
    } else {
      setEdgeDetail(null);
      setEdgeError(null);
      setEdgeLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, [selectedEdgeId, edges]);

  useEffect(() => {
    setPathError(null);
  }, [pathSourceId, pathTargetId]);

  useEffect(() => {
    if (pathSourceId && pathTargetId && !highlightedPath) {
      tracePath(pathSourceId, pathTargetId)
        .then((data) => {
          if (data.paths && data.paths.length > 0) {
            const path = data.paths[0];
            setHighlightedPath({
              nodeIds: path.nodes.map((node: any) => node.id),
              edgeIds: path.edges.map((edge: any) => edge.id),
            });
            setPathError(null);
            return;
          }

          setPathError('No path is available between the selected nodes in the current graph view.');
        })
        .catch((error) => {
          setPathError(error instanceof Error ? error.message : 'Path tracing failed.');
        });
    }
  }, [pathSourceId, pathTargetId, highlightedPath, setHighlightedPath]);

  if (!inspectorOpen) {
    return (
      <button
        className="w-8 bg-panel border-l border-border flex items-center justify-center hover:bg-panel-hover transition-colors shrink-0"
        onClick={openInspector}
        title="Open inspector"
      >
        <PanelRightOpen size={14} className="text-text-dim" />
      </button>
    );
  }

  return (
    <div className="w-96 bg-panel border-l border-border flex flex-col shrink-0 overflow-hidden">
      <div className="px-3 py-2 border-b border-border flex items-center justify-between shrink-0">
        <span className="text-xs font-semibold uppercase tracking-wider text-text-dim">
          {selectedNodeId && nodeDetail
            ? getDisplayLabel(nodeDetail.node)
            : selectedEdgeId && edgeDetail
              ? edgeDetail.edge.type
              : 'Inspector'}
        </span>
        <button className="p-1 rounded hover:bg-panel-hover text-text-dim" onClick={closeInspector} title="Minimize">
          <PanelRightClose size={14} />
        </button>
      </div>

      <div className="flex-1 overflow-hidden">
        {!selectedNodeId && !selectedEdgeId ? (
          <div className="h-full flex flex-col items-center justify-center p-6 text-center">
            <div className="text-sm text-text-dim mb-2">Select a node to see details.</div>
            {pathError && <div className="text-xs text-rose-300 max-w-xs">{pathError}</div>}
            <div className="text-xs text-text-dim">Click empty space to clear.</div>
          </div>
        ) : selectedNodeId && nodeLoading ? (
          <div className="h-full flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-border border-t-accent rounded-full animate-spin" />
          </div>
        ) : selectedNodeId && nodeError ? (
          <div className="h-full flex flex-col items-center justify-center p-6 text-center gap-2">
            <div className="text-sm text-text">Node details unavailable.</div>
            <div className="text-xs text-text-dim">{nodeError}</div>
          </div>
        ) : selectedNodeId && nodeDetail ? (
          <div className="flex flex-col h-full">
            {pathError && (
              <div className="mx-4 mt-3 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-xs text-rose-100">
                {pathError}
              </div>
            )}
            <div className="min-h-0 flex-1">
              <NodeInspector detail={nodeDetail} />
            </div>
          </div>
        ) : selectedEdgeId && edgeLoading ? (
          <div className="h-full flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-border border-t-accent rounded-full animate-spin" />
          </div>
        ) : selectedEdgeId && edgeError ? (
          <div className="h-full flex flex-col items-center justify-center p-6 text-center gap-2">
            <div className="text-sm text-text">Edge details unavailable.</div>
            <div className="text-xs text-text-dim">{edgeError}</div>
          </div>
        ) : selectedEdgeId && edgeDetail ? (
          <EdgeInspector detail={edgeDetail} />
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-border border-t-accent rounded-full animate-spin" />
          </div>
        )}
      </div>
    </div>
  );
}
