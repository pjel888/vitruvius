import { createHash } from 'node:crypto';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import type { ExternalMetadataCandidateInput, ExternalMetadataCandidatePreview } from './externalMetadataCandidates';
import { buildExternalCandidatePreview, validateExternalMetadataCandidate } from './externalMetadataCandidates';
import { withResourceLayerTransaction } from './transactionManifest';

export const EXTERNAL_CANDIDATE_REGISTRY_SCHEMA_VERSION = 'vitruvius-external-metadata-candidate/v1';
export const EXTERNAL_CANDIDATE_REGISTRY_FILE = 'external-metadata-candidates.json';

export interface ExternalMetadataCandidateRecord extends ExternalMetadataCandidatePreview {
  candidateId: string;
  persistedAt: string;
  previewHash: string;
  status: 'candidate' | 'needs_review' | 'blocked' | 'metadata_correction_needed' | 'source_custody_review_needed' | 'source_custody_in_review' | 'source_custody_verified' | 'source_custody_rejected' | 'rights_review_needed' | 'standards_context_needed' | 'standards_context_in_review' | 'standards_context_complete' | 'standards_context_rejected' | 'duplicate_candidate' | 'rejected' | 'deferred' | 'ready_for_promotion_review' | 'promotion_blocked';
  noAutoVerification: true;
  noAutoPromotion: true;
  noAutoLinking: true;
  noLearnerExposure: true;
  transactionManifestId?: string;
  decisions?: any[];
}

export interface ExternalCandidateRegistry {
  schemaVersion: string;
  generatedAt: string;
  candidates: ExternalMetadataCandidateRecord[];
}

function registryPath(repoRoot: string): string {
  return resolve(repoRoot, '006_System-Manifests', 'resource-layer', EXTERNAL_CANDIDATE_REGISTRY_FILE);
}

function readJsonObject(path: string): unknown {
  const text = readFileSync(path, 'utf-8').replace(/^\uFEFF/, '');
  return JSON.parse(text);
}

export function loadExternalCandidateRegistry(repoRoot: string): ExternalCandidateRegistry {
  const path = registryPath(repoRoot);
  if (!existsSync(path)) {
    return {
      schemaVersion: EXTERNAL_CANDIDATE_REGISTRY_SCHEMA_VERSION,
      generatedAt: new Date().toISOString(),
      candidates: [],
    };
  }
  const payload = readJsonObject(path) as ExternalCandidateRegistry;
  if (!payload || typeof payload !== 'object' || !Array.isArray(payload.candidates)) {
    throw new Error(`${path} must contain an object with a candidates array`);
  }
  return payload;
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

export function hashExternalCandidatePreview(preview: ExternalMetadataCandidatePreview): string {
  return createHash('sha256').update(stableStringify(preview)).digest('hex');
}

function deterministicWrite(path: string, payload: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  const temp = `${path}.tmp`;
  writeFileSync(temp, `${JSON.stringify(payload, null, 2)}\n`);
  if (existsSync(path)) {
    const { rmSync } = require('node:fs');
    rmSync(path, { force: true });
  }
  writeFileSync(path, readFileSync(temp));
  const { rmSync } = require('node:fs');
  rmSync(temp, { force: true });
}

export function saveRegistry(repoRoot: string, registry: ExternalCandidateRegistry) {
  const path = registryPath(repoRoot);
  registry.generatedAt = new Date().toISOString();
  deterministicWrite(path, registry);
}

export function buildExternalCandidateId(input: ExternalMetadataCandidateInput): string {
  const base = input.title?.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40) || 'candidate';
  const ts = Date.now().toString(36);
  const rand = Math.random().toString(36).slice(2, 6);
  return `ext-cand-${base}-${ts}-${rand}`;
}

function detectDuplicate(
  registry: ExternalCandidateRegistry,
  preview: ExternalMetadataCandidatePreview,
): ExternalMetadataCandidateRecord | null {
  return registry.candidates.find((c) => {
    if (preview.normalizedUrl && c.normalizedUrl === preview.normalizedUrl) return true;
    if (preview.normalizedDoi && c.normalizedDoi === preview.normalizedDoi) return true;
    if (preview.normalizedIsbn && c.normalizedIsbn === preview.normalizedIsbn) return true;
    if (
      !preview.normalizedUrl &&
      !preview.normalizedDoi &&
      !preview.normalizedIsbn &&
      c.title?.trim().toLowerCase() === preview.title?.trim().toLowerCase()
    ) {
      return true;
    }
    return false;
  }) || null;
}

export interface PersistResult {
  ok: boolean;
  candidate?: ExternalMetadataCandidateRecord;
  duplicateOf?: ExternalMetadataCandidateRecord;
  error?: string;
  manifest?: { transactionId: string; manifestHash?: string };
}

export function persistExternalCandidate(
  repoRoot: string,
  input: ExternalMetadataCandidateInput,
): PersistResult {
  const preview = buildExternalCandidatePreview(input);
  const validation = validateExternalMetadataCandidate(input);

  if (!validation.ok) {
    return { ok: false, error: `Preview validation failed: ${validation.errors.join('; ')}` };
  }

  if (preview.fakePlaceholderFlags.length > 0) {
    return { ok: false, error: `Placeholder metadata detected: ${preview.fakePlaceholderFlags.join(', ')}` };
  }

  if (preview.learnerVisible !== false) {
    return { ok: false, error: 'learnerVisible must be false' };
  }
  if (preview.displayPolicy !== 'reviewer_only' && preview.displayPolicy !== 'dev_only') {
    return { ok: false, error: 'displayPolicy must be reviewer_only or dev_only' };
  }

  const registry = loadExternalCandidateRegistry(repoRoot);
  const duplicate = detectDuplicate(registry, preview);
  if (duplicate) {
    return { ok: false, duplicateOf: duplicate, error: `Duplicate of existing candidate ${duplicate.candidateId}` };
  }

  const candidateId = buildExternalCandidateId(input);
  const previewHash = hashExternalCandidatePreview(preview);

  const record: ExternalMetadataCandidateRecord = {
    ...preview,
    candidateId,
    persistedAt: new Date().toISOString(),
    previewHash,
    status: 'candidate',
    noAutoVerification: true,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
  };

  const { result, manifest } = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_persist',
    [registryPath(repoRoot)],
    () => {
      registry.candidates.push(record);
      saveRegistry(repoRoot, registry);
      return record;
    },
  );

  result.transactionManifestId = manifest.transactionId;
  return {
    ok: true,
    candidate: result,
    manifest: { transactionId: manifest.transactionId, manifestHash: manifest.manifestHash },
  };
}

export function listExternalCandidates(
  repoRoot: string,
  filters?: { status?: string; resourceType?: string },
): ExternalMetadataCandidateRecord[] {
  const registry = loadExternalCandidateRegistry(repoRoot);
  let candidates = registry.candidates;
  if (filters?.status) {
    candidates = candidates.filter((c) => c.status === filters.status);
  }
  if (filters?.resourceType) {
    candidates = candidates.filter((c) => c.resourceType === filters.resourceType);
  }
  return candidates;
}

export function getExternalCandidate(repoRoot: string, candidateId: string): ExternalMetadataCandidateRecord | null {
  const registry = loadExternalCandidateRegistry(repoRoot);
  return registry.candidates.find((c) => c.candidateId === candidateId) || null;
}
