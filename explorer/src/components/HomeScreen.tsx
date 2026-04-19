import { useNavigate } from 'react-router-dom';
import { Search, GitGraph, BookOpen, Route, ShieldCheck, ChevronRight } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective } from '../api/graphApi';

export default function HomeScreen() {
  const navigate = useNavigate();
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setGraphData = useSceneStore(s => s.setGraphData);

  async function enterExplore(perspectiveId: string) {
    setPerspectiveId(perspectiveId);
    const { nodes, edges } = await getNodesForPerspective(perspectiveId);
    setGraphData(nodes, edges);
    navigate('/explore');
  }

  return (
    <div className="h-full flex flex-col items-center justify-center bg-bg p-8 overflow-y-auto">
      <div className="max-w-2xl w-full space-y-10">
        {/* Header */}
        <div className="text-center space-y-3">
          <h1 className="text-3xl font-semibold text-accent tracking-tight">Vitruvius Knowledge Graph</h1>
          <p className="text-text-dim">Explore concepts, rules, and evidence across Philippine building codes.</p>
        </div>

        {/* Primary actions */}
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => navigate('/explore')}
            className="flex items-center gap-3 p-4 rounded-xl bg-panel border border-border hover:border-accent transition-colors text-left"
          >
            <Search size={24} className="text-accent shrink-0" />
            <div>
              <div className="font-medium">Search the graph</div>
              <div className="text-xs text-text-dim">Find concepts, rules, definitions</div>
            </div>
          </button>
          <button
            onClick={() => enterExplore('default')}
            className="flex items-center gap-3 p-4 rounded-xl bg-panel border border-border hover:border-accent transition-colors text-left"
          >
            <GitGraph size={24} className="text-accent shrink-0" />
            <div>
              <div className="font-medium">Show sample graph</div>
              <div className="text-xs text-text-dim">Browse all knowledge</div>
            </div>
          </button>
        </div>

        {/* Perspectives */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-text-dim">Perspectives</div>
          <div className="grid grid-cols-2 gap-3">
            <PerspectiveCard
              icon={<BookOpen size={18} />}
              title="Concepts Only"
              description="Domain concepts and relationships"
              count="~108 nodes"
              onClick={() => enterExplore('concepts')}
            />
            <PerspectiveCard
              icon={<Route size={18} />}
              title="Taxonomy Browser"
              description="Hierarchy and classification"
              count="~86 nodes"
              onClick={() => enterExplore('taxonomy')}
            />
            <PerspectiveCard
              icon={<ShieldCheck size={18} />}
              title="Regulatory Rules"
              description="Rules and dependencies"
              count="~40 nodes"
              onClick={() => enterExplore('regulatory')}
            />
            <PerspectiveCard
              icon={<GitGraph size={18} />}
              title="All Knowledge"
              description="Everything in the graph"
              count="~205 nodes"
              onClick={() => enterExplore('default')}
            />
          </div>
        </div>

        {/* Example queries */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-text-dim">Example queries</div>
          <div className="space-y-2">
            <ExampleQuery text="Find rules about floor area" onClick={() => { setPerspectiveId('regulatory'); navigate('/explore'); }} />
            <ExampleQuery text="Browse Fire Life Safety taxonomy" onClick={() => { setPerspectiveId('taxonomy'); navigate('/explore'); }} />
            <ExampleQuery text="Trace path from BHL to AMVB" onClick={() => { setPerspectiveId('concepts'); navigate('/explore'); }} />
            <ExampleQuery text="Show high-confidence definitions" onClick={() => { setPerspectiveId('concepts'); navigate('/explore'); }} />
          </div>
        </div>
      </div>
    </div>
  );
}

function PerspectiveCard({ icon, title, description, count, onClick }: {
  icon: React.ReactNode;
  title: string;
  description: string;
  count: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-start gap-3 p-3 rounded-lg bg-panel border border-border hover:border-accent transition-colors text-left"
    >
      <div className="text-accent mt-0.5 shrink-0">{icon}</div>
      <div className="min-w-0">
        <div className="font-medium text-sm">{title}</div>
        <div className="text-xs text-text-dim">{description}</div>
        <div className="text-xs text-text-dim mt-1">{count}</div>
      </div>
    </button>
  );
}

function ExampleQuery({ text, onClick }: { text: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-panel border border-border hover:border-accent transition-colors text-left text-sm"
    >
      <ChevronRight size={14} className="text-text-dim shrink-0" />
      <span className="truncate">{text}</span>
    </button>
  );
}
