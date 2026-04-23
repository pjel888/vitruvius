import { useState, useRef, useCallback, useEffect } from 'react';
import { Play, X, Terminal, AlertCircle, CheckCircle2, BookmarkPlus, History, Copy, Trash2 } from 'lucide-react';
import { runCypherQuery } from '../../api/graphApi';
import type { GraphController } from './VisNetworkHost';
import { useSceneStore } from '../../stores/useSceneStore';
import { getQueryResultSummary, QUERY_TEMPLATES, upsertStoredQueries } from '../../utils/explorerRuntime';

const RECENT_QUERIES_KEY = 'vitruvius.explorer.recentQueries';
const SAVED_QUERIES_KEY = 'vitruvius.explorer.savedQueries';

interface QueryPanelProps {
  controllerRef: React.RefObject<GraphController | null>;
  onClose: () => void;
}

export default function QueryPanel({ controllerRef, onClose }: QueryPanelProps) {
  const [query, setQuery] = useState('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 20');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{ nodes: number; edges: number; recordCount: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recentQueries, setRecentQueries] = useState<string[]>([]);
  const [savedQueries, setSavedQueries] = useState<string[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const openBottom = useSceneStore(s => s.openBottom);

  useEffect(() => {
    try {
      const recent = JSON.parse(localStorage.getItem(RECENT_QUERIES_KEY) || '[]');
      const saved = JSON.parse(localStorage.getItem(SAVED_QUERIES_KEY) || '[]');
      setRecentQueries(Array.isArray(recent) ? recent : []);
      setSavedQueries(Array.isArray(saved) ? saved : []);
    } catch {
      setRecentQueries([]);
      setSavedQueries([]);
    }
  }, []);

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
      const data = await runCypherQuery(cypher);
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
    } catch (err: any) {
      setError(err.message || 'Query failed');
    } finally {
      setRunning(false);
    }
  }, [query, controllerRef, recentQueries, openBottom]);

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
      const data = await runCypherQuery(templateQuery);
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
    } catch (err: any) {
      setError(err.message || 'Query failed');
    } finally {
      setRunning(false);
    }
  }, [controllerRef, openBottom, recentQueries]);

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

      <div className="px-3 pb-3">
        <details className="text-xs text-text-dim">
          <summary className="cursor-pointer hover:text-text transition-colors">Templates ({QUERY_TEMPLATES.length})</summary>
          <div className="mt-1 space-y-1 pl-2">
            {QUERY_TEMPLATES.map((template) => (
              <div key={template.label} className="flex items-center justify-between gap-2">
                <button
                  onClick={() => handleTemplateSelect(template.query)}
                  className="block flex-1 text-left hover:text-accent transition-colors"
                >
                  {template.label}
                </button>
                <button
                  onClick={() => void handleTemplateRun(template.query)}
                  className="text-[10px] uppercase tracking-wider text-text-dim hover:text-accent transition-colors"
                >
                  Run
                </button>
              </div>
            ))}
          </div>
        </details>
      </div>

      {savedQueries.length > 0 && (
        <div className="px-3 pb-3">
          <details className="text-xs text-text-dim" open>
            <summary className="cursor-pointer hover:text-text transition-colors flex items-center gap-1">
              <BookmarkPlus size={12} />
              Saved Queries
            </summary>
            <div className="mt-1 space-y-1 pl-2">
              {savedQueries.map((savedQuery) => (
                <div key={savedQuery} className="flex items-center gap-2">
                  <button
                    onClick={() => setQuery(savedQuery)}
                    className="block flex-1 text-left truncate hover:text-accent transition-colors"
                    title={savedQuery}
                  >
                    {savedQuery}
                  </button>
                  <button
                    onClick={() => removeSavedQuery(savedQuery)}
                    className="text-text-dim hover:text-red-400 transition-colors"
                    title="Delete saved query"
                  >
                    <Trash2 size={12} />
                  </button>
                </div>
              ))}
            </div>
          </details>
        </div>
      )}

      {recentQueries.length > 0 && (
        <div className="px-3 pb-3">
          <details className="text-xs text-text-dim" open>
            <summary className="cursor-pointer hover:text-text transition-colors flex items-center gap-1">
              <History size={12} />
              Recent Queries
            </summary>
            <div className="mt-1 space-y-1 pl-2">
              {recentQueries.map((recentQuery) => (
                <div key={recentQuery} className="flex items-center gap-2">
                  <button
                    onClick={() => setQuery(recentQuery)}
                    className="block flex-1 text-left truncate hover:text-accent transition-colors"
                    title={recentQuery}
                  >
                    {recentQuery}
                  </button>
                  <button
                    onClick={() => removeRecentQuery(recentQuery)}
                    className="text-text-dim hover:text-red-400 transition-colors"
                    title="Delete recent query"
                  >
                    <Trash2 size={12} />
                  </button>
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
