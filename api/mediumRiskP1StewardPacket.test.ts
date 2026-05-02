import { describe, expect, test } from 'bun:test';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repoRoot = resolve(import.meta.dir, '..');

function text(path: string) {
  return readFileSync(resolve(repoRoot, path), 'utf8').replace(/^\uFEFF/, '');
}

function json(path: string) {
  return JSON.parse(text(path));
}

const mediumRiskCandidates = [
  {
    label: 'Buildings',
    packetId: 'p1-decision-packet-fee6fbd9a0fc',
    groupId: 'dup-ca1078594013',
    nodeIds: ['VTN-DOM-0000716', 'VTN-DOM-0000757'],
    proposedEdgeIds: [
      'VTN-DOM-0000716--disambiguated_from--VTN-DOM-0000757',
      'VTN-DOM-0000757--disambiguated_from--VTN-DOM-0000716',
    ],
    relationType: 'DISAMBIGUATED_FROM',
    admitted: false,
  },
  {
    label: 'Shallow Foundations',
    packetId: 'p1-decision-packet-d5a20759fdfd',
    groupId: 'dup-6400e3e0c204',
    nodeIds: ['VTN-DOM-0000261', 'VTN-DOM-0003010'],
    proposedEdgeIds: [
      'VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010',
      'VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261',
    ],
    relationType: 'CROSS_DOMAIN_ALIGNMENT',
    admitted: true,
  },
  {
    label: 'Deep Foundations',
    packetId: 'p1-decision-packet-8a66e785d02a',
    groupId: 'dup-5c6457d515c1',
    nodeIds: ['VTN-DOM-0000262', 'VTN-DOM-0003013'],
    proposedEdgeIds: [
      'VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013',
      'VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262',
    ],
    relationType: 'CROSS_DOMAIN_ALIGNMENT',
    admitted: true,
  },
];

describe('medium-risk P1 steward packet', () => {
  test('references existing reviewed P1 packets and current packet hashes', () => {
    const packets = json('006_System-Manifests/graph-canonical/p1-decision-packets.json').packets;
    const reviews = json('006_System-Manifests/graph-canonical/p1-packet-reviews.json').reviews;

    for (const candidate of mediumRiskCandidates) {
      const packet = packets.find((item: any) => item.packetId === candidate.packetId);
      const review = reviews.find((item: any) => item.packetId === candidate.packetId);

      expect(packet).toBeTruthy();
      expect(review).toBeTruthy();
      expect(packet.groupId).toBe(candidate.groupId);
      expect(review.groupId).toBe(candidate.groupId);
      expect(packet.nodeIds).toEqual(candidate.nodeIds);
      expect(review.packetContentHash).toBe(packet.previousPacketContentHash);
      expect(review.sourceSnapshotHash).toBe(packet.previousSourceSnapshotHash);
      expect(review.carriedForwardFromPacketContentHash).toBe(packet.previousPacketContentHash);
      expect(review.carriedForwardFromSourceSnapshotHash).toBe(packet.previousSourceSnapshotHash);
      expect(review.carriedForwardToPacketContentHash).toBe(packet.packetContentHash);
      expect(review.carriedForwardToSourceSnapshotHash).toBe(packet.sourceSnapshot.snapshotHash);
      expect(review.carriedForwardAt).toBeTruthy();
      expect(review.carryForwardCaveat).toContain('not a new Kimi or human review');
      expect(review.graphMutationApplied).toBe(false);
      expect(review.advisoryOnly).toBe(true);
    }
  });

  test('packet and preview are explicitly advisory and non-mutating', () => {
    const packet = text('.ai/13_research/medium_risk_p1_steward_review_packet.md');
    const preview = text('.ai/13_research/medium_risk_p1_admission_preview_report.md');
    const kimi = text('.ai/13_research/medium_risk_p1_steward_packet_kimi_review.md');

    for (const candidate of mediumRiskCandidates) {
      expect(packet).toContain(candidate.packetId);
      expect(packet).toContain(candidate.groupId);
      expect(preview).toContain(candidate.packetId);
      expect(preview).toContain(candidate.relationType);
      for (const nodeId of candidate.nodeIds) {
        expect(packet).toContain(nodeId);
        expect(preview).toContain(nodeId);
      }
    }

    expect(packet).toContain('not steward approval');
    expect(packet).toContain('No production graph node or edge is changed by this file');
    expect(preview).toContain('performs no mutation and creates no approval');
    expect(kimi).toContain('This is not approval for graph mutation/admission');
    expect(preview).not.toMatch(/Proposed future relation type: `CROSS_DOMAIN_EQUIVALENT`/);
    expect(packet).not.toMatch(/Decision:\s*`MERGE|Decision:\s*`ALIAS_TO_CANONICAL/);
  });

  test('foundation alignment edge IDs are admitted through the stewardship overlay only', () => {
    const graph = json('006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json');
    const baseEdgeIds = new Set(graph.edges.map((edge: any) => edge.id));
    const admitted = json('006_System-Manifests/graph-canonical/admitted-relationships.json').admittedRelationships;
    const admittedEdgeIds = new Set(admitted.filter((edge: any) => edge.reviewStatus !== 'rolled_back').map((edge: any) => edge.id));

    for (const candidate of mediumRiskCandidates) {
      for (const edgeId of candidate.proposedEdgeIds) {
        expect(baseEdgeIds.has(edgeId)).toBe(false);
        expect(admittedEdgeIds.has(edgeId)).toBe(candidate.admitted);
      }
    }

    expect(admitted.every((edge: any) => edge.type !== 'CROSS_DOMAIN_EQUIVALENT')).toBe(true);
    expect(admitted.filter((edge: any) => edge.type === 'CROSS_DOMAIN_ALIGNMENT' && edge.reviewStatus !== 'rolled_back')).toHaveLength(4);
  });

  test('approvals are scoped and no alias, redirect, tombstone, or Resource Layer link mutation occurred', () => {
    const canonicalRoot = '006_System-Manifests/graph-canonical';
    const approvals = json(`${canonicalRoot}/approvals.json`).approvals;
    const admitted = json(`${canonicalRoot}/admitted-relationships.json`).admittedRelationships;
    const scopedGroups = new Set(mediumRiskCandidates.map((candidate) => candidate.groupId));
    const scopedApprovals = approvals.filter((approval: any) => scopedGroups.has(approval.groupId));
    const activeAdmitted = admitted.filter((edge: any) => edge.reviewStatus !== 'rolled_back');

    expect(scopedApprovals).toHaveLength(3);
    expect(scopedApprovals.every((approval: any) => approval.approvedBy === 'project_owner_steward')).toBe(true);
    expect(scopedApprovals.every((approval: any) => approval.approvalSource === 'user_supplied_standing_steward_approval')).toBe(true);
    expect(scopedApprovals.filter((approval: any) => approval.mutationScope === 'non_destructive_edge_admission')).toHaveLength(2);
    expect(scopedApprovals.filter((approval: any) => approval.mutationScope === 'metadata_only')).toHaveLength(1);
    expect(JSON.stringify(scopedApprovals)).not.toContain('"ok":false');
    expect(activeAdmitted).toHaveLength(4);
    const decisions = json(`${canonicalRoot}/stewardship-decisions.json`).stewardshipDecisions;
    const buildings = decisions.find((decision: any) => decision.decisionId === 'canonical-20260502055700-8e92ff2fc366');
    expect(buildings.proposedRelationshipAdds).toEqual([]);

    const emptyRegistries = [
      'aliases.json',
      'redirects.json',
      'tombstones.json',
    ];

    for (const registry of emptyRegistries) {
      const path = `${canonicalRoot}/${registry}`;
      if (!existsSync(resolve(repoRoot, path))) continue;
      const data = json(path);
      const values = Array.isArray(data) ? data : Object.values(data).flat();
      expect(values.length).toBe(0);
    }

    const linksData = json('006_System-Manifests/resource-layer/node-resource-links.json');
    const links = Array.isArray(linksData) ? linksData : linksData.links ?? linksData.nodeResourceLinks ?? [];
    expect(links).toHaveLength(9);
    for (const candidate of mediumRiskCandidates) {
      for (const nodeId of candidate.nodeIds) {
        expect(links.filter((link: any) => link.nodeId === nodeId)).toHaveLength(0);
      }
    }
  });
});
