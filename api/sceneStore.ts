import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';
import { z } from 'zod';

export const sceneSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  savedAt: z.string(),
  perspectiveId: z.string().min(1),
  camera: z.object({
    x: z.number(),
    y: z.number(),
    ratio: z.number(),
  }),
  selectedNodeIds: z.array(z.string()),
  selectedEdgeIds: z.array(z.string()),
  pinnedNodeIds: z.array(z.string()),
  filters: z.object({
    nodeTypes: z.array(z.string()),
    edgeTypes: z.array(z.string()),
    minConfidence: z.number(),
    maxConfidence: z.number(),
    searchQuery: z.string(),
  }),
  expandedNodeIds: z.array(z.string()),
  hiddenNodeIds: z.array(z.string()),
  layout: z.enum(['forceatlas2', 'circular', 'random', 'clustered', 'time']),
  colorScheme: z.string(),
  sizeBy: z.enum(['uniform', 'confidence', 'degree']),
  graph: z.object({
    nodes: z.array(z.record(z.string(), z.any())),
    edges: z.array(z.record(z.string(), z.any())),
  }),
});

export const sceneCreateSchema = sceneSchema.omit({ id: true, savedAt: true });

export type StoredScene = z.infer<typeof sceneSchema>;
export type SceneCreateInput = z.infer<typeof sceneCreateSchema>;

async function ensureParentDir(filePath: string) {
  await mkdir(dirname(filePath), { recursive: true });
}

export async function readScenes(filePath: string): Promise<StoredScene[]> {
  try {
    const content = await readFile(filePath, 'utf8');
    const parsed = JSON.parse(content);
    return z.array(sceneSchema).parse(Array.isArray(parsed) ? parsed : []);
  } catch {
    return [];
  }
}

export async function writeScenes(filePath: string, scenes: StoredScene[]) {
  await ensureParentDir(filePath);
  const tempPath = `${filePath}.tmp`;
  await writeFile(tempPath, JSON.stringify(scenes, null, 2), 'utf8');
  await rename(tempPath, filePath);
}

export async function createScene(filePath: string, input: SceneCreateInput) {
  const scenes = await readScenes(filePath);
  const scene: StoredScene = sceneSchema.parse({
    ...input,
    id: crypto.randomUUID(),
    savedAt: new Date().toISOString(),
  });
  scenes.push(scene);
  await writeScenes(filePath, scenes);
  return scene;
}

export async function updateScene(filePath: string, id: string, input: SceneCreateInput) {
  const scenes = await readScenes(filePath);
  const index = scenes.findIndex((scene) => scene.id === id);
  if (index === -1) return null;

  const updatedScene: StoredScene = sceneSchema.parse({
    ...input,
    id,
    savedAt: new Date().toISOString(),
  });

  scenes[index] = updatedScene;
  await writeScenes(filePath, scenes);
  return updatedScene;
}

export async function deleteScene(filePath: string, id: string) {
  const scenes = await readScenes(filePath);
  const nextScenes = scenes.filter((scene) => scene.id !== id);
  if (nextScenes.length === scenes.length) return false;
  await writeScenes(filePath, nextScenes);
  return true;
}

export async function clearSceneFile(filePath: string) {
  await rm(filePath, { force: true });
}
