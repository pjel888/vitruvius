---
title: Vitruvius Standard Execution Loop (SEL)
version: 3.0
supersedes: 2.0
status: ACTIVE
owner: Vitruvius
last_updated: 2026-04-15
canonical_path: .ai/00_system/EXECUTION_LOOP.md
scope: All code, schema, plan, roadmap, decision, and canonical-document edits in the vitruvius repo.
---

# Vitruvius Standard Execution Loop (SEL) v3.0

## Purpose

Defines the mandatory workflow every engineering task MUST clear before any byte is written to this repository. The loop is **tailor-made for vitruvius** — it enforces the six-layer filesystem pipeline, the non-breaking feature-flag contract, the MCP-tool-first exploration rule, the append-only architectural decision ledger, and the sprint-closure protocol.

It exists because first answers are wrong often enough that the loop is cheaper than the rework. The audit pack in `.ai/02_audits/` and the 42-entry ledger in `.ai/10_state/decisions.md` are the receipts.

> **Authority.** If anything in this file conflicts with any *other* document in the repo, **this file wins for process** and `.ai/01_roadmap/master-roadmap.md` wins for *phase status*. The governing plan (`.ai/03_plans/00-governing-implementation-plan.md`) wins for *execution order*. Conflicts between those three documents are resolved via Phase 06 critique.

---

## 0. Project Context (non-negotiable)

Before doing anything, the executor MUST be able to answer these five questions correctly. If they cannot, return to `.ai/00_system/architecture.md` + `.ai/00_system/pipeline-overview.md` and read them.

1. **What is vitruvius?** A local-first, governance-first, domain-agnostic knowledge pipeline that converts professional-domain source corpora (currently PD 1096 Philippine building codes) into a validated, queryable knowledge graph via a six-layer filesystem architecture. It is **not** a RAG wrapper.
2. **What are the six layers?** `001_Raw-Source-Layer` (immutable input) → `002_Raw-Conversion-Layer` (machine-extracted text) → `003_Canonical-Knowledge-Layer` (trusted curated knowledge) → `004_Derived-Content-Layer` (generated learning content) → `005_Operational-Intelligence-Layer` (chunks, embeddings, graphs) → `006_System-Manifests` (registries, runs, snapshots).
3. **What language is the core?** Python. Rust crates live under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/` (pyo3 bridges). TypeScript lives **only** under `spatial-daemon/`. Bash is glue.
4. **Where do feature flags live?** Under `features:` in `config/vitruvius.yaml`, loaded by `scripts/vitruvius/features.py` into a frozen `Features` dataclass. **Every flag defaults `false`.** Exception list: `hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache`, `rust_mig_spatial_kernels`, `rust_mig_stats_kernels` (flipped to `true` per AD-029 / AD-038 after sprint exit gates cleared).
5. **How do I run the pipeline?** From repo root: `python3 scripts/pipeline_cli.py <subcommand>`. Subcommands are defined in `scripts/pipeline_cli.py::build_parser()`. The `run` composite stages are `scan → status → lint`; `run-with-review` additionally runs `convert → refine → review-relationships-ollama`. Idempotency is enforced via registry checks in `006_System-Manifests/registries/`.

---

## 1. Triggers & Scope

### 1.1 SEL is REQUIRED for any change touching

- Any file under `scripts/vitruvius/` (core pipeline modules)
- Any file under `scripts/vitruvius/engine_rs/`, `scripts/vitruvius/datalog_rs/` (Rust crates + pyo3 shims)
- Any file under `spatial-daemon/` (TypeScript sibling)
- Any entry point in `scripts/pipeline_cli.py` (new `subparsers.add_parser(...)` block or new `run_*` handler)
- `config/vitruvius.yaml` (adding flags, flipping defaults, changing Ollama pool, category list)
- `config/moe_routing.yaml` (Stream Y2 routing policy)
- `requirements.txt` (new pip dependencies — triggers the 8 GB M2 feasibility check)
- Any file under `003_Canonical-Knowledge-Layer/` that is **not** a curator-owned canonical markdown (schema, rules, shared/)
- Any file under `.ai/06_specs/` (schemas: `source-schema.md`, `concept-schema.md`, `relationship-schema.md`, `spatial-schema.md`)
- Any file under `scripts/vitruvius/rules/` (`canonical_rules.yaml`, stringency rules)
- Any file under `.ai/01_roadmap/` (`master-roadmap.md`, `current-phase.md`, `milestone-tracker.md`)
- Any file under `.ai/00_system/` (architecture, pipeline-overview, principles, naming-conventions, **this file**)
- Any file under `.ai/03_plans/` that is **not** an archived plan
- **Appending** to `.ai/10_state/decisions.md` (new AD-NNN). Editing existing AD entries is FORBIDDEN — they are append-only history.
- `.ai/10_state/known_issues.md` (the RI / risk-item ledger)
- `.ai/10_state/active_context.md` (session handoff document)

### 1.2 SEL is NOT required for

- Typo fixes in non-canonical docs (README scratch notes, chat exports, `chatGPT-Conversations/`)
- Dependency bumps with no API change AND a passing `pytest scripts/tests/` AND the MCP graph index is not invalidated
- Pure experiments under `.ai/07_experiments/` that the trigger file explicitly marks `will_not_merge: true`
- Adding files under `001_Raw-Source-Layer/` (new source PDFs). The pipeline treats raw as read-only but curators MAY add new files. The SEL is still required for the **ingestion run** that processes them.

A task is *non-trivial* by default. The burden of proof is on declaring something trivial, not the other way around. When in doubt, run the loop.

### 1.3 Identity-Locked Files — Tripwire

Any plan that proposes editing any of the files below triggers automatic **ESCALATE** unless the Phase 00 trigger file contains an explicit override block signed by Philip:

| File | Why it is locked |
|---|---|
| `.ai/00_system/principles.md` | Defines the 10 non-negotiable principles (P1–P10). Changes rewrite the contract. |
| `.ai/00_system/naming-conventions.md` | Defines the ID prefix / slug / timestamp format contract. Changes break graph lineage. |
| `.ai/00_system/EXECUTION_LOOP.md` (this file) | Changes rewrite the workflow itself. Meta-edit escalation. |
| `.ai/09_archive/plans/ingestion-refinement-contract.md` | Frozen per INDEX.md ❄️ (archived 2026-04-15). Interface between Phase 1B and Phase 1C. Version bumps only. |
| `.ai/03_plans/00-governing-implementation-plan.md` | Authoritative execution order. Only the STEWARD role may update it after a sprint closes. |
| `.ai/01_roadmap/master-roadmap.md` | v2.3.0 single source of truth for phase status. |
| `.ai/06_specs/source-schema.md` | Canonical source front-matter schema. |
| `.ai/06_specs/concept-schema.md` | Canonical concept front-matter schema. |
| `.ai/06_specs/relationship-schema.md` | Canonical relationship schema (7-predicate vocabulary). |
| `.ai/06_specs/spatial-schema.md` | Spatial contract schema (mirrors `spatial-daemon/`). |
| `scripts/vitruvius/constants.py` | Six-layer name constants. Renaming ANY of them breaks the filesystem contract. |
| `scripts/vitruvius/paths.py` | Filesystem contract (`ensure_*`, `build_*` helpers). |
| `scripts/vitruvius/features.py` | Frozen `Features` dataclass + `load_features()`. Changes the non-breaking flag contract. |
| `scripts/vitruvius/rules/canonical_rules.yaml` | Deterministic canonicalization rules (P5). Rule additions OK; rule deletions are an ESCALATE. |
| Any past `AD-NNN` entry in `.ai/10_state/decisions.md` | ADs are append-only. Use `Superseded by AD-MMM` — never delete or rewrite. |
| `001_Raw-Source-Layer/**` | Immutable per P2. Pipeline code MUST NOT write to this tree. |
| `scripts/vitruvius/spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts` | Paired implementation of the SHA-256 integrity-footer format per Sprint AUDIT-1 / AD-039. The two sides MUST stay in lockstep — edits to one without the other break cross-language contract verification. |

An override block looks like this in the Phase 00 trigger:

```yaml
identity_override:
  targets: [".ai/00_system/principles.md"]
  authorized_by: "Philip"
  authorized_at: "2026-04-15"
  reason: "Adding P11 (spatial integrity) after AUDIT-1 closure."
```

Without this block, the loop MUST halt and escalate before any edit is attempted.

---

## 2. Roles

The loop assumes role separation. One agent MAY play multiple roles, but adversarial phases (Phase 06) MUST be performed by a role separate from the one that produced the artifact under review.

| Role | Responsibility | Phases |
|---|---|---|
| **PLANNER** | Discovers, baselines, researches, audits, plans | 00–05 |
| **AUDITOR** | Adversarial review of the plan | 06 |
| **IMPLEMENTER** | Executes the checklist (typically the codebase agent with repo access) | 08 |
| **REVIEWER** | Validates outcomes against the plan | 09 |
| **STEWARD** | Closes the loop, writes the AD, archives superseded artifacts, updates INDEX.md and active_context.md | 10 |

Role assignment is recorded in the Phase 00 trigger file.

---

## 3. MCP & Graph Discipline (Mandatory Pre-Edit Protocol)

This project has **two** always-up-to-date knowledge graphs. Using them is not optional — `CLAUDE.md` and `AGENTS.md` both make this a hard requirement.

### 3.1 Before exploring unfamiliar code (Phases 01, 03)

- **Use `code-review-graph` first, Grep/Glob/Read second.** The graph (3509 nodes / 25575 edges / 433 files / python+rust+ts+bash) is faster, cheaper, and returns structural context Grep cannot.
- **Tools to prefer:** `semantic_search_nodes`, `query_graph` (callers_of / callees_of / imports_of / tests_for), `get_architecture_overview`, `list_communities`, `get_affected_flows`.
- **Fall back to Grep/Glob/Read only when the graph does not cover the question.**

### 3.2 Before editing any symbol (Phase 05 / 08)

- **Run `gitnexus_impact({target: "<symbol>", direction: "upstream"})` BEFORE the edit.** Report blast radius (direct callers, affected processes, risk level: LOW/MED/HIGH/CRITICAL) in the plan.
- **Run `gitnexus_context({name: "<symbol>"})` if you need the 360° view** (callers, callees, process participation).
- **Never rename symbols with find-and-replace.** Use `gitnexus_rename({symbol_name, new_name, dry_run: true})` first; review; then `dry_run: false`.
- **If impact returns HIGH or CRITICAL, the plan MUST surface this to Philip before execution.**

### 3.3 Before committing (Phase 09 / 10)

- **Run `gitnexus_detect_changes({scope: "staged"})`** to verify the change only affects expected symbols and execution flows.
- **Run `code-review-graph detect_changes`** for risk-scored diff analysis.
- If either returns unexpected scope, return to Phase 05 and re-plan.

### 3.4 Index freshness

- The `code-review-graph` index auto-updates on file changes via a hook.
- The `gitnexus` index drifts on commit. After any commit, run `npx gitnexus analyze` (with `--embeddings` if `.gitnexus/meta.json` shows `stats.embeddings > 0` — otherwise embeddings are destroyed).
- A PostToolUse hook handles this automatically after `git commit` and `git merge` for Claude Code users. Other agents MUST run it manually.

---

## 4. Artifact Index

Every SEL artifact opens with YAML frontmatter:

```yaml
---
task: {kebab-case task name}
phase: {00-10}
created: YYYY-MM-DD
author: {PLANNER | AUDITOR | IMPLEMENTER | REVIEWER | STEWARD}
supersedes: {prior artifact path or null}
status: {DRAFT | REVIEW | ACCEPTED | SUPERSEDED | CLOSED | ABORTED}
---
```

| Phase | Output | Canonical Path | Notes |
|---|---|---|---|
| 00 | Trigger | `.ai/04_tasks/{task}-trigger.md` | One per task. Never amend after ACCEPTED — create a revision block instead. |
| 01 | Discover note | Prepended to research pack | No separate file. Header `## 01 — Discover`. |
| 02 | Baseline | `.ai/10_state/baselines/{task}-baseline.md` | The `baselines/` subdirectory is created on first use (it does not currently exist — the STEWARD who runs the first Phase 02 creates it). |
| 03 | Research pack | `.ai/13_research/{task}-research.md` | The project already has three research files in this folder (ECS, AEC Ontology, Spatial Comprehension) — use the same frontmatter shape. |
| 04 | Audit | `.ai/02_audits/{task}-audit.md` | Existing audit files (`extraction-audit.md`, `ingestion-audit.md`, `review-layer-audit.md`, etc.) are the style template. |
| 05 | Plan | `.ai/03_plans/{task}-plan.md` OR `.ai/03_plans/YYYY-MM-DD-{task}-plan.md` for sprint plans | Register in `.ai/03_plans/INDEX.md`. |
| 06 | Critique | Appended to plan: `## Plan Critique` | Must carry `[C###]` IDs. |
| 07 | Checklist | Appended to plan: `## Execution Checklist` | Must reference `[G###]` or `[C###]` per step. |
| 08 | Implementation | Source code + dated comments | `# 2026-04-15: {what and why}` for non-trivial edits. |
| 09 | Validation | `.ai/05_logs/{task}-validation.md` | Currently only has a README; the first validation log creates the real convention. |
| 10 | Session delta | `.ai/05_logs/{task}-delta.md` + AD entry appended to `.ai/10_state/decisions.md` | The AD is the *canonical* delta. The log is the human-readable companion. |
| — | Deferred items | Appended to `.ai/10_state/known_issues.md` as a new RI (Risk Item) or carried in the trigger's `deferred:` block | **Do not create a `.ai/14_deferred/` directory.** Vitruvius uses `known_issues.md` for this. |
| — | Aborted tasks | Update trigger to `status: ABORTED` with an `abort_rationale:` block | **Do not create a `.ai/15_aborted/` directory.** |
| — | Superseded artifacts | `git mv` to `.ai/09_archive/plans/` or `.ai/09_archive/research/` with `supersededBy:` pointer added to frontmatter |

---

## Phase 00 — Trigger & Scope

**Objective.** Define the task in one sentence, draw the scope boundary, classify risk, check the identity-lock tripwire, and confirm the non-breaking flag contract.

**Requirements**

- One-sentence task statement (active verb, single deliverable)
- In-scope list (files, modules, behaviors) — each entry uses a real repo path
- Out-of-scope list (explicitly excluded)
- Identity-locked file check (PASS / TRIPWIRE — with override block if TRIPWIRE)
- Risk class:
  - **S** — single Python file under `scripts/vitruvius/`, reversible by `git revert`, no flag change
  - **M** — multi-file but same sprint surface (e.g. a new parser + its tests + one flag addition)
  - **L** — schema change, new CLI subcommand, new pip dependency, new `config/vitruvius.yaml` top-level key, new AD, new flag whose default might eventually flip
  - **XL** — breaks the non-breaking flag contract, modifies `001_Raw-Source-Layer/` write paths, adds an external database, renames a layer directory, edits an existing AD entry, touches identity-locked files
- Role assignments (PLANNER, AUDITOR, IMPLEMENTER, REVIEWER, STEWARD)
- Linked prior artifacts (if continuing earlier work)
- **MCP precheck:** which `code-review-graph` queries and `gitnexus_impact` calls the plan will need in Phase 03/05

**Gate.** No prior artifact for the same task name exists in `ACCEPTED` or `DRAFT` without an explicit supersede block.

**Output.** `.ai/04_tasks/{task}-trigger.md`

---

## Phase 01 — Discover

**Objective.** Read before write. Inventory what already exists on this surface.

**Requirements**

- **MCP graph sweep first** (not Grep). Use `semantic_search_nodes`, `query_graph`, `get_architecture_overview`, `get_affected_flows`. Write the queries and their results into the research pack.
- List existing entries in `.ai/01_roadmap/`, `.ai/06_specs/`, `.ai/10_state/`, `.ai/03_plans/` touching this surface.
- List superseded artifacts in `.ai/09_archive/plans/` and `.ai/09_archive/research/` that might still be referenced.
- Scan `.ai/10_state/decisions.md` for prior ADs on this surface (the file is 168 KB and append-only — use `grep -n "AD-[0-9]" .ai/10_state/decisions.md` via the Grep tool).
- Scan `.ai/10_state/known_issues.md` for open RIs that touch this surface.
- Check `.ai/03_plans/INDEX.md` for the plan status table — any 🔥 active sprint, 🔒 gated plan, or ❄️ frozen contract in-scope?
- Check `.ai/10_state/active_context.md` for the current session state.
- Note any relevant prompt in `.ai/08_prompts/` if this task dispatches to another agent.
- Note any relevant skill in `.ai/11_skills/` or agent in `.ai/12_agents/`.

**Gate.** If an `ACCEPTED` plan already covers this task, the loop halts and returns to Phase 00 for an explicit supersede decision. Duplicate plans are forbidden per Sprint PIPELINE-CLI drift findings.

**Output.** `## 01 — Discover` header prepended to the Phase 03 research pack.

---

## Phase 02 — Baseline

**Objective.** Capture the current state so any change has a defined origin and rollback target.

**Requirements**

- Current commit SHA: `git rev-parse HEAD`
- Current branch: `git branch --show-current`
- Current test-suite baseline: `pytest scripts/tests/ -q` (must be green before starting; record passing / skipped counts)
- Current spatial-daemon test baseline: `cd spatial-daemon && npm test` (if the change touches TS)
- Current Rust test baseline: `cd scripts/vitruvius/engine_rs && cargo test --workspace` (if the change touches Rust)
- Current feature-flag snapshot: which flags in `config/vitruvius.yaml` are `true` vs `false`. Reference the authoritative list under `features:`.
- Current GitNexus + code-review-graph index stats: `mcp__code-review-graph__list_graph_stats_tool` and `gitnexus_context({name: "<module>"})` for any entry symbol in scope.
- Current pipeline state snapshot: `python3 scripts/pipeline_cli.py status` (if the change touches scan/convert/canonicalize/review/promote stages).
- Relevant `.ai/10_state/bench_*.json` or `.ai/10_state/audit_*.json` artifacts that establish the number the new work must not regress.

**Gate.** Baseline MUST be reproducible — a reader must be able to check out the listed SHA, run the listed commands, and observe the described state.

**Output.** `.ai/10_state/baselines/{task}-baseline.md` (create the `baselines/` subdirectory on first use).

---

## Phase 03 — Research Pack

**Objective.** Establish full context. Make every assumption explicit and traceable.

**Requirements**

- Relevant code paths (file + line range, not just file name — e.g. `scripts/vitruvius/relationships_sections.py:240-290`)
- Related docs: architecture under `.ai/00_system/architecture.md`, pipeline walkthrough under `.ai/00_system/pipeline-overview.md`, principles under `.ai/00_system/principles.md`, naming contract under `.ai/00_system/naming-conventions.md`, roadmap under `.ai/01_roadmap/master-roadmap.md`, current phase under `.ai/01_roadmap/current-phase.md`, prior plans under `.ai/03_plans/` and `.ai/09_archive/plans/`
- Relevant AD references from `.ai/10_state/decisions.md` — quote the AD number and section
- External references (codes, RFCs, library docs, papers — with URLs and access dates). For PD 1096 / Philippine building code questions, cite the section number.
- Constraints:
  - **Local-first AI** (P8): no cloud LLM by default. Ollama at `http://127.0.0.1:11434`.
  - **8 GB M2 envelope**: the deployment target is a low-spec Apple Silicon machine. New pip dependencies that won't run there MUST be flagged.
  - **Filesystem-as-database** (P1): no new SQLite/Postgres/pickle for core lineage. Exception: Sprint HP.3-R already put a RocksDB KV store at the registry layer (AD-029); new DB choices must cite precedent and carry an AD.
  - **Non-breaking flag contract**: every new module's flag defaults `false` and the all-flags-off pipeline is byte-identical to the pre-flag baseline. Reference the test `scripts/tests/test_features.py::test_load_features_returns_all_defaults_false` (and the sibling `test_load_features_reads_explicit_true` for the flip case).
  - **Seven-predicate relationship vocabulary**: `governs`, `defines`, `requires`, `depends_on`, `limits`, `affects`, `supersedes`. Adding a predicate requires a schema version bump in `.ai/06_specs/relationship-schema.md` and an AD.
- Assumptions, each labeled `[A###]` with a verification path. Unverified assumptions get `⚠️ NEEDS INPUT`.

**Gate.** Every assumption has a stated verification path. No silent assumptions.

**Output.** `.ai/13_research/{task}-research.md`.

---

## Phase 04 — Audit

**Objective.** Compare current state (Phase 02) against intended outcome (Phase 00). Surface every gap, risk, and conflict.

**Requirements**

- Current implementation breakdown (file-by-file, function-by-function). Cite `gitnexus_context({name: "..."})` output for each entry symbol.
- Gaps, each labeled `[G###]` with location and intended end state
- Risks, each labeled `[R###]` with severity (LOW / MED / HIGH / BLOCKER) and mitigation. Surface the risk to the known_issues.md RI ledger if severity ≥ MED.
- Conflicts with the 10 core principles in `.ai/00_system/principles.md` (P1 filesystem-as-database, P2 raw immutability, P3 idempotency, P4 path-traceability, P5 deterministic canonicalization, P6 immutable canonical IDs, P7 explicit concept vocabulary, P8 local-first AI, P9 no soft output, P10 no schema-less growth)
- Conflicts with existing ADs (cite `AD-NNN`)
- Conflicts with the governing plan's execution order (`.ai/03_plans/00-governing-implementation-plan.md` §3)
- Conflicts with the naming contract (prefix format, slug format, timestamp format in `.ai/00_system/naming-conventions.md`)
- For any change touching `scripts/pipeline_cli.py`: reference AD-015 (lazy CLI imports) — new subcommands MUST keep their imports inside the `if args.command == ...` branch.
- For any change adding a Python→Rust port: reference AD-036 (Rust Line) — only port code that is NOT already a single numpy/C-backed primitive call. Pure orchestration belongs in Python.

**Gate.** Every `[G###]` MUST be addressed by a step in Phase 05 or explicitly deferred with rationale (which opens a new RI entry in `known_issues.md`).

**Output.** `.ai/02_audits/{task}-audit.md`.

---

## Phase 05 — Implementation Plan

**Objective.** Define exact steps for execution at file-and-function granularity. Follow the superpowers:writing-plans contract (bite-sized TDD, no placeholders, self-review at the end).

**Requirements**

- File-level changes, marked **NEW** or **EXTEND** (OVERWRITE is FORBIDDEN by default; overwrite requires an explicit override block). Use real repo paths.
- Function-level changes (signature, behavior, callers affected). Cite `gitnexus_impact({target: "<symbol>"})` output upstream and downstream.
- Dependency map:
  - Any new pip package goes in `requirements.txt` AND gets an `[A###]` assumption that the 8 GB M2 envelope can run it. Cite `.ai/10_state/feasibility_ml_deps_2026-04-15.json` precedent.
  - Any new Rust crate goes under `scripts/vitruvius/engine_rs/` as a workspace member OR as a new pyo3 sibling. Cite AD-036.
  - Any new TypeScript dep goes under `spatial-daemon/package.json`.
- **Feature flag contract.** If this plan adds new behavior, it adds a new flag to `config/vitruvius.yaml` under `features:` with a `false` default. Name it per the existing convention: `<stream_letter>_<module>` or `<sprint_prefix>_<module>`. Add a `test_features.py` assertion that the default is false. The all-flags-off pipeline MUST remain byte-identical.
- Order of execution (with reasons where order is non-obvious)
- Test requirements per step:
  - **Unit test** — goes in `scripts/tests/test_<module>.py` (the project has 215 test files as of 2026-04-15)
  - **Integration test** — reuses fixtures from `scripts/tests/fixtures/`
  - **Rust test** — `cargo test --package <crate>` for any engine_rs/datalog_rs change
  - **TS test** — `vitest` under `spatial-daemon/` for any TS change
  - **Bench** — if perf-sensitive, a harness under `scripts/vitruvius/bench/` writing its result to `.ai/10_state/bench_<name>_<date>.json`
- **Pipeline CLI test** — if a new subcommand lands, `test_cli_lazy_imports.py` must still pass (lazy import invariant from AD-015)
- Rollback procedure (per step and overall): prefer `git revert` per task commit; explicitly note any destructive ops.
- Dated comment plan (`# 2026-04-15: …` for non-trivial edits)
- `⚠️ NEEDS INPUT` flags wherever real information is missing — never fabricated
- If the plan is handed to a subagent, link the prompt under `.ai/08_prompts/{task}-prompt.md`

**Gate.** No `[G###]` unaccounted for. No file touched silently. No placeholders.

**Output.** `.ai/03_plans/{task}-plan.md` (or `.ai/03_plans/YYYY-MM-DD-{task}-plan.md` for sprint plans). Add a row to `.ai/03_plans/INDEX.md` under **Current Plans** with the status 📝 Queued.

---

## Phase 06 — Plan Critique (Adversarial)

**Objective.** Destroy the plan before execution does it for you.

**Performed by** AUDITOR role — MUST be a different agent (or a clearly separated planning pass). Self-critique by the PLANNER does not satisfy this phase.

**Requirements**

- Weak assumptions (cross-reference each `[A###]`)
- Edge cases the plan does not handle:
  - Empty `003_Canonical-Knowledge-Layer/shared/relationships/` (Sprint A first-run condition)
  - Ollama down or wrong model loaded (the Sprint Q / HP.3-R failure modes)
  - Idempotency: re-run behavior matches first-run behavior byte-for-byte (AD-012)
  - Resume: interrupted run resumes without duplicate work (Sprint R Y4 closed this gap at root via SQLite verdict cache)
  - Concurrent runs (the filesystem-as-database has no locks — most pipeline stages are single-writer; note any step that violates this)
  - Raw layer immutability (P2) — any code path that even *looks* like it could write into `001_Raw-Source-Layer/` is a BLOCKER
- Failure points (what breaks first under 8 GB M2 load, on a cold Ollama, on partial registry, on stale MCP index)
- Performance risks:
  - Wall-time regression vs the baseline recorded in Phase 02
  - Memory regression — RSS budget on the 8 GB M2 target
  - Rust Line violation (AD-036) — don't port numpy/BLAS calls; port only what is NOT already a C primitive
  - LSH-tax (AD-042) — any new LSH-style fuzzy path defaults to OFF until operator-run confirms real-corpus behavior
- Architectural violations:
  - Principle P1–P10 (cite the number)
  - AD conflicts (cite AD-NNN)
  - Governing plan sprint order
  - Naming contract (prefix/slug/timestamp)
  - Non-breaking flag contract (default-false + byte-identical)
- Scope creep risk (which steps are likely to balloon)
- Tests missing: every new public function, every new CLI branch, every new flag.
- Bench missing: any perf-sensitive path must have a harness and a committed artifact under `.ai/10_state/`.

Each finding receives `[C###]` and a disposition:

- **ACCEPT** — fold into plan (the plan is updated, Phase 05 re-runs for the touched steps, gate re-runs)
- **REJECT** — leave as-is, with recorded reasoning
- **DEFER** — open a new RI in `known_issues.md` and record the deferral in the plan

**Gate.** Zero findings without disposition. No `ACCEPT` finding left unfolded into the plan.

**Output.** Appended to plan file under `## Plan Critique`.

---

## Phase 07 — Execution Checklist

**Objective.** Convert the dispositioned plan into atomic, verifiable, reversible steps.

**Requirements**

- Each step has: pre-condition, action, post-condition, test (real command), rollback (real command)
- Each step references at least one `[G###]` or `[C###]` for traceability
- Each step is independently testable (runs a subset of `pytest scripts/tests/`)
- Each step is independently reversible (`git revert <step-commit-sha>`) — or explicitly marked irreversible with justification
- Steps ordered so any prefix of the checklist leaves the system in a working state (tests green at every commit)
- For multi-task sprints: each task is a commit. Commit message format: `<type>(<scope>): <summary>` where `<type>` is `feat`, `fix`, `refactor`, `docs`, `test`, `bench`, `chore` and `<scope>` matches the sprint prefix (e.g. `feat(relationships): Sprint LSH-1 Task 3 — …`)

**Gate.** A reader who has not read the plan can execute the checklist and produce the intended outcome.

**Output.** Appended to plan file under `## Execution Checklist`.

---

## Phase 08 — Implementation (Controlled)

**Performed by** IMPLEMENTER role.

### 8.1 Rules

- **Follow the checklist only.** No deviations without returning to Phase 05 for an update.
- **No silent changes.** Every non-trivial edit carries a dated comment: `# 2026-04-15: {what and why}`.
- **Run the step's test after each step.** Failing test halts execution and triggers re-entry to Phase 05.
- **Identity-locked files** (§1.3) remain off-limits absent the override block in Phase 00.
- **Scope guard:** any work outside the checklist halts and returns to Phase 05.
- **Extend, don't overwrite:** existing functions are extended, not replaced, unless the plan explicitly says **OVERWRITE** with rationale.
- **Pre-commit MCP check:** before every commit, run `mcp__code-review-graph__detect_changes_tool` (or `gitnexus_detect_changes({scope: "staged"})`). Unexpected scope halts the commit and returns to Phase 05.
- **No `--no-verify` on commits.** Hook failures are investigated, not bypassed.

### 8.2 Test discipline

- **Before the first task:** `pytest scripts/tests/ -q` → must match the Phase 02 baseline count.
- **After each task:** `pytest scripts/tests/ -q` → must be green and the pass count increases by the expected number.
- **After Rust changes:** `cd scripts/vitruvius/engine_rs && cargo test --workspace` or the datalog_rs equivalent.
- **After TS changes:** `cd spatial-daemon && npm test`.
- **After pipeline CLI changes:** `pytest scripts/tests/test_cli_lazy_imports.py` (AD-015 invariant) AND a smoke run of the new subcommand against a known-good fixture.
- **After flag-default flips (like AD-029, AD-038):** a byte-identity test MUST exist that compares the with-flag vs without-flag output on a committed fixture and they must match when the flag is off.

### 8.3 Commit cadence

- One commit per task per the writing-plans TDD rhythm (write failing test → implement → green → commit).
- Never batch multiple tasks in one commit.
- Never amend published commits. Create a new commit instead.
- Git user is already configured; do not edit `.git/config`.

---

## Phase 09 — Validation Report

**Performed by** REVIEWER role.

**Requirements**

- Test results, per checklist step (PASS / FAIL / SKIPPED with reason)
- Full-suite run: `pytest scripts/tests/ -q`, `cargo test --workspace` (if Rust touched), `npm test` (if TS touched) — record pass/skip counts
- Edge case validation (the cases identified in Phase 06)
- Performance notes:
  - Wall-time delta vs Phase 02 baseline
  - Memory delta (RSS) if the path is perf-sensitive on the 8 GB M2 target
  - Bench artifact under `.ai/10_state/bench_<name>_<date>.json` with the measured numbers
- Byte-identity check for flag-off path (the non-breaking contract)
- Regression checks against adjacent surfaces — use `code-review-graph get_affected_flows` to list impacted execution flows
- MCP index re-analyze: `npx gitnexus analyze` (with `--embeddings` if present) + `mcp__code-review-graph__build_or_update_graph_tool`
- Known limitations → becomes input to a future task's Phase 01 and may open a new RI

**Gate.** No FAIL or SKIPPED step without a follow-up artifact (RI entry, new task trigger, or recorded limitation).

**Output.** `.ai/05_logs/{task}-validation.md`.

---

## Phase 10 — Session Delta & Close

**Performed by** STEWARD role.

### 10.1 Sprint closure protocol (mandatory for any task that owns a sprint)

The STEWARD executes these steps in order. They are the closure contract enforced by every sprint from Sprint Q onward (see AD-024…AD-042 for the template):

1. **Verify all task commits are pushed.** `git log --oneline origin/main..HEAD` should be empty after push.
2. **Run the full test suite one last time.** `pytest scripts/tests/ -q`. Record the count.
3. **Write the AD entry.** Append a new `## AD-NNN — Sprint <NAME> closure — <one-line summary>` section to `.ai/10_state/decisions.md`. Use the AD-041 / AD-042 template:
    - Context (why the sprint existed, premise ADs it builds on)
    - Architectural choice (the one sentence that describes the shape of the solution)
    - Task ledger (table: Task / Description / Commit / Tests added)
    - Measurements (bench or audit results against the pre-committed exit gate)
    - Flag state (defaults stay false / flipped to true with rationale)
    - Sprint-wide perf call (Rust Line judgment per AD-036)
    - Commits (one-line-per-task ledger)
    - Test suite delta (X → Y, `+N net tests`)
    - Follow-ups (what was deferred and why)
4. **Archive the plan.** `git mv .ai/03_plans/<plan>.md .ai/09_archive/plans/<plan>.md`. Update the archived file's frontmatter to `status: complete` and add `archived: YYYY-MM-DD`.
5. **Update `.ai/03_plans/INDEX.md`.** The sprint row moves to the "Closed" state `✅ Complete (archived YYYY-MM-DD)` with the AD number quoted.
6. **Update `.ai/10_state/active_context.md`.** Bump the header "Updated:" line, add the sprint to the closure table, update the test count, update the "Next Phase Candidates" queue.
7. **Update `.ai/01_roadmap/current-phase.md`.** If the sprint was the current one, mark it closed and name the next sprint or write "None — between sprints".
8. **Tag the commit.** `git tag sprint-<kebab-case-name>-closed`.
9. **Push.** `git push origin main --tags` (only after Philip has consented to a push — see the "Executing actions with care" protocol in CLAUDE.md). Never push without explicit user consent.
10. **Update the session delta log.** `.ai/05_logs/{task}-delta.md` — path-level diff summary, docs updated, docs superseded, new RIs, handoff notes.

### 10.2 Non-sprint closure (single-task loop)

For loops that do not own a full sprint (a one-off bug fix, a single-file refactor), the STEWARD still executes steps 1, 2, 10, and optionally 3 (append a small AD if the decision is worth preserving). Skip the archive/tag/push steps for a task that did not warrant a sprint.

**Gate.** Trigger file (Phase 00) is updated to `status: CLOSED` with a link to the delta and validation. The `code-review-graph` and `gitnexus` indices are re-analyzed if the change touched symbols or files.

**Output.** `.ai/05_logs/{task}-delta.md` + appended `AD-NNN` in `.ai/10_state/decisions.md` + updated `INDEX.md` + updated `active_context.md`.

---

## 5. Failure Policy

Five outcomes are valid. Binary STOP/RETURN does not capture real failure modes.

| Outcome | Trigger | Action |
|---|---|---|
| **BLOCK** | Missing prerequisite phase | Return to that phase. Do not proceed. |
| **DEGRADE** | Step is harder than planned but task remains valuable at reduced scope | Document the scope reduction in the plan, re-run Phase 06 critique on the reduced plan, continue. Write an RI against `known_issues.md` for the deferred slice. |
| **DEFER** | Blocker is real but outside this task's scope | Open a new RI in `.ai/10_state/known_issues.md`, cite the trigger file, continue with what is unblocked. |
| **ESCALATE** | (a) Identity-locked file touched without override block, (b) raw layer write discovered, (c) non-breaking flag contract violated (a flag-off run diverges from baseline), (d) an existing AD would need to be rewritten, (e) schema change found mid-execution, (f) `gitnexus_impact` returns HIGH/CRITICAL without prior plan acknowledgement, (g) external dependency violating 8 GB M2 envelope discovered mid-execution | Halt. Surface to Philip with full context (trigger path, phase that caught it, proposed remediation). No further edits until Philip responds. |
| **ABORT** | Research or audit reveals the task should not be done | Update trigger to `status: ABORTED` with `abort_rationale:` block. No new directory needed. Optionally append a short AD under "AD-NNN — Sprint X ABORT rationale" if the decision is worth preserving. |

---

## 6. Re-entry Rules

When a phase is re-entered mid-loop, the loop does NOT restart from Phase 00. It restarts from the earliest invalidated phase:

- Implementation step fails on a logic bug → return to Phase 05 (re-plan), not Phase 03.
- Implementation step fails on a missing assumption → return to Phase 03 (re-research), then 04, then 05.
- Test suite regresses unexpectedly → return to Phase 04, add a `[G###]` for the regression, then replan.
- `gitnexus_impact` surfaces a HIGH callsite mid-execution → return to Phase 05, fold the callsite, re-run Phase 06 critique on the updated plan.
- Scope changes → return to Phase 00 (new trigger or amendment block with `revision: N`).
- Critique surfaces a missing risk → return to Phase 04, fold the gap, re-plan.
- Flag-off divergence discovered → escalate per §5.

Every re-entry adds a new `revision: N` entry to the affected artifact's frontmatter with a one-line note on what triggered the re-entry.

---

## 7. Vitruvius-Specific Invariants (Automatic Block Conditions)

These invariants are load-bearing for the entire repo. If any step of the loop would violate any of them, the loop MUST halt with BLOCK or ESCALATE.

### I1 — Non-breaking flag contract
With every flag in `config/vitruvius.yaml features:` set to its shipped default, the pipeline output MUST be byte-identical to the pre-plan baseline. Sprint Q, R, H, GEOM, PHYS, WIKI, GT, HP, Z, 1B-M1/M2/M3, PQ-1, and LSH-1 all honored this. Any new plan that *cannot* honor it is XL-risk and requires explicit Philip consent.

### I2 — Raw-layer immutability (P2)
No pipeline code writes to `001_Raw-Source-Layer/`. Ingestion commands accept input there but write outputs to `002_Raw-Conversion-Layer/`, `005_Operational-Intelligence-Layer/`, or `006_System-Manifests/`. Any proposed write handle inside an `001_*` code path is BLOCK.

### I3 — AD append-only
Past `AD-NNN` entries are history. A new decision gets `AD-(N+1)` and cites the prior AD via `Superseded by AD-XXX` or `Refines AD-YYY`. Editing an existing AD body is ESCALATE.

### I4 — Schema stability
`.ai/06_specs/` schemas version explicitly. Predicate additions to `relationship-schema.md` (currently the 7-predicate vocabulary: `governs`, `defines`, `requires`, `depends_on`, `limits`, `affects`, `supersedes`) require a schema bump AND an AD. Prefix additions to `naming-conventions.md` (currently `law`, `irr`, `concept`, `glossary`, `relationship`, `handout`, `reviewer`, `law-section`, `source`) follow the same rule.

### I5 — Lazy CLI imports (AD-015)
Every new `subparsers.add_parser(...)` handler in `scripts/pipeline_cli.py` imports its dependencies INSIDE the `if args.command == "..."` branch, never at module top. The test `test_cli_lazy_imports.py` enforces this. Violation = BLOCK.

### I6 — Rust Line (AD-036)
Port code to Rust only if the hot path is NOT already a single numpy/BLAS primitive call. Pure orchestration belongs in Python. Measurement-first: any Rust port must include a bench artifact clearing a ≥2× threshold on the measured kernel. Sprint PQ-1 and LSH-1 correctly DEFER_ALREADY_NATIVE this rule; RUST-MIG-1 S1/S2/N4 cleared it.

### I7 — Local-first AI (P8)
Review defaults to Ollama at `http://127.0.0.1:11434`. Cloud LLMs are opt-in only, never default. Any new LLM integration that would break the air-gap is XL-risk.

### I8 — Test baseline monotonic
`pytest scripts/tests/` pass count is monotonically non-decreasing across a commit. A plan that REDUCES the passing-test count without replacing the coverage is BLOCK. Sprint LSH-1 added +23 tests (1505 → 1528); Sprint PQ-1 added +11 (1494 → 1505). That is the expected shape.

### I9 — Registry single-writer
CSV registries under `006_System-Manifests/registries/` are single-writer per stage. Any plan introducing concurrent registry mutation requires a lock design + AD.

### I10 — Idempotency (P3, AD-012)
Every `run_*` handler in `scripts/vitruvius/` is re-runnable without duplicate writes. The Sprint A promotion governance module enforces strict byte-identical idempotency via the `skipped` action path. Any new handler that does not implement the equivalent check is BLOCK.

---

## 8. Enforcement Ladder

1. No direct coding without a Phase 05 plan.
2. No Phase 05 plan without a Phase 04 audit.
3. No Phase 04 audit without a Phase 03 research pack.
4. No Phase 03 research pack without a Phase 02 baseline.
5. No Phase 02 baseline without a Phase 01 discover sweep.
6. No Phase 01 discover without a Phase 00 trigger.
7. No Phase 08 execution without a Phase 06 critique by a separate AUDITOR role.
8. No Phase 08 execution without a Phase 07 checklist.
9. No Phase 10 close without a Phase 09 validation report.
10. No Phase 10 close without an `AD-NNN` entry if the task owns a sprint.
11. No edit to identity-locked files (§1.3) without an override block in the Phase 00 trigger.
12. No MCP-free exploration of unfamiliar code (§3.1).
13. No edit without `gitnexus_impact` on the edited symbol (§3.2).
14. No commit without `detect_changes` scope verification (§3.3).
15. No sprint closure without the 10-step protocol in §10.1.
16. No git push without explicit Philip consent (CLAUDE.md "Executing actions with care").

If any rung is incomplete: STOP → return to the earliest invalidated phase per §6.

---

## 9. Quick Reference — Real Commands

```bash
# Repo-root commands (run from /Users/philiplewis/vitruvius)

# Full Python test suite
pytest scripts/tests/ -q

# One test file
pytest scripts/tests/test_lsh_dedup.py -v

# Spatial daemon (TypeScript)
cd spatial-daemon && npm test

# Rust workspace tests
cd scripts/vitruvius/engine_rs && cargo test --workspace
cd scripts/vitruvius/datalog_rs && cargo test

# Pipeline stages (see scripts/pipeline_cli.py build_parser)
python3 scripts/pipeline_cli.py scan
python3 scripts/pipeline_cli.py status
python3 scripts/pipeline_cli.py lint
python3 scripts/pipeline_cli.py convert
python3 scripts/pipeline_cli.py canonicalize
python3 scripts/pipeline_cli.py extract-relationships-sections-one <relative_md_path>
python3 scripts/pipeline_cli.py review-relationships-ollama --model gemma4:31b
python3 scripts/pipeline_cli.py promote --execute
python3 scripts/pipeline_cli.py build-graph
python3 scripts/pipeline_cli.py ple-kv-migrate --store event --source <path> --dest <path>

# MCP index refresh (after any commit that changes symbols)
npx gitnexus analyze
# If embeddings exist:
npx gitnexus analyze --embeddings

# Inspect index freshness
cat .gitnexus/meta.json
```

---

## 10. Principle

> Do not trust the first answer. Trust only what survives the loop.
> Do not trust your memory of the codebase. Trust only what the graph and the tests currently say.
> When the loop survives, write the AD. Without the AD, it didn't happen.

---

## Changelog

- **3.0 (2026-04-15)** — Complete rewrite targeting the vitruvius repo. Replaced all SlateCamp / Next.js / Tailwind / Android references with real vitruvius stack (Python + Rust + TypeScript + Bash, six-layer filesystem pipeline). Replaced placeholder identity-locked components with the real locked file list (principles, naming contract, schemas, constants, paths, features, canonical rules, raw layer, spatial-daemon contracts, past ADs). Added §0 Project Context precheck. Added §3 MCP & Graph Discipline with mandatory `code-review-graph` + `gitnexus` usage (enforced by CLAUDE.md + AGENTS.md). Added §7 Vitruvius-Specific Invariants (I1–I10) covering non-breaking flag contract, raw-layer immutability, AD append-only, schema stability, lazy CLI imports (AD-015), Rust Line (AD-036), local-first AI (P8), test baseline monotonic, registry single-writer, idempotency (AD-012). Added §10.1 10-step Sprint closure protocol codifying the pattern from AD-024 through AD-042. Replaced non-existent `.ai/14_deferred/` and `.ai/15_aborted/` with real fixtures: `known_issues.md` RI ledger + trigger `status: ABORTED`. Added §9 Quick Reference with real pytest / cargo / pipeline_cli / MCP commands. Every path in this document maps to a real location in the current working tree as of commit `29268512c8ea`.
- **2.0 (2026-04-15, superseded same day)** — Added Phase 00/01/02/10, roles, failure policy, re-entry rules, traceability IDs. Used a SlateCamp Next.js template by mistake — references to `/app`, `/components`, `SlideToSubmit.tsx`, Tailwind, mobile/4G, RLS did not match the vitruvius repo and made the loop unenforceable. Replaced by v3.0.
- **1.0** — Original seven-phase loop. Superseded.
