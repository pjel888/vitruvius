export interface DisplayLabelSource {
  label: string;
  displayLabel?: string;
}

export function getDisplayLabel(item: DisplayLabelSource) {
  return item.displayLabel?.trim() || item.label;
}
