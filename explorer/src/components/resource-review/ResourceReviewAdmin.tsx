import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  getResourceReviewQueue,
  previewStandardsContextDecision,
  submitCandidateReviewDecision,
  submitLinkReviewDecision,
  submitLocalFileReviewDecision,
  submitStandardsContextDecision,
} from '../../api/graphApi';
import type {
  ResourceReviewCandidateItem,
  ResourceReviewLinkItem,
  ResourceReviewLocalFileItem,
  ResourceReviewMetrics,
  ResourceReviewQueue,
  StandardsContextPreviewResponse,
} from '../../types';

type ReviewTab = 'needs_review' | 'candidates' | 'local_files' | 'rejected' | 'standards' | 'accepted';

const tabs: { id: ReviewTab; label: string }[] = [
  { id: 'needs_review', label: 'Needs Review' },
  { id: 'candidates', label: 'Candidates' },
  { id: 'local_files', label: 'Local Files' },
  { id: 'rejected', label: 'Rejected' },
  { id: 'standards', label: 'Standards Missing Context' },
  { id: 'accepted', label: 'Accepted' },
];

const defaultMetrics: ResourceReviewMetrics = {
  acceptedResources: 0,
  acceptedLinks: 0,
  needsReviewLinks: 0,
  rejectedLinks: 0,
  candidateLinks: 0,
  candidates: 0,
  localFilesIndexed: 0,
  localFilesAdmitted: 0,
  standardsMissingContext: 0,
  standardsMissingEdition: 0,
  standardsMissingJurisdiction: 0,
  standardsMissingScope: 0,
  standardsContextNeedsReview: 0,
  standardsPromotionBlocked: 0,
  duplicateWarnings: 0,
  brokenLinkWarnings: 0,
};

function statusClass(status: string) {
  if (status === 'accepted' || status === 'human_reviewed') return 'border-emerald-400/30 bg-emerald-400/10 text-emerald-100';
  if (status === 'rejected') return 'border-rose-400/30 bg-rose-400/10 text-rose-100';
  if (status === 'needs_review') return 'border-amber-400/30 bg-amber-400/10 text-amber-100';
  return 'border-sky-400/30 bg-sky-400/10 text-sky-100';
}

function Badge({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'neutral' | 'warning' | 'danger' }) {
  const toneClass = tone === 'danger'
    ? 'border-rose-400/30 bg-rose-400/10 text-rose-100'
    : tone === 'warning'
      ? 'border-amber-400/30 bg-amber-400/10 text-amber-100'
      : 'border-white/10 bg-white/5 text-text-dim';
  return <span className={`rounded-full border px-2 py-0.5 text-[11px] ${toneClass}`}>{children}</span>;
}

function MetricCard({ label, value, danger }: { label: string; value: number | undefined; danger?: boolean }) {
  return (
    <div className={`rounded-xl border p-3 ${danger ? 'border-amber-400/30 bg-amber-400/10' : 'border-white/10 bg-white/5'}`}>
      <div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-text">{value ?? 0}</div>
    </div>
  );
}

function Warnings({ warnings }: { warnings?: string[] }) {
  if (!warnings?.length) return null;
  return (
    <div className="space-y-1">
      {warnings.map((warning) => (
        <div key={warning} className="rounded-lg border border-amber-400/30 bg-amber-400/10 px-2 py-1 text-xs text-amber-100">
          {warning}
        </div>
      ))}
    </div>
  );
}

function isLocalDevAdminGateOpen() {
  if (typeof window === 'undefined') return true;
  const host = window.location.hostname;
  return import.meta.env.DEV
    || import.meta.env.VITE_ENABLE_DEV_ADMIN === 'true'
    || host === 'localhost'
    || host === '127.0.0.1'
    || host === '::1';
}

type PendingResourceDecision = {
  targetType: 'link' | 'candidate' | 'local_file';
  id: string;
  decision: string;
  fallbackRationale: string;
};

function DecisionForm({
  pending,
  onCancel,
  onSubmit,
}: {
  pending: PendingResourceDecision;
  onCancel: () => void;
  onSubmit: (body: Record<string, unknown>) => Promise<unknown>;
}) {
  const [reviewer, setReviewer] = useState('local-dev-reviewer');
  const [rationale, setRationale] = useState(pending.fallbackRationale);
  const [notes, setNotes] = useState('');
  const [dryRun, setDryRun] = useState(true);
  const [preview, setPreview] = useState<unknown>(null);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  async function submitDecision(nextDryRun: boolean) {
    if (!reviewer.trim()) {
      setFormError('Reviewer is required.');
      return;
    }
    if (!rationale.trim()) {
      setFormError('Rationale is required.');
      return;
    }
    setSubmitting(true);
    setFormError(null);
    try {
      const result = await onSubmit({
        decision: pending.decision,
        reviewer: reviewer.trim(),
        rationale: rationale.trim(),
        notes: notes.trim() || undefined,
        dryRun: nextDryRun,
      });
      setPreview(result);
      if (!nextDryRun) onCancel();
    } catch (error) {
      setFormError(error instanceof Error ? error.message : 'Failed to submit resource review decision');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="rounded-2xl border border-accent/40 bg-accent/10 p-4" aria-label="Structured resource review decision form">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-text">Structured review decision</div>
          <div className="mt-1 text-xs text-text-dim">
            {pending.decision} {pending.targetType} {pending.id}. Preview is a dry run; Submit mutates the local file-backed registry through the dev/admin-gated API.
          </div>
        </div>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={onCancel}>Cancel</button>
      </div>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <label className="space-y-1 text-xs text-text-dim">
          Reviewer
          <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
        </label>
        <label className="flex items-end gap-2 text-xs text-text-dim">
          <input type="checkbox" checked={dryRun} onChange={(event) => setDryRun(event.target.checked)} />
          Submit as dry-run preview
        </label>
      </div>
      <label className="mt-3 block space-y-1 text-xs text-text-dim">
        Required rationale
        <textarea className="kg-input min-h-20 w-full rounded-lg px-3 py-2 text-sm text-text" value={rationale} onChange={(event) => setRationale(event.target.value)} />
      </label>
      <label className="mt-3 block space-y-1 text-xs text-text-dim">
        Notes
        <textarea className="kg-input min-h-16 w-full rounded-lg px-3 py-2 text-sm text-text" value={notes} onChange={(event) => setNotes(event.target.value)} />
      </label>
      {formError && <div className="mt-3 rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">{formError}</div>}
      {preview !== null && (
        <pre className="mt-3 max-h-64 overflow-auto rounded-lg bg-black/30 p-3 text-xs text-text-dim">
          {JSON.stringify(preview, null, 2)}
        </pre>
      )}
      <div className="mt-3 flex flex-wrap gap-2">
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={submitting} onClick={() => void submitDecision(true)}>Preview diff</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={submitting} onClick={() => void submitDecision(dryRun)}>Submit {dryRun ? 'dry-run' : 'decision'}</button>
      </div>
    </section>
  );
}

function LinkCard({ item, onDecision }: { item: ResourceReviewLinkItem; onDecision: (id: string, decision: string, fallback: string) => void }) {
  return (
    <article className="kg-card rounded-2xl p-4 space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-text">{item.title}</div>
          <div className="mt-1 text-xs text-text-dim">
            Node {item.nodeId} · Resource {item.resourceId}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className={`rounded-full border px-2 py-0.5 text-[11px] ${statusClass(item.reviewStatus)}`}>{item.reviewStatus}</span>
          <Badge>{item.relationship}</Badge>
          <Badge>{item.verificationStatus}</Badge>
          {item.missingStandardContext && <Badge tone="warning">missing edition/section</Badge>}
        </div>
      </div>
      <p className="text-sm leading-6 text-text-dim">{item.rationale || 'No rationale supplied.'}</p>
      {item.reviewNotes && <p className="text-xs leading-5 text-text-dim">Review notes: {item.reviewNotes}</p>}
      <Warnings warnings={item.warnings} />
      <div className="flex flex-wrap gap-2">
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'accept', 'Accepted after reviewer confirmed edition/scope/provenance context.')}>Accept</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'reject', 'Rejected after reviewer found the linkage too broad or unsupported.')}>Reject</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'needs_review', 'Hold for more source, section, jurisdiction, or rights context.')}>Hold / Needs More Context</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'reopen', 'Reopened for reviewer follow-up.')}>Reopen</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'downgrade', 'Downgraded pending narrower context.')}>Downgrade</button>
        {item.resource?.url && (
          <a className="kg-control rounded-lg px-3 py-1.5 text-xs" href={String(item.resource.url)} target="_blank" rel="noreferrer">View resource</a>
        )}
        <Link className="kg-control rounded-lg px-3 py-1.5 text-xs" to={`/explore?node=${encodeURIComponent(item.nodeId)}`}>View node</Link>
      </div>
    </article>
  );
}

function StandardsContextCard({
  item,
  adminGateOpen,
  onChanged,
}: {
  item: ResourceReviewLinkItem;
  adminGateOpen: boolean;
  onChanged: () => Promise<void>;
}) {
  const [decision, setDecision] = useState('keep_needs_review');
  const [reviewer, setReviewer] = useState('local-dev-reviewer');
  const [rationale, setRationale] = useState('Keep missing standards context visible; do not infer edition/version without source-backed review.');
  const [edition, setEdition] = useState('');
  const [version, setVersion] = useState('');
  const [publicationYear, setPublicationYear] = useState('');
  const [jurisdiction, setJurisdiction] = useState('');
  const [geographicScope, setGeographicScope] = useState('');
  const [applicabilityNote, setApplicabilityNote] = useState('');
  const [sourceOfContext, setSourceOfContext] = useState('');
  const [confidence, setConfidence] = useState<'low' | 'medium' | 'high'>('low');
  const [preview, setPreview] = useState<StandardsContextPreviewResponse | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const targetId = item.id || item.resourceId;
  const requiresSource = ['update_context_complete', 'mark_context_not_required', 'promote_if_context_complete'].includes(decision);
  const applyDisabled = !adminGateOpen
    || !reviewer.trim()
    || !rationale.trim()
    || (requiresSource && !sourceOfContext.trim())
    || submitting;

  function body() {
    return {
      decision,
      reviewer: reviewer.trim(),
      rationale: rationale.trim(),
      edition: edition.trim() || undefined,
      version: version.trim() || undefined,
      publicationYear: publicationYear.trim() ? Number(publicationYear.trim()) : undefined,
      jurisdiction: jurisdiction.trim() || undefined,
      geographicScope: geographicScope.trim() || undefined,
      applicabilityNote: applicabilityNote.trim() || undefined,
      sourceOfContext: sourceOfContext.trim() || undefined,
      confidence,
    };
  }

  async function previewDecision() {
    setSubmitting(true);
    setFormError(null);
    try {
      setPreview(await previewStandardsContextDecision(targetId, body()));
    } catch (error) {
      setFormError(error instanceof Error ? error.message : 'Failed to preview standards context update');
    } finally {
      setSubmitting(false);
    }
  }

  async function applyDecision() {
    if (applyDisabled) return;
    setSubmitting(true);
    setFormError(null);
    try {
      setPreview(await submitStandardsContextDecision(targetId, { ...body(), dryRun: false }));
      await onChanged();
    } catch (error) {
      setFormError(error instanceof Error ? error.message : 'Failed to apply standards context update');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <article className="kg-card rounded-2xl p-4 space-y-4" aria-label="Standards context review card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-text">{item.title}</div>
          <div className="mt-1 text-xs text-text-dim">
            {item.organization || 'Unknown organization'} · {item.resourceType || 'standard'} · Node {item.nodeId} · Resource {item.resourceId}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className={`rounded-full border px-2 py-0.5 text-[11px] ${statusClass(item.reviewStatus)}`}>{item.reviewStatus}</span>
          <Badge tone="warning">{item.standardContextStatus || 'needs_human_review'}</Badge>
          {item.promotionBlocked && <Badge tone="danger">promotion blocked</Badge>}
          {item.missingStandardContextFields?.map((field) => <Badge key={field} tone="warning">missing {field}</Badge>)}
        </div>
      </div>
      <div className="rounded-xl border border-amber-400/30 bg-amber-400/10 p-3 text-xs leading-5 text-amber-100">
        Missing context is honest while the item remains needs_review. Do not guess edition/version, “latest,” or jurisdiction/adoption. Promotion requires complete source-backed or reviewer-supported standards context.
      </div>
      <div className="grid gap-3 text-xs md:grid-cols-2">
        <div className="rounded-xl border border-white/10 bg-white/5 p-3">
          <div className="font-semibold text-text">Current context</div>
          <div className="mt-2 space-y-1 text-text-dim">
            <div>Edition: {item.currentEdition || 'not supplied'}</div>
            <div>Version: {item.currentVersion || 'not supplied'}</div>
            <div>Publication year: {item.currentPublicationYear || 'not supplied'}</div>
            <div>Jurisdiction: {item.currentJurisdiction || 'not supplied'}</div>
            <div>Geographic scope: {item.currentGeographicScope || 'not supplied'}</div>
            <div>Source of context: {item.sourceOfContext || 'not supplied'}</div>
          </div>
        </div>
        <div className="rounded-xl border border-white/10 bg-white/5 p-3">
          <div className="font-semibold text-text">Promotion blockers</div>
          <ul className="mt-2 list-disc space-y-1 pl-4 text-text-dim">
            {(item.promotionBlockerReasons?.length ? item.promotionBlockerReasons : ['No promotion blocker reported for current review status.']).map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      </div>
      <Warnings warnings={item.warnings} />
      <section className="rounded-xl border border-accent/30 bg-accent/10 p-3" aria-label="Structured standards context form">
        <div className="text-sm font-semibold text-text">Structured standards context form</div>
        <div className="mt-1 text-xs text-text-dim">
          Preview is non-mutating. Apply writes a review decision and Resource Layer transaction manifest through the dev/admin gate.
        </div>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          <label className="space-y-1 text-xs text-text-dim">
            Status decision
            <select className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={decision} onChange={(event) => setDecision(event.target.value)}>
              <option value="keep_needs_review">keep_needs_review</option>
              <option value="update_context_partial">update_context_partial</option>
              <option value="update_context_complete">update_context_complete</option>
              <option value="mark_context_not_required">mark_context_not_required</option>
              <option value="reject_context_update">reject_context_update</option>
              <option value="defer_context_review">defer_context_review</option>
              <option value="promote_if_context_complete">promote_if_context_complete</option>
              <option value="demote_to_needs_review">demote_to_needs_review</option>
            </select>
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Reviewer
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Confidence
            <select className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={confidence} onChange={(event) => setConfidence(event.target.value as 'low' | 'medium' | 'high')}>
              <option value="low">low</option>
              <option value="medium">medium</option>
              <option value="high">high</option>
            </select>
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Edition
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={edition} onChange={(event) => setEdition(event.target.value)} placeholder="Do not guess" />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Version
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={version} onChange={(event) => setVersion(event.target.value)} />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Publication year
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={publicationYear} onChange={(event) => setPublicationYear(event.target.value)} />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Jurisdiction
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={jurisdiction} onChange={(event) => setJurisdiction(event.target.value)} />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Geographic scope
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={geographicScope} onChange={(event) => setGeographicScope(event.target.value)} />
          </label>
          <label className="space-y-1 text-xs text-text-dim">
            Source of context
            <input className="kg-input w-full rounded-lg px-3 py-2 text-sm text-text" value={sourceOfContext} onChange={(event) => setSourceOfContext(event.target.value)} placeholder={requiresSource ? 'Required for this decision' : 'Optional'} />
          </label>
        </div>
        <label className="mt-3 block space-y-1 text-xs text-text-dim">
          Applicability / scope note
          <textarea className="kg-input min-h-16 w-full rounded-lg px-3 py-2 text-sm text-text" value={applicabilityNote} onChange={(event) => setApplicabilityNote(event.target.value)} />
        </label>
        <label className="mt-3 block space-y-1 text-xs text-text-dim">
          Required rationale
          <textarea className="kg-input min-h-16 w-full rounded-lg px-3 py-2 text-sm text-text" value={rationale} onChange={(event) => setRationale(event.target.value)} />
        </label>
        {formError && <div className="mt-3 rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">{formError}</div>}
        {preview && (
          <pre className="mt-3 max-h-72 overflow-auto rounded-lg bg-black/30 p-3 text-xs text-text-dim" aria-label="Standards context diff preview">
            {JSON.stringify(preview, null, 2)}
          </pre>
        )}
        <div className="mt-3 flex flex-wrap gap-2">
          <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={submitting} onClick={() => void previewDecision()}>Preview context diff</button>
          <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={applyDisabled} onClick={() => void applyDecision()}>Apply context decision</button>
          {item.resource?.url && (
            <a className="kg-control rounded-lg px-3 py-1.5 text-xs" href={String(item.resource.url)} target="_blank" rel="noreferrer">View resource</a>
          )}
        </div>
      </section>
    </article>
  );
}

function CandidateCard({ item, onDecision }: { item: ResourceReviewCandidateItem; onDecision: (id: string, decision: string, fallback: string) => void }) {
  return (
    <article className="kg-card rounded-2xl p-4 space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-text">{item.title}</div>
          <div className="mt-1 text-xs text-text-dim">
            Candidate {item.id}{item.nodeId ? ` · Suggested node ${item.nodeId}` : ''}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className={`rounded-full border px-2 py-0.5 text-[11px] ${statusClass(item.reviewStatus)}`}>{item.reviewStatus}</span>
          <Badge>score {Math.round((item.rankingScore || 0) * 100)}%</Badge>
          {item.duplicateResourceId && <Badge tone="warning">duplicate? {item.duplicateResourceId}</Badge>}
        </div>
      </div>
      {item.rawUrl && <a className="text-xs text-accent underline" href={item.rawUrl} target="_blank" rel="noreferrer">{item.rawUrl}</a>}
      {item.dedupeKey && <div className="text-xs text-text-dim">Dedupe key: {item.dedupeKey}</div>}
      <Warnings warnings={item.warnings} />
      <div className="flex flex-wrap gap-2">
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'hold', 'Candidate held for more context before admission.')}>Hold</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'needs_more_context', 'Candidate needs stronger provenance, source family, rights, or node mapping.')}>Needs More Context</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'reject_candidate', 'Candidate rejected by reviewer.')}>Reject</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'mark_duplicate', 'Candidate marked duplicate after reviewer comparison.')}>Mark duplicate</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.id, 'link_to_node', 'Reviewer requested node linkage; API will require complete resource/link fields.')}>Link to node</button>
      </div>
    </article>
  );
}

function LocalFileCard({ item, onDecision }: { item: ResourceReviewLocalFileItem; onDecision: (id: string, decision: string, fallback: string) => void }) {
  return (
    <article className="kg-card rounded-2xl p-4 space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-text">{item.title}</div>
          <div className="mt-1 text-xs text-text-dim">{item.localPath}</div>
        </div>
        <div className="flex flex-wrap gap-2">
          <Badge>{item.localFileType || 'local'}</Badge>
          <Badge>{item.admitted ? 'admitted' : 'not admitted'}</Badge>
          <Badge>{item.linkedNodeCount} linked nodes</Badge>
        </div>
      </div>
      {item.localFileHash && <div className="break-all rounded-lg bg-black/20 p-2 text-xs text-text-dim">Hash: {item.localFileHash}</div>}
      <Warnings warnings={item.warnings} />
      <div className="flex flex-wrap gap-2">
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.fileId, 'admit_as_resource', 'Local file admitted as metadata/hash-only resource after review.')}>Admit as resource</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.fileId, 'needs_review', 'Local file remains indexed but needs review before admission/linkage.')}>Needs review</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.fileId, 'ignore', 'Local file ignored for Resource Layer admission.')}>Ignore</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.fileId, 'reject_local_file', 'Local indexed file rejected for Resource Layer admission.')}>Reject</button>
        <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => onDecision(item.fileId, 'link_to_node', 'Reviewer requested explicit node linkage; API requires target node and link metadata.')}>Link to node</button>
      </div>
    </article>
  );
}

function EmptyState({ label }: { label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-8 text-center text-sm text-text-dim">
      No {label} records are currently in the review queue.
    </div>
  );
}

export default function ResourceReviewAdmin() {
  const [queue, setQueue] = useState<ResourceReviewQueue | null>(null);
  const [tab, setTab] = useState<ReviewTab>('needs_review');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingDecision, setPendingDecision] = useState<PendingResourceDecision | null>(null);
  const adminGateOpen = isLocalDevAdminGateOpen();

  async function loadQueue() {
    setRefreshing(true);
    try {
      const nextQueue = await getResourceReviewQueue({ status: 'all' });
      setQueue(nextQueue);
      setError(null);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to load resource review queue');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    void loadQueue();
  }, []);

  function decideLink(id: string, decision: string, fallback: string) {
    setPendingDecision({ targetType: 'link', id, decision, fallbackRationale: fallback });
  }

  function decideCandidate(id: string, decision: string, fallback: string) {
    setPendingDecision({ targetType: 'candidate', id, decision, fallbackRationale: fallback });
  }

  function decideLocalFile(id: string, decision: string, fallback: string) {
    setPendingDecision({ targetType: 'local_file', id, decision, fallbackRationale: fallback });
  }

  async function submitPendingDecision(body: Record<string, unknown>) {
    if (!pendingDecision) return null;
    if (!adminGateOpen) throw new Error('Local/dev admin gate is closed.');
    let result: unknown;
    try {
      if (pendingDecision.targetType === 'link') {
        result = await submitLinkReviewDecision(pendingDecision.id, body);
      } else if (pendingDecision.targetType === 'candidate') {
        result = await submitCandidateReviewDecision(pendingDecision.id, body);
      } else {
        result = await submitLocalFileReviewDecision(pendingDecision.id, body);
      }
      if (!body.dryRun) await loadQueue();
      return result;
    } catch (nextError) {
      const message = nextError instanceof Error ? nextError.message : 'Failed to submit resource review decision';
      setError(message);
      throw nextError;
    }
  }

  const metrics = queue?.metrics || defaultMetrics;
  const activeItems = useMemo(() => {
    if (!queue) return [];
    if (tab === 'needs_review') return queue.needsReviewLinks;
    if (tab === 'candidates') return queue.candidates;
    if (tab === 'local_files') return queue.localFiles;
    if (tab === 'rejected') return queue.rejectedLinks;
    if (tab === 'standards') return queue.standardsMissingContext;
    return queue.acceptedLinks;
  }, [queue, tab]);

  return (
    <div className="kg-shell min-h-screen bg-bg p-6 text-text">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-[11px] uppercase tracking-[0.24em] text-amber-100">
              Local/dev admin tool · file-backed registry
            </div>
            <h1 className="mt-3 text-3xl font-semibold">Resource Review Queue</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-text-dim">
              Review candidate, needs_review, rejected, standards-context, and local indexed resources before anything is accepted. This panel does not auto-promote candidates, does not auto-link local files, and does not write to Neo4j.
            </p>
          </div>
          <div className="flex gap-2">
            <Link to="/" className="kg-control rounded-xl px-3 py-2 text-sm">Home</Link>
            <button className="kg-control rounded-xl px-3 py-2 text-sm" onClick={() => void loadQueue()} disabled={refreshing}>
              {refreshing ? 'Refreshing…' : 'Refresh'}
            </button>
          </div>
        </header>

        {!adminGateOpen && (
          <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-100" role="alert">
            Local/dev admin gate is closed. Review records can be inspected, but mutations are disabled outside localhost/dev or without VITE_ENABLE_DEV_ADMIN=true.
          </div>
        )}

        <section className="grid grid-cols-2 gap-3 md:grid-cols-5">
          <MetricCard label="Resources total" value={metrics.resourcesTotal ?? metrics.acceptedResources} />
          <MetricCard label="Resources w/ accepted links" value={metrics.resourcesWithAcceptedLinks ?? metrics.acceptedNodeResourceLinks} />
          <MetricCard label="Accepted links" value={metrics.acceptedLinks} />
          <MetricCard label="Needs review" value={metrics.needsReviewLinks} danger={Boolean(metrics.needsReviewLinks)} />
          <MetricCard label="Rejected" value={metrics.rejectedLinks} />
          <MetricCard label="Candidates" value={metrics.candidates} danger={Boolean(metrics.candidates)} />
          <MetricCard label="Local indexed" value={metrics.localFilesIndexed} />
          <MetricCard label="Local admitted" value={metrics.localFilesAdmitted} />
          <MetricCard label="Standards missing context" value={metrics.standardsMissingContext} danger={Boolean(metrics.standardsMissingContext)} />
          <MetricCard label="Std. missing edition" value={metrics.standardsMissingEdition} danger={Boolean(metrics.standardsMissingEdition)} />
          <MetricCard label="Std. promotion blocked" value={metrics.standardsPromotionBlocked} danger={Boolean(metrics.standardsPromotionBlocked)} />
          <MetricCard label="Duplicate warnings" value={metrics.duplicateWarnings} danger={Boolean(metrics.duplicateWarnings)} />
          <MetricCard label="Broken link warnings" value={metrics.brokenLinkWarnings} danger={Boolean(metrics.brokenLinkWarnings)} />
          <MetricCard label="Decision history" value={metrics.reviewDecisions || 0} />
        </section>

        {error && (
          <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-100" role="alert">
            {error}
          </div>
        )}

        {loading && (
          <div className="rounded-2xl border border-white/10 bg-white/5 p-8 text-center text-sm text-text-dim">
            Loading resource review queue…
          </div>
        )}

        {!loading && queue && (
          <>
            <nav className="flex flex-wrap gap-2">
              {tabs.map((entry) => (
                <button
                  key={entry.id}
                  onClick={() => setTab(entry.id)}
                  className={`rounded-xl border px-3 py-2 text-sm ${tab === entry.id ? 'border-accent bg-accent/15 text-text' : 'border-white/10 bg-white/5 text-text-dim'}`}
                >
                  {entry.label}
                </button>
              ))}
            </nav>

            {pendingDecision && (
              <DecisionForm
                pending={pendingDecision}
                onCancel={() => setPendingDecision(null)}
                onSubmit={submitPendingDecision}
              />
            )}

            <section className="space-y-3">
              {activeItems.length === 0 && <EmptyState label={tabs.find((entry) => entry.id === tab)?.label || 'review'} />}
              {tab === 'candidates' && (activeItems as ResourceReviewCandidateItem[]).map((item) => (
                <CandidateCard key={item.id} item={item} onDecision={decideCandidate} />
              ))}
              {tab === 'local_files' && (activeItems as ResourceReviewLocalFileItem[]).map((item) => (
                <LocalFileCard key={item.id} item={item} onDecision={decideLocalFile} />
              ))}
              {tab === 'standards' && (activeItems as ResourceReviewLinkItem[]).map((item) => (
                <StandardsContextCard key={item.id} item={item} adminGateOpen={adminGateOpen} onChanged={loadQueue} />
              ))}
              {tab !== 'candidates' && tab !== 'local_files' && tab !== 'standards' && (activeItems as ResourceReviewLinkItem[]).map((item) => (
                <LinkCard key={item.id} item={item} onDecision={decideLink} />
              ))}
            </section>
          </>
        )}
      </div>
    </div>
  );
}
