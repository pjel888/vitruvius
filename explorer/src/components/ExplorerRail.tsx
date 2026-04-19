import { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, FolderTree, Filter, Palette, CircleDot } from 'lucide-react';
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

const COLOR_SCHEMES = [
  { key: 'default', label: 'Default' },
  { key: 'pastel', label: 'Pastel' },
  { key: 'vibrant', label: 'Vibrant' },
  { key: 'monochrome', label: 'Monochrome' },
];

const SIZE_OPTIONS = [
  { key: 'uniform', label: 'Uniform' },
  { key: 'confidence', label: 'By Confidence' },
  { key: 'degree', label: 'By Connectivity' },
];

export default function ExplorerRail() {
  const [roots, setRoots] = useState<TaxonomyNode[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const open = useSceneStore(s => s.explorerOpen);

  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const setVisibleNodeTypes = useSceneStore(s => s.setVisibleNodeTypes);
  const setVisibleEdgeTypes = useSceneStore(s => s.setVisibleEdgeTypes);
  const colorScheme = useSceneStore(s => s.colorScheme);
  const setColorScheme = useSceneStore(s => s.setColorScheme);
  const sizeBy = useSceneStore(s => s.sizeBy);
  const setSizeBy = useSceneStore(s => s.setSizeBy);

  useEffect(() => {
    getTaxonomy().then(setRoots);
  }, []);

  if (!open) return null;

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
        <div className="px-3 py-2 border-b border-border space-y-4 max-h-[60vh] overflow-y-auto">
          {/* Color scheme */}
          <div>
            <div className="flex items-center gap-1.5 text-xs font-medium text-text-dim mb-1.5">
              <Palette size={12} />
              Color Scheme
            </div>
            <div className="grid grid-cols-2 gap-1">
              {COLOR_SCHEMES.map(scheme => (
                <button
                  key={scheme.key}
                  onClick={() => setColorScheme(scheme.key)}
                  className={`px-2 py-1 text-xs rounded border transition-colors ${
                    colorScheme === scheme.key
                      ? 'bg-accent/20 border-accent text-accent'
                      : 'border-border text-text-dim hover:text-text hover:border-text-dim'
                  }`}
                >
                  {scheme.label}
                </button>
              ))}
            </div>
          </div>

          {/* Size by */}
          <div>
            <div className="flex items-center gap-1.5 text-xs font-medium text-text-dim mb-1.5">
              <CircleDot size={12} />
              Node Size
            </div>
            <div className="grid grid-cols-3 gap-1">
              {SIZE_OPTIONS.map(opt => (
                <button
                  key={opt.key}
                  onClick={() => setSizeBy(opt.key as any)}
                  className={`px-2 py-1 text-xs rounded border transition-colors ${
                    sizeBy === opt.key
                      ? 'bg-accent/20 border-accent text-accent'
                      : 'border-border text-text-dim hover:text-text hover:border-text-dim'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Node type filters */}
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

          {/* Edge type filters */}
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
