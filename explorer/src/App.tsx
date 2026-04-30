import { useEffect, useRef } from 'react';
import { BrowserRouter, Routes, Route, useSearchParams, useNavigate } from 'react-router-dom';
import { useSceneStore } from './stores/useSceneStore';
import { getNodesForPerspective, getNodesForPerspectiveUrl, getScene } from './api/graphApi';
import { shouldConsumePreloadedPerspective } from './utils/explorerRuntime';
import { DEFAULT_EXPLORER_PERSPECTIVE_ID } from './constants/perspectives';
import { loadGraphEngine } from './graph-engine/graphEngineClient';
import type { GraphEdge, GraphNode } from './types';
import CommandBar from './components/CommandBar';
import ExplorerRail from './components/ExplorerRail';
import GraphScene from './components/GraphScene';
import InspectorRail from './components/InspectorRail';
import HomeScreen from './components/HomeScreen';
import BottomDrawer from './components/BottomDrawer';

export function ExploreView() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const consumedPreloadRef = useRef(false);
  const searchParamString = searchParams.toString();
  // const location = useLocation();

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const nodes = useSceneStore(s => s.nodes);
  const preloadedPerspectiveId = useSceneStore(s => s.preloadedPerspectiveId);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setPendingSelectedNode = useSceneStore(s => s.setPendingSelectedNode);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);
  const setLoadError = useSceneStore(s => s.setLoadError);
  const setVisibleNodeTypes = useSceneStore(s => s.setVisibleNodeTypes);
  const setVisibleEdgeTypes = useSceneStore(s => s.setVisibleEdgeTypes);
  const markPreloadedPerspective = useSceneStore(s => s.markPreloadedPerspective);
  const applySceneState = useSceneStore(s => s.applySceneState);
  const setActiveScene = useSceneStore(s => s.setActiveScene);
  const openInspector = useSceneStore(s => s.openInspector);
  // const explorerOpen = useSceneStore(s => s.explorerOpen);
  // const inspectorOpen = useSceneStore(s => s.inspectorOpen);
  const toggleExplorer = useSceneStore(s => s.toggleExplorer);
  const toggleInspector = useSceneStore(s => s.toggleInspector);

  // Load from URL on mount
  useEffect(() => {
    const params = new URLSearchParams(searchParamString);
    const sceneId = params.get('scene');
    if (!sceneId || sceneId === activeSceneId) return;
    const targetSceneId = sceneId;

    let cancelled = false;
    async function loadScene() {
      setLoading(true);
      try {
        const scene = await getScene(targetSceneId);
        if (cancelled) return;
        setLoadError(null);
        applySceneState(scene);
        setGraphData(scene.graph.nodes, scene.graph.edges);
        void loadGraphEngine(scene.graph.nodes, scene.graph.edges);
      } catch (error) {
        if (cancelled) return;
        setLoadError(error instanceof Error ? error.message : 'Failed to load saved scene');
        setActiveScene(null, null);
        navigate('/explore', { replace: true });
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadScene();
    return () => {
      cancelled = true;
    };
  }, [searchParamString, activeSceneId, applySceneState, navigate, setActiveScene, setGraphData, setLoadError, setLoading]);

  useEffect(() => {
    const params = new URLSearchParams(searchParamString);
    if (params.get('scene')) return;

    const urlPerspective = params.get('perspective') || DEFAULT_EXPLORER_PERSPECTIVE_ID;
    const urlNode = params.get('node');
    const currentState = useSceneStore.getState();

    if (urlPerspective !== currentState.perspectiveId) {
      setPerspectiveId(urlPerspective);
    }

    if (urlNode && urlNode !== currentState.selectedNodeId) {
      setSelectedNode(urlNode);
      openInspector();
    }

    if (urlNode && currentState.pendingSelectedNodeId === urlNode) {
      setPendingSelectedNode(null);
    }
  }, [searchParamString, setPerspectiveId, setPendingSelectedNode, setSelectedNode, openInspector]);

  useEffect(() => {
    if (preloadedPerspectiveId !== perspectiveId) {
      consumedPreloadRef.current = false;
    }
  }, [perspectiveId, preloadedPerspectiveId]);

  // Sync state to URL
  useEffect(() => {
    const params = new URLSearchParams(searchParamString);
    if (activeSceneId) {
      params.set('scene', activeSceneId);
    } else {
      params.delete('scene');
    }
    if (perspectiveId && perspectiveId !== DEFAULT_EXPLORER_PERSPECTIVE_ID) {
      params.set('perspective', perspectiveId);
    } else {
      params.delete('perspective');
    }
    if (selectedNodeId) {
      params.set('node', selectedNodeId);
    } else {
      params.delete('node');
    }
    if (params.toString() !== searchParamString) {
      setSearchParams(params, { replace: true });
    }
  }, [activeSceneId, perspectiveId, selectedNodeId, searchParamString, setSearchParams]);

  // Load graph data when perspective changes
  useEffect(() => {
    const params = new URLSearchParams(searchParamString);
    if (params.get('focus') !== 'search') return;

    const frame = requestAnimationFrame(() => {
      const input = document.getElementById('command-search-input') as HTMLInputElement | null;
      input?.focus();
    });

    params.delete('focus');
    setSearchParams(params, { replace: true });

    return () => cancelAnimationFrame(frame);
  }, [searchParamString, setSearchParams]);

  useEffect(() => {
    if (activeSceneId) return;

    if (shouldConsumePreloadedPerspective({
      activeSceneId,
      preloadedPerspectiveId,
      perspectiveId,
      nodeCount: nodes.length,
      consumedPreload: consumedPreloadRef.current,
    })) {
      consumedPreloadRef.current = true;
      setLoadError(null);
      return;
    }

    async function load() {
      setLoading(true);
      try {
        const { nodes, edges } = await getNodesForPerspective(perspectiveId);
        setLoadError(null);
        setGraphData(nodes, edges);
        void loadGraphEngine(nodes, edges, { sourceUrl: getNodesForPerspectiveUrl(perspectiveId) });
        reconcileFiltersForGraph(nodes, edges, setVisibleNodeTypes, setVisibleEdgeTypes);
        markPreloadedPerspective(null);
      } catch (error) {
        setLoadError(error instanceof Error ? error.message : 'Failed to load graph for this perspective');
        setGraphData([], []);
        markPreloadedPerspective(null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeSceneId, markPreloadedPerspective, nodes.length, perspectiveId, preloadedPerspectiveId, setGraphData, setLoadError, setLoading, setVisibleEdgeTypes, setVisibleNodeTypes]);

  // Keyboard shortcuts
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      // Search focus: / or Ctrl+K
      if (e.key === '/' || (e.ctrlKey && e.key === 'k')) {
        e.preventDefault();
        const input = document.getElementById('command-search-input') as HTMLInputElement;
        input?.focus();
      }
      // Escape: clear selection
      if (e.key === 'Escape') {
        setSelectedNode(null);
      }
      // Toggle explorer: Ctrl+B
      if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        toggleExplorer();
      }
      // Toggle inspector: Ctrl+I
      if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        toggleInspector();
      }
      // Zoom in: + or =
      if (e.key === '+' || e.key === '=') {
        // Sigma zoom handled by graph scene
      }
      // Zoom out: -
      if (e.key === '-') {
        // Sigma zoom handled by graph scene
      }
      // Home: Ctrl+H
      if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        navigate('/');
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [navigate, setSelectedNode, toggleExplorer, toggleInspector]);

  return (
    <div className="kg-shell h-screen flex flex-col bg-bg text-text overflow-hidden">
      <CommandBar />
      <div className="flex flex-1 overflow-hidden">
        <ExplorerRail />
        <GraphScene />
        <InspectorRail />
      </div>
      <BottomDrawer />
    </div>
  );
}

function hasIntersection(activeTypes: Set<string>, availableTypes: Set<string>) {
  return [...availableTypes].some((type) => activeTypes.has(type));
}

function reconcileFiltersForGraph(
  nodes: GraphNode[],
  edges: GraphEdge[],
  setVisibleNodeTypes: (types: Set<string>) => void,
  setVisibleEdgeTypes: (types: Set<string>) => void,
) {
  const availableNodeTypes = new Set(nodes.map((node) => node.type).filter(Boolean));
  const availableEdgeTypes = new Set(edges.map((edge) => edge.type).filter(Boolean));
  const state = useSceneStore.getState();

  if (availableNodeTypes.size > 0 && !hasIntersection(state.visibleNodeTypes, availableNodeTypes)) {
    setVisibleNodeTypes(availableNodeTypes);
  }

  if (availableEdgeTypes.size > 0 && !hasIntersection(state.visibleEdgeTypes, availableEdgeTypes)) {
    setVisibleEdgeTypes(availableEdgeTypes);
  }
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeScreen />} />
        <Route path="/explore" element={<ExploreView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
