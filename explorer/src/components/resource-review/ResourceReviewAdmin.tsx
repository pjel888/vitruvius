import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  applyExternalCandidateCorrection,
  applyExternalCandidateReviewDecision,
  getExternalCandidateDecisionHistory,
  getResourceReviewQueue,
  getResourceReviewSourceCustody,
  listExternalMetadataCandidates,
  persistExternalMetadataCandidate,
  previewExternalCandidateCorrection,
  previewExternalCandidatePromotion,
  previewExternalMetadataCandidate,
  previewExternalCandidateReviewDecision,
  previewStandardsContextDecision,
  submitCandidateReviewDecision,
  submitLinkReviewDecision,
  submitLocalFileReviewDecision,
  submitStandardsContextDecision,
} from '../../api/graphApi';
import type {
  ExternalMetadataCandidatePreview,
  ExternalMetadataCandidateRecord,
  ResourceReviewCandidateItem,
  ResourceReviewLinkItem,
  ResourceReviewLocalFileItem,
  ResourceReviewMetrics,
  ResourceReviewQueue,
  SourceCustodyItem,
  SourceCustodyQueue,
  StandardsContextPreviewResponse,
} from '../../types';

type ReviewTab = 'needs_review' | 'candidates' | 'local_files' | 'rejected' | 'standards' | 'accepted' | 'source_custody' | 'external_candidates';

const tabs: { id: ReviewTab; label: string }[] = [
  { id: 'source_custody', label: 'Source Custody' },
  { id: 'needs_review', label: 'Needs Review' },
  { id: 'candidates', label: 'Candidates' },
  { id: 'external_candidates', label: 'External Candidates' },
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

function Badge({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'neutral' | 'warning' | 'danger' | 'success' }) {
  const toneClass = tone === 'danger'
    ? 'border-rose-400/30 bg-rose-400/10 text-rose-100'
    : tone === 'warning'
      ? 'border-amber-400/30 bg-amber-400/10 text-amber-100'
      : tone === 'success'
        ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-100'
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

function custodyBadgeTone(custodyStatus: string) {
  if (custodyStatus === 'learner_visible') return 'success';
  if (custodyStatus === 'blocked' || custodyStatus === 'rejected') return 'danger';
  if (custodyStatus === 'rights_limited' || custodyStatus === 'standards_incomplete') return 'warning';
  return 'neutral';
}

function CustodyBadge({ status }: { status: string }) {
  const labels: Record<string, string> = {
    learner_visible: 'Learner visible',
    reviewer_only: 'Reviewer only',
    blocked: 'Blocked',
    needs_review: 'Needs review',
    candidate: 'Candidate',
    indexed_only: 'Indexed only',
    standards_incomplete: 'Context incomplete',
    rights_limited: 'Rights limited',
  };
  return <Badge tone={custodyBadgeTone(status)}>{labels[status] || status}</Badge>;
}

function SourceCustodyCard({ item }: { item: SourceCustodyItem }) {
  return (
    <article className="kg-card rounded-2xl p-4 space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-text">{item.title}</div>
          <div className="mt-1 text-xs text-text-dim">
            {item.itemType === 'resource_link' && <>Node {item.nodeId} · Resource {item.resourceId}</>}
            {item.itemType === 'candidate' && <>Candidate · {item.rawUrl || item.id}</>}
            {item.itemType === 'local_file' && <>{item.localPath || item.id}</>}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <CustodyBadge status={item.custodyStatus} />
          {item.learnerEligible && <Badge tone="success">learner eligible</Badge>}
          {!item.learnerEligible && <Badge tone="warning">not learner visible</Badge>}
          {item.promotionBlocked && <Badge tone="danger">promotion blocked</Badge>}
          {item.rightsStatus && <Badge>{item.rightsStatus}</Badge>}
          {item.standardsContextStatus && <Badge>{item.standardsContextStatus}</Badge>}
        </div>
      </div>

      {item.reviewerOnlyReason && (
        <div className="rounded-lg border border-amber-400/20 bg-amber-400/10 px-2 py-1.5 text-xs text-amber-100">
          <span className="font-medium">Reviewer-only reason:</span> {item.reviewerOnlyReason}
        </div>
      )}

      {item.hiddenReason && (
        <div className="rounded-lg border border-rose-400/20 bg-rose-400/10 px-2 py-1.5 text-xs text-rose-100">
          <span className="font-medium">Hidden from learners:</span> {item.hiddenReason}
        </div>
      )}

      {item.nextReviewAction && (
        <div className="rounded-lg border border-sky-400/20 bg-sky-400/10 px-2 py-1.5 text-xs text-sky-100">
          <span className="font-medium">Next action:</span> {item.nextReviewAction}
        </div>
      )}

      {item.warningFlags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {item.warningFlags.map((flag) => (
            <span key={flag} className="rounded-full border border-amber-400/20 bg-amber-400/10 px-2 py-0.5 text-[10px] text-amber-100">
              {flag.replace(/_/g, ' ')}
            </span>
          ))}
        </div>
      )}

      {item.missingStandardContextFields && item.missingStandardContextFields.length > 0 && (
        <div className="text-xs text-text-dim">
          <span className="text-text">Missing context:</span> {item.missingStandardContextFields.join(', ')}
        </div>
      )}

      {item.warnings && item.warnings.length > 0 && <Warnings warnings={item.warnings} />}
    </article>
  );
}

function ExternalCandidatePreviewForm({
  form,
  setForm,
  preview,
  setPreview,
  loading,
  setLoading,
  adminGateOpen,
  onSaved,
}: {
  form: Record<string, unknown>;
  setForm: (v: Record<string, unknown>) => void;
  preview: ExternalMetadataCandidatePreview | null;
  setPreview: (v: ExternalMetadataCandidatePreview | null) => void;
  loading: boolean;
  setLoading: (v: boolean) => void;
  adminGateOpen: boolean;
  onSaved?: () => void;
}) {
  const [formError, setFormError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [saving, setSaving] = useState(false);

  function updateField(name: string, value: unknown) {
    setForm({ ...form, [name]: value });
    setPreview(null);
    setFormError(null);
    setSaveStatus(null);
  }

  async function handlePreview() {
    setLoading(true);
    setFormError(null);
    setSaveStatus(null);
    try {
      const body: Record<string, unknown> = {
        title: form.title,
        resourceType: form.resourceType,
        sourceType: form.sourceType || undefined,
        proposedUrl: form.proposedUrl || undefined,
        proposedDoi: form.proposedDoi || undefined,
        proposedIsbn: form.proposedIsbn || undefined,
        proposedPublisher: form.proposedPublisher || undefined,
        proposedAuthors: String(form.proposedAuthors || '').split(',').map((s) => s.trim()).filter(Boolean),
        proposedPublicationDate: form.proposedPublicationDate || undefined,
        proposedEdition: form.proposedEdition || undefined,
        proposedVersion: form.proposedVersion || undefined,
        proposedScope: form.proposedScope || undefined,
        proposedJurisdiction: form.proposedJurisdiction || undefined,
        candidateRationale: form.candidateRationale || undefined,
        submittedBy: form.submittedBy || undefined,
      };
      const result = await previewExternalMetadataCandidate(body);
      setPreview(result as unknown as ExternalMetadataCandidatePreview);
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Preview failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    if (!preview) return;
    setSaving(true);
    setSaveStatus(null);
    try {
      const body: Record<string, unknown> = {
        title: form.title,
        resourceType: form.resourceType,
        sourceType: form.sourceType || undefined,
        proposedUrl: form.proposedUrl || undefined,
        proposedDoi: form.proposedDoi || undefined,
        proposedIsbn: form.proposedIsbn || undefined,
        proposedPublisher: form.proposedPublisher || undefined,
        proposedAuthors: String(form.proposedAuthors || '').split(',').map((s) => s.trim()).filter(Boolean),
        proposedPublicationDate: form.proposedPublicationDate || undefined,
        proposedEdition: form.proposedEdition || undefined,
        proposedVersion: form.proposedVersion || undefined,
        proposedScope: form.proposedScope || undefined,
        proposedJurisdiction: form.proposedJurisdiction || undefined,
        candidateRationale: form.candidateRationale || undefined,
        submittedBy: form.submittedBy || undefined,
      };
      const result = await persistExternalMetadataCandidate(body);
      if ((result as Record<string, unknown>).ok) {
        const candidate = (result as Record<string, unknown>).candidate as ExternalMetadataCandidateRecord;
        setSaveStatus({ type: 'success', message: `Saved as reviewer-only candidate: ${candidate.candidateId}` });
        onSaved?.();
      } else {
        const errorMsg = ((result as Record<string, unknown>).error as Record<string, string>)?.message || 'Save failed';
        setSaveStatus({ type: 'error', message: errorMsg });
      }
    } catch (err) {
      setSaveStatus({ type: 'error', message: err instanceof Error ? err.message : 'Save failed' });
    } finally {
      setSaving(false);
    }
  }

  const canSave = preview && preview.fakePlaceholderFlags.length === 0 && adminGateOpen;

  const inputClass = 'w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-text placeholder:text-text-dim/50 focus:border-accent focus:outline-none';

  return (
    <div className="space-y-4">
      {!adminGateOpen && (
        <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-100" role="alert">
          Local/dev admin gate is closed. External candidate preview is disabled outside localhost/dev.
        </div>
      )}

      <div className="kg-card rounded-2xl p-4 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium">External Metadata Candidate Preview</h3>
          <Badge tone="warning">Preview only · No auto-verification</Badge>
        </div>

        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          <div className="md:col-span-2">
            <label className="mb-1 block text-xs text-text-dim">Title *</label>
            <input className={inputClass} value={String(form.title || '')} onChange={(e) => updateField('title', e.target.value)} placeholder="Resource title" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Resource Type *</label>
            <select className={inputClass} value={String(form.resourceType || 'external_url_candidate')} onChange={(e) => updateField('resourceType', e.target.value)}>
              <option value="external_url_candidate">External URL</option>
              <option value="book_candidate">Book</option>
              <option value="pdf_candidate">PDF</option>
              <option value="standard_candidate">Standard</option>
              <option value="guide_candidate">Guide</option>
              <option value="article_candidate">Article</option>
              <option value="dataset_candidate">Dataset</option>
              <option value="source_family_reference">Source Family Reference</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">URL</label>
            <input className={inputClass} value={String(form.proposedUrl || '')} onChange={(e) => updateField('proposedUrl', e.target.value)} placeholder="https://…" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">DOI</label>
            <input className={inputClass} value={String(form.proposedDoi || '')} onChange={(e) => updateField('proposedDoi', e.target.value)} placeholder="10.xxxx/xxxx" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">ISBN</label>
            <input className={inputClass} value={String(form.proposedIsbn || '')} onChange={(e) => updateField('proposedIsbn', e.target.value)} placeholder="978-…" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Publisher</label>
            <input className={inputClass} value={String(form.proposedPublisher || '')} onChange={(e) => updateField('proposedPublisher', e.target.value)} placeholder="Publisher name" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Authors (comma-separated)</label>
            <input className={inputClass} value={String(form.proposedAuthors || '')} onChange={(e) => updateField('proposedAuthors', e.target.value)} placeholder="Author 1, Author 2" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Publication Date</label>
            <input className={inputClass} value={String(form.proposedPublicationDate || '')} onChange={(e) => updateField('proposedPublicationDate', e.target.value)} placeholder="YYYY or YYYY-MM" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Edition</label>
            <input className={inputClass} value={String(form.proposedEdition || '')} onChange={(e) => updateField('proposedEdition', e.target.value)} placeholder="e.g. 7th ed." />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Version</label>
            <input className={inputClass} value={String(form.proposedVersion || '')} onChange={(e) => updateField('proposedVersion', e.target.value)} placeholder="e.g. 2022" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Scope</label>
            <input className={inputClass} value={String(form.proposedScope || '')} onChange={(e) => updateField('proposedScope', e.target.value)} placeholder="Geographic or topical scope" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Jurisdiction</label>
            <input className={inputClass} value={String(form.proposedJurisdiction || '')} onChange={(e) => updateField('proposedJurisdiction', e.target.value)} placeholder="e.g. US, Philippines" />
          </div>
          <div className="md:col-span-2">
            <label className="mb-1 block text-xs text-text-dim">Candidate Rationale</label>
            <textarea className={inputClass} rows={2} value={String(form.candidateRationale || '')} onChange={(e) => updateField('candidateRationale', e.target.value)} placeholder="Why should this resource be reviewed?" />
          </div>
          <div>
            <label className="mb-1 block text-xs text-text-dim">Submitted By</label>
            <input className={inputClass} value={String(form.submittedBy || '')} onChange={(e) => updateField('submittedBy', e.target.value)} placeholder="Reviewer name or identifier" />
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            className="kg-control rounded-lg px-4 py-2 text-sm"
            disabled={loading || !adminGateOpen}
            onClick={() => void handlePreview()}
          >
            {loading ? 'Previewing…' : 'Preview Candidate'}
          </button>
          {canSave && (
            <button
              className="kg-control rounded-lg px-4 py-2 text-sm bg-accent/20 hover:bg-accent/30"
              disabled={saving}
              onClick={() => void handleSave()}
            >
              {saving ? 'Saving…' : 'Save as reviewer-only candidate'}
            </button>
          )}
          <span className="text-xs text-text-dim">Does not create resources, links, or accepted candidates.</span>
        </div>

        {formError && (
          <div className="rounded-lg border border-rose-400/30 bg-rose-400/10 px-3 py-2 text-xs text-rose-100">
            {formError}
          </div>
        )}
        {saveStatus && (
          <div className={`rounded-lg border px-3 py-2 text-xs ${saveStatus.type === 'success' ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-100' : 'border-rose-400/30 bg-rose-400/10 text-rose-100'}`}>
            {saveStatus.message}
          </div>
        )}
      </div>

      {preview && (
        <article className="kg-card rounded-2xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium">Preview Result</h4>
            <div className="flex gap-2">
              <Badge tone="warning">{preview.verificationStatus}</Badge>
              <Badge tone="danger">{preview.learnerVisible ? 'learner visible' : 'not learner visible'}</Badge>
              <Badge>{preview.displayPolicy}</Badge>
            </div>
          </div>

          <div className="rounded-lg border border-amber-400/20 bg-amber-400/10 px-3 py-2 text-xs text-amber-100">
            <span className="font-medium">Source truth caveat:</span> {preview.sourceTruthCaveat}
          </div>

          {preview.warningFlags.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {preview.warningFlags.map((flag) => (
                <span key={flag} className="rounded-full border border-amber-400/20 bg-amber-400/10 px-2 py-0.5 text-[10px] text-amber-100">
                  {flag.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          )}

          {preview.fakePlaceholderFlags.length > 0 && (
            <div className="rounded-lg border border-rose-400/20 bg-rose-400/10 px-3 py-2 text-xs text-rose-100">
              <span className="font-medium">Placeholder flags:</span>{' '}
              {preview.fakePlaceholderFlags.join(', ')}
            </div>
          )}

          {preview.missingFields.length > 0 && (
            <div className="text-xs text-text-dim">
              <span className="text-text">Missing fields:</span>{' '}
              {preview.missingFields.join(', ')}
            </div>
          )}

          {preview.normalizedUrl && (
            <div className="text-xs text-text-dim">
              <span className="text-text">Normalized URL:</span>{' '}
              <code className="rounded bg-black/20 px-1 py-0.5 text-sky-100">{preview.normalizedUrl}</code>
            </div>
          )}
          {preview.normalizedDoi && (
            <div className="text-xs text-text-dim">
              <span className="text-text">Normalized DOI:</span>{' '}
              <code className="rounded bg-black/20 px-1 py-0.5 text-sky-100">{preview.normalizedDoi}</code>
            </div>
          )}
          {preview.normalizedIsbn && (
            <div className="text-xs text-text-dim">
              <span className="text-text">Normalized ISBN:</span>{' '}
              <code className="rounded bg-black/20 px-1 py-0.5 text-sky-100">{preview.normalizedIsbn}</code>
            </div>
          )}

          {canSave && (
            <div className="rounded-lg border border-sky-400/20 bg-sky-400/10 px-3 py-2 text-xs text-sky-100">
              <span className="font-medium">Ready to save:</span> This candidate passes validation and contains no placeholders.
              It will be stored as unverified, reviewer-only metadata. No resource or link will be created.
            </div>
          )}

          <pre className="max-h-72 overflow-auto rounded-lg bg-black/30 p-3 text-xs text-text-dim" aria-label="External candidate preview JSON">
            {JSON.stringify(preview, null, 2)}
          </pre>
        </article>
      )}
    </div>
  );
}

function ExternalCandidateReviewPanel({
  candidate,
  onChanged,
  adminGateOpen,
}: {
  candidate: ExternalMetadataCandidateRecord;
  onChanged: () => void;
  adminGateOpen: boolean;
}) {
  const [mode, setMode] = useState<'detail' | 'correction' | 'decision' | 'history' | 'promotion'>('detail');
  const [correctionPatch, setCorrectionPatch] = useState<Record<string, unknown>>({});
  const [correctionPreview, setCorrectionPreview] = useState<Record<string, unknown> | null>(null);
  const [correctionLoading, setCorrectionLoading] = useState(false);
  const [decisionType, setDecisionType] = useState('mark_needs_review');
  const [reviewer, setReviewer] = useState('local-dev-reviewer');
  const [rationale, setRationale] = useState('');
  const [rejectionReasons, setRejectionReasons] = useState('');
  const [duplicateOfId, setDuplicateOfId] = useState('');
  const [decisionPreview, setDecisionPreview] = useState<Record<string, unknown> | null>(null);
  const [decisionLoading, setDecisionLoading] = useState(false);
  const [history, setHistory] = useState<Record<string, unknown>[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [promotionPreview, setPromotionPreview] = useState<Record<string, unknown> | null>(null);
  const [promotionLoading, setPromotionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === 'history') {
      setHistoryLoading(true);
      getExternalCandidateDecisionHistory(candidate.candidateId)
        .then((data) => setHistory(data.decisions))
        .catch(() => setHistory([]))
        .finally(() => setHistoryLoading(false));
    }
    if (mode === 'promotion') {
      setPromotionLoading(true);
      setError(null);
      previewExternalCandidatePromotion(candidate.candidateId)
        .then((data) => setPromotionPreview(data))
        .catch((e) => setError(e instanceof Error ? e.message : 'Promotion preview failed'))
        .finally(() => setPromotionLoading(false));
    }
  }, [mode, candidate.candidateId]);

  async function runCorrectionPreview() {
    if (!adminGateOpen) return;
    setCorrectionLoading(true);
    setError(null);
    try {
      const result = await previewExternalCandidateCorrection(candidate.candidateId, {
        patch: correctionPatch,
        reviewer,
        rationale: rationale || 'correction preview',
      });
      setCorrectionPreview(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Correction preview failed');
    } finally {
      setCorrectionLoading(false);
    }
  }

  async function runCorrectionApply() {
    if (!adminGateOpen) return;
    setCorrectionLoading(true);
    setError(null);
    try {
      await applyExternalCandidateCorrection(candidate.candidateId, {
        patch: correctionPatch,
        reviewer,
        rationale: rationale || 'correction apply',
      });
      setCorrectionPreview(null);
      setCorrectionPatch({});
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Correction apply failed');
    } finally {
      setCorrectionLoading(false);
    }
  }

  async function runDecisionPreview() {
    if (!adminGateOpen) return;
    setDecisionLoading(true);
    setError(null);
    try {
      const body: Record<string, unknown> = {
        reviewer,
        rationale: rationale || 'review decision',
        decisionType,
      };
      if (rejectionReasons) body.rejectionReasons = rejectionReasons.split(',').map((s) => s.trim()).filter(Boolean);
      if (duplicateOfId) body.duplicateOfCandidateId = duplicateOfId;
      const result = await previewExternalCandidateReviewDecision(candidate.candidateId, body);
      setDecisionPreview(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Decision preview failed');
    } finally {
      setDecisionLoading(false);
    }
  }

  async function runDecisionApply() {
    if (!adminGateOpen) return;
    setDecisionLoading(true);
    setError(null);
    try {
      const body: Record<string, unknown> = {
        reviewer,
        rationale: rationale || 'review decision',
        decisionType,
      };
      if (rejectionReasons) body.rejectionReasons = rejectionReasons.split(',').map((s) => s.trim()).filter(Boolean);
      if (duplicateOfId) body.duplicateOfCandidateId = duplicateOfId;
      await applyExternalCandidateReviewDecision(candidate.candidateId, body);
      setDecisionPreview(null);
      setRationale('');
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Decision apply failed');
    } finally {
      setDecisionLoading(false);
    }
  }

  const readiness = (decisionPreview?.promotionReadinessChecklist || correctionPreview?.promotionReadinessChecklist || {}) as Record<string, boolean>;
  const blockers = ((decisionPreview?.blockers || correctionPreview?.blockers || []) as string[]);
  const warnings = ((decisionPreview?.warnings || correctionPreview?.warnings || []) as string[]);

  return (
    <div className="kg-card rounded-2xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-medium">Candidate Review: {candidate.title}</h4>
        <div className="flex gap-1.5">
          <Badge tone="warning">{candidate.verificationStatus}</Badge>
          <Badge tone="danger">{candidate.learnerVisible ? 'learner visible' : 'not learner visible'}</Badge>
          <Badge>{candidate.status?.replace(/_/g, ' ')}</Badge>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <button className={`kg-control rounded-lg px-2 py-1 text-xs ${mode === 'detail' ? 'bg-accent/30' : ''}`} onClick={() => setMode('detail')}>Detail</button>
        <button className={`kg-control rounded-lg px-2 py-1 text-xs ${mode === 'correction' ? 'bg-accent/30' : ''}`} onClick={() => setMode('correction')}>Correction</button>
        <button className={`kg-control rounded-lg px-2 py-1 text-xs ${mode === 'decision' ? 'bg-accent/30' : ''}`} onClick={() => setMode('decision')}>Review Decision</button>
        <button className={`kg-control rounded-lg px-2 py-1 text-xs ${mode === 'history' ? 'bg-accent/30' : ''}`} onClick={() => setMode('history')}>History ({candidate.decisions?.length ?? 0})</button>
        <button className={`kg-control rounded-lg px-2 py-1 text-xs ${mode === 'promotion' ? 'bg-accent/30' : ''}`} onClick={() => setMode('promotion')}>Promotion Preview</button>
      </div>

      {mode === 'detail' && (
        <div className="space-y-2 text-xs text-text-dim">
          <div><span className="text-text">ID:</span> {candidate.candidateId}</div>
          <div><span className="text-text">Type:</span> {candidate.resourceType}</div>
          {candidate.proposedUrl && <div><span className="text-text">URL:</span> {candidate.proposedUrl}</div>}
          {candidate.proposedDoi && <div><span className="text-text">DOI:</span> {candidate.proposedDoi}</div>}
          {candidate.proposedIsbn && <div><span className="text-text">ISBN:</span> {candidate.proposedIsbn}</div>}
          {candidate.proposedEdition && <div><span className="text-text">Edition:</span> {candidate.proposedEdition}</div>}
          {candidate.proposedJurisdiction && <div><span className="text-text">Jurisdiction:</span> {candidate.proposedJurisdiction}</div>}
          {candidate.proposedScope && <div><span className="text-text">Scope:</span> {candidate.proposedScope}</div>}
          <Warnings warnings={candidate.warningFlags} />
          {candidate.missingFields && candidate.missingFields.length > 0 && (
            <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 px-2 py-1 text-xs text-amber-100">
              Missing: {candidate.missingFields.join(', ')}
            </div>
          )}
          <div className="mt-2 rounded-lg border border-white/10 bg-white/5 p-2">
            <div className="mb-1 text-[10px] uppercase tracking-wider text-text-dim">Promotion Readiness</div>
            {Object.entries(readiness).map(([gate, passed]) => (
              <div key={gate} className="flex items-center gap-2">
                <span className={passed ? 'text-emerald-400' : 'text-rose-400'}>{passed ? '✓' : '✗'}</span>
                <span className="text-text-dim">{gate.replace(/Gate$/, '').replace(/([A-Z])/g, ' $1').trim()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {mode === 'correction' && (
        <div className="space-y-3">
          <div className="text-xs text-text-dim">Edit candidate metadata. No resource or link will be created.</div>
          <div className="grid gap-2 md:grid-cols-2">
            <label className="space-y-1 text-xs text-text-dim">Title <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.title ?? candidate.title ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, title: e.target.value })} /></label>
            <label className="space-y-1 text-xs text-text-dim">URL <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.proposedUrl ?? candidate.proposedUrl ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, proposedUrl: e.target.value })} /></label>
            <label className="space-y-1 text-xs text-text-dim">DOI <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.proposedDoi ?? candidate.proposedDoi ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, proposedDoi: e.target.value })} /></label>
            <label className="space-y-1 text-xs text-text-dim">ISBN <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.proposedIsbn ?? candidate.proposedIsbn ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, proposedIsbn: e.target.value })} /></label>
            <label className="space-y-1 text-xs text-text-dim">Edition <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.proposedEdition ?? candidate.proposedEdition ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, proposedEdition: e.target.value })} /></label>
            <label className="space-y-1 text-xs text-text-dim">Jurisdiction <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={String(correctionPatch.proposedJurisdiction ?? candidate.proposedJurisdiction ?? '')} onChange={(e) => setCorrectionPatch({ ...correctionPatch, proposedJurisdiction: e.target.value })} /></label>
          </div>
          <div className="flex flex-wrap gap-2">
            <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={correctionLoading} onClick={runCorrectionPreview}>Preview correction</button>
            <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={correctionLoading || !adminGateOpen} onClick={runCorrectionApply}>Apply correction</button>
          </div>
          {correctionPreview && (
            <div className="space-y-2">
              {blockers.length > 0 && <div className="rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">Blockers: {blockers.join(', ')}</div>}
              {warnings.length > 0 && <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-2 text-xs text-amber-100">Warnings: {warnings.join(', ')}</div>}
              <div className="text-xs text-text-dim">Changed fields: {(correctionPreview.diff as any)?.changedFields?.join(', ') || 'none'}</div>
            </div>
          )}
        </div>
      )}

      {mode === 'decision' && (
        <div className="space-y-3">
          <div className="text-xs text-text-dim">Choose a review decision. No resource or link will be created.</div>
          <select className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={decisionType} onChange={(e) => setDecisionType(e.target.value)}>
            <option value="mark_needs_review">Needs review</option>
            <option value="request_metadata_correction">Metadata correction needed</option>
            <option value="request_source_custody_review">Source custody review needed</option>
            <option value="request_rights_review">Rights review needed</option>
            <option value="request_standards_context">Standards context needed</option>
            <option value="mark_duplicate">Duplicate candidate</option>
            <option value="reject_candidate">Reject candidate</option>
            <option value="defer_candidate">Defer candidate</option>
            <option value="mark_ready_for_promotion_review">Ready for promotion review</option>
            <option value="block_promotion">Block promotion</option>
          </select>
          <label className="block space-y-1 text-xs text-text-dim">Reviewer <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={reviewer} onChange={(e) => setReviewer(e.target.value)} /></label>
          <label className="block space-y-1 text-xs text-text-dim">Rationale <textarea className="kg-input min-h-16 w-full rounded-lg px-2 py-1 text-sm text-text" value={rationale} onChange={(e) => setRationale(e.target.value)} /></label>
          {decisionType === 'reject_candidate' && (
            <label className="block space-y-1 text-xs text-text-dim">Rejection reasons (comma-separated) <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={rejectionReasons} onChange={(e) => setRejectionReasons(e.target.value)} /></label>
          )}
          {decisionType === 'mark_duplicate' && (
            <label className="block space-y-1 text-xs text-text-dim">Duplicate of candidate ID <input className="kg-input w-full rounded-lg px-2 py-1 text-sm text-text" value={duplicateOfId} onChange={(e) => setDuplicateOfId(e.target.value)} /></label>
          )}
          <div className="flex flex-wrap gap-2">
            <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={decisionLoading} onClick={runDecisionPreview}>Preview decision</button>
            <button className="kg-control rounded-lg px-3 py-1.5 text-xs" disabled={decisionLoading || !adminGateOpen} onClick={runDecisionApply}>Apply decision</button>
          </div>
          {decisionPreview && (
            <div className="space-y-2">
              <div className="text-xs text-text-dim">Proposed status: <span className="text-text">{(decisionPreview as any).proposedNextStatus?.replace(/_/g, ' ')}</span></div>
              {blockers.length > 0 && <div className="rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">Blockers: {blockers.join(', ')}</div>}
              {warnings.length > 0 && <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-2 text-xs text-amber-100">Warnings: {warnings.join(', ')}</div>}
            </div>
          )}
        </div>
      )}

      {mode === 'history' && (
        <div className="space-y-2">
          {historyLoading && <div className="text-xs text-text-dim">Loading history...</div>}
          {!historyLoading && history.length === 0 && <div className="text-xs text-text-dim">No decisions recorded.</div>}
          {history.map((decision, i) => (
            <div key={i} className="rounded-lg border border-white/10 bg-white/5 p-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-medium text-text">{(decision as any).decisionType?.replace(/_/g, ' ')}</span>
                <span className="text-text-dim">{(decision as any).reviewer}</span>
              </div>
              <div className="mt-1 text-text-dim">{(decision as any).rationale}</div>
              <div className="mt-1 text-[10px] text-text-dim">{(decision as any).reviewedAt}</div>
            </div>
          ))}
        </div>
      )}

      {mode === 'promotion' && (
        <div className="space-y-3">
          {promotionLoading && <div className="text-xs text-text-dim">Loading promotion preview...</div>}
          {!promotionLoading && !promotionPreview && <div className="text-xs text-text-dim">No promotion preview available.</div>}
          {!promotionLoading && promotionPreview && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Badge tone={(promotionPreview as any).eligibleForPromotionPreview ? 'success' : 'danger'}>
                  {(promotionPreview as any).eligibleForPromotionPreview ? 'Eligible for promotion preview' : 'Not eligible'}
                </Badge>
                <Badge tone="warning">Preview only</Badge>
              </div>

              {((promotionPreview as any).blockers || []).length > 0 && (
                <div className="rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">
                  <div className="font-medium mb-1">Blockers</div>
                  {((promotionPreview as any).blockers as string[]).map((b, i) => (
                    <div key={`blocker-${i}`}>• {b}</div>
                  ))}
                </div>
              )}

              {((promotionPreview as any).warnings || []).length > 0 && (
                <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-2 text-xs text-amber-100">
                  <div className="font-medium mb-1">Warnings</div>
                  {((promotionPreview as any).warnings as string[]).map((w, i) => (
                    <div key={`warn-${i}`}>• {w}</div>
                  ))}
                </div>
              )}

              {((promotionPreview as any).missingFields || []).length > 0 && (
                <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-2 text-xs text-amber-100">
                  <div className="font-medium mb-1">Missing fields</div>
                  {((promotionPreview as any).missingFields as string[]).join(', ')}
                </div>
              )}

              {(promotionPreview as any).proposedResourceDraft && (
                <div className="rounded-lg border border-white/10 bg-white/5 p-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="text-xs font-medium text-text">Proposed Resource Draft</div>
                    <Badge tone="warning">Preview only — not created</Badge>
                  </div>
                  <div className="text-xs text-text-dim space-y-1">
                    <div><span className="text-text">resourceId:</span> {String((promotionPreview as any).proposedResourceDraft.resourceId)}</div>
                    <div><span className="text-text">title:</span> {String((promotionPreview as any).proposedResourceDraft.title)}</div>
                    <div><span className="text-text">resourceType:</span> {String((promotionPreview as any).proposedResourceDraft.resourceType)}</div>
                    <div><span className="text-text">verificationStatus:</span> {String((promotionPreview as any).proposedResourceDraft.verificationStatus)}</div>
                    <div><span className="text-text">learnerVisible:</span> {String((promotionPreview as any).proposedResourceDraft.learnerVisible)}</div>
                    <div><span className="text-text">status:</span> {String((promotionPreview as any).proposedResourceDraft.status)}</div>
                  </div>
                  <div className="text-[10px] text-text-dim">No resource will be created by this preview.</div>
                </div>
              )}

              {((promotionPreview as any).proposedNodeResourceLinkDrafts || []).length > 0 && (
                <div className="rounded-lg border border-white/10 bg-white/5 p-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="text-xs font-medium text-text">Proposed Node-Resource Link Drafts</div>
                    <Badge tone="warning">Preview only — not created</Badge>
                  </div>
                  {((promotionPreview as any).proposedNodeResourceLinkDrafts as any[]).map((link: any, i: number) => (
                    <div key={`link-${i}`} className="text-xs text-text-dim space-y-1">
                      <div><span className="text-text">linkId:</span> {String(link.linkId)}</div>
                      <div><span className="text-text">nodeId:</span> {String(link.nodeId)}</div>
                      <div><span className="text-text">relationship:</span> {String(link.relationship)}</div>
                      <div><span className="text-text">reviewStatus:</span> {String(link.reviewStatus)}</div>
                      <div><span className="text-text">learnerVisible:</span> {String(link.learnerVisible)}</div>
                    </div>
                  ))}
                  <div className="text-[10px] text-text-dim">No node link will be created by this preview.</div>
                </div>
              )}

              <div className="rounded-lg border border-white/10 bg-white/5 p-2 space-y-1 text-[10px] text-text-dim">
                <div>{(promotionPreview as any).sourceTruthCaveat}</div>
                <div>{(promotionPreview as any).standardsContextCaveat}</div>
                <div>{(promotionPreview as any).rightsCaveat}</div>
                <div>{(promotionPreview as any).verificationCaveat}</div>
              </div>

              <div className="flex flex-wrap gap-2">
                <Badge tone="danger">Promotion apply not implemented</Badge>
                <Badge tone="danger">No resource creation</Badge>
                <Badge tone="danger">No link creation</Badge>
                <Badge tone="danger">No learner exposure</Badge>
              </div>
            </div>
          )}
        </div>
      )}

      {error && <div className="rounded-lg border border-rose-400/30 bg-rose-400/10 p-2 text-xs text-rose-100">{error}</div>}
    </div>
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
  const [sourceCustody, setSourceCustody] = useState<SourceCustodyQueue | null>(null);
  const [tab, setTab] = useState<ReviewTab>('source_custody');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingDecision, setPendingDecision] = useState<PendingResourceDecision | null>(null);
  const [externalPreview, setExternalPreview] = useState<ExternalMetadataCandidatePreview | null>(null);
  const [externalPreviewLoading, setExternalPreviewLoading] = useState(false);
  const [persistedExternalCandidates, setPersistedExternalCandidates] = useState<ExternalMetadataCandidateRecord[]>([]);
  const [selectedExternalCandidate, setSelectedExternalCandidate] = useState<ExternalMetadataCandidateRecord | null>(null);
  const [externalForm, setExternalForm] = useState<Record<string, unknown>>({
    title: '',
    resourceType: 'external_url_candidate',
    proposedUrl: '',
    proposedDoi: '',
    proposedIsbn: '',
    proposedPublisher: '',
    proposedAuthors: '',
    proposedPublicationDate: '',
    proposedEdition: '',
    proposedVersion: '',
    proposedScope: '',
    proposedJurisdiction: '',
    candidateRationale: '',
    submittedBy: '',
  });
  const adminGateOpen = isLocalDevAdminGateOpen();

  async function loadPersistedExternalCandidates() {
    try {
      const data = await listExternalMetadataCandidates();
      setPersistedExternalCandidates(data.candidates as unknown as ExternalMetadataCandidateRecord[]);
    } catch {
      // Silently ignore; persisted candidates are optional display
    }
  }

  async function loadQueue() {
    setRefreshing(true);
    try {
      const [nextQueue, nextCustody] = await Promise.all([
        getResourceReviewQueue({ status: 'all' }),
        getResourceReviewSourceCustody(),
      ]);
      setQueue(nextQueue);
      setSourceCustody(nextCustody);
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
    void loadPersistedExternalCandidates();
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
  const custodyMetrics = sourceCustody?.metrics;
  const activeItems = useMemo(() => {
    if (!queue) return [];
    if (tab === 'source_custody') return sourceCustody?.groups ? Object.values(sourceCustody.groups).flat() : [];
    if (tab === 'needs_review') return queue.needsReviewLinks;
    if (tab === 'candidates') return queue.candidates;
    if (tab === 'external_candidates') return [];
    if (tab === 'local_files') return queue.localFiles;
    if (tab === 'rejected') return queue.rejectedLinks;
    if (tab === 'standards') return queue.standardsMissingContext;
    return queue.acceptedLinks;
  }, [queue, sourceCustody, tab]);

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

        {custodyMetrics && (
          <section className="rounded-2xl border border-accent/20 bg-accent/5 p-4">
            <div className="mb-2 text-xs uppercase tracking-[0.18em] text-text-dim">Source Custody Overview</div>
            <div className="grid grid-cols-2 gap-2 md:grid-cols-5">
              <MetricCard label="Learner visible" value={custodyMetrics.learnerVisible} />
              <MetricCard label="Reviewer only" value={custodyMetrics.reviewerOnly} />
              <MetricCard label="Needs review" value={custodyMetrics.needsReview} danger={Boolean(custodyMetrics.needsReview)} />
              <MetricCard label="Candidates" value={custodyMetrics.candidates} danger={Boolean(custodyMetrics.candidates)} />
              <MetricCard label="Indexed only" value={custodyMetrics.localFilesIndexedOnly} />
              <MetricCard label="Std. incomplete" value={custodyMetrics.standardsContextIncomplete} danger={Boolean(custodyMetrics.standardsContextIncomplete)} />
              <MetricCard label="Rights limited" value={custodyMetrics.rightsLimited} danger={Boolean(custodyMetrics.rightsLimited)} />
              <MetricCard label="Rejected" value={custodyMetrics.rejected} />
              <MetricCard label="Blocked" value={custodyMetrics.blocked} />
              <MetricCard label="Total" value={custodyMetrics.total} />
            </div>
          </section>
        )}

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
              {activeItems.length === 0 && tab !== 'external_candidates' && <EmptyState label={tabs.find((entry) => entry.id === tab)?.label || 'review'} />}
              {tab === 'source_custody' && (activeItems as SourceCustodyItem[]).map((item) => (
                <SourceCustodyCard key={item.id} item={item} />
              ))}
              {tab === 'candidates' && (activeItems as ResourceReviewCandidateItem[]).map((item) => (
                <CandidateCard key={item.id} item={item} onDecision={decideCandidate} />
              ))}
              {tab === 'external_candidates' && (
                <>
                  <ExternalCandidatePreviewForm
                    form={externalForm}
                    setForm={setExternalForm}
                    preview={externalPreview}
                    setPreview={setExternalPreview}
                    loading={externalPreviewLoading}
                    setLoading={setExternalPreviewLoading}
                    adminGateOpen={adminGateOpen}
                    onSaved={loadPersistedExternalCandidates}
                  />
                  {selectedExternalCandidate && (
                    <ExternalCandidateReviewPanel
                      candidate={selectedExternalCandidate}
                      onChanged={() => { loadPersistedExternalCandidates(); setSelectedExternalCandidate(null); }}
                      adminGateOpen={adminGateOpen}
                    />
                  )}
                  {persistedExternalCandidates.length > 0 && (
                    <div className="kg-card rounded-2xl p-4 space-y-3">
                      <h4 className="text-sm font-medium">Persisted External Candidates ({persistedExternalCandidates.length})</h4>
                      <div className="space-y-2">
                        {persistedExternalCandidates.map((c) => (
                          <button
                            key={c.candidateId}
                            className="w-full rounded-lg border border-white/10 bg-white/5 p-3 text-left text-xs hover:bg-white/10"
                            onClick={() => setSelectedExternalCandidate(c)}
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-medium text-text">{c.title}</span>
                              <div className="flex gap-1.5">
                                <Badge tone="warning">{c.verificationStatus}</Badge>
                                <Badge tone="danger">{c.learnerVisible ? 'learner visible' : 'not learner visible'}</Badge>
                                <Badge>{c.status?.replace(/_/g, ' ') || 'candidate'}</Badge>
                              </div>
                            </div>
                            <div className="mt-1 text-text-dim">
                              {c.resourceType} · {c.candidateId}
                            </div>
                            {c.warningFlags && c.warningFlags.length > 0 && (
                              <div className="mt-1 flex flex-wrap gap-1">
                                {c.warningFlags.map((f) => (
                                  <span key={f} className="rounded-full border border-amber-400/20 bg-amber-400/10 px-1.5 py-0.5 text-[10px] text-amber-100">{f.replace(/_/g, ' ')}</span>
                                ))}
                              </div>
                            )}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
              {tab === 'local_files' && (activeItems as ResourceReviewLocalFileItem[]).map((item) => (
                <LocalFileCard key={item.id} item={item} onDecision={decideLocalFile} />
              ))}
              {tab === 'standards' && (activeItems as ResourceReviewLinkItem[]).map((item) => (
                <StandardsContextCard key={item.id} item={item} adminGateOpen={adminGateOpen} onChanged={loadQueue} />
              ))}
              {tab !== 'source_custody' && tab !== 'candidates' && tab !== 'external_candidates' && tab !== 'local_files' && tab !== 'standards' && (activeItems as ResourceReviewLinkItem[]).map((item) => (
                <LinkCard key={item.id} item={item} onDecision={decideLink} />
              ))}
            </section>
          </>
        )}
      </div>
    </div>
  );
}
