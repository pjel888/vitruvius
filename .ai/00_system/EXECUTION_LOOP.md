---
title: Vitruvius Standard Execution Loop (SEL)
version: 2.0
supersedes: 1.0
status: ACTIVE
owner: Vitruvius
last_updated: 2026-04-15
canonical_path: .ai/00_system/EXECUTION_LOOP.md
---

# Vitruvius Standard Execution Loop (SEL)

## Purpose

Defines the mandatory workflow for all qualifying engineering tasks across the SlateCamp codebase and its `.ai/` documentation system. The loop is enforced before any code, schema, or canonical document is touched. It exists because first answers are wrong often enough to make the loop cheaper than the rework.

---

## 0. Triggers & Scope

### SEL is REQUIRED for any change touching

- Production code (`/app`, `/components`, `/lib`, `/hooks`, `/stores`)
- Database schema, RLS policies, migrations, Server Actions, Route Handlers
- Public API surface or contract between modules
- Design tokens, brand colors, typography, Tailwind config
- Code-compliance logic (PD 1096, RA 9514, BP 344, BP 220, PD 957 computations)
- 3D module geometry, state machines, or Module Blueprint schemas
- Canonical documents under `docs/`, `.ai/01_roadmap/`, `.ai/06_specs/`, `.ai/10_state/`
- Codebase AI prompts written into `.ai/08_prompts/`

### SEL is NOT required for

- Typo fixes in non-canonical docs (READMEs, scratch notes)
- Dependency version bumps with no API change and a passing test suite
- Internal-only experiment branches under `.ai/07_experiments/` that will not be merged
- One-line copy edits to non-shipping marketing drafts

A task is *non-trivial* by default. The burden of proof is on declaring something trivial, not on declaring it non-trivial. When in doubt, run the loop.

### Identity-Locked Components — Tripwire

Any plan that proposes editing the following files triggers automatic **ESCALATE** unless the trigger file (Phase 00) contains an explicit override block authored by Philip:

- `SlideToSubmit.tsx`
- `GestureCaptureZone.tsx`
- `haptics.ts`

These files are part of the SLIDE TO SUBMIT / SLIDE TO START identity pattern and are not modifiable through the normal loop.

---

## 1. Roles

The loop assumes role separation. A single agent may play multiple roles, but adversarial phases (Phase 06) must be performed by a role separate from the one that produced the artifact under review.

| Role | Responsibility | Phases |
|---|---|---|
| **PLANNER** | Discovers, baselines, researches, audits, plans | 00–05 |
| **AUDITOR** | Adversarial review of the plan | 06 |
| **IMPLEMENTER** | Executes the checklist (typically the codebase AI with repo access) | 08 |
| **REVIEWER** | Validates outcomes against the plan | 09 |
| **STEWARD** | Closes the loop and writes the session delta | 10 |

Role assignment is recorded in the trigger file (Phase 00).

---

## 2. Artifact Index

| Phase | Output | Canonical Path |
|---|---|---|
| 00 | Trigger | `.ai/04_tasks/{task}-trigger.md` |
| 01 | Discover note | Prepended to research pack |
| 02 | Baseline | `.ai/10_state/baselines/{task}-baseline.md` |
| 03 | Research pack | `.ai/13_research/{task}-research.md` |
| 04 | Audit | `.ai/02_audits/{task}-audit.md` |
| 05 | Plan | `.ai/03_plans/{task}-plan.md` |
| 06 | Critique | Appended to plan: `## Plan Critique` |
| 07 | Checklist | Appended to plan: `## Execution Checklist` |
| 08 | Implementation | Source code + dated comments |
| 09 | Validation | `.ai/05_logs/{task}-validation.md` |
| 10 | Session delta | `.ai/05_logs/{task}-delta.md` |
| — | Deferred items | `.ai/14_deferred/{task}-deferred.md` ⚠️ NEEDS INPUT — confirm new dir |
| — | Aborted tasks | `.ai/15_aborted/{task}-rationale.md` ⚠️ NEEDS INPUT — confirm new dir |
| — | Superseded artifacts | Moved to `.ai/09_archive/` with successor pointer in front-matter |

Every artifact opens with YAML front-matter:

```yaml
---
task: {task_name}
phase: {00-10}
created: YYYY-MM-DD
author: {role}
supersedes: {prior artifact path or null}
status: {DRAFT | REVIEW | ACCEPTED | SUPERSEDED | CLOSED}
---
```

---

## Phase 00 — Trigger & Scope

**Objective.** Define the task in one sentence, draw the scope boundary, classify risk, and check the identity-lock tripwire before any other work begins.

**Requirements**

- One-sentence task statement (active verb, single deliverable)
- In-scope list (files, modules, behaviors)
- Out-of-scope list (explicitly excluded)
- Identity-locked component check (PASS / TRIPWIRE — with override block if TRIPWIRE)
- Risk class: **S** (single file, reversible) / **M** (multi-file, reversible) / **L** (schema or API contract) / **XL** (cross-cutting, irreversible)
- Role assignments for this task (PLANNER, AUDITOR, IMPLEMENTER, REVIEWER, STEWARD)
- Linked prior artifacts (if this task continues earlier work)

**Gate.** No prior artifact for the same task name exists in `ACCEPTED` or `DRAFT` status without being explicitly superseded.

**Output.** `.ai/04_tasks/{task}-trigger.md`

---

## Phase 01 — Discover

**Objective.** Read before write. Inventory what already exists in the `.ai/` system on this task or its neighbors.

**Requirements**

- List existing entries in `docs/`, `.ai/01_roadmap/`, `.ai/06_specs/`, `.ai/10_state/`, prior `.ai/03_plans/` touching this surface
- List superseded artifacts in `.ai/09_archive/` that may still be referenced elsewhere
- List open `⚠️ NEEDS INPUT` flags from prior sessions on this surface
- Note any Module Blueprint schema relevant to this task
- Note any existing codebase AI prompt in `.ai/08_prompts/` for the same surface

**Gate.** If a current `ACCEPTED` plan exists for this task, the loop halts and returns to Phase 00 for explicit supersede or merge decision.

**Output.** Prepended to the Phase 03 research pack as `## 01 — Discover`.

---

## Phase 02 — Baseline

**Objective.** Capture the current state of the world so any change has a defined origin and a defined rollback target.

**Requirements**

- Current commit SHA on the working branch
- Running version of affected modules (`package.json` + relevant feature flags)
- Last known-good state for any user-facing module touched
- Module Blueprint snapshot reference (if 3D module)
- Database schema snapshot (if migrations are in scope)

**Gate.** Baseline must be reproducible — a reader must be able to check out the listed SHA and observe the described state.

**Output.** `.ai/10_state/baselines/{task}-baseline.md`

---

## Phase 03 — Research Pack

**Objective.** Establish full context. Make every assumption explicit and traceable.

**Requirements**

- Relevant code paths (file + line range, not just file name)
- Related docs (architecture under `docs/`, roadmap under `.ai/01_roadmap/`, current state under `.ai/10_state/`, prior plans under `.ai/03_plans/`)
- External references (codes, RFCs, library docs — with URLs and access dates)
- Constraints (performance targets, mid-range Android / 4G envelope, code-compliance limits)
- Assumptions, each labeled `[A###]` with a verification path

**Gate.** Every assumption has a stated verification path. Unverified assumptions are flagged `⚠️ NEEDS INPUT`, not silently carried.

**Output.** `.ai/13_research/{task}-research.md`

---

## Phase 04 — Audit

**Objective.** Compare current state (Phase 02) against intended outcome (Phase 00). Surface every gap, risk, and conflict.

**Requirements**

- Current implementation breakdown (file-by-file)
- Gaps, each labeled `[G###]` with location and intended end state
- Risks, each labeled `[R###]` with severity (LOW / MED / HIGH / BLOCKER) and mitigation
- Conflicts with established principles (Viewport Sanctity, panel sizing, `frameloop="demand"`, computation/render separation, etc.)
- Conflicts with existing architecture or Module Blueprint

**Gate.** Every `[G###]` must be addressed by a step in Phase 05 or explicitly deferred with rationale.

**Output.** `.ai/02_audits/{task}-audit.md`

---

## Phase 05 — Implementation Plan

**Objective.** Define exact steps for execution at file and function granularity.

**Requirements**

- File-level changes, marked **EXTEND** or **NEW** (overwrite is forbidden by default — overwrite requires an explicit override block)
- Function-level changes (signature, behavior, callers affected)
- Dependency map (new packages, version constraints, bundle impact)
- Order of execution (with reasons where order is non-obvious)
- Test requirements per step (unit, integration, visual regression, manual on mid-range Android)
- Rollback procedure (per step and overall)
- Dated comment plan (`// 2026-04-15: …` for non-trivial edits)
- `⚠️ NEEDS INPUT` flags wherever real information is missing — never fabricated
- If the plan is to be handed to a codebase AI, also produce the prompt under `.ai/08_prompts/{task}-prompt.md` and link it here

**Gate.** No `[G###]` is unaccounted for. No file is touched silently.

**Output.** `.ai/03_plans/{task}-plan.md`

---

## Phase 06 — Plan Critique (Adversarial)

**Objective.** Destroy the plan before execution does it for you.

**Performed by** AUDITOR role — must be a different agent or a clearly separated planning pass. Self-critique by the PLANNER does not satisfy this phase.

**Requirements**

- Weak assumptions (cross-reference each `[A###]`)
- Edge cases the plan does not handle
- Failure points (what breaks first under load, on mobile, on slow 4G, in dark mode, with a returning user, with a partial cache)
- Performance risks (frame budget, bundle size, query complexity, memory leaks, dispose hygiene)
- Architectural violations (Client/Server boundary, computation/render separation, identity-lock proximity, RLS bypass risk)
- Scope creep risk (which steps are likely to balloon)

Each finding receives `[C###]` and a disposition:

- **ACCEPT** — fold into plan (plan is updated, gate re-runs)
- **REJECT** — leave as-is, with reasoning
- **DEFER** — log to `.ai/14_deferred/{task}-deferred.md`

**Gate.** Zero findings without disposition. No `ACCEPT` finding left unfolded into the plan.

**Output.** Appended to plan file under `## Plan Critique`.

---

## Phase 07 — Execution Checklist

**Objective.** Convert the dispositioned plan into atomic, verifiable, reversible steps.

**Requirements**

- Each step has: pre-condition, action, post-condition, test, rollback
- Each step references at least one `[G###]` or `[C###]` for traceability
- Each step is independently testable
- Each step is independently reversible (or explicitly marked irreversible with justification)
- Steps are ordered such that any prefix of the checklist leaves the system in a working state

**Gate.** A reader who has not read the plan can execute the checklist and produce the intended outcome.

**Output.** Appended to plan file under `## Execution Checklist`.

---

## Phase 08 — Implementation (Controlled)

**Performed by** IMPLEMENTER role (typically the codebase AI with repo access).

**Rules**

- Follow the checklist only. No deviations without returning to Phase 05 for an update.
- No silent changes. Every non-trivial edit carries a dated comment: `// 2026-04-15: {what and why}`
- Run the step's specified test after each step. A failing test halts execution.
- Identity-locked components remain off-limits absent the override block in Phase 00.
- Scope guard: any work outside the checklist halts and returns to Phase 05.
- Extend-not-overwrite: existing functions are extended, not replaced, unless the plan explicitly says **OVERWRITE** with rationale.

---

## Phase 09 — Validation Report

**Performed by** REVIEWER role.

**Requirements**

- Test results, per checklist step (PASS / FAIL / SKIPPED with reason)
- Edge case validation (the cases identified in Phase 06)
- Performance notes — for 3D work, sustained 30fps on mid-range Android over 4G is the bar; for general work, no measurable regression on first-paint or interaction-to-next-paint
- Regression checks against adjacent surfaces
- Known limitations (becomes input to a future task's Phase 01)

**Gate.** No FAIL or SKIPPED step without a follow-up artifact (deferred log, new task trigger, or accepted limitation).

**Output.** `.ai/05_logs/{task}-validation.md`

---

## Phase 10 — Session Delta & Close

**Performed by** STEWARD role.

**Requirements**

- Files added / modified / removed (path-level diff summary)
- Documents updated (which entries in `docs/`, `.ai/06_specs/`, `.ai/10_state/`, `.ai/01_roadmap/` changed and why)
- Documents superseded (move originals to `.ai/09_archive/` with `supersededBy` pointer in front-matter; new doc gets `supersedes` pointer)
- New `⚠️ NEEDS INPUT` items raised during execution
- Handoff notes for the next session (what the next agent needs to know that is not already in the plan)

**Gate.** Trigger file (Phase 00) is updated to `status: CLOSED` with link to delta and validation. Module Blueprint refreshed if a 3D module was touched.

**Output.** `.ai/05_logs/{task}-delta.md`

---

## 3. Failure Policy

The original v1.0 binary STOP/RETURN does not capture real failure modes. Five outcomes are valid:

| Outcome | Trigger | Action |
|---|---|---|
| **BLOCK** | Missing prerequisite phase | Return to that phase. Do not proceed. |
| **DEGRADE** | Step is harder than planned but task remains valuable at reduced scope | Document scope reduction in plan, re-run Phase 06 critique on the reduced plan, continue |
| **DEFER** | Blocker is real but outside this task's scope | Write to `.ai/14_deferred/{task}-deferred.md`, continue with what is unblocked |
| **ESCALATE** | Identity-locked component touched without override, or RLS bypass discovered, or schema change found mid-execution | Halt. Surface to Philip with full context. No further edits. |
| **ABORT** | Research or audit reveals the task should not be done | Write rationale to `.ai/15_aborted/{task}-rationale.md`. Update trigger to `status: ABORTED`. |

---

## 4. Re-entry Rules

When a phase is re-entered mid-loop, the loop does not restart from Phase 00. It restarts from the earliest invalidated phase:

- Implementation step fails → return to Phase 05 (re-plan), not Phase 03
- Audit assumption invalidated → return to Phase 03 (re-research), then 04, then 05
- Scope changes → return to Phase 00 (new trigger or amendment block)
- Critique surfaces a missing risk → return to Phase 04, fold the gap, re-plan

Every re-entry creates a new front-matter entry: `revision: N`, with a one-line note on what triggered it.

---

## 5. Enforcement

1. No direct coding without a plan.
2. No plan without an audit.
3. No audit without research.
4. No research without a baseline.
5. No baseline without discover.
6. No discover without a trigger.
7. No execution without an adversarial critique by a separate role.
8. No completion without validation.
9. No close without a session delta.
10. No edit to identity-locked components without an override block in the trigger file.

If any phase is incomplete: → STOP → return to the earliest invalidated phase per Section 4.

---

## Principle

> Do not trust the first answer. Trust only what survives the loop.
> And when the loop survives, write down what changed.

---

## Changelog

- **2.0 (2026-04-15)** — Added Phase 00 (Trigger & Scope), Phase 01 (Discover), Phase 02 (Baseline), Phase 10 (Session Delta & Close). Added Roles section with mandatory role separation for adversarial critique. Added Artifact Index with YAML front-matter standard. Added traceability IDs (`[A###]`, `[G###]`, `[R###]`, `[C###]`). Added identity-lock tripwire. Added five-state Failure Policy and Re-entry Rules. Promoted `⚠️ NEEDS INPUT` and dated comment conventions to first-class requirements. Aligned all paths to actual `.ai/` taxonomy.
- **1.0** — Original seven-phase loop. Superseded.