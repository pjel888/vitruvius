import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import { MemoryRouter } from 'react-router-dom';
import ResourceReviewAdmin from './ResourceReviewAdmin';
import type { ResourceReviewQueue, SourceCustodyQueue } from '../../types';

let dom: JSDOM;

function sampleSourceCustody(): SourceCustodyQueue {
  return {
    schemaVersion: 'vitruvius-resource-layer/v1',
    generatedAt: '2026-05-01T00:00:00.000Z',
    groups: {
      learnerVisible: [
        {
          itemType: 'resource_link',
          id: 'nrl-access-board-accepted',
          title: 'U.S. Access Board Accessible Routes',
          resourceId: 'res-us-access-board-accessible-routes-ch4',
          nodeId: 'VTN-DOM-0004630',
          resourceType: 'government_guidance',
          reviewStatus: 'accepted',
          verificationStatus: 'link_verified',
          custodyStatus: 'learner_visible',
          displayPolicy: 'show_to_user',
          learnerEligible: true,
          warningFlags: [],
          nextReviewAction: 'No action needed',
        },
      ],
      reviewerOnly: [],
      needsReview: [
        {
          itemType: 'resource_link',
          id: 'nrl-fhwa-needs-review',
          title: 'FHWA Earth Retaining Structures',
          resourceId: 'res-fhwa-earth-retaining-structures',
          nodeId: 'VTN-DOM-0012799',
          resourceType: 'government_guidance',
          reviewStatus: 'needs_review',
          verificationStatus: 'link_verified',
          custodyStatus: 'needs_review',
          displayPolicy: 'dev_only',
          learnerEligible: false,
          reviewerOnlyReason: 'Link status is needs_review.',
          hiddenReason: 'Pending review before trusted use.',
          warningFlags: ['needs_review'],
          nextReviewAction: 'Review link for accept, reject, or context completion',
        },
      ],
      externalCandidates: [
        {
          itemType: 'external_candidate',
          id: 'ext-cand-asce-7',
          title: 'ASCE 7 External Candidate',
          resourceType: 'standard_candidate',
          reviewStatus: 'standards_context_in_review',
          verificationStatus: 'unverified',
          custodyStatus: 'candidate',
          displayPolicy: 'dev_only',
          learnerEligible: false,
          reviewerOnlyReason: 'External candidate is standards context in review and not reviewed.',
          hiddenReason: 'External candidates are not learner-visible until reviewed and accepted.',
          warningFlags: ['standards_context_incomplete'],
          rightsStatus: 'standard_landing_page_metadata_only',
          promotionBlocked: true,
          nextReviewAction: 'Complete standards context review',
        },
        {
          itemType: 'external_candidate',
          id: 'ext-cand-fhwa-earth-retaining',
          title: 'FHWA Earth Retaining Structures External Candidate',
          resourceType: 'external_url_candidate',
          reviewStatus: 'source_custody_in_review',
          verificationStatus: 'unverified',
          custodyStatus: 'candidate',
          displayPolicy: 'dev_only',
          learnerEligible: false,
          reviewerOnlyReason: 'External candidate is source custody in review and not reviewed.',
          hiddenReason: 'External candidates are not learner-visible until reviewed and accepted.',
          warningFlags: ['source_custody_in_review'],
          rightsStatus: 'public_government_guidance_metadata_only',
          promotionBlocked: true,
          nextReviewAction: 'Complete source custody and rights review',
        },
      ],
      candidates: [],
      localFilesIndexedOnly: [
        {
          itemType: 'local_file',
          id: 'local-md-test',
          title: 'Local Resource Layer Plan',
          localPath: '.ai/13_research/resource_layer.md',
          localFileHash: 'a'.repeat(64),
          localFileType: 'md',
          reviewStatus: 'candidate',
          custodyStatus: 'indexed_only',
          displayPolicy: 'dev_only',
          learnerEligible: false,
          reviewerOnlyReason: 'Local file is indexed but not admitted to Resource Registry.',
          hiddenReason: 'Indexed-only local files are not learner-visible.',
          warningFlags: ['local_file_indexed_only'],
          nextReviewAction: 'Review local file for admission to Resource Registry',
        },
      ],
      standardsContextIncomplete: [
        {
          itemType: 'resource_link',
          id: 'nrl-wind-load-asce-7-needs-review',
          title: 'ASCE 7: Minimum Design Loads',
          resourceId: 'res-asce-7-official-landing',
          nodeId: 'VTN-DOM-0012777',
          resourceType: 'standard',
          reviewStatus: 'needs_review',
          verificationStatus: 'link_verified',
          custodyStatus: 'standards_incomplete',
          displayPolicy: 'dev_only',
          learnerEligible: false,
          reviewerOnlyReason: 'Standard context incomplete: missing edition/version, citation/scope.',
          hiddenReason: 'Incomplete standard context without structured justification.',
          warningFlags: ['needs_review', 'standards_context_incomplete'],
          missingStandardContextFields: ['edition/version', 'citation/scope'],
          nextReviewAction: 'Supply edition, jurisdiction, and citation context or structured justification',
        },
      ],
      rightsLimited: [],
      rejected: [
        {
          itemType: 'resource_link',
          id: 'nrl-structural-column-aci-rejected',
          title: 'ACI 318 Building Code Portal',
          resourceId: 'res-aci-318-building-code-portal',
          nodeId: 'VTN-DOM-0012781',
          resourceType: 'standard',
          reviewStatus: 'rejected',
          verificationStatus: 'link_verified',
          custodyStatus: 'blocked',
          displayPolicy: 'blocked',
          learnerEligible: false,
          hiddenReason: 'Link status is rejected.',
          warningFlags: ['rejected'],
          nextReviewAction: 'Item is rejected; no further action unless reopened',
        },
      ],
      blocked: [
        {
          itemType: 'resource_link',
          id: 'nrl-structural-column-aci-rejected-2',
          title: 'ACI 318 Building Code Portal',
          resourceId: 'res-aci-318-building-code-portal',
          nodeId: 'VTN-DOM-0012781',
          resourceType: 'standard',
          reviewStatus: 'rejected',
          verificationStatus: 'link_verified',
          custodyStatus: 'blocked',
          displayPolicy: 'blocked',
          learnerEligible: false,
          hiddenReason: 'Link status is rejected.',
          warningFlags: ['rejected'],
          nextReviewAction: 'Item is rejected; no further action unless reopened',
        },
      ],
    },
    metrics: {
      total: 9,
      learnerVisible: 1,
      reviewerOnly: 0,
      needsReview: 1,
      candidates: 0,
      externalCandidates: 2,
      localFilesIndexedOnly: 1,
      standardsContextIncomplete: 1,
      rightsLimited: 0,
      rejected: 1,
      blocked: 1,
    },
  };
}

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
    acceptedLinks: [
      {
        type: 'node_resource_link',
        id: 'nrl-load-path-wbdg-wind',
        title: 'Wind Safety of the Building Envelope',
        nodeId: 'VTN-DOM-0012160',
        resourceId: 'res-wbdg-wind-safety-building-envelope',
        sourceFamilyIds: ['wbdg_nibs'],
        authorityTier: 2,
        verificationStatus: 'link_verified',
        reviewStatus: 'accepted',
        relationship: 'provides_design_guidance',
        rationale: 'Accepted metadata-only public guidance link for Load Path context.',
        reviewNotes: 'Accepted after metadata-only source custody review; no source-truth claim.',
        warnings: ['metadata_only_no_source_truth_claim'],
        resource: {
          url: 'https://www.wbdg.org/resources/wind-safety-building-envelope',
          sourceTruthCaveat: 'Official public locator metadata checked only; not source truth.',
          rightsCaveat: 'Public-web metadata only; project use still requires source-rights review.',
          lastCheckedAt: '2026-05-01T00:00:00.000Z',
        },
      },
    ],
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
  function mockFetchForQueueAndCustody() {
    return mock((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/resources/review/source-custody')) {
        return Promise.resolve(new Response(JSON.stringify(sampleSourceCustody()), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 }));
    });
  }

  test('renders queue metrics, needs_review links, candidates, local files, and rejected records', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    expect(view.getByText('Loading resource review queue…')).toBeTruthy();

    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());
    expect(view.getByText('Local/dev admin tool · file-backed registry')).toBeTruthy();

    // Default tab is Source Custody; switch to Needs Review for legacy assertions
    fireEvent.click(view.getByText('Needs Review'));
    await waitFor(() => expect(view.getByText('ASCE 7: Minimum Design Loads')).toBeTruthy());
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

  test('Accepted tab shows Resource evidence caveats without learner trust overclaim', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    fireEvent.click(view.getByText('Accepted'));
    expect(view.getByText('Wind Safety of the Building Envelope')).toBeTruthy();
    expect(view.getByText('accepted')).toBeTruthy();
    expect(view.getByText('provides_design_guidance')).toBeTruthy();
    expect(view.getByText(/Accepted metadata-only public guidance/)).toBeTruthy();
    expect(view.getByText(/Official public locator metadata checked only/)).toBeTruthy();
    expect(view.getByText(/Public-web metadata only/)).toBeTruthy();
    expect(view.getByText('Checked:')).toBeTruthy();
    expect(view.getByText('2026-05-01')).toBeTruthy();
    expect(view.queryByText(/governing/i)).toBeNull();
    expect(view.queryByText(/compliant/i)).toBeNull();
    expect(view.queryByText(/AHJ/i)).toBeNull();
  });

  test('decision action uses structured form, calls API, and refreshes queue when applied', async () => {
    const calls: string[] = [];
    const fetchMock = mock((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push(`${init?.method || 'GET'} ${url}`);
      if (init?.method === 'POST') {
        return Promise.resolve(new Response(JSON.stringify({ ok: true }), { status: 200 }));
      }
      if (url.includes('/resources/review/source-custody')) {
        return Promise.resolve(new Response(JSON.stringify(sampleSourceCustody()), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 }));
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());
    fireEvent.click(view.getByText('Needs Review'));
    await waitFor(() => expect(view.getByText('ASCE 7: Minimum Design Loads')).toBeTruthy());
    fireEvent.click(view.getAllByText('Reject').find((node) => node.tagName === 'BUTTON')!);
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
      if (url.includes('/resources/review/source-custody')) {
        return Promise.resolve(new Response(JSON.stringify(sampleSourceCustody()), { status: 200 }));
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

  test('Source Custody tab renders grouped queue with safe badges', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    // Default tab is source_custody
    expect(view.getByText('U.S. Access Board Accessible Routes')).toBeTruthy();
    // Use getAllByText for labels that appear as both metric labels and badges
    expect(view.getAllByText('Learner visible').some((el) => el.tagName === 'SPAN')).toBe(true);
    expect(view.getByText('learner eligible')).toBeTruthy();

    // ASCE 7 appears as standards incomplete
    expect(view.getByText('ASCE 7: Minimum Design Loads')).toBeTruthy();
    expect(view.getByText('Context incomplete')).toBeTruthy();
    expect(view.getAllByText('not learner visible').length).toBeGreaterThanOrEqual(1);
    expect(view.getByText('ASCE 7 External Candidate')).toBeTruthy();
    expect(view.getByText('FHWA Earth Retaining Structures External Candidate')).toBeTruthy();
    expect(view.getByText('State: Standards Context In Review')).toBeTruthy();
    expect(view.getByText('State: Source Custody In Review')).toBeTruthy();
    const unverifiedBadges = view.getAllByText('Unverified').filter((el) => el.tagName === 'SPAN');
    expect(unverifiedBadges.length).toBeGreaterThanOrEqual(2);
    expect(unverifiedBadges.every((el) => String(el.getAttribute('class')).includes('amber'))).toBe(true);
    expect(unverifiedBadges.every((el) => !String(el.getAttribute('class')).includes('emerald'))).toBe(true);
    expect(view.getAllByText('External Candidate').length).toBeGreaterThanOrEqual(2);

    // ACI 318 appears as blocked
    expect(view.getAllByText('ACI 318 Building Code Portal').length).toBeGreaterThanOrEqual(1);
    expect(view.getAllByText('Blocked').some((el) => el.tagName === 'SPAN')).toBe(true);
  });

  test('Source Custody tab shows local files as indexed-only and not admitted', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    // Local file should show indexed-only badge
    expect(view.getByText('Local Resource Layer Plan')).toBeTruthy();
    expect(view.getAllByText('Indexed only').some((el) => el.tagName === 'SPAN')).toBe(true);
    expect(view.getAllByText('not learner visible').length).toBeGreaterThanOrEqual(1);
  });

  test('Source Custody tab shows needs_review items with safe wording', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    expect(view.getByText('FHWA Earth Retaining Structures')).toBeTruthy();
    expect(view.getAllByText('Needs review').some((el) => el.tagName === 'SPAN')).toBe(true);
    expect(view.getAllByText('not learner visible').length).toBeGreaterThanOrEqual(1);
  });

  test('Source Custody metrics render in overview section', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    expect(view.getByText('Source Custody Overview')).toBeTruthy();
    expect(view.getAllByText('Learner visible').some((el) => el.tagName === 'DIV')).toBe(true);
    expect(view.getByText('External candidates')).toBeTruthy();
    // metrics.learnerVisible = 1; look for it within the custody overview section
    const overviewSection = view.getByText('Source Custody Overview').parentElement!;
    expect(overviewSection.textContent).toContain('1');
    expect(overviewSection.textContent).toContain('2');
  });

  test('External Candidates tab renders preview form with safe wording', async () => {
    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    // Switch to External Candidates tab
    const externalTab = view.getByText('External Candidates');
    expect(externalTab).toBeTruthy();
    fireEvent.click(externalTab);

    expect(view.getByText('External Metadata Candidate Preview')).toBeTruthy();
    expect(view.getByText('Preview only · No auto-verification')).toBeTruthy();
    expect(view.getByText('Does not create resources, links, or accepted candidates.')).toBeTruthy();
    expect(view.getByPlaceholderText('Resource title')).toBeTruthy();
    expect(view.getByPlaceholderText('https://…')).toBeTruthy();
    expect(view.getByPlaceholderText('10.xxxx/xxxx')).toBeTruthy();
    expect(view.getByPlaceholderText('978-…')).toBeTruthy();
  });

  test('External Candidates form has all required fields and safe labels', async () => {
    const fetchMock = mockFetchForQueueAndCustody();
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());

    fireEvent.click(view.getByText('External Candidates'));

    expect(view.getByText('External Metadata Candidate Preview')).toBeTruthy();
    expect(view.getByText('Preview only · No auto-verification')).toBeTruthy();
    expect(view.getByText('Does not create resources, links, or accepted candidates.')).toBeTruthy();
    expect(view.getByPlaceholderText('Resource title')).toBeTruthy();
    expect(view.getByPlaceholderText('https://…')).toBeTruthy();
    expect(view.getByPlaceholderText('10.xxxx/xxxx')).toBeTruthy();
    expect(view.getByPlaceholderText('978-…')).toBeTruthy();
    expect(view.getByPlaceholderText('Publisher name')).toBeTruthy();
    expect(view.getByPlaceholderText('e.g. 7th ed.')).toBeTruthy();
    expect(view.getByPlaceholderText('e.g. 2022')).toBeTruthy();
    expect(view.getByPlaceholderText('Geographic or topical scope')).toBeTruthy();
    expect(view.getByPlaceholderText('e.g. US, Philippines')).toBeTruthy();
    expect(view.getByPlaceholderText('Why should this resource be reviewed?')).toBeTruthy();
    expect(view.getByPlaceholderText('Reviewer name or identifier')).toBeTruthy();

    // Safe wording: no "verified", "official", "current", "governing", "compliant"
    const container = view.container;
    expect(container.textContent).not.toMatch(/verified|official|current|governing|compliant/i);
  });

  test('External Candidates source verification panel previews and applies reviewer-only status decisions', async () => {
    const calls: string[] = [];
    const candidate = {
      candidateId: 'ext-cand-earth-retaining-structures-test',
      title: 'Earth Retaining Structures',
      resourceType: 'external_url_candidate',
      sourceType: 'official_agency_page',
      proposedUrl: 'https://www.fhwa.dot.gov/engineering/geotech/retaining/',
      submittedAt: '2026-05-06T00:00:00.000Z',
      persistedAt: '2026-05-06T00:00:00.000Z',
      previewHash: 'preview-hash',
      verificationStatus: 'unverified',
      displayPolicy: 'reviewer_only',
      learnerVisible: false,
      reviewRequired: true,
      warningFlags: ['controlled_source_check_required'],
      missingFields: ['rightsStatus'],
      fakePlaceholderFlags: [],
      sourceTruthCaveat: 'Candidate metadata is not source truth.',
      status: 'source_custody_in_review',
      noAutoVerification: true,
      noAutoPromotion: true,
      noAutoLinking: true,
      noLearnerExposure: true,
      decisions: [],
    };
    const preview = {
      schemaVersion: 'vitruvius-source-verification-preview/v1',
      kind: 'source_verification',
      candidateId: candidate.candidateId,
      priorStatus: 'source_custody_in_review',
      proposedNextStatus: 'source_custody_in_review',
      noWrite: true,
      learnerVisible: false,
      displayPolicy: 'reviewer_only',
      verificationStatus: 'unverified',
      sourceCheck: {
        checkedAt: '2026-05-06T00:00:00.000Z',
        requestedUrl: candidate.proposedUrl,
        finalUrl: candidate.proposedUrl,
        statusCode: 200,
        ok: true,
        contentType: 'text/html; charset=utf-8',
        contentLength: 1234,
        redirectChain: [],
        title: 'Earth Retaining Structures - FHWA',
        officialSourceFamilyMatch: true,
        sourceFamily: 'fhwa',
        publicMetadataOnly: true,
        externalVerificationPerformed: true,
        contentPayloadStored: false,
        protectedContentDownloaded: false,
        verificationLimitations: ['HTTP success is not source truth.'],
        caveats: ['No Resource, nodeResourceLink, promotion, or learner exposure.'],
        blockers: [],
        warnings: ['Rights/access review remains reviewer-only.'],
      },
      missingFields: [],
      warnings: ['Rights/access review remains reviewer-only.'],
      blockers: [],
      caveats: ['No Resource, nodeResourceLink, promotion, or learner exposure.'],
      previewHash: 'source-preview-hash',
      noResourceCreated: true,
      noNodeResourceLinkCreated: true,
      noPromotion: true,
      noGraphCanonicalMutation: true,
    };
    const fetchMock = mock((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push(`${init?.method || 'GET'} ${url}`);
      if (url.includes('/resources/review/source-custody')) {
        return Promise.resolve(new Response(JSON.stringify(sampleSourceCustody()), { status: 200 }));
      }
      if (url.endsWith('/resources/review/external-candidates')) {
        return Promise.resolve(new Response(JSON.stringify({ candidates: [candidate], count: 1 }), { status: 200 }));
      }
      if (url.includes('/source-verification-preview')) {
        return Promise.resolve(new Response(JSON.stringify(preview), { status: 200 }));
      }
      if (url.includes('/source-verification-decision')) {
        return Promise.resolve(new Response(JSON.stringify({ ok: true, candidate: { ...candidate, decisions: [{ decisionId: 'decision-1' }] } }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue()), { status: 200 }));
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;

    const view = renderAdmin();
    await waitFor(() => expect(view.getByText('Resource Review Queue')).toBeTruthy());
    fireEvent.click(view.getByText('External Candidates'));
    await waitFor(() => expect(view.getByText('Persisted External Candidates (1)')).toBeTruthy());
    fireEvent.click(view.getByText('Earth Retaining Structures'));
    fireEvent.click(view.getByText('Source Verification'));
    expect(view.getByText(/HTTP success is not source truth/)).toBeTruthy();
    expect(view.getByText(/not learner trust/)).toBeTruthy();
    expect(view.getByText(/not promotion/)).toBeTruthy();
    fireEvent.change(view.getByPlaceholderText('Official public landing page URL or repo-local metadata'), {
      target: { value: candidate.proposedUrl },
    });
    fireEvent.change(view.getByPlaceholderText('What was checked, what remains untrusted, and why the next status is safe'), {
      target: { value: 'Reviewer-only FHWA public metadata check; no source truth, promotion, or learner exposure.' },
    });
    fireEvent.click(view.getByText('Preview source check'));
    await waitFor(() => expect(view.getByText('Official-source check result')).toBeTruthy());
    expect(view.getByText('Earth Retaining Structures - FHWA')).toBeTruthy();
    expect(view.getByText('Payload stored:')).toBeTruthy();
    expect(view.getByText('preview only no write')).toBeTruthy();
    expect(view.getByText('no Resource creation')).toBeTruthy();
    expect(view.getByText('no nodeResourceLink creation')).toBeTruthy();
    expect(view.getByText('no graph/canonical mutation')).toBeTruthy();
    expect(view.getByText('Mutation guard')).toBeTruthy();
    expect(view.getByText('Registry write:')).toBeTruthy();
    expect(view.getByText('Resource created:')).toBeTruthy();
    expect(view.getByText('nodeResourceLink created:')).toBeTruthy();
    expect(view.getByText('Graph/canonical changed:')).toBeTruthy();
    const applyButton = view.getByText('Apply status decision') as HTMLButtonElement;
    await waitFor(() => expect(applyButton.disabled).toBe(false));
    fireEvent.click(applyButton);
    await waitFor(() => expect(calls.some((call) => call.includes('/source-verification-decision'))).toBe(true));
    expect(calls.some((call) => call.includes('/source-verification-preview'))).toBe(true);
    expect(calls.some((call) => call.includes('/promotion-apply'))).toBe(false);
  });

  test('renders empty and error states', async () => {
    const emptyFetch = mock((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/resources/review/source-custody')) {
        return Promise.resolve(new Response(JSON.stringify({
          ...sampleSourceCustody(),
          groups: {
            ...sampleSourceCustody().groups,
            learnerVisible: [],
            reviewerOnly: [],
            needsReview: [],
            candidates: [],
            externalCandidates: [],
            localFilesIndexedOnly: [],
            standardsContextIncomplete: [],
            rightsLimited: [],
            rejected: [],
            blocked: [],
          },
          metrics: { total: 0, learnerVisible: 0, reviewerOnly: 0, needsReview: 0, candidates: 0, externalCandidates: 0, localFilesIndexedOnly: 0, standardsContextIncomplete: 0, rightsLimited: 0, rejected: 0, blocked: 0 },
        }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify(sampleQueue({
        needsReviewLinks: [],
        rejectedLinks: [],
        candidates: [],
        localFiles: [],
        standardsMissingContext: [],
      })), { status: 200 }));
    });
    globalThis.fetch = emptyFetch as unknown as typeof fetch;
    const emptyView = renderAdmin();
    await waitFor(() => expect(emptyView.getByText('Resource Review Queue')).toBeTruthy());
    // Default tab is Source Custody; check empty state for that tab
    expect(emptyView.getByText(/No Source Custody records/)).toBeTruthy();
    cleanup();

    const errorFetch = mock(() => Promise.resolve(new Response(JSON.stringify({ error: { message: 'review queue unavailable' } }), { status: 500 })));
    globalThis.fetch = errorFetch as unknown as typeof fetch;
    const errorView = renderAdmin();
    await waitFor(() => expect(errorView.getByRole('alert').textContent).toContain('review queue unavailable'));
  });
});
