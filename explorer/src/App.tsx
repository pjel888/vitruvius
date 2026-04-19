import { useEffect } from 'react';
import { useSceneStore } from './stores/useSceneStore';
import { getNodesForPerspective } from './api/graphApi';
import CommandBar from './components/CommandBar';
import ExplorerRail from './components/ExplorerRail';
import GraphScene from './components/GraphScene';
import InspectorRail from './components/InspectorRail';

function App() {
  const perspectiveId = useSceneStore(s => s.perspectiveId);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setLoading = useSceneStore(s => s.setLoading);

  useEffect(() => {
    async function load() {
      setLoading(true);
      const { nodes, edges } = await getNodesForPerspective(perspectiveId);
      setGraphData(nodes, edges);
      setLoading(false);
    }
    load();
  }, [perspectiveId, setGraphData, setLoading]);

  return (
    <div className="h-screen flex flex-col bg-bg text-text overflow-hidden">
      <CommandBar />
      <div className="flex flex-1 overflow-hidden">
        <ExplorerRail />
        <GraphScene />
        <InspectorRail />
      </div>
    </div>
  );
}

export default App;
