import { useState, useRef, useEffect } from 'react';
import { Search, ChevronDown, X, Loader2 } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { searchNodes, getPerspectives } from '../api/graphApi';
import type { SearchResult, Perspective } from '../types';

export default function CommandBar() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlighted, setHighlighted] = useState(0);
  const [searching, setSearching] = useState(false);
  const [perspectives, setPerspectives] = useState<Perspective[]>([]);
  const [showPerspectives, setShowPerspectives] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setSearchQuery = useSceneStore(s => s.setSearchQuery);

  useEffect(() => {
    getPerspectives().then(setPerspectives);
  }, []);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setShowSuggestions(false);
      return;
    }
    const timer = setTimeout(async () => {
      setSearching(true);
      const res = await searchNodes(query, perspectiveId, 20);
      setResults(res);
      setShowSuggestions(true);
      setHighlighted(0);
      setSearching(false);
    }, 150);
    return () => clearTimeout(timer);
  }, [query, perspectiveId]);

  const activePerspective = perspectives.find(p => p.id === perspectiveId);

  function selectResult(r: SearchResult) {
    if (r.kind === 'node') {
      setSelectedNode(r.id);
    }
    setQuery(r.label);
    setShowSuggestions(false);
    setSearchQuery(r.label);
  }

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlighted(i => Math.min(i + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlighted(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[highlighted]) {
        selectResult(results[highlighted]);
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      inputRef.current?.blur();
    } else if (e.key === 'Tab' && results.length > 0) {
      e.preventDefault();
      selectResult(results[0]);
    }
  }

  return (
    <div className="h-14 bg-panel border-b border-border flex items-center px-4 gap-3 shrink-0">
      <div className="font-semibold text-accent text-sm tracking-wide">VITRUVIUS</div>

      {/* Perspective switcher */}
      <div className="relative">
        <button
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors min-w-[140px] justify-between"
          onClick={() => setShowPerspectives(!showPerspectives)}
        >
          <span className="truncate">{activePerspective?.name ?? 'All Knowledge'}</span>
          <ChevronDown size={14} className="text-text-dim shrink-0" />
        </button>
        {showPerspectives && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setShowPerspectives(false)} />
            <div className="absolute top-full left-0 mt-1 w-56 bg-panel border border-border rounded-lg shadow-xl z-20 py-1">
              {perspectives.map(p => (
                <button
                  key={p.id}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors ${p.id === perspectiveId ? 'text-accent' : ''}`}
                  onClick={() => { setPerspectiveId(p.id); setShowPerspectives(false); }}
                >
                  <div className="font-medium">{p.name}</div>
                  <div className="text-xs text-text-dim">{p.description}</div>
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Search combobox */}
      <div className="relative flex-1 max-w-xl">
        <div className="flex items-center gap-2 bg-bg border border-border rounded-md px-3 py-1.5 focus-within:border-accent transition-colors">
          <Search size={14} className="text-text-dim shrink-0" />
          <input
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent outline-none text-sm placeholder:text-text-dim"
            placeholder="Search nodes, taxonomies, paths..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={onKeyDown}
            onFocus={() => query.trim() && setShowSuggestions(true)}
          />
          {searching && <Loader2 size={14} className="text-text-dim animate-spin shrink-0" />}
          {query && (
            <button onClick={() => { setQuery(''); setResults([]); inputRef.current?.focus(); }} className="text-text-dim hover:text-text shrink-0">
              <X size={14} />
            </button>
          )}
        </div>

        {showSuggestions && results.length > 0 && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setShowSuggestions(false)} />
            <div className="absolute top-full left-0 right-0 mt-1 bg-panel border border-border rounded-lg shadow-xl z-20 py-1 max-h-80 overflow-y-auto">
              {results.map((r, i) => (
                <button
                  key={r.id + i}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors flex items-center gap-2 ${i === highlighted ? 'bg-panel-hover' : ''}`}
                  onMouseEnter={() => setHighlighted(i)}
                  onClick={() => selectResult(r)}
                >
                  <span className={`w-2 h-2 rounded-full shrink-0 ${
                    r.type === 'concept' ? 'bg-node-concept' :
                    r.type === 'rule' ? 'bg-node-rule' :
                    r.type === 'taxonomy' ? 'bg-node-taxonomy' :
                    r.type === 'topic' ? 'bg-node-topic' :
                    r.type === 'subtopic' ? 'bg-node-subtopic' : 'bg-node-definition'
                  }`} />
                  <span className="truncate">{r.label}</span>
                  <span className="text-xs text-text-dim ml-auto shrink-0">{r.type}</span>
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      <div className="flex-1" />

      <div className="text-xs text-text-dim">Connected</div>
    </div>
  );
}
