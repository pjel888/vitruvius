import { CircleDot, Palette } from 'lucide-react';

interface Option {
  key: string;
  label: string;
}

interface SizeOption {
  key: 'uniform' | 'confidence' | 'degree';
  label: string;
}

interface NodeTypeOption extends Option {
  color: string;
}

interface FiltersPanelProps {
  colorScheme: string;
  sizeBy: 'uniform' | 'confidence' | 'degree';
  visibleNodeTypes: Set<string>;
  visibleEdgeTypes: Set<string>;
  colorSchemes: Option[];
  sizeOptions: SizeOption[];
  nodeTypes: NodeTypeOption[];
  edgeTypes: Option[];
  onSelectColorScheme: (scheme: string) => void;
  onSelectSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
  onToggleNodeType: (key: string) => void;
  onToggleEdgeType: (key: string) => void;
}

export default function FiltersPanel({
  colorScheme,
  sizeBy,
  visibleNodeTypes,
  visibleEdgeTypes,
  colorSchemes,
  sizeOptions,
  nodeTypes,
  edgeTypes,
  onSelectColorScheme,
  onSelectSizeBy,
  onToggleNodeType,
  onToggleEdgeType,
}: FiltersPanelProps) {
  return (
    <div className="px-3 py-2 border-b border-border space-y-4 max-h-[60vh] overflow-y-auto">
      <div>
        <div className="flex items-center gap-1.5 text-xs font-medium text-text-dim mb-1.5">
          <Palette size={12} />
          Color Scheme
        </div>
        <div className="grid grid-cols-2 gap-1">
          {colorSchemes.map((scheme) => (
            <button
              key={scheme.key}
              onClick={() => onSelectColorScheme(scheme.key)}
              className={`px-2 py-1 text-xs rounded border transition-colors ${
                colorScheme === scheme.key
                  ? 'bg-accent/20 border-accent text-accent'
                  : 'border-border text-text-dim hover:text-text hover:border-text-dim'
              }`}
            >
              {scheme.label}
            </button>
          ))}
        </div>
      </div>

      <div>
        <div className="flex items-center gap-1.5 text-xs font-medium text-text-dim mb-1.5">
          <CircleDot size={12} />
          Node Size
        </div>
        <div className="grid grid-cols-3 gap-1">
          {sizeOptions.map((option) => (
            <button
              key={option.key}
              onClick={() => onSelectSizeBy(option.key)}
              className={`px-2 py-1 text-xs rounded border transition-colors ${
                sizeBy === option.key
                  ? 'bg-accent/20 border-accent text-accent'
                  : 'border-border text-text-dim hover:text-text hover:border-text-dim'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      <div>
        <div className="text-xs font-medium text-text-dim mb-1.5">Node types</div>
        <div className="space-y-1">
          {nodeTypes.map((nodeType) => (
            <label key={nodeType.key} className="flex items-center gap-2 text-sm cursor-pointer hover:text-text transition-colors">
              <input
                type="checkbox"
                checked={visibleNodeTypes.has(nodeType.key)}
                onChange={() => onToggleNodeType(nodeType.key)}
                className="rounded border-border accent-accent"
              />
              <span className={`w-2 h-2 rounded-full ${nodeType.color}`} />
              <span className="truncate">{nodeType.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <div className="text-xs font-medium text-text-dim mb-1.5">Edge types</div>
        <div className="space-y-1">
          {edgeTypes.map((edgeType) => (
            <label key={edgeType.key} className="flex items-center gap-2 text-sm cursor-pointer hover:text-text transition-colors">
              <input
                type="checkbox"
                checked={visibleEdgeTypes.has(edgeType.key)}
                onChange={() => onToggleEdgeType(edgeType.key)}
                className="rounded border-border accent-accent"
              />
              <span className="truncate">{edgeType.label}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
