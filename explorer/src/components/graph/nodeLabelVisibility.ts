import type { GraphNode } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

export function getNodeGraphLabel(node: GraphNode, visibleNodeLabelTypes: Set<string>) {
  return visibleNodeLabelTypes.has(node.type) ? getDisplayLabel(node) : '';
}
