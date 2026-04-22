import { describe, expect, test } from 'bun:test';
import { buildPerspectiveQueries, buildSearchTypeFilter } from './index';

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
});
