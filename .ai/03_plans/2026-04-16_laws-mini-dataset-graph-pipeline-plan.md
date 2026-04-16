---
task: laws-mini-dataset-graph-pipeline
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Laws Mini Dataset Graph Pipeline Plan

## 1. Executive Summary
Yes — Vitruvius can already output a real knowledge graph today, but only from the **global canonical shared layer**. It is **not yet safe or truthful** to call the current command set a clean one-folder or mini-dataset pipeline because key surfaces still depend on global shared roots and global `latest_*` artifacts.

The recommended next target is therefore **not** a generic raw-laws-folder pipeline. It is a **manifest-backed, 4-folder core-laws-bundle scoped graph proof** built from manifest-selected canonical/promoted inputs, with dataset-specific artifacts and **no writes to global `latest_*` paths**. The user-preferred bundle is:
- `PD-1096`
- `RA-9514`
- `BP-344`
- `BP-220`

Before any implementation starts, the next step is a **path audit**: map the full source→graph path, measure the blast radius of the required changes, and identify optimization opportunities — including whether any future hot-path work would legitimately belong in Rust. Because this bundle broadens beyond the repo’s current PD-1096-only reference-corpus framing, the proof should be treated as a **gated pilot implementation target**, not as already-cleared generic all-laws support. After that proof, the pipeline can widen in stages to dataset-safe review/promotion, then end-to-end dataset orchestration, then per-section and interconnected graphs.

## 2. RALPLAN-DR Summary

### Principles
1. **Truthful scope first** — M1 proves a bounded graph for a user-selected core-laws bundle, not a generic raw-laws pipeline.
2. **Canonical/promoted inputs only** — the graph proof is built from scoped canonical and approved relationship inputs, not directly from raw PDFs.
3. **No global artifact contamination** — M1 must not write to `latest_graph_snapshot.json` or any `latest_relationship_*` artifact.
4. **Manifest-bounded determinism** — dataset identity and allowed inputs must be explicit so leakage is testable.
5. **Scale by staged widening** — first core-laws-bundle proof, then upstream dataset-safe review/promotion, then broader per-section and merged graphs.

### Decision Drivers
1. **Need a real graph soon** without overclaiming full all-laws support.
2. **Must stay within current repo gates** by treating the 4-folder bundle as an explicit, reviewable pilot scope rather than silently assuming generic all-laws expansion is already allowed.
3. **Need a safe foundation** for later section-wide and interconnected graphs.
4. **Low-spec operation matters** — the eventual path must remain viable on an 8 GB M2-class machine, not just on high-end hardware.

### Viable Options
#### Option A — Full dataset-aware dual-mode across all stages first
Make convert/refine/canonicalize/extract/review/promote/build/query all dataset-aware immediately.
- **Pros:** comprehensive long-term shape
- **Cons:** too broad for first proof; high blast radius
- **Verdict:** not first move

#### Option B — Manifest-backed scoped graph proof first, then upstream scoping later
Start with a **4-folder core-laws-bundle manifest-backed graph proof** using scoped canonical/promoted inputs and dataset-specific outputs.
- **Pros:** smallest safe proof; truthful; extensible
- **Cons:** still needs later upstream scoping work
- **Verdict:** **chosen**

#### Option C — Ad hoc manual experiment using existing global latest artifacts
Use current commands and accept global output collisions.
- **Pros:** fastest demo
- **Cons:** not truthful, not deterministic, unsafe
- **Verdict:** rejected

## 3. ADR

### Decision
Implement **M0: path/blast-radius/optimization audit** first, then **M1: scoped graph proof**.

### Why Chosen
This answers the user’s real question — “can we output a useful knowledge graph for a bounded laws slice?” — honestly and safely, while preventing premature code changes that only make the first pilot succeed.

### Alternatives Considered
- Full dual-mode pipeline first
- Ad hoc global-latest demo
- Separate experimental mini-pipeline outside the main CLI contracts

### Consequences
- M1 can produce a real graph, but not yet a full raw-folder→graph pipeline.
- M2/M3 are required for broader dataset-safe orchestration.
- The first implementation slice is more useful than a one-law proof, but it also broadens beyond the repo’s current PD-1096-only reference-corpus framing. The plan therefore treats the 4-folder bundle as a **gated pilot** that must be explicitly accepted before implementation, rather than as automatic all-laws support.
- The implementation must remain **generic at the code level** even when the first validation target is a specific 4-folder bundle.

## 4. Current Repo Reality

### What already exists
The repo already ships a real source→graph path:
- upstream stages: `scan`, `convert`, `convert-one`, `refine`, `refine-one`, `canonicalize`, `canonicalize-one`, `canonicalize-plan-one`, `extract-relationships-one`, `extract-relationships-sections-one`, `review-relationships-ollama`, `review-relationships-ollama-second-pass`, `promote`
- downstream graph/query stages: `build-graph`, `query-graph`, `export-graph-owl`, `query`, `query-structured`

### What is already possible today
- a one-file or one-law operator-driven path is possible by chaining existing single-file commands manually
- `build-graph` can already emit a graph snapshot and `export-graph-owl` can emit Turtle/RDF

### What is not yet safe/truthful for dataset scoping
- `scripts/vitruvius/graph/cli.py` reads only `003_Canonical-Knowledge-Layer/shared` and writes only the global `latest_graph_snapshot.json`
- `scripts/vitruvius/query/cli.py` reads only the global latest snapshot
- `scripts/vitruvius/promotion/__init__.py` reads global latest high-confidence review artifacts
- `scripts/vitruvius/relationships_sections.py` writes global latest extraction artifacts and still hardcodes NBCP/IRR-centric source-ID behavior
- batch flows (`run_convert`, `run_refine`, `run_canonicalize`) are whole-layer operations

### Why the next step is a path audit, not code
The repo already has enough real pipeline/graph machinery that the main uncertainty is no longer “can it graph at all?” but:
- exactly which modules and commands must change for a scoped path
- how far the change blast radius reaches
- whether any performance-sensitive pieces are likely to become hot enough to justify Rust later
- where the safe boundary is between a scoped graph proof and a full dataset-aware orchestration rewrite
- how to keep the working set and execution model small enough for low-spec machines without sacrificing output integrity

### Current raw pilot anchor
- laws namespace: `001_Raw-Source-Layer/001-Laws/`
- user-preferred first pilot bundle:
  - `001_Raw-Source-Layer/001-Laws/PD-1096/`
  - `001_Raw-Source-Layer/001-Laws/RA-9514/`
  - `001_Raw-Source-Layer/001-Laws/BP-344/`
  - `001_Raw-Source-Layer/001-Laws/BP-220/`

## 5A. Formal Blast-Radius Matrix by Module

| Module / Surface | Stage | Why touched | Current coupling | Future change class | Blast risk | Low-spec concern | Rust candidacy now |
|---|---|---|---|---|---|---|---|
| `scripts/pipeline_cli.py` | orchestration entrypoint | future dataset-scoped commands/wrappers must be registered here | global/default command surface | CLI/orchestration | HIGH | command sprawl can encourage broad runs | no |
| `scripts/vitruvius/conversion.py` | conversion | reusable per-file conversion for pilot bundle | single-file path good; batch path global | orchestration reuse | MEDIUM | avoid accidental whole-bundle eager conversion | no |
| `scripts/vitruvius/normalization/refine.py` | refinement | reusable per-file refinement for pilot bundle | batch path global | orchestration reuse | MEDIUM | whole-layer traversal is a low-spec risk | no |
| `scripts/vitruvius/canonicalize.py` | canonicalization | turns refined markdown into canonical source pages | writes to shared canonical layer | truth/scoping | HIGH | avoid broad canonical rewrites | no |
| `scripts/vitruvius/relationships_sections.py` | extraction | likely main extractor for scoped proof | global latest extraction file; NBCP/IRR-specific source IDs | truth/scoping | HIGH | broad section processing may overrun small-machine budgets | maybe later only if profiling proves it |
| `scripts/vitruvius/ollama_review.py` | tier-1 review | needed if proof includes scoped review | consumes global latest extraction and writes global latest review artifacts | artifact isolation | HIGH | re-reviewing broad candidate sets is expensive on 8 GB | no |
| `scripts/vitruvius/ollama_review_second_pass.py` | tier-2 review | follow-on adjudication | global latest tier-1 outputs | artifact isolation | MEDIUM | not first optimization target | no |
| `scripts/vitruvius/promotion/__init__.py` | promotion | defines safe relationship input path into graphable truth | consumes global latest high-confidence file, writes shared truth | truth/governance boundary | HIGH | should avoid broad promotion churn | no |
| `scripts/vitruvius/graph/cli.py` | graph build/query | actual scoped proof surface | shared canonical root + global latest snapshot paths | graph scoping | HIGH | major low-spec win if inputs/outputs are bounded | maybe later if graph workloads grow |
| `scripts/vitruvius/graph/builder.py` | graph construction | walkers determine graph breadth and leakage | whole shared root semantics | graph scoping/leakage control | HIGH | bounded manifests reduce working set first | maybe later if profiling shows large-corpus hotspot |
| `scripts/vitruvius/query/cli.py` | query consumption | user-facing proof needs scoped query path | global latest snapshot only | query scoping | HIGH | snapshot selector prevents broad overwrite/copy patterns | no |
| `scripts/vitruvius/ontology/cli.py` | export | scoped TTL export is useful proof artifact | global latest snapshot/export paths | export scoping | MEDIUM | keep export bounded to dataset snapshot | no |
| `scripts/tests/test_graph_*`, `test_query_*`, `test_run_promote.py`, `test_integration_e2e.py`, `test_pipeline_cli_byte_identity.py` | verification | regression safety and compatibility proof | many tests assume current global/shared defaults | regression / compatibility | HIGH | critical to preserving low-spec-safe default behavior | no |

## 5. Scope and Non-Goals

### In Scope
- one **manifest-backed 4-folder core-laws bundle**
- one dataset-specific graph snapshot
- one dataset-specific integrity report
- one dataset-specific query path
- no writes to global `latest_*` artifacts for M1
- a staged scale path toward broader per-section and interconnected graphs
- explicit path/blast-radius/optimization study before implementation

### Explicit Non-Goals for M1
- direct raw-folder → graph building
- generic support for all laws folders
- full dataset-aware dual-mode across every pipeline stage
- cross-section merged graph
- proving that current extraction logic is generic across `001-Laws/*`
- any pilot-only code path that cannot scale to future dataset manifests

## 6. Micro / Macro Planning Rule

### Micro (pilot) requirement
The first implementation target must be useful enough to inspect as a graph:
- a 4-folder core-laws bundle is acceptable as the first validation target
- the plan must still keep that target bounded and explicitly gated

### Macro (codebase) requirement
The implementation must **not** be shaped only to make this first bundle succeed. It should be designed so the same mechanism can later support:
- a different dataset manifest
- a one-folder proof
- a section-wide proof
- an eventual merged/interconnected graph

### Hard anti-shortcut rule
Do **not** edit code in a way that hardcodes the first bundle by folder name just so the plan can succeed. The pilot bundle is a **validation target**, not an excuse for one-off logic.

## 7. Milestones

### M0 — Path Audit, Blast Radius, and Optimization Study
**Goal:** map the full source→graph path before implementation and identify the safest execution slice.

#### Deliverables
- explicit path map from raw slice anchor → conversion → refinement → canonicalization → extraction → review → promotion → graph build → query/export
- blast-radius map of all modules, commands, run artifacts, and state/docs touched by a scoped graph proof
- optimization/rust triage identifying:
  - what is orchestration only and should remain Python
  - what may become hot-path enough to justify future Rust consideration
  - what definitely should **not** be moved to Rust
- low-spec survivability notes identifying likely RAM/CPU pressure points and opportunities to keep the scoped proof viable on 8 GB-class machines
- implementation-slice recommendation for M1

#### Fresh starting evidence already gathered
- `build-graph --help`, `query --help`, `promote --help`, and `extract-relationships-sections-one --help` all resolve successfully
- current path map is now documented in the supporting research pack
- current blast-radius summary is now documented in the supporting audit
- current pilot bundle size is bounded:
  - `PD-1096`: 15 files
  - `RA-9514`: 1 file
  - `BP-344`: 2 files
  - `BP-220`: 1 file
- initial optimization triage says the first execution slice is still orchestration/state/artifact-routing work and should remain Python unless later profiling proves otherwise

#### Acceptance Criteria
- every touched command/module is enumerated
- global `latest_*` couplings are explicitly listed
- query/export path assumptions are explicitly listed
- promotion/review artifact safety risks are explicitly listed
- any future Rust candidates are named only as hypotheses, with justification requirements rather than premature commitments
- the audit explicitly distinguishes **micro pilot needs** from **macro codebase design constraints**
- the audit explicitly records low-spec constraints and likely memory-pressure points for the scoped proof

#### Implementation Direction
- inspect and document the full path through:
  - `pipeline_cli.py`
  - conversion/refine/canonicalize/extraction/review/promotion modules
  - graph/query/export modules
- run impact analysis on the likely touched code roots before execution
- classify candidate changes into:
  - required for scoped proof
  - required later for dataset-safe orchestration
  - optimization-only / defer
  - pilot-specific assumptions that must be turned into manifest data instead of code branches
- classify likely low-spec wins such as:
  - reducing whole-layer traversals
  - avoiding global latest-artifact rewrites
  - keeping query/build inputs manifest-bounded
  - preferring smaller working sets over convenience

### M1 — Scoped Graph Proof for the Core Laws Bundle
**Goal:** prove a real graph can be emitted for one bounded law-family mini-corpus slice.

#### Deliverables
- dataset manifest for a 4-folder bundle such as `laws-core-bundle-mini`
- dataset-specific graph snapshot
- dataset-specific integrity report
- dataset-specific query path or snapshot selector
- dataset-specific run outputs only

#### Acceptance Criteria
- one manifest-backed 4-folder core-laws bundle
- one dataset-specific snapshot
- one dataset-specific integrity report
- one dataset-specific query path
- **no writes to** `latest_graph_snapshot.json`
- **no writes to** any `latest_relationship_*`
- the proof design is still practical for an 8 GB M2-class machine by construction (bounded inputs, bounded outputs, bounded working set)

#### Implementation Direction
- add dataset manifest contract
- add scoped graph build mode (`build-graph --dataset <id>` or equivalent explicit root/output parameters)
- add scoped query mode or snapshot selector because current query CLI is global-latest-bound
- use **manifest-selected approved relationship inputs** or dataset staging inputs only — never global `latest_relationship_*`
- preserve the current default/global pipeline behavior when dataset mode is unused
- avoid special-casing the four selected folders in code; the dataset manifest should carry that selection
- implement only the minimum slice justified by M0 blast-radius findings
- prefer bounded/streamed/scoped execution over convenience batch behavior whenever there is a low-spec tradeoff

### M2 — Dataset-Safe Review/Promotion Inputs
**Goal:** remove dependence on unsafe global relationship artifact flows.

#### Deliverables
- dataset-scoped extraction outputs
- dataset-scoped review outputs
- dataset-scoped promotion inputs and audit logs
- explicit staging-vs-shared relationship policy

### M3 — End-to-End Mini Dataset → Graph Orchestration
**Goal:** add wrappers/orchestrators for dataset-scoped runs across the bounded slice.

#### Deliverables
- dataset wrapper CLI family or composite command
- end-to-end reproducible core-laws-bundle run

### M4 — Expansion Path
**Goal:** scale from one slice to more laws slices, then per-section graphs, then merged graphs.

#### Deliverables
- per-law repetition model
- per-section graph model
- merged-graph collision/provenance rules

## 8. Dataset Contract
The first implementation should define a compact manifest contract with fields such as:
- `dataset_id`
- `raw_slice_anchor`
- `canonical_input_manifest`
- `relationship_input_manifest`
- `graph_output_root`
- `run_output_root`
- `query_snapshot_path`
- `notes_on_scope`

Design rule:
- the manifest contract must be **dataset-generic**, not “laws-core-bundle-specific”
- the selected four folders are the first **manifest instance**, not the shape of the code
- if the implementation cannot generalize beyond the first manifest instance without code changes, stop and revisit the design

### Performance evidence note
Human-readable benchmark and optimization notes for this track should be written under:
- `/.ai/00_performance/`

The first execution slice does not yet require benchmark claims, but M0 and later M1/M2 work should use that directory to accumulate:
- low-spec survivability notes
- benchmark summaries
- optimization experiments
- Rust-candidacy evidence

## 9. Output Location Contract
Recommended roots:
- `006_System-Manifests/runs/datasets/<dataset_id>/...`
- `005_Operational-Intelligence-Layer/graph/datasets/<dataset_id>/...`

Hard rule:
- M1 must **not** mutate global `latest_*` graph or relationship artifacts.

## 10. Risks and Stop Conditions

### Key Risks
1. **Leakage risk** — scoped build may still ingest unrelated shared canonical nodes or relationships if not manifest-bounded.
2. **Promotion-input safety risk** — M1 must explicitly choose safe relationship inputs instead of borrowing from global latest review files.
3. **Scoped query risk** — query surfaces are currently global-latest-oriented.
4. **Overclaim risk** — current extractor logic is still NBCP/IRR-specific, so M1 cannot imply generic all-laws support even if the first pilot bundle contains four laws folders.
5. **Future merge risk** — later cross-section graphs will need explicit collision/provenance rules.
6. **Optimization scope drift** — performance/rust discussion could balloon the pilot if not bounded to M0 triage only.
7. **Wrong-layer optimization risk** — moving orchestration/state/artifact-routing logic into Rust would violate Vitruvius boundaries.
8. **Pilot-gate risk** — the 4-folder bundle is more useful than a single-law proof, but it still needs explicit acceptance as a bounded pilot before execution.
9. **Pilot-specialization risk** — implementation may drift into hardcoded support for the first four folders instead of a reusable dataset manifest mechanism.
10. **Low-spec failure risk** — an implementation that silently assumes large RAM or whole-corpus in-memory behavior would violate the project’s accessibility goal even if it works on powerful hardware.

### Stop Conditions
Stop execution planning and revisit the contract if:
- a scoped graph build cannot be achieved without mutating global latest artifacts
- a dataset-specific query path cannot be added without breaking the current global query surface
- the only available relationship inputs for M1 depend on unsafe global latest review artifacts
- the proposed scope drifts from the bounded 4-folder core-bundle proof into generic all-laws support prematurely
- the optimization discussion starts driving implementation before the scoped graph proof path is even mapped
- the implementation approach only works for the first selected four folders and cannot generalize to a second manifest instance without rewrites
- the only plausible implementation path assumes high-memory execution and cannot be made practical on an 8 GB-class machine

## 11. Verification Plan
M1 must include all of the following:

1. **Leakage check**
   - prove only manifest-allowed canonical pages and relationship records enter the scoped graph

2. **Artifact isolation check**
   - verify outputs land only under dataset-specific directories
   - verify global `latest_*` files remain unchanged

3. **Scoped integrity check**
   - run integrity against the dataset snapshot
   - require zero duplicate node IDs
   - require zero dangling edges
   - record warning count explicitly

4. **Scoped query check**
   - run at least 3–5 seeded questions against the scoped snapshot
   - require evidence-bearing answers

5. **Determinism / replay check**
   - rerun the same manifest twice
   - compare snapshot and integrity outputs

6. **Boundary check**
   - prove M1 did not write into shared canonical truth unintentionally

7. **Non-goal verification**
   - explicitly record that M1 is a 4-folder core-laws-bundle proof and does not claim generic all-laws support

8. **Macro-compatibility verification**
   - prove the dataset-scoped implementation preserves the current default/global path when dataset mode is unused
   - prove a second manifest instance could be supplied without code surgery

9. **Anti-special-case verification**
   - inspect the implementation for folder-name-specific branches or constants added only to make the first bundle pass
   - reject implementation success if the first four folders are wired in as code rather than manifest data

10. **Low-spec viability verification**
   - explicitly record the expected working-set controls for the scoped proof
   - reject the implementation if the design depends on whole-corpus/global-latest behavior that defeats low-spec execution
   - where performance-sensitive code is identified, document whether optimization stays in Python or becomes a future Rust candidate and why

## 12. Follow-On Staffing Guidance

### Available agent types
- `planner`
- `architect`
- `critic`
- `executor`
- `test-engineer`
- `verifier`
- `writer`

### Ralph path
- one sequential owner
- architect review at each milestone boundary
- good fit for M0 → M1 → M2 staged delivery

### Team path
- Lane 1: dataset manifest + scoped graph/query implementation
- Lane 2: leakage/isolation/determinism + blast-radius tests
- Lane 3: docs/state/validation evidence + optimization/rust triage + macro-compatibility + low-spec review

### Team launch hint
- `omx team 3:executor "implement core-laws-bundle scoped graph proof per accepted plan"`

## 13. Plan Critique

### What this plan avoids correctly
- pretending the graph can be built directly from raw PDFs
- pretending current command surfaces are already dataset-scoped
- pretending M1 proves generic all-laws support
- dualizing every pipeline stage before the first bounded proof exists
- making code changes that only make this first bundle pass without helping future dataset manifests

### Remaining tension
- the fastest proof is a scoped graph builder/query surface
- the fully correct long-term shape still requires dataset-safe review/promotion and then dataset orchestration
- the user also wants optimization/rust thinking early, but that must remain an **audit of the path** first, not a premature implementation branch
- the first pilot should be graph-useful, but the implementation must still be reusable beyond that pilot
- low-spec viability is a core success criterion, but the plan must still refuse cargo-cult optimization that would reduce correctness or truthfulness

## 14. Execution Checklist
- [ ] map the full source→graph path for the 4-folder core-laws-bundle pilot
- [ ] produce the blast-radius list for commands/modules/artifacts/docs likely to change
- [ ] perform optimization/rust triage and document what stays Python vs what could become future Rust candidates
- [ ] document low-spec constraints and likely RAM/CPU pressure points for the first proof
- [ ] create dataset manifest contract
- [ ] add scoped graph build mode and dataset-specific outputs
- [ ] add snapshot-selected/scoped query surface
- [ ] define safe M1 relationship input policy (manifest-selected approved inputs or dataset staging)
- [ ] define the macro-compatibility contract for future dataset manifests
- [ ] prove no writes to global `latest_*`
- [ ] run leakage, isolation, integrity, query, determinism, and boundary checks
- [ ] run macro-compatibility and anti-special-case checks
- [ ] run low-spec viability checks at the design level before approving implementation
- [ ] write validation log for the core-laws-bundle proof
- [ ] only then plan M2 dataset-safe review/promotion scoping
