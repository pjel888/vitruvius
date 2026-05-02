import { describe, expect, test } from 'bun:test';
import api from './index';

async function json(path: string) {
  const response = await api.fetch(new Request(`http://localhost${path}`));
  const body = await response.json() as any;
  expect(response.status).toBe(200);
  return body;
}

describe('Explorer performance data contract', () => {
  test('render profile keeps the full learner-facing graph renderable while bounding payload metadata', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const fullResponse = await api.fetch(new Request('http://localhost/perspective/aec-mepfs/nodes'));
    const fullText = await fullResponse.text();
    const renderResponse = await api.fetch(new Request('http://localhost/perspective/aec-mepfs/nodes?profile=render'));
    const renderText = await renderResponse.text();
    const render = JSON.parse(renderText);
    const firstNode = render.nodes[0];
    const firstEdge = render.edges[0];

    expect(fullResponse.status).toBe(200);
    expect(renderResponse.status).toBe(200);
    expect(render.nodes.length).toBe(10018);
    expect(render.edges.length).toBe(13805);
    expect(render.nodes.some((node: any) => node.id === 'VTN-DOM-0002711')).toBe(true);
    expect(render.nodes.every((node: any) => node.type !== 'source_reference')).toBe(true);
    expect(render.nodes.every((node: any) => node.type !== 'source_rights')).toBe(true);
    expect(render.nodes.every((node: any) => node.type !== 'provenance')).toBe(true);
    expect(Buffer.byteLength(renderText)).toBeLessThan(Buffer.byteLength(fullText));
    expect(Buffer.byteLength(renderText)).toBeLessThan(7_500_000);
    expect(firstNode).toEqual(expect.objectContaining({ id: expect.any(String), label: expect.any(String), type: expect.any(String) }));
    expect(firstNode.aliases.length).toBeGreaterThan(0);
    expect(firstNode.taxonomy_path.length).toBeGreaterThan(0);
    expect(firstNode.summary).toBeUndefined();
    expect(firstNode.slug).toBeUndefined();
    expect(firstNode.status).toBeUndefined();
    expect(firstEdge).toEqual(expect.objectContaining({ id: expect.any(String), source: expect.any(String), target: expect.any(String), type: expect.any(String) }));
    expect(firstEdge.reasoning).toBeUndefined();
    expect(firstEdge.assertionId).toBeUndefined();
    expect(firstEdge.relationType).toBeUndefined();
    expect(firstEdge.rationale).toBeUndefined();
    expect(firstEdge.sourceFamilyIds).toBeUndefined();
    expect(firstEdge.official_url).toBeUndefined();
    expect(firstEdge.source_path).toBeUndefined();
    expect(firstEdge.quote).toBeUndefined();
  });

  test('default render contract is full graph, not a bounded or selected-neighborhood subgraph', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const render = await json('/perspective/aec-mepfs/nodes?profile=render');
    const search = await json('/search?perspective=aec-mepfs&q=Tropical%20Architecture&limit=20');
    const expand = await json('/expand?nodeId=VTN-DOM-0002711&depth=1&limit=200');
    const renderNodeIds = new Set(render.nodes.map((node: any) => node.id));
    const renderEdgeIds = new Set(render.edges.map((edge: any) => edge.id));

    expect(render.nodes.length).toBe(10018);
    expect(render.edges.length).toBe(13805);
    expect(search.results.some((result: any) => result.id === 'VTN-DOM-0002711')).toBe(true);
    expect(renderNodeIds.has('VTN-DOM-0002711')).toBe(true);
    expect(expand.nodes.every((node: any) => renderNodeIds.has(node.id))).toBe(true);
    expect(expand.edges.every((edge: any) => renderEdgeIds.has(edge.id))).toBe(true);
    expect(render.nodes.length).toBeGreaterThan(expand.nodes.length);
    expect(render.edges.length).toBeGreaterThan(expand.edges.length);
  });



  test('render profile keeps serialized memory pressure under stable per-record budgets', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const renderResponse = await api.fetch(new Request('http://localhost/perspective/aec-mepfs/nodes?profile=render'));
    const renderText = await renderResponse.text();
    const render = JSON.parse(renderText);
    const nodeBytes = Buffer.byteLength(JSON.stringify(render.nodes));
    const edgeBytes = Buffer.byteLength(JSON.stringify(render.edges));
    const averageNodeBytes = nodeBytes / render.nodes.length;
    const averageEdgeBytes = edgeBytes / render.edges.length;

    expect(renderResponse.status).toBe(200);
    expect(Buffer.byteLength(renderText)).toBeLessThan(5_500_000);
    expect(averageNodeBytes).toBeLessThan(400);
    expect(averageEdgeBytes).toBeLessThan(170);
    expect(render.nodes.every((node: any) => node.summary === undefined && node.slug === undefined && node.status === undefined)).toBe(true);
    expect(render.edges.every((edge: any) => (
      edge.reasoning === undefined
      && edge.assertionId === undefined
      && edge.relationType === undefined
      && edge.rationale === undefined
      && edge.sourceFamilyIds === undefined
    ))).toBe(true);
  });

  test('indexed Explorer search and detail paths preserve source-rights safety', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const search = await json('/search?perspective=aec-mepfs&q=Tropical%20Architecture&limit=12');
    const alias = await json('/search?perspective=aec-mepfs&q=ARC&limit=5');
    const node = await json('/node/VTN-DOM-0002711');
    const expand = await json('/expand?nodeId=VTN-DOM-0000001&relTypes=HAS_CHILD&direction=out&depth=2');
    const path = await json('/path?from=VTN-DOM-0000001&to=VTN-DOM-0000002');
    const serialized = JSON.stringify({ search, alias, node, expand, path });

    expect(search.results.some((result: any) => result.id === 'VTN-DOM-0002711')).toBe(true);
    expect(alias.results[0]).toEqual(expect.objectContaining({ id: 'VTN-DOM-0000001' }));
    expect(['alias', 'pathCode']).toContain(alias.results[0].matchedField);
    expect(node.node.id).toBe('VTN-DOM-0002711');
    expect(node.taxonomyPath.length).toBeGreaterThan(0);
    expect(expand.nodes.length).toBeGreaterThan(2);
    expect(expand.edges.every((edge: any) => edge.type === 'HAS_CHILD')).toBe(true);
    expect(path.paths[0].length).toBe(1);
    expect(serialized).not.toContain('Local raw-source filename metadata');
    expect(serialized).not.toContain('raw-source filename metadata');
    expect(serialized).not.toContain('metadata-only source-family reference');
    expect(serialized).not.toContain('protected payload');
    expect(serialized).not.toContain('planning_reference_only');
  });

  test('indexed API operations stay within stable non-browser latency budgets', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
    await json('/perspective/aec-mepfs/nodes?profile=render');
    const operations = [
      '/search?perspective=aec-mepfs&q=Architecture&limit=20',
      '/search?perspective=aec-mepfs&q=Tropical%20Architecture&limit=20',
      '/search?perspective=aec-mepfs&q=ARC&limit=20',
      '/node/VTN-DOM-0000001',
      '/edge/VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
      '/expand?nodeId=VTN-DOM-0000001&depth=1&limit=200',
      '/expand?nodeId=VTN-DOM-0000001&depth=2&limit=200',
      '/path?from=VTN-DOM-0000001&to=VTN-DOM-0000002',
    ];

    const durations: number[] = [];
    for (const operation of operations) {
      const startedAt = performance.now();
      await json(operation);
      durations.push(performance.now() - startedAt);
    }

    expect(Math.max(...durations)).toBeLessThan(250);
    expect(durations.filter((duration) => duration < 120).length).toBeGreaterThanOrEqual(6);
  });
});
