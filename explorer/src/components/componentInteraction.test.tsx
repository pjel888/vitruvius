import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import PerspectiveSwitcher from './command-bar/PerspectiveSwitcher';
import SearchCombobox from './command-bar/SearchCombobox';
import SceneMenu from './command-bar/SceneMenu';
import FiltersPanel from './explorer-rail/FiltersPanel';
import LayoutMenu from './graph/LayoutMenu';
import { getGraphLayoutLabel } from './graph/layoutOptions';
import QueryTemplatesSection from './query-panel/QueryTemplatesSection';
import StoredQueriesSection from './query-panel/StoredQueriesSection';
import NodeInspector from './inspector/NodeInspector';
import { useSceneStore } from '../stores/useSceneStore';

let dom: JSDOM;

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>');
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
});

afterEach(() => {
  cleanup();
});

describe('explorer component interactions', () => {
  test('PerspectiveSwitcher calls onSelect for the chosen perspective', () => {
    const onSelect = mock(() => {});
    const view = render(
      <PerspectiveSwitcher
        activePerspectiveName="All Knowledge"
        perspectiveId="default"
        perspectives={[
          { id: 'default', name: 'All Knowledge', description: 'Everything' },
          { id: 'concepts', name: 'Concepts Only', description: 'Concept graph' },
        ]}
        showPerspectives
        onToggle={() => {}}
        onClose={() => {}}
        onSelect={onSelect}
      />,
    );

    fireEvent.click(view.getByText('Concepts Only'));
    expect(onSelect).toHaveBeenCalledWith('concepts');
  });

  test('SearchCombobox calls onSelect when a result is clicked', () => {
    const onSelect = mock(() => {});
    const view = render(
      <SearchCombobox
        query="fire"
        results={[
          { id: 'taxonomy-fire-life-safety', kind: 'node', label: 'Fire Life Safety', type: 'taxonomy', matchType: 'slug', matchedField: 'slug' },
        ]}
        searching={false}
        showSuggestions
        highlighted={0}
        inputRef={{ current: null }}
        onQueryChange={() => {}}
        onKeyDown={() => {}}
        onFocus={() => {}}
        onClear={() => {}}
        onClose={() => {}}
        onHighlight={() => {}}
        onSelect={onSelect}
        getResultDotClass={() => 'bg-node-taxonomy'}
      />,
    );

    fireEvent.click(view.getByText('Fire Life Safety'));
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'taxonomy-fire-life-safety' }));
  });

  test('SearchCombobox renders compact display labels while preserving selected result identity', () => {
    const onSelect = mock(() => {});
    const longLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    const view = render(
      <SearchCombobox
        query="permit"
        results={[
          {
            id: 'rule-long-1',
            kind: 'node',
            label: longLabel,
            displayLabel: 'Rule · Building permit documentation…',
            type: 'rule',
            matchType: 'label',
            matchedField: 'label',
          },
        ]}
        searching={false}
        showSuggestions
        highlighted={0}
        inputRef={{ current: null }}
        onQueryChange={() => {}}
        onKeyDown={() => {}}
        onFocus={() => {}}
        onClear={() => {}}
        onClose={() => {}}
        onHighlight={() => {}}
        onSelect={onSelect}
        getResultDotClass={() => 'bg-node-rule'}
      />,
    );

    expect(view.getByText('Rule · Building permit documentation…')).toBeTruthy();
    expect(view.queryByText(longLabel)).toBeNull();
    fireEvent.click(view.getByText('Rule · Building permit documentation…'));
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'rule-long-1', label: longLabel }));
  });

  test('NodeInspector opens on overview and shows compact title, full label, canonical ID, sources, relationships, and metadata tabs', () => {
    const longLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    useSceneStore.setState({ pinnedNodeIds: [], pathSourceId: null, pathTargetId: null, highlightedPath: null });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: 'rule-long-1',
            label: longLabel,
            displayLabel: 'Rule · Building permit documentation…',
            type: 'rule',
            confidence: 0.91,
            status: 'accepted',
          },
          taxonomyPath: [],
          incoming: [],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    expect(view.getByText('Rule · Building permit documentation…')).toBeTruthy();
    expect(view.getByText(longLabel)).toBeTruthy();
    expect(view.getByText('rule-long-1')).toBeTruthy();
    expect(view.getByText('Overview')).toBeTruthy();
    expect(view.getByText('Relationships')).toBeTruthy();
    expect(view.getByText('Sources')).toBeTruthy();
    expect(view.getByText('Metadata')).toBeTruthy();

    fireEvent.click(view.getByText('Relationships'));
    expect(view.getByText('No relationships are available for this node.')).toBeTruthy();
    expect(view.getByText('No incoming relationships.')).toBeTruthy();
    expect(view.getByText('No outgoing relationships.')).toBeTruthy();

    fireEvent.click(view.getByText('Sources'));
    expect(view.getByText('No source materials are linked to this node.')).toBeTruthy();

    fireEvent.click(view.getByText('Metadata'));
    expect(view.getByText('Canonical ID')).toBeTruthy();
    expect(view.getByText('Type')).toBeTruthy();
    expect(view.getByText('Status')).toBeTruthy();
  });

  test('NodeInspector exposes unpin and clear-isolation actions', () => {
    const writeText = mock(() => Promise.resolve());
    Object.defineProperty(globalThis.navigator, 'clipboard', {
      value: { writeText },
      configurable: true,
    });

    useSceneStore.setState({
      pinnedNodeIds: ['rule-long-1'],
      hiddenNodeIds: ['other-node'],
      showAllRequestId: 0,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: 'rule-long-1',
            label: 'Every building permit applicant must submit complete documentation.',
            displayLabel: 'Building Permit Rule',
            type: 'rule',
          },
          taxonomyPath: [],
          incoming: [{ relType: 'DEFINED_BY', other: { id: 'concept-building-permit', label: 'Building Permit', type: 'concept' } }],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    fireEvent.click(view.getByLabelText('Unpin node'));
    expect(useSceneStore.getState().pinnedNodeIds).toEqual([]);

    fireEvent.click(view.getByLabelText('Clear node isolation'));
    expect(useSceneStore.getState().showAllRequestId).toBe(1);

    fireEvent.click(view.getByLabelText('Copy node name'));
    expect(writeText).toHaveBeenCalledWith('Building Permit Rule');

    fireEvent.click(view.getByText('Relationships'));
    fireEvent.click(view.getByLabelText('Copy incoming node name'));
    expect(writeText).toHaveBeenCalledWith('Building Permit');
  });

  test('SceneMenu calls scene actions', () => {
    const onOpenScene = mock(() => {});
    const onRenameScene = mock(() => {});
    const onDeleteScene = mock(() => {});
    const view = render(
      <SceneMenu
        activeSceneId={null}
        activeSceneName={null}
        sceneFilter=""
        showScenes
        filteredScenes={[{ id: 'scene-1', name: 'My Scene', perspectiveId: 'default', savedAt: '2026-04-23T00:00:00Z' }]}
        deletingSceneId={null}
        onToggle={() => {}}
        onClose={() => {}}
        onSceneFilterChange={() => {}}
        onOpenScene={onOpenScene}
        onRenameScene={onRenameScene}
        onDeleteScene={onDeleteScene}
      />,
    );

    fireEvent.click(view.getByText('My Scene'));
    fireEvent.click(view.getByText('Rename'));
    fireEvent.click(view.getByText('Delete'));
    expect(onOpenScene).toHaveBeenCalledWith('scene-1');
    expect(onRenameScene).toHaveBeenCalledTimes(1);
    expect(onDeleteScene).toHaveBeenCalledTimes(1);
  });

  test('FiltersPanel dispatches toggle and selection callbacks', () => {
    const onSelectColorScheme = mock(() => {});
    const onSelectSizeBy = mock(() => {});
    const onToggleNodeType = mock(() => {});
    const onToggleEdgeType = mock(() => {});
    const view = render(
      <FiltersPanel
        colorScheme="default"
        sizeBy="uniform"
        visibleNodeTypes={new Set(['concept'])}
        visibleEdgeTypes={new Set(['RELATED_TO'])}
        colorSchemes={[{ key: 'default', label: 'Default' }, { key: 'pastel', label: 'Pastel' }]}
        sizeOptions={[{ key: 'uniform', label: 'Uniform' }, { key: 'degree', label: 'By Connectivity' }]}
        nodeTypes={[{ key: 'concept', label: 'Concept', color: 'bg-node-concept' }]}
        edgeTypes={[{ key: 'RELATED_TO', label: 'RELATED_TO' }]}
        onSelectColorScheme={onSelectColorScheme}
        onSelectSizeBy={onSelectSizeBy}
        onToggleNodeType={onToggleNodeType}
        onToggleEdgeType={onToggleEdgeType}
      />,
    );

    fireEvent.click(view.getByText('Pastel'));
    fireEvent.click(view.getByText('By Connectivity'));
    fireEvent.click(view.getByLabelText('Concept'));
    fireEvent.click(view.getByLabelText('RELATED_TO'));
    expect(onSelectColorScheme).toHaveBeenCalledWith('pastel');
    expect(onSelectSizeBy).toHaveBeenCalledWith('degree');
    expect(onToggleNodeType).toHaveBeenCalledWith('concept');
    expect(onToggleEdgeType).toHaveBeenCalledWith('RELATED_TO');
  });

  test('LayoutMenu exposes readable graph layout choices', () => {
    const onSelect = mock(() => {});
    const view = render(
      <LayoutMenu
        layout="forceatlas2"
        open
        onToggle={() => {}}
        onClose={() => {}}
        onSelect={onSelect}
      />,
    );

    expect(getGraphLayoutLabel('forceatlas2')).toBe('Network Layout');
    expect(view.getAllByText('Network Layout').length).toBe(2);
    expect(view.getByText('Taxonomy Clusters')).toBeTruthy();
    fireEvent.click(view.getByText('Taxonomy Clusters'));
    expect(onSelect).toHaveBeenCalledWith('clustered');
  });

  test('QueryTemplatesSection dispatches select and run callbacks', () => {
    const onSelectTemplate = mock(() => {});
    const onRunTemplate = mock(() => {});
    const view = render(
      <QueryTemplatesSection
        templates={[{ label: 'All rules', query: 'MATCH (n) RETURN n' }]}
        onSelectTemplate={onSelectTemplate}
        onRunTemplate={onRunTemplate}
      />,
    );

    fireEvent.click(view.getByText('All rules'));
    fireEvent.click(view.getByText('Run'));
    expect(onSelectTemplate).toHaveBeenCalledWith('MATCH (n) RETURN n');
    expect(onRunTemplate).toHaveBeenCalledWith('MATCH (n) RETURN n');
  });

  test('StoredQueriesSection dispatches select and delete callbacks', () => {
    const onSelect = mock(() => {});
    const onDelete = mock(() => {});
    const view = render(
      <StoredQueriesSection
        title="Saved Queries"
        icon={<span>icon</span>}
        queries={['MATCH (n) RETURN n LIMIT 10']}
        onSelect={onSelect}
        onDelete={onDelete}
      />,
    );

    fireEvent.click(view.getByText('MATCH (n) RETURN n LIMIT 10'));
    fireEvent.click(view.getByTitle('Delete saved querie'));
    expect(onSelect).toHaveBeenCalledWith('MATCH (n) RETURN n LIMIT 10');
    expect(onDelete).toHaveBeenCalledWith('MATCH (n) RETURN n LIMIT 10');
  });
});
