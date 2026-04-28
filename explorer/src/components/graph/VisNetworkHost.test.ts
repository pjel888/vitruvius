import { describe, expect, test } from 'bun:test';
import { buildPhysicsOptionsForGraph, shouldAutoFreezePhysicsAfterStabilization, shouldPreserveGraphVisibilityDuringDrag, shouldSkipExpensiveHoverHighlight, shouldUseLargeGraphRenderingGuardrails } from './largeGraphPerformance';
import { buildNodeTooltip, compactRuleDisplayLabel, deriveRuleDisplayLabelsFromConceptEdges } from './visNetworkDisplay';
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

  test('compacts source-provided semantic rule titles for graph display', () => {
    const nodes: GraphNode[] = [
      { id: 'concept-building-permit', label: 'Building Permit', displayLabel: 'Building Permit', type: 'concept' },
      {
        id: 'rule-building-permit-1',
        label: 'A building permit is required for all new construction',
        displayLabel: 'Building Permit Rule — Section 1 — PD 1096',
        type: 'rule',
      },
    ];
    const edges: GraphEdge[] = [
      { id: 'edge-1', source: 'concept-building-permit', target: 'rule-building-permit-1', type: 'DEFINED_BY' },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);

    expect(result.find((node) => node.id === 'rule-building-permit-1')?.displayLabel).toBe('Building Permit Rule · Sec. 1');
  });

  test('removes section and source suffixes from oversized rule titles', () => {
    expect(compactRuleDisplayLabel('Socialized Housing Projects Rule — Section 50 — Article I Title Of Ordinance [vol2-zoning-ordinance-123292]')).toBe('Socialized Housing Projects Rule · Sec. 50');
  });
});

describe('buildNodeTooltip', () => {
  test('includes canonical label when it differs from display label', () => {
    const tooltip = buildNodeTooltip({
      id: 'rule-building-permit-1',
      label: 'A building permit is required for all new construction',
      displayLabel: 'Building Permit Rule — Section 1 — PD 1096',
      type: 'rule',
    });

    expect(tooltip).toContain('Building Permit Rule');
    expect(tooltip).toContain('Canonical: A building permit is required for all new construction');
    expect(tooltip).not.toContain('<br');
    expect(tooltip).not.toContain('<b>');
  });
});


describe('large graph performance guardrails', () => {
  test('classifies the expanded AEC-MEPFS taxonomy as a large graph', () => {
    expect(shouldUseLargeGraphRenderingGuardrails(779, 760)).toBe(true);
    expect(shouldSkipExpensiveHoverHighlight(779, 760)).toBe(true);
    expect(shouldAutoFreezePhysicsAfterStabilization(779, 760)).toBe(true);
  });

  test('keeps small graphs interactive without large-graph guardrails', () => {
    expect(shouldUseLargeGraphRenderingGuardrails(20, 19)).toBe(false);
    expect(shouldSkipExpensiveHoverHighlight(20, 19)).toBe(false);
    expect(shouldAutoFreezePhysicsAfterStabilization(20, 19)).toBe(false);
  });

  test('uses bounded physics settings for expanded taxonomy graphs', () => {
    const large = buildPhysicsOptionsForGraph(779, 760, false);
    const small = buildPhysicsOptionsForGraph(20, 19, false);

    expect(large.enabled).toBe(true);
    expect(large.stabilization.iterations).toBeLessThan(small.stabilization.iterations);
    expect(large.maxVelocity).toBeLessThan(small.maxVelocity);
    expect(large.timestep).toBeLessThan(small.timestep);
    expect(buildPhysicsOptionsForGraph(779, 760, true).enabled).toBe(false);
  });

  test('preserves node and edge visibility while dragging the expanded graph', () => {
    expect(shouldPreserveGraphVisibilityDuringDrag()).toBe(true);
  });
});
