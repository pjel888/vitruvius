# Current Phase — Control-Surface Consolidation

**Status:** completed  
**Updated:** 2026-04-21  
**Purpose:** single authoritative statement of the current operating phase

## 1. Current Phase

Vitruvius has completed **control-surface consolidation**.

This phase existed because repository implementation was materially ahead of several active planning documents. The live planning surface is now compact and truthful enough to hand off to the next bounded decision lane.

## 2. Why This Phase Is Current

- shipped capabilities (promotion, graph/query, KG v2, laws-wave closure, explorer, nested AGENTS) already exist in the repo
- active planning docs previously mixed historical narrative with live status
- future work will be misrouted unless the active `.ai` surface stays compact and truthful

Primary evidence:

- `/.ai/AUDIT_REPORT.md`
- `/.ai/IMPLEMENTATION_MATRIX.md`
- `/.ai/03_plans/00-governing-implementation-plan.md`

## 3. Phase Closure Summary

### 3.1 Plan-family slimming
- **Status:** completed
- **Evidence:** `/.ai/03_plans/`, `/.ai/archive/ARCHIVE_INDEX.md`
- **Outcome:** the active plan surface now resolves to the dispatcher, `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, and the minimal AEC session packet; completed bursts are reference-only.

### 3.2 Reference integrity maintenance
- **Status:** completed
- **Evidence:** `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- **Outcome:** stale `/docs` references, dead artifact links, and invalid active-plan filename references were reconciled in the live docs.

### 3.3 AEC execution-readiness decision
- **Status:** planned
- **Evidence:** `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** decide whether AEC remains the next real implementation lane or should stay reference-only until runtime roots exist.

## 4. Success Criteria

This phase was considered done when all of the following became true:

1. `master-roadmap.md`, `current-phase.md`, `milestone-tracker.md`, `ACTIVE_WORK.md`, and `STRATEGIC_NEXT_MOVE.md` do not contradict each other.
2. No active doc claims an implemented capability is unimplemented.
3. No active doc points to a non-existent path that can be validated from the repo.
4. Nested AGENTS status is singular: **completed**.
5. Completed work is kept out of active-priority sections.

## 5. Blockers / Dependencies

### AEC runtime kickoff
- **Status:** blocked
- **Why:** planning artifacts exist, but runtime implementation roots were not verified.
- **Dependency:** explicit execution packet and verified code roots.

### Fresh verification for some historical claims
- **Status:** unverified
- **Why:** claims like full-suite pass counts are log-backed, not re-run in this phase.
- **Dependency:** rerun verification when the implementation surface changes.

## 6. Nested AGENTS Resolution

Nested AGENTS governance is **completed**, not pending.

Evidence:

- `**/AGENTS.md`
- `/.ai/05_logs/2026-04-20_nested-agents-governance-validation.md`

The corresponding plan is now historical/reference material and must not be treated as a live pending lane.

## 7. Next Review Trigger

Review this completed phase again when either of these happens:

- the live control surface drifts again and needs another bounded cleanup pass
- a new implementation lane is intentionally opened (for example, AEC runtime kickoff or a new bounded corpus lane)
