import type { Resource } from './types';
import { canonicalizeUrl, normalizeDoi, normalizeIsbn, normalizeTextKey } from './normalization';

export type DuplicateKind = 'doi' | 'isbn' | 'canonical_url' | 'local_file_hash' | 'internet_archive_identifier' | 'title_author_year';

export interface DuplicateGroup {
  kind: DuplicateKind;
  key: string;
  resourceIds: string[];
}

export function dedupeKeysForResource(resource: Resource): Array<{ kind: DuplicateKind; key: string }> {
  const keys: Array<{ kind: DuplicateKind; key: string }> = [];
  const doi = normalizeDoi(resource.doi);
  if (doi) keys.push({ kind: 'doi', key: doi });
  const isbn = normalizeIsbn(resource.isbn13) || normalizeIsbn(resource.isbn10);
  if (isbn) keys.push({ kind: 'isbn', key: isbn });
  const canonical = canonicalizeUrl(resource.canonicalUrl || resource.url || resource.landingPageUrl);
  if (canonical) keys.push({ kind: 'canonical_url', key: canonical });
  if (resource.localFileHash) keys.push({ kind: 'local_file_hash', key: resource.localFileHash.toLowerCase() });
  if (resource.internetArchiveIdentifier) keys.push({ kind: 'internet_archive_identifier', key: resource.internetArchiveIdentifier.toLowerCase() });
  const title = normalizeTextKey(resource.title);
  const creator = normalizeTextKey((resource.authors || []).join(' ') || resource.organization || resource.publisher || '');
  if (title && creator && resource.year) keys.push({ kind: 'title_author_year', key: `${title}|${creator}|${resource.year}` });
  return keys;
}

export function detectResourceDuplicates(resources: Resource[]): DuplicateGroup[] {
  const groups = new Map<string, { kind: DuplicateKind; key: string; resourceIds: string[] }>();
  for (const resource of resources) {
    for (const item of dedupeKeysForResource(resource)) {
      const mapKey = `${item.kind}:${item.key}`;
      const existing = groups.get(mapKey);
      if (existing) existing.resourceIds.push(resource.id);
      else groups.set(mapKey, { ...item, resourceIds: [resource.id] });
    }
  }
  return Array.from(groups.values()).filter((group) => new Set(group.resourceIds).size > 1);
}
