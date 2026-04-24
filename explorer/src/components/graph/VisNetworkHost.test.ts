import { describe, expect, test } from 'bun:test';
import { deriveRuleDisplayLabelsFromConceptEdges } from './VisNetworkHost';
import type { GraphEdge, GraphNode } from '../../types';

describe('deriveRuleDisplayLabelsFromConceptEdges', () => {
  test('uses the defining concept to create non-truncated semantic rule titles', () => {
    const longLegalLabel = 'The scope of this IRR shall cover the following disciplines: architectural, civil/structural, electrical, mechanical, sanitary, plumbing, and electronics.';
    const nodes: GraphNode[] = [
      { id: 'concept-building-permit', label: 'Building Permit', displayLabel: 'Building Permit', type: 'concept' },
      { id: 'rule-long-1', label: longLegalLabel, displayLabel: 'Rule · The scope of this IRR shall cover the following…', type: 'rule' },
    ];
    const edges: GraphEdge[] = [
      { id: 'edge-1', source: 'concept-building-permit', target: 'rule-long-1', type: 'DEFINED_BY' },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);
    const rule = result.find((node) => node.id === 'rule-long-1');

    expect(rule?.label).toBe(longLegalLabel);
    expect(rule?.displayLabel).toBe('Building Permit Rule');
    expect(rule?.displayLabel).not.toContain('…');
    expect(rule?.displayLabel).not.toContain('shall');
  });

  test('title-cases legacy lowercase concept labels for rule titles', () => {
    const nodes: GraphNode[] = [
      { id: 'concept-architectural-history', label: 'architectural history', type: 'concept' },
      { id: 'rule-history-1', label: 'Architectural History rule from handout', displayLabel: 'General Rule', type: 'rule' },
    ];
    const edges: GraphEdge[] = [
      { id: 'edge-1', source: 'concept-architectural-history', target: 'rule-history-1', type: 'DEFINED_BY' },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);

    expect(result.find((node) => node.id === 'rule-history-1')?.displayLabel).toBe('Architectural History Rule');
  });
});
