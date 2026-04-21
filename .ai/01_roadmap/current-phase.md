# Current Phase — Control-Surface Consolidation

**Status:** in_progress  
**Updated:** 2026-04-21  
**Purpose:** single authoritative statement of the current operating phase

## 1. Current Phase

Vitruvius is currently in **control-surface consolidation**.

This phase exists because repository implementation is materially ahead of several active planning documents. The work now is to keep the live planning surface short, contradiction-free, and evidence-linked.

## 2. Why This Phase Is Current

- shipped capabilities (promotion, graph/query, KG v2, laws-wave closure, explorer, nested AGENTS) already exist in the repo
- active planning docs previously mixed historical narrative with live status
- future work will be misrouted unless the active `.ai` surface stays compact and truthful

Primary evidence:

- `/.ai/AUDIT_REPORT.md`
- `/.ai/IMPLEMENTATION_MATRIX.md`
- `/.ai/03_plans/00-governing-implementation-plan.md`

## 3. Active Work Now

### 3.1 Plan-family slimming
- **Status:** in_progress
- **Evidence:** `/.ai/03_plans/`, `/.ai/archive/ARCHIVE_INDEX.md`
- **Next concrete action:** keep only the dispatcher, `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, and the minimal AEC session packet in the active index; treat completed laws-wave and governance bursts as reference-only.

### 3.2 Reference integrity maintenance
- **Status:** in_progress
- **Evidence:** `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- **Next concrete action:** remove stale `/docs` references, non-existent aggregate viewer artifacts, and invalid active-plan filename references from live docs.

### 3.3 AEC execution-readiness decision
- **Status:** planned
- **Evidence:** `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** decide whether AEC remains the next real implementation lane or should stay reference-only until runtime roots exist.

## 4. Success Criteria

This phase is done when all of the following are true:

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

Review this phase again when either of these happens:

- the active plan index has been slimmed to only live/incomplete families
- a new implementation lane is intentionally opened (for example, AEC runtime kickoff or a new bounded corpus lane)
