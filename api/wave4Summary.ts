import { readCanonicalAdmittedRelationships, readCanonicalDecisions, readCanonicalApprovals } from './graph/canonicalStewardship';
import { resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');
const edges = readCanonicalAdmittedRelationships(repoRoot).filter(e => e.reviewStatus !== 'rolled_back');

const byType: Record<string, number> = {};
for (const e of edges) {
  byType[e.type] = (byType[e.type] || 0) + 1;
}

const decisions = readCanonicalDecisions(repoRoot);
const approvals = readCanonicalApprovals(repoRoot);
const latestDecision = decisions[decisions.length - 1];
const latestApproval = approvals[approvals.length - 1];

const wave4Edges = edges.filter(e => e.stewardshipDecisionId === 'canonical-20260502175718-8917915ab454');

console.log(JSON.stringify({
  totalActive: edges.length,
  byType,
  latestDecisionId: latestDecision?.decisionId,
  latestApprovalId: latestApproval?.approvalId,
  wave4Count: wave4Edges.length,
  wave4Edges: wave4Edges.map(e => ({
    id: e.id,
    source: e.source,
    target: e.target,
    type: e.type,
    rationale: e.rationale,
  })),
}, null, 2));
