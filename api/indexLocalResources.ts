import { mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { scanLocalCorpus } from './resourceLayer/localCorpusScanner';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './resourceLayer/types';

function argValue(prefix: string) {
  const arg = process.argv.find((value) => value.startsWith(prefix));
  return arg ? arg.slice(prefix.length) : undefined;
}

const repoRoot = resolve(import.meta.dir, '..');
const dirs = process.argv
  .filter((value) => value.startsWith('--dir='))
  .map((value) => value.slice('--dir='.length))
  .filter(Boolean);
const maxFiles = Number.parseInt(argValue('--maxFiles=') || '250', 10);
const scan = scanLocalCorpus({
  repoRoot,
  directories: dirs.length > 0 ? dirs : undefined,
  maxFiles: Number.isFinite(maxFiles) ? maxFiles : 250,
});

const outDir = resolve(repoRoot, '006_System-Manifests', 'resource-layer');
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'local-file-index.json');
writeFileSync(outPath, JSON.stringify({
  schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
  generatedAt: new Date().toISOString(),
  indexedResourceCount: scan.resources.length,
  scannedDirectories: scan.scannedDirectories,
  errors: scan.errors,
  resources: scan.resources,
}, null, 2) + '\n');

console.log(JSON.stringify({
  outputPath: outPath,
  indexedResourceCount: scan.resources.length,
  scannedDirectories: scan.scannedDirectories,
  errorCount: scan.errors.length,
}, null, 2));
