import type { QueryResultRow } from '../types';

export const QUERY_TEMPLATES = [
  {
    label: 'All rules',
    query: 'MATCH (n:CanonicalNode {type: "rule"}) RETURN n LIMIT 10',
  },
  {
    label: 'Neighbors of floor-area',
    query: 'MATCH (n {id: "concept-floor-area"})-[r]-(m) RETURN n, r, m',
  },
  {
    label: 'Shortest path floor-area → stairs',
    query: 'MATCH p = shortestPath((a)-[*..6]-(b)) WHERE a.id = "concept-floor-area" AND b.id = "concept-stairs" RETURN p',
  },
] as const;

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

export function upsertStoredQueries(existingQueries: string[], nextQuery: string): string[] {
  return [nextQuery, ...existingQueries.filter((entry) => entry !== nextQuery)].slice(0, 8);
}
