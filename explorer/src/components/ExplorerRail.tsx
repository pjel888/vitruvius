import { useState, useEffect, useMemo, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronDown, FolderTree, Filter, Network } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getBackbonePlacementQaPreview, getBackboneSummary, getBackboneTaxonomyPreview, getTaxonomy } from '../api/graphApi';
import type { BackbonePlacementQaPreview, BackboneSummary, BackboneTaxonomyPreview, TaxonomyNode } from '../types';
import { getDisplayLabel } from '../utils/labels';
import FiltersPanel from './explorer-rail/FiltersPanel';
import BackbonePreviewPanel from './explorer-rail/BackbonePreviewPanel';

function TreeItem({ node, depth = 0, navigate }: { node: TaxonomyNode; depth?: number; navigate: ReturnType<typeof useNavigate> }) {
  const [open, setOpen] = useState(depth < 1);
  const hasChildren = node.children.length > 0;
  const displayLabel = getDisplayLabel(node);

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
        <span className="truncate" title={displayLabel}>{displayLabel}</span>
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
  { key: 'document_version', label: 'Document', color: 'bg-cyan-500' },
];

const EDGE_TYPES = [
  { key: 'HAS_CHILD', label: 'HAS_CHILD' },
  { key: 'BELONGS_TO', label: 'BELONGS_TO' },
  { key: 'RELATED_TO', label: 'RELATED_TO' },
  { key: 'DEPENDS_ON', label: 'DEPENDS_ON' },
  { key: 'APPLIES_TO', label: 'APPLIES_TO' },
  { key: 'PART_OF', label: 'PART_OF' },
  { key: 'DEFINED_BY', label: 'DEFINED_BY' },
  { key: 'REQUIRES', label: 'REQUIRES' },
  { key: 'EXCLUDES', label: 'EXCLUDES' },
  { key: 'CONSTRAINS', label: 'CONSTRAINS' },
  { key: 'AFFECTS', label: 'AFFECTS' },
  { key: 'INFLUENCES', label: 'INFLUENCES' },
  { key: 'USED_IN', label: 'USED_IN' },
  { key: 'EXECUTED_IN', label: 'EXECUTED_IN' },
  { key: 'REGULATED_BY', label: 'REGULATED_BY' },
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
  const [showBackbonePreview, setShowBackbonePreview] = useState(false);
  const [backboneSummary, setBackboneSummary] = useState<BackboneSummary | null>(null);
  const [backboneLoading, setBackboneLoading] = useState(false);
  const [backboneError, setBackboneError] = useState<string | null>(null);
  const [backboneTaxonomyPreview, setBackboneTaxonomyPreview] = useState<BackboneTaxonomyPreview | null>(null);
  const [backboneTaxonomyLoading, setBackboneTaxonomyLoading] = useState(false);
  const [backboneTaxonomyError, setBackboneTaxonomyError] = useState<string | null>(null);
  const [backbonePlacementQaPreview, setBackbonePlacementQaPreview] = useState<BackbonePlacementQaPreview | null>(null);
  const [backbonePlacementQaLoading, setBackbonePlacementQaLoading] = useState(false);
  const [backbonePlacementQaError, setBackbonePlacementQaError] = useState<string | null>(null);
  const backboneRequestId = useRef(0);
  const backboneTaxonomyRequestId = useRef(0);
  const backbonePlacementQaRequestId = useRef(0);
  const [taxonomyLoading, setTaxonomyLoading] = useState(true);
  const [taxonomyError, setTaxonomyError] = useState<string | null>(null);
  const open = useSceneStore(s => s.explorerOpen);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
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
  const nodeTypeCounts = useMemo(() => {
    const counts = new Map<string, number>();
    nodes.forEach((node) => counts.set(node.type, (counts.get(node.type) ?? 0) + 1));
    return counts;
  }, [nodes]);
  const edgeTypeCounts = useMemo(() => {
    const counts = new Map<string, number>();
    edges.forEach((edge) => counts.set(edge.type, (counts.get(edge.type) ?? 0) + 1));
    return counts;
  }, [edges]);
  const scopedNodeTypes = useMemo(
    () => NODE_TYPES.map((option) => ({
      ...option,
      count: nodeTypeCounts.get(option.key) ?? 0,
      available: nodeTypeCounts.has(option.key),
    })),
    [nodeTypeCounts]
  );
  const scopedEdgeTypes = useMemo(
    () => EDGE_TYPES.map((option) => ({
      ...option,
      count: edgeTypeCounts.get(option.key) ?? 0,
      available: edgeTypeCounts.has(option.key),
    })),
    [edgeTypeCounts]
  );
  const activeFilterCount = [...visibleNodeTypes].filter((type) => nodeTypeCounts.has(type)).length
    + [...visibleEdgeTypes].filter((type) => edgeTypeCounts.has(type)).length;

  const pinnedNodes = useMemo(
    () => pinnedNodeIds
      .map((id) => nodes.find((node) => node.id === id))
      .filter((node): node is NonNullable<typeof node> => Boolean(node)),
    [pinnedNodeIds, nodes]
  );

  useEffect(() => {
    let cancelled = false;
    getTaxonomy()
      .then((nextRoots) => {
        if (!cancelled) {
          setRoots(nextRoots);
          setTaxonomyError(null);
        }
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

  async function loadBackbonePreview() {
    const requestId = backboneRequestId.current + 1;
    backboneRequestId.current = requestId;
    backboneTaxonomyRequestId.current += 1;
    backbonePlacementQaRequestId.current += 1;
    setBackboneLoading(true);
    setBackboneTaxonomyLoading(false);
    setBackbonePlacementQaLoading(false);
    setBackboneTaxonomyPreview(null);
    setBackboneTaxonomyError(null);
    setBackbonePlacementQaPreview(null);
    setBackbonePlacementQaError(null);
    try {
      const summary = await getBackboneSummary();
      if (backboneRequestId.current !== requestId) return;
      setBackboneSummary(summary);
      setBackboneError(null);
    } catch (error) {
      if (backboneRequestId.current !== requestId) return;
      setBackboneSummary(null);
      setBackboneError(error instanceof Error ? error.message : 'Failed to load AEC-MEPFS Backbone preview');
    } finally {
      if (backboneRequestId.current === requestId) setBackboneLoading(false);
    }
  }

  async function loadBackboneTaxonomyPreview() {
    const requestId = backboneTaxonomyRequestId.current + 1;
    backboneTaxonomyRequestId.current = requestId;
    setBackboneTaxonomyLoading(true);
    try {
      const preview = await getBackboneTaxonomyPreview();
      if (backboneTaxonomyRequestId.current !== requestId) return;
      setBackboneTaxonomyPreview(preview);
      setBackboneTaxonomyError(null);
    } catch (error) {
      if (backboneTaxonomyRequestId.current !== requestId) return;
      setBackboneTaxonomyPreview(null);
      setBackboneTaxonomyError(error instanceof Error ? error.message : 'Failed to load AEC-MEPFS registry details');
    } finally {
      if (backboneTaxonomyRequestId.current === requestId) setBackboneTaxonomyLoading(false);
    }
  }

  async function loadBackbonePlacementQaPreview() {
    const requestId = backbonePlacementQaRequestId.current + 1;
    backbonePlacementQaRequestId.current = requestId;
    setBackbonePlacementQaLoading(true);
    try {
      const preview = await getBackbonePlacementQaPreview();
      if (backbonePlacementQaRequestId.current !== requestId) return;
      setBackbonePlacementQaPreview(preview);
      setBackbonePlacementQaError(null);
    } catch (error) {
      if (backbonePlacementQaRequestId.current !== requestId) return;
      setBackbonePlacementQaPreview(null);
      setBackbonePlacementQaError(error instanceof Error ? error.message : 'Failed to load AEC-MEPFS placement QA');
    } finally {
      if (backbonePlacementQaRequestId.current === requestId) setBackbonePlacementQaLoading(false);
    }
  }

  function toggleBackbonePreview() {
    const nextOpen = !showBackbonePreview;
    setShowBackbonePreview(nextOpen);
    if (nextOpen && !backboneSummary && !backboneLoading) {
      void loadBackbonePreview();
    }
  }

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
    <div className="kg-panel w-72 border-r border-border flex flex-col shrink-0 overflow-hidden">
      <div className="px-4 py-3 border-b border-border flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-text-dim">
            <FolderTree size={14} />
            Navigator
          </div>
          <div className="mt-1 text-[11px] text-text-dim">
            {roots.length.toLocaleString()} roots · {pinnedNodes.length} pinned · {activeFilterCount} filters
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <button
            className={`kg-control p-2 rounded-xl transition-colors ${showBackbonePreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={toggleBackbonePreview}
            title="Toggle AEC-MEPFS Backbone preview"
            aria-label="Toggle AEC-MEPFS Backbone preview"
            aria-pressed={showBackbonePreview}
          >
            <Network size={14} />
          </button>
          <button
            className={`kg-control p-2 rounded-xl transition-colors ${showFilters ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={() => setShowFilters(!showFilters)}
            title="Toggle filters"
            aria-label="Toggle graph filters"
            aria-pressed={showFilters}
          >
            <Filter size={14} />
          </button>
        </div>
      </div>

      {showBackbonePreview && (
        <BackbonePreviewPanel
          summary={backboneSummary}
          loading={backboneLoading}
          error={backboneError}
          onRefresh={() => { void loadBackbonePreview(); }}
          taxonomyPreview={backboneTaxonomyPreview}
          taxonomyLoading={backboneTaxonomyLoading}
          taxonomyError={backboneTaxonomyError}
          onLoadTaxonomyPreview={() => { void loadBackboneTaxonomyPreview(); }}
          placementQaPreview={backbonePlacementQaPreview}
          placementQaLoading={backbonePlacementQaLoading}
          placementQaError={backbonePlacementQaError}
          onLoadPlacementQaPreview={() => { void loadBackbonePlacementQaPreview(); }}
        />
      )}

      {showFilters && (
        <FiltersPanel
          colorScheme={colorScheme}
          sizeBy={sizeBy}
          visibleNodeTypes={visibleNodeTypes}
          visibleEdgeTypes={visibleEdgeTypes}
          colorSchemes={COLOR_SCHEMES}
          sizeOptions={SIZE_OPTIONS}
          nodeTypes={scopedNodeTypes}
          edgeTypes={scopedEdgeTypes}
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
                className="w-full text-left rounded-lg px-2 py-1.5 text-sm hover:bg-panel-hover transition-colors"
              >
                <div className="truncate text-text" title={getDisplayLabel(node)}>{getDisplayLabel(node)}</div>
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
