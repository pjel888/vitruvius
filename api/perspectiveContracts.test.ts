import { describe, expect, test } from 'bun:test';
import { buildDisplayLabel, buildNodeDetailQuery, buildPerspectiveQueries, buildRuleDisplayLabel, buildSearchTypeFilter, compactRuleDisplayLabel, dedupeRuleDisplayLabels, normalizeEvidenceSpan, normalizeNode, normalizeTaxonomyNode } from './index';

describe('perspective contract builders', () => {
  test('taxonomy search filter includes concepts', () => {
    const filter = buildSearchTypeFilter('taxonomy');
    expect(filter).toContain('c:Taxonomy');
    expect(filter).toContain('c.type = "concept"');
  });

  test('evidence search filter constrains to concept and evidence nodes', () => {
    const filter = buildSearchTypeFilter('evidence');
    expect(filter).toContain('c:EvidenceSpan');
    expect(filter).toContain('c:DocumentVersion');
    expect(filter).toContain('c.type = "concept"');
    expect(filter).toContain('c.type = "evidence_span"');
    expect(filter).not.toContain('"rule"');
  });

  test('concept perspective is concept-centric and excludes rule/document support edges', () => {
    const { nodeQuery, edgeQuery } = buildPerspectiveQueries('concepts');
    expect(nodeQuery).toContain("WHERE c.type = 'concept'");
    expect(nodeQuery).not.toContain("'rule'");
    expect(edgeQuery).toContain("a.type = 'concept'");
    expect(edgeQuery).toContain("b.type = 'concept'");
    expect(edgeQuery).toContain("'CONSTRAINS'");
    expect(edgeQuery).toContain("'REGULATED_BY'");
    expect(edgeQuery).not.toContain("'DEFINED_BY'");
    expect(edgeQuery).not.toContain("'SUPPORTED_BY'");
  });

  test('taxonomy perspective queries constrain canonical nodes to concepts', () => {
    const { nodeQuery, edgeQuery } = buildPerspectiveQueries('taxonomy');
    expect(nodeQuery).toContain("MATCH (c:CanonicalNode) WHERE c.type = 'concept'");
    expect(edgeQuery).toContain("a.type = 'concept'");
    expect(edgeQuery).toContain("b.type = 'concept'");
    expect(nodeQuery).not.toContain("c.type <> 'taxonomy'");
  });

  test('evidence perspective queries constrain support edges to concept -> EvidenceSpan', () => {
    const { nodeQuery, edgeQuery } = buildPerspectiveQueries('evidence');
    expect(nodeQuery).toContain("MATCH (c:CanonicalNode)-[:SUPPORTED_BY]->(e)");
    expect(nodeQuery).toContain("e:DocumentVersion");
    expect(edgeQuery).toContain("MATCH (a:CanonicalNode)-[r:SUPPORTED_BY]->(b)");
    expect(edgeQuery).toContain("b:DocumentVersion");
    expect(edgeQuery).toContain("a.type = 'concept'");
  });

  test('legacy display-label fallback compacts long rule text without replacing canonical labels', () => {
    const fullLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    const compact = buildDisplayLabel(fullLabel, 'rule');

    expect(compact.startsWith('Rule · ')).toBe(true);
    expect(compact.length).toBeLessThan(fullLabel.length);
    expect(compact.endsWith('…')).toBe(true);
  });

  test('rule display labels prefer semantic taxonomy anchors over truncated legal text', () => {
    const fullLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    const semantic = buildRuleDisplayLabel({
      id: 'rule-pd-1096-section-301-000',
      type: 'rule',
      taxonomy_path: ['taxonomy-building-code', 'topic-permits', 'subtopic-building-permit'],
    }, fullLabel);

    expect(semantic).toBe('Building Permit Rule');
    expect(semantic).not.toContain('…');
    expect(semantic).not.toContain('Every building permit applicant');
  });

  test('rule display labels strip section and source suffixes from stored graph titles', () => {
    const stored = 'Socialized Housing Projects Rule — Section 50 — Article I Title Of Ordinance [vol2-zoning-ordinance-123292]';

    expect(compactRuleDisplayLabel(stored)).toBe('Socialized Housing Projects Rule · Sec. 50');
    expect(buildRuleDisplayLabel({ display_label: stored }, 'full canonical evidence label')).toBe('Socialized Housing Projects Rule · Sec. 50');
  });

  test('duplicate rule display labels receive stable compact differentiators', () => {
    const nodes = dedupeRuleDisplayLabels([
      { id: 'rule-law-comprehensive-zoning-ordinance-of-the-city-of-tarlac-section-4-000', type: 'rule', displayLabel: 'Zoning Ordinance Rule · Sec. 4' },
      { id: 'rule-law-comprehensive-zoning-ordinance-of-the-municipality-of-meycauayan-section-4-000', type: 'rule', displayLabel: 'Zoning Ordinance Rule · Sec. 4' },
      { id: 'concept-zoning-ordinance', type: 'concept', displayLabel: 'Zoning Ordinance' },
    ]);

    expect(nodes[0].displayLabel).toBe('Zoning Ordinance Rule · Sec. 4 · Tarlac');
    expect(nodes[1].displayLabel).toBe('Zoning Ordinance Rule · Sec. 4 · Meycauayan');
    expect(nodes[2].displayLabel).toBe('Zoning Ordinance');
  });

  test('node detail query includes taxonomy relationships and correct incoming direction', () => {
    const query = buildNodeDetailQuery();

    expect(query).toContain('OPTIONAL MATCH (c)-[outgoingRel]->(outgoingNode)');
    expect(query).toContain('OPTIONAL MATCH (incomingNode)-[incomingRel]->(c)');
    expect(query).not.toContain("type(r) <> 'BELONGS_TO'");
    expect(query).not.toContain("type(rin) <> 'HAS_CHILD'");
  });

  test('node normalization accepts nested Neo4j node-like values from collected relationship maps', () => {
    const normalized = normalizeNode({
      labels: ['CanonicalNode'],
      properties: {
        id: 'rule-long-1',
        label: 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.',
        display_label: 'Building Permit Rule — Section 1 — PD 1096',
        type: 'rule',
        confidence: 0.91,
      },
    });

    expect(normalized?.id).toBe('rule-long-1');
    expect(normalized?.label).toContain('Every building permit applicant');
    expect(normalized?.displayLabel).toBe('Building Permit Rule · Sec. 1');
    expect(normalized?.confidence).toBe(0.91);
  });

  test('taxonomy normalization emits compact display labels for taxonomy tree payloads', () => {
    const fullLabel = 'A very long taxonomy branch name that should not fill the explorer rail tooltip or tree row forever';
    const normalized = normalizeTaxonomyNode({
      id: 'topic-long-branch',
      label: fullLabel,
      kind: 'topic',
      conceptCount: 4,
    });

    expect(normalized?.label).toBe(fullLabel);
    expect(normalized?.displayLabel?.length ?? 0).toBeLessThan(fullLabel.length);
    expect(normalized?.conceptCount).toBe(4);
  });

  test('evidence normalization accepts nested Neo4j node-like values from collected evidence arrays', () => {
    const normalized = normalizeEvidenceSpan({
      labels: ['EvidenceSpan'],
      properties: {
        id: 'evidence-1',
        quote: 'No building shall be constructed without a valid permit.',
        document_id: 'law-pd-1096',
        document_title: 'National Building Code of the Philippines',
        deep_link: 'file:///pd-1096#section-301',
        confidence: 0.88,
      },
    });

    expect(normalized.id).toBe('evidence-1');
    expect(normalized.quote).toContain('valid permit');
    expect(normalized.document_title).toBe('National Building Code of the Philippines');
    expect(normalized.deep_link).toBe('file:///pd-1096#section-301');
    expect(normalized.confidence).toBe(0.88);
  });

  test('document version nodes normalize with readable labels for evidence maps', () => {
    const normalized = normalizeNode({
      id: 'docv-spp-205-v1',
      document_id: 'doc-spp-205',
      title: 'SPP DOC. 205',
      source_uri: '003_Canonical-Knowledge-Layer/shared/sources/spp-doc-205.md',
      sha256: 'a'.repeat(64),
    });

    expect(normalized?.type).toBe('document_version');
    expect(normalized?.label).toBe('SPP DOC. 205');
    expect(normalized?.displayLabel).toBe('SPP DOC. 205');
  });
});
  test('concept search filter constrains to concept nodes only', () => {
    const filter = buildSearchTypeFilter('concepts');
    expect(filter).toContain('c.type = "concept"');
    expect(filter).not.toContain('"rule"');
  });
