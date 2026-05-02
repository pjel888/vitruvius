import { describe, expect, test } from 'bun:test';
import type { BackboneShadowGraphPreview } from '../types';

const PLACEMENT_QA_CLIENT_SCHEMA_CONSTANT = 'BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION';
const PLACEMENT_QA_CLIENT_PATH_CONSTANT = 'BACKBONE_PLACEMENT_QA_PREVIEW_PATH';
const PLACEMENT_QA_SERVER_SCHEMA_CONSTANT = 'SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION';
const EVIDENCE_CLIENT_SCHEMA_CONSTANT = 'BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION';
const EVIDENCE_CLIENT_PATH_CONSTANT = 'BACKBONE_EVIDENCE_PREVIEW_PATH';
const EVIDENCE_SERVER_SCHEMA_CONSTANT = 'SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION';

async function sourceText(relativePath: string) {
  return Bun.file(new URL(relativePath, import.meta.url)).text();
}

function exportedStringConstant(source: string, constantName: string) {
  const pattern = new RegExp(`export const ${constantName} = '([^']+)'`);
  const match = source.match(pattern);
  if (!match) throw new Error(`missing exported string constant: ${constantName}`);
  return match[1];
}

describe('graph API client contract', () => {
  test('AEC-MEPFS Explorer graph load requests compact render profile', async () => {
    const clientSource = await sourceText('./graphApi.ts');

    expect(clientSource).toContain("perspectiveId === 'aec-mepfs'");
    expect(clientSource).toContain("params.set('profile', 'render')");
    expect(clientSource).toContain("profile");
    expect(clientSource).toContain('getNodesForPerspectivePath');
    expect(clientSource).toContain('getNodesForPerspectiveUrl');
  });

  test('placement QA preview path and schema stay pinned to the server contract', async () => {
    const [clientSource, serverSource] = await Promise.all([
      sourceText('./graphApi.ts'),
      sourceText('../../../api/index.ts'),
    ]);

    const clientSchemaVersion = exportedStringConstant(clientSource, PLACEMENT_QA_CLIENT_SCHEMA_CONSTANT);
    const clientPath = exportedStringConstant(clientSource, PLACEMENT_QA_CLIENT_PATH_CONSTANT);
    const serverSchemaVersion = exportedStringConstant(serverSource, PLACEMENT_QA_SERVER_SCHEMA_CONSTANT);

    expect(clientPath).toBe('/v2/backbone/placement-qa');
    expect(clientSchemaVersion).toBe(serverSchemaVersion);
    expect(clientSource).toContain(`api<BackbonePlacementQaPreview>(${PLACEMENT_QA_CLIENT_PATH_CONSTANT})`);
  });

  test('evidence preview path and schema stay pinned to the server contract', async () => {
    const [clientSource, serverSource] = await Promise.all([
      sourceText('./graphApi.ts'),
      sourceText('../../../api/index.ts'),
    ]);

    const clientSchemaVersion = exportedStringConstant(clientSource, EVIDENCE_CLIENT_SCHEMA_CONSTANT);
    const clientPath = exportedStringConstant(clientSource, EVIDENCE_CLIENT_PATH_CONSTANT);
    const serverSchemaVersion = exportedStringConstant(serverSource, EVIDENCE_SERVER_SCHEMA_CONSTANT);

    expect(clientPath).toBe('/v2/backbone/evidence');
    expect(clientSchemaVersion).toBe(serverSchemaVersion);
    expect(clientSource).toContain(`api<BackboneEvidencePreview>(${EVIDENCE_CLIENT_PATH_CONSTANT})`);
  });

  test('resource review client helpers target reviewer workflow routes', async () => {
    const clientSource = await sourceText('./graphApi.ts');

    expect(clientSource).toContain('/resources/review/queue');
    expect(clientSource).toContain('/resources/review/candidates');
    expect(clientSource).toContain('/resources/review/local-files');
    expect(clientSource).toContain('/resources/review/standards');
    expect(clientSource).toContain('/resources/review/report');
    expect(clientSource).toContain('/resources/review/link/${encodeURIComponent(linkId)}/decision');
    expect(clientSource).toContain('/resources/review/candidate/${encodeURIComponent(candidateId)}/decision');
    expect(clientSource).toContain('/resources/review/local-file/${encodeURIComponent(fileId)}/decision');
    expect(clientSource).toContain('/resources/review/standards/${encodeURIComponent(id)}/context-preview');
    expect(clientSource).toContain('/resources/review/standards/${encodeURIComponent(id)}/context-decision');
  });

  test('canonical stewardship client helpers target duplicate review workflow routes', async () => {
    const clientSource = await sourceText('./graphApi.ts');

    expect(clientSource).toContain('/graph/canonical/duplicates');
    expect(clientSource).toContain('/graph/canonical/duplicates/${encodeURIComponent(groupId)}');
    expect(clientSource).toContain('/graph/canonical/duplicates/${encodeURIComponent(groupId)}/preview');
    expect(clientSource).toContain('/graph/canonical/duplicates/${encodeURIComponent(groupId)}/decision');
    expect(clientSource).toContain('/graph/canonical/decisions');
    expect(clientSource).toContain('/graph/canonical/approvals');
    expect(clientSource).toContain('/graph/canonical/approvals/${encodeURIComponent(approvalId)}');
    expect(clientSource).toContain('/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approval-preview');
    expect(clientSource).toContain('/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approve');
    expect(clientSource).toContain('/graph/canonical/decisions/${encodeURIComponent(decisionId)}/reject-approval');
    expect(clientSource).toContain('/graph/canonical/search?q=');
    expect(clientSource).toContain('/graph/canonical/validation');
    expect(clientSource).toContain('/graph/canonical/batches');
    expect(clientSource).toContain('/graph/canonical/batches/${encodeURIComponent(batchId)}/preview');
    expect(clientSource).toContain('/graph/canonical/batches/${encodeURIComponent(batchId)}/decision');
    expect(clientSource).toContain('/graph/canonical/p1-decision-packets');
    expect(clientSource).toContain('/graph/canonical/p1-decision-packets/generate');
    expect(clientSource).toContain('/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback-preview');
    expect(clientSource).toContain('/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback');
    expect(clientSource).toContain('/graph/canonical/remediation');
    expect(clientSource).toContain('/graph/canonical/remediation/${encodeURIComponent(id)}');
    expect(clientSource).toContain('/graph/canonical/remediation/${encodeURIComponent(id)}/status');
  });

  test('selected-node neighborhood helper targets graph hydration route with direct relationship options', async () => {
    const clientSource = await sourceText('./graphApi.ts');

    expect(clientSource).toContain('getNodeNeighborhood');
    expect(clientSource).toContain('/node/${encodeURIComponent(id)}/neighborhood');
    expect(clientSource).toContain("params.set('depth', String(options.depth))");
    expect(clientSource).toContain("params.set('direction', options.direction)");
    expect(clientSource).toContain("params.set('relTypes', options.relTypes.join(','))");
  });

  test('shadow graph preview edge contract accepts AHJ applicability metadata', () => {
    const preview: BackboneShadowGraphPreview = {
      available: true,
      counts: {
        nodes: 2,
        edges: 1,
        roots: 1,
        maxDepth: 2,
      },
      nodes: [],
      edges: [
        {
          id: 'VTN-DOM-0000001--requires--VTN-DOM-0000002',
          fromId: 'VTN-DOM-0000001',
          toId: 'VTN-DOM-0000002',
          predicate: 'requires',
          fromPathCode: 'COM.APP.AHJ',
          toPathCode: 'STR.LOA.LAT.WND',
          applicabilityBasis: 'source_family_only_ahj_or_project_basis_required',
          jurisdictionContext: 'source-family-mixed-ahj-required',
          designBasisStatus: 'no_project_numeric_criteria_admitted',
        },
      ],
    };

    expect(preview.edges[0].applicabilityBasis).toBe('source_family_only_ahj_or_project_basis_required');
    expect(preview.edges[0].jurisdictionContext).toBe('source-family-mixed-ahj-required');
    expect(preview.edges[0].designBasisStatus).toBe('no_project_numeric_criteria_admitted');
  });
});
