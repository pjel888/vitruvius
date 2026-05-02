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
      expect(review.packetContentHash).toBe(packet.packetContentHash);
      expect(review.sourceSnapshotHash).toBe(packet.sourceSnapshot.snapshotHash);
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

  test('proposed future edge IDs are not present in the production graph', () => {
    const graph = json('006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json');
    const edgeIds = new Set(graph.edges.map((edge: any) => edge.id));

    for (const candidate of mediumRiskCandidates) {
      for (const edgeId of candidate.proposedEdgeIds) {
        expect(edgeIds.has(edgeId)).toBe(false);
      }
    }
  });

  test('no approval, admitted relationship, alias, redirect, tombstone, or Resource Layer link mutation is encoded by the packet', () => {
    const canonicalRoot = '006_System-Manifests/graph-canonical';
    const emptyRegistries = [
      'approvals.json',
      'admitted-relationships.json',
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
