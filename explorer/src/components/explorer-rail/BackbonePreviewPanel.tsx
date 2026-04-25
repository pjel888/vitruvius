import { AlertTriangle, RefreshCcw, ShieldCheck } from 'lucide-react';
import type { BackboneSummary } from '../../types';

interface BackbonePreviewPanelProps {
  summary: BackboneSummary | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
}

function formatCount(value: number) {
  return value.toLocaleString();
}

function BoundaryRow({ label, clear }: { label: string; clear: boolean }) {
  return (
    <div className="flex items-center justify-between gap-3 text-[11px]">
      <span className="min-w-0 truncate text-text-dim">{label}</span>
      <span className={clear ? 'text-emerald-200' : 'text-rose-200'}>
        {clear ? 'Clear' : 'Blocked'}
      </span>
    </div>
  );
}

export default function BackbonePreviewPanel({
  summary,
  loading,
  error,
  onRefresh,
}: BackbonePreviewPanelProps) {
  return (
    <section className="border-b border-border px-3 py-3" aria-label="AEC-MEPFS Backbone preview">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-text-dim">
            <ShieldCheck size={13} />
            AEC-MEPFS
          </div>
          <div className="mt-1 truncate text-[11px] text-text-dim">Shadow preview - read-only</div>
        </div>
        <button
          className="kg-control flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-text-dim transition-colors"
          onClick={onRefresh}
          title="Refresh backbone preview"
          aria-label="Refresh backbone preview"
          disabled={loading}
        >
          <RefreshCcw size={13} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      {loading ? (
        <div className="text-sm text-text-dim">Loading preview...</div>
      ) : error ? (
        <div className="space-y-2 rounded-lg border border-rose-400/25 bg-rose-400/10 p-3">
          <div className="flex items-center gap-2 text-sm text-rose-100">
            <AlertTriangle size={14} />
            Preview unavailable
          </div>
          <div className="text-[11px] leading-5 text-text-dim">{error}</div>
        </div>
      ) : summary ? (
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-2">
            <div className="rounded-lg border border-border bg-bg/40 px-2 py-2">
              <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Predicates</div>
              <div className="mt-1 text-base font-semibold text-text">{formatCount(summary.counts.predicateRegistry)}</div>
            </div>
            <div className="rounded-lg border border-border bg-bg/40 px-2 py-2">
              <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Sources</div>
              <div className="mt-1 text-base font-semibold text-text">{formatCount(summary.counts.sourceRightsRegistry)}</div>
            </div>
          </div>

          <div className="space-y-1.5 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <BoundaryRow label="Shadow only" clear={summary.boundaries.shadowOnly} />
            <BoundaryRow label="File-backed" clear={summary.boundaries.fileBackedOnly} />
            <BoundaryRow label="No live graph writes" clear={!summary.boundaries.liveNeo4jWrites} />
            <BoundaryRow label="No Explorer cutover" clear={!summary.boundaries.apiExplorerCutover} />
            <BoundaryRow label="No protected ingest" clear={!summary.boundaries.protectedContentIngest} />
          </div>

          <div className="space-y-1 text-[11px] leading-5 text-text-dim">
            <div>
              No ingest: {formatCount(summary.noIngestBoundaryCoverage.explicitNoIngestSourceCount)}
              /{formatCount(summary.noIngestBoundaryCoverage.sourcesTotal)} source blocks explicit
            </div>
            <div>Content ingest: {formatCount(summary.noIngestBoundaryCoverage.contentIngestSourceCount)}</div>
            <div className="truncate" title={summary.runId}>Run: {summary.runId}</div>
          </div>
        </div>
      ) : (
        <div className="text-sm text-text-dim">Preview not loaded.</div>
      )}
    </section>
  );
}
