## Task Statement
Audit the whole Vitruvius codebase, then upgrade every active planning document under `.ai/03_plans/` so each plan is detailed, comprehensive, and grounded in the actual repository.

## Desired Outcome
- A codebase-wide audit artifact that maps real implementation surfaces, risks, and plan drift
- Updated active plans in `.ai/03_plans/` with stronger codebase context, dependencies, execution detail, and validation burden
- A validation report confirming the upgraded plan set is internally consistent and relevant to the live repo

## Known Facts / Evidence
- `npx gitnexus status` reports the GitNexus index is up to date at commit `027e457`.
- The repo is no longer just a simple document pipeline: it includes Python core modules, Rust crates under `scripts/vitruvius/engine_rs` and `scripts/vitruvius/datalog_rs`, and a TypeScript sibling project under `spatial-daemon/`.
- Active planning documents in `.ai/03_plans/` include the governing plan, nested AGENTS governance plan, and a full AEC engine plan set.
- Large live modules include `ollama_review.py`, `conversion.py`, graph/compound/geometric/spatial/query/wiki packages, and a wide test surface under `scripts/tests/`.
- `AGENTS.md` still points to `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`, but the live state files are under `.ai/01_roadmap/`.
- `current-phase.md` says the project is between sprints; the repo has substantial shipped capability beyond early roadmap phases.

## Constraints
- Follow SEL for this non-trivial governance/documentation task.
- Use repo intelligence first; GitNexus CLI status has already been run.
- Do not rewrite plans blindly; upgrade them against actual repo reality.
- Do not modify unrelated code.
- Any authoritative-document conflict must be surfaced explicitly.

## Unknowns / Open Questions
- Which active plans are materially stale versus merely thin
- Whether the nested-AGENTS governance plan should remain active or be archived/superseded
- Which plans need structural expansion versus only reality reconciliation
- Whether state docs need updates after the plan refresh

## Likely Codebase Touchpoints
- `.ai/03_plans/*`
- `.ai/02_audits/*`
- `.ai/05_logs/*`
- `.ai/01_roadmap/*`
- `.ai/10_state/*`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/**`
- `scripts/tests/**`
- `spatial-daemon/**`
- `config/vitruvius.yaml`
