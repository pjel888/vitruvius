import { createHash } from 'node:crypto';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { relative, resolve, sep } from 'node:path';
import type { Resource, ResourceCheck } from './types';
import { canonicalizeUrl, normalizeDoi, normalizeIsbn } from './normalization';

export function resolvePathInsideRepo(repoRoot: string, relativePath: string) {
  const root = resolve(repoRoot);
  const target = resolve(root, relativePath);
  const rel = relative(root, target);
  if (rel.startsWith('..') || rel.startsWith(sep)) throw new Error('Local resource path must stay inside the repository');
  return target;
}

export async function sha256File(path: string) {
  const hash = createHash('sha256');
  await new Promise<void>((resolvePromise, reject) => {
    const stream = createReadStream(path);
    stream.on('data', (chunk) => hash.update(chunk));
    stream.on('error', reject);
    stream.on('end', () => resolvePromise());
  });
  return hash.digest('hex');
}

export async function verifyUrlHealth(url: string, fetchImpl: typeof fetch = fetch) {
  const response = await fetchImpl(url, { method: 'HEAD', redirect: 'follow' });
  return { ok: response.ok, status: response.status, finalUrl: response.url || url };
}

export async function buildResourceChecks(
  resource: Resource,
  options: { repoRoot: string; checkedAt: string; checkExternal?: boolean; fetchImpl?: typeof fetch },
): Promise<ResourceCheck[]> {
  const checks: ResourceCheck[] = [];
  const idPrefix = `${resource.id}:${options.checkedAt}`;
  if (resource.url || resource.canonicalUrl) {
    const canonical = canonicalizeUrl(resource.canonicalUrl || resource.url);
    checks.push({ id: `${idPrefix}:canonical_url`, resourceId: resource.id, checkType: 'canonical_url', status: canonical ? 'pass' : 'fail', checkedAt: options.checkedAt, details: canonical || 'Invalid URL' });
    if (options.checkExternal && canonical) {
      try {
        const health = await verifyUrlHealth(canonical, options.fetchImpl || fetch);
        checks.push({ id: `${idPrefix}:url_health`, resourceId: resource.id, checkType: 'url_health', status: health.ok ? 'pass' : 'fail', checkedAt: options.checkedAt, details: `HTTP ${health.status} ${health.finalUrl}` });
      } catch (error) {
        checks.push({ id: `${idPrefix}:url_health`, resourceId: resource.id, checkType: 'url_health', status: 'fail', checkedAt: options.checkedAt, details: error instanceof Error ? error.message : 'URL health check failed' });
      }
    }
  }
  if (resource.doi) checks.push({ id: `${idPrefix}:doi_normalization`, resourceId: resource.id, checkType: 'doi_resolution', status: normalizeDoi(resource.doi) ? 'pass' : 'fail', checkedAt: options.checkedAt, details: normalizeDoi(resource.doi) || 'Invalid DOI format' });
  if (resource.isbn10 || resource.isbn13) {
    const normalized = normalizeIsbn(resource.isbn13) || normalizeIsbn(resource.isbn10);
    checks.push({ id: `${idPrefix}:isbn_normalization`, resourceId: resource.id, checkType: 'isbn_normalization', status: normalized ? 'pass' : 'fail', checkedAt: options.checkedAt, details: normalized || 'Invalid ISBN format' });
  }
  if (resource.localPath) {
    try {
      const resolved = resolvePathInsideRepo(options.repoRoot, resource.localPath);
      const exists = existsSync(resolved);
      checks.push({ id: `${idPrefix}:local_file_exists`, resourceId: resource.id, checkType: 'local_file_exists', status: exists ? 'pass' : 'fail', checkedAt: options.checkedAt, details: exists ? `size=${statSync(resolved).size}` : 'Missing local file' });
      if (exists && resource.localFileHash) {
        const actualHash = await sha256File(resolved);
        checks.push({ id: `${idPrefix}:local_file_hash`, resourceId: resource.id, checkType: 'local_file_hash', status: actualHash === resource.localFileHash ? 'pass' : 'fail', checkedAt: options.checkedAt, details: actualHash });
      }
    } catch (error) {
      checks.push({ id: `${idPrefix}:local_file_exists`, resourceId: resource.id, checkType: 'local_file_exists', status: 'fail', checkedAt: options.checkedAt, details: error instanceof Error ? error.message : 'Invalid local file path' });
    }
  }
  return checks;
}
