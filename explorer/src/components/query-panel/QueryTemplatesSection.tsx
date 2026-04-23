interface QueryTemplate {
  label: string;
  query: string;
}

interface QueryTemplatesSectionProps {
  templates: readonly QueryTemplate[];
  onSelectTemplate: (query: string) => void;
  onRunTemplate: (query: string) => void;
}

export default function QueryTemplatesSection({
  templates,
  onSelectTemplate,
  onRunTemplate,
}: QueryTemplatesSectionProps) {
  return (
    <div className="px-3 pb-3">
      <details className="text-xs text-text-dim">
        <summary className="cursor-pointer hover:text-text transition-colors">Templates ({templates.length})</summary>
        <div className="mt-1 space-y-1 pl-2">
          {templates.map((template) => (
            <div key={template.label} className="flex items-center justify-between gap-2">
              <button onClick={() => onSelectTemplate(template.query)} className="block flex-1 text-left hover:text-accent transition-colors">
                {template.label}
              </button>
              <button
                onClick={() => onRunTemplate(template.query)}
                className="text-[10px] uppercase tracking-wider text-text-dim hover:text-accent transition-colors"
              >
                Run
              </button>
            </div>
          ))}
        </div>
      </details>
    </div>
  );
}
