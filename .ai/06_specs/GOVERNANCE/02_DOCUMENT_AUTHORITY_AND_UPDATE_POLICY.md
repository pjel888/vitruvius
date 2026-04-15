# Vitruvius Document Authority and Update Policy

## Purpose
This document defines which documents are authoritative, how document conflicts are resolved, when documents must be updated, and how stale repo memory is prevented.

Vitruvius depends on durable project memory. Agents must not rely on guesswork, conversational memory, or implicit conventions when the repository can and should carry that memory explicitly.

## Core Principle
The repository must remember the truth better than any agent session.

## Authority Model
Documents in Vitruvius do not all have equal authority. Some define law. Some describe current state. Some record proposals. Some provide historical context only.

Agents must distinguish between:
- law
- state
- plan
- audit
- research
- history
- convenience summaries

---

## Section 1 — Authority Tiers

### Tier 1 — Root Operating Law
These documents define how agents must work:
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`

These documents govern behavior. They are not optional references.

### Tier 2 — Strategic Authority
These documents define official roadmap and execution priorities:
- `.ai/01_roadmap/master-roadmap.md`

This document governs:
- phase order
- priority
- official status
- gating metrics
- definitions of done at roadmap level

### Tier 3 — Active State Authority
These documents define the live operational reality of the repo:
- `.ai/10_state/current-phase.md`
- `.ai/10_state/milestone-tracker.md`
- `.ai/10_state/decisions.md`
- other current state ledgers as designated

These documents answer:
- what is active now
- what is complete now
- what has already been decided
- what remains blocked or deferred

### Tier 4 — Audited Reality
These documents define grounded assessments of current implementation:
- `.ai/02_audits/`

Audits describe what exists and where gaps are. They do not automatically authorize implementation, but they strongly constrain planning.

### Tier 5 — Planned Intent
These documents define approved execution intent:
- `.ai/03_plans/`

Plans are actionable only if aligned with higher-tier law and state.

### Tier 6 — Specifications and Governance Extensions
These include:
- `.ai/06_specs/`
- subsystem-specific governance docs
- Rust governance pack
- validation protocols
- cross-language contracts
- truth-promotion contracts

These are binding if they are referenced by higher-tier docs or AGENTS contract and do not conflict with higher tiers.

### Tier 7 — Research
These documents explore design space:
- research PDFs
- exploratory notes
- conceptual architecture documents
- domain research compilations

Research is not implementation authorization. Research informs audits and plans.

### Tier 8 — Historical or Convenience Context
These may include:
- outdated summaries
- sprint notes embedded in old files
- historical README passages no longer fully current
- convenience notes in subdirectories

These are useful but not authoritative when they conflict with higher tiers.

---

## Section 2 — Conflict Resolution

If two documents conflict, the higher authority tier wins.

### Mandatory Conflict Handling Procedure
1. Identify the conflicting files
2. Identify each file’s authority tier
3. Follow the higher-tier file
4. Record the conflict if it reveals stale memory
5. Update or flag the lower-tier file so drift does not persist

### Absolute Rule
Agents must never silently resolve document conflicts by intuition.

---

## Section 3 — Document Types and Their Roles

### Governing Documents
Define law or protocol. Example:
- AGENTS
- execution loop
- principles
- validation policy

### State Documents
Define live truth about what is current. Example:
- current phase
- milestone tracker
- decisions log

### Audit Documents
Describe reality as inspected.

### Plan Documents
Describe intended implementation sequence.

### Research Documents
Preserve ideas, tradeoffs, open questions, and conceptual directions.

### Validation Documents
Record whether a change actually passed required checks.

### Historical Documents
Preserve memory but do not override current law or state.

---

## Section 4 — Update Triggers

Documents must be updated when reality changes.

### Must Update Governing Docs When
- execution policy changes
- architecture law changes
- validation requirements change
- task classification changes
- cross-language boundaries change
- truth governance changes

### Must Update Strategic Docs When
- phase status changes materially
- official priority changes
- gating metric changes
- roadmap truth was inaccurate

### Must Update State Docs When
- a task or sprint changes status
- a milestone changes state
- an architecture decision is made
- implementation closes or opens a gap
- validation outcome materially changes execution status

### Must Update Audits When
- the audited subsystem changed materially
- audit assumptions were invalidated
- a formerly missing implementation now exists
- a prior claim is no longer true

### Must Update Plans When
- execution path changed
- step status changed
- plan was blocked or superseded
- plan critique found invalid assumptions

### Must Update Specs or Protocols When
- a repeated pattern becomes policy
- a fragile boundary needs formalization
- a subsystem now has mature enough rules to codify

---

## Section 5 — Staleness Policy

A document is stale when it no longer truthfully represents the area it claims to describe.

### Staleness Examples
- roadmap says “planned” when feature is already shipped
- AGENTS says purpose is exam-prep only while repo now serves broader engine goals
- active sprint block contradicts current-phase
- plan still says “to do” after implementation completed
- validation report missing after a task marked complete

### Agent Response To Staleness
If stale docs are discovered:
- do not ignore
- identify the stale file
- determine if task can continue safely
- update it if within scope, or flag it explicitly

### Rule
If a stale document is authoritative and affects the current task, stop until reconciled.

---

## Section 6 — Required Update Discipline by Task Type

### Trivial Task
Update docs only if behavior, status, or contract changed.

### Moderate Task
Update relevant plan status and validation notes.

### Major Task
Update:
- plan
- validation report
- current state
- milestone tracker if status changed

### Architecture Task
Update:
- plan
- validation report
- decisions log
- possibly principles, specs, or boundary contracts

### Truth-Critical Task
Update:
- validation report
- truth-governance artifacts
- state docs
- promotion or audit records

---

## Section 7 — Required Metadata in Major Docs

Where appropriate, major docs should include:
- purpose
- scope
- status
- authority role
- version or revision date
- owner or intended audience
- relation to other documents

This reduces ambiguity for both humans and agents.

---

## Section 8 — Repo Memory Maintenance Routine

At periodic checkpoints or after major implementation batches, perform a repo-memory reconciliation pass:
1. compare current-phase against milestone tracker
2. compare milestone tracker against roadmap
3. compare decisions log against recent architectural changes
4. compare audits against current implementation reality
5. compare plans against completed work
6. compare AGENTS and specs against current workflow practice

The purpose is to keep durable repo memory aligned with reality.

---

## Section 9 — Agent Rules for Updating Documents

When updating docs, agents must:
- preserve truth
- preserve authority hierarchy
- avoid weakening constraints without reason
- avoid silently deleting still-useful repo-specific instructions
- note supersession where needed
- avoid rewriting history casually
- distinguish between “current truth” and “historical context”

---

## Section 10 — Final Policy

Do not let document convenience override document truth.  
Do not let stale memory become operational law.  
Update the repo so that the next session starts from truth, not drift.
