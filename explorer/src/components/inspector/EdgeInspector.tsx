import { BadgeCheck, FileText, GitMerge, ShieldAlert, Sparkles, X } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { EdgeDetail } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

function formatStatus(value?: string | null) {
  if (!value) return '';
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatPercent(value?: number) {
  if (value === undefined || !Number.isFinite(value)) return '';
  return `${(value * 100).toFixed(0)}%`;
}

function providerModelLabel(provider?: string, model?: string) {
  if (!provider && !model) return '';
  if (!provider) return model ?? '';
  if (!model) return provider;
  return `${provider} / ${model}`;
}

function MetadataRow({
  label,
  value,
}: {
  label: string;
  value?: string | number | boolean | null;
}) {
  if (value === undefined || value === null || value === '') return null;
  return (
    <div className="grid grid-cols-[88px_minmax(0,1fr)] gap-2 text-xs leading-5">
      <span className="text-text-dim">{label}</span>
      <span className="min-w-0 break-words text-text">
        {typeof value === 'boolean' ? (value ? 'yes' : 'no') : value}
      </span>
    </div>
  );
}

function TextBlock({
  label,
  value,
}: {
  label: string;
  value?: string | null;
}) {
  if (!value) return null;
  return (
    <div>
      <div className="mb-1 text-xs uppercase tracking-wider text-text-dim">{label}</div>
      <div className="break-words text-sm leading-relaxed">{value}</div>
    </div>
  );
}

export default function EdgeInspector({ detail }: { detail: EdgeDetail }) {
  const { edge, source, target } = detail;
  const setSelectedNode = useSceneStore((s) => s.setSelectedNode);
  const setSelectedEdge = useSceneStore((s) => s.setSelectedEdge);
  const openBottom = useSceneStore((s) => s.openBottom);
  const confidence = edge.confidenceScore ?? edge.confidence;
  const isPendingOverlay = Boolean(edge.pendingOnly || edge.type.startsWith('PENDING_'));
  const isNodeConsolidation = edge.type.startsWith('PENDING_NODE_CONSOLIDATION');
  const evidenceText = edge.evidence;
  const rationaleText = edge.rationale || edge.reasoning;
  const distinctReasoning = edge.reasoning && edge.reasoning !== rationaleText ? edge.reasoning : '';
  const providerRows = [
    {
      label: 'Judge',
      value: providerModelLabel(edge.effectiveJudgeProvider || edge.judgeProvider, edge.effectiveJudgeModel || edge.judgeModel),
    },
    {
      label: 'Verifier',
      value: providerModelLabel(edge.effectiveVerifierProvider || edge.verifierProvider, edge.effectiveVerifierModel || edge.verifierModel),
    },
    {
      label: 'Adjudicator',
      value: providerModelLabel(edge.effectiveAdjudicatorProvider || edge.adjudicatorProvider, edge.effectiveAdjudicatorModel || edge.adjudicatorModel),
    },
  ].filter((row) => row.value);

  return (
    <div className="flex flex-col h-full p-4 space-y-4">
      <div className="flex items-start justify-between">
        <div className="min-w-0">
          <h2 className="break-words text-sm font-semibold text-accent">{edge.type}</h2>
          {isPendingOverlay && (
            <div className="mt-1 flex flex-wrap items-center gap-1.5 text-[10px] text-text-dim">
              <span className="inline-flex items-center gap-1 rounded border border-amber-300/25 bg-amber-300/10 px-1.5 py-0.5 text-amber-100">
                <ShieldAlert size={10} />
                Pending only
              </span>
              {edge.reviewStatus && (
                <span className="rounded border border-border bg-bg/40 px-1.5 py-0.5">
                  {formatStatus(edge.reviewStatus)}
                </span>
              )}
            </div>
          )}
        </div>
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
      {isPendingOverlay && (
        <div className="space-y-2 rounded-lg border border-border bg-bg/35 p-3">
          <div className="flex items-center gap-2 text-xs font-medium text-text">
            {isNodeConsolidation ? <GitMerge size={13} /> : <Sparkles size={13} />}
            Overlay decision
          </div>
          <div className="space-y-1">
            <MetadataRow label="Run" value={edge.improvementRunId} />
            <MetadataRow label="Decision" value={formatStatus(edge.resolutionDecision || edge.stewardDecision || edge.reviewStatus)} />
            <MetadataRow label="Admission" value={formatStatus(edge.admissionStatus)} />
            <MetadataRow label="Category" value={formatStatus(edge.semanticOverlayCategory)} />
            <MetadataRow label="Method" value={edge.generationMethod} />
            <MetadataRow label="Mutation" value={edge.activeGraphMutation === undefined ? 'false' : String(edge.activeGraphMutation)} />
          </div>
        </div>
      )}
      {(confidence !== undefined || edge.rawSimilarity !== undefined) && (
        <div className="grid grid-cols-2 gap-2">
          {confidence !== undefined && (
            <div className="rounded-lg border border-border bg-bg/35 px-3 py-2">
              <div className="text-[10px] uppercase tracking-[0.14em] text-text-dim">Confidence</div>
              <div className="mt-1 text-sm font-semibold text-text">{formatPercent(confidence)}</div>
            </div>
          )}
          {edge.rawSimilarity !== undefined && Number.isFinite(edge.rawSimilarity) && (
            <div className="rounded-lg border border-border bg-bg/35 px-3 py-2">
              <div className="text-[10px] uppercase tracking-[0.14em] text-text-dim">Similarity</div>
              <div className="mt-1 text-sm font-semibold text-text">{formatPercent(edge.rawSimilarity)}</div>
            </div>
          )}
        </div>
      )}
      <TextBlock label={isPendingOverlay ? 'Rationale' : 'Reasoning'} value={rationaleText} />
      {distinctReasoning && <TextBlock label="Reasoning" value={distinctReasoning} />}
      <TextBlock label="Evidence" value={evidenceText} />
      {providerRows.length > 0 && (
        <div className="space-y-2 rounded-lg border border-border bg-bg/35 p-3">
          <div className="flex items-center gap-2 text-xs font-medium text-text">
            <BadgeCheck size={13} />
            Provider route
          </div>
          <div className="space-y-1">
            {providerRows.map((row) => (
              <MetadataRow key={row.label} label={row.label} value={row.value} />
            ))}
          </div>
          {edge.providerRoute && edge.providerRoute.length > 0 && (
            <div className="flex flex-wrap gap-1.5 pt-1">
              {edge.providerRoute.map((route, index) => (
                <span
                  key={`${route.role}-${route.provider}-${route.model}-${index}`}
                  className="rounded border border-border bg-bg/50 px-1.5 py-0.5 text-[10px] text-text-dim"
                >
                  {formatStatus(route.role)}: {providerModelLabel(route.provider, route.model) || 'unknown'} {route.status ? `(${route.status})` : ''}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
      {isNodeConsolidation && (
        <div className="space-y-1 rounded-lg border border-border bg-bg/35 p-3">
          <MetadataRow label="Survivor" value={edge.canonicalSurvivorId} />
          <MetadataRow label="Label" value={edge.suggestedCanonicalLabel} />
          <MetadataRow label="Auto merge" value={edge.autoMergeAllowed === undefined ? 'false' : String(edge.autoMergeAllowed)} />
          <MetadataRow label="Batch merge" value={edge.batchMergeBlocked === undefined ? 'blocked' : edge.batchMergeBlocked ? 'blocked' : 'allowed'} />
        </div>
      )}
      {edge.resolutionNote && <TextBlock label="Steward note" value={edge.resolutionNote} />}
      {edge.admissionReviewReasons && edge.admissionReviewReasons.length > 0 && (
        <div>
          <div className="mb-1 text-xs uppercase tracking-wider text-text-dim">Review reasons</div>
          <div className="flex flex-wrap gap-1.5">
            {edge.admissionReviewReasons.map((reason) => (
              <span key={reason} className="rounded border border-border bg-bg/40 px-1.5 py-0.5 text-[10px] text-text-dim">
                {formatStatus(reason)}
              </span>
            ))}
          </div>
        </div>
      )}
      {edge.assertionId && (
        <div>
          <div className="text-xs uppercase tracking-wider text-text-dim mb-1">Assertion ID</div>
          <div className="break-all text-xs font-mono text-text-dim">{edge.assertionId}</div>
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
      ) : evidenceText ? (
        <div className="flex items-center gap-2 text-xs text-text-dim">
          <FileText size={12} />
          Artifact evidence shown above.
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
