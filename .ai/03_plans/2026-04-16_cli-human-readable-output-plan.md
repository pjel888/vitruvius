---
task: cli-operator-output-upgrade
phase: "05"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: DRAFT
---

# CLI Human-Readable Output Upgrade Plan — 2026-04-16

## Objective
Upgrade the Vitruvius CLI into a dual-layer operator interface so major commands explain themselves in human and technical terms, while preserving concise/script-safe behavior for automation-sensitive paths.

## In scope
- `scripts/pipeline_cli.py`
- a new shared CLI presentation helper module under `scripts/vitruvius/`
- help text for major CLI commands
- pre-run explanation blocks for major human-facing commands
- post-run success/failure/next-step interpretation blocks for those commands
- tests covering help enrichment and operator-mode wrapping behavior

## Out of scope
- rewriting every command handler's internal print statements
- changing pipeline semantics, exit codes, or file formats
- modifying JSON payload shapes produced by graph/query/spatial surfaces
- broad logging framework replacement

## Implementation strategy
### 1. Add a centralized command metadata registry
Create a lightweight helper module that stores per-command metadata:
- short help text
- human explanation
- technical explanation
- success meaning
- failure meaning
- suggested next step
- whether operator wrapping is safe by default

### 2. Add shared parser helpers
Refactor `build_parser()` to use a shared helper for `add_parser(...)` so major commands gain:
- consistent short help in top-level `--help`
- long-form subcommand descriptions
- epilog guidance for success/failure/next-step interpretation
- consistent `RawDescriptionHelpFormatter`

### 3. Add output-mode routing
Add a global CLI flag such as:
- `--output-mode {auto,operator,concise}`

Default behavior:
- `auto`: operator framing for human-facing commands on interactive terminals; concise elsewhere
- `operator`: always show operator framing when the command is marked safe for prose wrapping
- `concise`: never show framing blocks

### 4. Add a shared execution wrapper
Wrap command execution centrally in `main()` so operator-safe commands receive:
- a calm pre-run explanation block
- the existing live handler output
- a post-run interpretation block keyed to exit code

### 5. Preserve structured-output commands
Mark JSON/structured-output commands as concise-by-default so their stdout remains machine-usable:
- `build-graph`
- `query-graph`
- `export-graph-snapshot`
- `evaluate-spatial`
- other specialist surfaces where prose wrapping would be risky

### 6. Validate with targeted tests + real command runs
Automated validation should cover:
- improved `--help`
- operator wrapper rendering
- auto/concise mode preservation
- no lazy-import regressions

Manual validation should cover:
- top-level help
- `refine --help`
- `enrich-concepts --help`
- at least one real operator-mode command execution on a safe command

## Plan Critique
### C001 — duplication risk
If help text and runtime explanations are maintained in separate places, they will drift.
- **Mitigation:** one metadata registry powers both help output and runtime framing.

### C002 — too-much-output risk
If explanatory prose is always-on, operators will tune it out.
- **Mitigation:** default to `auto`; operator blocks only on interactive terminals for operator-safe commands.

### C003 — automation/script breakage risk
Some commands are already parsed by tests and likely by scripts.
- **Mitigation:** structured-output commands stay concise by default and never get wrapped in `auto` mode.

### C004 — inconsistent command coverage risk
If only a few commands are documented, the CLI will feel uneven.
- **Mitigation:** cover all major operator commands in the metadata registry during this pass; allow terse metadata for niche utilities.

### C005 — lazy import regression risk
A presentation helper that imports heavy modules at top level would violate an existing CLI contract.
- **Mitigation:** the helper module must use stdlib only.

## Execution Checklist
- [ ] G001 — Create shared CLI presentation helper module with metadata registry and renderer
- [ ] G002 — Refactor `build_parser()` to use centralized metadata for major commands
- [ ] G003 — Add global output mode flag and central run wrapper in `main()`
- [ ] G004 — Keep structured-output commands concise by default
- [ ] G005 — Add/adjust tests for help enrichment and operator-mode wrapping
- [ ] G006 — Run targeted pytest coverage for CLI behavior and lazy imports
- [ ] G007 — Manually run representative commands and capture validation notes

## Expected result
After implementation, Vitruvius CLI users should be able to see:
- what a command is for
- what it touches technically
- how to interpret success and failure
- what usually comes next

without turning automation-oriented command surfaces into noisy prose streams.
