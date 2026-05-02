import { Loader2, Search, X } from 'lucide-react';
import type { SearchResult } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

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
  const listboxId = 'command-search-results';
  const highlightedId = results[highlighted] ? `${listboxId}-${highlighted}` : undefined;

  return (
    <div className="relative z-[90] flex-1 max-w-xl">
      <div className="kg-control flex items-center gap-2 rounded-xl px-3 py-2 focus-within:border-accent transition-colors">
        <Search size={15} className="text-accent shrink-0" />
        <input
          id="command-search-input"
          ref={inputRef}
          type="text"
          role="combobox"
          aria-autocomplete="list"
          aria-expanded={showSuggestions}
          aria-controls={listboxId}
          aria-activedescendant={highlightedId}
          aria-label="Search graph nodes, rules, taxonomies, and evidence"
          className="flex-1 bg-transparent outline-none text-sm placeholder:text-text-dim"
          placeholder="Search concepts, rules, sources..."
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          onKeyDown={onKeyDown}
          onFocus={onFocus}
        />
        {!query && <span className="kg-chip hidden sm:inline-flex rounded px-1.5 py-0.5 text-[10px] uppercase tracking-wider">Ctrl K</span>}
        {searching && <Loader2 size={14} className="text-text-dim animate-spin shrink-0" />}
        {query && (
          <button onClick={onClear} className="text-text-dim hover:text-text shrink-0" aria-label="Clear search">
            <X size={14} />
          </button>
        )}
      </div>
      <div className="sr-only" aria-live="polite">
        {searching ? 'Searching graph.' : showSuggestions ? `${results.length} graph search results available.` : ''}
      </div>

      {showSuggestions && (
        <>
          <div className="fixed inset-0 z-[80]" onClick={onClose} />
          <div
            id={listboxId}
            role="listbox"
            className="kg-menu absolute top-full left-0 right-0 mt-2 border border-border rounded-xl z-[90] p-1.5 max-h-96 overflow-y-auto"
          >
            {results.length > 0 ? results.map((result, index) => (
              <button
                key={result.id + index}
                id={`${listboxId}-${index}`}
                role="option"
                aria-selected={index === highlighted}
                className={`w-full text-left px-3 py-2.5 text-sm hover:bg-panel-hover transition-colors flex items-center gap-2 rounded-lg ${index === highlighted ? 'bg-panel-hover text-text' : 'text-text-dim'}`}
                onMouseEnter={() => onHighlight(index)}
                onClick={() => onSelect(result)}
              >
                <span className={`w-2 h-2 rounded-full shrink-0 ${getResultDotClass(result)}`} />
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-text" title={getDisplayLabel(result)}>{getDisplayLabel(result)}</span>
                  <span className="block truncate text-[11px] text-text-dim">{result.id}</span>
                  {(result.disambiguationLabel || result.ambiguity?.message) && (
                    <span className="mt-0.5 block truncate text-[11px] text-amber-100" title={result.disambiguationText || result.ambiguity?.message}>
                      {result.disambiguationLabel || result.ambiguity?.message}
                    </span>
                  )}
                </span>
                {result.reviewState && (
                  <span className="kg-chip rounded-full border-amber-400/30 bg-amber-400/10 px-2 py-0.5 text-[10px] uppercase tracking-wider text-amber-100 shrink-0">
                    {result.reviewState === 'proposed_disambiguation' ? 'pending steward review' : result.reviewState.replaceAll('_', ' ')}
                  </span>
                )}
                {result.priorityBands?.includes('P0') && <span className="kg-chip rounded-full border-rose-400/30 bg-rose-400/10 px-2 py-0.5 text-[10px] uppercase tracking-wider text-rose-100 shrink-0">P0</span>}
                <span className="kg-chip rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wider shrink-0">{result.matchedField}</span>
                <span className="text-xs text-text-dim shrink-0">{result.type}</span>
              </button>
            )) : (
              <div className="px-3 py-4 text-sm text-text-dim">
                <div className="text-text">No graph matches in this perspective.</div>
                <div className="mt-1 text-xs">Try another keyword, switch perspective, or open the query panel for Cypher.</div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
