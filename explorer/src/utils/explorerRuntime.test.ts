import { describe, expect, test } from 'bun:test';
import {
  QUERY_TEMPLATES,
  formatPerspectiveCount,
  getQueryResultSummary,
  hasRenderableQueryRows,
  shouldConsumePreloadedPerspective,
  upsertStoredQueries,
} from './explorerRuntime';

describe('formatPerspectiveCount', () => {
  test('returns loading state before live count resolves', () => {
    expect(formatPerspectiveCount(undefined, true, null, 'Fallback')).toBe('Loading live count…');
  });

  test('returns unavailable state when count fetch fails', () => {
    expect(formatPerspectiveCount(undefined, false, 'boom', 'Fallback')).toBe('Live count unavailable');
  });

  test('returns live count when available', () => {
    expect(formatPerspectiveCount(88, false, null, 'Fallback')).toBe('88 nodes');
  });
});

describe('shouldConsumePreloadedPerspective', () => {
  test('consumes preloaded graph exactly once for the active perspective', () => {
    expect(shouldConsumePreloadedPerspective({
      activeSceneId: null,
      preloadedPerspectiveId: 'default',
      perspectiveId: 'default',
      nodeCount: 10,
      consumedPreload: false,
    })).toBe(true);
  });

  test('does not consume preloaded graph for a different perspective or after consumption', () => {
    expect(shouldConsumePreloadedPerspective({
      activeSceneId: null,
      preloadedPerspectiveId: 'default',
      perspectiveId: 'concepts',
      nodeCount: 10,
      consumedPreload: false,
    })).toBe(false);

    expect(shouldConsumePreloadedPerspective({
      activeSceneId: null,
      preloadedPerspectiveId: 'default',
      perspectiveId: 'default',
      nodeCount: 10,
      consumedPreload: true,
    })).toBe(false);
  });
});

describe('getQueryResultSummary', () => {
  test('returns explicit empty-state summary for zero-row results', () => {
    expect(getQueryResultSummary(0, 0, 0)).toBe('No rows returned · graph unchanged');
  });

  test('returns detailed summary for populated results', () => {
    expect(getQueryResultSummary(3, 2, 1)).toBe('3 rows returned · 2 nodes · 1 edges');
  });
});

describe('hasRenderableQueryRows', () => {
  test('requires both rows and columns for query table rendering', () => {
    expect(hasRenderableQueryRows([{ key: 'id', label: 'ID' }], [{ id: '1', values: { id: '1' } }])).toBe(true);
    expect(hasRenderableQueryRows([], [{ id: '1', values: { id: '1' } }])).toBe(false);
    expect(hasRenderableQueryRows([{ key: 'id', label: 'ID' }], [])).toBe(false);
  });
});

describe('upsertStoredQueries', () => {
  test('moves an existing query to the front and caps the list', () => {
    expect(upsertStoredQueries(['A', 'B', 'C'], 'B')).toEqual(['B', 'A', 'C']);
    expect(upsertStoredQueries(['1', '2', '3', '4', '5', '6', '7', '8'], '9')).toEqual(['9', '1', '2', '3', '4', '5', '6', '7']);
  });
});

describe('QUERY_TEMPLATES', () => {
  test('exposes the expected built-in query templates', () => {
    expect(QUERY_TEMPLATES).toHaveLength(3);
    expect(QUERY_TEMPLATES[0]?.label).toBe('All rules');
  });
});
