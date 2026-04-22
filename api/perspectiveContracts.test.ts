import { describe, expect, test } from 'bun:test';

describe('perspective contract guards', () => {
  test('taxonomy perspective query remains constrained to taxonomy hierarchy plus concepts', () => {
    const taxonomyEdgeQuery = `
      MATCH (a)-[r:HAS_CHILD|BELONGS_TO]->(b)
      WHERE (a:Taxonomy OR a:Topic OR a:Subtopic OR (a:CanonicalNode AND a.type = 'concept'))
        AND (b:Taxonomy OR b:Topic OR b:Subtopic OR (b:CanonicalNode AND b.type = 'concept'))
      RETURN r, a.id AS source, b.id AS target
    `;

    expect(taxonomyEdgeQuery).toContain("a.type = 'concept'");
    expect(taxonomyEdgeQuery).toContain("b.type = 'concept'");
    expect(taxonomyEdgeQuery).not.toContain("c.type <> 'taxonomy'");
  });

  test('evidence perspective query remains constrained to concept support edges', () => {
    const evidenceEdgeQuery = `
      MATCH (a:CanonicalNode)-[r:SUPPORTED_BY]->(b:EvidenceSpan)
      WHERE a.type = 'concept'
      RETURN r, a.id AS source, b.id AS target
    `;

    expect(evidenceEdgeQuery).toContain("SUPPORTED_BY");
    expect(evidenceEdgeQuery).toContain("a.type = 'concept'");
    expect(evidenceEdgeQuery).toContain('(b:EvidenceSpan)');
  });
});
