import { Hono } from 'hono';
import { serveStatic } from 'hono/bun';
import { cors } from 'hono/cors';
import neo4j from 'neo4j-driver';
import { join } from 'node:path';
import { createScene, deleteScene, readScenes, sceneCreateSchema, updateScene } from './sceneStore';

// ---------------------------------------------------------------------------
// Neo4j connection
// ---------------------------------------------------------------------------
const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASS || 'password'
  )
);

async function runQuery<T = any>(query: string, params?: Record<string, any>): Promise<T[]> {
  const session = driver.session();
  try {
    const result = await session.run(query, params);
    return result.records.map(r => {
      const obj: any = {};
      r.keys.forEach(k => {
        const v = r.get(k);
        if (v && typeof v === 'object' && 'properties' in v) {
          const props = { ...v.properties };
          // Neo4j Relationship has `type` metadata (not a property); Node has `labels`
          if ('type' in v && !('labels' in v)) {
            props.type = v.type;
          }
          obj[k] = props;
        } else {
          obj[k] = v;
        }
      });
      return obj;
    });
  } finally {
    await session.close();
  }
}

const scenesFilePath = join(import.meta.dir, '.data', 'scenes.json');

const DISPLAY_LABEL_LIMIT = 64;

function compactText(value: string, maxLength = DISPLAY_LABEL_LIMIT) {
  const normalized = value.replace(/\s+/g, ' ').trim();
  if (normalized.length <= maxLength) return normalized;
  return `${normalized.slice(0, maxLength - 1).trimEnd()}…`;
}

export function buildDisplayLabel(label: string, type?: string) {
  const normalized = label.replace(/\s+/g, ' ').trim();
  if (!normalized) return 'Untitled node';
  if (normalized.length <= DISPLAY_LABEL_LIMIT) return normalized;

  if (type === 'rule') {
    return `Rule · ${compactText(normalized, DISPLAY_LABEL_LIMIT - 'Rule · '.length)}`;
  }

  if (type === 'evidence_span') {
    return `Evidence · ${compactText(normalized, DISPLAY_LABEL_LIMIT - 'Evidence · '.length)}`;
  }

  return compactText(normalized);
}

function humanizeIdentifier(value: string) {
  let normalized = value.replace(/\s+/g, ' ').trim();
  for (const prefix of ['concept-', 'taxonomy-', 'topic-', 'subtopic-', 'rule-', 'definition-', 'procedure-', 'exception-', 'constraint-', 'example-', 'section-', 'sec-']) {
    if (normalized.startsWith(prefix)) {
      normalized = normalized.slice(prefix.length);
      break;
    }
  }
  normalized = normalized.replace(/[-_]+/g, ' ').trim();
  if (!normalized) return '';
  return normalized.replace(/\b\w/g, (char) => char.toUpperCase());
}

export function buildRuleDisplayLabel(props: Record<string, any>, label: string) {
  const existing = props.displayLabel || props.display_label;
  if (typeof existing === 'string' && existing.trim()) return existing.trim();

  const taxonomyPath = Array.isArray(props.taxonomy_path) ? props.taxonomy_path : [];
  const semanticAnchor = taxonomyPath.length > 0
    ? String(taxonomyPath[taxonomyPath.length - 1])
    : String(props.slug || props.id || '');
  const anchorLabel = humanizeIdentifier(semanticAnchor);

  if (anchorLabel) {
    return anchorLabel.toLowerCase().endsWith('rule') ? anchorLabel : `${anchorLabel} Rule`;
  }

  return buildDisplayLabel(label, 'rule');
}

export function buildNodeDetailQuery() {
  return `
    MATCH (c) WHERE c.id = $id
    OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(e:EvidenceSpan)
    OPTIONAL MATCH (c)-[outgoingRel]->(outgoingNode)
    OPTIONAL MATCH (incomingNode)-[incomingRel]->(c)
    RETURN c,
           collect(DISTINCT e) AS evidence,
           collect(DISTINCT {rel: type(outgoingRel), other: outgoingNode, reasoning: outgoingRel.reasoning_summary, confidence: outgoingRel.confidence, assertionId: outgoingRel.assertion_id}) AS outgoing,
           collect(DISTINCT {rel: type(incomingRel), other: incomingNode, reasoning: incomingRel.reasoning_summary, confidence: incomingRel.confidence, assertionId: incomingRel.assertion_id}) AS incoming
  `;
}

export function normalizeEvidenceSpan(e: any) {
  const props = e.properties ? e.properties : e;
  return {
    id: props.id,
    quote: props.quote || props.normalized_text || props.label || 'No quote',
    document_id: props.document_id,
    document_title: props.document_title || props.source_title || props.document_name || props.document_id,
    deep_link: props.deep_link,
    confidence: props.confidence != null ? Number(props.confidence) : undefined,
  };
}

export function normalizeNode(node: any) {
  if (!node) return null;
  const props = node.properties ? node.properties : node;
  const inferredType = props.type || props.kind || (props.quote || props.normalized_text ? 'evidence_span' : 'unknown');
  const label = props.label || props.quote || props.normalized_text || props.document_title || props.document_id || props.id;
  const displayLabel = inferredType === 'rule'
    ? buildRuleDisplayLabel(props, label)
    : props.displayLabel || props.display_label || buildDisplayLabel(label, inferredType);
  return {
    id: props.id,
    label,
    displayLabel,
    type: inferredType,
    kind: props.kind,
    summary: props.summary,
    slug: props.slug,
    status: props.status,
    confidence: props.confidence != null ? Number(props.confidence) : undefined,
    aliases: props.aliases,
    taxonomy_path: props.taxonomy_path,
    createdAt: props.created_at,
    updatedAt: props.updated_at,
    radius: inferredType === 'taxonomy' ? 12 : inferredType === 'topic' ? 10 : inferredType === 'subtopic' ? 9 : inferredType === 'rule' ? 9 : inferredType === 'evidence_span' ? 6 : 8,
  };
}

export function normalizeTaxonomyNode(node: any) {
  if (!node) return null;
  const label = String(node.label || node.id || 'Untitled taxonomy node');
  const kind = node.kind || 'taxonomy';
  return {
    id: node.id,
    label,
    displayLabel: node.displayLabel || node.display_label || buildDisplayLabel(label, kind),
    kind,
    conceptCount: Number(node.conceptCount) || 0,
  };
}

function normalizeEdge(rel: any, sourceId: string, targetId: string) {
  return {
    id: rel.assertion_id || `${sourceId}|${rel.type}|${targetId}`,
    source: sourceId,
    target: targetId,
    type: rel.type,
    reasoning: rel.reasoning_summary,
    confidence: rel.confidence != null ? Number(rel.confidence) : undefined,
    assertionId: rel.assertion_id,
  };
}

function summarizeValue(value: any): string {
  if (value == null) return '—';
  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }
  if (neo4j.isNode(value)) {
    try {
      return JSON.stringify(value.properties);
    } catch {
      return value.properties.label || value.properties.id || '[node]';
    }
  }
  if (neo4j.isRelationship(value)) {
    try {
      return JSON.stringify({ type: value.type, properties: value.properties });
    } catch {
      return `[${value.type}]`;
    }
  }
  if (neo4j.isPath(value)) {
    try {
      return JSON.stringify({
        segments: value.segments.map((segment: any) => ({
          start: segment.start.properties,
          relationship: { type: segment.relationship.type, properties: segment.relationship.properties },
          end: segment.end.properties,
        })),
      });
    } catch {
      return `path(${value.segments.length} hops)`;
    }
  }
  if (Array.isArray(value)) {
    return value.map((item) => summarizeValue(item)).join(', ');
  }
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value);
    } catch {
      return '[object]';
    }
  }
  return String(value);
}

export function buildSearchTypeFilter(perspective?: string) {
  if (perspective === 'concepts') {
    return 'AND c.type IN ["concept", "rule", "definition", "procedure", "exception"]';
  }
  if (perspective === 'taxonomy') {
    return 'AND (c:Taxonomy OR c:Topic OR c:Subtopic OR c.type = "concept")';
  }
  if (perspective === 'evidence') {
    return 'AND (c:EvidenceSpan OR c.type = "concept" OR c.type = "evidence_span")';
  }
  if (perspective === 'regulatory') {
    return 'AND c.type IN ["rule", "concept"]';
  }
  return '';
}

export function buildPerspectiveQueries(id: string) {
  if (id === 'concepts') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode)
      WHERE c.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
        AND b.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
        AND type(r) IN ['RELATED_TO', 'DEPENDS_ON', 'DEFINED_BY', 'REQUIRES']
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'taxonomy') {
    return {
      nodeQuery: `
      MATCH (n) WHERE n:Taxonomy OR n:Topic OR n:Subtopic OR (n:CanonicalNode AND n.type = 'taxonomy')
      RETURN n
      UNION
      MATCH (c:CanonicalNode) WHERE c.type = 'concept'
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a)-[r:HAS_CHILD|BELONGS_TO]->(b)
      WHERE (a:Taxonomy OR a:Topic OR a:Subtopic OR (a:CanonicalNode AND a.type = 'concept'))
        AND (b:Taxonomy OR b:Topic OR b:Subtopic OR (b:CanonicalNode AND b.type = 'concept'))
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'regulatory') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode) WHERE c.type IN ['rule', 'concept']
      RETURN c AS n
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type IN ['rule', 'concept'] AND b.type IN ['rule', 'concept']
        AND type(r) IN ['REQUIRES', 'DEPENDS_ON', 'DEFINED_BY']
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  if (id === 'evidence') {
    return {
      nodeQuery: `
      MATCH (c:CanonicalNode)-[:SUPPORTED_BY]->(e:EvidenceSpan)
      WHERE c.type = 'concept'
      RETURN c AS n
      UNION
      MATCH (e:EvidenceSpan)
      RETURN e AS n
      LIMIT 150
    `,
      edgeQuery: `
      MATCH (a:CanonicalNode)-[r:SUPPORTED_BY]->(b:EvidenceSpan)
      WHERE a.type = 'concept'
      RETURN r, a.id AS source, b.id AS target
    `,
    };
  }

  return {
    nodeQuery: `
      MATCH (n) WHERE n:CanonicalNode OR n:Taxonomy OR n:Topic OR n:Subtopic
      RETURN n
    `,
    edgeQuery: `
      MATCH (a)-[r]->(b)
      WHERE type(r) IN ['HAS_CHILD', 'BELONGS_TO', 'RELATED_TO', 'DEPENDS_ON', 'DEFINED_BY', 'REQUIRES', 'SUPPORTED_BY']
      RETURN r, a.id AS source, b.id AS target
    `,
  };
}

const PERSPECTIVE_METADATA = [
  { id: 'default', name: 'All Knowledge', description: 'All canonical and taxonomy nodes currently available' },
  { id: 'concepts', name: 'Concepts Only', description: 'Domain concepts and related rule nodes' },
  { id: 'taxonomy', name: 'Taxonomy Browser', description: 'Hierarchy, classification, and attached concepts' },
  { id: 'regulatory', name: 'Regulatory Rules', description: 'Rules and directly related concepts' },
  { id: 'evidence', name: 'Evidence Map', description: 'Concept nodes with source evidence links' },
] as const;

async function getPerspectiveNodeCount(id: string): Promise<number> {
  const { nodeQuery } = buildPerspectiveQueries(id);
  const records = await runQuery<{ nodeCount: number }>(`
    CALL {
      ${nodeQuery}
    }
    WITH n AS node
    WHERE node IS NOT NULL AND node.id IS NOT NULL
    RETURN count(DISTINCT node.id) AS nodeCount
  `);
  return Number(records[0]?.nodeCount ?? 0);
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------
const app = new Hono();

app.use(cors({ origin: '*' }));

// Health check
app.get('/health', async (c) => {
  try {
    await driver.verifyConnectivity();
    return c.json({ status: 'ok', neo4j: 'connected' });
  } catch (e: any) {
    return c.json({ status: 'error', neo4j: e.message }, 500);
  }
});

// GET /search
app.get('/search', async (c) => {
  const q = c.req.query('q') || '';
  const perspective = c.req.query('perspective');
  const limit = Math.min(parseInt(c.req.query('limit') || '20'), 100);

  if (!q.trim() || q.length < 2) return c.json({ results: [] });

  const typeFilter = buildSearchTypeFilter(perspective);

  const records = await runQuery(`
    MATCH (c)
    WHERE (c:CanonicalNode OR c:Taxonomy OR c:Topic OR c:Subtopic OR c:EvidenceSpan)
      AND (
        toLower(coalesce(c.label, c.quote, c.normalized_text, c.id)) CONTAINS $q
        OR toLower(c.id) CONTAINS $q
        OR toLower(coalesce(c.slug, '')) CONTAINS $q
        OR any(alias IN coalesce(c.aliases, []) WHERE toLower(alias) CONTAINS $q)
      )
      ${typeFilter}
    RETURN c.id AS id,
           coalesce(c.label, c.quote, c.normalized_text, c.id) AS label,
           c.display_label AS display_label,
           c.taxonomy_path AS taxonomy_path,
           coalesce(c.type, c.kind, CASE WHEN c:EvidenceSpan THEN 'evidence_span' ELSE null END) AS type,
           c.kind AS kind,
           c.slug AS slug,
           c.aliases AS aliases
    LIMIT $limit
  `, { q: q.toLowerCase(), limit: neo4j.int(limit) });

  const results = records.map((r) => {
    const label = String(r.label ?? r.id ?? 'Unknown node');
    const normalizedQuery = q.toLowerCase();
    const aliases = Array.isArray(r.aliases) ? r.aliases.map((alias) => String(alias).toLowerCase()) : [];
    const slug = typeof r.slug === 'string' ? r.slug.toLowerCase() : '';
    const matchedField = label.toLowerCase().includes(normalizedQuery)
      ? 'label'
      : aliases.some((alias) => alias.includes(normalizedQuery))
        ? 'alias'
        : slug.includes(normalizedQuery)
          ? 'slug'
          : 'id';

    return {
      kind: 'node' as const,
      id: r.id,
      label,
      displayLabel: r.type === 'rule'
        ? buildRuleDisplayLabel(r, label)
        : r.display_label || buildDisplayLabel(label, r.type || r.kind || 'unknown'),
      type: r.type || r.kind || 'unknown',
      matchType: matchedField,
      matchedField,
    };
  });

  return c.json({ results });
});

// GET /node/:id
app.get('/node/:id', async (c) => {
  const id = c.req.param('id');

  const nodes = await runQuery(buildNodeDetailQuery(), { id });

  if (!nodes.length) return c.json({ error: { code: 'NODE_NOT_FOUND', message: `Node '${id}' not found` } }, 404);

  const n = nodes[0];
  const node = normalizeNode(n.c);

  // Build taxonomy path
  const taxonomyPath: any[] = [];
  if (node?.taxonomy_path && Array.isArray(node.taxonomy_path)) {
    const taxonomyNodes = await runQuery(
      'MATCH (t) WHERE t.id IN $ids RETURN t.id AS id, t.label AS label, t.kind AS kind',
      { ids: node.taxonomy_path }
    );
    const taxonomyById = new Map(taxonomyNodes.map((taxo: any) => [taxo.id, taxo]));
    for (const taxoId of node.taxonomy_path) {
      const taxo = taxonomyById.get(taxoId);
      if (taxo) taxonomyPath.push(normalizeTaxonomyNode(taxo));
    }
  }

  const evidence = (n.evidence || []).filter(Boolean).map((e: any) => normalizeEvidenceSpan(e));
  if (node?.type === 'evidence_span' && evidence.length === 0) {
    evidence.push(normalizeEvidenceSpan(n.c));
  }

  const incoming = (n.incoming || []).filter((r: any) => r.rel && r.other).map((r: any) => ({
    relType: r.rel,
    other: normalizeNode(r.other),
    reasoning: r.reasoning,
    confidence: r.confidence != null ? Number(r.confidence) : undefined,
    assertionId: r.assertionId,
  }));

  const outgoing = (n.outgoing || []).filter((r: any) => r.rel && r.other).map((r: any) => ({
    relType: r.rel,
    other: normalizeNode(r.other),
    reasoning: r.reasoning,
    confidence: r.confidence != null ? Number(r.confidence) : undefined,
    assertionId: r.assertionId,
  }));

  return c.json({ node, taxonomyPath, incoming, outgoing, evidence });
});

// GET /edge/:id
app.get('/edge/:id', async (c) => {
  const id = c.req.param('id');

  // Try assertion_id first
  let records = await runQuery(`
    MATCH (a)-[r]->(b)
    WHERE r.assertion_id = $id
    RETURN r, a, b
  `, { id });

  // Fallback: parse as source|type|target
  if (!records.length && id.includes('|')) {
    const [sourceId, type, targetId] = id.split('|');
    records = await runQuery(`
      MATCH (a)-[r]->(b)
      WHERE a.id = $sourceId AND type(r) = $type AND b.id = $targetId
      RETURN r, a, b
    `, { sourceId, type, targetId });
  }

  if (!records.length) {
    return c.json({ error: { code: 'EDGE_NOT_FOUND', message: `Edge '${id}' not found` } }, 404);
  }

  const rec = records[0];
  const edge = normalizeEdge(rec.r, rec.a.id, rec.b.id);
  const edgeEvidence = edge.type === 'SUPPORTED_BY'
    ? [rec.a, rec.b]
        .map((node: any) => normalizeNode(node))
        .filter((node: any) => node?.type === 'evidence_span')
        .map((node: any) => ({
          id: node.id,
          quote: node.label,
          document_id: node.id,
          document_title: node.label,
          deep_link: undefined,
          confidence: undefined,
        }))
    : [];
  return c.json({
    edge,
    source: normalizeNode(rec.a),
    target: normalizeNode(rec.b),
    evidence: edgeEvidence,
  });
});

// POST /query
app.post('/query', async (c) => {
  const body = await c.req.json();
  const cypher = (body.cypher || '').trim();

  if (!cypher) {
    return c.json({ error: { code: 'BAD_REQUEST', message: 'cypher query is required' } }, 400);
  }

  function extractValue(value: any, nodeMap: Map<string, any>, edgeMap: Map<string, any>) {
    if (neo4j.isNode(value)) {
      const n = normalizeNode(value.properties);
      if (n) nodeMap.set(n.id, n);
    } else if (neo4j.isPath(value)) {
      value.segments.forEach((seg: any) => {
        const start = normalizeNode(seg.start.properties);
        const end = normalizeNode(seg.end.properties);
        if (start) nodeMap.set(start.id, start);
        if (end) nodeMap.set(end.id, end);
        if (start && end) {
          const rel = normalizeEdge(
            { ...seg.relationship.properties, type: seg.relationship.type },
            start.id,
            end.id
          );
          edgeMap.set(rel.id, rel);
        }
      });
    } else if (Array.isArray(value)) {
      value.forEach(v => extractValue(v, nodeMap, edgeMap));
    }
  }

  const session = driver.session({ defaultAccessMode: neo4j.session.READ });
  try {
    const result = await session.run(cypher);
    const nodeMap = new Map<string, any>();
    const edgeMap = new Map<string, any>();
    const rows = result.records.map((record: any, index: number) => {
      const values: Record<string, string> = {};
      record.keys.forEach((key: string) => {
        values[key] = summarizeValue(record.get(key));
      });
      return { id: `row-${index}`, values };
    });

    result.records.forEach((record: any) => {
      record.keys.forEach((key: string) => {
        extractValue(record.get(key), nodeMap, edgeMap);
      });
    });

      return c.json({
        nodes: Array.from(nodeMap.values()),
        edges: Array.from(edgeMap.values()),
        recordCount: result.records.length,
        rows,
      });
  } catch (err: any) {
    return c.json({ error: { code: 'QUERY_ERROR', message: err.message } }, 400);
  } finally {
    await session.close();
  }
});

// GET /expand
app.get('/expand', async (c) => {
  const nodeId = c.req.query('nodeId');
  const relTypes = c.req.query('relTypes')?.split(',').filter(Boolean);
  const direction = c.req.query('direction') || 'both';
  const limit = Math.min(parseInt(c.req.query('limit') || '50'), 200);

  if (!nodeId) return c.json({ error: { code: 'BAD_REQUEST', message: 'nodeId is required' } }, 400);

  let relFilter = '';
  if (relTypes && relTypes.length) {
    relFilter = 'AND type(r) IN $relTypes';
  }

  let query = '';
  if (direction === 'out') {
    query = `
      MATCH (c)-[r]->(other)
      WHERE c.id = $nodeId ${relFilter}
      RETURN c.id AS source, other, r
      LIMIT $limit
    `;
  } else if (direction === 'in') {
    query = `
      MATCH (other)-[r]->(c)
      WHERE c.id = $nodeId ${relFilter}
      RETURN other AS source, c AS other, r
      LIMIT $limit
    `;
  } else {
    query = `
      MATCH (c)-[r]-(other)
      WHERE c.id = $nodeId ${relFilter}
      RETURN c.id AS source, other, r
      LIMIT $limit
    `;
  }

  const records = await runQuery(query, { nodeId, relTypes: relTypes || [], limit: neo4j.int(limit) });

  const nodeIds = new Set([nodeId]);
  const edgeSet = new Map<string, any>();

  records.forEach((rec: any) => {
    const other = normalizeNode(rec.other);
    if (other) nodeIds.add(other.id);

    const sourceId = rec.source || nodeId;
    const targetId = rec.other?.id || rec.other?.properties?.id;
    if (targetId) {
      const edge = normalizeEdge(rec.r, sourceId, targetId);
      edgeSet.set(edge.id, edge);
    }
  });

  // Fetch all nodes
  const allNodes = await runQuery(`
    MATCH (n) WHERE n.id IN $ids
    RETURN n
  `, { ids: Array.from(nodeIds) });

  return c.json({
    nodeId,
    neighbors: records.map((rec: any) => ({
      node: normalizeNode(rec.other),
      relType: rec.r?.type,
      direction: direction,
    })).filter((n: any) => n.node),
    nodes: allNodes.map((r: any) => normalizeNode(r.n)).filter(Boolean),
    edges: Array.from(edgeSet.values()),
  });
});

// GET /path
app.get('/path', async (c) => {
  const from = c.req.query('from');
  const to = c.req.query('to');
  const maxHops = Math.min(parseInt(c.req.query('maxHops') || '6'), 12);
  const limit = Math.min(parseInt(c.req.query('limit') || '5'), 20);

  if (!from || !to) return c.json({ error: { code: 'BAD_REQUEST', message: 'from and to are required' } }, 400);

  const records = await runQuery(`
    MATCH path = shortestPath((a)-[*1..${maxHops}]-(b))
    WHERE a.id = $from AND b.id = $to
    RETURN path
    LIMIT $limit
  `, { from, to, limit: neo4j.int(limit) });

  if (!records.length) {
    return c.json({ error: { code: 'PATH_NOT_FOUND', message: `No path found between '${from}' and '${to}' within ${maxHops} hops` } }, 404);
  }

  const paths = records.map((rec: any) => {
    const path = rec.path;
    const nodes = path.segments.map((s: any) => normalizeNode(s.start.properties)).filter(Boolean);
    nodes.push(normalizeNode(path.end.properties));
    const edges = path.segments.map((s: any) => normalizeEdge(
      { ...s.relationship.properties, type: s.relationship.type },
      s.start.properties.id,
      s.end.properties.id
    ));
    return { length: edges.length, nodes, edges };
  });

  return c.json({ paths });
});

// GET /taxonomy
app.get('/taxonomy', async (c) => {
  const allNodes = await runQuery(`
    MATCH (n)
    WHERE n:Taxonomy OR n:Topic OR n:Subtopic
    RETURN n.id AS id, n.label AS label, n.kind AS kind
    ORDER BY label
  `);

  const edges = await runQuery(`
    MATCH (parent)-[:HAS_CHILD]->(child)
    WHERE parent:Taxonomy OR parent:Topic OR parent:Subtopic
    RETURN parent.id AS parentId, child.id AS childId
  `);

  const conceptCounts = await runQuery(`
    MATCH (c:CanonicalNode)-[:BELONGS_TO]->(node)
    WHERE c.type = 'concept' AND (node:Taxonomy OR node:Topic OR node:Subtopic)
    RETURN node.id AS id, count(DISTINCT c) AS conceptCount
  `);

  const countById = new Map(conceptCounts.map((row: any) => [row.id, Number(row.conceptCount) || 0]));
  const childrenByParent = new Map<string, string[]>();
  const childIds = new Set<string>();

  for (const edge of edges) {
    childIds.add(edge.childId);
    if (!childrenByParent.has(edge.parentId)) childrenByParent.set(edge.parentId, []);
    childrenByParent.get(edge.parentId)!.push(edge.childId);
  }

  const nodeById = new Map(
    allNodes.map((node: any) => [
      node.id,
      normalizeTaxonomyNode({ ...node, conceptCount: countById.get(node.id) || 0 }),
    ])
  );

  function buildTree(nodeId: string): any {
    const node = nodeById.get(nodeId);
    if (!node) return null;
    const children = (childrenByParent.get(nodeId) || [])
      .map((childId) => buildTree(childId))
      .filter(Boolean)
      .sort((a: any, b: any) => a.label.localeCompare(b.label));
    return { ...node, children };
  }

  const roots = allNodes
    .filter((node: any) => !childIds.has(node.id))
    .map((node: any) => buildTree(node.id))
    .filter(Boolean)
    .sort((a: any, b: any) => a.label.localeCompare(b.label));

  return c.json({ roots });
});

// GET /perspectives
app.get('/perspectives', async (c) => {
  const perspectives = await Promise.all(
    PERSPECTIVE_METADATA.map(async (perspective) => ({
      ...perspective,
      nodeCount: await getPerspectiveNodeCount(perspective.id),
    }))
  );
  return c.json({ perspectives });
});

// GET /perspective/:id/nodes
app.get('/perspective/:id/nodes', async (c) => {
  const id = c.req.param('id');

  const { nodeQuery, edgeQuery } = buildPerspectiveQueries(id);

  const nodes = await runQuery(nodeQuery);
  const edges = await runQuery(edgeQuery);

  return c.json({
    nodes: nodes.map((r: any) => normalizeNode(r.n || r.c)).filter(Boolean),
    edges: edges.map((r: any) => normalizeEdge(r.r, r.source, r.target)),
  });
});

// Scene storage (file-backed)
app.get('/scenes', async (c) => {
  const scenes = await readScenes(scenesFilePath);
  return c.json({
    scenes: scenes
      .map((scene) => ({
        id: scene.id,
        name: scene.name,
        savedAt: scene.savedAt,
        perspectiveId: scene.perspectiveId,
      }))
      .sort((a, b) => (b.savedAt || '').localeCompare(a.savedAt || '')),
  });
});

// POST /scene/save
app.post('/scene/save', async (c) => {
  const body = sceneCreateSchema.parse(await c.req.json());
  const scene = await createScene(scenesFilePath, body);
  return c.json({ sceneId: scene.id, url: `/explore?scene=${scene.id}`, scene });
});

app.put('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const body = sceneCreateSchema.parse(await c.req.json());
  const scene = await updateScene(scenesFilePath, id, body);
  if (!scene) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json({ scene });
});

app.delete('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const deleted = await deleteScene(scenesFilePath, id);
  if (!deleted) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json({ ok: true, id });
});

// GET /scene/:id
app.get('/scene/:id', async (c) => {
  const id = c.req.param('id');
  const scenes = await readScenes(scenesFilePath);
  const scene = scenes.find((entry) => entry.id === id);
  if (!scene) return c.json({ error: { code: 'NOT_FOUND', message: 'Scene not found' } }, 404);
  return c.json(scene);
});

// Serve static frontend build
app.use('/*', serveStatic({ root: '../explorer/dist' }));

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
const port = parseInt(process.env.PORT || '3000');
if (import.meta.main) {
  console.log(`Vitruvius Graph API starting on http://localhost:${port}`);
}

export default {
  port,
  fetch: app.fetch,
};
