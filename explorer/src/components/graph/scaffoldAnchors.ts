import type { GraphNode } from '../../types';

const GENERIC_SCAFFOLD_SUFFIXES = [' Concept Anchor', ' Rule Context'];

export function isGenericBackboneScaffoldNode(node: GraphNode) {
  const type = String(node.type || '').toLowerCase();
  if (type !== 'concept' && type !== 'rule') return false;

  const label = node.displayLabel || node.label || '';
  return GENERIC_SCAFFOLD_SUFFIXES.some((suffix) => label.endsWith(suffix));
}
