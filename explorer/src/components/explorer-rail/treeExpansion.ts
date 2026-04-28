import type { TaxonomyNode } from '../../types';

export function collectExpandableTreeIds(nodes: TaxonomyNode[]): string[] {
  const ids: string[] = [];
  const visit = (node: TaxonomyNode) => {
    if (node.children.length > 0) ids.push(node.id);
    node.children.forEach(visit);
  };
  nodes.forEach(visit);
  return ids;
}
