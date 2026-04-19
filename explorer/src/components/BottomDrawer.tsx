import { X, FileText } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';

export default function BottomDrawer() {
  const bottomOpen = useSceneStore(s => s.bottomOpen);
  const bottomContent = useSceneStore(s => s.bottomContent);
  const closeBottom = useSceneStore(s => s.closeBottom);

  if (!bottomOpen || !bottomContent) return null;

  return (
    <div className="h-48 bg-panel border-t border-border flex flex-col shrink-0">
      <div className="px-4 py-2 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-medium">
          <FileText size={14} className="text-accent" />
          {bottomContent.title}
        </div>
        <button
          className="p-1 rounded hover:bg-panel-hover text-text-dim"
          onClick={closeBottom}
        >
          <X size={14} />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        {bottomContent.type === 'source' && (
          <div className="space-y-2">
            <div className="text-xs text-text-dim">{bottomContent.documentId}</div>
            <div className="text-sm leading-relaxed font-mono bg-panel-hover p-3 rounded-lg">
              {bottomContent.quote}
            </div>
            {bottomContent.deepLink && (
              <a
                href={bottomContent.deepLink}
                target="_blank"
                rel="noreferrer"
                className="text-xs text-accent hover:underline"
              >
                Open source →
              </a>
            )}
          </div>
        )}
        {bottomContent.type === 'table' && (
          <div className="text-sm text-text-dim">Table view coming soon.</div>
        )}
      </div>
    </div>
  );
}
