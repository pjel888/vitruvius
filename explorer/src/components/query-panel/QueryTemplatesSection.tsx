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
    <details className="rounded-2xl border border-border/70 bg-bg/50 p-3 text-[11px] text-text-dim">
      <summary className="cursor-pointer text-[10px] font-semibold uppercase tracking-[0.18em] transition-colors hover:text-text">
        Templates ({templates.length})
      </summary>
      <div className="mt-3 space-y-2">
        {templates.map((template) => (
          <div key={template.label} className="flex items-center justify-between gap-2 rounded-xl border border-white/5 bg-panel/60 px-2.5 py-2">
            <button onClick={() => onSelectTemplate(template.query)} className="block flex-1 truncate text-left text-text-dim transition-colors hover:text-accent" title={template.label}>
              {template.label}
            </button>
            <button
              onClick={() => onRunTemplate(template.query)}
              className="rounded-lg border border-white/10 px-2 py-1 text-[9px] font-semibold uppercase tracking-[0.14em] text-text-dim transition hover:border-accent/50 hover:text-accent"
            >
              Run
            </button>
          </div>
        ))}
      </div>
    </details>
  );
}
