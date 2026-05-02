import { createHash, createHmac } from 'node:crypto';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, readdirSync, renameSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { resourceLayerFilePaths } from './registry';

export interface ResourceLayerTransactionManifest {
  transactionId: string;
  operationType: string;
  subsystem?: string;
  actor?: string;
  startedAt: string;
  completedAt?: string;
  filesTouched: string[];
  beforeHashes: Record<string, string>;
  afterHashes?: Record<string, string>;
  previousManifestHash?: string | null;
  manifestHash?: string;
  signature?: string;
  dryRun?: boolean;
  decisionIds?: string[];
  rollbackCapability?: 'full' | 'partial' | 'blocked' | 'unsupported';
  warnings?: string[];
  errors?: string[];
  validationStatus: 'pending' | 'passed' | 'failed';
  error?: string;
}

function nowIso() {
  return new Date().toISOString();
}

function digest(value: string | Buffer) {
  return createHash('sha256').update(value).digest('hex');
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

function manifestIntegrityPayload(manifest: ResourceLayerTransactionManifest) {
  const { manifestHash, signature, ...rest } = manifest;
  return rest;
}

function manifestHash(manifest: ResourceLayerTransactionManifest) {
  return digest(stableStringify(manifestIntegrityPayload(manifest)));
}

function manifestSignature(manifest: ResourceLayerTransactionManifest) {
  const key = process.env.VITRUVIUS_TRANSACTION_HMAC_KEY;
  if (!key) return undefined;
  const scopedKey = createHmac('sha256', key).update(manifest.subsystem || 'resource-layer').digest();
  return createHmac('sha256', scopedKey).update(stableStringify(manifestIntegrityPayload(manifest))).digest('hex');
}

function fileHash(path: string) {
  if (!existsSync(path)) return 'missing';
  return digest(readFileSync(path));
}

function deterministicWrite(path: string, payload: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  const temp = `${path}.tmp`;
  writeFileSync(temp, `${JSON.stringify(payload, null, 2)}\n`);
  if (existsSync(path)) rmSync(path, { force: true });
  renameSync(temp, path);
}

function latestManifestHash(transactionsDir: string) {
  if (!existsSync(transactionsDir)) return null;
  return readdirSync(transactionsDir)
    .filter((name) => name.endsWith('.json'))
    .map((name) => {
      try {
        const payload = JSON.parse(readFileSync(join(transactionsDir, name), 'utf-8')) as ResourceLayerTransactionManifest;
        return { name, startedAt: payload.startedAt || name, manifestHash: payload.manifestHash || null };
      } catch {
        return { name, startedAt: name, manifestHash: null };
      }
    })
    .sort((a, b) => a.startedAt.localeCompare(b.startedAt) || a.name.localeCompare(b.name))
    .at(-1)?.manifestHash || null;
}

function writeManifest(path: string, manifest: ResourceLayerTransactionManifest) {
  const next = { ...manifest };
  next.manifestHash = manifestHash(next);
  next.signature = manifestSignature(next);
  deterministicWrite(path, next);
  return next;
}

function clearStaleLock(path: string, maxAgeMs = 10 * 60 * 1000) {
  if (!existsSync(path)) return;
  const ageMs = Date.now() - statSync(path).mtimeMs;
  if (ageMs > maxAgeMs) rmSync(path, { force: true });
}

export function resourceLayerTransactionPaths(repoRoot: string) {
  const paths = resourceLayerFilePaths(repoRoot);
  return {
    transactionsDir: join(paths.dir, 'transaction-manifests'),
    lock: join(paths.dir, '.resource-layer-review.lock'),
  };
}

export function withResourceLayerTransaction<T>(
  repoRoot: string,
  operationType: string,
  filesTouched: string[],
  fn: () => T,
): { result: T; manifest: ResourceLayerTransactionManifest } {
  const transactionPaths = resourceLayerTransactionPaths(repoRoot);
  mkdirSync(transactionPaths.transactionsDir, { recursive: true });
  let lockFd: number | null = null;
  const startedAt = nowIso();
  const transactionId = `resource-layer-tx-${startedAt.replace(/\D/g, '').slice(0, 14)}-${digest(`${operationType}:${startedAt}`).slice(0, 12)}`;
  const manifestPath = join(transactionPaths.transactionsDir, `${transactionId}.json`);
  const manifest: ResourceLayerTransactionManifest = {
    transactionId,
    operationType,
    subsystem: 'resource-layer',
    startedAt,
    filesTouched,
    beforeHashes: Object.fromEntries(filesTouched.map((path) => [path, fileHash(path)])),
    previousManifestHash: latestManifestHash(transactionPaths.transactionsDir),
    dryRun: false,
    warnings: [],
    errors: [],
    validationStatus: 'pending',
  };

  try {
    clearStaleLock(transactionPaths.lock);
    lockFd = openSync(transactionPaths.lock, 'wx');
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    const result = fn();
    manifest.completedAt = nowIso();
    manifest.afterHashes = Object.fromEntries(filesTouched.map((path) => [path, fileHash(path)]));
    manifest.validationStatus = 'passed';
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    return { result, manifest };
  } catch (error) {
    manifest.completedAt = nowIso();
    manifest.validationStatus = 'failed';
    manifest.error = error instanceof Error ? error.message : String(error);
    manifest.errors = [manifest.error];
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    throw error;
  } finally {
    if (lockFd !== null) closeSync(lockFd);
    if (existsSync(transactionPaths.lock)) rmSync(transactionPaths.lock, { force: true });
  }
}
