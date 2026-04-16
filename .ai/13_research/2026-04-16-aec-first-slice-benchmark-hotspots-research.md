---
task: aec-first-slice-benchmark-hotspots
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC First-Slice Benchmark and Hotspots

## Purpose
Make AEC performance planning explicit enough that later implementation can identify danger spots, measure them, and decide whether refactoring is justified.

## Conclusion
Yes, benchmarking is already conceptually in the corpus via `AEC-T009`, but it should be strengthened with:
- a first-slice hotspot inventory
- explicit benchmark home under `.ai/00_performance/`
- threshold/decision rules for when a hotspot should trigger refactor or Rust candidacy review
