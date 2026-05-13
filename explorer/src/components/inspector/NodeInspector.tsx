import { useState, type MouseEvent } from 'react';
import { AlertTriangle, ArrowRight, BookOpen, Check, CheckCircle2, Circle, Copy, ExternalLink, FileText, Flag, Focus, Globe2, HardDrive, MapPin, Pin, Route, Trash2, X } from 'lucide-react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { NodeDetail, RelationDetail, ResourceReference } from '../../types';
import { getDisplayLabel } from '../../utils/labels';
import { isPositiveResourceVerificationStatus } from '../../utils/resourceVerification';

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
  INFORMS: '#06b6d4',
  SUPPORTS: '#84cc16',
  RESISTS: '#d946ef',
  COLLECTS: '#f59e0b',
  CONVEYS: '#3b82f6',
  MITIGATES: '#10b981',
  DRAINS_TO: '#6366f1',
  CONNECTS_TO: '#64748b',
  TRANSFERS_LOAD_TO: '#f43f5e',
  DISCHARGES_TO: '#8b5cf6',
  COORDINATES_WITH: '#0ea5e9',
  CROSS_DOMAIN_ALIGNMENT: '#22c55e',
};

type InspectorTab = 'overview' | 'relationships' | 'sources' | 'context' | 'metadata';

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

function RelationList({
  title,
  relations,
  onSelectRelation,
  getHiddenReasons,
}: {
  title: string;
  relations: RelationDetail[];
  onSelectRelation: (relation: RelationDetail) => void;
  getHiddenReasons: (relation: RelationDetail) => string[];
}) {
  return (
    <div className="space-y-2">
      <div className="text-xs uppercase tracking-wider text-text-dim">{title}</div>
      {relations.length === 0 ? (
        <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
          No {title.toLowerCase()} relationships.
        </div>
      ) : relations.map((relation, index) => {
        const otherLabel = getDisplayLabel(relation.other);
        const hiddenReasons = getHiddenReasons(relation);
        const isVisible = hiddenReasons.length === 0;
        const relationBadges = [
          relation.reviewStatus ? `review ${formatResourceLabel(relation.reviewStatus)}` : null,
          relation.sourceFamilyIds?.length ? `source refs ${relation.sourceFamilyIds.length}` : null,
          relation.provenanceNote ? 'provenance note' : null,
        ].filter((badge): badge is string => Boolean(badge));
        return (
          <div
            key={`${relation.relType}-${relation.other.id}-${index}`}
            className="kg-card flex w-full items-start gap-2 border-l-2 rounded-xl pl-3 pr-2 py-2.5 transition-colors hover:bg-panel-hover"
            style={{ borderLeftColor: EDGE_COLORS[relation.relType] || '#6b7280' }}
          >
            <button
              className="min-w-0 flex-1 text-left"
              type="button"
              onClick={() => onSelectRelation(relation)}
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
              <div className="mt-1 flex flex-wrap gap-1">
                <span className={`rounded-full border px-1.5 py-0.5 text-[9px] uppercase tracking-[0.1em] ${
                  isVisible
                    ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-100'
                    : 'border-amber-400/30 bg-amber-400/10 text-amber-100'
                }`}>
                  {isVisible ? 'visible in graph' : `hidden: ${hiddenReasons.join(', ')}`}
                </span>
                {relation.isSemanticEdge && (
                  <span className="rounded-full border border-cyan-400/25 bg-cyan-400/10 px-1.5 py-0.5 text-[9px] uppercase tracking-[0.1em] text-cyan-100">
                    semantic
                  </span>
                )}
                {relation.isHierarchyEdge && (
                  <span className="rounded-full border border-slate-400/25 bg-slate-400/10 px-1.5 py-0.5 text-[9px] uppercase tracking-[0.1em] text-slate-100">
                    hierarchy
                  </span>
                )}
                {relationBadges.map((badge) => (
                  <span
                    key={badge}
                    className="rounded-full border border-violet-400/25 bg-violet-400/10 px-1.5 py-0.5 text-[9px] uppercase tracking-[0.1em] text-violet-100"
                  >
                    {badge}
                  </span>
                ))}
              </div>
              <div className="text-[11px] text-text-dim mt-0.5 truncate">{relation.other.id}</div>
              {relation.reasoning && <div className="text-xs text-text-dim mt-1 leading-relaxed">{relation.reasoning}</div>}
              {relation.provenanceNote && (
                <div className="mt-1 text-xs leading-relaxed text-text-dim">
                  <span className="text-text">Provenance:</span> {relation.provenanceNote}
                </div>
              )}
            </button>
            <CopyValueButton value={otherLabel} label={`Copy ${title.toLowerCase()} node name`} />
          </div>
        );
      })}
    </div>
  );
}

function Breadcrumbs({ nodes, onSelectNode }: { nodes: NodeDetail['taxonomyPath']; onSelectNode: (id: string) => void }) {
  if (nodes.length === 0) return null;
  return (
    <div className="kg-card rounded-xl p-3">
      <div className="mb-2 text-xs uppercase tracking-wider text-text-dim">Breadcrumbs</div>
      <div className="flex flex-wrap items-center gap-1.5 text-sm">
        {nodes.map((taxonomyNode, index) => (
          <span key={taxonomyNode.id} className="inline-flex items-center gap-1.5">
            {index > 0 && <span className="text-text-dim">/</span>}
            <button
              type="button"
              className="rounded-md px-1.5 py-0.5 text-accent transition-colors hover:bg-panel-hover hover:text-text"
              onClick={() => onSelectNode(taxonomyNode.id)}
              title={`Select ${getDisplayLabel(taxonomyNode)}`}
            >
              {getDisplayLabel(taxonomyNode)}
            </button>
          </span>
        ))}
      </div>
    </div>
  );
}

const RESOURCE_ELIGIBLE_NODE_TYPES = new Set([
  'concept',
  'rule',
  'definition',
  'procedure',
  'exception',
  'evidence',
  'evidence_span',
  'document',
  'document_version',
]);

function formatResourceLabel(value?: string | number) {
  if (value === undefined || value === null || value === '') return '';
  return String(value)
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatPercent(value?: number) {
  if (value === undefined || Number.isNaN(value)) return 'n/a';
  return `${Math.round(value * 100)}%`;
}

function formatCheckedAt(value?: string) {
  if (!value) return undefined;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString().slice(0, 10);
}

function ResourceBadge({ children, tone = 'neutral' }: { children: string; tone?: 'neutral' | 'good' | 'warn' }) {
  const toneClass = tone === 'good'
    ? 'border-emerald-400/25 bg-emerald-400/10 text-emerald-100'
    : tone === 'warn'
      ? 'border-amber-400/30 bg-amber-400/10 text-amber-100'
      : 'border-border bg-bg/60 text-text-dim';
  return (
    <span className={`rounded-full border px-2 py-0.5 text-[10px] uppercase tracking-wider ${toneClass}`}>
      {children}
    </span>
  );
}

function ResourceCard({ resource }: { resource: ResourceReference }) {
  const isLocal = Boolean(resource.localFileName);
  const reviewTone = resource.reviewStatus === 'accepted' || resource.reviewStatus === 'human_reviewed' ? 'good' : 'warn';
  const accessTone = resource.accessType === 'restricted' || resource.accessType === 'paywalled' ? 'warn' : 'neutral';
  const hasStandardsWarning = resource.warning?.includes('Standard context incomplete');
  const hasRightsWarning = resource.warning?.includes('Rights-protected') || resource.warning?.includes('Restricted or protected');
  const checkedAt = formatCheckedAt(resource.lastCheckedAt);
  const caveats = [
    resource.sourceTruthCaveat ? { label: 'Evidence', value: resource.sourceTruthCaveat } : undefined,
    resource.rightsCaveat ? { label: 'Rights', value: resource.rightsCaveat } : undefined,
    checkedAt ? { label: 'Checked', value: checkedAt } : undefined,
  ].filter((item): item is { label: string; value: string } => Boolean(item));
  const refs = [
    ...(resource.chapterRefs || []).map((ref) => `Chapter ${ref.replace(/^Chapter\s+/i, '')}`),
    ...(resource.sectionRefs || []).map((ref) => `Section ${ref.replace(/^Section\s+/i, '')}`),
    ...(resource.pageRefs || []).map((ref) => `Page ${ref.replace(/^Page\s+/i, '')}`),
  ];
  return (
    <div className="kg-card rounded-xl border-l-2 border-cyan-400/45 p-3">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-1 text-sm font-semibold text-text">
            <BookOpen size={14} className="shrink-0 text-accent" />
            <span className="break-words">{resource.title}</span>
          </div>
          {(resource.organization || resource.publisher || resource.year) && (
            <div className="mt-1 text-xs text-text-dim">
              {[resource.organization || resource.publisher, resource.year].filter(Boolean).join(' · ')}
            </div>
          )}
        </div>
        <div className="shrink-0 text-right text-[10px] text-text-dim">
          <div>{formatPercent(resource.displayScore)}</div>
          <div>rank</div>
        </div>
      </div>

      <div className="mt-2 flex flex-wrap gap-1.5">
        <ResourceBadge>{formatResourceLabel(resource.resourceType)}</ResourceBadge>
        <ResourceBadge tone={resource.sourceAuthority === 'general_web' ? 'warn' : 'good'}>{formatResourceLabel(resource.sourceAuthority)}</ResourceBadge>
        <ResourceBadge tone={isPositiveResourceVerificationStatus(resource.verificationStatus) ? 'good' : 'warn'}>{formatResourceLabel(resource.verificationStatus)}</ResourceBadge>
        <ResourceBadge tone={reviewTone}>{formatResourceLabel(resource.reviewStatus)}</ResourceBadge>
        {(resource.reviewStatus === 'accepted' || resource.reviewStatus === 'human_reviewed') && (
          <ResourceBadge tone="good">Learner Visible</ResourceBadge>
        )}
        <ResourceBadge tone={accessTone}>{isLocal ? 'Local' : formatResourceLabel(resource.accessType || 'online')}</ResourceBadge>
        {hasRightsWarning && (
          <ResourceBadge tone="warn">Rights</ResourceBadge>
        )}
        {hasStandardsWarning && (
          <ResourceBadge tone="warn">Standards</ResourceBadge>
        )}
      </div>

      <div className="mt-2 grid grid-cols-3 gap-2 rounded-lg border border-border/60 bg-bg/40 px-2 py-1.5 text-[11px] text-text-dim">
        <div><span className="text-text">Rel.</span> {formatPercent(resource.relevanceScore)}</div>
        <div><span className="text-text">Auth.</span> {formatPercent(resource.authorityScore)}</div>
        <div><span className="text-text">Conf.</span> {formatPercent(resource.confidenceScore)}</div>
      </div>

      {resource.rationale && (
        <p className="mt-2 text-xs leading-relaxed text-text-dim">{resource.rationale}</p>
      )}

      {(resource.jurisdiction || resource.geographicScope) && (
        <div className="mt-2 rounded-lg border border-amber-400/20 bg-amber-400/10 px-2 py-1.5 text-[11px] leading-relaxed text-amber-100">
          <span className="font-medium">Scope:</span> {resource.jurisdiction || formatResourceLabel(resource.geographicScope)}
        </div>
      )}

      {refs.length > 0 && (
        <div className="mt-2 text-[11px] text-text-dim">
          <span className="text-text">Relevant refs:</span> {refs.join(', ')}
        </div>
      )}

      {resource.warning && (
        <div className="mt-2 flex items-start gap-1.5 rounded-lg border border-amber-400/20 bg-amber-400/10 px-2 py-1.5 text-[11px] text-amber-100">
          <AlertTriangle size={12} className="mt-0.5 shrink-0" />
          <span>{resource.warning}</span>
        </div>
      )}

      {caveats.length > 0 && (
        <div className="mt-2 space-y-1 border-l border-cyan-400/35 pl-2 text-[11px] leading-relaxed text-text-dim">
          {caveats.map((caveat) => (
            <div key={caveat.label}>
              <span className="font-medium text-text">{caveat.label}:</span> {caveat.value}
            </div>
          ))}
        </div>
      )}

      <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
        {resource.url && (
          <a
            href={resource.url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-accent hover:underline"
          >
            <Globe2 size={12} />
            Open online <ExternalLink size={10} />
          </a>
        )}
        {resource.localFileName && (
          <span className="inline-flex items-center gap-1 text-text-dim">
            <HardDrive size={12} />
            {resource.localFileName}
          </span>
        )}
      </div>
    </div>
  );
}

function SourceContextPanel({ context }: { context: NodeDetail['sourceGroundedContext'] }) {
  if (!context) {
    return (
      <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
        No source-grounded context packet is available for this node.
      </div>
    );
  }

  const summary = context.coverageSummary;
  const topPaths = context.graphPaths.slice(0, 8);
  const topResources = context.resources.slice(0, 6);
  const topSelectors = context.evidenceSelectors.slice(0, 8);

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-2">
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Source-backed</div>
          <div className="mt-1 text-lg font-semibold text-emerald-100">{summary.sourceBackedPathCount}</div>
        </div>
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Pending</div>
          <div className="mt-1 text-lg font-semibold text-amber-100">{summary.proposalOnlyPathCount}</div>
        </div>
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Resources</div>
          <div className="mt-1 text-lg font-semibold text-cyan-100">{summary.resourceCount}</div>
        </div>
      </div>

      <div className="rounded-md border border-sky-400/20 bg-sky-400/10 px-3 py-2 text-xs leading-relaxed text-sky-100">
        Read-only context packet. Pending overlay paths are visible for review but are not active graph admissions.
      </div>

      <div className="space-y-2">
        <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
          <Route size={12} />
          Context Paths
        </div>
        {topPaths.length === 0 ? (
          <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
            No context paths were selected.
          </div>
        ) : topPaths.map((path) => (
          <div key={path.edgeId} className="kg-card rounded-xl border-l-2 border-cyan-400/45 p-3">
            <div className="flex min-w-0 items-center gap-1 text-sm">
              <span className="truncate" title={path.fromLabel}>{path.fromLabel}</span>
              <ArrowRight size={12} className="shrink-0 text-text-dim" />
              <span className="shrink-0 font-medium">{path.predicate}</span>
              <ArrowRight size={12} className="shrink-0 text-text-dim" />
              <span className="truncate" title={path.toLabel}>{path.toLabel}</span>
            </div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              <ResourceBadge tone={path.classification === 'source_backed' ? 'good' : path.pendingOnly ? 'warn' : 'neutral'}>
                {formatResourceLabel(path.classification)}
              </ResourceBadge>
              {path.confidence !== undefined && <ResourceBadge>{formatPercent(path.confidence)}</ResourceBadge>}
              {path.sourceFamilyIds?.length ? <ResourceBadge tone="good">{`Source families ${path.sourceFamilyIds.length}`}</ResourceBadge> : null}
              {path.resourceLinkIds?.length ? <ResourceBadge tone="good">{`Resource links ${path.resourceLinkIds.length}`}</ResourceBadge> : null}
            </div>
            {path.rationale && <p className="mt-2 text-xs leading-relaxed text-text-dim">{path.rationale}</p>}
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
          <BookOpen size={12} />
          Context Resources
        </div>
        {topResources.length === 0 ? (
          <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
            No learner-visible resources are linked to this context packet.
          </div>
        ) : topResources.map((resource) => (
          <div key={`${resource.linkId}-${resource.resourceId}`} className="kg-card rounded-xl p-3">
            <div className="text-sm font-semibold text-text">{resource.title}</div>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {resource.resourceType && <ResourceBadge>{formatResourceLabel(resource.resourceType)}</ResourceBadge>}
              {resource.sourceAuthority && (
                <ResourceBadge tone={resource.sourceAuthority === 'general_web' ? 'warn' : 'good'}>
                  {formatResourceLabel(resource.sourceAuthority)}
                </ResourceBadge>
              )}
              {resource.reviewStatus && <ResourceBadge tone={resource.reviewStatus === 'accepted' || resource.reviewStatus === 'human_reviewed' ? 'good' : 'warn'}>{formatResourceLabel(resource.reviewStatus)}</ResourceBadge>}
            </div>
          </div>
        ))}
      </div>

      {topSelectors.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
            <FileText size={12} />
            Evidence Selectors
          </div>
          <div className="kg-card rounded-xl p-3 text-xs text-text-dim">
            {topSelectors.map((selector) => (
              <div key={`${selector.linkId}-${selector.kind}-${selector.ref}`} className="flex items-center justify-between gap-2 py-1">
                <span className="truncate">{selector.resourceId}</span>
                <span className="shrink-0 text-text">{formatResourceLabel(selector.kind)} {selector.ref}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function SourceGapWorkqueuePanel({ preview }: { preview: NodeDetail['sourceGapWorkqueue'] }) {
  if (!preview || !preview.available) {
    return (
      <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
        No source-gap workqueue artifact is available for this node.
      </div>
    );
  }

  const items = preview.items.slice(0, 6);
  const proposalById = new Map(preview.proposals.map((proposal) => [proposal.proposalId, proposal]));

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
          <AlertTriangle size={12} />
          Source Gap Workqueue
        </div>
        <ResourceBadge tone="warn">{`${preview.counts.filteredWorkqueueItems} Gaps`}</ResourceBadge>
      </div>

      <div className="grid grid-cols-3 gap-2">
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Returned</div>
          <div className="mt-1 text-lg font-semibold text-amber-100">{preview.counts.returnedWorkqueueItems}</div>
        </div>
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Proposals</div>
          <div className="mt-1 text-lg font-semibold text-cyan-100">{preview.counts.returnedSourceLinkProposals}</div>
        </div>
        <div className="kg-card rounded-xl p-3">
          <div className="text-[10px] uppercase tracking-wider text-text-dim">Run</div>
          <div className="mt-1 truncate text-xs font-semibold text-text" title={preview.runId || ''}>{preview.runId || 'latest'}</div>
        </div>
      </div>

      <div className="rounded-md border border-amber-400/25 bg-amber-400/10 px-3 py-2 text-xs leading-relaxed text-amber-100">
        Review-only source-link suggestions. These rows do not admit graph edges, do not create Resource Layer links, and do not write to Neo4j or Postgres.
      </div>

      {items.length === 0 ? (
        <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
          No source gaps in the current workqueue touch this node.
        </div>
      ) : items.map((item) => {
        const title = item.itemType === 'relationship_source_gap'
          ? `${item.fromLabel || item.fromId} ${item.predicate || ''} ${item.toLabel || item.toId}`.trim()
          : item.nodeLabel || item.nodeId || item.workqueueId;
        const proposals = item.proposalIds
          .map((id) => proposalById.get(id))
          .filter((proposal): proposal is NonNullable<typeof proposal> => Boolean(proposal));
        return (
          <div key={item.workqueueId} className="kg-card rounded-xl border-l-2 border-amber-300/50 p-3">
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0">
                <div className="truncate text-sm font-semibold text-text" title={title}>{title}</div>
                <div className="mt-1 flex flex-wrap gap-1.5">
                  <ResourceBadge tone={item.itemType === 'relationship_source_gap' ? 'warn' : 'neutral'}>
                    {formatResourceLabel(item.itemType)}
                  </ResourceBadge>
                  <ResourceBadge>{formatResourceLabel(item.sourceBackingStatus)}</ResourceBadge>
                  {item.priorityRank > 0 && <ResourceBadge>{`Rank ${item.priorityRank}`}</ResourceBadge>}
                  {Number.isFinite(item.priorityScore) && <ResourceBadge>{`Score ${item.priorityScore.toFixed(1)}`}</ResourceBadge>}
                </div>
              </div>
              <CopyValueButton value={item.edgeKey || item.nodeId || item.workqueueId} label="Copy source gap key" />
            </div>

            {item.suggestedResources.length > 0 && (
              <div className="mt-3 space-y-2">
                {item.suggestedResources.slice(0, 3).map((resource) => (
                  <div key={`${item.workqueueId}-${resource.resourceId}`} className="rounded-md border border-border/60 bg-bg/40 px-2.5 py-2">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <div className="truncate text-xs font-medium text-text" title={resource.title}>{resource.title}</div>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {resource.resourceType && <ResourceBadge>{formatResourceLabel(resource.resourceType)}</ResourceBadge>}
                          {resource.sourceAuthority && <ResourceBadge tone={resource.sourceAuthority === 'government' || resource.sourceAuthority === 'professional_body' ? 'good' : 'neutral'}>{formatResourceLabel(resource.sourceAuthority)}</ResourceBadge>}
                          {resource.accessType && <ResourceBadge tone={resource.accessType === 'paywalled' || resource.accessType === 'restricted' ? 'warn' : 'neutral'}>{formatResourceLabel(resource.accessType)}</ResourceBadge>}
                        </div>
                      </div>
                      <span className="shrink-0 text-[10px] text-text-dim">{resource.score.toFixed(3)}</span>
                    </div>
                    {resource.matchedTerms.length > 0 && (
                      <div className="mt-1 text-[11px] text-text-dim">
                        Matched: {resource.matchedTerms.slice(0, 6).join(', ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {proposals.length > 0 && (
              <div className="mt-3 space-y-2">
                <div className="text-[10px] uppercase tracking-wider text-text-dim">Source-link proposals</div>
                {proposals.slice(0, 3).map((proposal) => (
                  <div key={proposal.proposalId} className="rounded-md border border-border/60 bg-bg/40 px-2.5 py-2">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <div className="truncate text-xs font-medium text-text" title={proposal.title}>{proposal.title}</div>
                        <div className="mt-1 flex flex-wrap gap-1">
                          <ResourceBadge>{formatResourceLabel(proposal.reviewStatus)}</ResourceBadge>
                          <ResourceBadge>{formatResourceLabel(proposal.suggestedRelationship)}</ResourceBadge>
                          <ResourceBadge>{proposal.targetType === 'relationship' ? 'Relationship Target' : 'Node Target'}</ResourceBadge>
                        </div>
                      </div>
                      <span className="shrink-0 text-[10px] text-text-dim">{proposal.score.toFixed(3)}</span>
                    </div>
                    <div className="mt-2 grid grid-cols-1 gap-1 text-[11px] text-text-dim">
                      <div>Proposal: <span className="text-text">{proposal.proposalId}</span></div>
                      <div>Resource: <span className="text-text">{proposal.resourceId}</span></div>
                      {proposal.nodeId && <div>Node: <span className="text-text">{proposal.nodeId}</span></div>}
                      {proposal.edgeKey && <div>Edge: <span className="text-text">{proposal.edgeKey}</span></div>}
                      {(proposal.fromId || proposal.predicate || proposal.toId) && (
                        <div>
                          Target: <span className="text-text">{[proposal.fromId, proposal.predicate, proposal.toId].filter(Boolean).join(' - ')}</span>
                        </div>
                      )}
                      {proposal.matchedTerms.length > 0 && (
                        <div>Matched: <span className="text-text">{proposal.matchedTerms.slice(0, 8).join(', ')}</span></div>
                      )}
                      <div className="text-text-dim">{proposal.rationale}</div>
                    </div>
                  </div>
                ))}
                <div className="rounded-md border border-amber-400/25 bg-amber-400/10 px-2.5 py-2 text-[11px] leading-relaxed text-amber-100">
                  Pending-only detail: inspect before steward action; this panel does not create source links or mutate graph/database state.
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function NodeInspector({ detail }: { detail: NodeDetail }) {
  const { node, taxonomyPath, incoming, outgoing, evidence } = detail;
  const resources = detail.resources ?? [];
  const sourceGroundedContext = detail.sourceGroundedContext;
  const sourceGapWorkqueue = detail.sourceGapWorkqueue;
  const learnerVisibleResources = resources.filter(
    (resource) => resource.reviewStatus === 'accepted' || resource.reviewStatus === 'human_reviewed',
  );
  const [activeTab, setActiveTab] = useState<InspectorTab>('overview');
  const setSelectedNode = useSceneStore((s) => s.setSelectedNode);
  const openBottom = useSceneStore((s) => s.openBottom);
  const pinnedNodeIds = useSceneStore((s) => s.pinnedNodeIds);
  const togglePinnedNode = useSceneStore((s) => s.togglePinnedNode);
  const requestFocusSubgraph = useSceneStore((s) => s.requestFocusSubgraph);
  const requestFocusNode = useSceneStore((s) => s.requestFocusNode);
  const requestShowAll = useSceneStore((s) => s.requestShowAll);
  const hiddenNodeIds = useSceneStore((s) => s.hiddenNodeIds);
  const visibleNodeTypes = useSceneStore((s) => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore((s) => s.visibleEdgeTypes);
  const setVisibleNodeTypes = useSceneStore((s) => s.setVisibleNodeTypes);
  const setVisibleEdgeTypes = useSceneStore((s) => s.setVisibleEdgeTypes);
  const pathSourceId = useSceneStore((s) => s.pathSourceId);
  const pathTargetId = useSceneStore((s) => s.pathTargetId);
  const highlightedPath = useSceneStore((s) => s.highlightedPath);
  const setPathSource = useSceneStore((s) => s.setPathSource);
  const setPathTarget = useSceneStore((s) => s.setPathTarget);
  const clearPath = useSceneStore((s) => s.clearPath);
  const requestChildOrbit = useSceneStore((s) => s.requestChildOrbit);
  const [childOrbitStrength, setChildOrbitStrength] = useState(0);

  const displayLabel = getDisplayLabel(node);
  const relationshipCount = incoming.length + outgoing.length;
  const sourceCount = evidence.length + learnerVisibleResources.length;
  const contextPathCount = sourceGroundedContext?.coverageSummary.graphPathCount ?? 0;
  const sourceGapCount = sourceGapWorkqueue?.counts.filteredWorkqueueItems ?? 0;
  const childRelationCount = outgoing.filter((relation) => relation.relType === 'HAS_CHILD').length;
  const confidenceLabel = node.confidence !== undefined ? `${(node.confidence * 100).toFixed(0)}% confidence` : null;
  const pinned = pinnedNodeIds.includes(node.id);
  const isolated = hiddenNodeIds.length > 0;
  const resourcesEligible = RESOURCE_ELIGIBLE_NODE_TYPES.has(String(node.type || node.kind || '').toLowerCase());

  function getRelationshipHiddenReasons(relation: RelationDetail) {
    const reasons: string[] = [];
    if (!visibleEdgeTypes.has(relation.relType)) reasons.push(`edge type ${relation.relType}`);
    if (!visibleNodeTypes.has(relation.other.type)) reasons.push(`node type ${relation.other.type}`);
    if (hiddenNodeIds.includes(node.id) || hiddenNodeIds.includes(relation.other.id)) reasons.push('isolation');
    return reasons;
  }

  const allRelationships = [...incoming, ...outgoing];
  const hiddenRelationshipCount = allRelationships.filter((relation) => getRelationshipHiddenReasons(relation).length > 0).length;
  const semanticRelationshipCount = allRelationships.filter((relation) => relation.isSemanticEdge || relation.category === 'semantic').length;
  const hierarchyRelationshipCount = allRelationships.filter((relation) => relation.isHierarchyEdge || relation.category === 'hierarchy').length;

  function revealRelationshipFilters(relations: RelationDetail[]) {
    const nextEdgeTypes = new Set(visibleEdgeTypes);
    const nextNodeTypes = new Set(visibleNodeTypes);
    relations.forEach((relation) => {
      nextEdgeTypes.add(relation.relType);
      if (relation.other.type) nextNodeTypes.add(relation.other.type);
    });
    if (node.type) nextNodeTypes.add(node.type);
    setVisibleEdgeTypes(nextEdgeTypes);
    setVisibleNodeTypes(nextNodeTypes);
  }

  function revealAllDirectRelationships() {
    revealRelationshipFilters(allRelationships);
    requestShowAll();
    requestFocusNode(node.id);
  }

  function selectRelatedNode(relation: RelationDetail) {
    revealRelationshipFilters([relation]);
    requestShowAll();
    setSelectedNode(relation.other.id);
    requestFocusNode(relation.other.id);
  }

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

      <div className="grid grid-cols-5 border-b border-border bg-bg/20">
        {([
          ['overview', 'Overview', undefined],
          ['relationships', 'Relationships', relationshipCount],
          ['sources', 'Sources', sourceCount],
          ['context', 'Context', contextPathCount + sourceGapCount],
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
            {sourceGapCount > 0 && (
              <button
                type="button"
                className="kg-card w-full rounded-xl border-l-2 border-amber-300/60 p-3 text-left transition-colors hover:bg-panel-hover"
                onClick={() => setActiveTab('context')}
                aria-label="Review source gaps in context"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="text-xs uppercase tracking-wider text-amber-100">Source gaps awaiting review</div>
                    <div className="mt-1 text-sm text-text">
                      {sourceGapCount} pending source-link suggestion{sourceGapCount === 1 ? '' : 's'} touch this node.
                    </div>
                    <div className="mt-1 text-xs leading-relaxed text-text-dim">
                      Review-only: opens Context without creating Resource links or mutating graph/database state.
                    </div>
                  </div>
                  <ArrowRight size={14} className="mt-1 shrink-0 text-amber-100" />
                </div>
              </button>
            )}
            {detail.canonical && (
              <div className="rounded-md border border-amber-400/30 bg-amber-400/10 px-3 py-2 text-xs text-amber-100">
                <div className="font-semibold">Canonical stewardship</div>
                <div>Status: {String(detail.canonical.status || 'canonical')}</div>
                {detail.canonical.canonicalNodeId && detail.canonical.canonicalNodeId !== node.id && (
                  <div>Canonical target: {detail.canonical.canonicalNodeId}</div>
                )}
                {Array.isArray(detail.canonical.duplicateGroupIds) && detail.canonical.duplicateGroupIds.length > 0 && (
                  <div>Duplicate group(s): {detail.canonical.duplicateGroupIds.join(', ')}</div>
                )}
              </div>
            )}
            {node.summary && <MetadataRow label="Summary" value={node.summary} />}
            {taxonomyPath.length > 0 && (
              <>
                <Breadcrumbs nodes={taxonomyPath} onSelectNode={setSelectedNode} />
                <MetadataRow label="Taxonomy Path" value={taxonomyPath.map((taxonomyNode) => getDisplayLabel(taxonomyNode)).join(' > ')} />
              </>
            )}

            <div className="kg-card rounded-xl p-3">
              <div className="mb-2 flex items-center justify-between gap-2">
                <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
                  <Circle size={12} />
                  Child Council
                </div>
                <span className="text-[10px] text-text-dim">{Math.round(childOrbitStrength * 100)}%</span>
              </div>
              <p className="mb-3 text-xs leading-relaxed text-text-dim">
                Pull this node&apos;s child tree into evenly spaced circular rings around the selected node.
                {childRelationCount > 0 ? ` Direct children: ${childRelationCount}.` : ' No direct HAS_CHILD links are reported in the inspector, but descendants in the loaded graph are still checked.'}
              </p>
              <label className="flex items-center gap-2 text-[10px] uppercase tracking-[0.18em] text-text-dim">
                <span>Loose</span>
                <input
                  aria-label="Child council orbit strength"
                  className="min-w-0 flex-1 accent-cyan-300"
                  type="range"
                  min={0}
                  max={1}
                  step={0.05}
                  value={childOrbitStrength}
                  onInput={(event) => {
                    const nextStrength = Number(event.currentTarget.value);
                    setChildOrbitStrength(nextStrength);
                    requestChildOrbit(node.id, nextStrength);
                  }}
                />
                <span>Tight</span>
              </label>
            </div>

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
            {relationshipCount > 0 && (
              <div className="rounded-xl border border-border/70 bg-bg/40 p-3 text-xs text-text-dim">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <span className="font-semibold text-text">{relationshipCount}</span> direct relationships ·{' '}
                    <span className="font-semibold text-text">{semanticRelationshipCount}</span> semantic ·{' '}
                    <span className="font-semibold text-text">{hierarchyRelationshipCount}</span> hierarchy
                    {hiddenRelationshipCount > 0 && (
                      <span className="ml-1 text-amber-100">
                        · {hiddenRelationshipCount} hidden by current filters/isolation
                      </span>
                    )}
                  </div>
                  <button
                    type="button"
                    className="rounded-lg border border-cyan-300/30 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-cyan-100 transition hover:bg-cyan-300/10"
                    onClick={revealAllDirectRelationships}
                  >
                    Show all direct relationships
                  </button>
                </div>
              </div>
            )}
            {relationshipCount === 0 && (
              <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
                No relationships are available for this node.
              </div>
            )}
            <RelationList title="Incoming" relations={incoming} onSelectRelation={selectRelatedNode} getHiddenReasons={getRelationshipHiddenReasons} />
            <RelationList title="Outgoing" relations={outgoing} onSelectRelation={selectRelatedNode} getHiddenReasons={getRelationshipHiddenReasons} />
          </div>
        )}

        {activeTab === 'sources' && (
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
                  <BookOpen size={12} />
                  Resources / References
                </div>
                {learnerVisibleResources.length > 0 && (
                  <span className="text-[10px] text-text-dim">Top {learnerVisibleResources.length}</span>
                )}
              </div>
              <div className="rounded-md border border-sky-400/20 bg-sky-400/10 px-3 py-2 text-xs leading-relaxed text-sky-100">
                Learner mode shows accepted or human-reviewed links only. Reviewer-only candidates, unverified records, and incomplete standards context remain hidden here.
              </div>
              {resourcesEligible && learnerVisibleResources.length === 0 && (
                <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
                  No learner-visible resources linked yet.
                </div>
              )}
              {!resourcesEligible && learnerVisibleResources.length === 0 && (
                <div className="rounded-md border border-border/70 bg-bg/40 px-3 py-2 text-sm text-text-dim italic">
                  Resource references are shown for concept, rule, definition, procedure, exception, evidence, and document nodes.
                </div>
              )}
              {learnerVisibleResources.map((resource) => (
                <ResourceCard key={resource.linkId} resource={resource} />
              ))}
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-1 text-xs uppercase tracking-wider text-text-dim">
                <FileText size={12} />
                Evidence Spans
              </div>
            {evidence.length === 0 && learnerVisibleResources.length === 0 && (
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
            </div>
          </div>
        )}

        {activeTab === 'context' && (
          <div className="space-y-4">
            <SourceContextPanel context={sourceGroundedContext} />
            <SourceGapWorkqueuePanel preview={sourceGapWorkqueue} />
          </div>
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
