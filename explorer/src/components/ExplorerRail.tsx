import { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, FolderTree, Filter } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getTaxonomy } from '../api/graphApi';
import type { TaxonomyNode } from '../types';

function TreeItem({ node, depth = 0 }: { node: TaxonomyNode; depth?: number }) {
  const [open, setOpen] = useState(depth < 1);
  const hasChildren = node.children.length > 0;
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);

  async function onClick() {
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

const NODE_TYPES = [
  { key: 'taxonomy', label: 'Taxonomy', color: 'bg-node-taxonomy' },
  { key: 'topic', label: 'Topic', color: 'bg-node-topic' },
  { key: 'subtopic', label: 'Subtopic', color: 'bg-node-subtopic' },
  { key: 'concept', label: 'Concept', color: 'bg-node-concept' },
  { key: 'rule', label: 'Rule', color: 'bg-node-rule' },
  { key: 'definition', label: 'Definition', color: 'bg-node-definition' },
  { key: 'procedure', label: 'Procedure', color: 'bg-node-procedure' },
  { key: 'exception', label: 'Exception', color: 'bg-node-exception' },
];

const EDGE_TYPES = [
  { key: 'HAS_CHILD', label: 'HAS_CHILD' },
  { key: 'BELONGS_TO', label: 'BELONGS_TO' },
  { key: 'RELATED_TO', label: 'RELATED_TO' },
  { key: 'DEPENDS_ON', label: 'DEPENDS_ON' },
  { key: 'DEFINED_BY', label: 'DEFINED_BY' },
  { key: 'REQUIRES', label: 'REQUIRES' },
  { key: 'SUPPORTED_BY', label: 'SUPPORTED_BY' },
];

export default function ExplorerRail() {
  const [roots, setRoots] = useState<TaxonomyNode[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const open = useSceneStore(s => s.explorerOpen);

  const [visibleNodeTypes, setVisibleNodeTypes] = useState<Set<string>>(new Set(NODE_TYPES.map(n => n.key)));
  const [visibleEdgeTypes, setVisibleEdgeTypes] = useState<Set<string>>(new Set(EDGE_TYPES.map(e => e.key)));

  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);

  useEffect(() => {
    getTaxonomy().then(setRoots);
  }, []);

  // Apply filters to graph data
  useEffect(() => {
    const filteredNodes = nodes.filter(n => visibleNodeTypes.has(n.type));
    const nodeIds = new Set(filteredNodes.map(n => n.id));
    edges.filter(e => visibleEdgeTypes.has(e.type) && nodeIds.has(e.source) && nodeIds.has(e.target));
    // We don't call setGraphData here to avoid infinite loop; filters are visual only for now
    // In full implementation, we'd re-render the graph with filtered data
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [visibleNodeTypes, visibleEdgeTypes, nodes, edges]);

  if (!open) return null;

  function toggleNodeType(key: string) {
    setVisibleNodeTypes(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  function toggleEdgeType(key: string) {
    setVisibleEdgeTypes(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  return (
    <div className="w-72 bg-panel border-r border-border flex flex-col shrink-0 overflow-hidden">
      <div className="px-3 py-2.5 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-text-dim">
          <FolderTree size={14} />
          Taxonomy
        </div>
        <button
          className={`p-1 rounded hover:bg-panel-hover transition-colors ${showFilters ? 'text-accent' : 'text-text-dim'}`}
          onClick={() => setShowFilters(!showFilters)}
          title="Toggle filters"
        >
          <Filter size={14} />
        </button>
      </div>

      {showFilters && (
        <div className="px-3 py-2 border-b border-border space-y-3 max-h-64 overflow-y-auto">
          <div>
            <div className="text-xs font-medium text-text-dim mb-1.5">Node types</div>
            <div className="space-y-1">
              {NODE_TYPES.map(nt => (
                <label key={nt.key} className="flex items-center gap-2 text-sm cursor-pointer hover:text-text transition-colors">
                  <input
                    type="checkbox"
                    checked={visibleNodeTypes.has(nt.key)}
                    onChange={() => toggleNodeType(nt.key)}
                    className="rounded border-border accent-accent"
                  />
                  <span className={`w-2 h-2 rounded-full ${nt.color}`} />
                  <span className="truncate">{nt.label}</span>
                </label>
              ))}
            </div>
          </div>
          <div>
            <div className="text-xs font-medium text-text-dim mb-1.5">Edge types</div>
            <div className="space-y-1">
              {EDGE_TYPES.map(et => (
                <label key={et.key} className="flex items-center gap-2 text-sm cursor-pointer hover:text-text transition-colors">
                  <input
                    type="checkbox"
                    checked={visibleEdgeTypes.has(et.key)}
                    onChange={() => toggleEdgeType(et.key)}
                    className="rounded border-border accent-accent"
                  />
                  <span className="truncate">{et.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto py-1">
        {roots.map(root => (
          <TreeItem key={root.id} node={root} />
        ))}
      </div>
    </div>
  );
}
