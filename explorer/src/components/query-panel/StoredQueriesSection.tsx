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
    <div className="px-3 pb-3">
      <details className="text-xs text-text-dim" open>
        <summary className="cursor-pointer hover:text-text transition-colors flex items-center gap-1">
          {icon}
          {title}
        </summary>
        <div className="mt-1 space-y-1 pl-2">
          {queries.map((query) => (
            <div key={query} className="flex items-center gap-2">
              <button onClick={() => onSelect(query)} className="block flex-1 text-left truncate hover:text-accent transition-colors" title={query}>
                {query}
              </button>
              <button onClick={() => onDelete(query)} className="text-text-dim hover:text-red-400 transition-colors" title={`Delete ${title.toLowerCase().slice(0, -1)}`}>
                ×
              </button>
            </div>
          ))}
        </div>
      </details>
    </div>
  );
}
