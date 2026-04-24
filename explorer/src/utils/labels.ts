export interface DisplayLabelSource {
  label: string;
  displayLabel?: string;
}

export function getDisplayLabel(item: DisplayLabelSource) {
  return item.displayLabel?.trim() || item.label;
}

export function getCompactDisplayLabel(item: DisplayLabelSource, maxLength = 48) {
  const label = getDisplayLabel(item).replace(/\s+/g, ' ').trim();
  if (label.length <= maxLength) return label;
  return `${label.slice(0, maxLength - 1).trimEnd()}…`;
}
