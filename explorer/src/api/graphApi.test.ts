import { describe, expect, test } from 'bun:test';

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
});
