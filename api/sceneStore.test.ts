import { afterEach, describe, expect, test } from 'bun:test';
import { join } from 'node:path';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { clearSceneFile, createScene, deleteScene, readScenes, updateScene } from './sceneStore';

const fixtureInput = {
  name: 'QA Scene',
  perspectiveId: 'default',
  camera: { x: 1, y: 2, ratio: 1.25 },
  selectedNodeIds: ['node-1'],
  selectedEdgeIds: ['edge-1'],
  pinnedNodeIds: ['node-1'],
  filters: {
    nodeTypes: ['concept'],
    edgeTypes: ['RELATED_TO'],
    minConfidence: 0,
    maxConfidence: 1,
    searchQuery: 'floor',
  },
  expandedNodeIds: ['node-1'],
  hiddenNodeIds: [],
  layout: 'forceatlas2' as const,
  colorScheme: 'default',
  sizeBy: 'uniform' as const,
  graph: {
    nodes: [{ id: 'node-1', label: 'Node 1', type: 'concept' }],
    edges: [{ id: 'edge-1', source: 'node-1', target: 'node-2', type: 'RELATED_TO' }],
  },
};

const tempRoot = mkdtempSync(join(tmpdir(), 'vitruvius-scene-store-'));
const sceneFile = join(tempRoot, 'scenes.json');

afterEach(async () => {
  await clearSceneFile(sceneFile);
});

describe('sceneStore', () => {
  test('creates and reads a scene', async () => {
    const scene = await createScene(sceneFile, fixtureInput);
    const scenes = await readScenes(sceneFile);

    expect(scene.id).toBeString();
    expect(scenes).toHaveLength(1);
    expect(scenes[0]?.name).toBe('QA Scene');
    expect(scenes[0]?.graph.nodes).toHaveLength(1);
  });

  test('updates an existing scene', async () => {
    const created = await createScene(sceneFile, fixtureInput);
    const updated = await updateScene(sceneFile, created.id, {
      ...fixtureInput,
      name: 'Updated Scene',
      filters: {
        ...fixtureInput.filters,
        searchQuery: 'stairs',
      },
    });

    expect(updated).not.toBeNull();
    expect(updated?.name).toBe('Updated Scene');
    expect(updated?.filters.searchQuery).toBe('stairs');
  });

  test('deletes an existing scene', async () => {
    const created = await createScene(sceneFile, fixtureInput);
    const deleted = await deleteScene(sceneFile, created.id);
    const scenes = await readScenes(sceneFile);

    expect(deleted).toBe(true);
    expect(scenes).toHaveLength(0);
  });
});
