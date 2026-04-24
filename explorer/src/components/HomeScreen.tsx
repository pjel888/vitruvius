import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, GitGraph, BookOpen, Route, ShieldCheck, ChevronRight, FileText } from 'lucide-react';
import { useSceneStore } from '../stores/useSceneStore';
import { getNodesForPerspective, getPerspectives } from '../api/graphApi';
import type { Perspective } from '../types';
import { formatPerspectiveCount } from '../utils/explorerRuntime';

export default function HomeScreen() {
  const navigate = useNavigate();
  const [perspectives, setPerspectives] = useState<Perspective[]>([]);
  const [loadingPerspectives, setLoadingPerspectives] = useState(true);
  const [perspectiveError, setPerspectiveError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const setPerspectiveId = useSceneStore(s => s.setPerspectiveId);
  const setGraphData = useSceneStore(s => s.setGraphData);
  const setSearchQuery = useSceneStore(s => s.setSearchQuery);
  const setPathSource = useSceneStore(s => s.setPathSource);
  const setPathTarget = useSceneStore(s => s.setPathTarget);
  const markPreloadedPerspective = useSceneStore(s => s.markPreloadedPerspective);

  useEffect(() => {
    let cancelled = false;

    getPerspectives()
      .then((nextPerspectives) => {
        if (!cancelled) {
          setPerspectives(nextPerspectives);
          setPerspectiveError(null);
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setPerspectiveError(error instanceof Error ? error.message : 'Failed to load perspectives');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoadingPerspectives(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const perspectiveById = useMemo(
    () => new Map(perspectives.map((perspective) => [perspective.id, perspective])),
    [perspectives]
  );

  function getPerspectiveCountLabel(perspectiveId: string, fallback: string) {
    const nodeCount = perspectiveById.get(perspectiveId)?.nodeCount;
    return formatPerspectiveCount(nodeCount, loadingPerspectives, perspectiveError, fallback);
  }

  async function enterExplore(perspectiveId: string) {
    try {
      setActionError(null);
      setPerspectiveId(perspectiveId);
      setSearchQuery('');
      setPathSource(null);
      setPathTarget(null);
      const { nodes, edges } = await getNodesForPerspective(perspectiveId);
      setGraphData(nodes, edges);
      markPreloadedPerspective(perspectiveId);
      navigate('/explore');
    } catch (error) {
      setActionError(error instanceof Error ? error.message : 'Failed to open explorer');
    }
  }

  async function runExample(perspectiveId: string, searchQuery: string, path?: { from: string; to: string }) {
    try {
      setActionError(null);
      setPerspectiveId(perspectiveId);
      setSearchQuery(searchQuery);
      setPathSource(path?.from ?? null);
      setPathTarget(path?.to ?? null);
      const { nodes, edges } = await getNodesForPerspective(perspectiveId);
      setGraphData(nodes, edges);
      markPreloadedPerspective(perspectiveId);
      navigate('/explore');
    } catch (error) {
      setActionError(error instanceof Error ? error.message : 'Failed to run example');
    }
  }

  return (
    <div className="kg-shell h-full flex flex-col items-center justify-center bg-bg p-8 overflow-y-auto">
      <div className="max-w-5xl w-full space-y-10">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex rounded-full border border-accent/25 bg-accent/10 px-3 py-1 text-[11px] uppercase tracking-[0.26em] text-accent">
            Evidence-first graph exploration
          </div>
          <h1 className="text-5xl font-semibold tracking-tight text-text">Vitruvius Knowledge Graph</h1>
          <p className="mx-auto max-w-2xl text-base leading-7 text-text-dim">
            Start from a perspective, search with graph vocabulary, then inspect source-backed rules, concepts, and evidence.
          </p>
          {actionError && (
            <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-sm text-rose-100">
              {actionError}
            </div>
          )}
        </div>

        {/* Primary actions */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <button
            onClick={() => navigate('/explore?focus=search')}
            className="kg-card flex items-center gap-4 rounded-2xl p-5 text-left transition-colors hover:border-accent"
          >
            <Search size={24} className="text-accent shrink-0" />
            <div>
              <div className="font-medium text-text">Search the graph</div>
              <div className="text-xs text-text-dim">Open the explorer and focus search immediately</div>
            </div>
          </button>
          <button
            onClick={() => enterExplore('default')}
            className="kg-card flex items-center gap-4 rounded-2xl p-5 text-left transition-colors hover:border-accent"
          >
            <GitGraph size={24} className="text-accent shrink-0" />
            <div>
              <div className="font-medium text-text">Show sample graph</div>
              <div className="text-xs text-text-dim">Browse all knowledge</div>
            </div>
          </button>
        </div>

        {/* Perspectives */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-[0.24em] text-text-dim">Perspectives</div>
          {perspectiveError && (
            <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm text-amber-200">
              Perspective inventory is unavailable right now: {perspectiveError}
            </div>
          )}
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
            <PerspectiveCard
              icon={<BookOpen size={18} />}
              title="Concepts Only"
              description="Domain concepts and relationships"
              count={getPerspectiveCountLabel('concepts', 'Concept inventory unavailable')}
              onClick={() => enterExplore('concepts')}
            />
            <PerspectiveCard
              icon={<Route size={18} />}
              title="Taxonomy Browser"
              description="Hierarchy and classification"
              count={getPerspectiveCountLabel('taxonomy', 'Taxonomy inventory unavailable')}
              onClick={() => enterExplore('taxonomy')}
            />
            <PerspectiveCard
              icon={<ShieldCheck size={18} />}
              title="Regulatory Rules"
              description="Rules and dependencies"
              count={getPerspectiveCountLabel('regulatory', 'Rule inventory unavailable')}
              onClick={() => enterExplore('regulatory')}
            />
            <PerspectiveCard
              icon={<GitGraph size={18} />}
              title="All Knowledge"
              description="Everything in the graph"
              count={getPerspectiveCountLabel('default', 'Graph inventory unavailable')}
              onClick={() => enterExplore('default')}
            />
            <PerspectiveCard
              icon={<FileText size={18} />}
              title="Evidence Map"
              description="Browse support links and source evidence"
              count={getPerspectiveCountLabel('evidence', 'Support graph')}
              onClick={() => enterExplore('evidence')}
            />
          </div>
        </div>

        {/* Example queries */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-[0.24em] text-text-dim">Example queries</div>
          <div className="space-y-2">
            <ExampleQuery text="Open Regulatory Rules perspective" onClick={() => runExample('regulatory', '')} />
            <ExampleQuery text="Browse Fire Life Safety taxonomy" onClick={() => runExample('taxonomy', 'taxonomy-fire-life-safety')} />
            <ExampleQuery text="Prepare path tracing in Concepts Only" onClick={() => runExample('concepts', '', { from: 'concept-floor-area', to: 'concept-stairs' })} />
            <ExampleQuery text="Open Concepts Only and seed a concept search" onClick={() => runExample('concepts', 'concept')} />
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
      className="kg-card flex items-start gap-3 rounded-2xl p-4 text-left transition-colors hover:border-accent"
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
      className="kg-control w-full flex items-center gap-2 rounded-xl px-3 py-2 text-left text-sm transition-colors"
    >
      <ChevronRight size={14} className="text-text-dim shrink-0" />
      <span className="truncate">{text}</span>
    </button>
  );
}
