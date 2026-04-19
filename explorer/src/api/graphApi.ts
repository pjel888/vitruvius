import type {
  GraphNode,
  GraphEdge,
  TaxonomyNode,
  NodeDetail,
  EdgeDetail,
  SearchResult,
  Perspective,
  RelationDetail,
  EvidenceSpan,
} from '../types';

// ---------------------------------------------------------------------------
// Mock data derived from live Neo4j introspection (2026-04-19)
// ---------------------------------------------------------------------------

const TAXONOMY_ROOTS: TaxonomyNode[] = [
  { id: 'taxonomy-accessibility', label: 'Accessibility', kind: 'taxonomy', conceptCount: 3, children: [
    { id: 'topic-barrier-free-design', label: 'Barrier-Free Design', kind: 'topic', conceptCount: 3, children: [
      { id: 'subtopic-routes', label: 'Routes', kind: 'subtopic', conceptCount: 2, children: [] },
      { id: 'subtopic-ramps', label: 'Ramps', kind: 'subtopic', conceptCount: 1, children: [] },
    ]},
  ]},
  { id: 'taxonomy-architecture', label: 'Architecture', kind: 'taxonomy', conceptCount: 8, children: [] },
  { id: 'taxonomy-building-code', label: 'Building Code', kind: 'taxonomy', conceptCount: 15, children: [
    { id: 'topic-floor-area', label: 'Floor Area', kind: 'topic', conceptCount: 5, children: [
      { id: 'subtopic-gfa', label: 'Gross Floor Area', kind: 'subtopic', conceptCount: 3, children: [] },
      { id: 'subtopic-amvb', label: 'AMVB', kind: 'subtopic', conceptCount: 2, children: [] },
    ]},
    { id: 'topic-building-height', label: 'Building Height', kind: 'topic', conceptCount: 4, children: [] },
  ]},
  { id: 'taxonomy-building-systems', label: 'Building Systems', kind: 'taxonomy', conceptCount: 6, children: [] },
  { id: 'taxonomy-construction-execution', label: 'Construction Execution', kind: 'taxonomy', conceptCount: 4, children: [] },
  { id: 'taxonomy-energy-sustainability', label: 'Energy Sustainability', kind: 'taxonomy', conceptCount: 5, children: [] },
  { id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', kind: 'taxonomy', conceptCount: 7, children: [] },
  { id: 'taxonomy-project-practice', label: 'Project Practice', kind: 'taxonomy', conceptCount: 3, children: [] },
  { id: 'taxonomy-regulatory-permits', label: 'Regulatory Permits', kind: 'taxonomy', conceptCount: 9, children: [] },
  { id: 'taxonomy-site-infrastructure', label: 'Site Infrastructure', kind: 'taxonomy', conceptCount: 4, children: [] },
  { id: 'taxonomy-spaces-occupancy', label: 'Spaces Occupancy', kind: 'taxonomy', conceptCount: 6, children: [] },
];

const CONCEPTS: GraphNode[] = [
  { id: 'concept-floor-area', label: 'Floor Area', type: 'concept', summary: 'The overall size of a proposed building/structure characterized by gross floor area (GFA) or total gross floor area (TGFA).', confidence: 0.92, aliases: ['GFA', 'TGFA'] },
  { id: 'concept-building-height', label: 'Building Height', type: 'concept', summary: 'The maximum height to be allowed for buildings/structures based on their proposed use or occupancy.', confidence: 0.88, aliases: ['BHL'] },
  { id: 'concept-amvb', label: 'AMVB', type: 'concept', summary: 'Allowable Maximum Building Volume — the maximum volume expressed in cubic meters.', confidence: 0.85 },
  { id: 'concept-ambf', label: 'AMBF', type: 'concept', summary: 'Allowable Maximum Building Footprint — the overall dimensions of the allowable maximum building footprint.', confidence: 0.87 },
  { id: 'concept-building-bulk', label: 'Building Bulk', type: 'concept', summary: 'The overall size of a proposed building/structure as characterized by the expanse of its GFA, AMBF, and BHL.', confidence: 0.90 },
  { id: 'concept-accessible-ramps', label: 'Accessible Ramps', type: 'concept', summary: 'Accessible ramps shall have facilities and features provided where changes in level occur.', confidence: 0.78, aliases: ['accessible ramps', 'ramps for accessibility'] },
  { id: 'concept-setback', label: 'Setback', type: 'concept', summary: 'The required distance from a property line to a building face.', confidence: 0.82 },
  { id: 'concept-gfa', label: 'Gross Floor Area', type: 'concept', summary: 'The total floor area within the building measured to the outer surface of exterior walls.', confidence: 0.95 },
  { id: 'concept-mezzanine', label: 'Mezzanine', type: 'concept', summary: 'An intermediate level between the floor and ceiling of any story.', confidence: 0.76 },
  { id: 'concept-dropped-sidewalk', label: 'Dropped Sidewalk', type: 'concept', summary: 'A sidewalk lowered to meet grade changes without ramps.', confidence: 0.72 },
];

const RULES: GraphNode[] = [
  { id: 'rule-floor-area-height', label: 'Floor Area determines Building Height', type: 'rule', summary: 'The building bulk expressed in cubic meters must not exceed the established AMVB above grade.', confidence: 0.85 },
  { id: 'rule-accessible-ramp-slope', label: 'Accessible Ramp Slope Limit', type: 'rule', summary: 'Accessible ramps shall not exceed a 1:12 slope ratio.', confidence: 0.91 },
  { id: 'rule-setback-minimum', label: 'Minimum Setback Rule', type: 'rule', summary: 'All buildings shall maintain the minimum setback distance from property lines.', confidence: 0.88 },
  { id: 'rule-mezzanine-area', label: 'Mezzanine Area Limit', type: 'rule', summary: 'The area of a mezzanine shall not exceed one-third of the area of the room or space in which it is located.', confidence: 0.83 },
];

const ALL_NODES: GraphNode[] = [
  ...TAXONOMY_ROOTS.map(t => ({ id: t.id, label: t.label, type: 'taxonomy', kind: t.kind, radius: 12 })),
  ...TAXONOMY_ROOTS.flatMap(t => t.children).map(t => ({ id: t.id, label: t.label, type: 'topic', kind: t.kind, radius: 10 })),
  ...TAXONOMY_ROOTS.flatMap(t => t.children).flatMap(t => t.children).map(t => ({ id: t.id, label: t.label, type: 'subtopic', kind: t.kind, radius: 9 })),
  ...CONCEPTS.map(n => ({ ...n, radius: 8 })),
  ...RULES.map(n => ({ ...n, radius: 9 })),
];

const ALL_EDGES: GraphEdge[] = [
  // Taxonomy hierarchy
  { id: 'e1', source: 'taxonomy-building-code', target: 'topic-floor-area', type: 'HAS_CHILD' },
  { id: 'e2', source: 'topic-floor-area', target: 'subtopic-gfa', type: 'HAS_CHILD' },
  { id: 'e3', source: 'topic-floor-area', target: 'subtopic-amvb', type: 'HAS_CHILD' },
  { id: 'e4', source: 'taxonomy-building-code', target: 'topic-building-height', type: 'HAS_CHILD' },
  { id: 'e5', source: 'taxonomy-accessibility', target: 'topic-barrier-free-design', type: 'HAS_CHILD' },
  { id: 'e6', source: 'topic-barrier-free-design', target: 'subtopic-routes', type: 'HAS_CHILD' },
  { id: 'e7', source: 'topic-barrier-free-design', target: 'subtopic-ramps', type: 'HAS_CHILD' },
  // Belongs to
  { id: 'e8', source: 'concept-floor-area', target: 'topic-floor-area', type: 'BELONGS_TO' },
  { id: 'e9', source: 'concept-building-height', target: 'topic-building-height', type: 'BELONGS_TO' },
  { id: 'e10', source: 'concept-amvb', target: 'subtopic-amvb', type: 'BELONGS_TO' },
  { id: 'e11', source: 'concept-gfa', target: 'subtopic-gfa', type: 'BELONGS_TO' },
  { id: 'e12', source: 'concept-accessible-ramps', target: 'subtopic-ramps', type: 'BELONGS_TO' },
  { id: 'e13', source: 'concept-setback', target: 'taxonomy-regulatory-permits', type: 'BELONGS_TO' },
  { id: 'e14', source: 'concept-mezzanine', target: 'taxonomy-spaces-occupancy', type: 'BELONGS_TO' },
  // Concept relationships
  { id: 'e15', source: 'concept-floor-area', target: 'concept-building-height', type: 'DEPENDS_ON', reasoning: 'Floor area directly constrains the maximum building height through the AMVB calculation.', confidence: 0.82, assertionId: 'asst-001' },
  { id: 'e16', source: 'concept-building-bulk', target: 'concept-floor-area', type: 'DEFINED_BY', reasoning: 'Building bulk is defined by the expanse of its GFA, AMBF, and BHL.', confidence: 0.90, assertionId: 'asst-002' },
  { id: 'e17', source: 'concept-amvb', target: 'concept-building-height', type: 'REQUIRES', reasoning: 'AMVB calculation requires the building height limit as an input.', confidence: 0.78, assertionId: 'asst-003' },
  { id: 'e18', source: 'concept-floor-area', target: 'concept-gfa', type: 'DEFINED_BY', reasoning: 'Floor area is defined by gross floor area.', confidence: 0.95, assertionId: 'asst-004' },
  { id: 'e19', source: 'concept-floor-area', target: 'concept-ambf', type: 'RELATED_TO', reasoning: 'Both are measures of building size.', confidence: 0.70, assertionId: 'asst-005' },
  { id: 'e20', source: 'concept-setback', target: 'concept-building-height', type: 'DEPENDS_ON', reasoning: 'Setback requirements may affect allowable building height.', confidence: 0.65, assertionId: 'asst-006' },
  { id: 'e21', source: 'rule-floor-area-height', target: 'concept-floor-area', type: 'DEFINED_BY', reasoning: 'Rule is defined by the floor area concept.', confidence: 0.88, assertionId: 'asst-007' },
  { id: 'e22', source: 'rule-floor-area-height', target: 'concept-building-height', type: 'REQUIRES', reasoning: 'Rule requires building height compliance.', confidence: 0.85, assertionId: 'asst-008' },
  { id: 'e23', source: 'rule-accessible-ramp-slope', target: 'concept-accessible-ramps', type: 'DEFINED_BY', reasoning: 'Rule defines requirements for accessible ramps.', confidence: 0.91, assertionId: 'asst-009' },
];

const PERSPECTIVES: Perspective[] = [
  { id: 'default', name: 'All Knowledge', description: 'Everything', nodeTypes: ['taxonomy','topic','subtopic','concept','rule','definition','procedure','exception'], edgeTypes: ['HAS_CHILD','BELONGS_TO','RELATED_TO','DEPENDS_ON','DEFINED_BY','REQUIRES','SUPPORTED_BY'] },
  { id: 'concepts', name: 'Concepts Only', description: 'Domain concepts and their relationships', nodeTypes: ['concept','rule','definition','procedure','exception'], edgeTypes: ['RELATED_TO','DEPENDS_ON','DEFINED_BY','REQUIRES'] },
  { id: 'taxonomy', name: 'Taxonomy Browser', description: 'Hierarchy and classification', nodeTypes: ['taxonomy','topic','subtopic','concept'], edgeTypes: ['HAS_CHILD','BELONGS_TO'] },
  { id: 'regulatory', name: 'Regulatory Rules', description: 'Rules, requirements, and dependencies', nodeTypes: ['rule','concept'], edgeTypes: ['REQUIRES','DEPENDS_ON','DEFINED_BY'] },
];

// ---------------------------------------------------------------------------
// API functions
// ---------------------------------------------------------------------------

export async function searchNodes(q: string, perspectiveId?: string, limit = 20): Promise<SearchResult[]> {
  await delay(150);
  const term = q.toLowerCase().trim();
  if (!term) return [];

  const perspective = PERSPECTIVES.find(p => p.id === perspectiveId);
  const allowedTypes = perspective?.nodeTypes;

  const results: SearchResult[] = [];
  for (const node of ALL_NODES) {
    if (allowedTypes && !allowedTypes.includes(node.type)) continue;

    let matchType = '';
    let matchedField = '';

    if (node.label.toLowerCase() === term) { matchType = 'exact'; matchedField = 'label'; }
    else if (node.label.toLowerCase().startsWith(term)) { matchType = 'prefix'; matchedField = 'label'; }
    else if (node.label.toLowerCase().includes(term)) { matchType = 'substring'; matchedField = 'label'; }
    else if (node.aliases?.some(a => a.toLowerCase().includes(term))) { matchType = 'alias'; matchedField = 'aliases'; }
    else if (node.id.toLowerCase().includes(term)) { matchType = 'id'; matchedField = 'id'; }

    if (matchType) {
      results.push({ kind: 'node', id: node.id, label: node.label, type: node.type, matchType, matchedField });
    }
  }

  return results.slice(0, limit);
}

export async function getNode(id: string): Promise<NodeDetail | null> {
  await delay(200);
  const node = ALL_NODES.find(n => n.id === id);
  if (!node) return null;

  const taxonomyPath: TaxonomyNode[] = [];
  // Build a simple taxonomy path for demo
  if (node.type === 'concept' || node.type === 'rule') {
    const belongsEdge = ALL_EDGES.find(e => e.source === id && e.type === 'BELONGS_TO');
    if (belongsEdge) {
      const taxo = findTaxonomyNode(belongsEdge.target);
      if (taxo) taxonomyPath.push(taxo);
      // Find parent
      const parentEdge = ALL_EDGES.find(e => e.target === taxo?.id && e.type === 'HAS_CHILD');
      if (parentEdge) {
        const parent = findTaxonomyNode(parentEdge.source);
        if (parent) taxonomyPath.unshift(parent);
      }
    }
  }

  const incoming: RelationDetail[] = ALL_EDGES
    .filter(e => e.target === id)
    .map(e => ({
      relType: e.type,
      other: ALL_NODES.find(n => n.id === e.source)!,
      reasoning: e.reasoning,
      confidence: e.confidence,
      assertionId: e.assertionId,
    }));

  const outgoing: RelationDetail[] = ALL_EDGES
    .filter(e => e.source === id)
    .map(e => ({
      relType: e.type,
      other: ALL_NODES.find(n => n.id === e.target)!,
      reasoning: e.reasoning,
      confidence: e.confidence,
      assertionId: e.assertionId,
    }));

  const evidence: EvidenceSpan[] = node.type !== 'taxonomy' && node.type !== 'topic' && node.type !== 'subtopic'
    ? [{
        id: `span-${id}`,
        quote: `Evidence supporting ${node.label} from source document.`,
        document_id: 'doc-sample',
        document_title: 'Sample Document',
        deep_link: `/viewer/sample?section=${id}`,
        confidence: node.confidence ?? 0.8,
      }]
    : [];

  return { node, taxonomyPath, incoming, outgoing, evidence };
}

export async function getEdgeDetail(edgeId: string): Promise<EdgeDetail | null> {
  await delay(150);
  const edge = ALL_EDGES.find(e => e.id === edgeId);
  if (!edge) return null;
  const source = ALL_NODES.find(n => n.id === edge.source)!;
  const target = ALL_NODES.find(n => n.id === edge.target)!;
  return {
    edge,
    source,
    target,
    evidence: edge.confidence ? [{
      id: `span-${edgeId}`,
      quote: edge.reasoning || 'Supporting evidence for this relationship.',
      document_id: 'doc-sample',
      document_title: 'Sample Document',
      confidence: edge.confidence,
    }] : [],
  };
}

export async function getTaxonomy(): Promise<TaxonomyNode[]> {
  await delay(200);
  return TAXONOMY_ROOTS;
}

export async function getPerspectives(): Promise<Perspective[]> {
  await delay(50);
  return PERSPECTIVES;
}

export async function getNodesForPerspective(perspectiveId: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  await delay(300);
  const p = PERSPECTIVES.find(x => x.id === perspectiveId) ?? PERSPECTIVES[0];
  const nodes = ALL_NODES.filter(n => p.nodeTypes.includes(n.type));
  const nodeIds = new Set(nodes.map(n => n.id));
  const edges = ALL_EDGES.filter(e => p.edgeTypes.includes(e.type) && nodeIds.has(e.source) && nodeIds.has(e.target));
  return { nodes, edges };
}

export async function expandNode(nodeId: string, relTypes?: string[]): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  await delay(200);
  const edges = ALL_EDGES.filter(e =>
    (e.source === nodeId || e.target === nodeId) &&
    (!relTypes || relTypes.includes(e.type))
  );
  const nodeIds = new Set([nodeId]);
  edges.forEach(e => { nodeIds.add(e.source); nodeIds.add(e.target); });
  const nodes = ALL_NODES.filter(n => nodeIds.has(n.id));
  return { nodes, edges };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function delay(ms: number) {
  return new Promise(r => setTimeout(r, ms));
}

function findTaxonomyNode(id: string): TaxonomyNode | undefined {
  function walk(nodes: TaxonomyNode[]): TaxonomyNode | undefined {
    for (const n of nodes) {
      if (n.id === id) return n;
      const found = walk(n.children);
      if (found) return found;
    }
    return undefined;
  }
  return walk(TAXONOMY_ROOTS);
}
