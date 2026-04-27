import { useState, useRef, useEffect } from 'react';
import { PanelRightOpen, RefreshCcw, Save } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSceneStore } from '../stores/useSceneStore';
import { searchNodes, getPerspectives, listScenes, saveScene, updateScene, deleteScene, getScene, getHealth } from '../api/graphApi';
import type { SearchResult, Perspective, SceneSummary, SceneUpdateInput } from '../types';
import { buildExplorerNodeSearchParams } from '../utils/explorerRuntime';
import { getDisplayLabel } from '../utils/labels';
import PerspectiveSwitcher from './command-bar/PerspectiveSwitcher';
import SearchCombobox from './command-bar/SearchCombobox';
import SceneMenu from './command-bar/SceneMenu';
import { getGraphLayoutLabel } from './graph/layoutOptions';

export default function CommandBar() {
  const navigate = useNavigate();
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
  const [healthLabel, setHealthLabel] = useState('Checking API…');
  const inputRef = useRef<HTMLInputElement>(null);

  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const activeSceneName = useSceneStore(s => s.activeSceneName);
  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const query = useSceneStore(s => s.searchQuery);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setPendingSelectedNode = useSceneStore(s => s.setPendingSelectedNode);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setSearchQuery = useSceneStore(s => s.setSearchQuery);
  const openInspector = useSceneStore(s => s.openInspector);
  const closeInspector = useSceneStore(s => s.closeInspector);
  const requestFocusNode = useSceneStore(s => s.requestFocusNode);
  const setActiveScene = useSceneStore(s => s.setActiveScene);
  const nodes = useSceneStore(s => s.nodes);
  const edges = useSceneStore(s => s.edges);
  const inspectorOpen = useSceneStore(s => s.inspectorOpen);
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
    try {
      const nextScenes = await listScenes();
      setScenes(nextScenes);
    } catch (error) {
      setSceneMessage(error instanceof Error ? error.message : 'Failed to load scenes');
      setScenes([]);
    }
  }

  async function refreshHealthStatus() {
    try {
      const health = await getHealth();
      if (health.aecMepfs === 'ready') {
        setHealthLabel(health.neo4j === 'connected' ? 'AEC-MEPFS ready · Neo4j connected' : 'AEC-MEPFS ready · Neo4j degraded');
      } else {
        setHealthLabel(health.status === 'ok' ? 'Neo4j connected' : 'API degraded');
      }
    } catch {
      setHealthLabel('API unavailable');
    }
  }

  useEffect(() => {
    getPerspectives()
      .then(setPerspectives)
      .catch((error) => {
        setSceneMessage(error instanceof Error ? error.message : 'Failed to load perspectives');
        setPerspectives([]);
      });
    void Promise.resolve().then(() => {
      void refreshScenes();
      void refreshHealthStatus();
    });
    const intervalId = window.setInterval(() => {
      void refreshHealthStatus();
    }, 15000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    if (!sceneMessage) return;
    const timer = setTimeout(() => setSceneMessage(null), 3000);
    return () => clearTimeout(timer);
  }, [sceneMessage]);

  useEffect(() => {
    if (!query.trim()) {
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

  function handleQueryChange(value: string) {
    setSearchQuery(value);
    if (!value.trim()) {
      setResults([]);
      setShowSuggestions(false);
      setSearching(false);
    }
  }

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
  const graphSummary = `${nodes.length.toLocaleString()} nodes · ${edges.length.toLocaleString()} edges`;
  const nodeTypes = new Set(nodes.map((node) => node.type));
  const edgeTypes = new Set(edges.map((edge) => edge.type));
  const visibleTypeCount = [...visibleNodeTypes].filter((type) => nodeTypes.has(type)).length
    + [...visibleEdgeTypes].filter((type) => edgeTypes.has(type)).length;
  const hiddenLabel = hiddenNodeIds.length > 0 ? `${hiddenNodeIds.length.toLocaleString()} hidden · ` : '';
  const graphModeSummary = `${hiddenLabel}${getGraphLayoutLabel(layout)} · ${visibleTypeCount} filters`;
  const statusClass = sceneMessage
    ? 'border-amber-400/30 bg-amber-400/10 text-amber-100'
    : healthLabel.includes('connected')
      ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-100'
      : healthLabel.includes('unavailable')
        ? 'border-rose-400/30 bg-rose-400/10 text-rose-100'
        : 'border-sky-400/30 bg-sky-400/10 text-sky-100';

  function getResultDotClass(result: SearchResult) {
    return result.type === 'concept' ? 'bg-node-concept'
      : result.type === 'rule' ? 'bg-node-rule'
        : result.type === 'taxonomy' ? 'bg-node-taxonomy'
          : result.type === 'topic' ? 'bg-node-topic'
            : result.type === 'subtopic' ? 'bg-node-subtopic'
              : result.type === 'evidence_span' ? 'bg-sky-500'
                : 'bg-node-definition';
  }

  function selectResult(r: SearchResult) {
    if (r.kind === 'node') {
      setPendingSelectedNode(r.id);
      setSelectedNode(r.id);
      openInspector();
      requestFocusNode(r.id);
      navigate(`/explore?${buildExplorerNodeSearchParams(window.location.search, r.id)}`, { replace: true });
    }
    setSearchQuery(getDisplayLabel(r));
    setShowSuggestions(false);
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
    <div className="kg-command-bar relative z-50 flex min-h-[84px] shrink-0 items-stretch overflow-visible border-b border-border">
      <div className="flex w-72 shrink-0 flex-col justify-center border-r border-border px-4 py-3">
        <div className="text-[10px] uppercase tracking-[0.32em] text-accent">Vitruvius</div>
        <div className="text-sm font-semibold tracking-tight text-text">Knowledge Graph</div>
        <div className="mt-0.5 text-[11px] text-text-dim">Explorer workspace</div>
      </div>

      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-4 gap-y-2 px-4 py-3">
        <HeaderField label="Perspective">
          <PerspectiveSwitcher
            activePerspectiveName={activePerspective?.name ?? 'AEC-MEPFS Backbone'}
            perspectiveId={perspectiveId}
            perspectives={perspectives}
            showPerspectives={showPerspectives}
            onToggle={() => setShowPerspectives(!showPerspectives)}
            onClose={() => setShowPerspectives(false)}
            onSelect={(id) => {
              setPerspectiveId(id);
              setShowPerspectives(false);
            }}
          />
        </HeaderField>

        <HeaderField label="Scene">
          <SceneMenu
            activeSceneId={activeSceneId}
            activeSceneName={activeSceneName}
            sceneFilter={sceneFilter}
            showScenes={showScenes}
            filteredScenes={filteredScenes}
            deletingSceneId={deletingSceneId}
            onToggle={() => setShowScenes(!showScenes)}
            onClose={() => setShowScenes(false)}
            onSceneFilterChange={setSceneFilter}
            onOpenScene={(sceneId) => {
              setShowScenes(false);
              navigate(`/explore?scene=${sceneId}`);
            }}
            onRenameScene={handleRenameScene}
            onDeleteScene={handleDeleteScene}
          />
        </HeaderField>

        <div className="min-w-[22rem] flex-1">
          <HeaderField label="Search graph">
            <SearchCombobox
              query={query}
              results={results}
              searching={searching}
              showSuggestions={showSuggestions}
              highlighted={highlighted}
              inputRef={inputRef}
              onQueryChange={handleQueryChange}
              onKeyDown={onKeyDown}
              onFocus={() => query.trim() && setShowSuggestions(true)}
              onClear={() => {
                setSearchQuery('');
                setResults([]);
                setShowSuggestions(false);
                setSearching(false);
                inputRef.current?.focus();
              }}
              onClose={() => setShowSuggestions(false)}
              onHighlight={setHighlighted}
              onSelect={selectResult}
              getResultDotClass={getResultDotClass}
            />
          </HeaderField>
        </div>

        <HeaderField label="Actions">
          <div className="flex items-center gap-2">
            <button
              className="kg-control flex min-h-10 items-center gap-1.5 rounded-xl px-3 py-2 text-sm transition-colors disabled:opacity-45"
              onClick={handleSaveScene}
              disabled={savingScene || nodes.length === 0}
            >
              <Save size={14} className="text-text-dim" />
              {savingScene ? 'Saving…' : 'Save'}
            </button>
            <button
              className="kg-control flex min-h-10 items-center gap-1.5 rounded-xl px-3 py-2 text-sm transition-colors disabled:opacity-45"
              onClick={handleUpdateScene}
              disabled={updatingScene || !activeSceneId || nodes.length === 0}
            >
              <RefreshCcw size={14} className="text-text-dim" />
              {updatingScene ? 'Updating…' : 'Update'}
            </button>
          </div>
        </HeaderField>
      </div>

      <div className={`${inspectorOpen ? 'w-[28rem]' : 'w-10'} relative flex shrink-0 items-center border-l border-border`}>
        {inspectorOpen && (
          <div className="grid min-w-0 flex-1 grid-cols-[minmax(0,1fr)_auto] items-center gap-4 py-3 pl-4 pr-14">
            <div className="min-w-0 leading-tight">
              <div className="text-[10px] font-medium uppercase tracking-[0.22em] text-text-dim">Inspector</div>
              <div className="mt-1 truncate text-xs text-text">{graphSummary}</div>
              <div className="mt-0.5 truncate text-[11px] text-text-dim">{graphModeSummary}</div>
            </div>
            <div className="flex shrink-0 items-center gap-3">
              <div className={`max-w-[168px] truncate rounded-full border px-3 py-1 text-[11px] leading-none ${statusClass}`} aria-live="polite">
                {sceneMessage ?? healthLabel}
              </div>
            </div>
          </div>
        )}
        <button
          className="absolute right-0 top-0 flex h-full w-10 items-center justify-center text-text-dim transition-colors hover:bg-panel-hover hover:text-text"
          onClick={inspectorOpen ? closeInspector : openInspector}
          title={inspectorOpen ? 'Minimize inspector' : 'Maximize inspector'}
          aria-label={inspectorOpen ? 'Minimize inspector' : 'Maximize inspector'}
        >
          <PanelRightOpen size={14} className={`transition-transform ${inspectorOpen ? 'scale-x-[-1]' : ''}`} />
        </button>
      </div>
    </div>
  );
}

function HeaderField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex min-w-0 flex-col gap-1">
      <span className="px-1 text-[10px] font-medium uppercase tracking-[0.22em] text-text-dim">{label}</span>
      {children}
    </div>
  );
}
