import { useState, useRef, useEffect } from 'react';
import { Search, ChevronDown, X, Loader2, Save, Link2, RefreshCcw, Pencil, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSceneStore } from '../stores/useSceneStore';
import { searchNodes, getPerspectives, listScenes, saveScene, updateScene, deleteScene, getScene } from '../api/graphApi';
import type { SearchResult, Perspective, SceneSummary, SceneUpdateInput } from '../types';

export default function CommandBar() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlighted, setHighlighted] = useState(0);
  const [searching, setSearching] = useState(false);
  const [perspectives, setPerspectives] = useState<Perspective[]>([]);
  const [showPerspectives, setShowPerspectives] = useState(false);
  const [scenes, setScenes] = useState<SceneSummary[]>([]);
  const [showScenes, setShowScenes] = useState(false);
  const [sceneFilter, setSceneFilter] = useState('');
  const [sceneMessage, setSceneMessage] = useState<string | null>(null);
  const [savingScene, setSavingScene] = useState(false);
  const [updatingScene, setUpdatingScene] = useState(false);
  const [deletingSceneId, setDeletingSceneId] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const activeSceneName = useSceneStore(s => s.activeSceneName);
  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setSearchQuery = useSceneStore(s => s.setSearchQuery);
  const setActiveScene = useSceneStore(s => s.setActiveScene);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const selectedEdgeId = useSceneStore(s => s.selectedEdgeId);
  const pinnedNodeIds = useSceneStore(s => s.pinnedNodeIds);
  const camera = useSceneStore(s => s.camera);
  const visibleNodeTypes = useSceneStore(s => s.visibleNodeTypes);
  const visibleEdgeTypes = useSceneStore(s => s.visibleEdgeTypes);
  const hiddenNodeIds = useSceneStore(s => s.hiddenNodeIds);
  const expandedNodeIds = useSceneStore(s => s.expandedNodeIds);
  const layout = useSceneStore(s => s.layout);
  const colorScheme = useSceneStore(s => s.colorScheme);
  const sizeBy = useSceneStore(s => s.sizeBy);

  function buildScenePayload(sceneName: string): SceneUpdateInput {
    return {
      name: sceneName,
      perspectiveId,
      camera,
      selectedNodeIds: selectedNodeId ? [selectedNodeId] : [],
      selectedEdgeIds: selectedEdgeId ? [selectedEdgeId] : [],
      pinnedNodeIds,
      filters: {
        nodeTypes: Array.from(visibleNodeTypes),
        edgeTypes: Array.from(visibleEdgeTypes),
        minConfidence: 0,
        maxConfidence: 1,
        searchQuery: query,
      },
      expandedNodeIds,
      hiddenNodeIds,
      layout,
      colorScheme,
      sizeBy,
      graph: { nodes, edges },
    };
  }

  async function refreshScenes() {
    const nextScenes = await listScenes();
    setScenes(nextScenes);
  }

  useEffect(() => {
    getPerspectives().then(setPerspectives);
    refreshScenes();
  }, []);

  useEffect(() => {
    if (!sceneMessage) return;
    const timer = setTimeout(() => setSceneMessage(null), 3000);
    return () => clearTimeout(timer);
  }, [sceneMessage]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setShowSuggestions(false);
      return;
    }
    const timer = setTimeout(async () => {
      setSearching(true);
      try {
        const res = await searchNodes(query, perspectiveId, 20);
        setResults(res);
        setShowSuggestions(true);
        setHighlighted(0);
      } catch (error) {
        setSceneMessage(error instanceof Error ? error.message : 'Search failed');
        setResults([]);
        setShowSuggestions(false);
      } finally {
        setSearching(false);
      }
    }, 150);
    return () => clearTimeout(timer);
  }, [query, perspectiveId]);

  const activePerspective = perspectives.find(p => p.id === perspectiveId);

  async function handleSaveScene() {
    if (nodes.length === 0) return;
    setSavingScene(true);
    try {
      const sceneName = activeSceneName || `${activePerspective?.name ?? 'Scene'} · ${new Date().toLocaleString()}`;
      const response = await saveScene(buildScenePayload(sceneName));

      setActiveScene(response.scene.id, response.scene.name);
      await refreshScenes();
      navigate(response.url, { replace: true });
      try {
        await navigator.clipboard.writeText(`${window.location.origin}${response.url}`);
        setSceneMessage('Scene saved and link copied');
      } catch {
        setSceneMessage('Scene saved (link copy failed)');
      }
    } catch (error) {
      setSceneMessage(error instanceof Error ? error.message : 'Scene save failed');
    } finally {
      setSavingScene(false);
    }
  }

  async function handleUpdateScene() {
    if (!activeSceneId || nodes.length === 0) return;
    setUpdatingScene(true);
    try {
      const response = await updateScene(activeSceneId, buildScenePayload(activeSceneName || `${activePerspective?.name ?? 'Scene'} · ${new Date().toLocaleString()}`));
      setActiveScene(response.scene.id, response.scene.name);
      await refreshScenes();
      navigate(`/explore?scene=${response.scene.id}`, { replace: true });
      setSceneMessage('Scene updated');
    } catch (error) {
      setSceneMessage(error instanceof Error ? error.message : 'Scene update failed');
    } finally {
      setUpdatingScene(false);
    }
  }

  async function handleRenameScene(scene: SceneSummary) {
    const nextName = window.prompt('Rename scene', scene.name)?.trim();
    if (!nextName || nextName === scene.name) return;

    try {
      const fullScene = await getScene(scene.id);
      if (!fullScene) return;
      const response = await updateScene(scene.id, { ...fullScene, name: nextName });
      if (scene.id === activeSceneId) {
        setActiveScene(response.scene.id, response.scene.name);
      }
      await refreshScenes();
      setSceneMessage('Scene renamed');
    } catch (error) {
      setSceneMessage(error instanceof Error ? error.message : 'Scene rename failed');
    }
  }

  async function handleDeleteScene(scene: SceneSummary) {
    if (!window.confirm(`Delete scene "${scene.name}"?`)) return;
    setDeletingSceneId(scene.id);
    try {
      await deleteScene(scene.id);
      await refreshScenes();
      if (scene.id === activeSceneId) {
        setActiveScene(null, null);
        navigate('/explore', { replace: true });
      }
      setSceneMessage('Scene deleted');
    } catch (error) {
      setSceneMessage(error instanceof Error ? error.message : 'Scene delete failed');
    } finally {
      setDeletingSceneId(null);
    }
  }

  const filteredScenes = scenes.filter((scene) => {
    const q = sceneFilter.trim().toLowerCase();
    if (!q) return true;
    return `${scene.name} ${scene.perspectiveId}`.toLowerCase().includes(q);
  });

  function selectResult(r: SearchResult) {
    if (r.kind === 'node') {
      setSelectedNode(r.id);
    }
    setQuery(r.label);
    setShowSuggestions(false);
    setSearchQuery(r.label);
  }

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlighted(i => Math.min(i + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlighted(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[highlighted]) {
        selectResult(results[highlighted]);
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      inputRef.current?.blur();
    } else if (e.key === 'Tab' && results.length > 0) {
      e.preventDefault();
      selectResult(results[0]);
    }
  }

  return (
    <div className="h-14 bg-panel border-b border-border flex items-center px-4 gap-3 shrink-0">
      <div className="font-semibold text-accent text-sm tracking-wide">VITRUVIUS</div>

      {/* Perspective switcher */}
      <div className="relative">
        <button
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors min-w-[140px] justify-between"
          onClick={() => setShowPerspectives(!showPerspectives)}
        >
          <span className="truncate">{activePerspective?.name ?? 'All Knowledge'}</span>
          <ChevronDown size={14} className="text-text-dim shrink-0" />
        </button>
        {showPerspectives && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setShowPerspectives(false)} />
            <div className="absolute top-full left-0 mt-1 w-56 bg-panel border border-border rounded-lg shadow-xl z-20 py-1">
              {perspectives.map(p => (
                <button
                  key={p.id}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors ${p.id === perspectiveId ? 'text-accent' : ''}`}
                  onClick={() => { setPerspectiveId(p.id); setShowPerspectives(false); }}
                >
                  <div className="font-medium">{p.name}</div>
                  <div className="text-xs text-text-dim">{p.description}</div>
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Search combobox */}
      <div className="relative flex-1 max-w-xl">
        <div className="flex items-center gap-2 bg-bg border border-border rounded-md px-3 py-1.5 focus-within:border-accent transition-colors">
          <Search size={14} className="text-text-dim shrink-0" />
          <input
            id="command-search-input"
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent outline-none text-sm placeholder:text-text-dim"
            placeholder="Search nodes, taxonomies, paths..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={onKeyDown}
            onFocus={() => query.trim() && setShowSuggestions(true)}
          />
          {searching && <Loader2 size={14} className="text-text-dim animate-spin shrink-0" />}
          {query && (
            <button onClick={() => { setQuery(''); setResults([]); inputRef.current?.focus(); }} className="text-text-dim hover:text-text shrink-0">
              <X size={14} />
            </button>
          )}
        </div>

        {showSuggestions && results.length > 0 && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setShowSuggestions(false)} />
            <div className="absolute top-full left-0 right-0 mt-1 bg-panel border border-border rounded-lg shadow-xl z-20 py-1 max-h-80 overflow-y-auto">
              {results.map((r, i) => (
                <button
                  key={r.id + i}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-panel-hover transition-colors flex items-center gap-2 ${i === highlighted ? 'bg-panel-hover' : ''}`}
                  onMouseEnter={() => setHighlighted(i)}
                  onClick={() => selectResult(r)}
                >
                  <span className={`w-2 h-2 rounded-full shrink-0 ${
                    r.type === 'concept' ? 'bg-node-concept' :
                    r.type === 'rule' ? 'bg-node-rule' :
                    r.type === 'taxonomy' ? 'bg-node-taxonomy' :
                    r.type === 'topic' ? 'bg-node-topic' :
                    r.type === 'subtopic' ? 'bg-node-subtopic' :
                    r.type === 'evidence_span' ? 'bg-sky-500' :
                    'bg-node-definition'
                  }`} />
                  <span className="truncate">{r.label}</span>
                  <span className="text-xs text-text-dim ml-auto shrink-0">{r.type}</span>
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      <div className="flex-1" />

      <div className="relative">
        <div className="flex items-center gap-2">
          <button
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors"
            onClick={handleSaveScene}
            disabled={savingScene || nodes.length === 0}
          >
            <Save size={14} className="text-text-dim" />
            {savingScene ? 'Saving…' : 'Save Scene'}
          </button>
          <button
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors disabled:opacity-50"
            onClick={handleUpdateScene}
            disabled={updatingScene || !activeSceneId || nodes.length === 0}
          >
            <RefreshCcw size={14} className="text-text-dim" />
            {updatingScene ? 'Updating…' : 'Update Scene'}
          </button>
        </div>
      </div>

      <div className="relative">
        <button
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg border border-border text-sm hover:border-accent transition-colors min-w-[120px] justify-between"
          onClick={() => setShowScenes(!showScenes)}
        >
          <span className="truncate">{activeSceneName ?? 'Scenes'}</span>
          <ChevronDown size={14} className="text-text-dim shrink-0" />
        </button>
        {showScenes && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setShowScenes(false)} />
            <div className="absolute top-full right-0 mt-1 w-72 bg-panel border border-border rounded-lg shadow-xl z-20 py-1 max-h-80 overflow-y-auto">
              <div className="px-3 py-2 border-b border-border">
                <input
                  value={sceneFilter}
                  onChange={(e) => setSceneFilter(e.target.value)}
                  placeholder="Filter scenes..."
                  className="w-full bg-bg border border-border rounded-md px-2 py-1 text-sm outline-none focus:border-accent"
                />
              </div>
              {filteredScenes.length === 0 ? (
                <div className="px-3 py-2 text-sm text-text-dim">No saved scenes yet.</div>
              ) : (
                filteredScenes.map((scene) => (
                  <div key={scene.id} className={`px-3 py-2 hover:bg-panel-hover transition-colors ${scene.id === activeSceneId ? 'text-accent' : ''}`}>
                    <button
                      className="w-full text-left"
                      onClick={() => {
                        setShowScenes(false);
                        navigate(`/explore?scene=${scene.id}`);
                      }}
                    >
                      <div className="font-medium truncate">{scene.name}</div>
                      <div className="text-xs text-text-dim flex items-center gap-1">
                        <Link2 size={10} />
                        {scene.savedAt ? new Date(scene.savedAt).toLocaleString() : scene.perspectiveId}
                      </div>
                    </button>
                    <div className="mt-2 flex items-center gap-2 text-xs">
                      <button className="hover:text-accent transition-colors" onClick={() => handleRenameScene(scene)}>
                        <Pencil size={12} className="inline mr-1" />Rename
                      </button>
                      <button
                        className="hover:text-red-400 transition-colors disabled:opacity-50"
                        onClick={() => handleDeleteScene(scene)}
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

      <div className="text-xs text-text-dim">{sceneMessage ?? 'Connected'}</div>
    </div>
  );
}
