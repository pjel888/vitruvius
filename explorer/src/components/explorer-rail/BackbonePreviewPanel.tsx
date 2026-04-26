import { AlertTriangle, ClipboardCheck, FileText, ListTree, RefreshCcw, ShieldCheck } from 'lucide-react';
import type {
  BackboneEvidencePreview,
  BackbonePlacementQaPreview,
  BackboneSummary,
  BackboneTaxonomyPreview,
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

function compactQueueLabel(value: string) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
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
}: BackbonePreviewPanelProps) {
  const backboneNodeLevels = taxonomyPreview
    ? [...taxonomyPreview.backboneNodes.reduce((levels, node) => {
      levels.set(node.level, (levels.get(node.level) ?? 0) + 1);
      return levels;
    }, new Map<number, number>()).entries()].sort((a, b) => a[0] - b[0])
    : [];
  const shadowGraph = taxonomyPreview?.shadowGraph;

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
                      <span className="min-w-0 truncate text-text-dim">{state.clearanceState}</span>
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
                  <BoundaryRow label="No Explorer adoption" clear={!placementQaPreview.boundaries.explorerDefaultAdoption} />
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
                  <BoundaryRow label="Resolver routes unmounted" clear={evidencePreview.safetyInvariants.resolverRoutesUnmounted} />
                  <BoundaryRow label="Runtime thresholds not evaluated" clear={evidencePreview.safetyInvariants.runtimeThresholdsNotEvaluated} />
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
