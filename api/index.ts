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

function normalizeNode(node: any) {
  if (!node) return null;
  const inferredType = node.type || node.kind || (node.quote || node.normalized_text ? 'evidence_span' : 'unknown');
  return {
    id: node.id,
    label: node.label || node.quote || node.normalized_text || node.document_title || node.document_id || node.id,
    type: inferredType,
    kind: node.kind,
    summary: node.summary,
    slug: node.slug,
    status: node.status,
    confidence: node.confidence != null ? Number(node.confidence) : undefined,
    aliases: node.aliases,
    taxonomy_path: node.taxonomy_path,
    createdAt: node.created_at,
    updatedAt: node.updated_at,
    radius: inferredType === 'taxonomy' ? 12 : inferredType === 'topic' ? 10 : inferredType === 'subtopic' ? 9 : inferredType === 'rule' ? 9 : inferredType === 'evidence_span' ? 6 : 8,
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

  let typeFilter = '';
  if (perspective === 'concepts') {
    typeFilter = 'AND c.type IN ["concept", "rule", "definition", "procedure", "exception"]';
  } else if (perspective === 'taxonomy') {
    typeFilter = 'AND (c:Taxonomy OR c:Topic OR c:Subtopic OR c.type = "concept")';
  } else if (perspective === 'evidence') {
    typeFilter = 'AND (c:EvidenceSpan OR c.type = "concept" OR c.type = "evidence_span")';
  } else if (perspective === 'regulatory') {
    typeFilter = 'AND c.type IN ["rule", "concept"]';
  }

  const records = await runQuery(`
    MATCH (c)
    WHERE (c:CanonicalNode OR c:Taxonomy OR c:Topic OR c:Subtopic OR c:EvidenceSpan)
      AND (toLower(coalesce(c.label, c.quote, c.normalized_text, c.id)) CONTAINS $q OR toLower(c.id) CONTAINS $q)
      ${typeFilter}
    RETURN c.id AS id,
           coalesce(c.label, c.quote, c.normalized_text, c.id) AS label,
           coalesce(c.type, c.kind, CASE WHEN c:EvidenceSpan THEN 'evidence_span' ELSE null END) AS type,
           c.kind AS kind
    LIMIT $limit
  `, { q: q.toLowerCase(), limit: neo4j.int(limit) });

  const results = records.map((r) => {
    const label = String(r.label ?? r.id ?? 'Unknown node');
    return {
      kind: 'node' as const,
      id: r.id,
      label,
      type: r.type || r.kind || 'unknown',
      matchType: label.toLowerCase().includes(q.toLowerCase()) ? 'label' : 'id',
      matchedField: label.toLowerCase().includes(q.toLowerCase()) ? 'label' : 'id',
    };
  });

  return c.json({ results });
});

// GET /node/:id
app.get('/node/:id', async (c) => {
  const id = c.req.param('id');

  const nodes = await runQuery(`
    MATCH (c) WHERE c.id = $id
    OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(e:EvidenceSpan)
    OPTIONAL MATCH (c)-[r]->(other)
    WHERE type(r) <> 'BELONGS_TO' AND type(r) <> 'HAS_CHILD'
    OPTIONAL MATCH (in)<-[rin]-(c)
    WHERE type(rin) <> 'BELONGS_TO' AND type(rin) <> 'HAS_CHILD'
    RETURN c,
           collect(DISTINCT e) AS evidence,
           collect(DISTINCT {rel: type(r), other: other, reasoning: r.reasoning_summary, confidence: r.confidence, assertionId: r.assertion_id}) AS outgoing,
           collect(DISTINCT {rel: type(rin), other: in, reasoning: rin.reasoning_summary, confidence: rin.confidence, assertionId: rin.assertion_id}) AS incoming
  `, { id });

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
      if (taxo) taxonomyPath.push({ id: taxo.id, label: taxo.label, kind: taxo.kind });
    }
  }

  const evidence = (n.evidence || []).filter(Boolean).map((e: any) => ({
    id: e.id,
    quote: e.quote || e.normalized_text || 'No quote',
    document_id: e.document_id,
    document_title: e.document_id,
    deep_link: e.deep_link,
    confidence: e.confidence != null ? Number(e.confidence) : undefined,
  }));

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

    result.records.forEach((record: any) => {
      record.keys.forEach((key: string) => {
        extractValue(record.get(key), nodeMap, edgeMap);
      });
    });

    return c.json({
      nodes: Array.from(nodeMap.values()),
      edges: Array.from(edgeMap.values()),
      recordCount: result.records.length,
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
    WHERE node:Taxonomy OR node:Topic OR node:Subtopic
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
    allNodes.map((node: any) => [node.id, { id: node.id, label: node.label, kind: node.kind, conceptCount: countById.get(node.id) || 0 }])
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
  const perspectives = [
    { id: 'default', name: 'All Knowledge', description: 'Everything', nodeCount: 205 },
    { id: 'concepts', name: 'Concepts Only', description: 'Domain concepts and relationships', nodeCount: 108 },
    { id: 'taxonomy', name: 'Taxonomy Browser', description: 'Hierarchy and classification', nodeCount: 86 },
    { id: 'regulatory', name: 'Regulatory Rules', description: 'Rules and dependencies', nodeCount: 40 },
    { id: 'evidence', name: 'Evidence Map', description: 'Source evidence and support links', nodeCount: 0 },
  ];
  return c.json({ perspectives });
});

// GET /perspective/:id/nodes
app.get('/perspective/:id/nodes', async (c) => {
  const id = c.req.param('id');

  let nodeQuery = '';
  let edgeQuery = '';

  if (id === 'concepts') {
    nodeQuery = `
      MATCH (c:CanonicalNode)
      WHERE c.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
      RETURN c
    `;
    edgeQuery = `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
        AND b.type IN ['concept', 'rule', 'definition', 'procedure', 'exception']
        AND type(r) IN ['RELATED_TO', 'DEPENDS_ON', 'DEFINED_BY', 'REQUIRES']
      RETURN r, a.id AS source, b.id AS target
    `;
  } else if (id === 'taxonomy') {
    nodeQuery = `
      MATCH (n) WHERE n:Taxonomy OR n:Topic OR n:Subtopic OR (n:CanonicalNode AND n.type = 'taxonomy')
      RETURN n
      UNION
      MATCH (c:CanonicalNode) WHERE c.type = 'concept'
      RETURN c AS n
      LIMIT 50
    `;
    edgeQuery = `
      MATCH (a)-[r:HAS_CHILD|BELONGS_TO]->(b)
      RETURN r, a.id AS source, b.id AS target
    `;
  } else if (id === 'regulatory') {
    nodeQuery = `
      MATCH (c:CanonicalNode) WHERE c.type IN ['rule', 'concept']
      RETURN c
    `;
    edgeQuery = `
      MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
      WHERE a.type IN ['rule', 'concept'] AND b.type IN ['rule', 'concept']
        AND type(r) IN ['REQUIRES', 'DEPENDS_ON', 'DEFINED_BY']
      RETURN r, a.id AS source, b.id AS target
    `;
  } else if (id === 'evidence') {
    nodeQuery = `
      MATCH (c:CanonicalNode)-[:SUPPORTED_BY]->(e:EvidenceSpan)
      WHERE c.type = 'concept'
      RETURN c
      UNION
      MATCH (e:EvidenceSpan)
      RETURN e AS c
      LIMIT 150
    `;
    edgeQuery = `
      MATCH (a)-[r:SUPPORTED_BY]->(b)
      RETURN r, a.id AS source, b.id AS target
    `;
  } else {
    // default: all knowledge
    nodeQuery = `
      MATCH (n) WHERE n:CanonicalNode OR n:Taxonomy OR n:Topic OR n:Subtopic
      RETURN n
    `;
    edgeQuery = `
      MATCH (a)-[r]->(b)
      WHERE type(r) IN ['HAS_CHILD', 'BELONGS_TO', 'RELATED_TO', 'DEPENDS_ON', 'DEFINED_BY', 'REQUIRES', 'SUPPORTED_BY']
      RETURN r, a.id AS source, b.id AS target
    `;
  }

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
console.log(`Vitruvius Graph API starting on http://localhost:${port}`);

export default {
  port,
  fetch: app.fetch,
};
