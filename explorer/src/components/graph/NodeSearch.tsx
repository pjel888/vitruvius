import { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { Search, X } from 'lucide-react';
import type { GraphNode } from '../../types';

interface NodeSearchProps {
  nodes: GraphNode[];
  onSelect: (id: string) => void;
}

export default function NodeSearch({ nodes, onSelect }: NodeSearchProps) {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [highlighted, setHighlighted] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return nodes
      .filter((n) => {
        const haystack = [
          n.label,
          n.type,
          ...(n.aliases || []),
          n.slug,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase();
        return haystack.includes(q);
      })
      .slice(0, 10);
  }, [query, nodes]);

  const handleSelect = useCallback(
    (id: string) => {
      setQuery('');
      setOpen(false);
      onSelect(id);
      inputRef.current?.blur();
    },
    [onSelect]
  );

  useEffect(() => {
    setHighlighted(0);
  }, [results.length]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (!open) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setHighlighted((i) => Math.min(i + 1, results.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setHighlighted((i) => Math.max(i - 1, 0));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const node = results[highlighted];
        if (node) handleSelect(node.id);
      } else if (e.key === 'Escape') {
        setOpen(false);
        inputRef.current?.blur();
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [open, results, highlighted, handleSelect]);

  // Close on click outside
  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (!containerRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    window.addEventListener('mousedown', onClick);
    return () => window.removeEventListener('mousedown', onClick);
  }, []);

  // Scroll highlighted item into view
  useEffect(() => {
    if (!listRef.current) return;
    const el = listRef.current.children[highlighted] as HTMLElement | undefined;
    el?.scrollIntoView({ block: 'nearest' });
  }, [highlighted]);

  const typeColors: Record<string, string> = {
    taxonomy: 'bg-blue-500/20 text-blue-400',
    topic: 'bg-indigo-500/20 text-indigo-400',
    subtopic: 'bg-purple-500/20 text-purple-400',
    concept: 'bg-violet-500/20 text-violet-400',
    rule: 'bg-red-500/20 text-red-400',
    definition: 'bg-emerald-500/20 text-emerald-400',
    procedure: 'bg-amber-500/20 text-amber-400',
    exception: 'bg-pink-500/20 text-pink-400',
  };

  return (
    <div ref={containerRef} className="relative w-72">
      <div className="flex items-center gap-2 bg-panel border border-border rounded-md px-2.5 py-1.5 focus-within:border-accent transition-colors">
        <Search size={14} className="text-text-dim shrink-0" />
        <input
          ref={inputRef}
          type="text"
          placeholder="Search nodes…"
          className="bg-transparent text-sm text-text placeholder-text-dim outline-none w-full"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setOpen(true);
          }}
          onFocus={() => query.trim() && setOpen(true)}
          onKeyDown={(e) => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
              e.preventDefault();
            }
          }}
        />
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setOpen(false);
              inputRef.current?.focus();
            }}
            className="text-text-dim hover:text-text transition-colors shrink-0"
          >
            <X size={14} />
          </button>
        )}
      </div>

      {open && results.length > 0 && (
        <div
          ref={listRef}
          className="absolute top-full left-0 right-0 mt-1 bg-panel border border-border rounded-md shadow-lg max-h-72 overflow-y-auto z-50"
        >
          {results.map((node, i) => (
            <button
              key={node.id}
              onMouseEnter={() => setHighlighted(i)}
              onClick={() => handleSelect(node.id)}
              className={`w-full flex items-center gap-2 px-3 py-2 text-left transition-colors ${
                i === highlighted ? 'bg-panel-hover' : 'hover:bg-panel-hover'
              }`}
            >
              <span
                className={`text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded shrink-0 ${
                  typeColors[node.type] || 'bg-slate-500/20 text-slate-400'
                }`}
              >
                {node.type}
              </span>
              <span className="text-sm text-text truncate">{node.label}</span>
            </button>
          ))}
        </div>
      )}

      {open && query.trim() && results.length === 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-panel border border-border rounded-md shadow-lg p-3 text-sm text-text-dim z-50">
          No nodes match “{query}”.
        </div>
      )}
    </div>
  );
}
