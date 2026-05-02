import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import { MemoryRouter } from 'react-router-dom';
import ResourceReviewAdmin from './ResourceReviewAdmin';
import type { ResourceReviewQueue } from '../../types';

let dom: JSDOM;

function sampleQueue(overrides: Partial<ResourceReviewQueue> = {}): ResourceReviewQueue {
  return {
    schemaVersion: 'vitruvius-resource-layer/v1',
    generatedAt: '2026-05-01T00:00:00.000Z',
    needsReviewLinks: [
      {
        type: 'node_resource_link',
        id: 'nrl-wind-load-asce-7-needs-review',
        title: 'ASCE 7: Minimum Design Loads',
        nodeId: 'VTN-DOM-0012777',
        resourceId: 'res-asce-7-official-landing',
        sourceFamilyIds: ['asce'],
        authorityTier: 1,
        authorityScore: 0.95,
        verificationStatus: 'link_verified',
        reviewStatus: 'needs_review',
        relationship: 'is_supplementary_reference_for',
        rationale: 'Needs edition and section context before acceptance.',
        reviewNotes: 'Kimi advised needs_review.',
        missingStandardContext: true,
        warnings: ['Missing edition/version plus page/chapter/section context.'],
      },
    ],
    rejectedLinks: [
      {
        type: 'node_resource_link',
        id: 'nrl-structural-column-aci-rejected',
        title: 'ACI 318 Building Code Portal',
        nodeId: 'VTN-DOM-0012781',
        resourceId: 'res-aci-318-building-code-portal',
        sourceFamilyIds: ['aci'],
        authorityTier: 1,
        verificationStatus: 'link_verified',
        reviewStatus: 'rejected',
        relationship: 'provides_design_guidance',
        rationale: 'Too broad for structural column.',
        reviewNotes: 'Preserve rejection rationale.',
        warnings: [],
      },
    ],
    acceptedLinks: [],
    candidateLinks: [],
    candidates: [
      {
        type: 'candidate',
        id: 'cand-asce-7-wind-load',
        title: 'ASCE 7 Candidate',
        nodeId: 'VTN-DOM-0012777',
        rawUrl: 'https://www.asce.org/asce-7',
        rawIdentifier: 'res-asce-7-official-landing',
        preliminaryScore: 0.82,
        rankingScore: 0.82,
        reviewStatus: 'needs_review',
        dedupeKey: 'url:https://asce.org/asce-7',
        sourceFamilyIds: ['asce'],
        authorityTier: 1,
        warnings: ['Candidate appears related to existing resource res-asce-7-official-landing.'],
      },
    ],
    localFiles: [
      {
        type: 'local_file',
        id: 'local-md-test',
        fileId: 'local-md-test',
        title: 'Local Resource Layer Plan',
        localPath: '.ai/13_research/resource_layer.md',
        localFileHash: 'a'.repeat(64),
        localFileType: 'md',
        linkedNodeCount: 0,
        admitted: false,
        reviewStatus: 'candidate',
        sourceFamilyIds: [],
        authorityTier: 4,
        warnings: ['Indexed local file is not admitted to the Resource Registry.'],
      },
    ],
    standardsMissingContext: [
      {
        type: 'node_resource_link',
        id: 'nrl-wind-load-asce-7-needs-review',
        title: 'ASCE 7: Minimum Design Loads',
        nodeId: 'VTN-DOM-0012777',
        resourceId: 'res-asce-7-official-landing',
        sourceFamilyIds: ['asce'],
        authorityTier: 1,
        authorityScore: 0.95,
        verificationStatus: 'link_verified',
        reviewStatus: 'needs_review',
        relationship: 'is_supplementary_reference_for',
        rationale: 'Needs edition and section context before acceptance.',
        reviewNotes: 'Kimi advised needs_review.',
        missingStandardContext: true,
        missingStandardContextFields: ['edition/version', 'citation/scope'],
        standardContextStatus: 'needs_human_review',
        promotionBlocked: true,
        promotionBlockerReasons: ['Promotion blocked until standards context is complete or explicitly reviewer/source justified: missing edition/version, citation/scope.'],
        organization: 'American Society of Civil Engineers',
        resourceType: 'standard',
        currentJurisdiction: 'US model standard; adopted by reference by jurisdiction and edition.',
        currentGeographicScope: 'us',
        warnings: ['Missing standards context: edition/version, citation/scope.'],
        resource: { url: 'https://www.asce.org/asce-7' },
      },
      {
        type: 'node_resource_link',
        id: 'nrl-structural-column-aci-rejected',
        title: 'ACI 318 Building Code Portal',
        nodeId: 'VTN-DOM-0012781',
        resourceId: 'res-aci-318-building-code-portal',
        sourceFamilyIds: ['aci'],
        authorityTier: 1,
        verificationStatus: 'link_verified',
        reviewStatus: 'rejected',
        relationship: 'provides_design_guidance',
        rationale: 'Too broad for structural column.',
        reviewNotes: 'Preserve rejection rationale.',
        missingStandardContext: true,
        missingStandardContextFields: ['edition/version', 'citation/scope'],
        standardContextStatus: 'needs_human_review',
        promotionBlocked: true,
        promotionBlockerReasons: ['Promotion blocked until standards context is complete or explicitly reviewer/source justified: missing edition/version, citation/scope.'],
        organization: 'American Concrete Institute',
        resourceType: 'standard',
        warnings: ['Missing standards context: edition/version, citation/scope.'],
      },
    ],
    validationWarnings: [],
    validationErrors: [],
    validationBlockers: [],
    metrics: {
      acceptedResources: 7,
      acceptedLinks: 5,
      needsReviewLinks: 3,
      rejectedLinks: 1,
      candidateLinks: 0,
      candidates: 4,
      localFilesIndexed: 25,
      localFilesAdmitted: 0,
      standardsMissingContext: 2,
      standardsMissingEdition: 2,
      standardsMissingScope: 3,
      standardsPromotionBlocked: 3,
      duplicateWarnings: 0,
      brokenLinkWarnings: 0,
      reviewDecisions: 0,
    },
    ...overrides,
  };
}

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost/dev/resource-review' });
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
      <ResourceReviewAdmin />
    </MemoryRouter>,
  );
}

describe('ResourceReviewAdmin', () => {
  test('renders queue metrics, needs_review links, candidates, local files, and rejected records', async () => {
    const fetchMock = mock(() => Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 })));
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    expect(view.getByText('Loading resource review queue…')).toBeTruthy();

    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());
    expect(view.getByText('Local/dev admin tool · file-backed registry')).toBeTruthy();
    expect(view.getByText('ASCE 7: Minimum Design Loads')).toBeTruthy();
    expect(view.getByText('missing edition/section')).toBeTruthy();
    expect(view.getByText('25')).toBeTruthy();

    fireEvent.click(view.getAllByText('Candidates').find((node) => node.tagName === 'BUTTON')!);
    expect(view.getByText('ASCE 7 Candidate')).toBeTruthy();

    fireEvent.click(view.getByText('Local Files'));
    expect(view.getByText('Local Resource Layer Plan')).toBeTruthy();
    expect(view.getByText('not admitted')).toBeTruthy();

    fireEvent.click(view.getAllByText('Rejected').find((node) => node.tagName === 'BUTTON')!);
    expect(view.getByText('ACI 318 Building Code Portal')).toBeTruthy();
    expect(view.getByText(/Preserve rejection rationale/)).toBeTruthy();
  });

  test('decision action uses structured form, calls API, and refreshes queue when applied', async () => {
    const calls: string[] = [];
    const fetchMock = mock((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push(`${init?.method || 'GET'} ${url}`);
      if (init?.method === 'POST') {
        return Promise.resolve(new Response(JSON.stringify({ ok: true }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 }));
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('ASCE 7: Minimum Design Loads')).toBeTruthy());
    fireEvent.click(view.getByText('Reject'));
    expect(view.getByText('Structured review decision')).toBeTruthy();
    fireEvent.click(view.getByLabelText('Submit as dry-run preview'));
    fireEvent.click(view.getByText('Submit decision'));

    await waitFor(() => expect(calls.some((call) => call.includes('POST http://localhost:3000/resources/review/link/nrl-wind-load-asce-7-needs-review/decision'))).toBe(true));
    expect(calls.filter((call) => call.startsWith('GET ')).length).toBeGreaterThanOrEqual(2);
  });

  test('standards tab renders context workflow, preview diff, and disabled unsafe apply when gate is closed', async () => {
    dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'https://review.example.com/dev/resource-review' });
    globalThis.window = dom.window as typeof globalThis.window;
    globalThis.document = dom.window.document;
    globalThis.HTMLElement = dom.window.HTMLElement;
    globalThis.Node = dom.window.Node;
    globalThis.navigator = dom.window.navigator as Navigator;

    const calls: string[] = [];
    const fetchMock = mock((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push(`${init?.method || 'GET'} ${url}`);
      if (url.includes('/context-preview')) {
        return Promise.resolve(new Response(JSON.stringify({
          schemaVersion: 'vitruvius-resource-layer/v1',
          generatedAt: '2026-05-01T00:00:00.000Z',
          id: 'nrl-wind-load-asce-7-needs-review',
          resourceId: 'res-asce-7-official-landing',
          diff: { missingFieldsAfter: ['edition/version', 'citation/scope'] },
          validationImpact: { ok: true },
        }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 }));
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());
    fireEvent.click(view.getByText('Standards Missing Context'));
    expect(view.getAllByText('Structured standards context form').length).toBeGreaterThan(0);
    expect(view.getAllByText(/Do not guess edition\/version/).length).toBeGreaterThan(0);
    expect(view.getAllByText('promotion blocked').length).toBeGreaterThan(0);
    const applyButton = view.getAllByText('Apply context decision')[0] as HTMLButtonElement;
    expect(applyButton.disabled).toBe(true);
    fireEvent.click(view.getAllByText('Preview context diff')[0]);
    await waitFor(() => expect(calls.some((call) => call.includes('/resources/review/standards/nrl-wind-load-asce-7-needs-review/context-preview'))).toBe(true));
    expect(view.getByLabelText('Standards context diff preview')).toBeTruthy();
  });

  test('renders empty and error states', async () => {
    const emptyFetch = mock(() => Promise.resolve(new Response(JSON.stringify(sampleQueue({
      needsReviewLinks: [],
      rejectedLinks: [],
      candidates: [],
      localFiles: [],
      standardsMissingContext: [],
    })), { status: 200 })));
    globalThis.fetch = emptyFetch as unknown as typeof fetch;
    const emptyView = renderAdmin();
    await waitFor(() => expect(emptyView.getByText('No Needs Review records are currently in the review queue.')).toBeTruthy());
    cleanup();

    const errorFetch = mock(() => Promise.resolve(new Response(JSON.stringify({ error: { message: 'review queue unavailable' } }), { status: 500 })));
    globalThis.fetch = errorFetch as unknown as typeof fetch;
    const errorView = renderAdmin();
    await waitFor(() => expect(errorView.getByRole('alert').textContent).toContain('review queue unavailable'));
  });
});
