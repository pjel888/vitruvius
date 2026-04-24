import { useEffect, useState } from 'react';
import { PanelRightClose, PanelRightOpen } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getEdgeDetail, getNode, tracePath } from '../api/graphApi';
import type { EdgeDetail, NodeDetail } from '../types';
import NodeInspector from './inspector/NodeInspector';
import EdgeInspector from './inspector/EdgeInspector';
import { getDisplayLabel } from '../utils/labels';

interface NodeDetailState {
  id: string | null;
  detail: NodeDetail | null;
  error: string | null;
}

interface EdgeDetailState {
  id: string | null;
  detail: EdgeDetail | null;
  error: string | null;
}

interface PathErrorState {
  key: string | null;
  error: string | null;
}

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

  const [nodeState, setNodeState] = useState<NodeDetailState>({ id: null, detail: null, error: null });
  const [edgeState, setEdgeState] = useState<EdgeDetailState>({ id: null, detail: null, error: null });
  const [pathErrorState, setPathErrorState] = useState<PathErrorState>({ key: null, error: null });

  const selectedEdgeExists = selectedEdgeId ? edges.some((edge) => edge.id === selectedEdgeId) : false;
  const pathKey = pathSourceId && pathTargetId ? `${pathSourceId}->${pathTargetId}` : null;
  const nodeDetail = selectedNodeId && nodeState.id === selectedNodeId ? nodeState.detail : null;
  const nodeError = selectedNodeId && nodeState.id === selectedNodeId ? nodeState.error : null;
  const nodeLoading = Boolean(selectedNodeId && nodeState.id !== selectedNodeId);
  const edgeDetail = selectedEdgeId && edgeState.id === selectedEdgeId ? edgeState.detail : null;
  const edgeError = selectedEdgeId && !selectedEdgeExists
    ? 'Edge is not present in the current graph view.'
    : selectedEdgeId && edgeState.id === selectedEdgeId
      ? edgeState.error
      : null;
  const edgeLoading = Boolean(selectedEdgeId && selectedEdgeExists && edgeState.id !== selectedEdgeId);
  const pathError = pathKey && pathErrorState.key === pathKey ? pathErrorState.error : null;

  useEffect(() => {
    if ((selectedNodeId || selectedEdgeId) && !inspectorOpen) {
      openInspector();
    }
  }, [selectedNodeId, selectedEdgeId, inspectorOpen, openInspector]);

  useEffect(() => {
    let cancelled = false;

    if (!selectedNodeId) return;
    const nodeId = selectedNodeId;
    getNode(nodeId)
      .then((detail) => {
        if (!cancelled) setNodeState({ id: nodeId, detail, error: null });
      })
      .catch((error) => {
        if (!cancelled) {
          setNodeState({
            id: nodeId,
            detail: null,
            error: error instanceof Error ? error.message : 'Failed to load node',
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedNodeId]);

  useEffect(() => {
    let cancelled = false;

    if (!selectedEdgeId || !selectedEdgeExists) return;
    const edgeId = selectedEdgeId;
    getEdgeDetail(edgeId)
      .then((detail) => {
        if (!cancelled) setEdgeState({ id: edgeId, detail, error: null });
      })
      .catch((error) => {
        if (!cancelled) {
          setEdgeState({
            id: edgeId,
            detail: null,
            error: error instanceof Error ? error.message : 'Failed to load edge',
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedEdgeId, selectedEdgeExists]);

  useEffect(() => {
    if (!pathSourceId || !pathTargetId || !pathKey || highlightedPath) return;
    let cancelled = false;

    tracePath(pathSourceId, pathTargetId)
        .then((data) => {
          if (cancelled) return;
          if (data.paths && data.paths.length > 0) {
            const path = data.paths[0];
            setHighlightedPath({
              nodeIds: path.nodes.map((node) => node.id),
              edgeIds: path.edges.map((edge) => edge.id),
            });
            setPathErrorState({ key: pathKey, error: null });
            return;
          }

          setPathErrorState({ key: pathKey, error: 'No path is available between the selected nodes in the current graph view.' });
        })
        .catch((error) => {
          if (!cancelled) {
            setPathErrorState({ key: pathKey, error: error instanceof Error ? error.message : 'Path tracing failed.' });
          }
        });

    return () => {
      cancelled = true;
    };
  }, [pathSourceId, pathTargetId, pathKey, highlightedPath, setHighlightedPath]);

  if (!inspectorOpen) {
    return (
      <button
        className="w-10 kg-panel border-l border-border flex items-center justify-center hover:bg-panel-hover transition-colors shrink-0"
        onClick={openInspector}
        title="Open inspector"
        aria-label="Open inspector"
      >
        <PanelRightOpen size={14} className="text-text-dim" />
      </button>
    );
  }

  return (
    <div className="kg-panel w-96 border-l border-border flex flex-col shrink-0 overflow-hidden">
      <div className="px-4 py-3 border-b border-border flex items-center justify-between shrink-0">
        <span className="max-w-[18rem] truncate text-xs font-semibold uppercase tracking-[0.2em] text-text-dim">
          {selectedNodeId && nodeDetail
            ? getDisplayLabel(nodeDetail.node)
            : selectedEdgeId && edgeDetail
              ? edgeDetail.edge.type
              : 'Inspector'}
        </span>
        <button className="kg-control p-2 rounded-xl text-text-dim" onClick={closeInspector} title="Minimize" aria-label="Minimize inspector">
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
