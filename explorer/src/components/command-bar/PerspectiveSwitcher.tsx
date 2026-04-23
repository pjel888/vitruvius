import { ChevronDown } from 'lucide-react';
import type { Perspective } from '../../types';

interface PerspectiveSwitcherProps {
  activePerspectiveName: string;
  perspectiveId: string;
  perspectives: Perspective[];
  showPerspectives: boolean;
  onToggle: () => void;
  onClose: () => void;
  onSelect: (id: string) => void;
}

export default function PerspectiveSwitcher({
  activePerspectiveName,
  perspectiveId,
  perspectives,
  showPerspectives,
  onToggle,
  onClose,
  onSelect,
}: PerspectiveSwitcherProps) {
  return (
    <div className="relative">
      <button
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors min-w-[140px] justify-between"
        onClick={onToggle}
      >
        <span className="truncate">{activePerspectiveName}</span>
        <ChevronDown size={14} className="text-text-dim shrink-0" />
      </button>
      {showPerspectives && (
        <>
          <div className="fixed inset-0 z-10" onClick={onClose} />
          <div className="absolute top-full left-0 mt-1 w-56 bg-panel border border-border rounded-lg shadow-xl z-20 py-1">
            {perspectives.map((perspective) => (
              <button
                key={perspective.id}
                className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors ${perspective.id === perspectiveId ? 'text-accent' : ''}`}
                onClick={() => onSelect(perspective.id)}
              >
                <div className="font-medium">{perspective.name}</div>
                <div className="text-xs text-text-dim">{perspective.description}</div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
