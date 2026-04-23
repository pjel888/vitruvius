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
  return (
    <div className="relative">
      <button
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors min-w-[120px] justify-between"
        onClick={onToggle}
      >
        <span className="truncate">{activeSceneName ?? 'Scenes'}</span>
        <ChevronDown size={14} className="text-text-dim shrink-0" />
      </button>
      {showScenes && (
        <>
          <div className="fixed inset-0 z-10" onClick={onClose} />
          <div className="absolute top-full right-0 mt-1 w-72 bg-panel border border-border rounded-lg shadow-xl z-20 py-1 max-h-80 overflow-y-auto">
            <div className="px-3 py-2 border-b border-border">
              <input
                value={sceneFilter}
                onChange={(event) => onSceneFilterChange(event.target.value)}
                placeholder="Filter scenes..."
                className="w-full bg-bg border border-border rounded-md px-2 py-1 text-sm outline-none focus:border-accent"
              />
            </div>
            {filteredScenes.length === 0 ? (
              <div className="px-3 py-2 text-sm text-text-dim">No saved scenes yet.</div>
            ) : (
              filteredScenes.map((scene) => (
                <div key={scene.id} className={`px-3 py-2 hover:bg-panel-hover transition-colors ${scene.id === activeSceneId ? 'text-accent' : ''}`}>
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
