# `.ai/03_plans/` — Plan Index

> **Purpose:** One-stop index of every implementation plan, design spec, and contract in this directory.
> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md`
> **Updated:** 2026-04-14

Each plan is a self-contained document keyed by a `plan_id` and a `phase` label in its YAML frontmatter. Plans are one of three types:

| Type | Definition | Example |
|---|---|---|
| `implementation_tdd` | Full bite-sized TDD task list with code in every step. Ready to execute. | `phase-7-promotion-governance-plan.md` |
| `design_spec` | Architecture + task sequence, expanded to TDD before execution. | `phase-1b-multi-parser-integration-plan.md` |
| `contract` | Frozen interface between phases. Changes require a version bump. | `ingestion-refinement-contract.md` |

## Plan Naming Convention

- **Phase plans:** `phase-<N>-<topic>-plan.md` (e.g. `phase-7-promotion-governance-plan.md`)
- **Contracts:** `<topic>-contract.md` (legacy; new contracts should use `contract-<topic>.md`)
- **Frontmatter `plan_id`** uniquely identifies the plan regardless of filename.

## Current Plans

| Phase | Plan ID | Title | Status | Sprint | Type | File |
|---|---|---|---|---|---|---|
| 1A→12 | `statistical-architectural-upgrade` | **Statistical & Architectural Intelligence Upgrade** | 🔥 In progress (Streams A-G CLOSED 2026-04-14; H-K pending) | Sprint D onwards | implementation_tdd | [statistical-architectural-upgrade-plan.md](statistical-architectural-upgrade-plan.md) |
| 1B | `phase-1b-multi-parser-integration` | Multi-Parser Integration | 🔥 In progress (Foundation shipped) | Sprint C | design_spec | [phase-1b-multi-parser-integration-plan.md](phase-1b-multi-parser-integration-plan.md) |
| 1B↔1C | `contract-ingestion-refinement` | Ingestion → Refinement Handoff Contract | ❄️ Frozen | N/A | contract | [ingestion-refinement-contract.md](ingestion-refinement-contract.md) |
| 1C | `phase-1c-centralized-normalization` | Centralized Normalization — Text Refinement Layer | ✅ MVP Complete (archived 2026-04-14) | Sprint B — closed MVP scope | design_spec | [../09_archive/plans/phase-1c-centralized-normalization-plan.md](../09_archive/plans/phase-1c-centralized-normalization-plan.md) |
| 2 | `phase-2-canonicalizer-restoration` | Canonicalizer Restoration — Structured Section Generation | ✅ Complete (archived 2026-04-14) | Sprint B — closed | implementation_tdd | [../09_archive/plans/phase-2-canonicalizer-restoration-plan.md](../09_archive/plans/phase-2-canonicalizer-restoration-plan.md) |
| 3C | `phase-3-concept-enrichment` | Concept Enrichment — Placeholder to Knowledge Node | ✅ MVP Complete (13/20, archived 2026-04-14) | Post-Sprint-C — closed (deterministic) | design_spec | [../09_archive/plans/phase-3-concept-enrichment-plan.md](../09_archive/plans/phase-3-concept-enrichment-plan.md) |
| 6A | `phase-6a-review-gap-closure` | Review Layer Gap Closure | ✅ Complete (archived 2026-04-14) | Sprint A + B — closed | implementation_tdd | [../09_archive/plans/phase-6a-review-gap-closure-plan.md](../09_archive/plans/phase-6a-review-gap-closure-plan.md) |
| 6B | `phase-6b-second-pass-review` | Second-Pass Review (Two-Stage Adjudication) | ✅ Complete (archived 2026-04-14) | Sprint C — closed | implementation_tdd | [../09_archive/plans/phase-6b-second-pass-review-plan.md](../09_archive/plans/phase-6b-second-pass-review-plan.md) |
| 7 | `phase-7-promotion-governance` | Promotion Governance Layer | ✅ Complete (archived 2026-04-14) | Sprint A — closed | implementation_tdd | [../09_archive/plans/phase-7-promotion-governance-plan.md](../09_archive/plans/phase-7-promotion-governance-plan.md) |
| 8 | `phase-8-graph-contract-indexing` | Graph Contract & Filesystem-Backed Indexing | 🔒 Gated | Post-Sprint-C | design_spec | [phase-8-graph-contract-indexing-plan.md](phase-8-graph-contract-indexing-plan.md) |
| 9 | `phase-9-query-ai-layer` | Query & AI Augmentation Layer | 🔒 Gated | Post-Phase-8 | design_spec | [phase-9-query-ai-layer-plan.md](phase-9-query-ai-layer-plan.md) |
| — | `sprint-b-polish-improvements` | Sprint B Polish (extractor dedup, Ollama warmup, lazy CLI, timestamp-aware diff, utils deprecation, concept status) | ✅ Complete (archived 2026-04-14) | Sprint B follow-on — closed | implementation_tdd | [../09_archive/plans/sprint-b-polish-improvements-plan.md](../09_archive/plans/sprint-b-polish-improvements-plan.md) |

**Status legend:** ✅ complete · 🟡 partial · 🔥 in progress (active sprint) · 📝 planned · 🔒 gated (do not start) · ❄️ frozen (contract)

## Execution Order (Dependency-Correct)

> **2026-04-14 update:** `statistical-architectural-upgrade` now takes precedence over all other plans per user directive (see its §1.2). Phases 8, 9, and 11 are *extended* by this plan, not replaced — their base MVPs ship first inside Streams H.0 and I.0.

```
Sprint A-C (CLOSED 2026-04-14)
  ├── phase-7-promotion-governance          ✅ complete
  ├── phase-1c-centralized-normalization    ✅ complete (MVP)
  ├── phase-6a-review-gap-closure           ✅ complete
  ├── phase-6b-second-pass-review           ✅ complete
  ├── phase-2-canonicalizer-restoration     ✅ complete
  ├── phase-3-concept-enrichment            ✅ 16/20 complete (4 deferred to Stream D)
  └── phase-1b-multi-parser-integration     🔥 Foundation shipped (Modernization absorbed by Stream B)

Sprint D — Statistical & Architectural Upgrade (weeks 1-5) 🔥 [HIGHEST PRIORITY]
  ├── Stream A — Dependency Bootstrap + Merkle Hash + Feature Flags
  ├── Stream B — Shannon Classifier + Table-to-Graph + Parametric NER
  ├── Stream C — Tier C OCR + AST Chunker + Embedding Chunker + Mahalanobis
  └── Stream D — TF-IDF + PMI + FCA + Contrastive Adapter

Sprint E — Intelligence (weeks 6-11)
  ├── Stream E — spaCy + CRF + KG Link Prediction
  ├── Stream F — NB + SLM Swarm + Conformal + Choquet + Reflection + Ontology Prompting
  └── Stream G — Bayesian Fusion + Stringency Matrix + Temporal Edges

Sprint F — Graph & Query (weeks 12-18)
  ├── Stream H — Phase 8 base + Centrality + Spectral + Community + MCMC + TDA + Wasserstein + Causal + Tensor
  ├── Stream I — Phase 9 base + Ontology Translator + GraphRAG Router + MCMC Ranker + HMM
  └── Stream J — Active Learning + Expected Model Change scoring

Sprint G — Scaling (weeks 19+, gated on second jurisdiction)
  └── Stream K — Rosetta Stone + Precedence Router + Tensor activation

Deferred (prerequisites outside Vitruvius)
  ├── FUTURE-ML-01 — LoRA fine-tuning      (needs GPU)
  ├── FUTURE-ML-02 — DPO pedagogical align (needs GPU + Ranger dashboard)
  └── FUTURE-LRN-01 — Bayesian Knowledge Tracing (needs ILXP + learners)
```

## How to Consume a Plan

### Before execution
1. Open the plan file.
2. Confirm the frontmatter `status` matches the active sprint in `/.ai/01_roadmap/current-phase.md`.
3. Read the plan's §"Scope Boundary" section.
4. If `plan_type: design_spec`, first expand Task sequence into `implementation_tdd` style (bite-sized steps with code). Otherwise go straight to execution.

### During execution
- Follow the superpowers sub-skill referenced in the plan header (usually `subagent-driven-development`).
- Tick `- [ ]` checkboxes as steps complete.
- Never skip the "run the failing test" step — it validates that the test actually tests what you think.

### After execution
- Update the plan's frontmatter `status` to `complete`.
- Record an `AD-XXX` entry in `/.ai/10_state/decisions.md` summarizing the final shape.
- Update `/.ai/01_roadmap/master-roadmap.md` §4 status table.
- Tick boxes in `/.ai/01_roadmap/milestone-tracker.md`.

## Plan Types in Depth

### `implementation_tdd`
- Every task has at minimum: `Files` block, failing test, run-test-to-fail, implementation with full code, run-test-to-pass, commit.
- An engineer with zero context for the codebase should be able to execute each step mechanically.
- No "TBD", "implement later", "add validation", or "similar to Task N" — the plan fails self-review if these appear.
- Sprint-A-critical plans are always `implementation_tdd`.

### `design_spec`
- Architecture narrative + task sequence at the level of "what, not how".
- Expanded to `implementation_tdd` *before* execution starts, not during.
- Appropriate for phases that are weeks or months away — premature TDD detail rots.
- The expansion step is itself a task: "expand plan-X into TDD form".

### `contract`
- Frozen interface shape between two phases.
- Changes bump `contract_version` and require signed-off updates on both producer and consumer sides.
- Violating a contract is a build failure, not a warning.

## Relationship to Other `.ai` Directories

| Directory | Relationship |
|---|---|
| `.ai/01_roadmap/` | Sets priority. Plans here execute what the roadmap decides. |
| `.ai/02_audits/` | Historical state. Plans cite audits in their dependencies section. |
| `.ai/06_specs/` | Schemas the plans produce files matching. Plans reference `source-schema.md`, `concept-schema.md`, `relationship-schema.md`. |
| `.ai/07_experiments/` | Experimental protocols that *inform* plans (parser comparison, model comparison). Not themselves plans. |
| `.ai/08_prompts/` | LLM prompt reference files. Plans reference them verbatim. |
| `.ai/10_state/` | Live snapshot of project state. Update after executing any plan. |

## Changelog

- **2026-04-14** — Initial index. Added frontmatter headers to the 3 pre-existing plans (1B, 1C, contract). Created 7 new plans: Phase 2, 3C, 6A, 6B, 7, 8, 9. Phase 7 is the most detailed (`implementation_tdd`, Sprint A active).
