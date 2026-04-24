import { ChevronDown, Link2, Pencil, Trash2 } from 'lucide-react';
import type { SceneSummary } from '../../types';

interface SceneMenuProps {
  activeSceneId: string | null;
  activeSceneName: string | null;
  sceneFilter: string;
  showScenes: boolean;
  filteredScenes: SceneSummary[];
  deletingSceneId: string | null;
  onToggle: () => void;
  onClose: () => void;
  onSceneFilterChange: (value: string) => void;
  onOpenScene: (sceneId: string) => void;
  onRenameScene: (scene: SceneSummary) => void;
  onDeleteScene: (scene: SceneSummary) => void;
}

export default function SceneMenu({
  activeSceneId,
  activeSceneName,
  sceneFilter,
  showScenes,
  filteredScenes,
  deletingSceneId,
  onToggle,
  onClose,
  onSceneFilterChange,
  onOpenScene,
  onRenameScene,
  onDeleteScene,
}: SceneMenuProps) {
  const menuId = 'scene-menu';

  return (
    <div className="relative z-[90]">
      <button
        className="kg-control flex items-center gap-2 px-3 py-2 rounded-xl text-sm transition-colors min-w-[132px] justify-between"
        onClick={onToggle}
        aria-haspopup="menu"
        aria-expanded={showScenes}
        aria-controls={menuId}
      >
        <span className="min-w-0 text-left">
          <span className="block text-[10px] uppercase tracking-[0.22em] text-text-dim">Scene</span>
          <span className="block truncate text-text">{activeSceneName ?? 'Scenes'}</span>
        </span>
        <ChevronDown size={14} className="text-text-dim shrink-0" />
      </button>
      {showScenes && (
        <>
          <div className="fixed inset-0 z-[80]" onClick={onClose} />
          <div id={menuId} role="menu" className="kg-menu absolute top-full right-0 mt-2 w-80 border border-border rounded-xl z-[90] p-1.5 max-h-96 overflow-y-auto">
            <div className="px-3 py-2 border-b border-border">
              <input
                value={sceneFilter}
                onChange={(event) => onSceneFilterChange(event.target.value)}
                placeholder="Filter scenes..."
                aria-label="Filter saved scenes"
                className="w-full bg-bg/80 border border-border rounded-lg px-2.5 py-1.5 text-sm outline-none focus:border-accent"
              />
            </div>
            {filteredScenes.length === 0 ? (
              <div className="px-3 py-4 text-sm text-text-dim">No saved scenes match this filter.</div>
            ) : (
              filteredScenes.map((scene) => (
                <div key={scene.id} className={`px-3 py-2.5 hover:bg-panel-hover transition-colors rounded-lg ${scene.id === activeSceneId ? 'text-accent bg-accent/10' : ''}`}>
                  <button className="w-full text-left" onClick={() => onOpenScene(scene.id)}>
                    <div className="font-medium truncate">{scene.name}</div>
                    <div className="text-xs text-text-dim flex items-center gap-1">
                      <Link2 size={10} />
                      {scene.savedAt ? new Date(scene.savedAt).toLocaleString() : scene.perspectiveId}
                    </div>
                  </button>
                  <div className="mt-2 flex items-center gap-2 text-xs">
                    <button className="hover:text-accent transition-colors" onClick={() => onRenameScene(scene)}>
                      <Pencil size={12} className="inline mr-1" />Rename
                    </button>
                    <button
                      className="hover:text-red-400 transition-colors disabled:opacity-50"
                      onClick={() => onDeleteScene(scene)}
                      disabled={deletingSceneId === scene.id}
                    >
                      <Trash2 size={12} className="inline mr-1" />{deletingSceneId === scene.id ? 'Deleting…' : 'Delete'}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
