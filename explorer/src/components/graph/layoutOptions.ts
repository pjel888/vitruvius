export type GraphLayout = 'precomputed' | 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time';

export interface GraphLayoutOption {
  key: GraphLayout;
  label: string;
  description: string;
}

export const GRAPH_LAYOUT_OPTIONS: GraphLayoutOption[] = [
  {
    key: 'precomputed',
    label: 'Saved Backbone Map',
    description: 'Open the cached wide AEC-MEPFS map exactly as arranged.',
  },
  {
    key: 'forceatlas2',
    label: 'Network Layout',
    description: 'Let connected nodes settle inside the invisible physics boundary.',
  },
  {
    key: 'clustered',
    label: 'Taxonomy Clusters',
    description: 'Group nodes around their top-level taxonomy.',
  },
  {
    key: 'circular',
    label: 'Circle Layout',
    description: 'Place every node around a single ring.',
  },
  {
    key: 'time',
    label: 'Timeline Layout',
    description: 'Arrange dated nodes from oldest to newest.',
  },
  {
    key: 'random',
    label: 'Random Scatter',
    description: 'Spread nodes randomly for visual debugging.',
  },
];

export function getGraphLayoutLabel(layout: GraphLayout) {
  return GRAPH_LAYOUT_OPTIONS.find((option) => option.key === layout)?.label ?? 'Network Layout';
}
