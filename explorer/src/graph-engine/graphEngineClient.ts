import type { GraphEdge, GraphNode, SearchResult } from '../types';
import {
  buildGraphIndex,
  buildGraphFingerprint,
  buildVisibleSubgraph,
  searchGraphIndex,
  resolveAlias,
  expandNeighborhood,
  tracePathInIndex,
  type VisibleSubgraphOptions,
} from './graphIndex';

type WorkerResponse<T = unknown> = {
  id: number;
  ok: boolean;
  data?: T;
  error?: string;
  timingMs?: number;
};

type PendingRequest = {
  resolve: (value: unknown) => void;
  reject: (error: Error) => void;
  type: string;
};

let worker: Worker | null = null;
let nextRequestId = 1;
let activeFingerprint: string | null = null;
let workerReady = false;
let fallbackIndex: ReturnType<typeof buildGraphIndex> | null = null;
let fallbackSource: { fingerprint: string; nodes: GraphNode[]; edges: GraphEdge[] } | null = null;
const pending = new Map<number, PendingRequest>();
const lastWorkerTimingsMs: Record<string, number> = {};

function canUseWorker() {
  return typeof Worker !== 'undefined' && typeof URL !== 'undefined';
}

function getWorker() {
  if (!canUseWorker()) return null;
  if (worker) return worker;
  try {
    worker = new Worker(new URL('./graphWorker.ts', import.meta.url), { type: 'module' });
    worker.onmessage = (event: MessageEvent<WorkerResponse>) => {
      const request = pending.get(event.data.id);
      if (!request) return;
      pending.delete(event.data.id);
      if (typeof event.data.timingMs === 'number') {
        lastWorkerTimingsMs[request.type] = event.data.timingMs;
      }
      if (event.data.ok) request.resolve(event.data.data);
      else request.reject(new Error(event.data.error || 'Graph worker request failed'));
    };
    worker.onerror = () => {
      worker = null;
      workerReady = false;
      for (const [id, request] of pending) {
        pending.delete(id);
        request.reject(new Error('Graph worker failed'));
      }
    };
    return worker;
  } catch {
    worker = null;
    return null;
  }
}

function postWorkerMessage<T>(message: Record<string, unknown>): Promise<T> {
  const targetWorker = getWorker();
  if (!targetWorker) return Promise.reject(new Error('Graph worker unavailable'));
  const id = nextRequestId++;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve: resolve as (value: unknown) => void, reject, type: String(message.type || 'unknown') });
    targetWorker.postMessage({ ...message, id });
  });
}

function ensureFallbackIndex() {
  if (fallbackIndex) return fallbackIndex;
  if (!fallbackSource || fallbackSource.fingerprint !== activeFingerprint) return null;
  fallbackIndex = buildGraphIndex(fallbackSource.nodes, fallbackSource.edges);
  return fallbackIndex;
}

export async function loadGraphEngine(nodes: GraphNode[], edges: GraphEdge[], options: { sourceUrl?: string } = {}) {
  const fingerprint = buildGraphFingerprint(nodes, edges);
  if (fingerprint === activeFingerprint && (workerReady || fallbackIndex)) return { fingerprint, reused: true, worker: workerReady, stale: false };
  activeFingerprint = fingerprint;
  workerReady = false;
  fallbackIndex = null;
  fallbackSource = { fingerprint, nodes, edges };
  try {
    const result = await postWorkerMessage<{ fingerprint: string }>(
      options.sourceUrl
        ? { type: 'loadFromUrl', url: options.sourceUrl, expectedFingerprint: fingerprint }
        : { type: 'load', nodes, edges }
    );
    if (result.fingerprint !== fingerprint) throw new Error('Graph worker loaded a mismatched fingerprint');
    if (activeFingerprint !== fingerprint) return { fingerprint, reused: false, worker: false, stale: true };
    workerReady = true;
    return { fingerprint, reused: false, worker: true, stale: false };
  } catch {
    if (activeFingerprint !== fingerprint) return { fingerprint, reused: false, worker: false, stale: true };
    ensureFallbackIndex();
    return { fingerprint, reused: false, worker: false, stale: false };
  }
}

export function getGraphEngineFingerprint() {
  return activeFingerprint;
}

export function isGraphEngineReady() {
  return Boolean(activeFingerprint && (workerReady || fallbackIndex));
}

export function isGraphEngineReadyForFingerprint(fingerprint: string | null | undefined) {
  return Boolean(fingerprint && fingerprint === activeFingerprint && (workerReady || fallbackIndex));
}

export function getGraphEngineDiagnostics() {
  return {
    activeFingerprint,
    workerReady,
    fallbackIndexReady: Boolean(fallbackIndex),
    fallbackSourceReady: Boolean(fallbackSource),
    pendingRequests: pending.size,
    lastWorkerTimingsMs: { ...lastWorkerTimingsMs },
  };
}

export function resetGraphEngineForTests() {
  worker?.terminate?.();
  worker = null;
  workerReady = false;
  nextRequestId = 1;
  activeFingerprint = null;
  fallbackIndex = null;
  fallbackSource = null;
  for (const key of Object.keys(lastWorkerTimingsMs)) delete lastWorkerTimingsMs[key];
  pending.clear();
}

function isExpectedFingerprintCurrent(expectedFingerprint?: string | null) {
  return !expectedFingerprint || expectedFingerprint === activeFingerprint;
}

export async function searchGraphEngine(query: string, limit = 20, expectedFingerprint?: string | null): Promise<SearchResult[]> {
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return [];
  if (workerReady) {
    try {
      const results = await postWorkerMessage<SearchResult[]>({ type: 'search', query, limit });
      return isExpectedFingerprintCurrent(expectedFingerprint) ? results : [];
    } catch {
      workerReady = false;
    }
  }
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return [];
  const index = ensureFallbackIndex();
  return index ? searchGraphIndex(index, query, limit) : [];
}

export async function resolveGraphAlias(alias: string, expectedFingerprint?: string | null) {
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  if (workerReady) {
    try {
      const result = await postWorkerMessage({ type: 'alias', alias });
      return isExpectedFingerprintCurrent(expectedFingerprint) ? result : null;
    } catch {
      workerReady = false;
    }
  }
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  const index = ensureFallbackIndex();
  return index ? resolveAlias(index, alias) : null;
}

export async function expandGraphNeighborhood(nodeId: string, depth = 1, maxEdges = 200, expectedFingerprint?: string | null) {
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  if (workerReady) {
    try {
      const result = await postWorkerMessage({ type: 'expand', nodeId, depth, maxEdges });
      return isExpectedFingerprintCurrent(expectedFingerprint) ? result : null;
    } catch {
      workerReady = false;
    }
  }
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  const index = ensureFallbackIndex();
  return index ? expandNeighborhood(index, nodeId, depth, maxEdges) : null;
}

export async function traceGraphEnginePath(from: string, to: string, maxHops = 6, expectedFingerprint?: string | null) {
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  if (workerReady) {
    try {
      const result = await postWorkerMessage({ type: 'path', from, to, maxHops });
      return isExpectedFingerprintCurrent(expectedFingerprint) ? result : null;
    } catch {
      workerReady = false;
    }
  }
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  const index = ensureFallbackIndex();
  return index ? tracePathInIndex(index, from, to, maxHops) : null;
}

export async function buildGraphEngineVisibleSubgraph(
  options: VisibleSubgraphOptions = {},
  expectedFingerprint?: string | null
) {
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  if (workerReady) {
    try {
      const result = await postWorkerMessage({ type: 'visibleSubgraph', ...options });
      return isExpectedFingerprintCurrent(expectedFingerprint) ? result : null;
    } catch {
      workerReady = false;
    }
  }
  if (!isExpectedFingerprintCurrent(expectedFingerprint)) return null;
  const index = ensureFallbackIndex();
  return index ? buildVisibleSubgraph(index, options) : null;
}
