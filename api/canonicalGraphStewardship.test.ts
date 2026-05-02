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
  getCanonicalP1PacketDetail,
  listCanonicalBatches,
  listCanonicalP1DecisionPackets,
  listCanonicalP1PacketsWithReviews,
  previewCanonicalDecision,
  previewCanonicalApproval,
  previewCanonicalBatchDecision,
  previewCanonicalP1PacketReview,
  previewCanonicalRollback,
  readCanonicalAdmittedRelationships,
  readCanonicalApprovals,
  readCanonicalDecisions,
  readCanonicalP1PacketReviews,
  recordCanonicalDecision,
  recordCanonicalBatchDecision,
  recordCanonicalP1PacketReview,
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

function withEnv<T>(updates: Record<string, string | undefined>, fn: () => T): T {
  const previous: Record<string, string | undefined> = {};
  for (const key of Object.keys(updates)) {
    previous[key] = process.env[key];
    const value = updates[key];
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
  try {
    return fn();
  } finally {
    for (const key of Object.keys(previous)) {
      const value = previous[key];
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
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
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: undefined, VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_PACKET_SIGNATURES: undefined }, () => {
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
      expect(result.packets.every((packet: any) => packet.signature?.signatureStatus === 'unsigned')).toBe(true);
      expect(result.packets[0].sourceSnapshot.graphNodeCount).toBe(nodes.length);
      expect(result.packets[0].sourceSnapshot.graphEdgeCount).toBe(0);
      expect(listCanonicalP1DecisionPackets(tmpDir).length).toBe(result.packets.length);
      const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(validation.p1DecisionPackets).toBe(result.packets.length);
      expect(validation.p1PacketsUnsigned).toBe(result.packets.length);
      expect(validation.p1PacketsMissingSourceSnapshot).toBe(0);
      expect(validation.p1PacketsTamperedSourceSnapshot).toBe(0);
      expect(validation.ok).toBe(true);

      const strictValidation = withEnv({ VITRUVIUS_REQUIRE_PACKET_SIGNATURES: 'true' }, () => validateCanonicalStewardship(tmpDir, nodes, [], undefined));
      expect(strictValidation.ok).toBe(false);
      expect(strictValidation.p1PacketsStrictSignatureBlockers).toBe(result.packets.length);

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
  });

  test('signs and validates P1 decision packet evidence locks when HMAC key is configured', () => {
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: 'test-packet-secret', VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_PACKET_SIGNATURES: undefined }, () => {
      mkdirSync(tmpDir, { recursive: true });
      const nodes = [
        node('foundation-a', 'Foundation', 'STR.FND', 'topic'),
        node('foundation-b', 'foundation', 'ARC.FND', 'topic'),
      ];
      const groups = buildDuplicateCandidateGroups(nodes, [], undefined).filter((group) => group.priorityBand !== 'P0');
      const result = generateCanonicalP1DecisionPackets(tmpDir, groups.map((group) => ({ ...group, priorityBand: 'P1' as const })), [], {
        reviewer: 'packet-reviewer',
        limit: 1,
        apply: true,
      }, { nodes }) as any;
      expect(result.packets).toHaveLength(1);
      expect(result.packets[0].signature.signatureStatus).toBe('valid');
      expect(result.packets[0].signature.signature).toBeTruthy();
      expect(JSON.stringify(result.packets)).not.toContain('test-packet-secret');
      const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(validation.ok).toBe(true);
      expect(validation.p1PacketsSigned).toBe(1);
      expect(validation.p1PacketsUnsigned).toBe(0);
      expect(validation.p1PacketsInvalidSignature).toBe(0);

      const packetPath = resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'p1-decision-packets.json');
      const payload = JSON.parse(readFileSync(packetPath, 'utf-8'));
      payload.packets[0].signature.signedBy = 'changed-signer-field';
      writeFileSync(packetPath, JSON.stringify(payload, null, 2));
      expect(validateCanonicalStewardship(tmpDir, nodes, [], undefined).ok).toBe(true);

      payload.packets[0].packetContentHash = 'bad-content-hash';
      writeFileSync(packetPath, JSON.stringify(payload, null, 2));
      const invalid = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(invalid.ok).toBe(false);
      expect(invalid.p1PacketsInvalidSignature).toBe(1);
      expect(invalid.p1PacketsContentHashMismatch).toBe(1);
    });
  });

  test('records advisory P1 packet ontology review metadata without mutating packet custody or graph state', () => {
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: undefined, VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS: undefined }, () => {
      mkdirSync(tmpDir, { recursive: true });
      const nodes = [
        node('atrium-a', 'Atrium', 'ARC.ATRIUM', 'topic'),
        node('atrium-b', 'atrium', 'FLS.ATRIUM', 'topic'),
      ];
      const groups = buildDuplicateCandidateGroups(nodes, [], undefined).filter((group) => group.priorityBand !== 'P0');
      const result = generateCanonicalP1DecisionPackets(tmpDir, groups.map((group) => ({ ...group, priorityBand: 'P1' as const })), [], {
        reviewer: 'packet-reviewer',
        limit: 1,
        apply: true,
      }, { nodes }) as any;
      const packet = result.packets[0];
      const originalContentHash = packet.packetContentHash;
      const originalSnapshotHash = packet.sourceSnapshot.snapshotHash;

      const preview = previewCanonicalP1PacketReview(tmpDir, packet.packetId, {
        ontologyReviewStatus: 'human_review_needed',
        reviewerType: 'human',
        reviewedBy: 'domain-steward',
        reviewSummary: 'Packet identifies ambiguous atrium concepts; no graph mutation is approved.',
        nextAction: 'Human steward should decide keep-separate versus disambiguation.',
        reviewRiskLevel: 'medium',
        acceptedSuggestions: ['Keep advisory only.'],
      }) as any;
      expect(preview.blockers).toEqual([]);
      expect(preview.mutationScope).toBe('p1_packet_review_metadata_only');
      expect(preview.graphMutation).toBe(false);
      expect(readCanonicalP1PacketReviews(tmpDir)).toHaveLength(0);

      const applied = recordCanonicalP1PacketReview(tmpDir, packet.packetId, {
        ontologyReviewStatus: 'human_review_needed',
        reviewerType: 'human',
        reviewedBy: 'domain-steward',
        reviewSummary: 'Packet identifies ambiguous atrium concepts; no graph mutation is approved.',
        nextAction: 'Human steward should decide keep-separate versus disambiguation.',
        reviewRiskLevel: 'medium',
        acceptedSuggestions: ['Keep advisory only.'],
        apply: true,
      }) as any;
      expect(applied.review.graphMutationApplied).toBe(false);
      expect(applied.review.mutationScope).toBe('review_metadata_only');
      expect(applied.manifest.operationType).toBe('canonical_p1_packet_ontology_review');
      expect(readCanonicalP1PacketReviews(tmpDir)).toHaveLength(1);

      const storedPacket = listCanonicalP1DecisionPackets(tmpDir)[0];
      expect(storedPacket.packetContentHash).toBe(originalContentHash);
      expect(storedPacket.sourceSnapshot?.snapshotHash).toBe(originalSnapshotHash);
      const enriched = listCanonicalP1PacketsWithReviews(tmpDir, { ontologyReviewStatus: 'human_review_needed' });
      expect(enriched).toHaveLength(1);
      expect(enriched[0].ontologyReviewStatus).toBe('human_review_needed');
      const detail = getCanonicalP1PacketDetail(tmpDir, packet.packetId) as any;
      expect(detail.custody.packetContentHash).toBe(originalContentHash);
      expect(detail.reviewHistory).toHaveLength(1);

      const validation = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(validation.ok).toBe(true);
      expect(validation.p1PacketsWithOntologyReview).toBe(1);
      expect(validation.p1PacketsHumanReviewNeeded).toBe(1);
      expect(validation.p1PacketReviewTransactionManifests).toBe(1);
      expect(validation.p1PacketReviewDoesNotMutateGraph).toBe(true);
      expect(validation.approvals).toBe(0);
      expect(validation.admittedRelationships).toBe(0);
      expect(validation.aliases).toBe(0);
      expect(validation.redirects).toBe(0);
      expect(validation.tombstones).toBe(0);
    });
  });

  test('validates P1 ontology reviews for Kimi, missing packet references, stale hashes, and strict coverage', () => {
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: undefined, VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS: undefined }, () => {
      mkdirSync(tmpDir, { recursive: true });
      const nodes = [
        node('corridor-a', 'Corridor', 'ARC.CORRIDOR', 'topic'),
        node('corridor-b', 'corridor', 'FLS.CORRIDOR', 'topic'),
      ];
      const groups = buildDuplicateCandidateGroups(nodes, [], undefined).filter((group) => group.priorityBand !== 'P0');
      const result = generateCanonicalP1DecisionPackets(tmpDir, groups.map((group) => ({ ...group, priorityBand: 'P1' as const })), [], {
        reviewer: 'packet-reviewer',
        limit: 1,
        apply: true,
      }, { nodes }) as any;
      const packet = result.packets[0];
      const kimi = recordCanonicalP1PacketReview(tmpDir, packet.packetId, {
        ontologyReviewStatus: 'kimi_reviewed',
        reviewerType: 'kimi',
        source: 'kimi',
        reviewedBy: 'kimi',
        reviewSummary: 'Kimi says this packet needs human review before any duplicate action.',
        reviewRiskLevel: 'high',
        nextAction: 'Route to human domain steward.',
        apply: true,
      }) as any;
      expect(kimi.review.ontologyReviewStatus).toBe('kimi_reviewed');
      expect(validateCanonicalStewardship(tmpDir, nodes, [], undefined).p1PacketsKimiReviewed).toBe(1);

      const reviewPath = resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'p1-packet-reviews.json');
      const payload = JSON.parse(readFileSync(reviewPath, 'utf-8'));
      payload.reviews.push({
        ...payload.reviews[0],
        reviewId: 'p1-packet-review-missing-packet',
        packetId: 'missing-packet',
        groupId: 'missing-group',
      });
      writeFileSync(reviewPath, JSON.stringify(payload, null, 2));
      const invalidReference = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(invalidReference.ok).toBe(false);
      expect(invalidReference.p1PacketReviewReferencesMissingPacket).toBe(1);

      payload.reviews = [payload.reviews[0]];
      payload.reviews[0].packetContentHash = 'stale-content-hash';
      writeFileSync(reviewPath, JSON.stringify(payload, null, 2));
      const stale = validateCanonicalStewardship(tmpDir, nodes, [], undefined);
      expect(stale.ok).toBe(true);
      expect(stale.p1PacketReviewHashMismatch).toBe(1);
      expect(stale.p1PacketReviewStale).toBe(1);
      expect(stale.warnings.some((warning: string) => warning.includes('stale packetContentHash'))).toBe(true);

      const strict = withEnv({ VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS: 'true' }, () => validateCanonicalStewardship(tmpDir, nodes, [], undefined));
      expect(strict.ok).toBe(false);
      expect(strict.blockers.some((blocker: string) => blocker.includes('strict P1 packet review mode'))).toBe(true);
    });
  });

  test('validates latest transaction manifest afterHash without treating superseded manifests as current drift', () => {
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: undefined, VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH: undefined }, () => {
      mkdirSync(tmpDir, { recursive: true });
      const nodes = [
        node('door-a', 'Door', 'ARC.DOOR', 'topic'),
        node('door-b', 'door', 'STR.DOOR', 'topic'),
        node('roof-a', 'Roof', 'ARC.ROOF', 'topic'),
        node('roof-b', 'roof', 'STR.ROOF', 'topic'),
      ];
      const groups = buildDuplicateCandidateGroups(nodes, [], undefined)
        .filter((group) => group.priorityBand !== 'P0')
        .map((group) => ({ ...group, priorityBand: 'P1' as const }));
      generateCanonicalP1DecisionPackets(tmpDir, groups.slice(0, 1), [], {
        reviewer: 'packet-reviewer',
        limit: 1,
        apply: true,
      }, { nodes });
      generateCanonicalP1DecisionPackets(tmpDir, groups, [], {
        reviewer: 'packet-reviewer',
        limit: 2,
        apply: true,
      }, { nodes });

      const manifestValidation = validateCanonicalTransactionManifests(tmpDir);
      expect(manifestValidation.count).toBeGreaterThanOrEqual(2);
      expect(manifestValidation.transactionManifestsWithAfterHash).toBeGreaterThanOrEqual(2);
      expect(manifestValidation.filesUnderManifestCustody).toBeGreaterThan(0);
      expect(manifestValidation.latestAfterHashMismatches).toBe(0);
      expect(manifestValidation.latestAfterHashMatches).toBe(manifestValidation.filesUnderManifestCustody);
      expect(manifestValidation.manifestAfterHashStatuses.some((status) => status.filePath.endsWith('p1-decision-packets.json') && status.matches)).toBe(true);
    });
  });

  test('reports latest manifest afterHash drift as warning in non-strict mode and blocker in strict mode', () => {
    withEnv({ VITRUVIUS_PACKET_HMAC_KEY: undefined, VITRUVIUS_TRANSACTION_HMAC_KEY: undefined, VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH: undefined }, () => {
      mkdirSync(tmpDir, { recursive: true });
      const nodes = [
        node('stair-a', 'Stair', 'ARC.STAIR', 'topic'),
        node('stair-b', 'stair', 'STR.STAIR', 'topic'),
      ];
      const groups = buildDuplicateCandidateGroups(nodes, [], undefined)
        .filter((group) => group.priorityBand !== 'P0')
        .map((group) => ({ ...group, priorityBand: 'P1' as const }));
      generateCanonicalP1DecisionPackets(tmpDir, groups, [], {
        reviewer: 'packet-reviewer',
        limit: 1,
        apply: true,
      }, { nodes });

      const packetPath = resolve(tmpDir, '006_System-Manifests', 'graph-canonical', 'p1-decision-packets.json');
      const payload = JSON.parse(readFileSync(packetPath, 'utf-8'));
      payload.generatedOutsideManifest = true;
      writeFileSync(packetPath, `${JSON.stringify(payload, null, 2)}\n`);

      const nonStrictValidation = validateCanonicalTransactionManifests(tmpDir);
      expect(nonStrictValidation.latestAfterHashMismatches).toBe(1);
      expect(nonStrictValidation.blockers).toHaveLength(0);
      expect(nonStrictValidation.warnings.some((warning) => warning.includes('drift since latest manifest'))).toBe(true);

      const strictValidation = withEnv({ VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH: 'true' }, () => validateCanonicalTransactionManifests(tmpDir));
      expect(strictValidation.latestAfterHashMismatches).toBe(1);
      expect(strictValidation.blockers.some((blocker) => blocker.includes('drift since latest manifest'))).toBe(true);
    });
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

  test('serves P1 packet review list, detail, and preview without graph mutation', async () => {
    const listResponse = await api.fetch(new Request('http://localhost/graph/canonical/p1-packets?unreviewed=true'));
    expect(listResponse.status).toBe(200);
    const listBody = await listResponse.json();
    expect(Array.isArray(listBody.packets)).toBe(true);
    expect(listBody.packets.length).toBeGreaterThan(0);
    expect(listBody.packets[0].ontologyReviewStatus || 'unreviewed').toBe('unreviewed');

    const packetId = listBody.packets[0].packetId;
    const detailResponse = await api.fetch(new Request(`http://localhost/graph/canonical/p1-packets/${encodeURIComponent(packetId)}`));
    expect(detailResponse.status).toBe(200);
    const detailBody = await detailResponse.json();
    expect(detailBody.packet.packetId).toBe(packetId);
    expect(detailBody.custody.packetContentHash).toBeTruthy();

    const previewResponse = await api.fetch(new Request(`http://localhost/graph/canonical/p1-packets/${encodeURIComponent(packetId)}/review-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ontologyReviewStatus: 'human_review_needed',
        reviewerType: 'human',
        reviewedBy: 'api-test-reviewer',
        reviewSummary: 'Route to human steward; this preview does not mutate the graph.',
        nextAction: 'Human review required before any duplicate action.',
      }),
    }));
    expect(previewResponse.status).toBe(200);
    const previewBody = await previewResponse.json();
    expect(previewBody.graphMutation).toBe(false);
    expect(previewBody.mutationScope).toBe('p1_packet_review_metadata_only');
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

      const p1ReviewBlocked = await api.fetch(new Request('http://example.com/graph/canonical/p1-packets/fake/review-decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ontologyReviewStatus: 'human_review_needed', reviewerType: 'human', reviewedBy: 'test', reviewSummary: 'gate test', nextAction: 'review' }),
      }));
      expect(p1ReviewBlocked.status).toBe(403);

      const p1ReviewAllowedPastGate = await api.fetch(new Request('http://example.com/graph/canonical/p1-packets/fake/review-decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-vitruvius-admin-token': 'secret-test-token' },
        body: JSON.stringify({ ontologyReviewStatus: 'human_review_needed', reviewerType: 'human', reviewedBy: 'test', reviewSummary: 'gate test', nextAction: 'review', apply: true }),
      }));
      expect(p1ReviewAllowedPastGate.status).toBe(200);
      const p1ReviewAllowedBody = await p1ReviewAllowedPastGate.json();
      expect(p1ReviewAllowedBody.blockers.some((blocker: string) => blocker.includes('not found'))).toBe(true);
    } finally {
      if (previousNodeEnv === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = previousNodeEnv;
      if (previousToken === undefined) delete process.env.VITRUVIUS_ADMIN_TOKEN; else process.env.VITRUVIUS_ADMIN_TOKEN = previousToken;
      if (previousDevAdmin === undefined) delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN; else process.env.VITRUVIUS_ENABLE_DEV_ADMIN = previousDevAdmin;
    }
  });
});
