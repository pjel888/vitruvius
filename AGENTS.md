<!-- Generated: 2026-04-13 | Upgraded and merged: 2026-04-15 -->

# Vitruvius Root — AGENTS.md

## Purpose
Vitruvius is a local-first, multi-layered knowledge and computational system. It processes raw and structured inputs through deterministic pipelines, canonicalization, review, and downstream computation to produce machine-readable, auditable, and verifiable outputs.

This file is the **root operating contract for all AI agents** working in this repository, including Codex, Claude Code, Gemini CLI, and any future codebase agents.

It defines:
- how agents must work
- what documents are authoritative
- what tools must be used first
- what cannot be violated
- when to stop
- what counts as complete

This file is not a casual guide. It is the root contract.

---

# SECTION 01 — AUTHORITY ORDER (MANDATORY)

All agents MUST follow this precedence order when making decisions:

1. `AGENTS.md` — root operating contract
2. `.ai/00_system/EXECUTION_LOOP.md` — mandatory lifecycle protocol for non-trivial work
3. `.ai/00_system/principles.md` — non-negotiable architectural law
4. `.ai/01_roadmap/master-roadmap.md` — authoritative roadmap, priorities, phase status, and gates
5. `.ai/01_roadmap/current-phase.md` — active execution state
6. `.ai/01_roadmap/milestone-tracker.md` — completion truth
7. `.ai/10_state/decisions.md` and related state ledgers — architecture memory and decision continuity
8. `.ai/02_audits/` — audited reality checks
9. `.ai/03_plans/` — implementation intent and execution plans
10. Codebase itself
11. README and supporting docs

If any of the above conflict:
- STOP
- surface the conflict explicitly
- do not guess
- do not silently choose one interpretation

---

# SECTION 02 — MANDATORY EXECUTION LOOP

For all non-trivial work, agents MUST follow the Standard Execution Loop:

1. Research Pack
2. Audit Document
3. Implementation Plan
4. Plan Critique
5. Execution Checklist
6. Controlled Implementation
7. Validation Report

## Non-Negotiable Rules
- No coding without a plan
- No plan without an audit
- No audit without research
- No execution without critique
- No completion without validation
- No major change without state reconciliation

If any required phase is missing:
- STOP
- create or update the missing artifact first

## Trivial Work Exception
The full loop may be shortened only when ALL of the following are true:
- the task is isolated
- there is no architecture impact
- there is no data-model impact
- there is no performance implication
- there is no Rust impact
- there is no truth-governance implication
- the blast radius is demonstrably low

If there is doubt, treat the task as non-trivial.

---

# SECTION 03 — STATE-FIRST WORKFLOW

Before any implementation, agents MUST:
- read `current-phase.md`
- read `milestone-tracker.md`
- confirm alignment with `master-roadmap.md`
- check relevant audits and plans
- determine whether the task is active, deferred, blocked, or gated

After implementation, agents MUST:
- update the relevant plan status
- write or update the validation report
- update state files if execution status changed
- update decision logs if an architectural decision was made
- ensure milestone and current-phase files remain truthful

State drift is a failure condition.

---

# SECTION 04 — WORKING IN THIS DIRECTORY

## Key Files
| File | Description |
|------|-------------|
| `README.md` | Full project documentation |
| `AGENTS.md` | This file — root AI agent guidance and operating contract |
| `CLAUDE.md` | Claude Code-specific instructions |
| `GEMINI.md` | Gemini CLI instructions |
| `config/vitruvius.yaml` | Project configuration |
| `init_vitruvius_structure.sh` | Directory structure initialization script |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `scripts/` | Python pipeline CLI and core package (see `scripts/AGENTS.md`) |
| `config/` | Configuration files (see `config/AGENTS.md`) |
| `docs/` | Documentation files (see `docs/AGENTS.md`) |
| `001_Raw-Source-Layer/` | Original source documents (PDFs, scans) |
| `002_Raw-Conversion-Layer/` | Machine-extracted text outputs |
| `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge pages |
| `004_Derived-Content-Layer/` | Generated downstream content |
| `005_Operational-Intelligence-Layer/` | Machine infrastructure (chunks, embeddings, graphs) |
| `006_System-Manifests/` | Pipeline control, audit logs, registries |
| `.ai/` | Operating system for research, audits, plans, state, and agent governance |

## Common Patterns
- All pipeline modules are in `scripts/vitruvius/`
- Use the six-layer architecture consistently
- All outputs and operational reports must remain auditable
- Content trust order for knowledge work is Canonical > Raw Conversion > Raw Source
- Deterministic and traceable outputs are preferred over convenient but opaque outputs

---

# SECTION 05 — REQUIRED EXPLORATION TOOLS FIRST

## Global Rule
ALWAYS use code-review-graph MCP tools and GitNexus tools before using Grep, Glob, Read, or manual file scanning to explore the codebase, unless the graph tooling clearly does not cover the required question.

These tools are faster, cheaper in tokens, and provide structural relationships that manual scanning cannot.

---

## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper, and gives
structural context such as callers, dependents, and test coverage that file
scanning cannot.

### When to use graph tools FIRST
- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of, callees_of, imports_of, tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep, Glob, or Read only when the graph does not cover the need.

### Key Tools
| Tool | Use when |
|------|----------|
| `detect_changes` | Reviewing code changes and risk-scored analysis |
| `get_review_context` | Need source snippets for review, token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow
1. The graph auto-updates on file changes via hooks.
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern=`tests_for` to check coverage.

---

## GitNexus — Code Intelligence

This project is indexed by GitNexus as **vitruvius**. Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

### Always Do
- MUST run impact analysis before editing any symbol
- Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})`
- Report the blast radius when relevant to the task
- MUST run `gitnexus_detect_changes()` before committing or finalizing code changes
- MUST warn explicitly if impact analysis returns HIGH or CRITICAL risk before proceeding
- Use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping when exploring unfamiliar code
- Use `gitnexus_context({name: "symbolName"})` for full context on callers, callees, and process participation

### When Debugging
1. `gitnexus_query({query: "<error or symptom>"})`
2. `gitnexus_context({name: "<suspect function>"})`
3. Read `gitnexus://repo/vitruvius/process/{processName}`
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})`

### When Refactoring
- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first
- **Extracting/Splitting**: MUST run `gitnexus_context` and `gitnexus_impact` before moving code
- After any refactor: run `gitnexus_detect_changes({scope: "all"})`

### Never Do
- NEVER edit a function, class, or method without first running `gitnexus_impact`
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis
- NEVER rename symbols with find-and-replace
- NEVER finalize changes without running `gitnexus_detect_changes()`

### Tools Quick Reference
| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

### Impact Risk Levels
| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

### Resources
| Resource | Use for |
|----------|---------|
| `gitnexus://repo/vitruvius/context` | Codebase overview, check index freshness |
| `gitnexus://repo/vitruvius/clusters` | All functional areas |
| `gitnexus://repo/vitruvius/processes` | All execution flows |
| `gitnexus://repo/vitruvius/process/{name}` | Step-by-step execution trace |

### Self-Check Before Finishing
Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH or CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 dependents were updated

### Keeping the Index Fresh
After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count.

---

# SECTION 06 — IMPLEMENTATION RULES

## General Rules
- Prefer the smallest safe change that satisfies the task
- Preserve architecture boundaries
- Do not broaden scope silently
- Do not “improve” unrelated code during a scoped task
- Do not mark work complete based on confidence alone

## Documentation Rules
For non-trivial work:
- docs and state must be read before coding
- docs and state must be updated after coding when reality changes
- implementation must be traceable to research, audit, and plan artifacts

## Truthfulness Rule
If uncertain:
- say exactly what is uncertain
- say why it is uncertain
- say what evidence would resolve it

Never fabricate certainty.

---

# SECTION 07 — RUST OPERATING RULES

If a task touches Rust in any meaningful way, agents MUST read the Rust governance documents before writing Rust code.

Minimum required Rust documents:
- Rust Operating Contract
- Rust Kernel Development Protocol
- Rust Safeguards and Failure Containment
- Rust Architecture and Boundary Rules
- Rust Testing, Benchmarking, and Validation
- Rust Code Review Checklist
- Rust Style and Implementation Rules

## Rust Philosophy
Rust is a hardened compute zone.

Rust exists for:
- deterministic computation
- geometry kernels
- ECS systems
- spatial indexing
- numerical routines
- Wasm-compatible compute modules
- PyO3-exposed compute primitives where justified

Rust does NOT exist for:
- orchestration
- legal or policy interpretation
- AI prompt logic
- knowledge-truth governance
- casual feature experimentation

## Rust Mandatory Rules
- define data contract before code
- define numeric type policy before code
- define edge cases before code
- define tolerance policy before code
- implement reference version before optimization when appropriate
- test before optimization
- benchmark before claiming performance
- avoid `unsafe` unless explicitly justified and reviewed
- stop if architecture boundaries blur

---

# SECTION 08 — STOP CONDITIONS (CRITICAL)

Agents MUST stop and surface the issue if:
- authoritative docs conflict
- architecture intent is unclear
- current state is stale or contradictory
- task scope is unclear
- impact analysis is HIGH or CRITICAL and unresolved
- Rust data contract is undefined
- coordinate frame or units are undefined
- tolerance policy is undefined
- benchmark target is undefined for hot-path Rust
- a required audit or plan does not exist
- the requested change would violate principles or roadmap gates

Never guess through a stop condition.

---

# SECTION 09 — VALIDATION AND DONE CRITERIA

Work is NOT complete unless the following are true where applicable:
- impacted tests pass
- validation report exists for non-trivial work
- benchmarks were run for hot-path or performance-sensitive changes
- impacted docs were updated
- impacted state files were updated
- blast radius was checked
- scope of change matches expected change
- known caveats are explicitly recorded

## Minimum Honest Completion Standard
A task can only be called complete if:
- the implemented change matches the approved plan or justified deviation
- the code compiles or runs as expected
- validation artifacts exist
- no unresolved critical risk is being hidden

---

# SECTION 10 — PIPELINE COMMANDS

```bash
# Full pipeline
python scripts/pipeline_cli.py run

# Convert PDFs
python scripts/pipeline_cli.py convert

# Detect PDF type
python scripts/pipeline_cli.py detect-one "path/to/file.pdf"

# Run OCR
python scripts/pipeline_cli.py ocr-execute
```

## Testing Requirements
- Test any pipeline modification with the relevant targeted tests
- At minimum, historically relevant examples include `test_pdf_text_detection.py` and `test_odl_one.py` where applicable
- Verify reports are written correctly to `006_System-Manifests/runs/`
- Prefer focused tests first, then broader suite as needed by risk and blast radius

---

# SECTION 11 — DEPENDENCIES

## External
- `pypdf` — PDF text extraction for detection
- `opendataloader-pdf` — PDF-to-Markdown conversion
- `ocrmypdf` — OCR processing for scanned PDFs
- `PyYAML` — Configuration file parsing

## Internal
- `scripts/vitruvius/` — core pipeline modules
- six data layers for the knowledge lifecycle
- `.ai/` operating documents for governance, planning, state, and execution control

---

# SECTION 12 — DATA LAYERS OVERVIEW

| Layer | Folder | Purpose |
|-------|--------|---------|
| 1 | `001_Raw-Source-Layer/` | Original source documents (git-ignored) |
| 2 | `002_Raw-Conversion-Layer/` | Machine-extracted text (Markdown, JSON, OCR PDFs) |
| 3 | `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge |
| 4 | `004_Derived-Content-Layer/` | Generated downstream content |
| 5 | `005_Operational-Intelligence-Layer/` | Chunks, embeddings, graphs |
| 6 | `006_System-Manifests/` | Pipeline control, audit, logs, registries |

## Content Trust Order
Canonical > Raw Conversion > Raw Source

Raw materials are evidence.
Canonical materials are the trusted working layer.
Derived materials are downstream artifacts and must not silently redefine truth.

---

# SECTION 13 — ACTIVE SPRINT / CURRENT STATE REFERENCE

Agents must not rely on this file alone for live execution state.

Before acting on any sprint, phase, or active work:
- read `.ai/01_roadmap/current-phase.md`
- read `.ai/01_roadmap/milestone-tracker.md`
- confirm against `.ai/01_roadmap/master-roadmap.md`

If this root file contains stale sprint context and the state files disagree, the state files win.

## Historical Context
This repository has used active sprint blocks here for operator convenience. Treat them as informational only unless confirmed by current state files.

If you are a subagent opening this repo fresh, read the governing implementation plan and the current state documents before choosing a task.

---

# SECTION 14 — PRINCIPLES TO KEEP IN MIND

- Do not trust first outputs
- Truth is admitted, not generated
- All work must be traceable
- All outputs must be verifiable
- Determinism over convenience
- Validation over speed
- Small safe changes over broad speculative changes
- State must reflect reality
- If impact is unclear, stop and inspect
- If correctness is not proven, it is not done

---

# SECTION 15 — CLI / SKILLS REFERENCES

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

---

# SECTION 16 — FINAL RULE

If unsure:
- STOP
- explain the uncertainty clearly
- identify the missing authority, missing evidence, or missing state
- resolve that first

Never fabricate certainty.
Never skip the loop on serious work.
Never let implementation outrun truth.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **vitruvius** (6722 symbols, 16559 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/vitruvius/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/vitruvius/context` | Codebase overview, check index freshness |
| `gitnexus://repo/vitruvius/clusters` | All functional areas |
| `gitnexus://repo/vitruvius/processes` | All execution flows |
| `gitnexus://repo/vitruvius/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
