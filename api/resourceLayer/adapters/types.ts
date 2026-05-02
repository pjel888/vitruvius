import type { ResourceCandidate, ResourceType, SourceAuthority } from '../types';
import { canonicalizeUrl, normalizeIsbn } from '../normalization';

export interface ResourceSearchQuery {
  nodeId?: string;
  label: string;
  aliases?: string[];
  taxonomy?: string;
  disciplineTags?: string[];
  resourceTypes?: ResourceType[];
  limit?: number;
}

export interface ResourceDiscoveryAdapter {
  id: string;
  displayName: string;
  isConfigured(): boolean;
  search(query: ResourceSearchQuery): Promise<ResourceCandidate[]>;
}

export function buildCandidateId(adapter: string, identifier: string) {
  return `candidate-${adapter}-${identifier}`.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 120);
}

export function candidateFromMetadata(input: {
  adapter: string;
  nodeId?: string;
  query: string;
  title?: string;
  url?: string;
  identifier?: string;
  preliminaryScore?: number;
  rawMetadata?: unknown;
}): ResourceCandidate {
  const stable = input.identifier || canonicalizeUrl(input.url) || input.title || input.query;
  return {
    id: buildCandidateId(input.adapter, stable || 'unknown'),
    nodeId: input.nodeId,
    adapter: input.adapter,
    query: input.query,
    rawTitle: input.title,
    rawUrl: input.url,
    rawIdentifier: input.identifier,
    rawMetadata: input.rawMetadata,
    preliminaryScore: Math.max(0, Math.min(1, input.preliminaryScore ?? 0.5)),
    dedupeKey: input.identifier || canonicalizeUrl(input.url),
    reviewStatus: 'candidate',
    createdAt: new Date().toISOString(),
  };
}

export function authorityFromBookProvider(): SourceAuthority {
  return 'recognized_publisher';
}

export function normalizedIsbnFromIdentifiers(values: unknown): string | undefined {
  if (!Array.isArray(values)) return undefined;
  for (const value of values) {
    const identifier = typeof value === 'string'
      ? value
      : value && typeof value === 'object'
        ? String((value as { identifier?: unknown }).identifier || '')
        : '';
    const normalized = normalizeIsbn(identifier);
    if (normalized) return normalized;
  }
  return undefined;
}
