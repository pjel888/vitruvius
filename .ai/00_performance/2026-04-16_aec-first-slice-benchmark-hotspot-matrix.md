---
task: aec-first-slice-benchmark-hotspots
date: 2026-04-16
author: PLANNER
status: ACCEPTED
---

# AEC First-Slice Benchmark Hotspot Matrix

## Purpose
This is the human-readable performance planning home for the bounded first AEC slice.

## Hotspot classes to watch

| Area | Likely hotspot | Why risky | Benchmark question | When to consider refactor |
|---|---|---|---|---|
| Boundary | repeated schema/footer validation | may add overhead to every import | does strict import stay cheap on bounded fixtures? | if repeated validation dominates small bounded runs |
| ECS | snapshot serialization / replay | unstable or heavy snapshots can slow all downstream lanes | what is snapshot roundtrip cost per bounded world revision? | if replay overhead dominates ECS tests |
| Spatial | bounded fact generation / routing | likely hottest Python-first path before any Rust decision | what is wall time and peak RSS per bounded spatial fixture family? | if Python reference path becomes the dominant wall time |
| Verification | AST compile + bounded solver invocation | whitelist checks can look cheap until fixture count grows | what is cost per supported rule-family fixture batch? | if compile/refusal/solver time dominates end-to-end proof |
| Artifact IO | writing candidate/admitted/promotion outputs | many small files can create noisy latency | what is artifact-write overhead per bounded slice run? | if IO dominates relative to actual computation |

## Required benchmark note destinations
Future benchmark and hotspot notes for the bounded first slice should be written under:
- `.ai/00_performance/`

Recommended filenames:
- `YYYY-MM-DD_aec-first-slice-boundary-benchmark.md`
- `YYYY-MM-DD_aec-first-slice-ecs-benchmark.md`
- `YYYY-MM-DD_aec-first-slice-spatial-benchmark.md`
- `YYYY-MM-DD_aec-first-slice-verification-benchmark.md`
- `YYYY-MM-DD_aec-first-slice-artifact-io-benchmark.md`
- `YYYY-MM-DD_aec-first-slice-hotspot-review.md`

## Minimum benchmark fields
Each first-slice performance note should include:
- work package / lane
- hardware context
- fixture family used
- command or harness
- baseline result
- current result
- wall time
- peak RSS when relevant
- threshold / interpretation
- whether refactor or Rust candidacy review is warranted

## Refactor decision rules
Use hotspot notes to justify refactor only when:
- the cost is repeatable on bounded fixtures
- the cost is inside the current slice, not caused by out-of-scope drift
- the benchmark shows meaningful pressure relative to the bounded slice goals
- a simpler structural fix is unlikely to solve it first

## Rust candidacy reminder
A hotspot does **not** automatically justify Rust.
Rust candidacy review requires:
- Python reference path exists
- parity path exists or is planned
- benchmark note shows real pressure
- the hotspot is numeric/compute-heavy rather than policy/IO-heavy

## Final rule
Performance notes should help reveal danger spots and guide later refactor decisions, not create a pretext for premature optimization.
