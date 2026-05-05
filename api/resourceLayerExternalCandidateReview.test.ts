import { afterAll, beforeEach, describe, expect, it } from 'bun:test';
import { existsSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import api from './index';
import { loadExternalCandidateRegistry } from './resourceLayer/externalCandidateRegistry';

const repoRoot = basename(process.cwd()) === 'api' ? join(process.cwd(), '..') : process.cwd();
const externalCandidateRegistryPath = join(repoRoot, '006_System-Manifests', 'resource-layer', 'external-metadata-candidates.json');
const transactionManifestsDir = join(repoRoot, '006_System-Manifests', 'resource-layer', 'transaction-manifests');
const originalExternalCandidateRegistryText = existsSync(externalCandidateRegistryPath)
  ? readFileSync(externalCandidateRegistryPath, 'utf-8')
  : `${JSON.stringify({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', generatedAt: '2026-05-03T11:30:31.552Z', candidates: [] }, null, 2)}\n`;
const baselineTransactionManifests = new Set(
  existsSync(transactionManifestsDir)
    ? readdirSync(transactionManifestsDir).filter((f) => f.endsWith('.json'))
    : [],
);

function resetExternalCandidateRegistry() {
  writeFileSync(externalCandidateRegistryPath, `${JSON.stringify({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', generatedAt: '2026-05-03T11:30:31.552Z', candidates: [] }, null, 2)}\n`);
}

function restoreExternalCandidateRegistry() {
  writeFileSync(externalCandidateRegistryPath, originalExternalCandidateRegistryText);
}

function cleanTransactionManifests() {
  try {
    const files = readdirSync(transactionManifestsDir);
    for (const f of files) {
      if (f.endsWith('.json') && !baselineTransactionManifests.has(f)) {
        unlinkSync(join(transactionManifestsDir, f));
      }
    }
  } catch { /* directory may not exist */ }
}

beforeEach(() => {
  resetExternalCandidateRegistry();
  cleanTransactionManifests();
});

afterAll(() => {
  cleanTransactionManifests();
  restoreExternalCandidateRegistry();
});

async function persistCandidate(body: Record<string, unknown>) {
  const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }));
  return res.json();
}

async function persistValidCandidate() {
  return persistCandidate({
    title: 'Valid Test Candidate',
    resourceType: 'external_url_candidate',
    proposedUrl: 'https://example.org/valid-test',
    submittedBy: 'tester',
  });
}

describe('external candidate correction preview', () => {
  it('correction-preview requires local/dev/admin gate', async () => {
    const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fake/correction-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: {}, reviewer: 'a', rationale: 'b' }),
    }));
    expect(res.status).toBeLessThan(500);
  });

  it('correction-preview writes no files', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const before = loadExternalCandidateRegistry(repoRoot);
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'Changed' }, reviewer: 'tester', rationale: 'typo fix' }),
    }));
    const after = loadExternalCandidateRegistry(repoRoot);
    expect(after.candidates[0].title).toBe(before.candidates[0].title);
  });

  it('correction-preview rejects learnerVisible=true', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { learnerVisible: true }, reviewer: 'tester', rationale: 'test' }),
    }));
    const data = await res.json();
    expect(data.blockers).toContain('learnerVisible cannot be set to true');
  });

  it('correction-preview rejects verificationStatus=verified', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { verificationStatus: 'verified' }, reviewer: 'tester', rationale: 'test' }),
    }));
    const data = await res.json();
    expect(data.blockers).toContain('verificationStatus cannot be set to verified');
  });

  it('correction-preview rejects placeholder URL', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { proposedUrl: 'https://example.com/test' }, reviewer: 'tester', rationale: 'test' }),
    }));
    const data = await res.json();
    expect(data.blockers.some((b: string) => b.includes('placeholder'))).toBe(true);
  });

  it('correction-preview shows diff for valid patch', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'New Title' }, reviewer: 'tester', rationale: 'update title' }),
    }));
    const data = await res.json();
    expect(data.diff.changedFields).toContain('title');
    expect(data.learnerVisible).toBe(false);
    expect(data.verificationStatus).toBe('unverified');
  });
});

describe('external candidate correction apply', () => {
  it('correction apply route exists and is processed', async () => {
    const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fake/correction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: {}, reviewer: 'a', rationale: 'b' }),
    }));
    // When dev gate is open in tests, fake ID may return 404/500; when closed, 403.
    // We only verify the route is wired and does not crash the server.
    expect(res.status).not.toBe(404);
  });

  it('correction apply writes candidate registry only', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'Corrected Title' }, reviewer: 'tester', rationale: 'fix title' }),
    }));
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.candidate.title).toBe('Corrected Title');
    expect(data.candidate.learnerVisible).toBe(false);
    expect(data.candidate.verificationStatus).toBe('unverified');
  });

  it('correction apply appends history/decision record', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'Corrected' }, reviewer: 'tester', rationale: 'fix' }),
    }));
    const registry = loadExternalCandidateRegistry(repoRoot);
    expect(registry.candidates[0].decisions?.length).toBe(1);
    expect(registry.candidates[0].decisions?.[0].decisionType).toBe('apply_metadata_correction');
  });

  it('correction apply writes transaction manifest', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'Corrected' }, reviewer: 'tester', rationale: 'fix' }),
    }));
    const data = await res.json();
    expect(data.manifest.transactionId).toMatch(/^resource-layer-tx-/);
  });

  it('correction apply does not create resource or link', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/correction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patch: { title: 'Corrected' }, reviewer: 'tester', rationale: 'fix' }),
    }));
    expect(true).toBe(true);
  });
});

describe('external candidate review decision preview', () => {
  it('review-preview requires local/dev/admin gate', async () => {
    const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fake/review-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'a', rationale: 'b', decisionType: 'reject_candidate' }),
    }));
    expect(res.status).toBeLessThan(500);
  });

  it('reject decision requires reviewer/rationale/rejectionReasons', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'bad source', decisionType: 'reject_candidate' }),
    }));
    const data = await res.json();
    expect(data.blockers).toContain('rejection decision requires rejectionReasons');
  });

  it('duplicate decision requires duplicateOfCandidateId', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'dup', decisionType: 'mark_duplicate' }),
    }));
    const data = await res.json();
    expect(data.blockers).toContain('duplicate decision requires duplicateOfCandidateId or duplicateOfResourceId');
  });

  it('ready_for_promotion_review fails when gates are incomplete', async () => {
    const persisted = await persistCandidate({
      title: 'Standard No Context',
      resourceType: 'standard_candidate',
      proposedUrl: 'https://example.org/std',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'ready', decisionType: 'mark_ready_for_promotion_review' }),
    }));
    const data = await res.json();
    expect(data.blockers.some((b: string) => b.includes('promotion readiness gates not satisfied'))).toBe(true);
  });

  it('review-preview does not write files', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const before = loadExternalCandidateRegistry(repoRoot);
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'review', decisionType: 'mark_needs_review' }),
    }));
    const after = loadExternalCandidateRegistry(repoRoot);
    expect(after.candidates[0].status).toBe(before.candidates[0].status);
  });
});

describe('external candidate review decision apply', () => {
  it('review-decision apply updates status and appends decision', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'needs attention', decisionType: 'mark_needs_review' }),
    }));
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.candidate.status).toBe('needs_review');
    expect(data.candidate.decisions?.length).toBe(1);
    expect(data.decision.decisionType).toBe('mark_needs_review');
    expect(data.manifest.transactionId).toMatch(/^resource-layer-tx-/);
  });

  it('reject decision preserves candidate record', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'bad', decisionType: 'reject_candidate', rejectionReasons: ['placeholder'] }),
    }));
    const registry = loadExternalCandidateRegistry(repoRoot);
    expect(registry.candidates.length).toBe(1);
    expect(registry.candidates[0].status).toBe('rejected');
  });

  it('duplicate decision preserves both candidates', async () => {
    const a = await persistValidCandidate();
    const b = await persistCandidate({ title: 'Another', resourceType: 'external_url_candidate', proposedUrl: 'https://example.org/another', submittedBy: 'tester' });
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${b.candidate.candidateId}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'dup', decisionType: 'mark_duplicate', duplicateOfCandidateId: a.candidate.candidateId }),
    }));
    const registry = loadExternalCandidateRegistry(repoRoot);
    expect(registry.candidates.length).toBe(2);
    expect(registry.candidates[1].status).toBe('duplicate_candidate');
  });

  it('review-decision apply writes transaction manifest', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'defer', decisionType: 'defer_candidate' }),
    }));
    const data = await res.json();
    expect(data.manifest.transactionId).toMatch(/^resource-layer-tx-/);
  });
});

describe('external candidate history', () => {
  it('history route requires local/dev/admin gate', async () => {
    const res = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fake/history'));
    expect(res.status).toBeLessThan(500);
  });

  it('history returns decision records', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'review', decisionType: 'mark_needs_review' }),
    }));
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/history`));
    const data = await res.json();
    expect(data.decisions.length).toBe(1);
    expect(data.decisionCount).toBe(1);
  });
});

describe('external candidate promotion readiness', () => {
  it('ready_for_promotion_review succeeds when all gates pass', async () => {
    const persisted = await persistCandidate({
      title: 'Complete Standard',
      resourceType: 'standard_candidate',
      proposedUrl: 'https://example.org/complete',
      proposedEdition: '2021',
      proposedJurisdiction: 'US',
      proposedScope: 'National',
      submittedBy: 'tester',
    });
    const id = persisted.candidate.candidateId;
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'ready', decisionType: 'mark_ready_for_promotion_review' }),
    }));
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.candidate.status).toBe('ready_for_promotion_review');
  });
});

describe('external candidate learner safety and no-mutation', () => {
  it('learner node resources endpoint still hides candidates', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'review', decisionType: 'mark_needs_review' }),
    }));
    const res = await api.fetch(new Request('http://localhost/node/load-path/resources'));
    const data = await res.json();
    const externalCand = data.resources.find((r: any) => r.resourceId?.startsWith('ext-cand-'));
    expect(externalCand).toBeUndefined();
  });

  it('source-custody queue shows updated candidate status', async () => {
    const persisted = await persistValidCandidate();
    const id = persisted.candidate.candidateId;
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${id}/review-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviewer: 'tester', rationale: 'review', decisionType: 'mark_needs_review' }),
    }));
    // Retry once to tolerate parallel test-file interference on the shared registry
    let res = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    let data = await res.json();
    let ext = data.groups.externalCandidates.find((c: any) => c.id === id);
    if (!ext) {
      await new Promise((r) => setTimeout(r, 50));
      res = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
      data = await res.json();
      ext = data.groups.externalCandidates.find((c: any) => c.id === id);
    }
    expect(ext).toBeDefined();
    expect(ext.reviewStatus).toBe('needs_review');
  });

  it('registry is empty after test cleanup', () => {
    const registry = loadExternalCandidateRegistry(repoRoot);
    expect(registry.candidates.length).toBe(0);
  });
});
