import { AlertTriangle, CheckCircle2, ClipboardCheck, FileText, GitMerge, Layers3, ListTree, RefreshCcw, SearchCheck, ShieldCheck, Sparkles } from 'lucide-react';
import { useState, type ReactNode } from 'react';
import type {
  BackboneEvidencePreview,
  BackboneImprovementOverlayPreview,
  BackbonePlacementQaPreview,
  BackboneSummary,
  BackboneTaxonomyPreview,
  SourceGapWorkqueuePreview,
} from '../../types';

interface BackbonePreviewPanelProps {
  summary: BackboneSummary | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
  taxonomyPreview: BackboneTaxonomyPreview | null;
  taxonomyLoading: boolean;
  taxonomyError: string | null;
  onLoadTaxonomyPreview: () => void;
  placementQaPreview: BackbonePlacementQaPreview | null;
  placementQaLoading: boolean;
  placementQaError: string | null;
  onLoadPlacementQaPreview: () => void;
  evidencePreview: BackboneEvidencePreview | null;
  evidenceLoading: boolean;
  evidenceError: string | null;
  onLoadEvidencePreview: () => void;
  improvementOverlayPreview?: BackboneImprovementOverlayPreview | null;
  improvementOverlayLoading?: boolean;
  improvementOverlayError?: string | null;
  onLoadImprovementOverlayPreview?: () => void;
  sourceGapPreview?: SourceGapWorkqueuePreview | null;
  sourceGapLoading?: boolean;
  sourceGapError?: string | null;
  onLoadSourceGapPreview?: () => void;
  onOpenSourceGapNode?: (nodeId: string) => void;
  onShowApprovedOverlays?: () => void;
  onShowNeedsEvidenceOverlays?: () => void;
  onShowRelationshipOverlays?: () => void;
  onShowNodeConsolidationOverlays?: () => void;
  onShowAllOverlays?: () => void;
}

function formatCount(value: number) {
  return value.toLocaleString();
}

function formatNullableCount(value: number | null) {
  return value === null ? 'unknown' : formatCount(value);
}

function formatNullableBoolean(value: boolean | null) {
  if (value === null) return 'unknown';
  return value ? 'yes' : 'no';
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

function compactQueueLabel(value: string) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatScore(value: number) {
  if (!Number.isFinite(value)) return 'unknown';
  return value <= 1 ? value.toFixed(3) : value.toFixed(2);
}

function compactMaybe(value: string | null | undefined, fallback = 'none') {
  return value && value.trim().length > 0 ? value : fallback;
}

function OverlayLegendRow({
  icon,
  label,
  count,
  tone,
}: {
  icon: ReactNode;
  label: string;
  count: number;
  tone: 'approved' | 'review';
}) {
  return (
    <div className="flex items-center justify-between gap-2 rounded border border-border bg-bg/40 px-2 py-1.5">
      <div className="flex min-w-0 items-center gap-2">
        <span className={tone === 'approved' ? 'text-emerald-200' : 'text-amber-200'}>
          {icon}
        </span>
        <span className="min-w-0 truncate text-[11px] text-text-dim">{label}</span>
      </div>
      <span className="shrink-0 text-xs font-semibold text-text">{formatCount(count)}</span>
    </div>
  );
}

function OverlayFilterButton({
  label,
  onClick,
}: {
  label: string;
  onClick?: () => void;
}) {
  return (
    <button
      type="button"
      className="kg-control min-h-7 w-full rounded px-2 py-1 text-[10px] font-medium text-text-dim transition-colors hover:text-accent disabled:cursor-not-allowed disabled:opacity-45"
      onClick={onClick}
      disabled={!onClick}
    >
      {label}
    </button>
  );
}

export default function BackbonePreviewPanel({
  summary,
  loading,
  error,
  onRefresh,
  taxonomyPreview,
  taxonomyLoading,
  taxonomyError,
  onLoadTaxonomyPreview,
  placementQaPreview,
  placementQaLoading,
  placementQaError,
  onLoadPlacementQaPreview,
  evidencePreview,
  evidenceLoading,
  evidenceError,
  onLoadEvidencePreview,
  improvementOverlayPreview,
  improvementOverlayLoading,
  improvementOverlayError,
  onLoadImprovementOverlayPreview = () => {},
  sourceGapPreview,
  sourceGapLoading,
  sourceGapError,
  onLoadSourceGapPreview = () => {},
  onOpenSourceGapNode,
  onShowApprovedOverlays,
  onShowNeedsEvidenceOverlays,
  onShowRelationshipOverlays,
  onShowNodeConsolidationOverlays,
  onShowAllOverlays,
}: BackbonePreviewPanelProps) {
  const [sourceGapFilter, setSourceGapFilter] = useState<'all' | 'node' | 'relationship'>('all');
  const [expandedSourceGapId, setExpandedSourceGapId] = useState<string | null>(null);
  const backboneNodeLevels = taxonomyPreview
    ? [...taxonomyPreview.backboneNodes.reduce((levels, node) => {
      levels.set(node.level, (levels.get(node.level) ?? 0) + 1);
      return levels;
    }, new Map<number, number>()).entries()].sort((a, b) => a[0] - b[0])
    : [];
  const shadowGraph = taxonomyPreview?.shadowGraph;
  const improvementCounts = improvementOverlayPreview?.counts;
  const approvedRelationshipCount = improvementCounts?.relationshipAdmissionReady ?? 0;
  const approvedNodeConsolidationCount = improvementCounts?.nodeConsolidationAccepted ?? 0;
  const relationshipNeedsEvidenceCount = Math.max(
    0,
    (improvementCounts?.projectedRelationshipOverlayEdges ?? 0) - approvedRelationshipCount,
  );
  const nodeConsolidationNeedsEvidenceCount = Math.max(
    0,
    (improvementCounts?.projectedNodeConsolidationOverlayEdges ?? 0) - approvedNodeConsolidationCount,
  );
  const sourceGapItems = sourceGapPreview?.items ?? [];
  const sourceGapProposalById = new Map((sourceGapPreview?.proposals ?? []).map((proposal) => [proposal.proposalId, proposal]));
  const filteredSourceGapItems = sourceGapItems.filter((item) => {
    if (sourceGapFilter === 'node') return item.itemType === 'node_resource_gap';
    if (sourceGapFilter === 'relationship') return item.itemType === 'relationship_source_gap';
    return true;
  });

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
        <div className="flex shrink-0 items-center gap-1.5">
          <button
            className={`kg-control flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${taxonomyPreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={onLoadTaxonomyPreview}
            title="Load taxonomy readiness details"
            aria-label="Load taxonomy readiness details"
            disabled={taxonomyLoading}
          >
            <ListTree size={13} />
          </button>
          <button
            className={`kg-control flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${placementQaPreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={onLoadPlacementQaPreview}
            title="Load placement QA summary"
            aria-label="Load placement QA summary"
            disabled={placementQaLoading}
          >
            <ClipboardCheck size={13} />
          </button>
          <button
            className={`kg-control flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${evidencePreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={onLoadEvidencePreview}
            title="Load evidence summary"
            aria-label="Load evidence summary"
            disabled={evidenceLoading}
          >
            <FileText size={13} />
          </button>
          <button
            className={`kg-control flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${improvementOverlayPreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={onLoadImprovementOverlayPreview}
            title="Load pending improvement overlay"
            aria-label="Load pending improvement overlay"
            disabled={improvementOverlayLoading}
          >
            <Sparkles size={13} />
          </button>
          <button
            className={`kg-control flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${sourceGapPreview ? 'text-accent border-accent/60' : 'text-text-dim'}`}
            onClick={onLoadSourceGapPreview}
            title="Load source-gap workqueue"
            aria-label="Load source-gap workqueue"
            disabled={sourceGapLoading}
          >
            <SearchCheck size={13} />
          </button>
          <button
            className="kg-control flex h-8 w-8 items-center justify-center rounded-lg text-text-dim transition-colors"
            onClick={onRefresh}
            title="Refresh backbone preview"
            aria-label="Refresh backbone preview"
            disabled={loading}
          >
            <RefreshCcw size={13} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
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
          <div className="grid grid-cols-3 gap-2">
            <div className="rounded-lg border border-border bg-bg/40 px-2 py-2">
              <div className="text-[9px] uppercase tracking-[0.14em] text-text-dim">Predicates</div>
              <div className="mt-1 text-base font-semibold text-text">{formatCount(summary.counts.predicateRegistry)}</div>
            </div>
            <div className="rounded-lg border border-border bg-bg/40 px-2 py-2">
              <div className="text-[9px] uppercase tracking-[0.14em] text-text-dim">Sources</div>
              <div className="mt-1 text-base font-semibold text-text">{formatCount(summary.counts.sourceRightsRegistry)}</div>
            </div>
            <div className="rounded-lg border border-border bg-bg/40 px-2 py-2">
              <div className="text-[9px] uppercase tracking-[0.14em] text-text-dim">Nodes</div>
              <div className="mt-1 text-base font-semibold text-text">{formatCount(summary.counts.backboneNodes)}</div>
            </div>
          </div>

          <div className="space-y-1.5 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <BoundaryRow label="Shadow only" clear={summary.boundaries.shadowOnly} />
            <BoundaryRow label="File-backed" clear={summary.boundaries.fileBackedOnly} />
            <BoundaryRow label="No live graph writes" clear={!summary.boundaries.liveNeo4jWrites} />
            <BoundaryRow label="No live Explorer mutation" clear={!summary.boundaries.apiExplorerCutover} />
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

          <div className="space-y-2 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <div className="flex items-center justify-between gap-2 text-[11px]">
              <span className="font-medium text-text">Pending improvements</span>
              <span className="text-text-dim">
                {improvementOverlayPreview ? 'Loaded' : improvementOverlayLoading ? 'Loading' : 'Not loaded'}
              </span>
            </div>
            {improvementOverlayError ? (
              <div className="text-[11px] leading-5 text-rose-100">{improvementOverlayError}</div>
            ) : improvementOverlayLoading ? (
              <div className="text-[11px] leading-5 text-text-dim">Loading relationship-improvement overlay...</div>
            ) : improvementOverlayPreview ? (
              <div className="space-y-2">
                <div className="rounded-lg border border-amber-400/20 bg-amber-400/10 p-2 text-[11px] leading-5 text-amber-100">
                  Pending-only overlay. These relationship and node-consolidation candidates are not admitted graph data.
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Rel edges</div>
                    <div className="text-xs font-semibold text-text">{formatCount(improvementOverlayPreview.counts.projectedRelationshipOverlayEdges)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Node pairs</div>
                    <div className="text-xs font-semibold text-text">{formatCount(improvementOverlayPreview.counts.projectedNodeConsolidationOverlayEdges)}</div>
                  </div>
                </div>
                <div className="space-y-1.5">
                  <div className="grid grid-cols-1 gap-1.5">
                    <OverlayLegendRow
                      icon={<CheckCircle2 size={12} />}
                      label="Approved relationship overlays"
                      count={approvedRelationshipCount}
                      tone="approved"
                    />
                    <OverlayLegendRow
                      icon={<GitMerge size={12} />}
                      label="Alias-approved node pairs"
                      count={approvedNodeConsolidationCount}
                      tone="approved"
                    />
                    <OverlayLegendRow
                      icon={<SearchCheck size={12} />}
                      label="Relationship needs evidence"
                      count={relationshipNeedsEvidenceCount}
                      tone="review"
                    />
                    <OverlayLegendRow
                      icon={<Layers3 size={12} />}
                      label="Node pair needs evidence"
                      count={nodeConsolidationNeedsEvidenceCount}
                      tone="review"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-1.5">
                    <OverlayFilterButton label="Approved only" onClick={onShowApprovedOverlays} />
                    <OverlayFilterButton label="Needs evidence" onClick={onShowNeedsEvidenceOverlays} />
                    <OverlayFilterButton label="Relationships" onClick={onShowRelationshipOverlays} />
                    <OverlayFilterButton label="Node consolidations" onClick={onShowNodeConsolidationOverlays} />
                    <div className="col-span-2">
                      <OverlayFilterButton label="All overlay" onClick={onShowAllOverlays} />
                    </div>
                  </div>
                </div>
                <div className="space-y-1 text-[11px] leading-5 text-text-dim">
                  <div>Run: {improvementOverlayPreview.runId || 'none'}</div>
                  <div>Status: {improvementOverlayPreview.enabled ? (improvementOverlayPreview.available ? 'available' : 'no artifacts') : 'disabled'}</div>
                  <div>Relationship accepted/review: {formatCount(improvementOverlayPreview.counts.relationshipAccepted)}/{formatCount(improvementOverlayPreview.counts.relationshipNeedsReview)}</div>
                  <div>Node accepted/review: {formatCount(improvementOverlayPreview.counts.nodeConsolidationAccepted)}/{formatCount(improvementOverlayPreview.counts.nodeConsolidationNeedsReview)}</div>
                  <div>Admission-ready rels: {formatCount(improvementOverlayPreview.counts.relationshipAdmissionReady ?? 0)}</div>
                  <div>Node steward actions: {formatCount(improvementOverlayPreview.counts.nodeConsolidationStewardActions ?? 0)}</div>
                  <div>Resolution queue: {formatCount(improvementOverlayPreview.counts.totalResolutionWorkqueue ?? 0)}</div>
                  <div>Recorded decisions: {formatCount(improvementOverlayPreview.counts.totalResolutionDecisions ?? 0)}</div>
                  <div>Displayed overlay edges: {formatCount(improvementOverlayPreview.counts.projectedRelationshipOverlayEdges + improvementOverlayPreview.counts.projectedNodeConsolidationOverlayEdges)}</div>
                  {(improvementOverlayPreview.counts.skippedInvalid > 0 || improvementOverlayPreview.counts.skippedDuplicateActive > 0) && (
                    <div>Skipped overlay rows: {formatCount(improvementOverlayPreview.counts.skippedInvalid + improvementOverlayPreview.counts.skippedDuplicateActive)}</div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-[11px] leading-5 text-text-dim">
                Use the sparkle control to inspect the latest pending improvement run.
              </div>
            )}
          </div>

          <div className="space-y-2 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <div className="flex items-center justify-between gap-2 text-[11px]">
              <span className="font-medium text-text">Source gaps</span>
              <span className="text-text-dim">
                {sourceGapPreview ? 'Loaded' : sourceGapLoading ? 'Loading' : 'Not loaded'}
              </span>
            </div>
            {sourceGapError ? (
              <div className="text-[11px] leading-5 text-rose-100">{sourceGapError}</div>
            ) : sourceGapLoading ? (
              <div className="text-[11px] leading-5 text-text-dim">Loading source-gap workqueue...</div>
            ) : sourceGapPreview ? (
              <div className="space-y-2">
                <div className="rounded-lg border border-amber-400/20 bg-amber-400/10 p-2 text-[11px] leading-5 text-amber-100">
                  Review-only source-link proposals. This view does not create Resource Layer links or mutate graph/database state.
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Returned</div>
                    <div className="text-xs font-semibold text-text">{formatCount(sourceGapPreview.counts.returnedWorkqueueItems)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Total gaps</div>
                    <div className="text-xs font-semibold text-text">{formatCount(sourceGapPreview.counts.totalWorkqueueItems)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Node gaps</div>
                    <div className="text-xs font-semibold text-text">{formatCount(sourceGapPreview.counts.nodeResourceGaps)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Rel gaps</div>
                    <div className="text-xs font-semibold text-text">{formatCount(sourceGapPreview.counts.relationshipSourceGaps)}</div>
                  </div>
                </div>
                <div className="space-y-1 text-[11px] leading-5 text-text-dim">
                  <div>Source-link proposals: {formatCount(sourceGapPreview.counts.totalSourceLinkProposals)}</div>
                  <div>Returned proposals: {formatCount(sourceGapPreview.counts.returnedSourceLinkProposals)}</div>
                  <div className="truncate" title={sourceGapPreview.runId || ''}>Inventory run: {sourceGapPreview.runId || 'none'}</div>
                  <div>Status: {sourceGapPreview.available ? 'available' : 'no artifacts'}</div>
                </div>
                <div className="grid grid-cols-3 gap-1">
                  {([
                    ['all', 'All'],
                    ['node', 'Nodes'],
                    ['relationship', 'Relationships'],
                  ] as const).map(([filter, label]) => (
                    <button
                      key={filter}
                      type="button"
                      className={`kg-control min-h-7 rounded px-1.5 py-1 text-[10px] font-medium transition-colors ${sourceGapFilter === filter ? 'border-accent/60 text-accent' : 'text-text-dim hover:text-text'}`}
                      onClick={() => setSourceGapFilter(filter)}
                    >
                      {label}
                    </button>
                  ))}
                </div>
                {filteredSourceGapItems.length > 0 ? (
                  <div className="space-y-1.5">
                    <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Top workqueue items</div>
                    {filteredSourceGapItems.slice(0, 4).map((item) => {
                      const title = item.itemType === 'relationship_source_gap'
                        ? `${item.fromLabel || item.fromId || 'Relationship'} ${item.predicate || ''} ${item.toLabel || item.toId || ''}`.trim()
                        : item.nodeLabel || item.nodeId || item.workqueueId;
                      const nodeTargets = item.itemType === 'relationship_source_gap'
                        ? [
                          { label: 'From', nodeId: item.fromId },
                          { label: 'To', nodeId: item.toId },
                        ]
                        : [{ label: 'Open node', nodeId: item.nodeId }];
                      const availableTargets = nodeTargets.filter((target): target is { label: string; nodeId: string } => Boolean(target.nodeId));
                      const matchedProposals = item.proposalIds
                        .map((proposalId) => sourceGapProposalById.get(proposalId))
                        .filter((proposal): proposal is NonNullable<typeof proposal> => Boolean(proposal))
                        .slice(0, 2);
                      const expanded = expandedSourceGapId === item.workqueueId;
                      return (
                        <div key={item.workqueueId} className="rounded border border-border bg-bg/40 px-2 py-1.5">
                          <div className="flex items-center justify-between gap-2 text-[11px]">
                            <span className="min-w-0 truncate text-text" title={title}>{title}</span>
                            <span className="shrink-0 text-text-dim">#{formatCount(item.priorityRank)}</span>
                          </div>
                          <div className="mt-1 flex items-center justify-between gap-2 text-[10px] text-text-dim">
                            <span>{compactQueueLabel(item.itemType)}</span>
                            <span>{item.suggestedResources.length} resource hints</span>
                          </div>
                          {item.suggestedResources[0] && (
                            <div className="mt-1 truncate text-[10px] text-amber-100" title={item.suggestedResources[0].title}>
                              {item.suggestedResources[0].title}
                            </div>
                          )}
                          <div className="mt-2 flex items-center justify-between gap-2">
                            <button
                              type="button"
                              className="kg-control min-h-6 rounded px-1.5 py-0.5 text-[10px] text-text-dim transition-colors hover:text-accent"
                              aria-expanded={expanded}
                              aria-label={`${expanded ? 'Hide' : 'Show'} source-gap details for ${title}`}
                              onClick={() => setExpandedSourceGapId(expanded ? null : item.workqueueId)}
                            >
                              {expanded ? 'Hide details' : 'Details'}
                            </button>
                            <span className="text-[10px] text-text-dim">score {formatScore(item.priorityScore)}</span>
                          </div>
                          {availableTargets.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {availableTargets.map((target) => (
                                <button
                                  key={`${item.workqueueId}-${target.label}-${target.nodeId}`}
                                  type="button"
                                  className="kg-control min-h-6 rounded px-1.5 py-0.5 text-[10px] text-text-dim transition-colors hover:text-accent disabled:cursor-not-allowed disabled:opacity-45"
                                  onClick={() => onOpenSourceGapNode?.(target.nodeId)}
                                  disabled={!onOpenSourceGapNode}
                                >
                                  {target.label}
                                </button>
                              ))}
                            </div>
                          )}
                          {expanded && (
                            <div className="mt-2 space-y-2 rounded border border-border/80 bg-bg/50 p-2 text-[10px] leading-4 text-text-dim">
                              <div className="grid grid-cols-2 gap-x-2 gap-y-1">
                                <div>Workqueue: <span className="text-text">{item.workqueueId}</span></div>
                                <div>Action: <span className="text-text">{compactQueueLabel(item.finalAction)}</span></div>
                                <div>Class: <span className="text-text">{compactQueueLabel(item.classification)}</span></div>
                                <div>Status: <span className="text-text">{compactQueueLabel(item.sourceBackingStatus)}</span></div>
                                <div>Degree: <span className="text-text">{formatCount(item.degree)}</span></div>
                                <div>Priority: <span className="text-text">{formatScore(item.priorityScore)}</span></div>
                              </div>
                              <div className="space-y-0.5">
                                <div>Node: <span className="text-text">{compactMaybe(item.nodeId)}</span></div>
                                <div>Edge: <span className="text-text">{compactMaybe(item.edgeKey)}</span></div>
                                {item.itemType === 'relationship_source_gap' && (
                                  <div>
                                    Endpoints: <span className="text-text">{compactMaybe(item.fromId)} - {compactMaybe(item.predicate)} - {compactMaybe(item.toId)}</span>
                                  </div>
                                )}
                              </div>
                              {item.suggestedResources.length > 0 && (
                                <div className="space-y-1">
                                  <div className="text-[9px] uppercase tracking-[0.14em] text-text-dim">Resource hints</div>
                                  {item.suggestedResources.slice(0, 2).map((resource) => (
                                    <div key={`${item.workqueueId}-${resource.resourceId}`} className="rounded border border-border bg-bg/40 p-1.5">
                                      <div className="truncate text-amber-100" title={resource.title}>{resource.title}</div>
                                      <div>Resource: <span className="text-text">{resource.resourceId}</span> · score {formatScore(resource.score)}</div>
                                      {resource.matchedTerms.length > 0 && (
                                        <div className="truncate" title={resource.matchedTerms.join(', ')}>
                                          Matched: <span className="text-text">{resource.matchedTerms.join(', ')}</span>
                                        </div>
                                      )}
                                      {resource.suggestedRelationship && (
                                        <div>Suggested: <span className="text-text">{compactQueueLabel(resource.suggestedRelationship)}</span></div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                              {matchedProposals.length > 0 && (
                                <div className="space-y-1">
                                  <div className="text-[9px] uppercase tracking-[0.14em] text-text-dim">Source-link proposals</div>
                                  {matchedProposals.map((proposal) => (
                                    <div key={proposal.proposalId} className="rounded border border-border bg-bg/40 p-1.5">
                                      <div className="truncate text-text" title={proposal.title}>{proposal.title}</div>
                                      <div>Proposal: <span className="text-text">{proposal.proposalId}</span> · {compactQueueLabel(proposal.reviewStatus)}</div>
                                      <div>Relationship: <span className="text-text">{compactQueueLabel(proposal.suggestedRelationship)}</span> · score {formatScore(proposal.score)}</div>
                                      {proposal.matchedTerms.length > 0 && (
                                        <div className="truncate" title={proposal.matchedTerms.join(', ')}>
                                          Matched: <span className="text-text">{proposal.matchedTerms.join(', ')}</span>
                                        </div>
                                      )}
                                      <div className="line-clamp-2 text-text-dim" title={proposal.rationale}>{proposal.rationale}</div>
                                    </div>
                                  ))}
                                </div>
                              )}
                              <div className="rounded border border-amber-400/20 bg-amber-400/10 px-1.5 py-1 text-amber-100">
                                Pending-only detail: no source link is created and no graph or database state is changed from this panel.
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="text-[11px] leading-5 text-text-dim">No source gaps match this filter.</div>
                )}
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Safety</div>
                  <BoundaryRow label="Read-only" clear={sourceGapPreview.safetyBoundaries.readOnly} />
                  <BoundaryRow label="No active graph mutation" clear={!sourceGapPreview.safetyBoundaries.activeGraphMutation} />
                  <BoundaryRow label="No Resource Layer mutation" clear={!sourceGapPreview.safetyBoundaries.resourceLayerMutation} />
                  <BoundaryRow label="No database writes" clear={!sourceGapPreview.safetyBoundaries.neo4jWrites && !sourceGapPreview.safetyBoundaries.postgresWrites} />
                  <BoundaryRow label="No protected source text" clear={!sourceGapPreview.safetyBoundaries.protectedSourceTextIncluded} />
                </div>
              </div>
            ) : (
              <div className="text-[11px] leading-5 text-text-dim">
                Use the source-gap control to inspect source/resource attachment gaps across the graph.
              </div>
            )}
          </div>

          <div className="space-y-2 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <div className="flex items-center justify-between gap-2 text-[11px]">
              <span className="font-medium text-text">Readiness details</span>
              <span className="text-text-dim">
                {taxonomyPreview ? 'Loaded' : taxonomyLoading ? 'Loading' : 'Not loaded'}
              </span>
            </div>
            {taxonomyError ? (
              <div className="text-[11px] leading-5 text-rose-100">{taxonomyError}</div>
            ) : taxonomyLoading ? (
              <div className="text-[11px] leading-5 text-text-dim">Loading registry metadata...</div>
            ) : taxonomyPreview ? (
              <div className="space-y-2">
                <div className="text-[11px] leading-5 text-text-dim">
                  Canonical tree: {taxonomyPreview.readiness.canonicalTaxonomyTreeAvailable ? 'available' : 'not admitted yet'}
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Backbone nodes</div>
                  <div className="flex items-center justify-between gap-2 text-[11px]">
                    <span className="text-text-dim">
                      {taxonomyPreview.readiness.backboneNodesAvailable ? 'Admitted preview' : 'No admitted preview'}
                    </span>
                    <span className="text-text">{formatCount(taxonomyPreview.backboneNodes.length)}</span>
                  </div>
                  {backboneNodeLevels.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {backboneNodeLevels.map(([level, count]) => (
                        <span key={level} className="rounded border border-border bg-bg/40 px-1.5 py-0.5 text-[10px] text-text-dim">
                          L{level}: {formatCount(count)}
                        </span>
                      ))}
                    </div>
                  )}
                  {taxonomyPreview.backboneNodes.slice(0, 6).map((node) => (
                    <div key={node.id} className="flex items-center justify-between gap-2 text-[11px]">
                      <span className="min-w-0 truncate text-text-dim" title={`${node.pathCode} - ${node.label}`}>
                        {node.pathCode} - {node.label}
                      </span>
                      <span className="text-text">L{node.level}</span>
                    </div>
                  ))}
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Shadow graph</div>
                  <div className="grid grid-cols-2 gap-1.5">
                    <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                      <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Nodes</div>
                      <div className="text-xs font-semibold text-text">{formatCount(shadowGraph?.counts.nodes ?? 0)}</div>
                    </div>
                    <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                      <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Edges</div>
                      <div className="text-xs font-semibold text-text">{formatCount(shadowGraph?.counts.edges ?? 0)}</div>
                    </div>
                  </div>
                  {shadowGraph?.edges.slice(0, 5).map((edge) => (
                    <div key={edge.id} className="flex items-center justify-between gap-2 text-[11px]">
                      <span className="min-w-0 truncate text-text-dim" title={`${edge.fromPathCode} -> ${edge.toPathCode}`}>
                        {edge.fromPathCode}{' -> '}{edge.toPathCode}
                      </span>
                      <span className="text-text">{edge.predicate}</span>
                    </div>
                  ))}
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Predicate categories</div>
                  {taxonomyPreview.predicateCategories.slice(0, 5).map((category) => (
                    <div key={category.category} className="flex items-center justify-between gap-2 text-[11px]">
                      <span className="min-w-0 truncate text-text-dim" title={category.predicates.join(', ')}>
                        {category.category}
                      </span>
                      <span className="text-text">{formatCount(category.count)}</span>
                    </div>
                  ))}
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Source clearance</div>
                  {taxonomyPreview.clearanceStates.map((state) => (
                    <div key={state.clearanceState} className="flex items-center justify-between gap-2 text-[11px]">
                      <span className="min-w-0 truncate text-text-dim" title={state.clearanceState}>
                        {compactQueueLabel(state.clearanceState)}
                      </span>
                      <span className="text-text">{formatCount(state.count)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-[11px] leading-5 text-text-dim">
                Use the detail control to inspect registry metadata.
              </div>
            )}
          </div>

          <div className="space-y-2 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <div className="flex items-center justify-between gap-2 text-[11px]">
              <span className="font-medium text-text">Placement QA</span>
              <span className="text-text-dim">
                {placementQaPreview ? 'Loaded' : placementQaLoading ? 'Loading' : 'Not loaded'}
              </span>
            </div>
            {placementQaError ? (
              <div className="text-[11px] leading-5 text-rose-100">{placementQaError}</div>
            ) : placementQaLoading ? (
              <div className="text-[11px] leading-5 text-text-dim">Loading placement QA...</div>
            ) : placementQaPreview ? (
              <div className="space-y-2">
                <div className="grid grid-cols-3 gap-1.5">
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Passed</div>
                    <div className="text-xs font-semibold text-text">
                      {formatCount(placementQaPreview.summary.casesPassed)}/{formatCount(placementQaPreview.summary.casesTotal)}
                    </div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Auto</div>
                    <div className="text-xs font-semibold text-text">{formatCount(placementQaPreview.summary.autoAcceptCases)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Failed</div>
                    <div className="text-xs font-semibold text-text">{formatCount(placementQaPreview.summary.casesFailed)}</div>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Coverage</div>
                  <BoundaryRow label="L1/L2 human review" clear={placementQaPreview.requiredCoverage.l1_l2_human_review} />
                  <BoundaryRow label="LD-8 auto-accept" clear={placementQaPreview.requiredCoverage.l3_l4_ld8_auto_accept} />
                  <BoundaryRow label="Legacy labels as aliases" clear={placementQaPreview.requiredCoverage.legacy_label_alias} />
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Safety</div>
                  <BoundaryRow label="No live graph writes" clear={!placementQaPreview.boundaries.liveNeo4jWrites} />
                  <BoundaryRow label="No KG rebuild" clear={!placementQaPreview.boundaries.kgRebuild} />
                  <BoundaryRow label="No live graph adoption" clear={!placementQaPreview.boundaries.explorerDefaultAdoption} />
                  <BoundaryRow label="No protected ingest" clear={!placementQaPreview.boundaries.protectedContentIngest} />
                </div>
                {Object.keys(placementQaPreview.summary.reviewQueueCounts).length > 0 && (
                  <div className="space-y-1">
                    <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Review queues</div>
                    {Object.entries(placementQaPreview.summary.reviewQueueCounts).map(([queue, count]) => (
                      <div key={queue} className="flex items-center justify-between gap-2 text-[11px]">
                        <span className="min-w-0 truncate text-text-dim" title={queue}>
                          {compactQueueLabel(queue)}
                        </span>
                        <span className="text-text">{formatCount(count)}</span>
                      </div>
                    ))}
                  </div>
                )}
                {placementQaPreview.warnings.length > 0 && (
                  <div className="text-[11px] leading-5 text-amber-100">
                    {placementQaPreview.warnings[0]}
                  </div>
                )}
                <div className="truncate text-[11px] text-text-dim" title={placementQaPreview.runId}>
                  QA run: {placementQaPreview.runId}
                </div>
              </div>
            ) : (
              <div className="text-[11px] leading-5 text-text-dim">
                Use the QA control to inspect placement readiness.
              </div>
            )}
          </div>

          <div className="space-y-2 rounded-lg border border-border bg-bg/30 px-2 py-2">
            <div className="flex items-center justify-between gap-2 text-[11px]">
              <span className="font-medium text-text">Evidence summary</span>
              <span className="text-text-dim">
                {evidencePreview ? 'Loaded' : evidenceLoading ? 'Loading' : 'Not loaded'}
              </span>
            </div>
            {evidenceError ? (
              <div className="text-[11px] leading-5 text-rose-100">{evidenceError}</div>
            ) : evidenceLoading ? (
              <div className="text-[11px] leading-5 text-text-dim">Loading evidence summary...</div>
            ) : evidencePreview ? (
              <div className="space-y-2">
                <div className="grid grid-cols-3 gap-1.5">
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Files</div>
                    <div className="text-xs font-semibold text-text">{formatCount(evidencePreview.summary.artifactCount)}</div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Routes</div>
                    <div className="text-xs font-semibold text-text">
                      {formatCount(evidencePreview.summary.previewRoutesPresent)}/{formatCount(evidencePreview.summary.previewRoutesRequired)}
                    </div>
                  </div>
                  <div className="rounded border border-border bg-bg/40 px-1.5 py-1">
                    <div className="text-[9px] uppercase tracking-[0.12em] text-text-dim">Checks</div>
                    <div className="text-xs font-semibold text-text">
                      {formatCount(evidencePreview.summary.boundaryChecksPassed)}/{formatCount(evidencePreview.summary.boundaryChecksTotal)}
                    </div>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Safety</div>
                  <BoundaryRow label="All artifacts ok" clear={evidencePreview.safetyInvariants.allArtifactsOk} />
                  <BoundaryRow label="No runtime promotion" clear={evidencePreview.safetyInvariants.noRuntimePromotion} />
                  <BoundaryRow label="Resolver routes absent or default-off" clear={evidencePreview.safetyInvariants.resolverRoutesAbsentOrDefaultOff} />
                  <BoundaryRow label="Runtime thresholds not evaluated" clear={evidencePreview.safetyInvariants.runtimeThresholdsNotEvaluated} />
                </div>
                <div className="space-y-1 text-[11px] leading-5 text-text-dim">
                  <div className="truncate" title={evidencePreview.summary.resolverRoutePolicy}>
                    Route policy: {compactQueueLabel(evidencePreview.summary.resolverRoutePolicy)}
                  </div>
                  <div className="truncate" title={evidencePreview.summary.benchmarkRuntimeThresholdDisposition}>
                    Threshold disposition: {compactQueueLabel(evidencePreview.summary.benchmarkRuntimeThresholdDisposition)}
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="text-[10px] uppercase tracking-[0.16em] text-text-dim">Evidence files</div>
                  {evidencePreview.evidenceFiles.slice(0, 6).map((file) => (
                    <div key={file.label} className="flex items-center justify-between gap-2 text-[11px]">
                      <span className="min-w-0 truncate text-text-dim" title={`${file.label} - ${file.path}`}>
                        {compactQueueLabel(file.label)}
                      </span>
                      <span className={file.ok ? 'text-emerald-200' : 'text-rose-200'}>
                        {file.ok ? 'OK' : 'Issue'}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="space-y-1 text-[11px] leading-5 text-text-dim">
                  <div>
                    Benchmark ops: {formatCount(evidencePreview.summary.benchmarkOperationsPassed)}
                    /{formatCount(evidencePreview.summary.benchmarkOperationsTotal)}
                  </div>
                  <div>Input hashes: {formatCount(evidencePreview.summary.inputHashCount)}</div>
                  <div className="truncate" title={evidencePreview.repoState.gitHeadCommit}>
                    Commit: {evidencePreview.repoState.gitHeadCommit}
                  </div>
                  <div>
                    Freshness fields: {evidencePreview.repoState.freshnessAvailable ? 'available' : 'unknown'}
                  </div>
                  <div>
                    Source dirty: {formatNullableBoolean(evidencePreview.repoState.sourceWorkingTreeDirtyAtGeneration)}
                  </div>
                  <div>
                    Source dirty paths: {formatNullableCount(evidencePreview.repoState.sourceDirtyPathCount)}
                  </div>
                  <div>
                    Evidence dirty: {formatNullableBoolean(evidencePreview.repoState.generatedEvidenceDirtyAtGeneration)}
                  </div>
                  <div>
                    Evidence dirty paths: {formatNullableCount(evidencePreview.repoState.generatedEvidenceDirtyPathCount)}
                  </div>
                  <div className="truncate" title={evidencePreview.runId}>Evidence run: {evidencePreview.runId}</div>
                </div>
              </div>
            ) : (
              <div className="text-[11px] leading-5 text-text-dim">
                Use the evidence control to inspect manifest health.
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="text-sm text-text-dim">Preview not loaded.</div>
      )}
    </section>
  );
}
