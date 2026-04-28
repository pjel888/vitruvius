import type { GraphNode } from '../../types';

export function getOverviewVisibleNodes(
  nodes: GraphNode[],
  hiddenNodeIds: Set<string>,
  visibleNodeTypes: Set<string>,
  filtersInitialized: boolean,
) {
  return nodes.filter((node) => {
    if (hiddenNodeIds.has(node.id)) return false;
    return !filtersInitialized || visibleNodeTypes.has(node.type);
  });
}
