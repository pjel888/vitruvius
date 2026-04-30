---
task: explorer-performance-optimization
phase: 02
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Explorer Performance Baseline

Source: `/tmp/vitruvius_explorer_baseline.ts` run before optimization edits.

```json
{
  "measuredAtUtc": "2026-04-30T10:19:28.177Z",
  "graph": {
    "nodes": 9880,
    "edges": 13285,
    "responseBytes": 9032825,
    "responseMiB": 8.614373207092285,
    "fileSizes": {
      "reportPath": 5229,
      "artifactPath": 15685791,
      "shadowGraphPath": 5367411
    }
  },
  "timings": {
    "firstExplorerShellImportMs": 63.48016700000002,
    "fetchGraphMs": 126.664333,
    "parseGraphResponseMs": 17.224916000000007,
    "parseRawShadowGraphMs": 8.621624999999995,
    "firstSearchableGraphMs": 143.889249,
    "firstInteractiveGraphProxyMs": 143.889249,
    "search": {
      "minMs": 13.098541999999952,
      "p50Ms": 14.980374999999981,
      "p95Ms": 28.43295900000004,
      "maxMs": 29.181791999999973
    },
    "aliasLookup": {
      "minMs": 14.405042000000094,
      "p50Ms": 15.463666999999987,
      "p95Ms": 19.097999999999956,
      "maxMs": 19.097999999999956
    },
    "selectionNeighborhood": {
      "minMs": 0.27083300000003874,
      "p50Ms": 0.2880410000000211,
      "p95Ms": 0.32733299999995324,
      "maxMs": 0.46345899999982976
    },
    "highlightReasonBatch": {
      "minMs": 0.9182079999998223,
      "p50Ms": 1.077583999999888,
      "p95Ms": 2.084500000000162,
      "maxMs": 2.9610000000000127
    },
    "oneHopExpansion": {
      "minMs": 0.7091250000000855,
      "p50Ms": 0.8236660000000029,
      "p95Ms": 3.830417000000125,
      "maxMs": 3.830417000000125
    },
    "twoHopExpansion": {
      "minMs": 0.9120000000000346,
      "p50Ms": 1.0956249999999272,
      "p95Ms": 6.070125000000189,
      "maxMs": 6.070125000000189
    },
    "pathQuery": {
      "minMs": 1.4420410000000174,
      "p50Ms": 2.7662920000000213,
      "p95Ms": 4.300291000000016,
      "maxMs": 4.300291000000016
    },
    "previewPanelNodeDetail": {
      "minMs": 22.511708999999883,
      "p50Ms": 24.432958999999983,
      "p95Ms": 27.232999999999947,
      "maxMs": 29.05899999999997
    }
  },
  "memory": {
    "heapBeforeMiB": 5.291593551635742,
    "heapAfterGraphMiB": 48.36160087585449,
    "heapDeltaMiB": 43.07000732421875
  },
  "notes": [
    "Baseline uses in-process Hono API fetch plus component helper timing, not a browser FPS trace.",
    "Pan/zoom and vis-network stabilization require browser smoke after implementation."
  ]
}
```
