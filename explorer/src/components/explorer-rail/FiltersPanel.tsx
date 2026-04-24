import { CircleDot, Palette } from 'lucide-react';

interface Option {
  key: string;
  label: string;
  count?: number;
  available?: boolean;
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
    <div className="px-3 py-3 border-b border-border space-y-4 max-h-[60vh] overflow-y-auto bg-bg/20">
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
              aria-pressed={colorScheme === scheme.key}
              className={`px-2 py-1.5 text-xs rounded-lg border transition-colors ${
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
              aria-pressed={sizeBy === option.key}
              className={`px-2 py-1.5 text-xs rounded-lg border transition-colors ${
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
          {nodeTypes.map((nodeType) => {
            const available = nodeType.available ?? true;
            return (
            <label
              key={nodeType.key}
              className={`flex items-center gap-2 rounded-lg px-2 py-1 text-sm transition-colors ${
                available ? 'cursor-pointer hover:bg-panel-hover hover:text-text' : 'cursor-not-allowed text-text-dim/50'
              }`}
            >
              <input
                type="checkbox"
                aria-label={nodeType.label}
                checked={visibleNodeTypes.has(nodeType.key)}
                disabled={!available}
                onChange={() => onToggleNodeType(nodeType.key)}
                className="rounded border-border accent-accent"
              />
              <span className={`w-2 h-2 rounded-full ${available ? nodeType.color : 'bg-border'}`} />
              <span className="truncate">{nodeType.label}</span>
              <span className="ml-auto text-[10px] text-text-dim">{nodeType.count ?? 0}</span>
            </label>
            );
          })}
        </div>
      </div>

      <div>
        <div className="text-xs font-medium text-text-dim mb-1.5">Edge types</div>
        <div className="space-y-1">
          {edgeTypes.map((edgeType) => {
            const available = edgeType.available ?? true;
            return (
            <label
              key={edgeType.key}
              className={`flex items-center gap-2 rounded-lg px-2 py-1 text-sm transition-colors ${
                available ? 'cursor-pointer hover:bg-panel-hover hover:text-text' : 'cursor-not-allowed text-text-dim/50'
              }`}
            >
              <input
                type="checkbox"
                aria-label={edgeType.label}
                checked={visibleEdgeTypes.has(edgeType.key)}
                disabled={!available}
                onChange={() => onToggleEdgeType(edgeType.key)}
                className="rounded border-border accent-accent"
              />
              <span className="truncate">{edgeType.label}</span>
              <span className="ml-auto text-[10px] text-text-dim">{edgeType.count ?? 0}</span>
            </label>
            );
          })}
        </div>
      </div>
    </div>
  );
}
