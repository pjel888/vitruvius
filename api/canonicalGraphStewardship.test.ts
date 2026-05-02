import { afterEach, describe, expect, test } from 'bun:test';
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { GraphEdgeLike, GraphNodeLike } from './graph/relationshipVisibility';
import type { ResourceLayerData } from './resourceLayer/types';
import {
  buildDuplicateCandidateGroups,
  canonicalNodeStatus,
  canonicalPreferredSearch,
  approveCanonicalDecision,
  createCanonicalBatch,
  generateCanonicalP1DecisionPackets,
  listCanonicalBatches,
  listCanonicalP1DecisionPackets,
  previewCanonicalDecision,
  previewCanonicalApproval,
  previewCanonicalBatchDecision,
  previewCanonicalRollback,
  readCanonicalAdmittedRelationships,
  readCanonicalApprovals,
  readCanonicalDecisions,
  recordCanonicalDecision,
  recordCanonicalBatchDecision,
  rollbackCanonicalDecision,
  listCanonicalRemediationManifests,
  setCanonicalGroupPriority,
  validateCanonicalTransactionManifests,
  validateCanonicalStewardship,
} from './graph/canonicalStewardship';
import api from './index';

const repoRoot = resolve(import.meta.dir, '..');
const tmpDir = resolve(import.meta.dir, '.tmp-canonical-stewardship-test');

afterEach(() => {
  rmSync(tmpDir, { recursive: true, force: true });
});

function node(id: string, label: string, taxonomy = 'MAT.CON', type = 'concept'): GraphNodeLike {
  return {
    id,
    label,
    displayLabel: label,
    type,
    aliases: [],
    taxonomy_path: taxonomy.split('.'),
  };
}

function resourceData(nodeId = 'concrete-a'): ResourceLayerData {
  return {
    schemaVersion: 'vitruvius-resource-layer/v1',
    resources: [],
    sourceFamilies: [],
    resourceChecks: [],
    resourceCandidates: [],
    nodeResourceLinks: [{
      id: 'nrl-test',
      nodeId,
      resourceId: 'res-test',
      relationship: 'explains',
      relevanceScore: 0.8,
      authorityScore: 0.8,
      confidenceScore: 0.8,
      rationale: 'Fixture resource link to preserve during canonical preview.',
      reviewStatus: 'accepted',
      createdAt: '2026-05-01T00:00:00.000Z',
      updatedAt: '2026-05-01T00:00:00.000Z',
    }],
  } as ResourceLayerData;
}

describe('canonical graph stewardship service', () => {
  test('detects exact/case duplicate labels and categorizes different taxonomy as unsafe for auto-merge', () => {
    const groups = buildDuplicateCandidateGroups([
      node('concrete-a', 'Concrete', 'MAT.CON'),
      node('concrete-b', 'concrete', 'STR.CON'),
      node('beam', 'Beam', 'STR.BEAM'),
    ], [], resourceData('concrete-a'));

    const concrete = groups.find((group) => group.looseNormalizedLabel === 'concrete');
    expect(concrete).toBeTruthy();
    expect(concrete?.nodeIds.sort()).toEqual(['concrete-a', 'concrete-b']);
    expect(concrete?.riskLevel).not.toBe('low');
    expect(concrete?.suggestedAction).toBe('NEEDS_HUMAN_REVIEW');
  });

  test('dry-run merge previews edge rewrites, resource link rewrites, duplicate edges, and self-loop risks without writing', () => {
    const nodes = [node('concrete-a', 'Concrete'), node('concrete-b', 'concrete'), node('slab', 'Slab', 'STR.SLAB')];
    const edges: GraphEdgeLike[] = [
      { id: 'edge-a', source: 'concrete-b', target: 'slab', type: 'MATERIAL_OF' },
      { id: 'edge-b', source: 'concrete-a', target: 'slab', type: 'MATERIAL_OF' },
      { id: 'edge-c', source: 'concrete-a', target: 'concrete-b', type: 'RELATED_TO' },
    ];
    const groups = buildDuplicateCandidateGroups(nodes, edges, resourceData('concrete-b'));
    const preview = previewCanonicalDecision(groups[0], {
      decisionType: 'MERGE_INTO_CANONICAL',
      canonicalNodeId: 'concrete-a',
      reviewer: 'test',
      rationale: 'Dry-run only.',
    }, edges, resourceData('concrete-b').nodeResourceLinks);

    expect(preview.affectedEdgeIds.sort()).toEqual(['edge-a', 'edge-c']);
    expect(preview.affectedResourceLinkIds).toEqual(['nrl-test']);
    expect(preview.duplicateEdgeConsolidations).toContain('edge-a');
    expect(preview.selfLoopRisks).toContain('edge-c');
    expect(existsSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical'))).toBe(false);
  });

  test('prioritizes concrete duplicate groups as P0 and supports non-destructive batch review', () => {
    mkdirSync(tmpDir, { recursive: true });
    const groups = buildDuplicateCandidateGroups([
      node('concrete-a', 'Concrete', 'MAT.CON', 'topic'),
      node('concrete-b', 'concrete', 'STR.CON', 'subtopic'),
      node('wall-a', 'Wall', 'ARC.WALL'),
      node('wall-b', 'wall', 'STR.WALL'),
    ], [], undefined);
    const concrete = groups.find((group) => group.looseNormalizedLabel === 'concrete');
    expect(concrete?.priorityBand).toBe('P0');

    const created = createCanonicalBatch(tmpDir, groups.filter((group) => group.priorityBand === 'P0'), {
      name: 'P0 concrete stewardship',
      reviewer: 'batch-reviewer',
      priorityBand: 'P0',
      tags: ['concrete'],
    }) as any;
    expect(created.batch.stats.destructiveActionsBlocked).toBe(true);
    expect(listCanonicalBatches(tmpDir, groups)[0].groupIds).toEqual([concrete?.groupId]);

    const preview = previewCanonicalBatchDecision(created.batch, groups, {
      action: 'MERGE_INTO_CANONICAL',
      reviewer: 'batch-reviewer',
      rationale: 'Attempt batch merge should be blocked.',
    });
    expect(preview.blockers.some((blocker) => blocker.includes('unsupported or destructive'))).toBe(true);

    const decision = recordCanonicalBatchDecision(tmpDir, created.batch.batchId, groups, {
      action: 'assign_reviewer',
      reviewer: 'batch-reviewer',
      rationale: 'Assign P0 batch without canonical mutation.',
      apply: true,
    }) as any;
    expect(decision.batchDecision.applied).toBe(true);
  });

  test('applies alias decisions as alias records without tombstoning the original node', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [node('concrete-a', 'Concrete'), node('concrete-b', 'concrete')];
    const groups = buildDuplicateCandidateGroups(nodes, [], resourceData('concrete-b'));
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'ALIAS_TO_CANONICAL',
      canonicalNodeId: 'concrete-a',
      reviewer: 'test-reviewer',
      rationale: 'Alias-only fixture; keep original node available.',
      apply: true,
    }, [], resourceData('concrete-b').nodeResourceLinks) as any;

    expect(result.decision.status).toBe('applied');
    expect(result.manifest.validationStatus).toBe('passed');
    expect(canonicalNodeStatus(tmpDir, 'concrete-b', groups).status).toBe('alias_of');
    expect(canonicalPreferredSearch(tmpDir, nodes, 'concrete', groups, 2)[0].id).toBe('concrete-a');
    const manifests = readdirSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'transaction-manifests'));
    expect(manifests.length).toBe(1);
    expect(result.manifest.manifestHash).toBeTruthy();
  });

  test('rolls back alias decisions and keeps manifest hash chain valid', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [node('alias-a', 'Alias Target'), node('alias-b', 'alias target')];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'ALIAS_TO_CANONICAL',
      canonicalNodeId: 'alias-a',
      reviewer: 'test-reviewer',
      rationale: 'Alias-only fixture for rollback.',
      apply: true,
    }, [], []) as any;

    const preview = previewCanonicalRollback(tmpDir, result.decision.decisionId) as any;
    expect(preview.rollbackCapability).toBe('full');
    const rollback = rollbackCanonicalDecision(tmpDir, result.decision.decisionId, {
      reviewer: 'test-reviewer',
      rationale: 'Rollback alias fixture.',
      apply: true,
    }) as any;
    expect(rollback.rollback.rollbackCapability).toBe('full');
    expect(canonicalNodeStatus(tmpDir, 'alias-b', groups).status).not.toBe('alias_of');
    const manifestValidation = validateCanonicalTransactionManifests(tmpDir);
    expect(manifestValidation.invalidManifestCount).toBe(0);
    expect(manifestValidation.brokenHashChainCount).toBe(0);
  });

  test('detects tampered canonical transaction manifests', () => {
    mkdirSync(tmpDir, { recursive: true });
    const groups = buildDuplicateCandidateGroups([node('keep-a', 'Keep'), node('keep-b', 'keep')], [], undefined);
    recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Create a manifest to tamper with.',
      apply: true,
    }, [], []);
    const manifestPath = resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'transaction-manifests', readdirSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'transaction-manifests'))[0]);
    const parsed = JSON.parse(readFileSync(manifestPath, 'utf-8'));
    parsed.operationType = 'tampered';
    writeFileSync(manifestPath, `${JSON.stringify(parsed, null, 2)}\n`);
    expect(validateCanonicalTransactionManifests(tmpDir).invalidManifestCount).toBe(1);
  });

  test('records keep-separate decisions with rationale and no graph mutation redirects', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [node('wall-a', 'Wall', 'ARC.WALL'), node('wall-b', 'wall', 'STR.WALL')];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Architectural wall and structural wall remain separately scoped.',
      apply: true,
    }, [], []) as any;

    expect(result.decision.status).toBe('applied');
    const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.ok).toBe(true);
    expect(validation.redirects).toBe(0);
  });

  test('records manual priority overrides without applying canonical aliases or redirects', () => {
    mkdirSync(tmpDir, { recursive: true });
    const groups = buildDuplicateCandidateGroups([node('roof-a', 'Roof'), node('roof-b', 'roof')], [], undefined);
    const result = setCanonicalGroupPriority(tmpDir, groups[0].groupId, {
      priorityBand: 'P1',
      reviewer: 'test-reviewer',
      owner: 'domain-steward',
      tags: ['envelope'],
      notes: 'Prioritize roof duplicate review.',
    }) as any;
    expect(result.priority.priorityBand).toBe('P1');
    const validation = validateCanonicalStewardship(tmpDir, [node('roof-a', 'Roof'), node('roof-b', 'roof')], [], undefined);
    expect(validation.aliases).toBe(0);
    expect(validation.redirects).toBe(0);
  });

  test('records proposed decisions without applying aliases or redirects when apply is false', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [node('door-a', 'Door', 'ARC.DOOR'), node('door-b', 'door', 'BIM.DOOR')];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'NEEDS_HUMAN_REVIEW',
      reviewer: 'test-reviewer',
      rationale: 'Record a proposed queue decision without canonical mutation.',
      apply: false,
      dryRun: false,
    }, [], []) as any;

    expect(result.decision.status).toBe('proposed');
    const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.ok).toBe(true);
    expect(validation.stewardshipDecisions).toBe(1);
    expect(validation.aliases).toBe(0);
    expect(validation.redirects).toBe(0);
  });

  test('previews and records governed disambiguation without destructive canonical mutation', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('concrete-material', 'Concrete', 'MAT.CON', 'topic'),
      node('concrete-structural', 'Concrete', 'STR.MAT.CON', 'subtopic'),
    ];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const preview = previewCanonicalDecision(groups[0], {
      decisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Concrete material and structural-material concrete remain separate but related.',
      dryRun: true,
    }, [], []) as any;

    expect(preview.proposedRelationshipAdds).toHaveLength(1);
    expect(preview.proposedRelationshipAdds[0].relationType).toBe('RELATED_SPECIALIZATION_OF');
    expect(preview.proposedRelationshipAdds[0].sourceNodeId).toBe('concrete-structural');
    expect(preview.proposedRelationshipAdds[0].targetNodeId).toBe('concrete-material');

    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Concrete material and structural-material concrete remain separate but related.',
      apply: false,
    }, [], []) as any;
    expect(result.decision.status).toBe('proposed');
    expect(result.decision.proposedRelationshipAdds[0].stewardshipDecisionId).toBe(result.decision.decisionId);
    const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.ok).toBe(true);
    expect(validation.graphStewardshipEdgeProposals).toBe(1);
    expect(validation.disambiguatedKeepSeparateDecisions).toBe(1);
    expect(validation.aliases).toBe(0);
    expect(validation.redirects).toBe(0);
  });

  test('requires steward approval gate before applying disambiguation decisions', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('concrete-material', 'Concrete', 'MAT.CON', 'topic'),
      node('concrete-structural', 'Concrete', 'STR.MAT.CON', 'subtopic'),
    ];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Do not let direct apply bypass steward approval.',
      apply: true,
    }, [], []) as any;

    expect(result.blockers.join(' ')).toContain('steward approval/admission gate');
    expect(readCanonicalDecisions(tmpDir)).toHaveLength(0);
  });

  test('canonical search surfaces proposed concrete disambiguation metadata without claiming approval', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('concrete-material', 'Concrete', 'MAT.CON', 'topic'),
      node('concrete-structural', 'Concrete', 'STR.MAT.CON', 'subtopic'),
    ];
    let groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'GOVERNED_DISAMBIGUATION',
      reviewer: 'test-reviewer',
      rationale: 'Propose governed disambiguation only.',
      searchDisambiguationText: 'Concrete has material and structural-material review contexts.',
      apply: false,
    }, [], []);
    groups = buildDuplicateCandidateGroups(nodes, [], undefined, readCanonicalDecisions(tmpDir));
    const results = canonicalPreferredSearch(tmpDir, nodes, 'concrete', groups, 5) as any[];
    expect(results[0].reviewState).toBe('proposed_disambiguation');
    expect(results[0].canonicalStatus).toBe('unresolved_duplicate_candidate');
    expect(results[0].disambiguationText).toContain('Concrete has material');
  });

  test('approval gate blocks admission without required steward metadata and admits non-destructive fixture edges with rollback/replay', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('fixture-concrete-material', 'Concrete', 'MAT.CON', 'topic'),
      node('fixture-concrete-structural', 'Concrete', 'STR.MAT.CON', 'subtopic'),
    ];
    let groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const proposed = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
      reviewer: 'test-reviewer',
      rationale: 'Fixture material concrete and structural-material concrete remain separate but related.',
      apply: false,
    }, [], []) as any;

    const blocked = previewCanonicalApproval(tmpDir, proposed.decision.decisionId, {
      mutationScope: 'non_destructive_edge_admission',
    }, nodes, [], undefined) as any;
    expect(blocked.blockers).toContain('approvedBy is required');
    expect(blocked.blockers).toContain('approvalRationale is required');

    const approval = approveCanonicalDecision(tmpDir, proposed.decision.decisionId, {
      approvedBy: 'fixture-steward',
      reviewerRole: 'test-steward',
      approvalSource: 'api',
      approvalRationale: 'Approve non-destructive disambiguation edge for rollback/replay fixture.',
      riskAcknowledgment: true,
      mutationScope: 'non_destructive_edge_admission',
      rollbackPlan: 'Rollback by decisionId marks admitted relationships and approval rolled_back.',
      apply: true,
    }, nodes, [], undefined) as any;
    expect(approval.approval.status).toBe('admitted');
    expect(approval.admittedRelationships).toHaveLength(1);
    expect(readCanonicalApprovals(tmpDir)).toHaveLength(1);
    expect(readCanonicalAdmittedRelationships(tmpDir).filter((edge) => edge.reviewStatus !== 'rolled_back')).toHaveLength(1);
    let validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.ok).toBe(true);
    expect(validation.approvals).toBe(1);
    expect(validation.admittedRelationships).toBe(1);

    const rollback = rollbackCanonicalDecision(tmpDir, proposed.decision.decisionId, {
      reviewer: 'fixture-steward',
      rationale: 'Rollback non-destructive admission fixture.',
      apply: true,
    }) as any;
    expect(rollback.rollback.rollbackCapability).toBe('full');
    expect(readCanonicalAdmittedRelationships(tmpDir).filter((edge) => edge.reviewStatus !== 'rolled_back')).toHaveLength(0);
    validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.ok).toBe(true);

    const replay = approveCanonicalDecision(tmpDir, proposed.decision.decisionId, {
      approvedBy: 'fixture-steward',
      reviewerRole: 'test-steward',
      approvalSource: 'api',
      approvalRationale: 'Replay non-destructive admission after rollback drill.',
      riskAcknowledgment: true,
      mutationScope: 'non_destructive_edge_admission',
      rollbackPlan: 'Rollback by decisionId marks replayed relationship rolled_back.',
      apply: true,
    }, nodes, [], undefined) as any;
    expect(replay.admittedRelationships).toHaveLength(1);
    expect(readCanonicalApprovals(tmpDir).length).toBe(2);
    expect(readCanonicalAdmittedRelationships(tmpDir).length).toBe(2);
    expect(readCanonicalAdmittedRelationships(tmpDir).filter((edge) => edge.reviewStatus !== 'rolled_back')).toHaveLength(1);
    expect(validateCanonicalStewardship(tmpDir, nodes, [], undefined).ok).toBe(true);
  });

  test('cross-domain equivalent proposals are normalized to CROSS_DOMAIN_ALIGNMENT before admission', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('fixture-rc-structural', 'Reinforced concrete', 'STR.SYS.RC', 'topic'),
      node('fixture-rc-architecture', 'Reinforced Concrete', 'ARC.MAT.RC', 'topic'),
    ];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const proposed = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'CROSS_DOMAIN_EQUIVALENCE',
      reviewer: 'test-reviewer',
      rationale: 'Fixture cross-domain proposal should use safer alignment wording at admission.',
      apply: false,
    }, [], []) as any;
    expect(proposed.decision.proposedRelationshipAdds[0].relationType).toBe('CROSS_DOMAIN_ALIGNMENT');

    const preview = previewCanonicalApproval(tmpDir, proposed.decision.decisionId, {
      approvedBy: 'fixture-steward',
      reviewerRole: 'test-steward',
      approvalSource: 'api',
      approvalRationale: 'Approve alignment fixture.',
      riskAcknowledgment: true,
      mutationScope: 'non_destructive_edge_admission',
      rollbackPlan: 'Rollback by decisionId.',
    }, nodes, [], undefined) as any;
    expect(preview.approvalPreview.admittedRelationshipPreview.every((edge: any) => edge.type === 'CROSS_DOMAIN_ALIGNMENT')).toBe(true);
    expect(preview.approvalPreview.admittedRelationshipPreview).toHaveLength(2);
  });

  test('generates P1 decision packets without destructive actions', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('wall-a', 'Wall', 'ARC.WALL', 'topic'),
      node('wall-b', 'wall', 'STR.WALL', 'subtopic'),
      node('beam-a', 'Beam', 'STR.BEAM', 'topic'),
      node('beam-b', 'beam', 'ARC.BEAM', 'topic'),
    ];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined).filter((group) => group.priorityBand !== 'P0');
    const result = generateCanonicalP1DecisionPackets(tmpDir, groups.map((group) => ({ ...group, priorityBand: 'P1' as const })), [], {
      reviewer: 'packet-reviewer',
      limit: 2,
      apply: true,
    }, { nodes }) as any;
    expect(result.packets.length).toBeGreaterThan(0);
    expect(result.packets.every((packet: any) => packet.recommendedDecisionType !== 'MERGE_INTO_CANONICAL')).toBe(true);
    expect(result.packets.every((packet: any) => packet.sourceSnapshot?.snapshotHash)).toBe(true);
    expect(result.packets.every((packet: any) => packet.packetContentHash && packet.groupInputHash && packet.truthCaveat)).toBe(true);
    expect(result.packets[0].sourceSnapshot.graphNodeCount).toBe(nodes.length);
    expect(result.packets[0].sourceSnapshot.graphEdgeCount).toBe(0);
    expect(listCanonicalP1DecisionPackets(tmpDir).length).toBe(result.packets.length);
    const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(validation.p1DecisionPackets).toBe(result.packets.length);
    expect(validation.p1PacketsMissingSourceSnapshot).toBe(0);
    expect(validation.p1PacketsTamperedSourceSnapshot).toBe(0);
    expect(validation.ok).toBe(true);

    const packetPath = resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'p1-decision-packets.json');
    const payload = JSON.parse(readFileSync(packetPath, 'utf-8'));
    payload.packets[0].sourceSnapshot.graphNodeCount += 1;
    writeFileSync(packetPath, JSON.stringify(payload, null, 2));
    const tamperedValidation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(tamperedValidation.ok).toBe(false);
    expect(tamperedValidation.p1PacketsTamperedSourceSnapshot).toBe(1);

    payload.packets[0].sourceSnapshot.graphNodeCount -= 1;
    payload.packets[0].normalizedLabel = 'tampered label';
    writeFileSync(packetPath, JSON.stringify(payload, null, 2));
    const packetTamperValidation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
    expect(packetTamperValidation.ok).toBe(false);
    expect(packetTamperValidation.blockers.some((blocker: string) => blocker.includes('packetContentHash mismatch'))).toBe(true);
  });

  test('validates alias, redirect, and tombstone safety rules', () => {
    mkdirSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical'), { recursive: true });
    writeFileSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'aliases.json'), JSON.stringify({
      aliases: [{ alias: 'ghost', normalizedAlias: 'ghost', canonicalNodeId: 'missing-node', sourceNodeIds: [], decisionId: 'd1', createdAt: '2026-05-01T00:00:00.000Z' }],
    }, null, 2));
    writeFileSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'redirects.json'), JSON.stringify({
      redirects: [
        { sourceNodeId: 'a', canonicalNodeId: 'b', decisionId: 'd1', createdAt: '2026-05-01T00:00:00.000Z', reason: 'fixture' },
        { sourceNodeId: 'b', canonicalNodeId: 'a', decisionId: 'd2', createdAt: '2026-05-01T00:00:00.000Z', reason: 'fixture' },
      ],
    }, null, 2));
    writeFileSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'tombstones.json'), JSON.stringify({
      tombstones: [{ nodeId: 'a', tombstoneStatus: 'deprecated', decisionId: 'd3', createdAt: '2026-05-01T00:00:00.000Z', reason: '' }],
    }, null, 2));
    const validation = validateCanonicalStewardship(tmpDir, [node('a', 'A'), node('b', 'B')], [], undefined);
    expect(validation.ok).toBe(false);
    expect(validation.blockers.some((blocker) => blocker.includes('missing canonical node'))).toBe(true);
    expect(validation.redirectCycles).toBeGreaterThan(0);
    expect(validation.tombstonePolicyViolations).toBeGreaterThan(0);
  });

  test('partial merge rollback creates an open remediation manifest', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [node('safe-a', 'Safe'), node('safe-b', 'safe'), node('slab', 'Slab')];
    const edges: GraphEdgeLike[] = [{ id: 'safe-edge', source: 'safe-b', target: 'slab', type: 'MATERIAL_OF' }];
    const groups = buildDuplicateCandidateGroups(nodes, edges, resourceData('safe-b'));
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'MERGE_INTO_CANONICAL',
      canonicalNodeId: 'safe-a',
      reviewer: 'test-reviewer',
      rationale: 'Low-risk fixture merge to exercise partial rollback remediation.',
      apply: true,
    }, edges, resourceData('safe-b').nodeResourceLinks) as any;
    expect(result.decision.rollbackCapability).toBe('partial');
    const rollback = rollbackCanonicalDecision(tmpDir, result.decision.decisionId, {
      reviewer: 'test-reviewer',
      rationale: 'Rollback partial merge fixture and create remediation.',
      apply: true,
    }) as any;
    expect(rollback.remediation.remediationManifestId).toBeTruthy();
    expect(listCanonicalRemediationManifests(tmpDir)).toHaveLength(1);
    const validation = validateCanonicalStewardship(tmpDir, nodes, edges, resourceData('safe-b'));
    expect(validation.ok).toBe(true);
    expect(validation.openRemediationManifests).toBe(1);
  });

  test('blocks unsafe production-style destructive merge unless low risk and explicitly safe', () => {
    mkdirSync(tmpDir, { recursive: true });
    const nodes = [
      node('building-concept', 'Building', 'ARC.BLDG', 'concept'),
      node('building-project', 'building', 'FIG.WORK', 'document'),
    ];
    const groups = buildDuplicateCandidateGroups(nodes, [], undefined);
    const result = recordCanonicalDecision(tmpDir, groups[0], {
      decisionType: 'MERGE_INTO_CANONICAL',
      canonicalNodeId: 'building-concept',
      reviewer: 'test-reviewer',
      rationale: 'Attempt unsafe merge.',
      apply: true,
      highRiskAcknowledged: true,
    }, [], []) as any;

    expect(result.blockers.some((blocker: string) => blocker.includes('destructive merge apply is blocked'))).toBe(true);
    expect(existsSync(resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'redirects.json'))).toBe(false);
  });
});

describe('canonical stewardship API regressions', () => {
  test('serves concrete duplicate groups without mutating production graph data', async () => {
    const response = await api.fetch(new Request('http://localhost/graph/canonical/duplicates?concreteOnly=true&limit=25'));
    expect(response.status).toBe(200);
    const body = await response.json();
    const nodeIds = body.groups.flatMap((group: any) => group.nodeIds);
    expect(nodeIds).toContain('VTN-DOM-0000068');
    expect(nodeIds).toContain('VTN-DOM-0000267');
    expect(nodeIds).toContain('VTN-DOM-0000271');
    expect(nodeIds).toContain('VTN-DOM-0012147');
  });

  test('keeps Sendai Mediatheque / Toyo Ito selected-node relationship visible', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012495/neighborhood?depth=1&direction=both'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.nodes.some((node: any) => node.id === 'VTN-DOM-0012436')).toBe(true);
    expect(body.edges.some((edge: any) => edge.id === 'VTN-DOM-0012436--has_facet--VTN-DOM-0012495')).toBe(true);
  });

  test('serves priority queue and read-only batch list without requiring admin mutation token', async () => {
    const priorityResponse = await api.fetch(new Request('http://localhost/graph/canonical/priorities?concreteOnly=true&limit=10'));
    expect(priorityResponse.status).toBe(200);
    const priorityBody = await priorityResponse.json();
    expect(priorityBody.priorities.some((group: any) => group.priorityBand === 'P0')).toBe(true);

    const batchResponse = await api.fetch(new Request('http://localhost/graph/canonical/batches'));
    expect(batchResponse.status).toBe(200);
  });

  test('blocks production canonical mutation routes without admin token but allows token to reach route validation', async () => {
    const previousNodeEnv = process.env.NODE_ENV;
    const previousToken = process.env.VITRUVIUS_ADMIN_TOKEN;
    const previousDevAdmin = process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    process.env.NODE_ENV = 'production';
    delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    process.env.VITRUVIUS_ADMIN_TOKEN = 'secret-test-token';
    try {
      const blocked = await api.fetch(new Request('http://example.com/graph/canonical/duplicates/fake/decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decisionType: 'NEEDS_HUMAN_REVIEW', reviewer: 'test', rationale: 'gate test' }),
      }));
      expect(blocked.status).toBe(403);

      const allowedPastGate = await api.fetch(new Request('http://example.com/graph/canonical/duplicates/fake/decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-vitruvius-admin-token': 'secret-test-token' },
        body: JSON.stringify({ decisionType: 'NEEDS_HUMAN_REVIEW', reviewer: 'test', rationale: 'gate test' }),
      }));
      expect(allowedPastGate.status).toBe(404);
    } finally {
      if (previousNodeEnv === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = previousNodeEnv;
      if (previousToken === undefined) delete process.env.VITRUVIUS_ADMIN_TOKEN; else process.env.VITRUVIUS_ADMIN_TOKEN = previousToken;
      if (previousDevAdmin === undefined) delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN; else process.env.VITRUVIUS_ENABLE_DEV_ADMIN = previousDevAdmin;
    }
  });
});
