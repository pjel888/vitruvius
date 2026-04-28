import type { ReactNode } from 'react';

interface StoredQueriesSectionProps {
  title: string;
  icon: ReactNode;
  queries: string[];
  onSelect: (query: string) => void;
  onDelete: (query: string) => void;
}

export default function StoredQueriesSection({
  title,
  icon,
  queries,
  onSelect,
  onDelete,
}: StoredQueriesSectionProps) {
  if (queries.length === 0) return null;

  return (
    <details className="rounded-2xl border border-border/70 bg-bg/50 p-3 text-[11px] text-text-dim" open>
      <summary className="flex cursor-pointer items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.18em] transition-colors hover:text-text">
        {icon}
        {title}
      </summary>
      <div className="mt-3 space-y-2">
        {queries.map((query) => (
          <div key={query} className="flex items-center gap-2 rounded-xl border border-white/5 bg-panel/60 px-2.5 py-2">
            <button onClick={() => onSelect(query)} className="block flex-1 truncate text-left transition-colors hover:text-accent" title={query}>
              {query}
            </button>
            <button
              onClick={() => onDelete(query)}
              className="rounded-lg px-1.5 text-text-dim transition hover:bg-red-400/10 hover:text-red-300"
              title={`Delete ${title.toLowerCase().slice(0, -1)}`}
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </details>
  );
}
