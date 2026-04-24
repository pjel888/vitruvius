import { FileText, X } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { EdgeDetail } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

export default function EdgeInspector({ detail }: { detail: EdgeDetail }) {
  const { edge, source, target } = detail;
  const setSelectedNode = useSceneStore((s) => s.setSelectedNode);
  const setSelectedEdge = useSceneStore((s) => s.setSelectedEdge);
  const openBottom = useSceneStore((s) => s.openBottom);

  return (
    <div className="flex flex-col h-full p-4 space-y-4">
      <div className="flex items-start justify-between">
        <h2 className="text-sm font-semibold text-accent">{edge.type}</h2>
        <div className="flex items-center gap-1">
          <button className="p-1 rounded hover:bg-panel-hover text-text-dim" onClick={() => setSelectedEdge(null)} title="Close">
            <X size={14} />
          </button>
        </div>
      </div>
      <div>
        <div className="text-xs uppercase tracking-wider text-text-dim mb-1">From</div>
        <button className="text-sm hover:text-accent transition-colors" onClick={() => setSelectedNode(source.id)}>
          {getDisplayLabel(source)}
        </button>
      </div>
      <div>
        <div className="text-xs uppercase tracking-wider text-text-dim mb-1">To</div>
        <button className="text-sm hover:text-accent transition-colors" onClick={() => setSelectedNode(target.id)}>
          {getDisplayLabel(target)}
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
      {detail.evidence.length > 0 ? (
        <div>
          <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Evidence</div>
          <button
            onClick={() => openBottom({
              type: 'table',
              title: `${edge.type} Evidence`,
              columns: [
                { key: 'document', label: 'Document' },
                { key: 'quote', label: 'Quote' },
              ],
              rows: detail.evidence.map((item) => ({
                id: item.id,
                deepLink: item.deep_link,
                values: {
                  document: item.document_title || item.document_id || 'Unknown source',
                  quote: item.quote,
                },
              })),
            })}
            className="text-xs text-accent hover:underline"
          >
            Open edge evidence
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-2 text-xs text-text-dim">
          <FileText size={12} />
          No edge evidence available.
        </div>
      )}
    </div>
  );
}
