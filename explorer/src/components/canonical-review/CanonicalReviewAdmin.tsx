import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  getCanonicalDuplicateGroups,
  getCanonicalValidation,
  getCanonicalBatches,
  getCanonicalApprovals,
  getCanonicalP1DecisionPackets,
  createCanonicalBatch,
  generateCanonicalP1DecisionPackets,
  getCanonicalDecisions,
  getCanonicalRemediation,
  getCanonicalRollbackPreview,
  previewCanonicalDecision,
  previewCanonicalApproval,
  previewCanonicalBatchDecision,
  submitCanonicalBatchDecision,
  submitCanonicalApproval,
  submitCanonicalDecision,
  submitCanonicalRemediationStatus,
  submitCanonicalRollback,
} from '../../api/graphApi';
import type { CanonicalAdmittedRelationship, CanonicalBatchRecord, CanonicalDecisionPreview, CanonicalDuplicateGroup, CanonicalDuplicateQueue, CanonicalP1DecisionPacket, CanonicalStewardshipApproval, CanonicalStewardshipDecision, CanonicalValidationResult } from '../../types';

const decisionTypes = [
  'NEEDS_HUMAN_REVIEW',
  'ALIAS_TO_CANONICAL',
  'KEEP_SEPARATE',
  'REJECT_DUPLICATE_CANDIDATE',
  'SPLIT_OR_RETYPE_NEEDED',
  'GOVERNED_DISAMBIGUATION',
  'RELATED_SPECIALIZATION',
  'CROSS_DOMAIN_EQUIVALENCE',
  'CANONICAL_LABEL_CLARIFICATION',
  'DISAMBIGUATED_KEEP_SEPARATE',
  'MERGE_INTO_CANONICAL',
] as const;

const approvalGateDecisionTypes = new Set<string>([
  'GOVERNED_DISAMBIGUATION',
  'RELATED_SPECIALIZATION',
  'CROSS_DOMAIN_EQUIVALENCE',
  'CANONICAL_LABEL_CLARIFICATION',
  'DISAMBIGUATED_KEEP_SEPARATE',
]);

function isLocalDevAdminGateOpen() {
  if (typeof window === 'undefined') return true;
  const host = window.location.hostname;
  return import.meta.env.DEV
    || import.meta.env.VITE_ENABLE_DEV_ADMIN === 'true'
    || host === 'localhost'
    || host === '127.0.0.1'
    || host === '::1';
}

function Badge({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'neutral' | 'warning' | 'danger' }) {
  const toneClass = tone === 'danger'
    ? 'border-rose-400/30 bg-rose-400/10 text-rose-100'
    : tone === 'warning'
      ? 'border-amber-400/30 bg-amber-400/10 text-amber-100'
      : 'border-white/10 bg-white/5 text-text-dim';
  return <span className={`rounded-full border px-2 py-0.5 text-[11px] ${toneClass}`}>{children}</span>;
}

function riskTone(risk: string): 'neutral' | 'warning' | 'danger' {
  if (risk === 'critical' || risk === 'high') return 'danger';
  if (risk === 'medium') return 'warning';
  return 'neutral';
}

function signatureTone(status?: string): 'neutral' | 'warning' | 'danger' {
  if (status === 'invalid' || status === 'unsupported') return 'danger';
  if (status === 'unsigned' || status === 'missing_key') return 'warning';
  return 'neutral';
}

function shortHashText(value?: string) {
  return value ? value.slice(0, 12) : 'missing';
}

function GroupCard({ group, selected, onSelect }: { group: CanonicalDuplicateGroup; selected: boolean; onSelect: () => void }) {
  return (
    <button
      className={`w-full rounded-2xl border p-4 text-left transition ${selected ? 'border-accent bg-accent/10' : 'border-white/10 bg-white/5 hover:border-white/20'}`}
      onClick={onSelect}
    >
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <div className="font-medium text-text">{group.looseNormalizedLabel}</div>
          <div className="mt-1 text-xs text-text-dim">{group.nodeIds.length} nodes · {group.edgeCount} edges · {group.resourceLinkCount} resource links</div>
        </div>
        <div className="flex flex-wrap gap-2">
          <Badge tone={riskTone(group.riskLevel)}>{group.riskLevel}</Badge>
          <Badge tone={group.priorityBand === 'P0' || group.priorityBand === 'BLOCKED' ? 'danger' : group.priorityBand === 'P1' ? 'warning' : 'neutral'}>{group.priorityBand}</Badge>
          <Badge>{group.status}</Badge>
        </div>
      </div>
      <div className="mt-2 text-xs leading-5 text-text-dim">
        {group.labels.join(', ')}
      </div>
    </button>
  );
}

function NodeSummary({ node }: { node: CanonicalDuplicateGroup['nodes'][number] }) {
  return (
    <article className="rounded-xl border border-white/10 bg-black/20 p-3">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <div className="font-medium text-text">{node.label}</div>
          <div className="mt-1 text-xs text-text-dim">{node.id}</div>
        </div>
        <Badge>{node.type || 'unknown'}</Badge>
      </div>
      <div className="mt-2 text-xs text-text-dim">
        Taxonomy: {node.taxonomyPath.length ? node.taxonomyPath.join(' > ') : 'none recorded'}
      </div>
      <div className="mt-1 text-xs text-accent">
        Disambiguation label: {node.taxonomyPath.length ? `${node.label} (${node.taxonomyPath.join(' > ')})` : `${node.label} (${node.type || 'untyped'})`}
      </div>
      <div className="mt-2 flex flex-wrap gap-2">
        <Badge>{node.incomingEdgeCount} incoming</Badge>
        <Badge>{node.outgoingEdgeCount} outgoing</Badge>
        <Badge>{node.resourceLinkCount} resources</Badge>
      </div>
      {node.aliases.length > 0 && <div className="mt-2 text-xs text-text-dim">Aliases: {node.aliases.join(', ')}</div>}
      <Link className="mt-3 inline-flex text-xs text-accent underline" to={`/explore?node=${encodeURIComponent(node.id)}`}>Open node</Link>
    </article>
  );
}

function PreviewPanel({ preview }: { preview: CanonicalDecisionPreview | null }) {
  if (!preview) return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-text-dim">
      Choose a decision and run Preview. No production graph nodes are merged from this panel without an explicit applied decision.
    </div>
  );
  return (
    <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="flex flex-wrap gap-2">
        <Badge tone={preview.blockers.length ? 'danger' : 'neutral'}>{preview.blockers.length} blockers</Badge>
        <Badge tone={preview.warnings.length ? 'warning' : 'neutral'}>{preview.warnings.length} warnings</Badge>
        <Badge>{preview.affectedEdgeIds.length} affected edges</Badge>
        <Badge>{preview.affectedResourceLinkIds.length} affected resource links</Badge>
        <Badge>{preview.selfLoopRisks.length} self-loop risks</Badge>
      </div>
      {preview.blockers.length > 0 && (
        <ul className="mt-3 space-y-1 text-xs text-rose-100">
          {preview.blockers.map((blocker) => <li key={blocker}>Blocker: {blocker}</li>)}
        </ul>
      )}
      {preview.warnings.length > 0 && (
        <ul className="mt-3 space-y-1 text-xs text-amber-100">
          {preview.warnings.map((warning) => <li key={warning}>Warning: {warning}</li>)}
        </ul>
      )}
      <pre className="mt-3 max-h-80 overflow-auto rounded-lg bg-black/30 p-3 text-xs text-text-dim">
        {JSON.stringify({
          decisionType: preview.decisionType,
          canonicalNodeId: preview.canonicalNodeId,
          sourceNodeIds: preview.sourceNodeIds,
          edgeRewrites: preview.edgeRewrites,
          resourceLinkRewrites: preview.resourceLinkRewrites,
          afterPreview: preview.afterPreview,
        }, null, 2)}
      </pre>
    </section>
  );
}

export default function CanonicalReviewAdmin() {
  const [queue, setQueue] = useState<CanonicalDuplicateQueue | null>(null);
  const [batches, setBatches] = useState<CanonicalBatchRecord[]>([]);
  const [decisions, setDecisions] = useState<CanonicalStewardshipDecision[]>([]);
  const [approvals, setApprovals] = useState<CanonicalStewardshipApproval[]>([]);
  const [admittedRelationships, setAdmittedRelationships] = useState<CanonicalAdmittedRelationship[]>([]);
  const [p1Packets, setP1Packets] = useState<CanonicalP1DecisionPacket[]>([]);
  const [remediationManifests, setRemediationManifests] = useState<Array<Record<string, unknown>>>([]);
  const [validation, setValidation] = useState<CanonicalValidationResult | null>(null);
  const [selectedGroupId, setSelectedGroupId] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [concreteOnly, setConcreteOnly] = useState(false);
  const [priorityBand, setPriorityBand] = useState('');
  const [batchName, setBatchName] = useState('P0 canonical duplicate triage');
  const [batchAction, setBatchAction] = useState('assign_reviewer');
  const [batchPreview, setBatchPreview] = useState<unknown | null>(null);
  const [approvalPreview, setApprovalPreview] = useState<unknown | null>(null);
  const [rollbackPreview, setRollbackPreview] = useState<unknown | null>(null);
  const [rollbackRationale, setRollbackRationale] = useState('Rollback preview reviewed; revert metadata-only canonical decision.');
  const [decisionType, setDecisionType] = useState<(typeof decisionTypes)[number]>('NEEDS_HUMAN_REVIEW');
  const [canonicalNodeId, setCanonicalNodeId] = useState('');
  const [reviewer, setReviewer] = useState('local-dev-reviewer');
  const [rationale, setRationale] = useState('');
  const [notes, setNotes] = useState('');
  const [highRiskAcknowledged, setHighRiskAcknowledged] = useState(false);
  const [applyDecision, setApplyDecision] = useState(false);
  const [approvalDecisionId, setApprovalDecisionId] = useState('');
  const [approvalSource, setApprovalSource] = useState('dev_admin_ui');
  const [mutationScope, setMutationScope] = useState('metadata_only');
  const [approvalRationale, setApprovalRationale] = useState('Steward reviewed the proposed P0 disambiguation; no merge, alias, redirect, or tombstone is authorized.');
  const [rollbackPlan, setRollbackPlan] = useState('Rollback removes admitted stewardship metadata/edges by decisionId and re-runs canonical validation.');
  const [riskAcknowledgment, setRiskAcknowledgment] = useState(false);
  const [preview, setPreview] = useState<CanonicalDecisionPreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const adminGateOpen = isLocalDevAdminGateOpen();
  const canApplyDirectDecision = !approvalGateDecisionTypes.has(decisionType);

  async function load() {
    setLoading(true);
    try {
      const [nextQueue, nextValidation] = await Promise.all([
        getCanonicalDuplicateGroups({ status: 'all', query, concreteOnly, priorityBand, limit: 250 }),
        getCanonicalValidation(),
      ]);
      const [nextBatches, nextDecisions, nextRemediation, nextApprovals, nextP1Packets] = await Promise.all([
        getCanonicalBatches().catch(() => ({ batches: [] })),
        getCanonicalDecisions().catch(() => ({ decisions: [] })),
        getCanonicalRemediation().catch(() => ({ remediationManifests: [] })),
        getCanonicalApprovals().catch(() => ({ approvals: [], admittedRelationships: [] })),
        getCanonicalP1DecisionPackets().catch(() => ({ packets: [], total: 0 })),
      ]);
      setQueue(nextQueue);
      setValidation(nextValidation);
      setBatches(nextBatches.batches || []);
      setDecisions(nextDecisions.decisions || []);
      setRemediationManifests(nextRemediation.remediationManifests || []);
      setApprovals(nextApprovals.approvals || []);
      setAdmittedRelationships(nextApprovals.admittedRelationships || []);
      setP1Packets(nextP1Packets.packets || []);
      setSelectedGroupId((current) => current && nextQueue.groups.some((group) => group.groupId === current)
        ? current
        : nextQueue.groups[0]?.groupId || null);
      setError(null);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to load canonical duplicate queue');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const selectedGroup = useMemo(() => queue?.groups.find((group) => group.groupId === selectedGroupId) || null, [queue, selectedGroupId]);

  useEffect(() => {
    if (!selectedGroup) return;
    setCanonicalNodeId(selectedGroup.nodes[0]?.id || '');
    setDecisionType(selectedGroup.suggestedAction as (typeof decisionTypes)[number]);
    setRationale(selectedGroup.status === 'unresolved' ? `Review ${selectedGroup.looseNormalizedLabel} duplicate group before any merge.` : '');
    setPreview(null);
    setApprovalPreview(null);
    setApprovalDecisionId(selectedGroup.existingDecisions[0]?.decisionId || '');
  }, [selectedGroup?.groupId]);

  async function previewDecision() {
    if (!selectedGroup) return;
    try {
      const response = await previewCanonicalDecision(selectedGroup.groupId, {
        decisionType,
        canonicalNodeId: canonicalNodeId || undefined,
        reviewer,
        rationale,
        notes,
        highRiskAcknowledged,
      });
      setPreview((response.preview || (response as unknown as { preview: CanonicalDecisionPreview }).preview) ?? null);
      setError(response.blockers?.length ? response.blockers.join('; ') : null);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to preview canonical decision');
    }
  }

  async function submitDecision() {
    if (!selectedGroup) return;
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await submitCanonicalDecision(selectedGroup.groupId, {
        decisionType,
        canonicalNodeId: canonicalNodeId || undefined,
        reviewer,
        rationale,
        notes,
        highRiskAcknowledged,
        apply: canApplyDirectDecision ? applyDecision : false,
        dryRun: false,
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to record canonical decision');
    }
  }

  async function createBatchFromCurrentFilter() {
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await createCanonicalBatch({
        name: batchName,
        reviewer,
        priorityBand: priorityBand || undefined,
        tags: [concreteOnly ? 'concrete' : 'canonical-review'].filter(Boolean),
        notes: 'Batch created from the current canonical review filter. Destructive merge remains blocked.',
        filters: { status: 'all', query, concreteOnly, priorityBand: priorityBand || undefined, limit: 250 },
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to create canonical review batch');
    }
  }

  async function previewFirstBatchAction() {
    const batch = batches[0];
    if (!batch) return;
    try {
      const response = await previewCanonicalBatchDecision(batch.batchId, {
        action: batchAction,
        reviewer,
        rationale: 'Dry-run batch review action; destructive canonical merges are blocked from batch mode.',
        priorityBand: priorityBand || batch.priorityBand,
        tags: ['batch-preview'],
      });
      setBatchPreview(response.preview);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to preview batch action');
    }
  }

  async function submitFirstBatchAction() {
    const batch = batches[0];
    if (!batch || !adminGateOpen) return;
    try {
      await submitCanonicalBatchDecision(batch.batchId, {
        action: batchAction,
        reviewer,
        rationale: 'Apply non-destructive batch stewardship metadata only; destructive merge remains blocked.',
        priorityBand: priorityBand || batch.priorityBand,
        tags: ['batch-applied'],
        apply: true,
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to record batch decision');
    }
  }

  async function previewApproval() {
    if (!approvalDecisionId) {
      setError('Select a proposed decision before previewing approval.');
      return;
    }
    try {
      const response = await previewCanonicalApproval(approvalDecisionId, {
        approvedBy: reviewer,
        reviewerRole: 'steward',
        approvalSource,
        mutationScope,
        approvalRationale,
        rollbackPlan,
        riskAcknowledgment,
        kimiReviewSummary: notes,
      });
      setApprovalPreview(response);
      setError(null);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to preview stewardship approval');
    }
  }

  async function approveDecision() {
    if (!approvalDecisionId) {
      setError('Select a proposed decision before approval.');
      return;
    }
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await submitCanonicalApproval(approvalDecisionId, {
        approvedBy: reviewer,
        reviewerRole: 'steward',
        approvalSource,
        mutationScope,
        approvalRationale,
        rollbackPlan,
        riskAcknowledgment,
        kimiReviewSummary: notes,
        apply: true,
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to approve canonical stewardship decision');
    }
  }

  async function generateP1Packets() {
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await generateCanonicalP1DecisionPackets({ reviewer, limit: 20, apply: true });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to generate P1 decision packets');
    }
  }

  async function previewRollback(decisionId: string) {
    try {
      setRollbackPreview(await getCanonicalRollbackPreview(decisionId));
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to preview rollback');
    }
  }

  async function rollbackDecision(decisionId: string) {
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await submitCanonicalRollback(decisionId, {
        reviewer,
        rationale: rollbackRationale,
        apply: true,
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to apply rollback');
    }
  }

  async function resolveRemediation(id: string) {
    if (!adminGateOpen) {
      setError('Local/dev admin gate is closed.');
      return;
    }
    try {
      await submitCanonicalRemediationStatus(id, {
        status: 'resolved',
        reviewer,
        resolutionNotes: 'Reviewer confirmed remediation follow-up is complete in local/dev canonical review.',
      });
      await load();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : 'Failed to update remediation status');
    }
  }

  return (
    <div className="kg-shell min-h-screen bg-bg p-6 text-text">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="inline-flex rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-[11px] uppercase tracking-[0.24em] text-amber-100">
              Local/dev canonical stewardship · dry-run first
            </div>
            <h1 className="mt-3 text-3xl font-semibold">Canonical Graph Stewardship</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-text-dim">
              Review duplicate normalized-label groups, compare node neighborhoods and Resource Layer links, and record merge, alias, keep-separate, or needs-review decisions without broad automatic cleanup.
            </p>
          </div>
          <div className="flex gap-2">
            <Link to="/" className="kg-control rounded-xl px-3 py-2 text-sm">Home</Link>
            <Link to="/dev/resource-review" className="kg-control rounded-xl px-3 py-2 text-sm">Resource Review</Link>
            <button className="kg-control rounded-xl px-3 py-2 text-sm" onClick={() => void load()}>Refresh</button>
          </div>
        </header>

        {!adminGateOpen && (
          <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-100" role="alert">
            Local/dev admin gate is closed. Duplicate groups can be inspected, but applied decisions are disabled outside localhost/dev or without VITE_ENABLE_DEV_ADMIN=true.
          </div>
        )}

        <section className="grid grid-cols-2 gap-3 md:grid-cols-5">
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Duplicate groups</div><div className="mt-1 text-2xl font-semibold">{validation?.duplicateGroups ?? queue?.total ?? 0}</div></div>
          <div className="rounded-xl border border-amber-400/30 bg-amber-400/10 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Unresolved</div><div className="mt-1 text-2xl font-semibold">{validation?.unresolvedDuplicateGroups ?? 0}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Concrete groups</div><div className="mt-1 text-2xl font-semibold">{validation?.concreteDuplicateGroups ?? 0}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">P0 unresolved</div><div className="mt-1 text-2xl font-semibold">{validation?.p0UnresolvedGroups ?? 0}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Batches</div><div className="mt-1 text-2xl font-semibold">{validation?.batchCount ?? batches.length}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Approvals</div><div className="mt-1 text-2xl font-semibold">{validation?.approvals ?? approvals.length}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Admitted edges</div><div className="mt-1 text-2xl font-semibold">{validation?.admittedRelationships ?? admittedRelationships.length}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">P1 packets</div><div className="mt-1 text-2xl font-semibold">{validation?.p1DecisionPackets ?? p1Packets.length}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">P1 signed/unsigned</div><div className="mt-1 text-2xl font-semibold">{validation?.p1PacketsSigned ?? 0}/{validation?.p1PacketsUnsigned ?? 0}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Disambiguations</div><div className="mt-1 text-2xl font-semibold">{(validation?.governedDisambiguationDecisions ?? 0) + (validation?.disambiguatedKeepSeparateDecisions ?? 0) + (validation?.crossDomainEquivalenceDecisions ?? 0)}</div></div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Remediation open</div><div className="mt-1 text-2xl font-semibold">{validation?.openRemediationManifests ?? remediationManifests.filter((entry) => entry.status === 'open' || entry.status === 'in_progress').length}</div></div>
          <div className={`rounded-xl border p-3 ${validation?.ok === false ? 'border-rose-400/30 bg-rose-400/10' : 'border-white/10 bg-white/5'}`}><div className="text-[11px] uppercase tracking-[0.18em] text-text-dim">Validation</div><div className="mt-1 text-2xl font-semibold">{validation?.ok === false ? 'Blocked' : 'OK'}</div></div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">Batch review and priority queue</h2>
              <p className="mt-1 text-xs text-text-dim">Batch workflow is non-destructive: it can assign reviewers, tags, priority, and triage state. Batch merge is blocked server-side.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {(['', 'P0', 'P1', 'P2', 'P3', 'BLOCKED'] as const).map((band) => (
                <button key={band || 'all'} className={`kg-control rounded-lg px-3 py-1.5 text-xs ${priorityBand === band ? 'border-accent text-accent' : ''}`} onClick={() => setPriorityBand(band)}>
                  {band || 'All priorities'}
                </button>
              ))}
            </div>
          </div>
          <div className="mt-3 grid gap-3 md:grid-cols-3">
            <label className="space-y-1 text-xs text-text-dim">
              Batch name
              <input className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={batchName} onChange={(event) => setBatchName(event.target.value)} />
            </label>
            <label className="space-y-1 text-xs text-text-dim">
              Batch action preview
              <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={batchAction} onChange={(event) => setBatchAction(event.target.value)}>
                <option value="assign_reviewer">assign_reviewer</option>
                <option value="set_priority">set_priority</option>
                <option value="tag_groups">tag_groups</option>
                <option value="mark_needs_review">mark_needs_review</option>
                <option value="mark_keep_separate">mark_keep_separate</option>
                <option value="reject_duplicate_candidate">reject_duplicate_candidate</option>
                <option value="MERGE_INTO_CANONICAL">MERGE_INTO_CANONICAL (blocked)</option>
              </select>
            </label>
            <div className="flex items-end gap-2">
              <button className="kg-control rounded-lg px-3 py-2 text-xs" onClick={() => void createBatchFromCurrentFilter()}>Create batch from filter</button>
              <button className="kg-control rounded-lg px-3 py-2 text-xs" onClick={() => void previewFirstBatchAction()} disabled={!batches.length}>Preview first batch</button>
              <button className="kg-control rounded-lg px-3 py-2 text-xs" onClick={() => void submitFirstBatchAction()} disabled={!batches.length || !adminGateOpen}>Record batch triage</button>
            </div>
          </div>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">
              <div className="font-medium text-text">Recent batches</div>
              {batches.length === 0 ? <div className="mt-2">No canonical review batches created yet.</div> : batches.slice(0, 3).map((batch) => (
                <div key={batch.batchId} className="mt-2 rounded-lg border border-white/10 p-2">
                  <div className="text-text">{batch.name}</div>
                  <div>{batch.stats.groupCount} groups · {batch.status} · merge blocked={String(batch.stats.destructiveActionsBlocked)}</div>
                </div>
              ))}
            </div>
            <pre className="max-h-44 overflow-auto rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">{batchPreview ? JSON.stringify(batchPreview, null, 2) : 'Batch preview appears here.'}</pre>
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">P1 decision packet generation</h2>
              <p className="mt-1 text-xs text-text-dim">Generates non-destructive packets for the top P1 duplicate groups. It does not merge, alias, redirect, or tombstone production nodes.</p>
            </div>
            <button className="kg-control rounded-lg px-3 py-2 text-xs" onClick={() => void generateP1Packets()} disabled={!adminGateOpen}>Generate top 20 P1 packets</button>
          </div>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            {p1Packets.length === 0 ? (
              <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">No P1 decision packets generated yet.</div>
            ) : p1Packets.slice(0, 6).map((packet) => (
              <article key={packet.packetId} className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="font-medium text-text">{packet.normalizedLabel}</div>
                  <div className="flex flex-wrap gap-2">
                    <Badge tone={packet.riskLevel === 'high' || packet.riskLevel === 'critical' ? 'danger' : packet.riskLevel === 'medium' ? 'warning' : 'neutral'}>{packet.riskLevel}</Badge>
                    <Badge tone={signatureTone(packet.signature?.signatureStatus)}>{packet.signature?.signatureStatus || 'unsigned'}</Badge>
                  </div>
                </div>
                <div className="mt-1">{packet.nodeIds.length} nodes · {packet.resourceLinkCount} resource links · {packet.mergeSafety}</div>
                <div className="mt-1">
                  Source lock: {packet.sourceSnapshot?.snapshotHash
                    ? `${shortHashText(packet.sourceSnapshot.snapshotHash)} · ${packet.sourceSnapshot.graphNodeCount ?? '?'} nodes/${packet.sourceSnapshot.graphEdgeCount ?? '?'} edges`
                    : 'missing'}
                </div>
                <div className="mt-1">Packet hash: {shortHashText(packet.packetContentHash)} · Group: {shortHashText(packet.groupInputHash)} · Edge neighborhood: {shortHashText(packet.candidateEdgeNeighborhoodHash)}</div>
                <div className="mt-1">
                  Signature: {packet.signature?.signatureAlgorithm || 'hmac-sha256'} · payload {shortHashText(packet.signature?.signaturePayloadHash)}
                  {packet.signature?.signedAt ? ` · signed ${packet.signature.signedAt}` : ''}
                  {packet.signature?.signatureVerificationCheckedAt ? ` · checked ${packet.signature.signatureVerificationCheckedAt}` : ''}
                </div>
                <div className="mt-1 text-[11px] text-amber-100">
                  {packet.truthCaveat || 'advisory packet only; not approval, source truth, or merge safety'}
                </div>
                <div className="mt-2">Next: {packet.nextAction}</div>
              </article>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">Decision history, rollback, and manifest integrity</h2>
              <p className="mt-1 text-xs text-text-dim">Rollback is full for metadata-only alias/triage decisions and partial/blocked for destructive merge cases. Production merge remains blocked without per-group stewardship.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge tone={(validation?.invalidManifestCount || validation?.brokenHashChainCount) ? 'danger' : 'neutral'}>{validation?.transactionManifests || 0} manifests</Badge>
              <Badge tone={(validation?.brokenHashChainCount || 0) > 0 ? 'danger' : 'neutral'}>{validation?.brokenHashChainCount || 0} chain breaks</Badge>
              <Badge tone={(validation?.invalidManifestCount || 0) > 0 ? 'danger' : 'neutral'}>{validation?.invalidManifestCount || 0} invalid</Badge>
            </div>
          </div>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">
              <div className="font-medium text-text">Recent decisions</div>
              {decisions.length === 0 ? <div className="mt-2">No canonical decisions recorded yet.</div> : decisions.slice(0, 5).map((decision) => (
                <div key={decision.decisionId} className="mt-2 rounded-lg border border-white/10 p-2">
                  <div className="text-text">{decision.decisionType} · {decision.status}</div>
                  <div className="break-all">{decision.decisionId}</div>
                  <div className="mt-2 flex flex-wrap gap-2">
                    <button className="kg-control rounded-lg px-2 py-1 text-[11px]" onClick={() => void previewRollback(decision.decisionId)}>Rollback preview</button>
                    <button className="kg-control rounded-lg px-2 py-1 text-[11px]" onClick={() => void rollbackDecision(decision.decisionId)} disabled={!adminGateOpen || decision.status === 'rolled_back'}>Apply rollback</button>
                  </div>
                </div>
              ))}
              <label className="mt-3 block space-y-1 text-xs text-text-dim">
                Rollback rationale
                <textarea className="min-h-16 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-xs text-text" value={rollbackRationale} onChange={(event) => setRollbackRationale(event.target.value)} />
              </label>
            </div>
            <pre className="max-h-64 overflow-auto rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">{rollbackPreview ? JSON.stringify(rollbackPreview, null, 2) : 'Rollback preview appears here.'}</pre>
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">Rollback remediation manifests</h2>
              <p className="mt-1 text-xs text-text-dim">Partial rollback cases must stay visible until a reviewer resolves or waives the manual restoration tasks.</p>
            </div>
            <Badge tone={(validation?.openRemediationManifests || 0) > 0 ? 'warning' : 'neutral'}>{validation?.openRemediationManifests || 0} open</Badge>
          </div>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            {remediationManifests.length === 0 ? (
              <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">No remediation manifests recorded.</div>
            ) : remediationManifests.slice(0, 4).map((manifest) => (
              <article key={String(manifest.remediationManifestId)} className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-text-dim">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="font-medium text-text">{String(manifest.rollbackCapability)} · {String(manifest.status)}</div>
                  <Badge tone={manifest.status === 'open' || manifest.status === 'in_progress' ? 'warning' : 'neutral'}>{String(manifest.status)}</Badge>
                </div>
                <div className="mt-2 break-all">{String(manifest.remediationManifestId)}</div>
                <div className="mt-1 break-all">Decision: {String(manifest.decisionId)}</div>
                <div className="mt-2">{String(manifest.reason || '')}</div>
                <button className="kg-control mt-3 rounded-lg px-2 py-1 text-[11px]" onClick={() => void resolveRemediation(String(manifest.remediationManifestId))} disabled={!adminGateOpen || manifest.status === 'resolved'}>
                  Mark resolved
                </button>
              </article>
            ))}
          </div>
        </section>

        {error && <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-100" role="alert">{error}</div>}
        {loading && <div className="rounded-2xl border border-white/10 bg-white/5 p-8 text-center text-sm text-text-dim">Loading canonical duplicate queue…</div>}

        {!loading && queue && (
          <div className="grid gap-6 lg:grid-cols-[minmax(280px,380px)_1fr]">
            <aside className="space-y-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                <label className="block text-xs text-text-dim">
                  Search labels / node IDs
                  <input className="mt-1 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={query} onChange={(event) => setQuery(event.target.value)} />
                </label>
                <label className="mt-3 flex items-center gap-2 text-xs text-text-dim">
                  <input type="checkbox" checked={concreteOnly} onChange={(event) => setConcreteOnly(event.target.checked)} />
                  Concrete quick filter
                </label>
                <button className="kg-control mt-3 rounded-lg px-3 py-1.5 text-xs" onClick={() => void load()}>Apply filters</button>
              </div>
              {queue.groups.length === 0 && <div className="rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-text-dim">No duplicate groups match the current filter.</div>}
              {queue.groups.map((group) => (
                <GroupCard key={group.groupId} group={group} selected={group.groupId === selectedGroupId} onSelect={() => setSelectedGroupId(group.groupId)} />
              ))}
            </aside>

            <main className="space-y-4">
              {!selectedGroup && <div className="rounded-2xl border border-white/10 bg-white/5 p-8 text-center text-sm text-text-dim">Select a duplicate group to review.</div>}
              {selectedGroup && (
                <>
                  <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <h2 className="text-xl font-semibold">{selectedGroup.looseNormalizedLabel}</h2>
                        <div className="mt-1 text-xs text-text-dim">{selectedGroup.groupId}</div>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <Badge tone={riskTone(selectedGroup.riskLevel)}>{selectedGroup.riskLevel}</Badge>
                        <Badge tone={selectedGroup.priorityBand === 'P0' || selectedGroup.priorityBand === 'BLOCKED' ? 'danger' : selectedGroup.priorityBand === 'P1' ? 'warning' : 'neutral'}>{selectedGroup.priorityBand}</Badge>
                        <Badge>{selectedGroup.candidateCategory}</Badge>
                        <Badge>{selectedGroup.suggestedAction}</Badge>
                      </div>
                    </div>
                    {selectedGroup.existingDecisions.length > 0 && (
                      <div className="mt-3 rounded-xl border border-amber-400/30 bg-amber-400/10 p-3 text-xs text-amber-100">
                        <div className="font-semibold">Existing stewardship status</div>
                        {selectedGroup.existingDecisions.map((decision) => (
                          <div key={decision.decisionId} className="mt-1">
                            {decision.decisionType} · {decision.status} · {(decision.proposedRelationshipAdds?.length || 0)} proposed relationship(s)
                            {decision.searchDisambiguationText ? ` · ${decision.searchDisambiguationText}` : ''}
                            {approvals.some((approval) => approval.decisionId === decision.decisionId) ? ' · approval recorded' : ' · no approval recorded'}
                          </div>
                        ))}
                      </div>
                    )}
                    <div className="mt-3 space-y-1">
                      {selectedGroup.riskReasons.map((reason) => (
                        <div key={reason} className="rounded-lg border border-amber-400/30 bg-amber-400/10 px-2 py-1 text-xs text-amber-100">{reason}</div>
                      ))}
                      {selectedGroup.priorityReasons.map((reason) => (
                        <div key={reason} className="rounded-lg border border-accent/30 bg-accent/10 px-2 py-1 text-xs text-accent">Priority: {reason}</div>
                      ))}
                    </div>
                  </section>

                  <section className="grid gap-3 md:grid-cols-2">
                    {selectedGroup.nodes.map((node) => <NodeSummary key={node.id} node={node} />)}
                  </section>

                  <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-semibold">Steward approval / admission gate</h3>
                        <p className="mt-1 text-xs text-text-dim">Approval is separate from proposal creation. It requires rationale, risk acknowledgment for high-risk groups, validation snapshot, rollback plan, and local/dev admin gate before any admitted edge is written.</p>
                      </div>
                      <Badge tone={selectedGroup.priorityBand === 'P0' ? 'danger' : 'neutral'}>{selectedGroup.priorityBand}</Badge>
                    </div>
                    <div className="mt-3 grid gap-3 md:grid-cols-2">
                      <label className="space-y-1 text-xs text-text-dim">
                        Decision to approve
                        <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={approvalDecisionId} onChange={(event) => setApprovalDecisionId(event.target.value)}>
                          <option value="">Select a recorded decision</option>
                          {selectedGroup.existingDecisions.map((decision) => <option key={decision.decisionId} value={decision.decisionId}>{decision.decisionType} · {decision.status}</option>)}
                        </select>
                      </label>
                      <label className="space-y-1 text-xs text-text-dim">
                        Mutation scope
                        <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={mutationScope} onChange={(event) => setMutationScope(event.target.value)}>
                          <option value="metadata_only">metadata_only</option>
                          <option value="non_destructive_edge_admission">non_destructive_edge_admission</option>
                          <option value="alias_only">alias_only</option>
                          <option value="redirect">redirect (guarded)</option>
                          <option value="tombstone">tombstone (guarded)</option>
                          <option value="destructive_merge">destructive_merge (blocked)</option>
                        </select>
                      </label>
                      <label className="space-y-1 text-xs text-text-dim">
                        Approval source
                        <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={approvalSource} onChange={(event) => setApprovalSource(event.target.value)}>
                          <option value="dev_admin_ui">dev_admin_ui</option>
                          <option value="api">api</option>
                          <option value="human_record">human_record</option>
                          <option value="imported_decision_record">imported_decision_record</option>
                        </select>
                      </label>
                      <label className="flex items-end gap-2 text-xs text-text-dim">
                        <input type="checkbox" checked={riskAcknowledgment} onChange={(event) => setRiskAcknowledgment(event.target.checked)} />
                        Risk acknowledged for high-risk admission
                      </label>
                    </div>
                    <label className="mt-3 block space-y-1 text-xs text-text-dim">
                      Approval rationale
                      <textarea className="min-h-16 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={approvalRationale} onChange={(event) => setApprovalRationale(event.target.value)} />
                    </label>
                    <label className="mt-3 block space-y-1 text-xs text-text-dim">
                      Rollback plan
                      <textarea className="min-h-16 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={rollbackPlan} onChange={(event) => setRollbackPlan(event.target.value)} />
                    </label>
                    <div className="mt-3 flex flex-wrap gap-2">
                      <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => void previewApproval()} disabled={!approvalDecisionId}>Preview approval</button>
                      <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => void approveDecision()} disabled={!approvalDecisionId || !adminGateOpen}>Approve/admit</button>
                    </div>
                    <pre className="mt-3 max-h-52 overflow-auto rounded-lg bg-black/30 p-3 text-xs text-text-dim">{approvalPreview ? JSON.stringify(approvalPreview, null, 2) : 'Approval preview appears here. P0 production admission remains blocked unless a real steward approval is provided.'}</pre>
                  </section>

                  <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <h3 className="text-sm font-semibold">Structured stewardship decision</h3>
                    <div className="mt-3 grid gap-3 md:grid-cols-2">
                      <label className="space-y-1 text-xs text-text-dim">
                        Decision type
                        <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={decisionType} onChange={(event) => setDecisionType(event.target.value as (typeof decisionTypes)[number])}>
                          {decisionTypes.map((type) => <option key={type} value={type}>{type}</option>)}
                        </select>
                      </label>
                      <label className="space-y-1 text-xs text-text-dim">
                        Canonical target
                        <select className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={canonicalNodeId} onChange={(event) => setCanonicalNodeId(event.target.value)}>
                          {selectedGroup.nodes.map((node) => <option key={node.id} value={node.id}>{node.label} ({node.id})</option>)}
                        </select>
                      </label>
                      <label className="space-y-1 text-xs text-text-dim">
                        Reviewer
                        <input className="w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
                      </label>
                      <label className="flex items-end gap-2 text-xs text-text-dim">
                        <input type="checkbox" checked={highRiskAcknowledged} onChange={(event) => setHighRiskAcknowledged(event.target.checked)} />
                        Explicitly acknowledge high-risk decision
                      </label>
                    </div>
                    <label className="mt-3 block space-y-1 text-xs text-text-dim">
                      Required rationale
                      <textarea className="min-h-20 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={rationale} onChange={(event) => setRationale(event.target.value)} />
                    </label>
                    <label className="mt-3 block space-y-1 text-xs text-text-dim">
                      Notes / Kimi review summary
                      <textarea className="min-h-16 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2 text-sm text-text" value={notes} onChange={(event) => setNotes(event.target.value)} />
                    </label>
                    <label className="mt-3 flex items-center gap-2 text-xs text-text-dim">
                      <input
                        type="checkbox"
                        checked={applyDecision && canApplyDirectDecision}
                        disabled={!canApplyDirectDecision}
                        onChange={(event) => setApplyDecision(event.target.checked)}
                      />
                      {canApplyDirectDecision
                        ? 'Apply decision now. Leave unchecked to record a proposed decision only. Destructive non-low-risk merges remain blocked server-side.'
                        : 'Record this decision as proposed first. Disambiguation/admission decisions must pass the steward approval gate before becoming admitted.'}
                    </label>
                    <div className="mt-3 flex flex-wrap gap-2">
                      <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => void previewDecision()}>Preview diff</button>
                      <button className="kg-control rounded-lg px-3 py-1.5 text-xs" onClick={() => void submitDecision()}>Record {applyDecision && canApplyDirectDecision ? 'applied' : 'proposed'} decision</button>
                    </div>
                  </section>

                  <PreviewPanel preview={preview} />
                </>
              )}
            </main>
          </div>
        )}
      </div>
    </div>
  );
}
