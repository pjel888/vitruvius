# Plan â€” NodeInspector Source-Gap Detail

## Objective

Add proposal-level detail to `SourceGapWorkqueuePanel` in `NodeInspector`.

## Implementation Checklist

1. Reuse the existing `proposalById` map in `SourceGapWorkqueuePanel`.
2. Replace the proposal-ID-only display with compact proposal cards.
3. Show proposal title, ID, review status, suggested relationship, score, matched terms, target IDs, and rationale.
4. Keep explicit read-only/pending-only copy.
5. Extend the existing NodeInspector source-grounded context test to assert proposal detail visibility.
6. Run focused component tests, Explorer build, diff check, code-intelligence refresh, and GitNexus change detection.

## Safety Boundary

This is display-only. No approve/apply/admit action is added.
