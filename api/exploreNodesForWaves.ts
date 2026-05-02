import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');
const shadowStagingRoot = resolve(repoRoot, '006_System-Manifests', 'aec-mepfs-backbone', 'shadow-staging');

function latestShadowGraphPath() {
  const runs = readdirSync(shadowStagingRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d{8}T\d{6}Z$/.test(entry.name))
    .map((entry) => entry.name)
    .sort((left, right) => right.localeCompare(left));
  for (const run of runs) {
    const candidate = join(shadowStagingRoot, run, 'shadow-backbone-graph.json');
    if (existsSync(candidate)) return candidate;
  }
  throw new Error('No shadow-backbone-graph.json artifact found');
}

const graphPath = latestShadowGraphPath();
const raw = JSON.parse(readFileSync(graphPath, 'utf-8'));
const nodes = raw.nodes || [];

// Group nodes by top-level domain code
const byDomain: Record<string, Array<{id: string; label: string; path_code?: string}>> = {};
for (const n of nodes) {
  const id = String(n.id);
  const label = String(n.label || n.pref_label || '');
  const pathCode = String(n.path_code || '');
  const domain = pathCode.split('.')[0] || 'UNKNOWN';
  if (!byDomain[domain]) byDomain[domain] = [];
  byDomain[domain].push({ id, label, path_code: pathCode });
}

// Sort by path code for readability
for (const domain of Object.keys(byDomain)) {
  byDomain[domain].sort((a, b) => (a.path_code || '').localeCompare(b.path_code || ''));
}

console.log(JSON.stringify({
  totalNodes: nodes.length,
  domainCounts: Object.fromEntries(Object.entries(byDomain).map(([k, v]) => [k, v.length])),
  domains: Object.fromEntries(Object.entries(byDomain).map(([k, v]) => [k, v.slice(0, 40)])),
}, null, 2));
