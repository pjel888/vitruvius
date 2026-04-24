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
  const menuId = 'perspective-switcher-menu';

  return (
    <div className="relative z-[90]">
      <button
        className="kg-control flex min-h-10 min-w-[172px] items-center justify-between gap-2 rounded-xl px-3 py-2 text-sm transition-colors"
        onClick={onToggle}
        aria-haspopup="menu"
        aria-expanded={showPerspectives}
        aria-controls={menuId}
      >
        <span className="min-w-0 truncate text-left text-text">{activePerspectiveName}</span>
        <ChevronDown size={14} className="text-text-dim shrink-0" />
      </button>
      {showPerspectives && (
        <>
          <div className="fixed inset-0 z-[80]" onClick={onClose} />
          <div id={menuId} role="menu" className="kg-menu absolute top-full left-0 mt-2 w-64 border border-border rounded-xl z-[90] p-1.5">
            {perspectives.map((perspective) => (
              <button
                key={perspective.id}
                role="menuitemradio"
                aria-checked={perspective.id === perspectiveId}
                className={`w-full text-left px-3 py-2.5 text-sm hover:bg-panel-hover transition-colors rounded-lg ${perspective.id === perspectiveId ? 'text-accent bg-accent/10' : ''}`}
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
