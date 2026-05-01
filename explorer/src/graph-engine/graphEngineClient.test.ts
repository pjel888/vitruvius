import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import type { GraphEdge, GraphNode, SearchResult } from '../types';
import { buildGraphFingerprint } from './graphIndex';
import {
  buildGraphEngineVisibleSubgraph,
  getGraphEngineDiagnostics,
  getGraphEngineFingerprint,
  isGraphEngineReady,
  isGraphEngineReadyForFingerprint,
  loadGraphEngine,
  resetGraphEngineForTests,
  searchGraphEngine,
} from './graphEngineClient';

const nodes: GraphNode[] = [
  { id: 'architecture', label: 'Architecture', type: 'taxonomy', aliases: ['ARC'] },
  { id: 'tropical', label: 'Tropical Architecture', type: 'concept', aliases: ['ARC.TAC'] },
];

const edges: GraphEdge[] = [
  { id: 'e1', source: 'architecture', target: 'tropical', type: 'HAS_CHILD' },
];

const originalWorker = globalThis.Worker;

type FakeWorkerMessage = {
  id: number;
  type: string;
  nodes?: GraphNode[];
  edges?: GraphEdge[];
  query?: string;
  url?: string;
  expectedFingerprint?: string;
  rootNodeId?: string | null;
  depth?: number;
  maxNodes?: number;
  maxEdges?: number;
};

class FakeGraphWorker {
  static instances: FakeGraphWorker[] = [];
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: (() => void) | null = null;
  messages: unknown[] = [];

  terminate() {}

  constructor() {
    FakeGraphWorker.instances.push(this);
  }

  postMessage(message: FakeWorkerMessage) {
    this.messages.push(message);
    queueMicrotask(() => {
      if (message.type === 'load') {
        const fingerprint = buildGraphFingerprint(message.nodes ?? [], message.edges ?? []);
        this.onmessage?.({ data: { id: message.id, ok: true, data: { fingerprint } } } as MessageEvent);
        return;
      }
      if (message.type === 'loadFromUrl') {
        this.onmessage?.({ data: { id: message.id, ok: true, data: { fingerprint: message.expectedFingerprint } } } as MessageEvent);
        return;
      }
      if (message.type === 'search') {
        const results: SearchResult[] = [{ kind: 'node', id: 'tropical', label: 'Tropical Architecture', type: 'concept', matchType: 'label', matchedField: 'label' }];
        this.onmessage?.({ data: { id: message.id, ok: true, data: results, timingMs: 1.25 } } as MessageEvent);
        return;
      }
      if (message.type === 'visibleSubgraph') {
        this.onmessage?.({ data: { id: message.id, ok: true, data: { nodes, edges }, timingMs: 2.5 } } as MessageEvent);
      }
    });
  }
}

class ManualGraphWorker {
  static instances: ManualGraphWorker[] = [];
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: (() => void) | null = null;
  messages: FakeWorkerMessage[] = [];

  terminate() {}

  constructor() {
    ManualGraphWorker.instances.push(this);
  }

  postMessage(message: FakeWorkerMessage) {
    this.messages.push(message);
  }

  respond(message: { id: number }, data: unknown) {
    this.onmessage?.({ data: { id: message.id, ok: true, data } } as MessageEvent);
  }
}

beforeEach(() => {
  resetGraphEngineForTests();
  FakeGraphWorker.instances = [];
  ManualGraphWorker.instances = [];
});

afterEach(() => {
  resetGraphEngineForTests();
  FakeGraphWorker.instances = [];
  ManualGraphWorker.instances = [];
  (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = originalWorker;
});

describe('graph engine client worker lifecycle', () => {
  test('loads the full graph index in a worker without building the fallback index on the main thread', async () => {
    (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = FakeGraphWorker as unknown as typeof Worker;

    const result = await loadGraphEngine(nodes, edges);
    const diagnostics = getGraphEngineDiagnostics();
    const searchResults = await searchGraphEngine('tropical');
    const visibleSubgraph = await buildGraphEngineVisibleSubgraph({ rootNodeId: 'architecture', depth: 1, maxNodes: 25, maxEdges: 25 });

    expect(result).toEqual(expect.objectContaining({ worker: true, reused: false }));
    expect(isGraphEngineReady()).toBe(true);
    expect(diagnostics.workerReady).toBe(true);
    expect(diagnostics.fallbackSourceReady).toBe(true);
    expect(diagnostics.fallbackIndexReady).toBe(false);
    expect(FakeGraphWorker.instances[0]?.messages.map((message) => (message as { type: string }).type)).toEqual(['load', 'search', 'visibleSubgraph']);
    expect(searchResults[0]?.id).toBe('tropical');
    expect(visibleSubgraph).toEqual({ nodes, edges });
    expect(getGraphEngineDiagnostics().lastWorkerTimingsMs).toEqual(expect.objectContaining({ search: 1.25, visibleSubgraph: 2.5 }));
  });

  test('can ask the worker to fetch the graph by URL instead of structured-cloning the graph object', async () => {
    (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = FakeGraphWorker as unknown as typeof Worker;

    const result = await loadGraphEngine(nodes, edges, { sourceUrl: 'http://example.test/perspective/aec-mepfs/nodes?profile=render' });
    const message = FakeGraphWorker.instances[0]?.messages[0] as FakeWorkerMessage;

    expect(result).toEqual(expect.objectContaining({ worker: true, reused: false }));
    expect(message.type).toBe('loadFromUrl');
    expect(message.url).toBe('http://example.test/perspective/aec-mepfs/nodes?profile=render');
    expect(message.expectedFingerprint).toBe(buildGraphFingerprint(nodes, edges));
    expect(message.nodes).toBeUndefined();
    expect(message.edges).toBeUndefined();
    expect(getGraphEngineDiagnostics()).toEqual(expect.objectContaining({ workerReady: true, fallbackIndexReady: false }));
  });

  test('does not mark a stale worker load response as ready for the current graph', async () => {
    (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = ManualGraphWorker as unknown as typeof Worker;
    const nextNodes: GraphNode[] = [...nodes, { id: 'bamboo', label: 'Bamboo', type: 'concept', aliases: ['MAT.BAM'] }];
    const firstFingerprint = buildGraphFingerprint(nodes, edges);
    const secondFingerprint = buildGraphFingerprint(nextNodes, edges);

    const firstLoad = loadGraphEngine(nodes, edges);
    const secondLoad = loadGraphEngine(nextNodes, edges);
    const worker = ManualGraphWorker.instances[0]!;
    const firstMessage = worker.messages[0]!;
    const secondMessage = worker.messages[1]!;

    worker.respond(firstMessage, { fingerprint: firstFingerprint });
    const firstResult = await firstLoad;

    expect(firstResult).toEqual(expect.objectContaining({ stale: true, worker: false }));
    expect(getGraphEngineFingerprint()).toBe(secondFingerprint);
    expect(getGraphEngineDiagnostics()).toEqual(expect.objectContaining({ workerReady: false, fallbackIndexReady: false }));
    expect(isGraphEngineReadyForFingerprint(firstFingerprint)).toBe(false);

    worker.respond(secondMessage, { fingerprint: secondFingerprint });
    const secondResult = await secondLoad;

    expect(secondResult).toEqual(expect.objectContaining({ stale: false, worker: true }));
    expect(getGraphEngineDiagnostics()).toEqual(expect.objectContaining({ workerReady: true, fallbackIndexReady: false }));
    expect(isGraphEngineReadyForFingerprint(secondFingerprint)).toBe(true);
  });

  test('refuses local search when the caller expects a different graph fingerprint', async () => {
    (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = FakeGraphWorker as unknown as typeof Worker;
    const fingerprint = buildGraphFingerprint(nodes, edges);

    await loadGraphEngine(nodes, edges);
    const staleResults = await searchGraphEngine('tropical', 20, `${fingerprint}:stale`);
    const freshResults = await searchGraphEngine('tropical', 20, fingerprint);

    expect(staleResults).toEqual([]);
    expect(freshResults[0]?.id).toBe('tropical');
    expect(FakeGraphWorker.instances[0]?.messages.map((message) => (message as { type: string }).type)).toEqual(['load', 'search']);
  });

  test('builds the same index lazily on the main thread only when the worker path is unavailable', async () => {
    class ThrowingWorker {
      constructor() {
        throw new Error('worker unavailable');
      }
    }
    (globalThis as typeof globalThis & { Worker?: typeof Worker }).Worker = ThrowingWorker as unknown as typeof Worker;

    const result = await loadGraphEngine(nodes, edges);
    const diagnostics = getGraphEngineDiagnostics();
    const searchResults = await searchGraphEngine('ARC.TAC');

    expect(result).toEqual(expect.objectContaining({ worker: false, reused: false }));
    expect(isGraphEngineReady()).toBe(true);
    expect(diagnostics.workerReady).toBe(false);
    expect(diagnostics.fallbackIndexReady).toBe(true);
    expect(searchResults[0]?.id).toBe('tropical');
  });
});
