import { describe, expect, test } from 'bun:test';
import { clampGraphLayoutSpread, getCircularLayoutRadius, getClusteredLayoutRadii } from './layoutSpread';
import { buildPhysicsOptionsForGraph, shouldAutoFreezePhysicsAfterStabilization, shouldPreserveGraphVisibilityDuringDrag, shouldSkipExpensiveHoverHighlight, shouldUseLargeGraphRenderingGuardrails } from './largeGraphPerformance';
import { getOverviewVisibleNodes } from './overviewSnapshot';
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
    expect(shouldUseLargeGraphRenderingGuardrails(984, 960)).toBe(true);
    expect(shouldSkipExpensiveHoverHighlight(984, 960)).toBe(true);
    expect(shouldAutoFreezePhysicsAfterStabilization(984, 960)).toBe(true);
  });

  test('keeps small graphs interactive without large-graph guardrails', () => {
    expect(shouldUseLargeGraphRenderingGuardrails(20, 19)).toBe(false);
    expect(shouldSkipExpensiveHoverHighlight(20, 19)).toBe(false);
    expect(shouldAutoFreezePhysicsAfterStabilization(20, 19)).toBe(false);
  });

  test('uses bounded physics settings for expanded taxonomy graphs', () => {
    const large = buildPhysicsOptionsForGraph(984, 960, false);
    const small = buildPhysicsOptionsForGraph(20, 19, false);

    expect(large.enabled).toBe(true);
    expect(large.stabilization.iterations).toBeLessThan(small.stabilization.iterations);
    expect(large.maxVelocity).toBeLessThan(small.maxVelocity);
    expect(large.timestep).toBeLessThan(small.timestep);
    expect(buildPhysicsOptionsForGraph(984, 960, true).enabled).toBe(false);
  });

  test('preserves node and edge visibility while dragging the expanded graph', () => {
    expect(shouldPreserveGraphVisibilityDuringDrag()).toBe(true);
  });
});

describe('overview snapshot visibility', () => {
  const nodes: GraphNode[] = [
    { id: 'taxonomy-architecture', label: 'Architecture', type: 'taxonomy' },
    { id: 'topic-history-theory', label: 'History / Theory', type: 'topic' },
    { id: 'subtopic-vernacular', label: 'Vernacular Architecture', type: 'subtopic' },
  ];

  test('includes non-hidden nodes before filter state reaches the graph host', () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set(['subtopic-vernacular']),
      new Set<string>(),
      false,
    );

    expect(visible.map((node) => node.id)).toEqual(['taxonomy-architecture', 'topic-history-theory']);
  });

  test('matches node type filters after filter state is initialized', () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set<string>(),
      new Set(['topic']),
      true,
    );

    expect(visible.map((node) => node.id)).toEqual(['topic-history-theory']);
  });

  test('shows no nodes when the user filters every node type off', () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set<string>(),
      new Set<string>(),
      true,
    );

    expect(visible).toEqual([]);
  });
});

describe('graph layout spread controls', () => {
  test('clamps user spread values to the supported interactive range', () => {
    expect(clampGraphLayoutSpread(0.1)).toBe(0.75);
    expect(clampGraphLayoutSpread(3.5)).toBe(2.5);
    expect(clampGraphLayoutSpread(Number.NaN)).toBe(1.45);
  });

  test('expands circular and clustered layout radii from the same spread scalar', () => {
    expect(getCircularLayoutRadius(2)).toBe(600);
    expect(getClusteredLayoutRadii(24, 2)).toEqual({
      groupRadius: 1728,
      memberRadius: 280,
    });
  });
});
