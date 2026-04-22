import type { QueryResultRow } from '../types';

export function formatPerspectiveCount(
  nodeCount: number | undefined,
  loading: boolean,
  error: string | null,
  fallback: string,
): string {
  if (loading) return 'Loading live count…';
  if (error) return 'Live count unavailable';
  return typeof nodeCount === 'number' ? `${nodeCount} nodes` : fallback;
}

export function shouldConsumePreloadedPerspective(options: {
  activeSceneId: string | null;
  preloadedPerspectiveId: string | null;
  perspectiveId: string;
  nodeCount: number;
  consumedPreload: boolean;
}): boolean {
  return Boolean(
    !options.activeSceneId
      && options.preloadedPerspectiveId === options.perspectiveId
      && options.nodeCount > 0
      && !options.consumedPreload,
  );
}

export function getQueryResultSummary(recordCount: number, nodeCount: number, edgeCount: number): string {
  if (recordCount === 0) {
    return 'No rows returned · graph unchanged';
  }

  return `${recordCount} rows returned · ${nodeCount} nodes · ${edgeCount} edges`;
}

export function hasRenderableQueryRows(columns: Array<{ key: string; label: string }> | undefined, rows: QueryResultRow[] | undefined): boolean {
  return Boolean(columns && rows && columns.length > 0 && rows.length > 0);
}
