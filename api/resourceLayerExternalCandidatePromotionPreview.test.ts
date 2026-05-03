import { afterAll, beforeEach, describe, expect, it } from 'bun:test';
import { readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import api from './index';
import { loadExternalCandidateRegistry } from './resourceLayer/externalCandidateRegistry';

const repoRoot = join(process.cwd(), '..');
const externalCandidateRegistryPath = join(repoRoot, '006_System-Manifests', 'resource-layer', 'external-metadata-candidates.json');
const transactionManifestsDir = join(repoRoot, '006_System-Manifests', 'resource-layer', 'transaction-manifests');

function resetExternalCandidateRegistry() {
  writeFileSync(externalCandidateRegistryPath, `${JSON.stringify({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', generatedAt: '2026-05-03T11:30:31.552Z', candidates: [] }, null, 2)}\n`);
}

function cleanTransactionManifests() {
  try {
    const files = readdirSync(transactionManifestsDir);
    for (const f of files) {
      if (f.endsWith('.json')) unlinkSync(join(transactionManifestsDir, f));
    }
  } catch { /* directory may not exist */ }
}

beforeEach(() => {
  resetExternalCandidateRegistry();
  cleanTransactionManifests();
});

afterAll(() => {
  resetExternalCandidateRegistry();
  cleanTransactionManifests();
});

async function persistCandidate(body: Record<string, unknown>) {
  const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }));
  return res.json();
}

async function applyReviewDecision(candidateId: string, body: Record<string, unknown>) {
  const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidateId}/review-decision`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }));
  return res.json();
}

describe('external candidate promotion preview', () => {
  it('promotion-preview requires local/dev/admin gate', async () => {
    const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fake/promotion-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    expect(res.status).toBeLessThan(500);
  });

  it('promotion-preview is read-only and writes no files', async () => {
    const persisted = await persistCandidate({
      title: 'Valid Test Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/valid-test',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    // Move to ready_for_promotion_review
    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const beforeRegistry = loadExternalCandidateRegistry(repoRoot);
    const beforeCount = beforeRegistry.candidates.length;

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    expect(res.status).toBe(200);

    const afterRegistry = loadExternalCandidateRegistry(repoRoot);
    expect(afterRegistry.candidates.length).toBe(beforeCount);
    expect(afterRegistry.candidates[0].status).toBe('ready_for_promotion_review');
  });

  it('promotion-preview creates no resource, no nodeResourceLink, no decision, no manifest', async () => {
    const persisted = await persistCandidate({
      title: 'Valid Test Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/valid-test',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;
    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.createsResource).toBe(false);
    expect(data.createsNodeResourceLink).toBe(false);
    expect(data.noApplyAvailable).toBe(true);
    expect(data.transactionRequiredForFutureApply).toBe(true);

    const registry = loadExternalCandidateRegistry(repoRoot);
    const candidate = registry.candidates.find((c) => c.candidateId === id);
    expect(candidate?.decisions?.length).toBe(1); // Only the review decision, no promotion decision
  });

  it('promotion-preview returns blockers for candidate status candidate/needs_review', async () => {
    const persisted = await persistCandidate({
      title: 'Valid Test Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/valid-test',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(false);
    expect(data.blockers.some((b: string) => b.includes('candidate'))).toBe(true);
    expect(data.proposedResourceDraft).toBeNull();
  });

  it('promotion-preview returns blockers for rejected/deferred/duplicate/promotion_blocked', async () => {
    const persisted = await persistCandidate({
      title: 'Valid Test Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/valid-test',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, { reviewer: 'tester', rationale: 'reject', decisionType: 'reject_candidate', rejectionReasons: ['not suitable'] });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(false);
    expect(data.blockers.some((b: string) => b.includes('rejected'))).toBe(true);
  });

  it('promotion-preview returns blockers if readiness gates fail', async () => {
    const persisted = await persistCandidate({
      title: 'No Identifier Candidate',
      resourceType: 'external_url_candidate',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    // Mark ready even though no URL/DOI/ISBN exists — the preview should still block
    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(false);
    expect(data.blockers.some((b: string) => b.includes('Source metadata gate'))).toBe(true);
  });

  it('promotion-preview returns blockers for incomplete standards context', async () => {
    const persisted = await persistCandidate({
      title: 'Standard Candidate',
      resourceType: 'standard_candidate',
      proposedUrl: 'https://example.org/standard',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(false);
    expect(data.blockers.some((b: string) => b.includes('Standards'))).toBe(true);
  });

  it('promotion-preview returns preview-only proposed resource draft for ready candidate', async () => {
    const persisted = await persistCandidate({
      title: 'Ready Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/ready',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(true);
    expect(data.proposedResourceDraft).toBeDefined();
    expect(data.proposedResourceDraft.previewOnly).toBe(true);
    expect(data.proposedResourceDraft.learnerVisible).toBe(false);
    expect(data.proposedResourceDraft.status).toBe('draft_preview');
    expect(data.proposedResourceDraft.noApplyAvailable).toBe(true);
    expect(data.proposedResourceDraft.resourceId.startsWith('res-')).toBe(true);
  });

  it('promotion-preview returns preview-only proposed node-link drafts when valid', async () => {
    const persisted = await persistCandidate({
      title: 'Linked Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/linked',
      submittedBy: 'tester',
      proposedNodeIds: ['VTN-DOM-0000001'],
      proposedRelation: 'is_primary_reference_for',
      candidateRationale: 'Relevant to node',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(true);
    expect(data.proposedNodeResourceLinkDrafts.length).toBe(1);
    expect(data.proposedNodeResourceLinkDrafts[0].previewOnly).toBe(true);
    expect(data.proposedNodeResourceLinkDrafts[0].learnerVisible).toBe(false);
    expect(data.proposedNodeResourceLinkDrafts[0].reviewStatus).toBe('preview_only');
  });

  it('promotion-preview returns blockers for invalid proposedRelation', async () => {
    const persisted = await persistCandidate({
      title: 'Bad Relation Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/bad',
      submittedBy: 'tester',
      proposedNodeIds: ['VTN-DOM-0000001'],
      proposedRelation: 'invalid_relation',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.eligibleForPromotionPreview).toBe(false);
    expect(data.blockers.some((b: string) => b.includes('proposedRelation'))).toBe(true);
  });

  it('promotion-preview performs no external verification', async () => {
    const persisted = await persistCandidate({
      title: 'No Verify Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/novalidate',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));
    const data = await res.json();
    expect(data.externalVerificationPerformed).toBe(false);
    expect(data.proposedResourceDraft?.verificationStatus).toBe('unverified');
  });

  it('GET /node/:id/resources still hides external candidates', async () => {
    const persisted = await persistCandidate({
      title: 'Hidden Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/hidden',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    // Run promotion preview
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));

    // Check learner endpoint
    const res = await api.fetch(new Request('http://localhost/node/VTN-DOM-0000001/resources?mode=learner'));
    const data = await res.json();
    const ext = data.resources?.find((r: any) => r.resourceId?.startsWith('ext-cand-'));
    expect(ext).toBeUndefined();
  });

  it('source-custody queue remains reviewer-only after promotion preview', async () => {
    const persisted = await persistCandidate({
      title: 'Reviewer Only Candidate',
      resourceType: 'external_url_candidate',
      proposedUrl: 'https://example.org/reviewer-only',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;

    await applyReviewDecision(id, {
      reviewer: 'tester',
      rationale: 'ready',
      decisionType: 'mark_ready_for_promotion_review',
    });

    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/promotion-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    }));

    const res = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const data = await res.json();
    const ext = data.groups.externalCandidates.find((c: any) => c.id === id);
    expect(ext).toBeDefined();
    expect(ext.learnerEligible).toBe(false);
    expect(ext.displayPolicy).toBe('dev_only');
  });

  it('registry is empty after test cleanup', () => {
    const registry = loadExternalCandidateRegistry(repoRoot);
    expect(registry.candidates.length).toBe(0);
  });
});
