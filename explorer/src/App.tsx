import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useSearchParams, useNavigate } from 'react-router-dom';
import { useSceneStore } from './stores/useSceneStore';
import { getNodesForPerspective } from './api/graphApi';
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
  const selectedNodeId = useSceneStore(s => s.selectedNodeId);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setSelectedNode = useSceneStore(s => s.setSelectedNode);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);
  // const explorerOpen = useSceneStore(s => s.explorerOpen);
  // const inspectorOpen = useSceneStore(s => s.inspectorOpen);
  const toggleExplorer = useSceneStore(s => s.toggleExplorer);
  const toggleInspector = useSceneStore(s => s.toggleInspector);

  // Load from URL on mount
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
  }, [perspectiveId, selectedNodeId]);

  // Load graph data when perspective changes
  useEffect(() => {
    async function load() {
      setLoading(true);
      const { nodes, edges } = await getNodesForPerspective(perspectiveId);
      setGraphData(nodes, edges);
      setLoading(false);
    }
    load();
  }, [perspectiveId, setGraphData, setLoading]);

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
