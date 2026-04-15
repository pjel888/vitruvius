---
task: nested-agents-governance
phase: 05
created: 2026-04-15
last_updated: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Plan — Nested AGENTS Governance

## 1. Scope Boundary
This plan governs the hierarchical `AGENTS.md` system only.

It does not:
- rewrite runtime architecture
- reopen archived sprint work
- replace root law with local law
- create `AGENTS.md` files in every leaf directory

## 2. Why This Plan Is Still Live
The repo still does not have the full justified AGENTS hierarchy this plan targeted.

Current relevant coverage:
- `AGENTS.md`
- `config/AGENTS.md`
- `docs/AGENTS.md`
- `scripts/AGENTS.md`
- `scripts/vitruvius/AGENTS.md`
- `scripts/vitruvius/rules/AGENTS.md`
- `006_System-Manifests/AGENTS.md`

Still missing from the originally justified hierarchy:
- `.ai/AGENTS.md`
- `scripts/tests/AGENTS.md`
- `scripts/vitruvius/engine_rs/AGENTS.md`
- `scripts/vitruvius/datalog_rs/AGENTS.md`
- `spatial-daemon/AGENTS.md`
- `003_Canonical-Knowledge-Layer/AGENTS.md`
- `005_Operational-Intelligence-Layer/AGENTS.md`

The plan therefore remains relevant as a pending governance-maintenance item.

## 3. Target Files

### Create
- `.ai/AGENTS.md`
- `scripts/tests/AGENTS.md`
- `scripts/vitruvius/engine_rs/AGENTS.md`
- `scripts/vitruvius/datalog_rs/AGENTS.md`
- `spatial-daemon/AGENTS.md`
- `003_Canonical-Knowledge-Layer/AGENTS.md`
- `005_Operational-Intelligence-Layer/AGENTS.md`

### Update
- `AGENTS.md`
- `scripts/AGENTS.md`
- `scripts/vitruvius/AGENTS.md`
- `scripts/vitruvius/rules/AGENTS.md`
- `config/AGENTS.md`
- `docs/AGENTS.md`
- `006_System-Manifests/AGENTS.md`

## 4. Repo-Specific Justification By Directory

### Root `AGENTS.md`
- remains the governing root contract
- must be truthful about live state-file paths
- must point downward only where a local contract materially changes behavior

### `.ai/`
- owns plans, audits, state, specs, prompts, and archive memory
- requires a local contract because this subtree is governance memory, not product code
- must explicitly forbid treating archived or stale docs as live authority

### `scripts/`
- owns the CLI spine and Python package root
- needs a local contract because lazy-import discipline and orchestration boundaries live here

### `scripts/vitruvius/`
- owns Python orchestration and multiple subsystem boundaries
- needs a strong local contract because it sits at the Python/Rust/TypeScript seam

### `scripts/tests/`
- test behavior differs materially from production code behavior
- needs rules around fixture ownership, determinism, feature-flag coverage, and regression expectations

### `scripts/vitruvius/rules/`
- truth-critical registry and rule files live here
- needs strict admission/change rules and validation expectations

### Rust crate roots
- `scripts/vitruvius/engine_rs/`
- `scripts/vitruvius/datalog_rs/`
- both require local contracts that explicitly point to the RUST pack and forbid policy creep

### `spatial-daemon/`
- owns the strongest TypeScript ↔ Python contract in the repo
- needs a local contract because integrity-footer parity and file-contract discipline are easy to break casually

### `003_Canonical-Knowledge-Layer/`
- this is trusted canonical truth storage
- needs a local contract because accidental edits here have truth-governance impact

### `005_Operational-Intelligence-Layer/`
- holds graph snapshots, embeddings, and derivative machine artifacts
- needs a local contract because it is easy to confuse derivative infrastructure with canonical truth

## 5. Content Model For Each Local AGENTS File
Each local file must contain only local additions to root law:
- directory purpose
- what belongs there
- what does not belong there
- local boundaries
- relevant commands or validations
- caution areas
- inheritance statement pointing back to the parent/root contract

Each local file must not:
- restate full authority order
- restate the full execution loop
- become a generic coding-style essay
- weaken root stop conditions

## 6. Required Local Rules By High-Risk Boundary

### Rust Roots
Must explicitly state:
- Rust is a hardened compute zone
- relevant RUST pack docs are mandatory
- no legal, pricing, or orchestration logic belongs there
- benchmarks are required before performance claims

### TypeScript Spatial Boundary
Must explicitly state:
- ownership is limited to spatial translation/contract emission
- Python reads files; there is no live daemon authority
- contract footer parity with `scripts/vitruvius/spatial/contract_reader.py` is mandatory

### Canonical Layer
Must explicitly state:
- canonical truth is admitted, not casually edited
- generated downstream artifacts must not overwrite canonical truth
- provenance and schema rules are mandatory

### `.ai/`
Must explicitly state:
- this subtree is repo memory, not runtime code
- archived documents do not become active by proximity
- state drift must be repaired rather than silently worked around

## 7. Implementation Sequence
1. repair root truthfulness issues that would undermine the hierarchy
2. upgrade existing nested `AGENTS.md` files
3. create the missing high-risk local contracts
4. run coverage and stale-path scans
5. write validation report with intentional skips and remaining risks

## 8. Validation Plan
- structural scan of all repo-relevant `AGENTS.md` files
- stale-path scan for known wrong state references
- duplicate-risk scan so local files do not repeat root law excessively
- directory coverage review against the justified target list
- `git diff --stat` and file-by-file governance review

## 9. Plan Critique

### Over-Documentation Risk
- adding files below `scripts/vitruvius/graph/`, `review/`, `query/`, `parsers/`, or `normalization/` would create maintenance clutter
- adding files to raw or derived data layers would mostly repeat root law

### Under-Documentation Risk
- leaving `.ai/`, Rust roots, `spatial-daemon/`, or `scripts/tests/` uncovered leaves the highest-risk boundaries governed only by generic parent text

### Duplication Risk
- root law already defines authority order, execution loop, and stop conditions
- local files must only add local consequences and commands

### Drift Risk
- `.ai/` and `docs/` are the most likely to drift because they summarize other artifacts
- root `AGENTS.md` can drift again if state-file paths move and nested plans are not reconciled

### Tempting But Harmful Targets To Skip
- `001_Raw-Source-Layer/`
- `002_Raw-Conversion-Layer/`
- `004_Derived-Content-Layer/`
- deep `scripts/vitruvius/*` leaves with no stable independent operating identity

## 10. Refined Plan
Keep the AGENTS hierarchy shallow, strict, and boundary-driven:
- root law at the top
- major runtime/governance boundaries only
- no leaf-spam
- no generic filler

## 11. Execution Checklist
- [ ] patch root `AGENTS.md` only where truthfulness or hierarchy references require it
- [ ] upgrade the six existing nested `AGENTS.md` files
- [ ] create the seven missing justified nested `AGENTS.md` files
- [ ] avoid generated directories, caches, vendored paths, `node_modules`, and `target/`
- [ ] run stale-path and coverage scans
- [ ] write validation report with created, updated, skipped, and remaining-gap directories
