import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { extname, join, relative, resolve } from 'node:path';
import type { LocalFileType, Resource } from './types';

export const DEFAULT_LOCAL_CORPUS_DIRS = [
  'resources', 'docs', 'library', 'public/resources', 'public/library',
  'assets/resources', 'data/resources', '.ai/resources', '.ai/13_research',
];

const SUPPORTED_EXTENSIONS = new Map<string, LocalFileType>([
  ['.pdf', 'pdf'], ['.epub', 'epub'], ['.html', 'html'], ['.htm', 'html'],
  ['.docx', 'docx'], ['.txt', 'txt'], ['.md', 'md'],
]);

function walkFiles(root: string, output: string[]) {
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const path = join(root, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules' || entry.name === '.git') continue;
      walkFiles(path, output);
    } else if (entry.isFile() && SUPPORTED_EXTENSIONS.has(extname(entry.name).toLowerCase())) {
      output.push(path);
    }
  }
}

function hashFileSync(path: string) {
  const hash = createHash('sha256');
  hash.update(readFileSync(path));
  return hash.digest('hex');
}

function titleFromPath(path: string) {
  return path.replace(/\.[^.]+$/, '').split(/[\\/]/).pop()!
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function resourceTypeFromFileType(fileType: LocalFileType): Resource['resourceType'] {
  if (fileType === 'pdf') return 'local_pdf';
  if (fileType === 'epub') return 'local_book';
  return 'internal_document';
}

export interface LocalCorpusScanOptions {
  repoRoot: string;
  directories?: string[];
  now?: string;
  maxFiles?: number;
}

export interface LocalCorpusScanResult {
  scannedDirectories: string[];
  localFilesIndexed: number;
  resources: Resource[];
  errors: string[];
}

export function scanLocalCorpus(options: LocalCorpusScanOptions): LocalCorpusScanResult {
  const root = resolve(options.repoRoot);
  const now = options.now || new Date().toISOString();
  const files: string[] = [];
  const scannedDirectories: string[] = [];
  const errors: string[] = [];
  for (const dir of options.directories || DEFAULT_LOCAL_CORPUS_DIRS) {
    const target = resolve(root, dir);
    if (!existsSync(target)) continue;
    scannedDirectories.push(relative(root, target).replace(/\\/g, '/'));
    try {
      walkFiles(target, files);
    } catch (error) {
      errors.push(`${dir}: ${error instanceof Error ? error.message : 'scan failed'}`);
    }
  }
  const resources: Resource[] = [];
  for (const filePath of files.slice(0, options.maxFiles ?? files.length)) {
    try {
      const ext = extname(filePath).toLowerCase();
      const fileType = SUPPORTED_EXTENSIONS.get(ext);
      if (!fileType) continue;
      const stat = statSync(filePath);
      const localFileHash = hashFileSync(filePath);
      const localPath = relative(root, filePath).replace(/\\/g, '/');
      resources.push({
        id: `local-${fileType}-${localFileHash.slice(0, 16)}`,
        title: titleFromPath(filePath),
        resourceType: resourceTypeFromFileType(fileType),
        sourceAuthority: 'internal',
        authorityTier: 4,
        localPath,
        localFileHash,
        localFileType: fileType,
        localFileSizeBytes: stat.size,
        disciplineTags: [],
        taxonomyTags: [],
        accessType: 'local_only',
        sourceRights: {
          rightsClass: 'local_file_metadata_only',
          restrictions: ['metadata_and_hash_only_no_content_republication'],
          declaredUseBoundary: 'Local corpus scanner stores file metadata and hashes only; it does not admit or republish document text.',
        },
        admissionProvenance: {
          admittedBy: 'script',
          admittedAt: now,
          evidenceRef: localPath,
          custodyChain: [localPath],
          reviewSummary: 'Hash-backed local file discovery record; node linkage requires separate review.',
        },
        verificationStatus: 'local_file_verified',
        lastCheckedAt: now,
        createdAt: now,
        updatedAt: now,
      });
    } catch (error) {
      errors.push(`${filePath}: ${error instanceof Error ? error.message : 'index failed'}`);
    }
  }
  return { scannedDirectories, localFilesIndexed: resources.length, resources, errors };
}
