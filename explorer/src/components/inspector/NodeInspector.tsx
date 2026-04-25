import { useState, type MouseEvent } from 'react';
import { ArrowRight, Check, CheckCircle2, Copy, ExternalLink, FileText, Flag, Focus, MapPin, Pin, Route, Trash2, X } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { NodeDetail, RelationDetail } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

const EDGE_COLORS: Record<string, string> = {
  HAS_CHILD: '#6b7280',
  BELONGS_TO: '#6b7280',
  RELATED_TO: '#6b7280',
  DEPENDS_ON: '#f59e0b',
  APPLIES_TO: '#14b8a6',
  PART_OF: '#64748b',
  DEFINED_BY: '#10b981',
  REQUIRES: '#8b5cf6',
  EXCLUDES: '#f97316',
  CONSTRAINS: '#ef4444',
  AFFECTS: '#0ea5e9',
  INFLUENCES: '#22c55e',
  USED_IN: '#eab308',
  EXECUTED_IN: '#a855f7',
  REGULATED_BY: '#f43f5e',
  SUPPORTED_BY: '#94a3b8',
};

type InspectorTab = 'overview' | 'relationships' | 'sources' | 'metadata';

function CopyValueButton({ value, label }: { value: string; label: string }) {
  const [copied, setCopied] = useState(false);
  if (!value) return null;

  async function copyValue(event: MouseEvent<HTMLButtonElement>) {
    event.stopPropagation();
    try {
      await navigator.clipboard?.writeText(value);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 900);
    } catch {
      setCopied(false);
    }
  }

  return (
    <button
      className="shrink-0 rounded-md p-1 text-text-dim transition-colors hover:bg-panel-hover hover:text-text"
      type="button"
      title={copied ? 'Copied' : label}
      aria-label={label}
      onClick={(event) => void copyValue(event)}
    >
      {copied ? <Check size={12} className="text-accent" /> : <Copy size={12} />}
    </button>
  );
}

function MetadataRow({ label, value }: { label: string; value?: string | number | null }) {
  if (value === undefined || value === null || value === '') return null;
  const textValue = String(value);
  return (
    <div className="kg-card rounded-xl p-3">
      <div className="mb-1 flex items-center justify-between gap-2">
        <div className="text-xs uppercase tracking-wider text-text-dim">{label}</div>
        <CopyValueButton value={textValue} label={`Copy ${label.toLowerCase()}`} />
      </div>
      <div className="text-sm break-words">{textValue}</div>
    </div>
  );
}

function RelationList({ title, relations, onSelectNode }: { title: string; relations: RelationDetail[]; onSelectNode: (id: string) => void }) {
  return (
    <div className="space-y-2">
      <div className="text-xs uppercase tracking-wider text-text-dim">{title}</div>
      {relations.length === 0 ? (
        <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
          No {title.toLowerCase()} relationships.
        </div>
      ) : relations.map((relation, index) => {
        const otherLabel = getDisplayLabel(relation.other);
        return (
          <div
            key={`${relation.relType}-${relation.other.id}-${index}`}
            className="kg-card flex w-full items-start gap-2 border-l-2 rounded-xl pl-3 pr-2 py-2.5 transition-colors hover:bg-panel-hover"
            style={{ borderLeftColor: EDGE_COLORS[relation.relType] || '#6b7280' }}
          >
            <button
              className="min-w-0 flex-1 text-left"
              type="button"
              onClick={() => onSelectNode(relation.other.id)}
            >
              <div className="flex min-w-0 items-center gap-1 text-sm">
                {title === 'Incoming' ? (
                  <>
                    <span className="truncate" title={otherLabel}>{otherLabel}</span>
                    <ArrowRight size={12} className="text-text-dim shrink-0" />
                    <span className="font-medium shrink-0">{relation.relType}</span>
                  </>
                ) : (
                  <>
                    <span className="font-medium shrink-0">{relation.relType}</span>
                    <ArrowRight size={12} className="text-text-dim shrink-0" />
                    <span className="truncate" title={otherLabel}>{otherLabel}</span>
                  </>
                )}
              </div>
              <div className="text-[11px] text-text-dim mt-0.5 truncate">{relation.other.id}</div>
              {relation.reasoning && <div className="text-xs text-text-dim mt-1 leading-relaxed">{relation.reasoning}</div>}
            </button>
            <CopyValueButton value={otherLabel} label={`Copy ${title.toLowerCase()} node name`} />
          </div>
        );
      })}
    </div>
  );
}

export default function NodeInspector({ detail }: { detail: NodeDetail }) {
  const { node, taxonomyPath, incoming, outgoing, evidence } = detail;
  const [activeTab, setActiveTab] = useState<InspectorTab>('overview');
  const setSelectedNode = useSceneStore((s) => s.setSelectedNode);
  const openBottom = useSceneStore((s) => s.openBottom);
  const pinnedNodeIds = useSceneStore((s) => s.pinnedNodeIds);
  const togglePinnedNode = useSceneStore((s) => s.togglePinnedNode);
  const requestFocusSubgraph = useSceneStore((s) => s.requestFocusSubgraph);
  const requestShowAll = useSceneStore((s) => s.requestShowAll);
  const hiddenNodeIds = useSceneStore((s) => s.hiddenNodeIds);
  const pathSourceId = useSceneStore((s) => s.pathSourceId);
  const pathTargetId = useSceneStore((s) => s.pathTargetId);
  const highlightedPath = useSceneStore((s) => s.highlightedPath);
  const setPathSource = useSceneStore((s) => s.setPathSource);
  const setPathTarget = useSceneStore((s) => s.setPathTarget);
  const clearPath = useSceneStore((s) => s.clearPath);

  const displayLabel = getDisplayLabel(node);
  const relationshipCount = incoming.length + outgoing.length;
  const confidenceLabel = node.confidence !== undefined ? `${(node.confidence * 100).toFixed(0)}% confidence` : null;
  const pinned = pinnedNodeIds.includes(node.id);
  const isolated = hiddenNodeIds.length > 0;

  function openEvidenceTable() {
    openBottom({
      type: 'table',
      title: `${displayLabel} Sources`,
      columns: [
        { key: 'document', label: 'Document' },
        { key: 'quote', label: 'Quote' },
        { key: 'confidence', label: 'Confidence' },
      ],
      rows: evidence.map((item) => ({
        id: item.id,
        deepLink: item.deep_link,
        values: {
          document: item.document_title || item.document_id || 'Unknown source',
          quote: item.quote,
          confidence: item.confidence !== undefined ? `${(item.confidence * 100).toFixed(0)}%` : '—',
        },
      })),
    });
  }

  return (
    <div className="flex flex-col h-full">
      <div className="sticky top-0 z-10 border-b border-border bg-panel/95 px-4 py-3 backdrop-blur">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <div className="flex min-w-0 items-center gap-1">
              <h2 className="truncate text-base font-semibold text-accent" title={displayLabel}>{displayLabel}</h2>
              <CopyValueButton value={displayLabel} label="Copy node name" />
            </div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              <span className="kg-chip rounded-full px-2 py-0.5 text-[11px] uppercase tracking-wider">{node.type}</span>
              {node.status && <span className="kg-chip rounded-full px-2 py-0.5 text-[11px] uppercase tracking-wider">{node.status}</span>}
              {confidenceLabel && <span className="rounded-full border border-emerald-400/25 bg-emerald-400/10 px-2 py-0.5 text-[11px] text-emerald-100">{confidenceLabel}</span>}
            </div>
          </div>
          <div className="flex items-center gap-1">
            <button
              className="p-1.5 rounded-lg hover:bg-panel-hover text-text-dim"
              title={pinned ? 'Unpin' : 'Pin'}
              aria-label={pinned ? 'Unpin node' : 'Pin node'}
              onClick={() => togglePinnedNode(node.id)}
            >
              <Pin size={14} className={pinned ? 'text-accent' : ''} />
            </button>
            <button
              className={`p-1.5 rounded-lg hover:bg-panel-hover ${isolated ? 'text-accent' : 'text-text-dim'}`}
              title={isolated ? 'Clear isolation' : 'Isolate connected nodes'}
              aria-label={isolated ? 'Clear node isolation' : 'Isolate connected nodes'}
              onClick={() => isolated ? requestShowAll() : requestFocusSubgraph(node.id)}
            >
              <Focus size={14} />
            </button>
            <button className="p-1.5 rounded-lg hover:bg-panel-hover text-text-dim" onClick={() => setSelectedNode(null)} title="Close" aria-label="Close node inspector">
              <X size={14} />
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 border-b border-border bg-bg/20">
        {([
          ['overview', 'Overview', undefined],
          ['relationships', 'Relationships', relationshipCount],
          ['sources', 'Sources', evidence.length],
          ['metadata', 'Metadata', undefined],
        ] as const).map(([tab, label, count]) => (
          <button
            key={tab}
            className={`min-w-0 py-2.5 text-[8px] font-medium border-b-2 transition-colors ${activeTab === tab ? 'border-accent text-accent bg-accent/5' : 'border-transparent text-text-dim hover:text-text'}`}
            onClick={() => setActiveTab(tab)}
          >
            <span className="inline-flex max-w-full items-center justify-center gap-0.5 whitespace-nowrap">
              <span className="truncate">{label}</span>
              {count ? <span className="shrink-0">({count})</span> : null}
            </span>
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'overview' && (
          <>
            <MetadataRow label="Full label" value={node.label} />
            <MetadataRow label="Canonical ID" value={node.id} />
            {node.summary && <MetadataRow label="Summary" value={node.summary} />}
            {taxonomyPath.length > 0 && (
              <MetadataRow label="Taxonomy Path" value={taxonomyPath.map((taxonomyNode) => getDisplayLabel(taxonomyNode)).join(' > ')} />
            )}

            <div className="kg-card rounded-xl p-3">
              <div className="text-xs uppercase tracking-wider text-text-dim mb-2 flex items-center gap-1">
                <Route size={12} />
                Path Tracing
              </div>
              {highlightedPath ? (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm text-emerald-400">
                    <CheckCircle2 size={14} />
                    Path highlighted ({highlightedPath.nodeIds.length} nodes, {highlightedPath.edgeIds.length} edges)
                  </div>
                  <button onClick={clearPath} className="flex items-center gap-1.5 text-xs text-text-dim hover:text-text transition-colors">
                    <Trash2 size={12} />
                    Clear path
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-1.5">
                  {pathSourceId === null && (
                    <button onClick={() => setPathSource(node.id)} className="flex items-center gap-2 text-sm text-text hover:text-accent transition-colors">
                      <MapPin size={14} />
                      Set as path start
                    </button>
                  )}
                  {pathSourceId === node.id && (
                    <div className="flex items-center gap-2 text-sm text-amber-400">
                      <MapPin size={14} />
                      Path start selected
                    </div>
                  )}
                  {pathSourceId && pathSourceId !== node.id && pathTargetId === null && (
                    <button onClick={() => setPathTarget(node.id)} className="flex items-center gap-2 text-sm text-text hover:text-accent transition-colors">
                      <Flag size={14} />
                      Set as path end
                    </button>
                  )}
                  {pathTargetId === node.id && (
                    <div className="flex items-center gap-2 text-sm text-amber-400">
                      <Flag size={14} />
                      Path end selected
                    </div>
                  )}
                  {(pathSourceId || pathTargetId) && (
                    <button onClick={clearPath} className="flex items-center gap-1.5 text-xs text-text-dim hover:text-text transition-colors mt-1">
                      <Trash2 size={12} />
                      Clear selection
                    </button>
                  )}
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === 'relationships' && (
          <div className="space-y-4">
            {relationshipCount === 0 && (
              <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
                No relationships are available for this node.
              </div>
            )}
            <RelationList title="Incoming" relations={incoming} onSelectNode={setSelectedNode} />
            <RelationList title="Outgoing" relations={outgoing} onSelectNode={setSelectedNode} />
          </div>
        )}

        {activeTab === 'sources' && (
          <>
            {evidence.length === 0 && (
              <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
                No source materials are linked to this node.
              </div>
            )}
            {evidence.length > 0 && (
              <button onClick={openEvidenceTable} className="kg-control rounded-lg px-3 py-1.5 text-xs text-accent">
                Open source table
              </button>
            )}
            {evidence.map((item) => (
              <div key={item.id} className="kg-card rounded-xl border-l-2 border-border p-3">
                <div className="text-sm italic leading-relaxed text-text">"{item.quote}"</div>
                <div className="flex items-center gap-1 mt-1 text-xs text-text-dim">
                  <FileText size={12} />
                  {item.document_title || item.document_id || 'Unknown source'}
                </div>
                {item.deep_link && (
                  <button
                    onClick={() => openBottom({
                      type: 'source',
                      title: item.document_title || item.document_id || 'Source Document',
                      documentId: item.document_id,
                      quote: item.quote,
                      deepLink: item.deep_link,
                    })}
                    className="text-xs text-accent hover:underline mt-1 inline-flex items-center gap-1"
                  >
                    Open source <ExternalLink size={10} />
                  </button>
                )}
              </div>
            ))}
          </>
        )}

        {activeTab === 'metadata' && (
          <>
            <MetadataRow label="Canonical ID" value={node.id} />
            <MetadataRow label="Type" value={node.type} />
            <MetadataRow label="Kind" value={node.kind} />
            <MetadataRow label="Slug" value={node.slug} />
            <MetadataRow label="Status" value={node.status} />
            {node.confidence !== undefined && <MetadataRow label="Confidence" value={`${(node.confidence * 100).toFixed(0)}%`} />}
            {node.aliases && node.aliases.length > 0 && <MetadataRow label="Aliases" value={node.aliases.join(', ')} />}
            <MetadataRow label="Created" value={node.createdAt} />
            <MetadataRow label="Updated" value={node.updatedAt} />
          </>
        )}
      </div>
    </div>
  );
}
