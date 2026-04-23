import { Loader2, Search, X } from 'lucide-react';
import type { SearchResult } from '../../types';

interface SearchComboboxProps {
  query: string;
  results: SearchResult[];
  searching: boolean;
  showSuggestions: boolean;
  highlighted: number;
  inputRef: React.RefObject<HTMLInputElement | null>;
  onQueryChange: (value: string) => void;
  onKeyDown: (event: React.KeyboardEvent) => void;
  onFocus: () => void;
  onClear: () => void;
  onClose: () => void;
  onHighlight: (index: number) => void;
  onSelect: (result: SearchResult) => void;
  getResultDotClass: (result: SearchResult) => string;
}

export default function SearchCombobox({
  query,
  results,
  searching,
  showSuggestions,
  highlighted,
  inputRef,
  onQueryChange,
  onKeyDown,
  onFocus,
  onClear,
  onClose,
  onHighlight,
  onSelect,
  getResultDotClass,
}: SearchComboboxProps) {
  return (
    <div className="relative flex-1 max-w-xl">
      <div className="flex items-center gap-2 bg-bg border border-border rounded-md px-3 py-1.5 focus-within:border-accent transition-colors">
        <Search size={14} className="text-text-dim shrink-0" />
        <input
          id="command-search-input"
          ref={inputRef}
          type="text"
          className="flex-1 bg-transparent outline-none text-sm placeholder:text-text-dim"
          placeholder="Search nodes and taxonomies..."
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          onKeyDown={onKeyDown}
          onFocus={onFocus}
        />
        {searching && <Loader2 size={14} className="text-text-dim animate-spin shrink-0" />}
        {query && (
          <button onClick={onClear} className="text-text-dim hover:text-text shrink-0">
            <X size={14} />
          </button>
        )}
      </div>

      {showSuggestions && (
        <>
          <div className="fixed inset-0 z-10" onClick={onClose} />
          <div className="absolute top-full left-0 right-0 mt-1 bg-panel border border-border rounded-lg shadow-xl z-20 py-1 max-h-80 overflow-y-auto">
            {results.length > 0 ? results.map((result, index) => (
              <button
                key={result.id + index}
                className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors flex items-center gap-2 ${index === highlighted ? 'bg-panel-hover' : ''}`}
                onMouseEnter={() => onHighlight(index)}
                onClick={() => onSelect(result)}
              >
                <span className={`w-2 h-2 rounded-full shrink-0 ${getResultDotClass(result)}`} />
                <span className="truncate">{result.label}</span>
                <span className="text-[10px] uppercase tracking-wider text-text-dim shrink-0">{result.matchedField}</span>
                <span className="text-xs text-text-dim ml-auto shrink-0">{result.type}</span>
              </button>
            )) : (
              <div className="px-3 py-3 text-sm text-text-dim">
                No results for “{query}” in this perspective.
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
