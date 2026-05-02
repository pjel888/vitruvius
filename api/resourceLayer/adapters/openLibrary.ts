import type { ResourceCandidate } from '../types';
import { canonicalizeUrl } from '../normalization';
import type { ResourceDiscoveryAdapter, ResourceSearchQuery } from './types';
import { candidateFromMetadata, normalizedIsbnFromIdentifiers } from './types';

interface OpenLibraryDoc {
  key?: string;
  title?: string;
  author_name?: string[];
  first_publish_year?: number;
  isbn?: string[];
  publisher?: string[];
}

interface OpenLibrarySearchResponse {
  docs?: OpenLibraryDoc[];
}

export class OpenLibraryAdapter implements ResourceDiscoveryAdapter {
  id = 'open_library';
  displayName = 'Open Library';

  constructor(private readonly fetchImpl: typeof fetch = fetch) {}

  isConfigured() {
    return true;
  }

  async search(query: ResourceSearchQuery): Promise<ResourceCandidate[]> {
    const limit = Math.min(Math.max(query.limit ?? 5, 1), 20);
    const params = new URLSearchParams({ q: [query.label, ...(query.disciplineTags || [])].join(' '), limit: String(limit) });
    const url = `https://openlibrary.org/search.json?${params.toString()}`;
    const response = await this.fetchImpl(url, { method: 'GET' });
    if (!response.ok) return [];
    const payload = await response.json() as OpenLibrarySearchResponse;
    return (payload.docs || []).slice(0, limit).map((doc) => {
      const keyUrl = doc.key ? `https://openlibrary.org${doc.key}` : undefined;
      const isbn = normalizedIsbnFromIdentifiers(doc.isbn || []);
      return candidateFromMetadata({
        adapter: this.id,
        nodeId: query.nodeId,
        query: query.label,
        title: doc.title,
        url: keyUrl,
        identifier: isbn || canonicalizeUrl(keyUrl),
        preliminaryScore: doc.title?.toLowerCase().includes(query.label.toLowerCase()) ? 0.7 : 0.45,
        rawMetadata: {
          provider: 'open_library',
          title: doc.title,
          authors: doc.author_name,
          firstPublishYear: doc.first_publish_year,
          isbn,
          publisher: doc.publisher?.[0],
        },
      });
    });
  }
}
