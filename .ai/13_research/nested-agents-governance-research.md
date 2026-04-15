---
task: nested-agents-governance
phase: 03
created: 2026-04-15
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research Pack — Nested AGENTS Governance

## 01 — Discover

### Governing Documents Read
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/decisions.md`
- `.ai/10_state/active_context.md`
- `.ai/10_state/known_issues.md`
- `.ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md`
- `.ai/06_specs/GOVERNANCE/02_DOCUMENT_AUTHORITY_AND_UPDATE_POLICY.md`
- `.ai/06_specs/GOVERNANCE/03_TASK_CLASSIFICATION_POLICY.md`
- `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`
- `.ai/06_specs/RUST/00_README_RUST_DOC_SET.md`
- `.ai/00_system/architecture.md`
- `.ai/03_plans/INDEX.md`

### Repo-Intelligence-First Exploration
- GitNexus skill path read: `.ai/skills/gitnexus/gitnexus-exploring/SKILL.md`
- GitNexus CLI skill path read: `.ai/skills/gitnexus/gitnexus-cli/SKILL.md`
- GitNexus CLI command run:
  - `npx gitnexus status`
  - Result: repo indexed and up to date at commit `027e457`
- code-review-graph MCP tools were mandated by root law, but no accessible tool surface was exposed in this session. This was recorded as a tooling-availability constraint rather than ignored.

### Existing AGENTS Coverage
- Existing governed roots:
  - `AGENTS.md`
  - `scripts/AGENTS.md`
  - `scripts/vitruvius/AGENTS.md`
  - `scripts/vitruvius/rules/AGENTS.md`
  - `config/AGENTS.md`
  - `docs/AGENTS.md`
  - `006_System-Manifests/AGENTS.md`
- Existing nested files are thin stubs with generic descriptions and little boundary enforcement.

### Structural Clusters Relevant To This Task
- Governance / memory: `.ai/`
- Python orchestration + package surface: `scripts/`, `scripts/vitruvius/`, `scripts/tests/`
- Rust compute boundaries: `scripts/vitruvius/engine_rs/`, `scripts/vitruvius/datalog_rs/`
- TypeScript sibling and contract producer: `spatial-daemon/`
- Truth-bearing canonical storage: `003_Canonical-Knowledge-Layer/`
- Performance / graph / cache artifact layer: `005_Operational-Intelligence-Layer/`
- Operational manifests and run outputs: `006_System-Manifests/`
- Configuration and legacy docs: `config/`, `docs/`

### Directly Relevant Risks
- Governance drift: root and lower-tier docs disagree about current state file paths
- Over-generation risk: the repo has many subpackages under `scripts/vitruvius/`; adding AGENTS to all of them would create noise
- Cross-language risk: Python/Rust/Wasm/TypeScript boundaries are real and need explicit local ownership rules
- Truth risk: canonical knowledge and rules directories should not be treated like casual editable docs
- Output-directory risk: `006_System-Manifests/` and `005_Operational-Intelligence-Layer/` contain generated or semi-generated artifacts that agents should not “clean up” casually

### Candidate Directories That Likely Need Local AGENTS
- `.ai/`
- `scripts/`
- `scripts/vitruvius/`
- `scripts/tests/`
- `scripts/vitruvius/engine_rs/`
- `scripts/vitruvius/datalog_rs/`
- `scripts/vitruvius/rules/`
- `spatial-daemon/`
- `003_Canonical-Knowledge-Layer/`
- `005_Operational-Intelligence-Layer/`
- `006_System-Manifests/`
- `config/`
- `docs/`

### Candidate Directories Intentionally Not Targeted By Default
- `001_Raw-Source-Layer/` — root law already states immutability; low need for nested authoring guidance
- `002_Raw-Conversion-Layer/` — generated intermediate outputs; local AGENTS would mostly repeat “do not hand-edit generated artifacts”
- `004_Derived-Content-Layer/` — currently thin and not an active engineering boundary
- deep `scripts/vitruvius/*` subpackages such as `graph/`, `review/`, `query/`, `parsers/`, `normalization/`
  - reason: package-level `scripts/vitruvius/AGENTS.md` can cover them without fragmenting the instruction hierarchy

### Conflicts / Drift Found
1. `AGENTS.md` authority order references non-existent `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`.
2. `.ai/06_specs/GOVERNANCE/02_DOCUMENT_AUTHORITY_AND_UPDATE_POLICY.md` repeats the same stale paths.
3. `.ai/01_roadmap/current-phase.md` and `.ai/10_state/active_context.md` are stale relative to actual git branch `main`.
4. Existing nested AGENTS files describe a much smaller repository than the one present today.
