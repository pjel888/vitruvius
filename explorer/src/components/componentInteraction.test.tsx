import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import PerspectiveSwitcher from './command-bar/PerspectiveSwitcher';
import SearchCombobox from './command-bar/SearchCombobox';
import SceneMenu from './command-bar/SceneMenu';
import FiltersPanel from './explorer-rail/FiltersPanel';
import QueryTemplatesSection from './query-panel/QueryTemplatesSection';
import StoredQueriesSection from './query-panel/StoredQueriesSection';

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
