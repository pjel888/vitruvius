import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import { MemoryRouter } from 'react-router-dom';
import CanonicalReviewAdmin from './CanonicalReviewAdmin';

let dom: JSDOM;

function duplicateQueue() {
  return {
    schemaVersion: 'vitruvius-graph-canonical-stewardship/v1',
    generatedAt: '2026-05-01T00:00:00.000Z',
    total: 1,
    groups: [{
      groupId: 'dup-concrete',
      normalizedLabel: 'concrete',
      looseNormalizedLabel: 'concrete',
      labels: ['Concrete', 'concrete'],
      nodeIds: ['VTN-DOM-0000068', 'VTN-DOM-0000267'],
      nodes: [
        {
          id: 'VTN-DOM-0000068',
          label: 'Concrete',
          type: 'concept',
          aliases: [],
          taxonomyPath: ['MAT', 'CON'],
          incomingEdgeCount: 2,
          outgoingEdgeCount: 4,
          resourceLinkCount: 0,
        },
        {
          id: 'VTN-DOM-0000267',
          label: 'concrete',
          type: 'concept',
          aliases: [],
          taxonomyPath: ['STR', 'CON'],
          incomingEdgeCount: 1,
          outgoingEdgeCount: 2,
          resourceLinkCount: 0,
        },
      ],
      candidateCategory: 'manual_review_candidate',
      riskLevel: 'high',
      riskScore: 0.5,
      suggestedAction: 'NEEDS_HUMAN_REVIEW',
      riskReasons: ['different taxonomy contexts'],
      priorityBand: 'P0',
      priorityScore: 110,
      priorityReasons: ['user-mentioned concrete/reinforced concrete duplicate group'],
      edgeCount: 9,
      resourceLinkCount: 0,
      existingDecisions: [{
        decisionId: 'decision-concrete',
        decisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
        candidateGroupId: 'dup-concrete',
        sourceNodeIds: ['VTN-DOM-0000068', 'VTN-DOM-0000267'],
        affectedEdgeIds: [],
        affectedResourceLinkIds: [],
        affectedAliases: [],
        affectedSearchTerms: ['concrete'],
        reviewer: 'test',
        createdAt: '2026-05-01T00:00:00.000Z',
        rationale: 'Proposed only.',
        riskLevel: 'high',
        status: 'proposed',
        proposedRelationshipAdds: [{ relationType: 'RELATED_SPECIALIZATION_OF' }],
      }],
      status: 'unresolved',
    }],
  };
}

function validation() {
  return {
    ok: true,
    duplicateGroups: 544,
    unresolvedDuplicateGroups: 544,
    concreteDuplicateGroups: 2,
    p0UnresolvedGroups: 2,
    batchCount: 1,
    stewardshipDecisions: 0,
    appliedDecisions: 0,
    approvals: 0,
    admittedRelationships: 0,
    p1DecisionPackets: 20,
    p1PacketsSigned: 1,
    p1PacketsUnsigned: 1,
    p1PacketsInvalidSignature: 0,
    p1PacketsMissingKey: 0,
    p1PacketsStrictSignatureBlockers: 0,
    p1PacketsContentHashMismatch: 0,
    aliases: 0,
    redirects: 0,
    blockers: [],
    warnings: [],
  };
}

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost/dev/canonical-review' });
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
});

afterEach(() => {
  cleanup();
});

function renderAdmin() {
  return render(
    <MemoryRouter>
      <CanonicalReviewAdmin />
    </MemoryRouter>,
  );
}

describe.serial('CanonicalReviewAdmin', () => {
  test('renders duplicate queue, concrete quick filter, and structured decision preview', async () => {
    const calls: string[] = [];
    const fetchMock = mock((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push(`${init?.method || 'GET'} ${url}`);
      if (url.includes('/graph/canonical/validation')) {
        return Promise.resolve(new Response(JSON.stringify(validation()), { status: 200 }));
      }
      if (url.includes('/graph/canonical/decisions')) {
        return Promise.resolve(new Response(JSON.stringify({ decisions: [] }), { status: 200 }));
      }
      if (url.includes('/graph/canonical/remediation')) {
        return Promise.resolve(new Response(JSON.stringify({ remediationManifests: [] }), { status: 200 }));
      }
      if (url.includes('/graph/canonical/approvals')) {
        return Promise.resolve(new Response(JSON.stringify({ approvals: [], admittedRelationships: [] }), { status: 200 }));
      }
      if (url.includes('/graph/canonical/p1-decision-packets')) {
        return Promise.resolve(new Response(JSON.stringify({
          packets: [{
            packetId: 'packet-load-path',
            groupId: 'dup-load-path',
            normalizedLabel: 'load path',
            nodeIds: ['VTN-DOM-0002932', 'VTN-DOM-0012160'],
            resourceLinkCount: 2,
            riskLevel: 'high',
            mergeSafety: 'blocked_without_domain_review',
            packetContentHash: 'abcdef1234567890',
            groupInputHash: '123456abcdef',
            candidateEdgeNeighborhoodHash: 'fedcba654321',
            sourceSnapshot: {
              snapshotHash: '9988776655443322',
              graphNodeCount: 10018,
              graphEdgeCount: 13670,
            },
            signature: {
              signatureStatus: 'valid',
              signatureAlgorithm: 'hmac-sha256',
              signatureScope: 'p1_packet_snapshot',
              signaturePayloadHash: 'aabbccddeeff0011',
              signedAt: '2026-05-02T00:00:00.000Z',
              signatureVerificationCheckedAt: '2026-05-02T00:01:00.000Z',
            },
            truthCaveat: 'advisory_packet_only_not_steward_approval_not_canonical_admission',
            nextAction: 'Prepare steward review.',
            recommendedDecisionType: 'NEEDS_HUMAN_REVIEW',
            needsKimiReview: true,
            needsHumanDomainReview: true,
            rationale: 'High-impact duplicate needs review.',
          }],
          total: 1,
        }), { status: 200 }));
      }
      if (url.includes('/graph/canonical/batches')) {
        return Promise.resolve(new Response(JSON.stringify({
          batches: [{
            batchId: 'batch-1',
            name: 'P0 concrete stewardship',
            filters: {},
            groupIds: ['dup-concrete'],
            status: 'open',
            tags: ['concrete'],
            createdAt: '2026-05-01T00:00:00.000Z',
            updatedAt: '2026-05-01T00:00:00.000Z',
            stats: { groupCount: 1, riskCounts: { high: 1 }, priorityCounts: { P0: 1 }, candidateCategoryCounts: { manual_review_candidate: 1 }, destructiveActionsBlocked: true },
            decisions: [],
          }],
          total: 1,
        }), { status: 200 }));
      }
      if (init?.method === 'POST') {
        return Promise.resolve(new Response(JSON.stringify({
          preview: {
            dryRun: true,
            decisionType: 'NEEDS_HUMAN_REVIEW',
            candidateGroupId: 'dup-concrete',
            canonicalNodeId: 'VTN-DOM-0000068',
            sourceNodeIds: ['VTN-DOM-0000267'],
            affectedEdgeIds: ['edge-a'],
            affectedResourceLinkIds: [],
            affectedAliases: ['concrete'],
            affectedSearchTerms: ['concrete'],
            edgeRewrites: [],
            duplicateEdgeConsolidations: [],
            selfLoopRisks: [],
            resourceLinkRewrites: [],
            warnings: ['different taxonomy contexts'],
            blockers: [],
            riskLevel: 'high',
            riskScore: 0.5,
            beforeSnapshot: {},
            afterPreview: {},
          },
        }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(duplicateQueue()), { status: 200 }));
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Canonical Graph Stewardship')).toBeTruthy());
    expect(view.getAllByText('concrete').length).toBeGreaterThan(0);
    expect(view.getByText('VTN-DOM-0000068')).toBeTruthy();
    expect(view.getByLabelText('Concrete quick filter')).toBeTruthy();
    expect(view.getByText('Batch review and priority queue')).toBeTruthy();
    expect(view.getByText('Decision history, rollback, and manifest integrity')).toBeTruthy();
    expect(view.getByText('Rollback remediation manifests')).toBeTruthy();
    expect(view.getByText('P1 decision packet generation')).toBeTruthy();
    expect(view.getByText('P1 signed/unsigned')).toBeTruthy();
    expect(view.getByText('valid')).toBeTruthy();
    expect(view.getByText(/Packet hash: abcdef123456/)).toBeTruthy();
    expect(view.getByText(/Signature: hmac-sha256/)).toBeTruthy();
    expect(view.getByText('Steward approval / admission gate')).toBeTruthy();
    expect(view.getAllByText('P0').length).toBeGreaterThan(0);

    fireEvent.click(view.getByText('Preview diff'));
    await waitFor(() => expect(calls.some((call) => call.includes('POST http://localhost:3000/graph/canonical/duplicates/dup-concrete/preview'))).toBe(true));
  });

  test('renders empty and error states', async () => {
    globalThis.fetch = mock((input: RequestInfo | URL) => {
      if (String(input).includes('/graph/canonical/validation')) return Promise.resolve(new Response(JSON.stringify(validation()), { status: 200 }));
      if (String(input).includes('/graph/canonical/decisions')) return Promise.resolve(new Response(JSON.stringify({ decisions: [] }), { status: 200 }));
      if (String(input).includes('/graph/canonical/remediation')) return Promise.resolve(new Response(JSON.stringify({ remediationManifests: [] }), { status: 200 }));
      if (String(input).includes('/graph/canonical/approvals')) return Promise.resolve(new Response(JSON.stringify({ approvals: [], admittedRelationships: [] }), { status: 200 }));
      if (String(input).includes('/graph/canonical/p1-decision-packets')) return Promise.resolve(new Response(JSON.stringify({ packets: [], total: 0 }), { status: 200 }));
      if (String(input).includes('/graph/canonical/batches')) return Promise.resolve(new Response(JSON.stringify({ batches: [], total: 0 }), { status: 200 }));
      return Promise.resolve(new Response(JSON.stringify({ ...duplicateQueue(), groups: [], total: 0 }), { status: 200 }));
    }) as unknown as typeof fetch;
    const emptyView = renderAdmin();
    await waitFor(() => expect(emptyView.getByText('No duplicate groups match the current filter.')).toBeTruthy());
    cleanup();

    globalThis.fetch = mock(() => Promise.resolve(new Response(JSON.stringify({ error: { message: 'canonical queue unavailable' } }), { status: 500 }))) as unknown as typeof fetch;
    const errorView = renderAdmin();
    await waitFor(() => expect(errorView.getByRole('alert').textContent).toContain('canonical queue unavailable'));
  });
});
