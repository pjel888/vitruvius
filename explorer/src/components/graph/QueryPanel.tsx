import { useState, useRef, useCallback } from 'react';
import { Play, X, Code2, AlertCircle, CheckCircle2, BookmarkPlus, History, Copy } from 'lucide-react';
import { runCypherQuery } from '../../api/graphApi';
import type { GraphController } from './VisNetworkHost';
import { useSceneStore } from '../../stores/useSceneStore';
import { getQueryResultSummary, QUERY_TEMPLATES, upsertStoredQueries } from '../../utils/explorerRuntime';
import QueryTemplatesSection from '../query-panel/QueryTemplatesSection';
import StoredQueriesSection from '../query-panel/StoredQueriesSection';

const RECENT_QUERIES_KEY = 'vitruvius.explorer.recentQueries';
const SAVED_QUERIES_KEY = 'vitruvius.explorer.savedQueries';

interface QueryPanelProps {
  controllerRef: React.RefObject<GraphController | null>;
  onClose: () => void;
  runQuery?: typeof runCypherQuery;
}

function readStoredQueries(key: string) {
  try {
    const value = JSON.parse(localStorage.getItem(key) || '[]');
    return Array.isArray(value) ? value.filter((entry): entry is string => typeof entry === 'string') : [];
  } catch {
    return [];
  }
}

export default function QueryPanel({ controllerRef, onClose, runQuery = runCypherQuery }: QueryPanelProps) {
  const [query, setQuery] = useState('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 20');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{ nodes: number; edges: number; recordCount: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recentQueries, setRecentQueries] = useState(() => readStoredQueries(RECENT_QUERIES_KEY));
  const [savedQueries, setSavedQueries] = useState(() => readStoredQueries(SAVED_QUERIES_KEY));
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const openBottom = useSceneStore(s => s.openBottom);

  function persistRecentQueries(nextQueries: string[]) {
    setRecentQueries(nextQueries);
    localStorage.setItem(RECENT_QUERIES_KEY, JSON.stringify(nextQueries));
  }

  function persistSavedQueries(nextQueries: string[]) {
    setSavedQueries(nextQueries);
    localStorage.setItem(SAVED_QUERIES_KEY, JSON.stringify(nextQueries));
  }

  function removeSavedQuery(queryToRemove: string) {
    persistSavedQueries(savedQueries.filter((entry) => entry !== queryToRemove));
  }

  function removeRecentQuery(queryToRemove: string) {
    persistRecentQueries(recentQueries.filter((entry) => entry !== queryToRemove));
  }

  const handleRun = useCallback(async () => {
    const cypher = query.trim();
    if (!cypher) return;
    setRunning(true);
    setError(null);
    setResult(null);
    try {
      const data = await runQuery(cypher);
      controllerRef.current?.mergeNodesEdges(data.nodes, data.edges);
      setResult({ nodes: data.nodes.length, edges: data.edges.length, recordCount: data.recordCount });
      const nextRecent = upsertStoredQueries(recentQueries, cypher);
      persistRecentQueries(nextRecent);
      const queryColumns = Array.from(
        data.rows.reduce((keys, row) => {
          Object.keys(row.values).forEach((key) => keys.add(key));
          return keys;
        }, new Set<string>())
      ).map((key) => ({ key, label: key }));
      openBottom({
        type: 'query',
        title: 'Query Result',
        query: cypher,
        resultSummary: getQueryResultSummary(data.recordCount, data.nodes.length, data.edges.length),
        columns: queryColumns,
        rows: data.rows,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Query failed');
    } finally {
      setRunning(false);
    }
  }, [query, controllerRef, recentQueries, openBottom, runQuery]);

  const handleSaveCurrentQuery = useCallback(() => {
    const cypher = query.trim();
    if (!cypher) return;
    const nextSaved = upsertStoredQueries(savedQueries, cypher);
    persistSavedQueries(nextSaved);
  }, [query, savedQueries]);

  const handleTemplateSelect = useCallback((templateQuery: string) => {
    setQuery(templateQuery);
    textareaRef.current?.focus();
  }, []);

  const handleTemplateRun = useCallback(async (templateQuery: string) => {
    setQuery(templateQuery);
    setRunning(true);
    setError(null);
    setResult(null);
    try {
      const data = await runQuery(templateQuery);
      controllerRef.current?.mergeNodesEdges(data.nodes, data.edges);
      setResult({ nodes: data.nodes.length, edges: data.edges.length, recordCount: data.recordCount });
      persistRecentQueries(upsertStoredQueries(recentQueries, templateQuery));
      const queryColumns = Array.from(
        data.rows.reduce((keys, row) => {
          Object.keys(row.values).forEach((key) => keys.add(key));
          return keys;
        }, new Set<string>())
      ).map((key) => ({ key, label: key }));
      openBottom({
        type: 'query',
        title: 'Query Result',
        query: templateQuery,
        resultSummary: getQueryResultSummary(data.recordCount, data.nodes.length, data.edges.length),
        columns: queryColumns,
        rows: data.rows,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Query failed');
    } finally {
      setRunning(false);
    }
  }, [controllerRef, openBottom, recentQueries, runQuery]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
    }
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <aside
      aria-labelledby="advanced-query-panel-title"
      className="fixed right-4 top-16 z-40 flex max-h-[calc(100vh-6rem)] w-[min(32rem,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-cyan-300/20 bg-panel/95 shadow-2xl shadow-black/40 backdrop-blur"
      role="dialog"
    >
      <div className="border-b border-border/80 bg-white/[0.03] px-4 py-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 rounded-xl border border-cyan-300/20 bg-cyan-300/10 p-2 text-cyan-100">
              <Code2 size={15} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 id="advanced-query-panel-title" className="text-sm font-semibold text-text">Advanced Graph Query</h2>
                <span className="rounded-full border border-amber-300/20 bg-amber-300/10 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.14em] text-amber-100/90">Optional</span>
              </div>
              <p className="mt-1 max-w-sm text-[10px] leading-4 text-text-dim">
                Run Cypher when search and taxonomy browsing are not enough. Results merge into the graph and open in the bottom drawer.
              </p>
            </div>
          </div>
          <button
            aria-label="Close advanced graph query panel"
            className="rounded-xl p-2 text-text-dim transition hover:bg-panel-hover hover:text-text"
            onClick={onClose}
            title="Close advanced graph query panel"
          >
            <X size={14} />
          </button>
        </div>
      </div>

      <div className="flex min-h-0 flex-1 flex-col overflow-y-auto p-4">
        <div className="rounded-2xl border border-border/80 bg-bg/70 p-3">
          <div className="mb-2 flex items-center justify-between gap-3">
            <label className="text-[10px] font-semibold uppercase tracking-[0.18em] text-text-dim" htmlFor="advanced-graph-query-input">
              Query
            </label>
            <span className="text-[10px] text-text-dim">Ctrl/⌘ + Enter runs</span>
          </div>
          <textarea
            ref={textareaRef}
            id="advanced-graph-query-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            className="h-32 w-full resize-none rounded-xl border border-border bg-panel/80 p-3 font-mono text-[11px] leading-5 text-text outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
            placeholder="MATCH (n) RETURN n LIMIT 10"
            spellCheck={false}
          />
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
            <span className="text-[10px] text-text-dim">Tip: keep queries small; large results can slow the canvas.</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => navigator.clipboard.writeText(query)}
                className="flex items-center gap-1.5 rounded-lg border border-border px-2.5 py-1.5 text-[10px] font-medium text-text-dim transition hover:border-accent hover:text-text"
              >
                <Copy size={12} />
                Copy
              </button>
              <button
                onClick={handleSaveCurrentQuery}
                className="flex items-center gap-1.5 rounded-lg border border-border px-2.5 py-1.5 text-[10px] font-medium text-text-dim transition hover:border-accent hover:text-text"
              >
                <BookmarkPlus size={12} />
                Save
              </button>
              <button
                onClick={handleRun}
                disabled={running}
                className="flex items-center gap-1.5 rounded-lg bg-accent/20 px-3 py-1.5 text-[10px] font-semibold text-accent transition hover:bg-accent/30 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Play size={12} />
                {running ? 'Running…' : 'Run Query'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="mt-3 flex items-start gap-2 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-[11px] leading-4 text-red-300">
            <AlertCircle size={14} className="mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="mt-3 flex items-start gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-3 text-[11px] leading-4 text-emerald-300">
            <CheckCircle2 size={14} className="mt-0.5 shrink-0" />
            <div>
              <div className="font-semibold">{result.recordCount} rows returned</div>
              <div className="text-emerald-300/70">
                {result.recordCount === 0
                  ? 'No records matched this query. The graph view was left unchanged.'
                  : `${result.nodes} nodes + ${result.edges} edges merged into graph`}
              </div>
            </div>
          </div>
        )}

        <div className="mt-4 space-y-3">
          <QueryTemplatesSection templates={QUERY_TEMPLATES} onSelectTemplate={handleTemplateSelect} onRunTemplate={(query) => void handleTemplateRun(query)} />
          <StoredQueriesSection
            title="Saved Queries"
            icon={<BookmarkPlus size={12} />}
            queries={savedQueries}
            onSelect={setQuery}
            onDelete={removeSavedQuery}
          />
          <StoredQueriesSection
            title="Recent Queries"
            icon={<History size={12} />}
            queries={recentQueries}
            onSelect={setQuery}
            onDelete={removeRecentQuery}
          />
        </div>
      </div>
    </aside>
  );
}
