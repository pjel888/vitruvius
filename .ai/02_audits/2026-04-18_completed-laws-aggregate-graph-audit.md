---
task: completed-laws-aggregate-graph
created: 2026-04-18
status: complete
---

# Audit — Aggregate completed-laws graph

## Reality check
A single all-authoritative completed-laws graph is the right end-state for inspecting interconnectedness. The key risk is not conceptual, but structural: law units must stay distinct even when they share the same raw storage folder (especially `LGU` and legacy `HLURB-DHSUD`).

## Safe scope
- aggregate only the completed manifest-defined lanes
- do not pull in deferred residual folders
- preserve raw-folder truth while keeping lane/law-unit identity distinct
