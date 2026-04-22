import { useState, useEffect } from 'react';
import { X, Pin, Focus, PanelRightOpen, PanelRightClose, ArrowRight, FileText, ExternalLink, Route, MapPin, Flag, Trash2, CheckCircle2 } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNode, getEdgeDetail, tracePath } from '../api/graphApi';
import type { NodeDetail, EdgeDetail } from '../types';

const EDGE_COLORS: Record<string, string> = {
  HAS_CHILD: '#6b7280',
  BELONGS_TO: '#6b7280',
  RELATED_TO: '#6b7280',
  DEPENDS_ON: '#f59e0b',
  DEFINED_BY: '#10b981',
  REQUIRES: '#8b5cf6',
  SUPPORTED_BY: '#94a3b8',
};

function NodeInspector({ detail }: { detail: NodeDetail }) {
  const { node, taxonomyPath, incoming, outgoing, evidence } = detail;
  const [activeTab, setActiveTab] = useState<'summary' | 'evidence' | 'incoming' | 'outgoing'>('summary');
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const openBottom = useSceneStore(s => s.openBottom);
  const pathSourceId = useSceneStore(s => s.pathSourceId);
  const pathTargetId = useSceneStore(s => s.pathTargetId);
  const highlightedPath = useSceneStore(s => s.highlightedPath);
  const setPathSource = useSceneStore(s => s.setPathSource);
  const setPathTarget = useSceneStore(s => s.setPathTarget);
  const clearPath = useSceneStore(s => s.clearPath);

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-border">
        <div className="flex items-start justify-between gap-2">
          <div>
            <h2 className="text-sm font-semibold text-accent">{node.label}</h2>
            <span className="text-xs text-text-dim">{node.type}</span>
          </div>
          <div className="flex items-center gap-1">
            <button className="p-1 rounded hover:bg-panel-hover text-text-dim" title="Pin">
              <Pin size={14} />
            </button>
            <button className="p-1 rounded hover:bg-panel-hover text-text-dim" title="Focus 1-hop">
              <Focus size={14} />
            </button>
            <button
              className="p-1 rounded hover:bg-panel-hover text-text-dim"
              onClick={() => setSelectedNode(null)}
              title="Close"
            >
              <X size={14} />
            </button>
          </div>
        </div>
      </div>

      <div className="flex border-b border-border">
        {(['summary', 'evidence', 'incoming', 'outgoing'] as const).map(tab => (
          <button
            key={tab}
            className={`flex-1 py-2 text-xs font-medium capitalize border-b-2 transition-colors ${
              activeTab === tab ? 'border-accent text-accent' : 'border-transparent text-text-dim hover:text-text'
            }`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
            {tab === 'evidence' && evidence.length > 0 && ` (${evidence.length})`}
            {tab === 'incoming' && incoming.length > 0 && ` (${incoming.length})`}
            {tab === 'outgoing' && outgoing.length > 0 && ` (${outgoing.length})`}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'summary' && (
          <>
            {node.summary && (
              <div>
                <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Summary</div>
                <div className="text-sm leading-relaxed">{node.summary}</div>
              </div>
            )}
            {taxonomyPath.length > 0 && (
              <div>
                <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Taxonomy Path</div>
                <div className="text-sm">{taxonomyPath.map(t => t.label).join(' > ')}</div>
              </div>
            )}
            {node.aliases && node.aliases.length > 0 && (
              <div>
                <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Aliases</div>
                <div className="text-sm">{node.aliases.join(', ')}</div>
              </div>
            )}
            {node.confidence !== undefined && (
              <div>
                <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Confidence</div>
                <div className="text-sm">{(node.confidence * 100).toFixed(0)}%</div>
              </div>
            )}

            {/* Path Tracing */}
            <div className="border-t border-border pt-3">
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
                  <button
                    onClick={clearPath}
                    className="flex items-center gap-1.5 text-xs text-text-dim hover:text-text transition-colors"
                  >
                    <Trash2 size={12} />
                    Clear path
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-1.5">
                  {pathSourceId === null && (
                    <button
                      onClick={() => setPathSource(node.id)}
                      className="flex items-center gap-2 text-sm text-text hover:text-accent transition-colors"
                    >
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
                    <button
                      onClick={() => setPathTarget(node.id)}
                      className="flex items-center gap-2 text-sm text-text hover:text-accent transition-colors"
                    >
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
                    <button
                      onClick={clearPath}
                      className="flex items-center gap-1.5 text-xs text-text-dim hover:text-text transition-colors mt-1"
                    >
                      <Trash2 size={12} />
                      Clear selection
                    </button>
                  )}
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === 'evidence' && (
          <>
            {evidence.length === 0 && <div className="text-sm text-text-dim italic">No evidence spans.</div>}
            {evidence.length > 0 && (
              <button
                onClick={() => openBottom({
                  type: 'table',
                  title: `${node.label} Evidence`,
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
                })}
                className="text-xs text-accent hover:underline"
              >
                Open evidence table
              </button>
            )}
            {evidence.map(e => (
              <div key={e.id} className="border-l-2 border-border pl-3 py-1">
                <div className="text-sm italic leading-relaxed">{e.quote}</div>
                {e.document_title && (
                  <div className="flex items-center gap-1 mt-1 text-xs text-text-dim">
                    <FileText size={12} />
                    {e.document_title}
                  </div>
                )}
                {e.deep_link && (
                  <button
                    onClick={() => openBottom({
                      type: 'source',
                      title: e.document_title || 'Source Document',
                      documentId: e.document_id,
                      quote: e.quote,
                      deepLink: e.deep_link,
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

        {activeTab === 'incoming' && (
          <>
            {incoming.length === 0 && <div className="text-sm text-text-dim italic">No incoming relationships.</div>}
            {incoming.map((rel, i) => (
              <button
                key={i}
                className="w-full text-left border-l-2 pl-3 py-1 hover:bg-panel-hover transition-colors"
                style={{ borderLeftColor: EDGE_COLORS[rel.relType] || '#6b7280' }}
                onClick={() => setSelectedNode(rel.other.id)}
              >
                <div className="flex items-center gap-1 text-sm">
                  <span className="truncate">{rel.other.label}</span>
                  <ArrowRight size={12} className="text-text-dim shrink-0" />
                  <span className="font-medium shrink-0">{rel.relType}</span>
                </div>
                {rel.reasoning && <div className="text-xs text-text-dim mt-0.5">{rel.reasoning}</div>}
              </button>
            ))}
          </>
        )}

        {activeTab === 'outgoing' && (
          <>
            {outgoing.length === 0 && <div className="text-sm text-text-dim italic">No outgoing relationships.</div>}
            {outgoing.map((rel, i) => (
              <button
                key={i}
                className="w-full text-left border-l-2 pl-3 py-1 hover:bg-panel-hover transition-colors"
                style={{ borderLeftColor: EDGE_COLORS[rel.relType] || '#6b7280' }}
                onClick={() => setSelectedNode(rel.other.id)}
              >
                <div className="flex items-center gap-1 text-sm">
                  <span className="font-medium shrink-0">{rel.relType}</span>
                  <ArrowRight size={12} className="text-text-dim shrink-0" />
                  <span className="truncate">{rel.other.label}</span>
                </div>
                {rel.reasoning && <div className="text-xs text-text-dim mt-0.5">{rel.reasoning}</div>}
              </button>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

function EdgeInspector({ detail }: { detail: EdgeDetail }) {
  const { edge, source, target } = detail;
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);

  return (
    <div className="flex flex-col h-full p-4 space-y-4">
      <div className="flex items-start justify-between">
        <h2 className="text-sm font-semibold text-accent">{edge.type}</h2>
        <div className="flex items-center gap-1">
          <button className="p-1 rounded hover:bg-panel-hover text-text-dim" onClick={() => {}} title="Close">
            <X size={14} />
          </button>
        </div>
      </div>
      <div>
        <div className="text-xs uppercase tracking-wider text-text-dim mb-1">From</div>
        <button className="text-sm hover:text-accent transition-colors" onClick={() => setSelectedNode(source.id)}>
          {source.label}
        </button>
      </div>
      <div>
        <div className="text-xs uppercase tracking-wider text-text-dim mb-1">To</div>
        <button className="text-sm hover:text-accent transition-colors" onClick={() => setSelectedNode(target.id)}>
          {target.label}
        </button>
      </div>
      {edge.confidence !== undefined && (
        <div>
          <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Confidence</div>
          <div className="text-sm">{(edge.confidence * 100).toFixed(0)}%</div>
        </div>
      )}
      {edge.reasoning && (
        <div>
          <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Reasoning</div>
          <div className="text-sm leading-relaxed">{edge.reasoning}</div>
        </div>
      )}
      {edge.assertionId && (
        <div>
          <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Assertion ID</div>
          <div className="text-xs font-mono text-text-dim">{edge.assertionId}</div>
        </div>
      )}
    </div>
  );
}

export default function InspectorRail() {
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const selectedEdgeId = useSceneStore(s => s.selectedEdgeId);
  const inspectorOpen = useSceneStore(s => s.inspectorOpen);
  const openInspector = useSceneStore(s => s.openInspector);
  const closeInspector = useSceneStore(s => s.closeInspector);
  const pathSourceId = useSceneStore(s => s.pathSourceId);
  const pathTargetId = useSceneStore(s => s.pathTargetId);
  const highlightedPath = useSceneStore(s => s.highlightedPath);
  const setHighlightedPath = useSceneStore(s => s.setHighlightedPath);

  const [nodeDetail, setNodeDetail] = useState<NodeDetail | null>(null);
  const [edgeDetail, setEdgeDetail] = useState<EdgeDetail | null>(null);

  useEffect(() => {
    if (selectedNodeId) {
      getNode(selectedNodeId).then(setNodeDetail);
    } else {
      setNodeDetail(null);
    }
  }, [selectedNodeId]);

  useEffect(() => {
    if (selectedEdgeId) {
      getEdgeDetail(selectedEdgeId).then(setEdgeDetail);
    } else {
      setEdgeDetail(null);
    }
  }, [selectedEdgeId]);

  // Auto-find path when both source and target are set
  useEffect(() => {
    if (pathSourceId && pathTargetId && !highlightedPath) {
      tracePath(pathSourceId, pathTargetId).then(data => {
        if (data.paths && data.paths.length > 0) {
          const path = data.paths[0];
          setHighlightedPath({
            nodeIds: path.nodes.map((n: any) => n.id),
            edgeIds: path.edges.map((e: any) => e.id),
          });
        }
      }).catch(() => {
        // Path not found — leave highlightedPath null
      });
    }
  }, [pathSourceId, pathTargetId, highlightedPath, setHighlightedPath]);

  // Collapsed state — thin expand button
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

  // Expanded state
  return (
    <div className="w-96 bg-panel border-l border-border flex flex-col shrink-0 overflow-hidden">
      {/* Persistent panel header — minimize button always visible */}
      <div className="px-3 py-2 border-b border-border flex items-center justify-between shrink-0">
        <span className="text-xs font-semibold uppercase tracking-wider text-text-dim">
          {selectedNodeId && nodeDetail
            ? nodeDetail.node.label
            : selectedEdgeId && edgeDetail
            ? edgeDetail.edge.type
            : 'Inspector'}
        </span>
        <button
          className="p-1 rounded hover:bg-panel-hover text-text-dim"
          onClick={closeInspector}
          title="Minimize"
        >
          <PanelRightClose size={14} />
        </button>
      </div>

      <div className="flex-1 overflow-hidden">
        {!selectedNodeId && !selectedEdgeId ? (
          <div className="h-full flex flex-col items-center justify-center p-6 text-center">
            <div className="text-sm text-text-dim mb-2">Select a node to see details.</div>
            <div className="text-xs text-text-dim">Click empty space to clear.</div>
          </div>
        ) : selectedNodeId && nodeDetail ? (
          <NodeInspector detail={nodeDetail} />
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
