import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronDown, FolderTree, Filter } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getTaxonomy } from '../api/graphApi';
import type { TaxonomyNode } from '../types';
import FiltersPanel from './explorer-rail/FiltersPanel';

function TreeItem({ node, depth = 0, navigate }: { node: TaxonomyNode; depth?: number; navigate: ReturnType<typeof useNavigate> }) {
  const [open, setOpen] = useState(depth < 1);
  const hasChildren = node.children.length > 0;

  async function onClick() {
    navigate(`/explore?perspective=taxonomy&node=${encodeURIComponent(node.id)}`);
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
            <TreeItem key={child.id} node={child} depth={depth + 1} navigate={navigate} />
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
  { key: 'evidence_span', label: 'Evidence', color: 'bg-sky-500' },
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

const COLOR_SCHEMES = [
  { key: 'default', label: 'Default' },
  { key: 'pastel', label: 'Pastel' },
  { key: 'vibrant', label: 'Vibrant' },
  { key: 'monochrome', label: 'Monochrome' },
];

const SIZE_OPTIONS: Array<{ key: 'uniform' | 'confidence' | 'degree'; label: string }> = [
  { key: 'uniform', label: 'Uniform' },
  { key: 'confidence', label: 'By Confidence' },
  { key: 'degree', label: 'By Connectivity' },
];

export default function ExplorerRail() {
  const navigate = useNavigate();
  const [roots, setRoots] = useState<TaxonomyNode[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [taxonomyLoading, setTaxonomyLoading] = useState(false);
  const [taxonomyError, setTaxonomyError] = useState<string | null>(null);
  const open = useSceneStore(s => s.explorerOpen);
  const nodes = useSceneStore(s => s.nodes);
  const pinnedNodeIds = useSceneStore(s => s.pinnedNodeIds);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);

  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const setVisibleNodeTypes = useSceneStore(s => s.setVisibleNodeTypes);
  const setVisibleEdgeTypes = useSceneStore(s => s.setVisibleEdgeTypes);
  const colorScheme = useSceneStore(s => s.colorScheme);
  const setColorScheme = useSceneStore(s => s.setColorScheme);
  const sizeBy = useSceneStore(s => s.sizeBy);
  const setSizeBy = useSceneStore(s => s.setSizeBy);

  useEffect(() => {
    let cancelled = false;
    setTaxonomyLoading(true);
    setTaxonomyError(null);
    getTaxonomy()
      .then((nextRoots) => {
        if (!cancelled) setRoots(nextRoots);
      })
      .catch((error) => {
        if (!cancelled) setTaxonomyError(error instanceof Error ? error.message : 'Failed to load taxonomy');
      })
      .finally(() => {
        if (!cancelled) setTaxonomyLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  if (!open) return null;

  const pinnedNodes = useMemo(
    () => pinnedNodeIds
      .map((id) => nodes.find((node) => node.id === id))
      .filter((node): node is NonNullable<typeof node> => Boolean(node)),
    [pinnedNodeIds, nodes]
  );

  function toggleNodeType(key: string) {
    setVisibleNodeTypes(new Set(
      visibleNodeTypes.has(key)
        ? [...visibleNodeTypes].filter(k => k !== key)
        : [...visibleNodeTypes, key]
    ));
  }

  function toggleEdgeType(key: string) {
    setVisibleEdgeTypes(new Set(
      visibleEdgeTypes.has(key)
        ? [...visibleEdgeTypes].filter(k => k !== key)
        : [...visibleEdgeTypes, key]
    ));
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
        <FiltersPanel
          colorScheme={colorScheme}
          sizeBy={sizeBy}
          visibleNodeTypes={visibleNodeTypes}
          visibleEdgeTypes={visibleEdgeTypes}
          colorSchemes={COLOR_SCHEMES}
          sizeOptions={SIZE_OPTIONS}
          nodeTypes={NODE_TYPES}
          edgeTypes={EDGE_TYPES}
          onSelectColorScheme={setColorScheme}
          onSelectSizeBy={setSizeBy}
          onToggleNodeType={toggleNodeType}
          onToggleEdgeType={toggleEdgeType}
        />
      )}

      {pinnedNodes.length > 0 && (
        <div className="border-b border-border px-3 py-2">
          <div className="text-xs font-semibold uppercase tracking-wider text-text-dim mb-2">Pinned</div>
          <div className="space-y-1">
            {pinnedNodes.map((node) => (
              <button
                key={node.id}
                onClick={() => setSelectedNode(node.id)}
                className="w-full text-left rounded-md px-2 py-1.5 text-sm hover:bg-panel-hover transition-colors"
              >
                <div className="truncate text-text">{node.label}</div>
                <div className="text-xs text-text-dim truncate">{node.type}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto py-1">
        {taxonomyLoading ? (
          <div className="px-3 py-3 text-sm text-text-dim">Loading taxonomy…</div>
        ) : taxonomyError ? (
          <div className="px-3 py-3 space-y-2">
            <div className="text-sm text-text">Taxonomy unavailable.</div>
            <div className="text-xs text-text-dim">{taxonomyError}</div>
          </div>
        ) : roots.length === 0 ? (
          <div className="px-3 py-3 text-sm text-text-dim">No taxonomy data available.</div>
        ) : (
          roots.map(root => (
            <TreeItem key={root.id} node={root} navigate={navigate} />
          ))
        )}
      </div>
    </div>
  );
}
