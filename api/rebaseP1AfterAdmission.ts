import { rebaseCanonicalP1DecisionPackets, buildDuplicateCandidateGroups } from './graph/canonicalStewardship';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');

const graph = JSON.parse(
  readFileSync(resolve(repoRoot, '006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json'), 'utf8')
);
const nodes = graph.nodes;
const baseEdges = graph.edges;

const resourceData = JSON.parse(
  readFileSync(resolve(repoRoot, '006_System-Manifests/resource-layer/resources.json'), 'utf8')
);
const linksJson = JSON.parse(
  readFileSync(resolve(repoRoot, '006_System-Manifests/resource-layer/node-resource-links.json'), 'utf8')
);
(resourceData as any).nodeResourceLinks = linksJson.nodeResourceLinks;

const decisions = JSON.parse(
  readFileSync(resolve(repoRoot, '006_System-Manifests/graph-canonical/stewardship-decisions.json'), 'utf8')
);

const groups = buildDuplicateCandidateGroups(nodes, baseEdges, resourceData, decisions.stewardshipDecisions);

console.log('Rebasing P1 packets...');
const result = rebaseCanonicalP1DecisionPackets(repoRoot, groups, baseEdges, {
  reviewer: 'project_owner_steward',
  dryRun: false,
  apply: true,
}, { nodes, resourceData });

console.log('Rebase result:', result);
