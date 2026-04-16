# .ai/00_performance — Performance Evidence Layer

## Purpose
This directory is the human-readable markdown home for Vitruvius performance evidence:
- benchmark notes
- optimization records
- low-spec survivability findings
- performance tradeoff decisions
- innovation summaries tied to measured outcomes

It complements, rather than replaces:
- machine-readable benchmark artifacts in `.ai/10_state/`
- validation logs in `.ai/05_logs/`
- code-level benchmark harnesses under `scripts/vitruvius/bench/`

## Why this exists
Vitruvius needs a durable, searchable markdown record of performance work so future planning and implementation can answer:
- what was measured
- on what hardware
- against what workload
- what improved or regressed
- what was deferred
- what optimizations remained generic and safe versus pilot-specific shortcuts

## Recommended file types
- `YYYY-MM-DD_<topic>-benchmark.md`
- `YYYY-MM-DD_<topic>-optimization-note.md`
- `YYYY-MM-DD_<topic>-low-spec-validation.md`
- `YYYY-MM-DD_<topic>-innovation-record.md`

## Minimum record fields
Every benchmark/optimization markdown note should include:
- task / topic
- date
- hardware context
- workload description
- baseline
- current result
- interpretation
- caveats
- follow-ups

## Current status
This directory has been initialized during the laws mini dataset→graph planning task.
No historical benchmark markdown records have been migrated here yet.

## Active AEC note
- `2026-04-16_aec-first-slice-benchmark-hotspot-matrix.md` is the current human-readable benchmark/hotspot planning note for the bounded first slice.
- `2026-04-16_aec-first-slice-adjacent-surface-baseline-observations.md` captures bounded adjacent-surface readiness observations for future execution preflight.

## Relationship to planning
For the laws mini dataset→graph work, this directory is the preferred markdown destination for future:
- low-spec survivability notes
- benchmark summaries
- optimization experiments
- Rust candidacy evidence summaries
