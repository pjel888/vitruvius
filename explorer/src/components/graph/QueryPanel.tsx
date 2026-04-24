import { useState, useRef, useCallback } from 'react';
import { Play, X, Terminal, AlertCircle, CheckCircle2, BookmarkPlus, History, Copy } from 'lucide-react';
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
    <div className="fixed z-40 top-16 right-4 w-96 bg-panel border border-border rounded-md shadow-lg flex flex-col max-h-[70vh]">
      <div className="px-3 py-2 border-b border-border flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2 text-sm font-medium">
          <Terminal size={14} className="text-accent" />
          Cypher Query
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-panel-hover text-text-dim"
          title="Close"
        >
          <X size={14} />
        </button>
      </div>

      <div className="p-3 flex flex-col gap-2">
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full h-28 bg-bg border border-border rounded-md p-2 text-sm font-mono text-text placeholder-text-dim outline-none focus:border-accent resize-none"
          placeholder="MATCH (n) RETURN n LIMIT 10"
          spellCheck={false}
        />
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-text-dim">Ctrl+Enter to run</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigator.clipboard.writeText(query)}
              className="flex items-center gap-1.5 px-3 py-1.5 border border-border text-text-dim text-sm rounded-md hover:border-accent hover:text-text transition-colors"
            >
              <Copy size={12} />
              Copy
            </button>
            <button
              onClick={handleSaveCurrentQuery}
              className="flex items-center gap-1.5 px-3 py-1.5 border border-border text-text-dim text-sm rounded-md hover:border-accent hover:text-text transition-colors"
            >
              <BookmarkPlus size={12} />
              Save
            </button>
            <button
              onClick={handleRun}
              disabled={running}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-accent/20 text-accent text-sm rounded-md hover:bg-accent/30 transition-colors disabled:opacity-50"
            >
              <Play size={12} />
              {running ? 'Running…' : 'Run'}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="px-3 pb-3">
          <div className="flex items-start gap-2 p-2 bg-red-500/10 border border-red-500/20 rounded-md text-sm text-red-400">
            <AlertCircle size={14} className="shrink-0 mt-0.5" />
            {error}
          </div>
        </div>
      )}

      {result && (
        <div className="px-3 pb-3">
          <div className="flex items-start gap-2 p-2 bg-emerald-500/10 border border-emerald-500/20 rounded-md text-sm text-emerald-400">
            <CheckCircle2 size={14} className="shrink-0 mt-0.5" />
            <div>
              <div>{result.recordCount} rows returned</div>
              <div className="text-xs text-emerald-400/70">
                {result.recordCount === 0
                  ? 'No records matched this query. The graph view was left unchanged.'
                  : `${result.nodes} nodes + ${result.edges} edges merged into graph`}
              </div>
            </div>
          </div>
        </div>
      )}

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
  );
}
