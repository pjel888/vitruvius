# Plan â€” NodeInspector Source-Gap Overview Callout

## Objective

Add a visible Overview tab prompt when `sourceGapCount > 0`, so operators can jump directly to node-specific source-gap review.

## Implementation Checklist

1. Add a button-like callout in the Overview tab when source gaps exist.
2. The callout sets `activeTab` to `context`.
3. Include count, pending-only/read-only wording, and a concise action label.
4. Extend the NodeInspector component test.
5. Run focused tests, Explorer build, diff check, code-intelligence refresh, and GitNexus change detection.
