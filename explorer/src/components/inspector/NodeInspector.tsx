import { useState } from 'react';
import { ArrowRight, CheckCircle2, ExternalLink, FileText, Flag, Focus, MapPin, Pin, Route, Trash2, X } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { NodeDetail, RelationDetail } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

const EDGE_COLORS: Record<string, string> = {
  HAS_CHILD: '#6b7280',
  BELONGS_TO: '#6b7280',
  RELATED_TO: '#6b7280',
  DEPENDS_ON: '#f59e0b',
  DEFINED_BY: '#10b981',
  REQUIRES: '#8b5cf6',
  SUPPORTED_BY: '#94a3b8',
};

type InspectorTab = 'overview' | 'relationships' | 'sources' | 'metadata';

function MetadataRow({ label, value }: { label: string; value?: string | number | null }) {
  if (value === undefined || value === null || value === '') return null;
  return (
    <div className="kg-card rounded-xl p-3">
      <div className="text-xs uppercase tracking-wider text-text-dim mb-1">{label}</div>
      <div className="text-sm break-words">{value}</div>
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
          <button
            key={`${relation.relType}-${relation.other.id}-${index}`}
            className="kg-card w-full text-left border-l-2 rounded-xl pl-3 pr-3 py-2.5 hover:bg-panel-hover transition-colors"
            style={{ borderLeftColor: EDGE_COLORS[relation.relType] || '#6b7280' }}
            onClick={() => onSelectNode(relation.other.id)}
          >
            <div className="flex items-center gap-1 text-sm">
              {title === 'Incoming' ? (
                <>
                  <span className="truncate" title={relation.other.label}>{otherLabel}</span>
                  <ArrowRight size={12} className="text-text-dim shrink-0" />
                  <span className="font-medium shrink-0">{relation.relType}</span>
                </>
              ) : (
                <>
                  <span className="font-medium shrink-0">{relation.relType}</span>
                  <ArrowRight size={12} className="text-text-dim shrink-0" />
                  <span className="truncate" title={relation.other.label}>{otherLabel}</span>
                </>
              )}
            </div>
            <div className="text-[11px] text-text-dim mt-0.5 truncate">{relation.other.id}</div>
            {relation.reasoning && <div className="text-xs text-text-dim mt-1 leading-relaxed">{relation.reasoning}</div>}
          </button>
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
  const pathSourceId = useSceneStore((s) => s.pathSourceId);
  const pathTargetId = useSceneStore((s) => s.pathTargetId);
  const highlightedPath = useSceneStore((s) => s.highlightedPath);
  const setPathSource = useSceneStore((s) => s.setPathSource);
  const setPathTarget = useSceneStore((s) => s.setPathTarget);
  const clearPath = useSceneStore((s) => s.clearPath);

  const displayLabel = getDisplayLabel(node);
  const relationshipCount = incoming.length + outgoing.length;
  const confidenceLabel = node.confidence !== undefined ? `${(node.confidence * 100).toFixed(0)}% confidence` : null;

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
            <h2 className="text-base font-semibold text-accent truncate" title={node.label}>{displayLabel}</h2>
            <div className="mt-2 flex flex-wrap gap-1.5">
              <span className="kg-chip rounded-full px-2 py-0.5 text-[11px] uppercase tracking-wider">{node.type}</span>
              {node.status && <span className="kg-chip rounded-full px-2 py-0.5 text-[11px] uppercase tracking-wider">{node.status}</span>}
              {confidenceLabel && <span className="rounded-full border border-emerald-400/25 bg-emerald-400/10 px-2 py-0.5 text-[11px] text-emerald-100">{confidenceLabel}</span>}
            </div>
          </div>
          <div className="flex items-center gap-1">
            <button className="p-1.5 rounded-lg hover:bg-panel-hover text-text-dim" title="Pin" aria-label="Pin node" onClick={() => togglePinnedNode(node.id)}>
              <Pin size={14} className={pinnedNodeIds.includes(node.id) ? 'text-accent' : ''} />
            </button>
            <button className="p-1.5 rounded-lg hover:bg-panel-hover text-text-dim" title="Focus 1-hop" aria-label="Focus one-hop neighborhood" onClick={() => requestFocusSubgraph(node.id)}>
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
            className={`py-2.5 text-[11px] font-medium border-b-2 transition-colors ${activeTab === tab ? 'border-accent text-accent bg-accent/5' : 'border-transparent text-text-dim hover:text-text'}`}
            onClick={() => setActiveTab(tab)}
          >
            {label}{count ? ` (${count})` : ''}
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
