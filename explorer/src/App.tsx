import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useSearchParams, useNavigate } from 'react-router-dom';
import { useSceneStore } from './stores/useSceneStore';
import { getNodesForPerspective, getScene } from './api/graphApi';
import CommandBar from './components/CommandBar';
import ExplorerRail from './components/ExplorerRail';
import GraphScene from './components/GraphScene';
import InspectorRail from './components/InspectorRail';
import HomeScreen from './components/HomeScreen';
import BottomDrawer from './components/BottomDrawer';

function ExploreView() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  // const location = useLocation();

  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const activeSceneId = useSceneStore(s => s.activeSceneId);
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);
  const applySceneState = useSceneStore(s => s.applySceneState);
  const setActiveScene = useSceneStore(s => s.setActiveScene);
  // const explorerOpen = useSceneStore(s => s.explorerOpen);
  // const inspectorOpen = useSceneStore(s => s.inspectorOpen);
  const toggleExplorer = useSceneStore(s => s.toggleExplorer);
  const toggleInspector = useSceneStore(s => s.toggleInspector);

  // Load from URL on mount
  useEffect(() => {
    const sceneId = searchParams.get('scene');
    if (!sceneId || sceneId === activeSceneId) return;
    const targetSceneId = sceneId;

    let cancelled = false;
    async function loadScene() {
      setLoading(true);
      try {
        const scene = await getScene(targetSceneId);
        if (cancelled) return;
        applySceneState(scene);
        setGraphData(scene.graph.nodes, scene.graph.edges);
      } catch {
        if (cancelled) return;
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
  }, [searchParams, activeSceneId, applySceneState, navigate, setActiveScene, setGraphData, setLoading]);

  useEffect(() => {
    const urlPerspective = searchParams.get('perspective');
    const urlNode = searchParams.get('node');
    if (urlPerspective && urlPerspective !== perspectiveId) {
      setPerspectiveId(urlPerspective);
    }
    if (urlNode) {
      setSelectedNode(urlNode);
    }
  }, []);

  // Sync state to URL
  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (activeSceneId) {
      params.set('scene', activeSceneId);
    } else {
      params.delete('scene');
    }
    if (perspectiveId && perspectiveId !== 'default') {
      params.set('perspective', perspectiveId);
    } else {
      params.delete('perspective');
    }
    if (selectedNodeId) {
      params.set('node', selectedNodeId);
    } else {
      params.delete('node');
    }
    setSearchParams(params, { replace: true });
  }, [activeSceneId, perspectiveId, selectedNodeId]);

  // Load graph data when perspective changes
  useEffect(() => {
    if (searchParams.get('scene')) return;

    async function load() {
      setLoading(true);
      try {
        const { nodes, edges } = await getNodesForPerspective(perspectiveId);
        setGraphData(nodes, edges);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [perspectiveId, searchParams, setGraphData, setLoading]);

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
    <div className="h-screen flex flex-col bg-bg text-text overflow-hidden">
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
