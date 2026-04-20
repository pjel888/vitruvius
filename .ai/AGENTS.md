<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# .ai

## Purpose
Operating system for research, audits, plans, state, prompts, and agent governance memory. This subtree is governance memory, not product code.

## Key Files
| File | Description |
|------|-------------|
| `00_system/EXECUTION_LOOP.md` | Mandatory lifecycle protocol for non-trivial work |
| `00_system/principles.md` | Non-negotiable architectural law |
| `01_roadmap/master-roadmap.md` | Authoritative roadmap, priorities, phase status |
| `01_roadmap/current-phase.md` | Active execution state |
| `01_roadmap/milestone-tracker.md` | Completion truth |
| `03_plans/00-governing-implementation-plan.md` | Live plan dispatcher |
| `03_plans/INDEX.md` | Active plan inventory |
| `10_state/decisions.md` | Architecture memory and decision continuity |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `00_system/` | Execution loop, principles, performance |
| `01_roadmap/` | Roadmap, phases, milestones |
| `02_audits/` | Audited reality checks |
| `03_plans/` | Implementation intent and execution plans |
| `04_tasks/` | Task artifacts and handoff dossiers |
| `05_logs/` | Validation logs and execution evidence |
| `06_specs/` | Specification packs |
| `07_experiments/` | Experimental work and prototypes |
| `08_prompts/` | Reusable prompt templates |
| `09_archive/` | Archived plans, audits, and state |
| `10_state/` | Live state ledgers |
| `13_research/` | Research packs and background |

## For AI Agents

### Working In This Directory
- **Do not treat archived or stale docs as live authority.** Files in `09_archive/` are historical inputs only.
- **Do not restate root law.** Reference `AGENTS.md` and `00_system/` documents rather than duplicating them.
- **Keep state truthful.** After any implementation, update the relevant plan status, state files, and decision logs.
- **Authority order:** `AGENTS.md` > `00_system/` > `01_roadmap/` > `02_audits/` > `03_plans/` > codebase > README.

### Testing Requirements
- Plans and audits are validated by structural integrity, not by runtime execution.
- Verify that `INDEX.md` matches the actual directory listing after adding new plans.
- Verify that `current-phase.md` and `milestone-tracker.md` remain consistent after status changes.

### Common Patterns
- New plans go in `03_plans/` with frontmatter (`task`, `phase`, `status`, `created`).
- Completed non-trivial work must produce a validation log in `05_logs/`.
- Archived plans move to `09_archive/plans/` with a cross-reference left in the live layer.
