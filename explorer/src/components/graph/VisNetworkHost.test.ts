import { describe, expect, test } from "bun:test";
import {
  buildCenteredNetworkLayoutPositions,
  clampGraphLayoutSpread,
  getCircularLayoutRadius,
  getClusteredLayoutRadii,
  scaleNetworkLayoutPositions,
} from "./layoutSpread";
import {
  buildPhysicsOptionsForGraph,
  getNetworkPhysicsSpreadRatio,
  shouldAutoFreezePhysicsAfterStabilization,
  shouldPreserveGraphVisibilityDuringDrag,
  shouldSkipExpensiveHoverHighlight,
  shouldUseLargeGraphRenderingGuardrails,
} from "./largeGraphPerformance";
import {
  buildPrecomputedNetworkLayoutCacheKey,
  buildPrecomputedNetworkLayoutPositions,
  getCachedOrBuildPrecomputedNetworkLayoutPositions,
  shouldUsePrecomputedNetworkLayout,
} from "./precomputedNetworkLayout";
import { getOverviewVisibleNodes } from "./overviewSnapshot";
import { getNodeGraphLabel } from "./nodeLabelVisibility";
import {
  buildNodeTooltip,
  compactRuleDisplayLabel,
  deriveRuleDisplayLabelsFromConceptEdges,
} from "./visNetworkDisplay";
import {
  DIMMED_EDGE_OPACITY,
  EDGE_ARROW_SCALE,
  EDGE_ARROW_TYPE,
  EDGE_SMOOTH,
  EMPHASIZED_EDGE_WIDTH,
  MIN_NODE_BODY_SIZE,
  NORMAL_EDGE_OPACITY,
  NODE_LABEL_FONT_SIZE,
  NORMAL_EDGE_WIDTH,
  SELECTED_NEIGHBORHOOD_INACTIVE_MIN_SIZE,
  SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY,
  SELECTED_NEIGHBORHOOD_INACTIVE_SIZE_RATIO,
  clampGraphZoomScale,
  clampUserFacingZoomScale,
  getNodeBodySize,
  getSelectedNeighborhoodIds,
  getUniformArrowEdgeStyle,
  isSelectedNeighborhoodEdge,
  toRgba,
} from "./graphVisualEmphasis";
import { buildChildOrbitLayoutUpdates, getChildOrbitDescendants, getChildOrbitRingRadius } from './childOrbitLayout';
import type { GraphEdge, GraphNode } from "../../types";

describe("deriveRuleDisplayLabelsFromConceptEdges", () => {
  test("uses the defining concept to create non-truncated semantic rule titles", () => {
    const longLegalLabel =
      "The scope of this IRR shall cover the following disciplines: architectural, civil/structural, electrical, mechanical, sanitary, plumbing, and electronics.";
    const nodes: GraphNode[] = [
      {
        id: "concept-building-permit",
        label: "Building Permit",
        displayLabel: "Building Permit",
        type: "concept",
      },
      {
        id: "rule-long-1",
        label: longLegalLabel,
        displayLabel: "Rule · The scope of this IRR shall cover the following…",
        type: "rule",
      },
    ];
    const edges: GraphEdge[] = [
      {
        id: "edge-1",
        source: "concept-building-permit",
        target: "rule-long-1",
        type: "DEFINED_BY",
      },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);
    const rule = result.find((node) => node.id === "rule-long-1");

    expect(rule?.label).toBe(longLegalLabel);
    expect(rule?.displayLabel).toBe("Building Permit Rule");
    expect(rule?.displayLabel).not.toContain("…");
    expect(rule?.displayLabel).not.toContain("shall");
  });

  test("title-cases legacy lowercase concept labels for rule titles", () => {
    const nodes: GraphNode[] = [
      {
        id: "concept-architectural-history",
        label: "architectural history",
        type: "concept",
      },
      {
        id: "rule-history-1",
        label: "Architectural History rule from handout",
        displayLabel: "General Rule",
        type: "rule",
      },
    ];
    const edges: GraphEdge[] = [
      {
        id: "edge-1",
        source: "concept-architectural-history",
        target: "rule-history-1",
        type: "DEFINED_BY",
      },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);

    expect(
      result.find((node) => node.id === "rule-history-1")?.displayLabel,
    ).toBe("Architectural History Rule");
  });

  test("compacts source-provided semantic rule titles for graph display", () => {
    const nodes: GraphNode[] = [
      {
        id: "concept-building-permit",
        label: "Building Permit",
        displayLabel: "Building Permit",
        type: "concept",
      },
      {
        id: "rule-building-permit-1",
        label: "A building permit is required for all new construction",
        displayLabel: "Building Permit Rule — Section 1 — PD 1096",
        type: "rule",
      },
    ];
    const edges: GraphEdge[] = [
      {
        id: "edge-1",
        source: "concept-building-permit",
        target: "rule-building-permit-1",
        type: "DEFINED_BY",
      },
    ];

    const result = deriveRuleDisplayLabelsFromConceptEdges(nodes, edges);

    expect(
      result.find((node) => node.id === "rule-building-permit-1")?.displayLabel,
    ).toBe("Building Permit Rule · Sec. 1");
  });

  test("removes section and source suffixes from oversized rule titles", () => {
    expect(
      compactRuleDisplayLabel(
        "Socialized Housing Projects Rule — Section 50 — Article I Title Of Ordinance [vol2-zoning-ordinance-123292]",
      ),
    ).toBe("Socialized Housing Projects Rule · Sec. 50");
  });
});

describe("buildNodeTooltip", () => {
  test("includes canonical label when it differs from display label", () => {
    const tooltip = buildNodeTooltip({
      id: "rule-building-permit-1",
      label: "A building permit is required for all new construction",
      displayLabel: "Building Permit Rule — Section 1 — PD 1096",
      type: "rule",
    });

    expect(tooltip).toContain("Building Permit Rule");
    expect(tooltip).toContain(
      "Canonical: A building permit is required for all new construction",
    );
    expect(tooltip).not.toContain("<br");
    expect(tooltip).not.toContain("<b>");
  });
});

describe("large graph performance guardrails", () => {
  test("classifies the expanded AEC-MEPFS taxonomy as a large graph", () => {
    expect(shouldUseLargeGraphRenderingGuardrails(2424, 2400)).toBe(true);
    expect(shouldSkipExpensiveHoverHighlight(2424, 2400)).toBe(true);
    expect(shouldAutoFreezePhysicsAfterStabilization(2424, 2400)).toBe(true);
  });

  test("keeps small graphs interactive without large-graph guardrails", () => {
    expect(shouldUseLargeGraphRenderingGuardrails(20, 19)).toBe(false);
    expect(shouldSkipExpensiveHoverHighlight(20, 19)).toBe(false);
    expect(shouldAutoFreezePhysicsAfterStabilization(20, 19)).toBe(false);
  });

  test("uses bounded physics settings for expanded taxonomy graphs", () => {
    const large = buildPhysicsOptionsForGraph(2424, 2400, false);
    const small = buildPhysicsOptionsForGraph(20, 19, false);

    expect(large.enabled).toBe(true);
    expect(large.stabilization.iterations).toBeLessThan(
      small.stabilization.iterations,
    );
    expect(large.maxVelocity).toBeLessThan(small.maxVelocity);
    expect(large.timestep).toBeLessThan(small.timestep);
    expect(buildPhysicsOptionsForGraph(2424, 2400, true).enabled).toBe(false);
  });

  test("uses spread to expand Network Layout physics without changing layout mode", () => {
    const defaultPhysics = buildPhysicsOptionsForGraph(2424, 2400, false, 2.65);
    const expandedPhysics = buildPhysicsOptionsForGraph(2424, 2400, false, 5.3);

    expect(getNetworkPhysicsSpreadRatio(5.3)).toBe(2);
    expect(expandedPhysics.forceAtlas2Based.springLength).toBeGreaterThan(defaultPhysics.forceAtlas2Based.springLength);
    expect(expandedPhysics.forceAtlas2Based.gravitationalConstant).toBeLessThan(defaultPhysics.forceAtlas2Based.gravitationalConstant);
    expect(expandedPhysics.forceAtlas2Based.centralGravity).toBeLessThan(defaultPhysics.forceAtlas2Based.centralGravity);
  });

  test("uses the saved precomputed map only for the large cached layout", () => {
    expect(shouldUsePrecomputedNetworkLayout(2424, 2400, 'precomputed')).toBe(true);
    expect(shouldUsePrecomputedNetworkLayout(20, 19, 'precomputed')).toBe(false);
    expect(shouldUsePrecomputedNetworkLayout(2424, 2400, 'forceatlas2')).toBe(false);
    expect(shouldUsePrecomputedNetworkLayout(2424, 2400, 'clustered')).toBe(false);
  });

  test("preserves node and edge visibility while dragging the expanded graph", () => {
    expect(shouldPreserveGraphVisibilityDuringDrag()).toBe(true);
  });
});

describe("node label visibility", () => {
  test("keeps nodes visible while suppressing labels for hidden label types", () => {
    const subtopic: GraphNode = {
      id: "subtopic-vernacular",
      label: "Vernacular Architecture",
      type: "subtopic",
    };

    expect(getNodeGraphLabel(subtopic, new Set(["taxonomy", "topic"]))).toBe(
      "",
    );
    expect(getNodeGraphLabel(subtopic, new Set(["subtopic"]))).toBe(
      "Vernacular Architecture",
    );
  });
});

describe("overview snapshot visibility", () => {
  const nodes: GraphNode[] = [
    { id: "taxonomy-architecture", label: "Architecture", type: "taxonomy" },
    { id: "topic-history-theory", label: "History / Theory", type: "topic" },
    {
      id: "subtopic-vernacular",
      label: "Vernacular Architecture",
      type: "subtopic",
    },
  ];

  test("includes non-hidden nodes before filter state reaches the graph host", () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set(["subtopic-vernacular"]),
      new Set<string>(),
      false,
    );

    expect(visible.map((node) => node.id)).toEqual([
      "taxonomy-architecture",
      "topic-history-theory",
    ]);
  });

  test("matches node type filters after filter state is initialized", () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set<string>(),
      new Set(["topic"]),
      true,
    );

    expect(visible.map((node) => node.id)).toEqual(["topic-history-theory"]);
  });

  test("shows no nodes when the user filters every node type off", () => {
    const visible = getOverviewVisibleNodes(
      nodes,
      new Set<string>(),
      new Set<string>(),
      true,
    );

    expect(visible).toEqual([]);
  });
});

describe("graph layout spread controls", () => {
  test("clamps user spread values to the supported interactive range", () => {
    expect(clampGraphLayoutSpread(0.1)).toBe(0.75);
    expect(clampGraphLayoutSpread(6.5)).toBe(6);
    expect(clampGraphLayoutSpread(Number.NaN)).toBe(2.65);
  });

  test("expands circular and clustered layout radii from the same spread scalar", () => {
    expect(getCircularLayoutRadius(2)).toBe(600);
    expect(getClusteredLayoutRadii(24, 2)).toEqual({
      groupRadius: 1728,
      memberRadius: 280,
    });
    expect(getClusteredLayoutRadii(24, 4)).toEqual({
      groupRadius: 3456,
      memberRadius: 560,
    });
    expect(getClusteredLayoutRadii(24, 6)).toEqual({
      groupRadius: 5184,
      memberRadius: 840,
    });
  });

  test("keeps small Network Layout startup positions compact and centered", () => {
    const updates = buildCenteredNetworkLayoutPositions(["a", "b", "c", "d"], 2.65);

    expect(updates[0]).toEqual({ id: "a", x: 0, y: 0 });
    updates.forEach((position) => {
      expect(Math.hypot(position.x, position.y)).toBeLessThanOrEqual(50);
    });
  });

  test("keeps the bounded Network Layout reset compact before physics expands it", () => {
    const ids = Array.from({ length: 2424 }, (_, index) => `node-${index}`);
    const updates = buildCenteredNetworkLayoutPositions(ids, 2.65);
    const maxRadius = Math.max(...updates.map((position) => Math.hypot(position.x, position.y)));

    expect(updates).toHaveLength(ids.length);
    expect(maxRadius).toBeLessThan(300);
  });

  test("precomputes large Network Layout positions into wide deterministic rings", () => {
    const nodes: GraphNode[] = Array.from({ length: 96 }, (_, index) => {
      const root = index < 48 ? "Architecture" : "Electrical Engineering";
      const level = index % 4;
      return {
        id: `node-${index}`,
        label: `Node ${index}`,
        type: level === 0 ? "taxonomy" : level === 1 ? "topic" : level === 2 ? "subtopic" : "concept",
        taxonomy_path: [root, `Topic ${Math.floor(index / 8)}`, `Subtopic ${index}`].slice(0, level + 1),
      };
    });
    const edges: GraphEdge[] = nodes.slice(1).map((node, index) => ({
      id: `edge-${index}`,
      source: nodes[Math.max(0, index - 1)].id,
      target: node.id,
      type: "HAS_CHILD",
    }));

    const first = buildPrecomputedNetworkLayoutPositions(nodes, edges, 2.65);
    const second = buildPrecomputedNetworkLayoutPositions(nodes, edges, 2.65);
    const maxRadius = Math.max(...first.map((position) => Math.hypot(position.x, position.y)));

    expect(first).toEqual(second);
    expect(first).toHaveLength(nodes.length);
    expect(maxRadius).toBeGreaterThan(1800);
  });

  test("caches precomputed Network Layout positions by graph signature and spread", () => {
    const storageMap = new Map<string, string>();
    const storage = {
      getItem: (key: string) => storageMap.get(key) ?? null,
      setItem: (key: string, value: string) => storageMap.set(key, value),
    };
    const nodes: GraphNode[] = [
      { id: "taxonomy-architecture", label: "Architecture", type: "taxonomy", taxonomy_path: ["Architecture"] },
      { id: "topic-history", label: "History", type: "topic", taxonomy_path: ["Architecture", "History"] },
      { id: "subtopic-modern", label: "Modern", type: "subtopic", taxonomy_path: ["Architecture", "History", "Modern"] },
    ];
    const edges: GraphEdge[] = [
      { id: "e1", source: "taxonomy-architecture", target: "topic-history", type: "HAS_CHILD" },
      { id: "e2", source: "topic-history", target: "subtopic-modern", type: "HAS_CHILD" },
    ];

    const initial = getCachedOrBuildPrecomputedNetworkLayoutPositions(nodes, edges, 2.65, storage);
    const cached = getCachedOrBuildPrecomputedNetworkLayoutPositions(nodes, edges, 2.65, storage);
    const expandedKey = buildPrecomputedNetworkLayoutCacheKey(nodes, edges, 5.3);

    expect(initial.cacheHit).toBe(false);
    expect(cached.cacheHit).toBe(true);
    expect(cached.positions).toEqual(initial.positions);
    expect(expandedKey).not.toBe(initial.cacheKey);
  });

  test("scales Network Layout positions around their current center instead of taxonomy clusters", () => {
    const updates = scaleNetworkLayoutPositions([
      { id: "a", x: -10, y: 0 },
      { id: "b", x: 10, y: 0 },
    ], 2, 4);

    expect(updates).toEqual([
      { id: "a", x: -20, y: 0 },
      { id: "b", x: 20, y: 0 },
    ]);
  });
});


describe("graph visual hierarchy controls", () => {
  const edges: GraphEdge[] = [
    { id: "e1", source: "architecture", target: "history", type: "HAS_CHILD" },
    { id: "e2", source: "architecture", target: "structures", type: "HAS_CHILD" },
    { id: "e4", source: "history", target: "theory", type: "HAS_CHILD" },
    { id: "e5", source: "ornament", target: "theory", type: "PART_OF" },
    { id: "e3", source: "electrical", target: "lighting", type: "HAS_CHILD" },
  ];

  test("clamps zoom to defensive and user-facing ranges", () => {
    expect(clampGraphZoomScale(0.01)).toBe(0.08);
    expect(clampGraphZoomScale(8)).toBe(4);
    expect(clampUserFacingZoomScale(0.01)).toBe(0.1);
    expect(clampUserFacingZoomScale(Number.NaN)).toBe(1);
  });

  test("pins thin normal edges and stronger selected edges", () => {
    expect(NORMAL_EDGE_WIDTH).toBeLessThan(0.35);
    expect(NORMAL_EDGE_OPACITY).toBeLessThan(0.5);
    expect(DIMMED_EDGE_OPACITY).toBeLessThan(0.08);
    expect(EDGE_SMOOTH).toBe(false);
    expect(EDGE_ARROW_TYPE).toBe("vee");
    expect(EDGE_ARROW_SCALE).toBeLessThan(0.25);
    expect(EMPHASIZED_EDGE_WIDTH).toBeLessThan(0.75);
    expect(EMPHASIZED_EDGE_WIDTH).toBeGreaterThan(NORMAL_EDGE_WIDTH);
  });

  test("keeps root-to-topic and topic-to-subtopic arrows visually uniform", () => {
    const taxonomyToTopic = getUniformArrowEdgeStyle();
    const topicToSubtopic = getUniformArrowEdgeStyle();

    expect(taxonomyToTopic).toEqual(topicToSubtopic);
    expect(taxonomyToTopic.smooth).toBe(false);
    expect(taxonomyToTopic.dashes).toBe(false);
    expect(taxonomyToTopic.arrows.to).toEqual({ enabled: true, type: "vee", scaleFactor: EDGE_ARROW_SCALE });
    expect(taxonomyToTopic.chosen).toBe(false);
    expect(taxonomyToTopic.selectionWidth).toBe(0);
    expect(taxonomyToTopic.hoverWidth).toBe(0);
  });

  test("uses the same size helper for query and expansion merge paths", () => {
    expect(getNodeBodySize({ id: "small", label: "Small", type: "concept", radius: 1 }, 0, "uniform")).toBe(MIN_NODE_BODY_SIZE);
    expect(getNodeBodySize({ id: "conf", label: "Confident", type: "concept", confidence: 0.95 }, 0, "confidence")).toBe(9.5);
    expect(getNodeBodySize({ id: "degree", label: "Degree", type: "concept", radius: 4 }, 20, "degree")).toBe(14);
  });

  test("keeps graph labels smaller than node bodies", () => {
    expect(NODE_LABEL_FONT_SIZE).toBeLessThan(MIN_NODE_BODY_SIZE);
    expect(getNodeBodySize({ id: "n", label: "Node", type: "concept", radius: 2 })).toBe(MIN_NODE_BODY_SIZE);
  });

  test("dims non-selected nodes enough to make selected subtrees legible", () => {
    expect(SELECTED_NEIGHBORHOOD_INACTIVE_OPACITY).toBeLessThan(0.1);
    expect(SELECTED_NEIGHBORHOOD_INACTIVE_SIZE_RATIO).toBeLessThan(0.5);
    expect(SELECTED_NEIGHBORHOOD_INACTIVE_MIN_SIZE).toBeLessThan(MIN_NODE_BODY_SIZE);
  });

  test("builds a recursive selected subtree for focus opacity", () => {
    const neighborhood = getSelectedNeighborhoodIds(edges, "architecture");

    expect(neighborhood).toEqual(new Set(["architecture", "history", "structures", "theory", "ornament"]));
    expect(isSelectedNeighborhoodEdge(edges[0], neighborhood, "architecture")).toBe(true);
    expect(isSelectedNeighborhoodEdge(edges[2], neighborhood, "architecture")).toBe(true);
    expect(isSelectedNeighborhoodEdge(edges[4], neighborhood, "architecture")).toBe(false);
  });

  test("converts hex colors into dimmed rgba values", () => {
    expect(toRgba("#60a5fa", 0.5)).toBe("rgba(96, 165, 250, 0.5)");
  });
});


describe("child council orbit layout", () => {
  const nodes: GraphNode[] = [
    { id: "taxonomy-architecture", label: "Architecture", type: "taxonomy" },
    { id: "topic-history", label: "History", type: "topic" },
    { id: "subtopic-theory", label: "Theory", type: "subtopic" },
    { id: "topic-structures", label: "Structures", type: "topic" },
  ];
  const edges: GraphEdge[] = [
    { id: "e1", source: "taxonomy-architecture", target: "topic-history", type: "HAS_CHILD" },
    { id: "e2", source: "topic-history", target: "subtopic-theory", type: "HAS_CHILD" },
    { id: "e3", source: "topic-structures", target: "taxonomy-architecture", type: "BELONGS_TO" },
  ];

  test("collects child and grandchild descendants from directed taxonomy edges", () => {
    expect(getChildOrbitDescendants(nodes, edges, "taxonomy-architecture")).toEqual([
      { id: "topic-history", depth: 1 },
      { id: "topic-structures", depth: 1 },
      { id: "subtopic-theory", depth: 2 },
    ]);
  });

  test("places descendants into deterministic circular rings around the selected node", () => {
    const updates = buildChildOrbitLayoutUpdates(nodes, edges, "taxonomy-architecture", {
      "taxonomy-architecture": { x: 100, y: 100 },
      "topic-history": { x: 100, y: 100 },
      "topic-structures": { x: 100, y: 100 },
      "subtopic-theory": { x: 100, y: 100 },
    }, 1);

    expect(updates).toHaveLength(3);
    expect(updates[0].id).toBe("topic-history");
    expect(updates[0].x).toBeCloseTo(100);
    expect(updates[0].y).toBeCloseTo(100 - getChildOrbitRingRadius(2, 1));
    expect(updates[1].id).toBe("topic-structures");
    expect(Math.round(updates[1].x)).toBe(100);
    expect(Math.round(updates[1].y)).toBe(100 + getChildOrbitRingRadius(2, 1));
    expect(updates[2].id).toBe("subtopic-theory");
    expect(updates[2].x).toBeCloseTo(100);
    expect(updates[2].y).toBeCloseTo(100 - getChildOrbitRingRadius(1, 2));
  });
});
