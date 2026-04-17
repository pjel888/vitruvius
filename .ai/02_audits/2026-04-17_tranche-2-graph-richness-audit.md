---
task: tranche-2-graph-richness
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Tranche-2 Graph Richness Audit

## Audit question
Should the next move be tranche-3, or should tranche-2 be enriched first?

## Verdict
**Enrich tranche-2 first.**

## Why
- tranche-2 execute works mechanically but yields `0` generated relationships
- moving immediately to tranche-3 would scale breadth before depth
- the current best evidence supports a bounded richness fix inside tranche-2 first

## Audit recommendation
Create a minimal tranche-2 concept-fit admission slice starting with `RA-7899`, then rerun tranche-2 source-to-graph.
