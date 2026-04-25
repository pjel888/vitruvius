import type { GraphEdge, GraphNode } from '../../types';
import { getDisplayLabel } from '../../utils/labels';

export function deriveRuleDisplayLabelsFromConceptEdges(nodes: GraphNode[], edges: GraphEdge[]) {
  const nodeById = new Map(nodes.map((node) => [node.id, node]));
  const ruleTitleById = new Map<string, string>();

  edges.forEach((edge) => {
    if (edge.type !== 'DEFINED_BY') return;
    const concept = nodeById.get(edge.source);
    const rule = nodeById.get(edge.target);
    if (!concept || !rule || rule.type !== 'rule') return;
    if (!shouldSynthesizeRuleDisplayLabelFromConcept(rule)) return;
    const conceptLabel = titleIfAllLower(getDisplayLabel(concept));
    if (!conceptLabel) return;
    ruleTitleById.set(rule.id, conceptLabel.toLowerCase().endsWith('rule') ? conceptLabel : `${conceptLabel} Rule`);
  });

  return nodes.map((node) => {
    if (node.type !== 'rule') return node;
    const displayLabel = ruleTitleById.get(node.id) || compactRuleDisplayLabel(node.displayLabel || '');
    if (!displayLabel || node.displayLabel === displayLabel) return node;
    return { ...node, displayLabel };
  });
}

function shouldSynthesizeRuleDisplayLabelFromConcept(node: GraphNode) {
  const existing = (node.displayLabel || '').replace(/\s+/g, ' ').trim();
  if (!existing) return true;
  if (existing.startsWith('Rule ·')) return true;
  return existing.toLowerCase() === 'general rule';
}

export function compactRuleDisplayLabel(value: string) {
  const normalized = value
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (!normalized) return '';
  const withoutSourceRef = normalized.replace(/\s+\[[^\]]+\]$/g, '').trim();
  const parts = withoutSourceRef.split(/\s+—\s+/).map((part) => part.trim()).filter(Boolean);
  const semanticHead = parts[0] || withoutSourceRef;
  const sectionSuffix = buildRuleSectionSuffix(parts.slice(1));
  if (!sectionSuffix && semanticHead.length <= 56) return semanticHead;

  const suffix = sectionSuffix ? ` · ${sectionSuffix}` : '';
  const headLimit = Math.max(16, 56 - suffix.length);
  if (semanticHead.length <= headLimit) return `${semanticHead}${suffix}`;

  let compact = '';
  for (const word of semanticHead.split(' ')) {
    const next = compact ? `${compact} ${word}` : word;
    if (next.length > headLimit) break;
    compact = next;
  }
  return `${compact || semanticHead.slice(0, headLimit).trim()}${suffix}`;
}

function buildRuleSectionSuffix(parts: string[]) {
  for (const part of parts) {
    const section = part.match(/^Section\s+([A-Za-z0-9.-]+)/i);
    if (section) return `Sec. ${section[1]}`;
    const article = part.match(/^Article\s+([IVXLCDM0-9.-]+)/i);
    if (article) return `Art. ${article[1]}`;
  }
  return '';
}

function titleIfAllLower(value: string) {
  const normalized = value.replace(/\s+/g, ' ').trim();
  if (!normalized || normalized !== normalized.toLowerCase()) return normalized;
  return normalized.replace(/\b\w/g, (char) => char.toUpperCase());
}

function plainTooltipText(value: string) {
  return value
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function buildNodeTooltip(node: GraphNode) {
  const displayLabel = plainTooltipText(getDisplayLabel(node));
  const canonicalLabel = plainTooltipText(node.label || '');
  const lines = [
    displayLabel,
    plainTooltipText(node.type),
    plainTooltipText(node.id),
  ];
  if (canonicalLabel && canonicalLabel !== displayLabel) {
    lines.splice(1, 0, `Canonical: ${canonicalLabel}`);
  }
  return lines.join('\n');
}
