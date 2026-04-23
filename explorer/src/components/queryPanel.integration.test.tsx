import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { cleanup, fireEvent, render } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import QueryPanel from './graph/QueryPanel';
import { useSceneStore } from '../stores/useSceneStore';

let dom: JSDOM;

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost:5173/explore' });
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
  globalThis.localStorage = dom.window.localStorage;
  useSceneStore.setState({ bottomOpen: false, bottomContent: null });
});

afterEach(() => {
  cleanup();
});

describe('QueryPanel integration', () => {
  test('running a template query opens the bottom drawer with query results', async () => {
    const runQuery = mock(async () => ({
      nodes: [{ id: 'n1', label: 'Node 1', type: 'concept' }],
      edges: [],
      recordCount: 1,
      rows: [{ id: 'row-1', values: { id: 'n1' } }],
    }));
    const mergeNodesEdges = mock(() => {});

    const view = render(
      <QueryPanel
        controllerRef={{ current: { mergeNodesEdges } as any }}
        onClose={() => {}}
        runQuery={runQuery}
      />,
    );

    fireEvent.click(view.getByText('Templates (3)'));
    fireEvent.click(view.getAllByText('Run')[0]!);

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(runQuery).toHaveBeenCalled();
    expect(mergeNodesEdges).toHaveBeenCalled();
    expect(useSceneStore.getState().bottomContent).toEqual(expect.objectContaining({
      type: 'query',
      title: 'Query Result',
    }));
  });
});
