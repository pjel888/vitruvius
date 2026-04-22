# Milestone Tracker

**Updated:** 2026-04-21  
**Purpose:** verified milestone tracker for active, completed, blocked, and deferred milestones

## 1. Active Milestones

| Milestone | Status | Evidence | Next concrete action | Dependency / blocker |
|---|---|---|---|---|
| AEC execution-readiness decision | planned | `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md` | decide whether AEC becomes the next live implementation lane | runtime roots not yet verified |

## 2. Completed Milestones

| Milestone | Status | Evidence | Notes |
|---|---|---|---|
| Core pipeline through promotion | completed | `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/` | Not a live roadmap target anymore |
| Live-docs rebase across `.ai/01_roadmap/` and `.ai/03_plans/INDEX.md` | completed | `/.ai/01_roadmap/`, `/.ai/03_plans/INDEX.md`, `/.ai/README.md` | Active operating docs now use repo-verified status language |
| Plan-family slimming | completed | `/.ai/03_plans/INDEX.md`, `/.ai/03_plans/00-governing-implementation-plan.md`, `/.ai/archive/ARCHIVE_INDEX.md` | The active plan surface now reduces AEC to the master plan + blocked session packet and marks the remaining burst reference-only |
| Reference/path integrity cleanup | completed | `/.ai/README.md`, `/.ai/01_roadmap/`, `/.ai/05_logs/2026-04-21_control-surface-consolidation-validation.md` | Live docs no longer carry stale path/viewer/reference drift in the active surface |
| Graph build/query surface | completed | `scripts/vitruvius/graph/cli.py`, `scripts/vitruvius/graph/visualize.py`, `005_Operational-Intelligence-Layer/graph/` | Historical “not started” checklist removed from active tracking |
| Knowledge Graph v2 transition | completed | `scripts/vitruvius/kg/`, `scripts/tests/test_kg*.py`, `005_Operational-Intelligence-Layer/graph/kg-v2/` | v2 audit and rectification docs are authoritative |
| Laws-wave bounded automation and ready-family aggregate closure | completed | `.ai/10_state/laws-wave-status.json`, `.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md` | RA-386 residual-hardening is closed; do not keep as active milestone |
| Graph Explorer implementation | completed | `explorer/src/components/graph/*`, `api/index.ts`, `explorer/README.md` | Maintained as shipped capability |
| Nested AGENTS governance | completed | `**/AGENTS.md`, `.ai/05_logs/2026-04-20_nested-agents-governance-validation.md` | No longer a pending active milestone |

## 3. Blocked / Deferred Milestones

| Milestone | Status | Evidence | Blocker / reason | Next concrete action |
|---|---|---|---|---|
| AEC first bounded slice runtime kickoff | blocked | `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | runtime implementation roots not verified; planning corpus remains gated | decide whether to open the lane or demote it further |
| Generic dataset expansion beyond bounded laws-wave | blocked | `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_RELOAD_PROTOCOL.md` | current truthful state is maintenance/completion, not open expansion | reopen only with new authoritative source or explicit strategy change |
| Skills/agents layer consolidation | deferred | `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/` | not blocking core operating surface | handle after active plan-family slimming |

## 4. Milestone Evidence Notes

- Use repository artifacts and run logs as evidence before plan text.
- Treat old tranche-by-tranche and sprint-by-sprint narrative as historical reference only.
- Treat fresh verification claims as **unverified** unless they were rerun after the last implementation change.
