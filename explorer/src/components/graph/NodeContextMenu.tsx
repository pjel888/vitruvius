import { useRef, useEffect } from 'react';
import { Expand, Focus, EyeOff, Maximize } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import { expandNode } from '../../api/graphApi';
import type { GraphController } from './VisNetworkHost';

interface NodeContextMenuProps {
  controllerRef: React.RefObject<GraphController | null>;
}

export default function NodeContextMenu({ controllerRef }: NodeContextMenuProps) {
  const nodeId = useSceneStore(s => s.contextMenuNodeId);
  const pos = useSceneStore(s => s.contextMenuPos);
  const closeContextMenu = useSceneStore(s => s.closeContextMenu);
  const addExpandedNodeIds = useSceneStore(s => s.addExpandedNodeIds);
  const mergeGraphData = useSceneStore(s => s.mergeGraphData);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (!menuRef.current?.contains(e.target as Node)) {
        closeContextMenu();
      }
    }
    window.addEventListener('mousedown', onClick);
    return () => window.removeEventListener('mousedown', onClick);
  }, [closeContextMenu]);

  // Close on Escape
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') closeContextMenu();
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [closeContextMenu]);

  if (!nodeId || !pos) return null;

  const handleExpand = async () => {
    closeContextMenu();
    try {
      const data = await expandNode(nodeId, ['HAS_CHILD'], { direction: 'out', depth: 4 });
      addExpandedNodeIds(data.nodes.map((node) => node.id));
      mergeGraphData(data.nodes, data.edges);
      controllerRef.current?.mergeNodesEdges(data.nodes, data.edges);
    } catch (err) {
      console.error('Expand failed:', err);
    }
  };

  const handleExpandDirectRelationships = async () => {
    closeContextMenu();
    try {
      const data = await expandNode(nodeId, undefined, { direction: 'both', depth: 1 });
      addExpandedNodeIds(data.nodes.map((node) => node.id));
      mergeGraphData(data.nodes, data.edges);
      controllerRef.current?.mergeNodesEdges(data.nodes, data.edges);
    } catch (err) {
      console.error('Direct relationship expansion failed:', err);
    }
  };

  const handleFocusSubgraph = () => {
    closeContextMenu();
    controllerRef.current?.focusSubgraph(nodeId);
  };

  const handleHide = () => {
    closeContextMenu();
    controllerRef.current?.hideNode(nodeId);
  };

  const handleShowAll = () => {
    closeContextMenu();
    controllerRef.current?.showAll();
  };

  return (
    <div
      ref={menuRef}
      className="fixed z-50 bg-panel border border-border rounded-md shadow-lg py-1 min-w-[160px]"
      style={{ left: pos.x, top: pos.y }}
    >
      <button
        onClick={handleExpand}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-text hover:bg-panel-hover transition-colors text-left"
      >
        <Expand size={14} className="text-text-dim" />
        Expand child tree
      </button>
      <button
        onClick={handleExpandDirectRelationships}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-text hover:bg-panel-hover transition-colors text-left"
      >
        <Expand size={14} className="text-text-dim" />
        Expand direct relationships
      </button>
      <button
        onClick={handleFocusSubgraph}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-text hover:bg-panel-hover transition-colors text-left"
      >
        <Focus size={14} className="text-text-dim" />
        Focus 1-hop
      </button>
      <button
        onClick={handleHide}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-text hover:bg-panel-hover transition-colors text-left"
      >
        <EyeOff size={14} className="text-text-dim" />
        Hide node
      </button>
      <div className="border-t border-border my-1" />
      <button
        onClick={handleShowAll}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-text hover:bg-panel-hover transition-colors text-left"
      >
        <Maximize size={14} className="text-text-dim" />
        Show all
      </button>
    </div>
  );
}
