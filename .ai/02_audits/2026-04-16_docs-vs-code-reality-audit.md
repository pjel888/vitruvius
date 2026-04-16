---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Docs vs Code Reality Audit

## Purpose
Identify truthfulness drift between governance/state/docs claims and the live repo.

## Scope
- `AGENTS.md`
- `.ai/00_system/*`
- `.ai/01_roadmap/*`
- `.ai/03_plans/*`
- `.ai/10_state/*`
- `README.md`

## What Was Inspected
- Authority stack and state files
- README positioning and validation counts
- Existing 2026-04-16 audit docs

## What Was Tested
- Fresh runtime validation commands from PASS 1 baseline
- Cross-check of branch/commit/test counts against docs

## What Works
- `current-phase.md` and `.ai/03_plans/INDEX.md` broadly agree that the repo is between implementation sprints and in governance/planning mode.
- The live plan-layer docs are more truthful than older state snapshots.

## What Fails
- Multiple docs disagree on where current phase and milestone tracker live.
- `active_context.md` carries contradictory branch/test snapshots in the same file.
- `principles.md`, `master-roadmap.md`, and README hard-code stale validation counts.
- Existing “app integrity” audit claims Python instability that is no longer true on the current checkout.

## What Is Misleading
- README mixes delivered runtime, future AEC positioning, and externally gated browser/dashboard language in one narrative.
- Older docs read like current truth unless the reader already knows which files are stale.

## Severity-Ranked Findings
- `HIGH` Path authority conflict: prompt/governance references `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`, but the repo’s actual authority order points to `.ai/01_roadmap/current-phase.md` and `.ai/01_roadmap/milestone-tracker.md`.
- `HIGH` `active_context.md` is stale and internally contradictory on branch and validation counts.
- `HIGH` Hard-coded baseline counts in `principles.md`, `master-roadmap.md`, and README are stale against fresh PASS 1 validation.
- `MEDIUM` README’s AEC/browser/dashboards story needs explicit “vision vs current implementation” labeling.
- `MEDIUM` `milestone-tracker.md` overstates at least one shipped claim (`ProcessPoolExecutor` parallelism) relative to code reality.

## Reproduction Steps
1. Compare `AGENTS.md` authority order with actual file locations.
2. Compare `.ai/01_roadmap/current-phase.md` with `.ai/10_state/active_context.md`.
3. Run `pytest scripts/tests -q`.
4. Compare fresh counts with `.ai/00_system/principles.md`, `.ai/01_roadmap/master-roadmap.md`, and README.

## Suspected Root Causes
- Fast-moving governance/doc rewrites without a single canonical runtime-health refresh step.
- Historical sprint narratives left in live state files after branch changes.
- Vision documentation merged into operator docs without a sharper implementation boundary.

## Recommended Fix Direction
- Freeze one authoritative runtime-health snapshot and make all other docs point to it.
- Explicitly label historical files as historical or refresh them.
- Separate current implementation claims from future AEC/browser direction.

## Validation Needed After Fix
- Re-run PASS 1 validation commands.
- Confirm every branch/commit/test count matches across the live authority stack.
- Confirm path references for `current-phase` and `milestone-tracker` are consistent everywhere.

## Audit Verdict
Truthfulness drift is one of the repo’s primary stabilization problems. It is not a cosmetic issue.

## PASS 2 Note — 2026-04-16
- Live state docs were refreshed to the current `main`-branch stabilization reality.
- `active_context.md` was rewritten as a live handoff file instead of a stale feature-branch snapshot.
- README/master-roadmap wording now distinguishes historical sprint-closure numbers from the live 2026-04-16 stabilization baseline.
