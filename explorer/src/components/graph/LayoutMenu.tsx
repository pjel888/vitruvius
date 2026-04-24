import { Calendar, ChevronDown, Circle, FolderTree, LayoutGrid, Map } from 'lucide-react';
import { GRAPH_LAYOUT_OPTIONS, type GraphLayout } from './layoutOptions';

interface LayoutMenuProps {
  layout: GraphLayout;
  open: boolean;
  onToggle: () => void;
  onClose: () => void;
  onSelect: (layout: GraphLayout) => void;
}

const LAYOUT_ICONS: Record<GraphLayout, React.ReactNode> = {
  forceatlas2: <LayoutGrid size={14} />,
  clustered: <FolderTree size={14} />,
  circular: <Circle size={14} />,
  time: <Calendar size={14} />,
  random: <Map size={14} />,
};

export default function LayoutMenu({ layout, open, onToggle, onClose, onSelect }: LayoutMenuProps) {
  const activeOption = GRAPH_LAYOUT_OPTIONS.find((option) => option.key === layout) ?? GRAPH_LAYOUT_OPTIONS[0];
  const menuId = 'graph-layout-menu';

  return (
    <div className="relative z-[40]">
      <button
        className="kg-control flex min-w-52 items-center justify-between gap-3 rounded-xl px-3 py-2 text-left text-sm transition-colors"
        onClick={onToggle}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={menuId}
      >
        <span className="flex min-w-0 items-center gap-2">
          <span className="text-accent">{LAYOUT_ICONS[activeOption.key]}</span>
          <span className="min-w-0">
            <span className="block text-[10px] uppercase tracking-[0.22em] text-text-dim">Layout</span>
            <span className="block truncate text-text">{activeOption.label}</span>
          </span>
        </span>
        <ChevronDown size={14} className="shrink-0 text-text-dim" />
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-[35]" onClick={onClose} />
          <div id={menuId} role="menu" className="kg-menu absolute left-0 top-full z-[40] mt-2 w-72 rounded-xl border border-border p-1.5">
            {GRAPH_LAYOUT_OPTIONS.map((option) => (
              <button
                key={option.key}
                role="menuitemradio"
                aria-checked={option.key === layout}
                className={`flex w-full items-start gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors hover:bg-panel-hover ${
                  option.key === layout ? 'bg-accent/10 text-accent' : 'text-text'
                }`}
                onClick={() => onSelect(option.key)}
              >
                <span className="mt-0.5 text-current">{LAYOUT_ICONS[option.key]}</span>
                <span className="min-w-0">
                  <span className="block font-medium">{option.label}</span>
                  <span className="block text-xs text-text-dim">{option.description}</span>
                </span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
