import { describe, expect, test } from 'bun:test';
import { getDisplayLabel } from './labels';

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
});
