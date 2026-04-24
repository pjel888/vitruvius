import { describe, expect, test } from 'bun:test';
import { buildDisplayLabel, buildNodeDetailQuery, buildPerspectiveQueries, buildSearchTypeFilter, normalizeEvidenceSpan, normalizeNode } from './index';

describe('perspective contract builders', () => {
  test('taxonomy search filter includes concepts', () => {
    const filter = buildSearchTypeFilter('taxonomy');
    expect(filter).toContain('c:Taxonomy');
    expect(filter).toContain('c.type = "concept"');
  });

  test('evidence search filter constrains to concept and evidence nodes', () => {
    const filter = buildSearchTypeFilter('evidence');
    expect(filter).toContain('c:EvidenceSpan');
    expect(filter).toContain('c.type = "concept"');
    expect(filter).toContain('c.type = "evidence_span"');
    expect(filter).not.toContain('"rule"');
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
    expect(nodeQuery).toContain("MATCH (c:CanonicalNode)-[:SUPPORTED_BY]->(e:EvidenceSpan)");
    expect(edgeQuery).toContain("MATCH (a:CanonicalNode)-[r:SUPPORTED_BY]->(b:EvidenceSpan)");
    expect(edgeQuery).toContain("a.type = 'concept'");
  });

  test('display labels compact long rule text without replacing canonical labels', () => {
    const fullLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    const compact = buildDisplayLabel(fullLabel, 'rule');

    expect(compact.startsWith('Rule · ')).toBe(true);
    expect(compact.length).toBeLessThan(fullLabel.length);
    expect(compact.endsWith('…')).toBe(true);
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
        type: 'rule',
        confidence: 0.91,
      },
    });

    expect(normalized?.id).toBe('rule-long-1');
    expect(normalized?.label).toContain('Every building permit applicant');
    expect(normalized?.displayLabel).toStartWith('Rule · ');
    expect(normalized?.confidence).toBe(0.91);
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
});
