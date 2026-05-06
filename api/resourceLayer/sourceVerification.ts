import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import type { ExternalMetadataCandidateRecord } from './externalCandidateRegistry';
import {
  loadExternalCandidateRegistry,
  saveRegistry as saveExternalCandidateRegistry,
} from './externalCandidateRegistry';
import { detectExternalMetadataPlaceholders } from './externalMetadataCandidates';
import { withResourceLayerTransaction } from './transactionManifest';

export type SourceVerificationKind = 'source_verification' | 'standards_context_verification';

export type SourceVerificationNextStatus =
  | 'source_custody_review_needed'
  | 'source_custody_in_review'
  | 'source_custody_verified'
  | 'rights_review_needed'
  | 'source_custody_rejected'
  | 'standards_context_needed'
  | 'standards_context_in_review'
  | 'standards_context_complete'
  | 'standards_context_rejected';

export interface ControlledSourceCheckOptions {
  fetchImpl?: typeof fetch;
  now?: () => string;
  timeoutMs?: number;
  maxRedirects?: number;
  maxBodyBytes?: number;
  requestedUrl?: string;
}

export type ControlledSourceFamily =
  | 'asce'
  | 'fhwa'
  | 'buildingsmart'
  | 'aisc'
  | 'aia'
  | 'us_access_board'
  | 'wbdg_nibs'
  | 'istructe'
  | 'ice'
  | 'riba'
  | 'uniclass_nbs'
  | 'omniclass_csi'
  | 'unknown';

export interface ControlledSourceCheckResult {
  checkedAt: string;
  requestedUrl: string;
  finalUrl?: string;
  statusCode?: number;
  ok: boolean;
  contentType?: string;
  contentLength?: number;
  redirectChain: string[];
  title?: string;
  officialSourceFamilyMatch: boolean;
  sourceFamily: ControlledSourceFamily;
  publicMetadataOnly: true;
  externalVerificationPerformed: boolean;
  contentPayloadStored: false;
  protectedContentDownloaded: false;
  verificationLimitations: string[];
  caveats: string[];
  blockers: string[];
  warnings: string[];
}

export interface StandardsContextInput {
  standardTitle?: string;
  edition?: string;
  version?: string;
  publicationYear?: string | number;
  scope?: string;
  jurisdictionApplicabilityCaveat?: string;
}

export interface SourceVerificationDecisionInput {
  reviewer: string;
  rationale: string;
  sourceOfContext: string;
  requestedUrl?: string;
  nextStatus?: SourceVerificationNextStatus;
  decisionType?: string;
  previewHash?: string;
  rightsStatus?: string;
  accessType?: string;
  rightsAssessmentRationale?: string;
  standardsContext?: StandardsContextInput;
}

export interface SourceVerificationPreview {
  schemaVersion: 'vitruvius-source-verification-preview/v1';
  kind: SourceVerificationKind;
  candidateId: string;
  priorStatus: string;
  proposedNextStatus: SourceVerificationNextStatus | string;
  noWrite: true;
  learnerVisible: false;
  displayPolicy: 'reviewer_only' | 'dev_only';
  verificationStatus: 'unverified';
  sourceCheck: ControlledSourceCheckResult;
  missingFields: string[];
  warnings: string[];
  blockers: string[];
  caveats: string[];
  previewHash: string;
  noResourceCreated: true;
  noNodeResourceLinkCreated: true;
  noPromotion: true;
  noGraphCanonicalMutation: true;
}

export interface SourceVerificationApplyResult {
  ok: true;
  candidate: ExternalMetadataCandidateRecord;
  decision: Record<string, unknown>;
  preview: SourceVerificationPreview;
  manifest: { transactionId: string };
  rollbackPlan: {
    action: 'restore_prior_status_append_rollback_decision';
    candidateId: string;
    priorStatus: string;
    nextStatus: string;
    auditHistoryPreserved: true;
  };
  noResourceCreated: true;
  noNodeResourceLinkCreated: true;
  noPromotion: true;
  learnerVisible: false;
  externalVerificationPerformed: boolean;
}

const DEFAULT_TIMEOUT_MS = 10_000;
const DEFAULT_MAX_REDIRECTS = 5;
const DEFAULT_MAX_BODY_BYTES = 1_048_576;
const FORBIDDEN_PLACEHOLDER_VALUE = /^(latest|current|tbd|to be determined|unknown|n\/a|na|sample|assumed|placeholder)$/i;
const UNSUPPORTED_TRUST_CLAIM = /\b(current|governing|compliant|compliance|ahj|adopted|accepted by|officially approved)\b/i;

function nowIso(options?: ControlledSourceCheckOptions): string {
  return options?.now?.() || new Date().toISOString();
}

function stableStringify(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value as Record<string, unknown>).sort().map((key) => (
      `${JSON.stringify(key)}:${stableStringify((value as Record<string, unknown>)[key])}`
    )).join(',')}}`;
  }
  return JSON.stringify(value);
}

function hashPreview(input: Omit<SourceVerificationPreview, 'previewHash'>): string {
  return createHash('sha256').update(stableStringify(input)).digest('hex');
}

function externalCandidateRegistryPath(repoRoot: string): string {
  return resolve(repoRoot, '006_System-Manifests', 'resource-layer', 'external-metadata-candidates.json');
}

function safeContentLength(value: string | null): number | undefined {
  if (!value) return undefined;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : undefined;
}

function normalizeHost(url: string): string {
  return new URL(url).hostname.toLowerCase().replace(/^www\./, '');
}

function isOfficialHostForFamily(host: string, sourceFamily: ControlledSourceCheckResult['sourceFamily']): boolean {
  if (sourceFamily === 'asce') {
    return host === 'asce.org' || host.endsWith('.asce.org') || host === 'ascelibrary.org' || host.endsWith('.ascelibrary.org');
  }
  if (sourceFamily === 'fhwa') {
    return host === 'fhwa.dot.gov' || host.endsWith('.fhwa.dot.gov') || host === 'highways.dot.gov' || host.endsWith('.highways.dot.gov');
  }
  if (sourceFamily === 'buildingsmart') {
    return host === 'buildingsmart.org' || host.endsWith('.buildingsmart.org');
  }
  if (sourceFamily === 'aisc') {
    return host === 'aisc.org' || host.endsWith('.aisc.org');
  }
  if (sourceFamily === 'aia') {
    return host === 'aia.org' || host.endsWith('.aia.org');
  }
  if (sourceFamily === 'us_access_board') {
    return host === 'access-board.gov' || host.endsWith('.access-board.gov');
  }
  if (sourceFamily === 'wbdg_nibs') {
    return host === 'wbdg.org' || host.endsWith('.wbdg.org') || host === 'nibs.org' || host.endsWith('.nibs.org');
  }
  if (sourceFamily === 'istructe') {
    return host === 'istructe.org' || host.endsWith('.istructe.org');
  }
  if (sourceFamily === 'ice') {
    return host === 'ice.org.uk' || host.endsWith('.ice.org.uk') || host === 'knowledgehub.ice.org.uk' || host.endsWith('.knowledgehub.ice.org.uk');
  }
  if (sourceFamily === 'riba') {
    return host === 'architecture.com' || host.endsWith('.architecture.com') || host === 'riba.org' || host.endsWith('.riba.org');
  }
  if (sourceFamily === 'uniclass_nbs') {
    return host === 'thenbs.com' || host.endsWith('.thenbs.com') || host === 'uniclass.thenbs.com' || host.endsWith('.uniclass.thenbs.com');
  }
  if (sourceFamily === 'omniclass_csi') {
    return host === 'csiresources.org' || host.endsWith('.csiresources.org') || host === 'csinet.org' || host.endsWith('.csinet.org');
  }
  return false;
}

export function officialSourceFamilyForCandidate(candidate: ExternalMetadataCandidateRecord): ControlledSourceCheckResult['sourceFamily'] {
  const family = `${candidate.proposedSourceFamilyId || ''}`.toLowerCase();
  const publisher = `${candidate.proposedPublisher || ''}`.toLowerCase();
  const title = `${candidate.title || ''}`.toLowerCase();
  const proposedHost = candidate.proposedUrl ? normalizeHost(candidate.proposedUrl) : '';
  if (family.includes('asce') || publisher.includes('asce') || title.includes('asce 7')) return 'asce';
  if (
    family.includes('fhwa') ||
    publisher.includes('fhwa') ||
    proposedHost === 'fhwa.dot.gov' ||
    proposedHost.endsWith('.fhwa.dot.gov') ||
    proposedHost === 'highways.dot.gov' ||
    proposedHost.endsWith('.highways.dot.gov')
  ) {
    return 'fhwa';
  }
  if (
    family === 'buildingsmart' ||
    publisher.includes('buildingsmart') ||
    title.includes('buildingsmart') ||
    proposedHost === 'buildingsmart.org' ||
    proposedHost.endsWith('.buildingsmart.org')
  ) {
    return 'buildingsmart';
  }
  if (
    family === 'aisc' ||
    publisher.includes('american institute of steel construction') ||
    title.includes('american institute of steel construction') ||
    proposedHost === 'aisc.org' ||
    proposedHost.endsWith('.aisc.org')
  ) {
    return 'aisc';
  }
  if (
    family === 'aia' ||
    publisher.includes('american institute of architects') ||
    title.includes('american institute of architects') ||
    proposedHost === 'aia.org' ||
    proposedHost.endsWith('.aia.org')
  ) {
    return 'aia';
  }
  if (
    family === 'us_access_board' ||
    publisher.includes('u.s. access board') ||
    publisher.includes('us access board') ||
    title.includes('u.s. access board') ||
    title.includes('us access board') ||
    proposedHost === 'access-board.gov' ||
    proposedHost.endsWith('.access-board.gov')
  ) {
    return 'us_access_board';
  }
  if (
    family === 'wbdg_nibs' ||
    publisher.includes('whole building design guide') ||
    publisher.includes('national institute of building sciences') ||
    title.includes('whole building design guide') ||
    title.includes('nibs') ||
    proposedHost === 'wbdg.org' ||
    proposedHost.endsWith('.wbdg.org') ||
    proposedHost === 'nibs.org' ||
    proposedHost.endsWith('.nibs.org')
  ) {
    return 'wbdg_nibs';
  }
  if (
    family === 'istructe' ||
    publisher.includes('institution of structural engineers') ||
    title.includes('institution of structural engineers') ||
    proposedHost === 'istructe.org' ||
    proposedHost.endsWith('.istructe.org')
  ) {
    return 'istructe';
  }
  if (
    family === 'ice' ||
    publisher.includes('institution of civil engineers') ||
    title.includes('institution of civil engineers') ||
    proposedHost === 'ice.org.uk' ||
    proposedHost.endsWith('.ice.org.uk') ||
    proposedHost === 'knowledgehub.ice.org.uk' ||
    proposedHost.endsWith('.knowledgehub.ice.org.uk')
  ) {
    return 'ice';
  }
  if (
    family === 'riba' ||
    publisher.includes('royal institute of british architects') ||
    title.includes('royal institute of british architects') ||
    proposedHost === 'architecture.com' ||
    proposedHost.endsWith('.architecture.com') ||
    proposedHost === 'riba.org' ||
    proposedHost.endsWith('.riba.org')
  ) {
    return 'riba';
  }
  if (
    family === 'uniclass_nbs' ||
    publisher === 'nbs' ||
    publisher.includes('national building specification') ||
    title.includes('uniclass') ||
    proposedHost === 'thenbs.com' ||
    proposedHost.endsWith('.thenbs.com') ||
    proposedHost === 'uniclass.thenbs.com' ||
    proposedHost.endsWith('.uniclass.thenbs.com')
  ) {
    return 'uniclass_nbs';
  }
  if (
    family === 'omniclass_csi' ||
    publisher.includes('construction specifications institute') ||
    title.includes('omniclass') ||
    proposedHost === 'csiresources.org' ||
    proposedHost.endsWith('.csiresources.org') ||
    proposedHost === 'csinet.org' ||
    proposedHost.endsWith('.csinet.org')
  ) {
    return 'omniclass_csi';
  }
  return 'unknown';
}

function baseBlockedResult(
  checkedAt: string,
  requestedUrl: string,
  sourceFamily: ControlledSourceCheckResult['sourceFamily'],
  blockers: string[],
  warnings: string[] = [],
): ControlledSourceCheckResult {
  return {
    checkedAt,
    requestedUrl,
    ok: false,
    redirectChain: [],
    officialSourceFamilyMatch: false,
    sourceFamily,
    publicMetadataOnly: true,
    externalVerificationPerformed: false,
    contentPayloadStored: false,
    protectedContentDownloaded: false,
    verificationLimitations: [
      'No protected content was downloaded or stored.',
      'This check verifies bounded URL metadata only and does not establish source truth.',
    ],
    caveats: [
      'HTTP reachability is not a content-correctness, compliance, governing, AHJ, DOI, ISBN, or learner-trust claim.',
    ],
    blockers,
    warnings,
  };
}

async function fetchWithTimeout(fetchImpl: typeof fetch, url: string, method: 'HEAD' | 'GET', timeoutMs: number): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetchImpl(url, {
      method,
      redirect: 'manual',
      signal: controller.signal,
      headers: {
        'User-Agent': 'Vitruvius-Resource-Layer-Source-Check/1.0',
        Accept: method === 'HEAD' ? '*/*' : 'text/html,application/xhtml+xml,text/plain,*/*;q=0.2',
      },
    });
  } finally {
    clearTimeout(timeout);
  }
}

async function followRedirects(
  fetchImpl: typeof fetch,
  url: string,
  method: 'HEAD' | 'GET',
  sourceFamily: ControlledSourceCheckResult['sourceFamily'],
  timeoutMs: number,
  maxRedirects: number,
): Promise<{ response: Response; finalUrl: string; redirectChain: string[]; blockers: string[] }> {
  let currentUrl = url;
  const redirectChain: string[] = [];
  const blockers: string[] = [];

  for (let i = 0; i <= maxRedirects; i += 1) {
    const response = await fetchWithTimeout(fetchImpl, currentUrl, method, timeoutMs);
    if (![301, 302, 303, 307, 308].includes(response.status)) {
      return { response, finalUrl: currentUrl, redirectChain, blockers };
    }
    const location = response.headers.get('location');
    if (!location) {
      blockers.push('Redirect response missing Location header');
      return { response, finalUrl: currentUrl, redirectChain, blockers };
    }
    const nextUrl = new URL(location, currentUrl).toString();
    redirectChain.push(nextUrl);
    const nextHost = normalizeHost(nextUrl);
    if (!nextUrl.startsWith('https://')) {
      blockers.push('Redirect target is not HTTPS');
      return { response, finalUrl: nextUrl, redirectChain, blockers };
    }
    if (!isOfficialHostForFamily(nextHost, sourceFamily)) {
      blockers.push(`Redirect target is outside official ${sourceFamily} domains: ${nextHost}`);
      return { response, finalUrl: nextUrl, redirectChain, blockers };
    }
    currentUrl = nextUrl;
  }

  blockers.push(`Redirect chain exceeded ${maxRedirects} redirects`);
  return {
    response: await fetchWithTimeout(fetchImpl, currentUrl, method, timeoutMs),
    finalUrl: currentUrl,
    redirectChain,
    blockers,
  };
}

async function readLimitedText(response: Response, maxBodyBytes: number): Promise<{ text: string; truncated: boolean }> {
  if (!response.body) return { text: '', truncated: false };
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  let truncated = false;

  try {
    while (total < maxBodyBytes) {
      const { done, value } = await reader.read();
      if (done) break;
      const remaining = maxBodyBytes - total;
      if (value.length > remaining) {
        chunks.push(value.slice(0, remaining));
        total += remaining;
        truncated = true;
        break;
      }
      chunks.push(value);
      total += value.length;
    }
    if (!truncated) {
      const { done, value } = await reader.read();
      if (!done && value?.length) truncated = true;
    }
  } finally {
    try {
      await reader.cancel();
    } catch {
      // Ignore stream cancellation failures after enough metadata was read.
    }
  }

  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.length;
  }
  return { text: new TextDecoder().decode(bytes), truncated };
}

function titleFromHtml(text: string): string | undefined {
  const ogTitle = text.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["'][^>]*>/i)?.[1]
    || text.match(/<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:title["'][^>]*>/i)?.[1];
  const title = ogTitle || text.match(/<title[^>]*>([\s\S]{1,500}?)<\/title>/i)?.[1];
  return title?.replace(/\s+/g, ' ').trim();
}

function isPdfLike(url: string, contentType?: string): boolean {
  return /\.pdf(?:$|[?#])/i.test(url) || Boolean(contentType?.toLowerCase().includes('application/pdf'));
}

export async function checkUrlMetadata(url: string, options: ControlledSourceCheckOptions & { sourceFamily?: ControlledSourceCheckResult['sourceFamily'] } = {}): Promise<ControlledSourceCheckResult> {
  const checkedAt = nowIso(options);
  const sourceFamily = options.sourceFamily || 'unknown';
  const warnings: string[] = [];
  const blockers: string[] = [];

  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    return baseBlockedResult(checkedAt, url, sourceFamily, ['Requested URL is not parseable']);
  }

  if (parsed.protocol !== 'https:') blockers.push('Requested URL must use HTTPS');
  const host = parsed.hostname.toLowerCase().replace(/^www\./, '');
  const officialSourceFamilyMatch = isOfficialHostForFamily(host, sourceFamily);
  if (sourceFamily === 'unknown') blockers.push('Candidate source family is unsupported for controlled verification');
  if (!officialSourceFamilyMatch) blockers.push(`Requested URL is outside official ${sourceFamily} domains: ${host}`);

  const placeholderFlags = detectExternalMetadataPlaceholders({
    title: 'source check',
    resourceType: 'external_url_candidate',
    proposedUrl: url,
  } as any);
  if (placeholderFlags.length > 0) blockers.push(`Requested URL has placeholder/fake metadata flags: ${placeholderFlags.join(', ')}`);

  if (blockers.length > 0) {
    return {
      ...baseBlockedResult(checkedAt, url, sourceFamily, blockers, warnings),
      officialSourceFamilyMatch,
    };
  }

  const fetchImpl = options.fetchImpl || globalThis.fetch;
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxRedirects = options.maxRedirects ?? DEFAULT_MAX_REDIRECTS;
  const maxBodyBytes = options.maxBodyBytes || DEFAULT_MAX_BODY_BYTES;

  try {
    const head = await followRedirects(fetchImpl, parsed.toString(), 'HEAD', sourceFamily, timeoutMs, maxRedirects);
    warnings.push(...head.blockers);
    let response = head.response;
    let finalUrl = head.finalUrl;
    let redirectChain = head.redirectChain;
    let contentType = response.headers.get('content-type') || undefined;
    const contentLength = safeContentLength(response.headers.get('content-length'));
    let title: string | undefined;

    const canGetMetadata =
      response.status === 405 ||
      response.status === 403 ||
      !contentType ||
      /^text\/|html|xhtml|json/i.test(contentType);

    if (canGetMetadata && !isPdfLike(finalUrl, contentType)) {
      const get = await followRedirects(fetchImpl, finalUrl, 'GET', sourceFamily, timeoutMs, maxRedirects);
      warnings.push(...get.blockers);
      response = get.response;
      finalUrl = get.finalUrl;
      redirectChain = Array.from(new Set([...redirectChain, ...get.redirectChain]));
      contentType = response.headers.get('content-type') || contentType;
      if (/^text\/|html|xhtml|json/i.test(contentType || '')) {
        const limited = await readLimitedText(response, maxBodyBytes);
        if (limited.truncated) warnings.push(`Response body inspection stopped at ${maxBodyBytes} bytes`);
        title = titleFromHtml(limited.text);
      }
    }

    if (isPdfLike(finalUrl, contentType)) {
      warnings.push('PDF-like response detected; protected payload was not downloaded or stored');
    }
    if (response.status >= 400) blockers.push(`HTTP status is not successful: ${response.status}`);

    return {
      checkedAt,
      requestedUrl: parsed.toString(),
      finalUrl,
      statusCode: response.status,
      ok: response.ok,
      contentType,
      contentLength,
      redirectChain,
      title,
      officialSourceFamilyMatch: isOfficialHostForFamily(normalizeHost(finalUrl), sourceFamily),
      sourceFamily,
      publicMetadataOnly: true,
      externalVerificationPerformed: true,
      contentPayloadStored: false,
      protectedContentDownloaded: false,
      verificationLimitations: [
        'Only URL reachability and public response metadata were checked.',
        'No full page body, PDF content, protected standard text, DOI lookup, ISBN lookup, or source-truth verification was stored.',
      ],
      caveats: [
        'HTTP success is not source truth.',
        'This check does not establish current/governing/compliance/AHJ status or learner trust.',
      ],
      blockers: Array.from(new Set(blockers)),
      warnings: Array.from(new Set(warnings)),
    };
  } catch (error) {
    return {
      ...baseBlockedResult(
        checkedAt,
        parsed.toString(),
        sourceFamily,
        [`Controlled URL check failed: ${error instanceof Error ? error.message : String(error)}`],
        warnings,
      ),
      officialSourceFamilyMatch,
    };
  }
}

export async function checkOfficialSourceCandidate(candidate: ExternalMetadataCandidateRecord, options: ControlledSourceCheckOptions = {}): Promise<ControlledSourceCheckResult> {
  const sourceFamily = officialSourceFamilyForCandidate(candidate);
  const requestedUrl = options.requestedUrl || candidate.proposedUrl || candidate.normalizedUrl;
  if (!requestedUrl) {
    return baseBlockedResult(nowIso(options), '', sourceFamily, ['Candidate has no URL to verify']);
  }
  return checkUrlMetadata(requestedUrl, { ...options, sourceFamily });
}

function candidateMissingSourceCustodyFields(candidate: ExternalMetadataCandidateRecord): string[] {
  const missing: string[] = [];
  if (!candidate.title?.trim()) missing.push('title');
  if (!candidate.proposedUrl?.trim()) missing.push('url');
  if (!candidate.proposedSourceFamilyId?.trim()) missing.push('sourceFamily');
  if (!candidate.proposedRightsStatus?.trim()) missing.push('rightsStatus');
  return missing;
}

function standardsMissingContextFields(candidate: ExternalMetadataCandidateRecord, context?: StandardsContextInput): string[] {
  const missing: string[] = [];
  if (!(context?.standardTitle || candidate.title)?.toString().trim()) missing.push('standardTitle');
  if (!context?.edition?.toString().trim() && !candidate.proposedEdition?.trim()) missing.push('edition');
  if (!context?.version?.toString().trim() && context?.publicationYear === undefined && !candidate.proposedVersion?.trim()) missing.push('version/year');
  if (!context?.scope?.toString().trim() && !candidate.proposedScope?.trim()) missing.push('scope');
  if (!context?.jurisdictionApplicabilityCaveat?.toString().trim() && !candidate.proposedJurisdiction?.trim()) missing.push('jurisdiction/applicability caveat');
  return missing;
}

function placeholderStandardsFields(context?: StandardsContextInput): string[] {
  const flags: string[] = [];
  for (const [key, value] of Object.entries(context || {})) {
    if (value === undefined || value === null) continue;
    const text = String(value).trim();
    if (FORBIDDEN_PLACEHOLDER_VALUE.test(text)) flags.push(key);
    if (UNSUPPORTED_TRUST_CLAIM.test(text)) flags.push(`${key}:unsupported_trust_claim`);
  }
  return flags;
}

export function classifySourceVerificationOutcome(
  candidate: ExternalMetadataCandidateRecord,
  checkResult: ControlledSourceCheckResult,
  input: Partial<SourceVerificationDecisionInput> = {},
): { proposedNextStatus: SourceVerificationNextStatus; missingFields: string[]; blockers: string[]; warnings: string[] } {
  const blockers = [...checkResult.blockers];
  const warnings = [...checkResult.warnings];
  const missingFields = candidateMissingSourceCustodyFields(candidate);

  let proposedNextStatus: SourceVerificationNextStatus = 'source_custody_review_needed';
  if (checkResult.ok && checkResult.officialSourceFamilyMatch && blockers.length === 0) {
    proposedNextStatus = 'source_custody_in_review';
  }
  if (input.nextStatus) proposedNextStatus = input.nextStatus;

  if (proposedNextStatus === 'source_custody_verified') {
    if (!checkResult.ok || !checkResult.officialSourceFamilyMatch) blockers.push('source_custody_verified requires a reachable official source-family URL');
    if (!input.rightsStatus?.trim()) blockers.push('source_custody_verified requires rightsStatus');
    if (!input.accessType?.trim()) blockers.push('source_custody_verified requires accessType');
    if (!input.rightsAssessmentRationale?.trim()) blockers.push('source_custody_verified requires rightsAssessmentRationale');
  }
  if (proposedNextStatus === 'rights_review_needed') {
    warnings.push('Rights/access context remains unresolved; learner visibility and promotion remain blocked');
  }

  return {
    proposedNextStatus,
    missingFields,
    blockers: Array.from(new Set(blockers)),
    warnings: Array.from(new Set(warnings)),
  };
}

export function classifyStandardsContextOutcome(
  candidate: ExternalMetadataCandidateRecord,
  checkResult: ControlledSourceCheckResult,
  input: Partial<SourceVerificationDecisionInput> = {},
): { proposedNextStatus: SourceVerificationNextStatus; missingFields: string[]; blockers: string[]; warnings: string[] } {
  const blockers = [...checkResult.blockers];
  const warnings = [...checkResult.warnings];
  const context = input.standardsContext;
  const placeholderFields = placeholderStandardsFields(context);
  const missingFields = standardsMissingContextFields(candidate, context);

  if (candidate.resourceType !== 'standard_candidate' && candidate.resourceType !== 'guide_candidate') {
    blockers.push('Standards context verification applies only to standard_candidate or guide_candidate');
  }
  if (placeholderFields.length > 0) {
    blockers.push(`Standards context contains placeholder or unsupported trust-claim fields: ${placeholderFields.join(', ')}`);
  }

  let proposedNextStatus: SourceVerificationNextStatus = 'standards_context_needed';
  if (checkResult.ok && checkResult.officialSourceFamilyMatch) proposedNextStatus = 'standards_context_in_review';
  if (missingFields.length === 0 && placeholderFields.length === 0) proposedNextStatus = 'standards_context_complete';
  if (input.nextStatus) proposedNextStatus = input.nextStatus;

  if (proposedNextStatus === 'standards_context_complete') {
    if (missingFields.length > 0) blockers.push(`standards_context_complete requires: ${missingFields.join(', ')}`);
    if (!input.sourceOfContext?.trim()) blockers.push('standards_context_complete requires sourceOfContext');
    if (!input.reviewer?.trim()) blockers.push('standards_context_complete requires reviewer');
    if (!input.rationale?.trim()) blockers.push('standards_context_complete requires rationale');
  }

  return {
    proposedNextStatus,
    missingFields,
    blockers: Array.from(new Set(blockers)),
    warnings: Array.from(new Set(warnings)),
  };
}

export async function buildSourceVerificationPreview(
  candidate: ExternalMetadataCandidateRecord,
  input: Partial<SourceVerificationDecisionInput> = {},
  options: ControlledSourceCheckOptions = {},
): Promise<SourceVerificationPreview> {
  const sourceCheck = await checkOfficialSourceCandidate(candidate, { ...options, requestedUrl: input.requestedUrl || options.requestedUrl });
  const outcome = classifySourceVerificationOutcome(candidate, sourceCheck, input);
  const previewWithoutHash: Omit<SourceVerificationPreview, 'previewHash'> = {
    schemaVersion: 'vitruvius-source-verification-preview/v1',
    kind: 'source_verification',
    candidateId: candidate.candidateId,
    priorStatus: candidate.status,
    proposedNextStatus: outcome.proposedNextStatus,
    noWrite: true,
    learnerVisible: false,
    displayPolicy: candidate.displayPolicy === 'dev_only' ? 'dev_only' : 'reviewer_only',
    verificationStatus: 'unverified',
    sourceCheck,
    missingFields: outcome.missingFields,
    warnings: outcome.warnings,
    blockers: outcome.blockers,
    caveats: sourceCheck.caveats,
    noResourceCreated: true,
    noNodeResourceLinkCreated: true,
    noPromotion: true,
    noGraphCanonicalMutation: true,
  };
  return { ...previewWithoutHash, previewHash: hashPreview(previewWithoutHash) };
}

export async function buildStandardsContextVerificationPreview(
  candidate: ExternalMetadataCandidateRecord,
  input: Partial<SourceVerificationDecisionInput> = {},
  options: ControlledSourceCheckOptions = {},
): Promise<SourceVerificationPreview> {
  const sourceCheck = await checkOfficialSourceCandidate(candidate, { ...options, requestedUrl: input.requestedUrl || options.requestedUrl });
  const outcome = classifyStandardsContextOutcome(candidate, sourceCheck, input);
  const previewWithoutHash: Omit<SourceVerificationPreview, 'previewHash'> = {
    schemaVersion: 'vitruvius-source-verification-preview/v1',
    kind: 'standards_context_verification',
    candidateId: candidate.candidateId,
    priorStatus: candidate.status,
    proposedNextStatus: outcome.proposedNextStatus,
    noWrite: true,
    learnerVisible: false,
    displayPolicy: candidate.displayPolicy === 'dev_only' ? 'dev_only' : 'reviewer_only',
    verificationStatus: 'unverified',
    sourceCheck,
    missingFields: outcome.missingFields,
    warnings: outcome.warnings,
    blockers: outcome.blockers,
    caveats: sourceCheck.caveats,
    noResourceCreated: true,
    noNodeResourceLinkCreated: true,
    noPromotion: true,
    noGraphCanonicalMutation: true,
  };
  return { ...previewWithoutHash, previewHash: hashPreview(previewWithoutHash) };
}

function validateDecisionInput(input: SourceVerificationDecisionInput): string[] {
  const blockers: string[] = [];
  if (!input.reviewer?.trim()) blockers.push('reviewer is required');
  if (!input.rationale?.trim()) blockers.push('rationale is required');
  if (!input.sourceOfContext?.trim()) blockers.push('sourceOfContext is required');
  return blockers;
}

async function applyVerificationDecision(
  repoRoot: string,
  candidateId: string,
  kind: SourceVerificationKind,
  input: SourceVerificationDecisionInput,
  options: ControlledSourceCheckOptions = {},
): Promise<SourceVerificationApplyResult> {
  const registry = loadExternalCandidateRegistry(repoRoot);
  const candidate = registry.candidates.find((c) => c.candidateId === candidateId);
  if (!candidate) throw new Error(`Candidate not found: ${candidateId}`);

  const preview = kind === 'standards_context_verification'
    ? await buildStandardsContextVerificationPreview(candidate, input, options)
    : await buildSourceVerificationPreview(candidate, input, options);

  const inputBlockers = validateDecisionInput(input);
  const blockers = [...inputBlockers, ...preview.blockers];
  if (input.previewHash && input.previewHash !== preview.previewHash) {
    blockers.push('previewHash does not match server-rerun preview');
  }
  if (blockers.length > 0) {
    throw new Error(`Source verification decision blocked: ${Array.from(new Set(blockers)).join('; ')}`);
  }

  const reviewedAt = nowIso(options);
  const priorStatus = candidate.status;
  const nextStatus = input.nextStatus || preview.proposedNextStatus;
  const decisionId = `ext-src-dec-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const decision = {
    decisionId,
    candidateId,
    decisionType: input.decisionType || kind,
    priorStatus,
    nextStatus,
    reviewer: input.reviewer,
    reviewerIdentity: 'project_owner_delegated_ai_reviewer',
    reviewerCaveat: 'Delegated external AI review is not a biological human review, not source truth, and not production approval by itself.',
    reviewedAt,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    sourceVerificationCheck: preview.sourceCheck,
    previewHash: preview.previewHash,
    previewRerun: true,
    warnings: preview.warnings,
    missingFields: preview.missingFields,
    caveats: preview.caveats,
    noResourceCreated: true,
    noNodeResourceLinkCreated: true,
    noPromotion: true,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
    learnerVisible: false,
    verificationStatus: 'unverified',
    auditCaveat: 'Decision applied to external candidate status/history only. No Resource, nodeResourceLink, promotion, graph/canonical mutation, or learner exposure occurred.',
  };

  const updated: ExternalMetadataCandidateRecord = {
    ...candidate,
    status: nextStatus as any,
    verificationStatus: 'unverified',
    learnerVisible: false,
    displayPolicy: candidate.displayPolicy === 'dev_only' ? 'dev_only' : 'reviewer_only',
    warningFlags: Array.from(new Set([...(candidate.warningFlags || []), ...preview.warnings])),
    decisions: [...(candidate.decisions || []), decision],
  };

  const idx = registry.candidates.findIndex((c) => c.candidateId === candidateId);
  registry.candidates[idx] = updated;

  const operationType = kind === 'standards_context_verification'
    ? 'external_candidate_standards_context_verification_decision'
    : 'external_candidate_source_verification_decision';
  const { manifest } = withResourceLayerTransaction(
    repoRoot,
    operationType,
    [externalCandidateRegistryPath(repoRoot)],
    () => {
      saveExternalCandidateRegistry(repoRoot, registry);
      return updated;
    },
  );

  updated.transactionManifestId = manifest.transactionId;
  return {
    ok: true,
    candidate: updated,
    decision,
    preview,
    manifest: { transactionId: manifest.transactionId },
    rollbackPlan: {
      action: 'restore_prior_status_append_rollback_decision',
      candidateId,
      priorStatus,
      nextStatus,
      auditHistoryPreserved: true,
    },
    noResourceCreated: true,
    noNodeResourceLinkCreated: true,
    noPromotion: true,
    learnerVisible: false,
    externalVerificationPerformed: preview.sourceCheck.externalVerificationPerformed,
  };
}

export function applySourceVerificationDecision(
  repoRoot: string,
  candidateId: string,
  input: SourceVerificationDecisionInput,
  options: ControlledSourceCheckOptions = {},
): Promise<SourceVerificationApplyResult> {
  return applyVerificationDecision(repoRoot, candidateId, 'source_verification', input, options);
}

export function applyStandardsContextVerificationDecision(
  repoRoot: string,
  candidateId: string,
  input: SourceVerificationDecisionInput,
  options: ControlledSourceCheckOptions = {},
): Promise<SourceVerificationApplyResult> {
  return applyVerificationDecision(repoRoot, candidateId, 'standards_context_verification', input, options);
}
