import { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, FolderTree } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getTaxonomy, getNodesForPerspective } from '../api/graphApi';
import type { TaxonomyNode } from '../types';

function TreeItem({ node, depth = 0 }: { node: TaxonomyNode; depth?: number }) {
  const [open, setOpen] = useState(depth < 1);
  const hasChildren = node.children.length > 0;
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);

  async function onClick() {
    // Filter graph to concepts under this branch
    const { nodes, edges } = await getNodesForPerspective('default');
    // For demo: just show all for now, in real app would filter by descendant
    setGraphData(nodes, edges);
    setSelectedNode(null);
  }

  return (
    <div>
      <div
        className="flex items-center gap-1.5 px-3 py-1.5 text-sm cursor-pointer hover:bg-panel-hover transition-colors select-none"
        style={{ paddingLeft: `${12 + depth * 16}px` }}
        onClick={onClick}
      >
        <button
          className={`w-4 h-4 flex items-center justify-center text-text-dim shrink-0 ${!hasChildren ? 'invisible' : ''}`}
          onClick={e => { e.stopPropagation(); setOpen(!open); }}
        >
          {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        </button>
        <span className={`w-2.5 h-2.5 rounded-sm shrink-0 ${
          node.kind === 'taxonomy' ? 'bg-node-taxonomy' :
          node.kind === 'topic' ? 'bg-node-topic' : 'bg-node-subtopic'
        }`} />
        <span className="truncate">{node.label}</span>
        {node.conceptCount > 0 && (
          <span className="text-xs text-text-dim ml-auto shrink-0">{node.conceptCount}</span>
        )}
      </div>
      {hasChildren && open && (
        <div>
          {node.children.map(child => (
            <TreeItem key={child.id} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function ExplorerRail() {
  const [roots, setRoots] = useState<TaxonomyNode[]>([]);
  const open = useSceneStore(s => s.explorerOpen);

  useEffect(() => {
    getTaxonomy().then(setRoots);
  }, []);

  if (!open) return null;

  return (
    <div className="w-72 bg-panel border-r border-border flex flex-col shrink-0 overflow-hidden">
      <div className="px-3 py-2.5 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-text-dim">
          <FolderTree size={14} />
          Taxonomy
        </div>
      </div>
      <div className="flex-1 overflow-y-auto py-1">
        {roots.map(root => (
          <TreeItem key={root.id} node={root} />
        ))}
      </div>
    </div>
  );
}
