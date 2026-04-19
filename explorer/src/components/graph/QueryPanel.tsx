import { useState, useRef, useCallback } from 'react';
import { Play, X, Terminal, AlertCircle, CheckCircle2 } from 'lucide-react';
import { runCypherQuery } from '../../api/graphApi';
import type { GraphController } from './VisNetworkHost';

interface QueryPanelProps {
  controllerRef: React.RefObject<GraphController | null>;
  onClose: () => void;
}

export default function QueryPanel({ controllerRef, onClose }: QueryPanelProps) {
  const [query, setQuery] = useState('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 20');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{ nodes: number; edges: number; recordCount: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

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
    } catch (err: any) {
      setError(err.message || 'Query failed');
    } finally {
      setRunning(false);
    }
  }, [query, controllerRef]);

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
              <div>{result.recordCount} records scanned</div>
              <div className="text-xs text-emerald-400/70">
                {result.nodes} nodes + {result.edges} edges merged into graph
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="px-3 pb-3">
        <details className="text-xs text-text-dim">
          <summary className="cursor-pointer hover:text-text transition-colors">Examples</summary>
          <div className="mt-1 space-y-1 pl-2">
            <button
              onClick={() => setQuery('MATCH (n:CanonicalNode {type: "rule"}) RETURN n LIMIT 10')}
              className="block text-left hover:text-accent transition-colors"
            >
              All rules
            </button>
            <button
              onClick={() => setQuery('MATCH (n {id: "concept-floor-area"})-[r]-(m) RETURN n, r, m')}
              className="block text-left hover:text-accent transition-colors"
            >
              Neighbors of floor-area
            </button>
            <button
              onClick={() => setQuery('MATCH p = shortestPath((a)-[*..6]-(b)) WHERE a.id = "concept-floor-area" AND b.id = "concept-stairs" RETURN p')}
              className="block text-left hover:text-accent transition-colors"
            >
              Shortest path floor-area → stairs
            </button>
          </div>
        </details>
      </div>
    </div>
  );
}
