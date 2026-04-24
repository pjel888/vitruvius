import { describe, expect, test } from 'bun:test';
import { getCompactDisplayLabel, getDisplayLabel } from './labels';

describe('display label helpers', () => {
  test('uses API-provided displayLabel before canonical label', () => {
    expect(getDisplayLabel({
      id: 'rule-long-1',
      label: 'A very long canonical label that should remain available in the inspector',
      displayLabel: 'Rule · Compact label',
      type: 'rule',
    })).toBe('Rule · Compact label');
  });

  test('falls back to canonical label when displayLabel is absent', () => {
    expect(getDisplayLabel({
      id: 'concept-building-permit',
      label: 'Building Permit',
      type: 'concept',
    })).toBe('Building Permit');
  });

  test('can still cap labels as an explicit legacy fallback without mutating the source', () => {
    const item = {
      label: 'A very long rule display label that would crowd the graph canvas when zoomed out',
      displayLabel: 'Rule · Building permit documentation and occupancy requirements',
    };

    expect(getCompactDisplayLabel(item, 24)).toBe('Rule · Building permit…');
    expect(getDisplayLabel(item)).toBe('Rule · Building permit documentation and occupancy requirements');
  });
});
