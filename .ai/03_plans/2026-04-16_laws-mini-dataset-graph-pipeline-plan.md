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
- pilot-bundle admission checklist covering include/exclude decisions for adjacent or related law-family documents that sit outside the four named pilot folders
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
- raw-bundle boundary evidence already shows at least one adjacent related document lives outside a pilot folder:
  - `001_Raw-Source-Layer/001-Laws/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.pdf`
  - this makes folder-name heuristics unsafe; manifest membership must stay explicit
- initial optimization triage says the first execution slice is still orchestration/state/artifact-routing work and should remain Python unless later profiling proves otherwise
- team-assisted audit also confirmed:
  - current shared graph footprint: `23` nodes / `30` edges / `6` warnings / `0` errors
  - `latest_graph_snapshot.json` ≈ `38 KB`
  - `latest_relationship_extraction_sections.json` ≈ `96 KB`
  - `latest_relationship_review_high_confidence.json` ≈ `37 KB`
  - targeted graph/query test slice passed (`57` tests), with an additional graph/query CLI slice observed at `13` passing tests
- `npx gitnexus status` currently reports the index as stale (`indexed commit: 616c14a`, `current commit: e3c2bda`), so any later execution-phase impact analysis must refresh GitNexus before code edits

#### Acceptance Criteria
- every touched command/module is enumerated
- global `latest_*` couplings are explicitly listed
- query/export path assumptions are explicitly listed
- promotion/review artifact safety risks are explicitly listed
- any future Rust candidates are named only as hypotheses, with justification requirements rather than premature commitments
- the audit explicitly distinguishes **micro pilot needs** from **macro codebase design constraints**
- the audit explicitly records low-spec constraints and likely memory-pressure points for the scoped proof
- any adjacent law-family sources outside the four named folders are explicitly included or excluded by manifest rather than inferred by directory heuristics

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

#### M0 Exit Criteria
M0 is complete only when all of the following are true:
- the source→graph path map is explicit
- the module blast-radius matrix is explicit
- the artifact-level blast-radius / freshness / rollback model is explicit
- the M1 decision defaults are explicit
- the M1 cut line is explicit
- the low-spec execution budget is explicit
- the anti-special-case and macro-compatibility rules are explicit
- the M1 go/no-go readiness gate is explicit
- the planning artifacts agree with each other

#### Recommended execution slice order for M1
1. dataset manifest contract
2. dataset-specific output roots
3. scoped graph build surface
4. snapshot-selected/scoped query surface
5. safe relationship input policy
6. only then determine whether scoped review/promotion changes are required for the first proof
7. leakage / isolation / determinism / low-spec / anti-special-case verification

This order is chosen to keep the first proof truthful, bounded, and as low-risk as possible.

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
- `entry_role_manifest` or equivalent per-file role metadata

Design rule:
- the manifest contract must be **dataset-generic**, not “laws-core-bundle-specific”
- the selected four folders are the first **manifest instance**, not the shape of the code
- if the implementation cannot generalize beyond the first manifest instance without code changes, stop and revisit the design

### M1 Decision Ledger — Recommended Defaults

#### Manifest shape
- **Default:** one dataset manifest per pilot bundle
- **Recommended fields:** `dataset_id`, `dataset_kind`, `raw_slice_anchors`, `canonical_input_manifest`, `relationship_input_manifest`, `graph_output_root`, `run_output_root`, `query_snapshot_path`, `freshness_policy`, `pilot_gate`, and per-entry role/authority metadata
- **Rationale:** this keeps scope in data, not code, and is the cleanest defense against hardcoding the first 4-folder bundle into implementation logic

#### Canonical input selection
- **Default:** explicit canonical input allowlist, not a free-form root scan
- **Rationale:** strongest leakage control, deterministic bounded working set, and safer behavior on 8 GB-class machines

#### Relationship input policy
- **Default:** manifest-selected approved relationship files or dataset staging inputs only
- **Explicit prohibition:** never read global `latest_relationship_*` when dataset mode is requested
- **Rationale:** this is the main truth-governance boundary for M1

#### Scoped query selector
- **Default:** add a `--snapshot <path>` selector first, then `--dataset <dataset_id>` as a convenience layer later
- **Rationale:** path-based selection is the narrowest and easiest first contract to validate

#### Export selector
- **Default:** mirror query scoping with explicit snapshot-in / export-out selectors
- **Recommended shape:** `export-graph-owl --snapshot <path> --out <path>`

#### Freshness model
- **Default:** dataset outputs are fresh only when tied to the exact manifest hash + input fingerprint set
- **Minimum freshness fields:** `dataset_id`, `run_id`, `manifest_hash`, `generated_at`, upstream artifact references

#### Pilot acceptance gate
- **Default:** M1 is allowed only if manifest validation, bounded inputs, bounded outputs, scoped query, anti-special-case checks, and low-spec planning are all satisfied

### Pilot Manifest Entry Metadata Defaults
At minimum, each pilot-manifest entry should be able to express:
- `raw_path`
- `entry_role` (`authoritative`, `reference`, `summary`, `illustrative`, `partial_extract`, `adjacent_context`)
- `authority_tier`
- `variant_family`
- `edition_or_source_note`
- `include_in_m1` (boolean)
- `reason`

Design rule:
- file-role ambiguity must be handled in manifest data, not by silent filename heuristics or code branches

### Bundle-Wide Policy Statements
- The 4-folder bundle is a **validation target**, not an implementation special case.
- M1 builds from **canonical/promoted truth-bearing inputs**, not raw PDFs directly.
- M1 proves a **scoped graph for one bounded pilot bundle**, not generic all-laws support.
- Optimization priority is:
  1. bounded working set
  2. artifact isolation
  3. replay/freshness discipline
  4. only then compute-level optimization
- No Rust in M1 unless a measured hot path appears during later profiling.

### Decision Closure Order
The unresolved design decisions should be closed in this order:
1. manifest shape
2. canonical input selection
3. relationship input policy
4. scoped query selector
5. export selector
6. freshness model
7. pilot gate

Why this order:
- each later decision depends on earlier scope/freshness boundaries
- query/export choices are weaker until manifest/input policy is settled
- the pilot gate should be finalized last because it depends on the preceding defaults

### Dataset Artifact Metadata Schema (Planning Default)

Every dataset-scoped artifact family should carry, at minimum:
- `dataset_id`
- `dataset_kind`
- `run_id`
- `manifest_hash`
- `generated_at`
- `input_fingerprint` or equivalent source fingerprint summary
- `upstream_artifact_refs`
- `scope_notes`

Recommended by artifact family:
- **dataset extraction artifact** → add source markdown refs + extractor version
- **dataset review artifact** → add model, review policy, confidence filter settings
- **dataset promotion artifact** → add relationship-input manifest ref + promotion policy ref
- **dataset graph snapshot** → add canonical input manifest ref + relationship input manifest ref
- **dataset query/export output** → add selected snapshot path + selected snapshot manifest/run identity

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

### Current artifact baseline
Current shared/global artifacts are still small enough that the first proof is feasible on low-spec hardware, but they are already large enough that duplicated broad rewrites would be wasteful:
- `latest_graph_snapshot.json` ≈ `38 KB`
- `latest_relationship_extraction_sections.json` ≈ `96 KB`
- `latest_relationship_review_high_confidence.json` ≈ `37 KB`

### Default / Global Path Preservation Contract
The first implementation must be **strictly additive** to the existing global/shared pipeline.

Hard rules:
- when dataset mode is **not** invoked, the current default/global CLI entrypoints, paths, and outputs must continue to behave as they do today
- M1 must not repoint existing default commands from global/shared outputs to dataset-scoped outputs
- dataset-scoped graph/query/export behavior must be entered only through an explicit manifest, dataset selector, or scoped output argument
- compatibility should be proven by preserving current global test expectations unless a deliberate, separately-audited migration plan is approved

Planning clause to preserve long-term architecture:
- the first four-folder bundle may appear in manifests, examples, validation fixtures, and planning docs, but **must not** appear as a hardcoded routing condition, folder-name allowlist in core logic, or special branch that changes default/global behavior

### Pilot Distortion Guardrails
The first pilot must prove usefulness without bending the architecture around the pilot itself.

Hard rules:
- the four-folder core-laws bundle is a **validation target**, not an architectural primitive
- any logic that depends on `PD-1096`, `RA-9514`, `BP-344`, or `BP-220` by name in core orchestration should be treated as a plan violation unless confined to manifest data or test fixtures
- if supporting a second manifest instance would require code edits rather than manifest edits, stop and re-plan before implementation
- M1 must be reviewable as a generic dataset-scoped capability even if only one pilot manifest is executed first

### Rollout and Rollback Rules
The first implementation should widen capability in reversible slices.

Rollout rules:
- M1 must be introduced behind additive dataset-scoped commands, flags, or manifest-driven entrypoints
- no in-place migration of existing global `latest_*` artifacts is allowed during M1
- no shared canonical truth rewrite is allowed merely to make the pilot succeed

Rollback rules:
- M1 rollback must be achievable by removing or ignoring dataset-scoped manifests and outputs without restoring overwritten global/shared artifacts
- dataset-scoped outputs must live under dedicated dataset roots so they can be archived or removed independently
- if an M1 slice cannot be disabled without affecting the current global/shared graph and query path, the slice is too invasive for first implementation

### Dataset Output Freshness Contract
Dataset-scoped outputs must be unambiguous about whether they are current, stale, or selected for query/export.

Required metadata / semantics:
- every dataset-scoped output family should carry `dataset_id`, `generated_at`, and a stable path contract
- query/export must operate on an **explicitly selected** dataset snapshot path or manifest-selected snapshot, not by silently reusing a dataset-local `latest` without provenance
- M1 validation should prove that stale dataset outputs cannot be mistaken for current truth merely because they exist under the same dataset root

### Artifact Freshness / Metadata Table

| Artifact family | Must identify | Must prove | Failure if missing |
|---|---|---|---|
| Extraction | `dataset_id`, `run_id`, `manifest_hash`, source markdown refs | which candidate set belongs to which dataset run | review may consume stale or foreign candidates |
| Review | `dataset_id`, `run_id`, upstream extraction ref, model/policy | which review answers belong to which candidate set | promotion may consume stale or foreign review outputs |
| Promotion input/output | `dataset_id`, `run_id`, upstream review ref, promotion policy | which approved relationships were selected and why | scoped graph may inherit wrong truth inputs |
| Graph snapshot | `dataset_id`, `run_id`, canonical input ref, relationship input ref | exactly which truth-bearing inputs formed the graph | query/export can read the wrong graph |
| Query/export | selected snapshot path + selected snapshot identity | which graph was actually queried/exported | operator cannot distinguish scoped vs global result |

### Partial Run / Incomplete Output Contract
Rules:
- partial-run artifacts must be marked `incomplete`
- partial-run outputs must not be treated as current dataset truth
- the final scoped proof becomes “current” only after all required stage outputs pass validation
- missing bundle members cannot silently disappear from final reporting

### Bundle Coverage Contract
For the 4-folder bundle, the implementation must report per-folder coverage:
- raw files present
- canonical pages produced
- approved relationship inputs present
- nodes contributed
- edges contributed

Minimum rule:
- every folder in the manifest must appear in the final run report
- each folder must either contribute at least one truth-bearing artifact or be explicitly marked blocked/deferred with reason

### Per-Folder Coverage Report Schema
The final M1 validation/reporting layer should include one row per bundle member with at least:
- `folder_name`
- `raw_file_count`
- `converted_count`
- `refined_count`
- `canonical_count`
- `approved_relationship_input_count`
- `node_count_contributed`
- `edge_count_contributed`
- `status` (`covered`, `partial`, `blocked`, `deferred`)
- `notes`

### Thin-Graph Decision Rule
A scoped graph proof is **not** automatically successful merely because it emits a valid snapshot.

If the graph is valid but too sparse, the result should be `PARTIAL`, not `SUCCESS`.

Minimum usefulness checks should include:
- more than one connected relation chain
- not mostly isolated nodes
- 3–5 seeded questions returning evidence-bearing answers

### Thin-Graph Metrics to Record
The first proof should record, at minimum:
- connected-component count
- isolated-node count or rate
- edge type diversity
- per-folder node/edge contribution balance
- seeded query hit rate
- final outcome judgment: `SUCCESS` / `PARTIAL` / `FAIL`

### M1 Success vs Partial Success vs Fail Rubric

#### SUCCESS
Call M1 a success only if all of the following are true:
- dataset manifest is valid and generic
- graph build is scoped and does not mutate global `latest_*`
- query/export are scoped to the selected snapshot
- artifact freshness contract is satisfied
- all four bundle members are accounted for in final reporting
- graph integrity passes for the scoped snapshot
- seeded scoped queries return evidence-bearing answers
- macro-compatibility and anti-special-case checks pass
- low-spec execution constraints are respected by design

#### PARTIAL
Call M1 partial if:
- the scoped graph is valid but too thin to be useful
- one or more bundle members are explicitly blocked/deferred but reported honestly
- the graph proof works but one follow-on requirement (for example export ergonomics) is intentionally deferred
- the output is truthful, but not yet strong enough to claim the full pilot objective

#### FAIL
Call M1 failed if any of the following occur:
- global `latest_*` artifacts are mutated or silently reused
- the scoped query path still reads the wrong snapshot
- the implementation hardcodes the first four folders
- stale dataset outputs can masquerade as current truth
- the design cannot preserve the current default/global path
- the approach is not viable on an 8 GB-class machine without breaking the bounded-scope assumptions

## 10I. M1 → M2 Boundary and Expansion Triggers

### M1 may stop without widening to M2 if:
- the scoped graph proof succeeds using manifest-selected approved relationship inputs
- the scoped query surface is truthful and evidence-bearing
- no review/promotion artifact scoping changes are required for the proof
- the proof is generic enough to accept a second manifest instance without code surgery

### M2 must start immediately if any of the following are true:
- the first proof requires new relationship generation/review outputs that cannot be sourced safely from manifest-selected approved inputs
- promotion must be involved and the only available path depends on global `latest_relationship_*`
- the graph proof cannot stay truthful without dataset-scoped review/promotion artifacts
- scoped artifact freshness cannot be guaranteed without dataset-tagged review/promotion outputs

### After M1 success, the following may stay deferred:
- dataset-scoped batch conversion wrappers
- dataset-scoped batch refinement wrappers
- dataset-scoped batch canonicalization wrappers
- broader all-laws or per-section orchestration
- any Rust implementation work

### Planning note
This boundary is critical: M1 is a **scoped graph proof**, not a promise that review/promotion scoping is already solved.

## 10F. M1 Execution-Readiness Gate

M1 may begin only when all of the following are satisfied in the planning layer:
- full source→graph path map exists
- formal module blast-radius matrix exists
- artifact-level blast-radius and rollback shape are explicit
- manifest contract and metadata schema are explicit
- relationship input policy is explicit
- scoped query/export selector choice is explicit
- freshness/selection semantics are explicit
- anti-special-case and macro-compatibility rules are explicit
- low-spec execution budget assumptions are explicit
- M1 cut line is explicit

If any one of these is still fuzzy, M1 remains blocked.

## 10G. Low-Spec Execution Budget (Planning Level)

The first scoped proof should plan against an **8 GB M2-class machine** as a real constraint.

### Budget categories for M1
- **Working-set budget** — keep inputs bounded to the manifest-selected pilot bundle only
- **Artifact budget** — no unnecessary duplication or rewriting of global `latest_*` artifacts
- **Traversal budget** — no whole-shared-root scans when a manifest-selected subset is sufficient
- **Query budget** — no hidden reload of unrelated graph data when querying the scoped snapshot

### Planning-level no-go conditions
- M1 requires whole-canonical-root graph construction to function
- M1 requires whole-layer review/promotion artifact loading to function
- M1 cannot remain bounded in memory/work set on a modest pilot bundle
- M1 can only succeed by broad global artifact rewrites that negate the scoped design

### Default optimization stance
- prefer bounded manifests over broad scans
- prefer selected snapshots over global latest state
- prefer fewer artifact rewrites over convenience
- only escalate to Rust after later profiling identifies a true hot path

### Scoped Query Correctness Contract
The scoped query surface should echo:
- `dataset_id`
- selected snapshot path
- manifest hash or run identifier

The plan must explicitly prove:
- answers come from the scoped snapshot, not the global latest snapshot
- differing scope selections can yield appropriately different results

## 10H. Codebase Protection List for M1

The following behaviors and surfaces must remain unchanged during M1 unless a separately-audited migration explicitly says otherwise:

### Default/global behaviors that must remain intact
- current global `build-graph` default behavior
- current global `query` and `query-structured` default behavior
- current global `query-graph` default behavior
- current global `export-graph-owl` default behavior
- current default/global `latest_*` artifact consumers when dataset mode is not invoked

### Truth-bearing locations that must not be implicitly repurposed
- `003_Canonical-Knowledge-Layer/shared/relationships/` as the shared canonical relationship layer
- existing shared canonical source and concept files unless the scoped proof explicitly and safely selects from them
- existing promotion audit semantics for the global/default path

### Planning rule
M1 may add **parallel scoped paths** and **dataset-scoped artifacts**, but it must not silently redefine the default/global path in order to make the pilot work.

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
11. **Artifact-reuse risk** — stale dataset-specific outputs could be mistaken for current truth unless the plan defines clear refresh/selection semantics.
12. **Partial-run truth risk** — a partially completed bundle could still emit a technically valid graph and mislead operators if incompleteness is not surfaced explicitly.
13. **Thin-graph false-success risk** — a graph may be valid but too sparse or skewed to be an honest success for the intended bundle.
14. **Adjacent-source contamination risk** — related laws or orders may live outside the four chosen pilot folders (for example, BP-344-adjacent material under `001-Laws/DPWH/`), so folder-only inclusion rules can silently widen scope.
15. **Stale-impact-map risk** — a stale GitNexus index or stale graph-tool context can underreport the real blast radius right before coding starts.

### Stop Conditions
Stop execution planning and revisit the contract if:
- a scoped graph build cannot be achieved without mutating global latest artifacts
- a dataset-specific query path cannot be added without breaking the current global query surface
- the only available relationship inputs for M1 depend on unsafe global latest review artifacts
- the proposed scope drifts from the bounded 4-folder core-bundle proof into generic all-laws support prematurely
- the optimization discussion starts driving implementation before the scoped graph proof path is even mapped
- the implementation approach only works for the first selected four folders and cannot generalize to a second manifest instance without rewrites
- the only plausible implementation path assumes high-memory execution and cannot be made practical on an 8 GB-class machine
- stale or ambiguous dataset-specific outputs cannot be clearly distinguished from current scoped truth
- partial bundle execution can produce a misleadingly “successful” graph without explicit incompleteness markers
- the graph is technically valid but operationally too thin to support meaningful scoped queries
- pilot-bundle membership is ambiguous because adjacent law-family documents outside the four selected folders have not been explicitly included or excluded
- GitNexus freshness has not been re-established on the then-current commit before implementation planning turns into code edits

## 11. Verification Plan
M1 must include all of the following:

1. **Leakage check**
   - prove only manifest-allowed canonical pages and relationship records enter the scoped graph

2. **Artifact isolation check**
   - verify outputs land only under dataset-specific directories
   - verify global `latest_*` files remain unchanged
   - verify the default/global graph and query path still resolve exactly as before when dataset mode is unused

3. **Rollback check**
   - prove the M1 slice can be disabled or ignored without repairing overwritten global/shared artifacts
   - prove dataset-scoped outputs can be removed or archived independently

4. **Freshness / selection check**
   - prove the chosen dataset snapshot is explicit and provenance-bearing
   - prove stale dataset outputs cannot be silently mistaken for current scoped truth

5. **Scoped integrity check**
   - run integrity against the dataset snapshot
   - require zero duplicate node IDs
   - require zero dangling edges
   - record warning count explicitly

6. **Scoped query check**
   - run at least 3–5 seeded questions against the scoped snapshot
   - require evidence-bearing answers

7. **Determinism / replay check**
   - rerun the same manifest twice
   - compare snapshot and integrity outputs

8. **Boundary check**
   - prove M1 did not write into shared canonical truth unintentionally

9. **Non-goal verification**
   - explicitly record that M1 is a 4-folder core-laws-bundle proof and does not claim generic all-laws support

10. **Macro-compatibility verification**
   - prove the dataset-scoped implementation preserves the current default/global path when dataset mode is unused
   - prove a second manifest instance could be supplied without code surgery

11. **Anti-special-case verification**
   - inspect the implementation for folder-name-specific branches or constants added only to make the first bundle pass
   - reject implementation success if the first four folders are wired in as code rather than manifest data

12. **Low-spec viability verification**
   - explicitly record the expected working-set controls for the scoped proof
   - reject the implementation if the design depends on whole-corpus/global-latest behavior that defeats low-spec execution
   - where performance-sensitive code is identified, document whether optimization stays in Python or becomes a future Rust candidate and why

13. **Artifact freshness verification**
   - verify the dataset-specific proof defines how current run outputs are selected or refreshed
   - reject designs that allow stale scoped artifacts to masquerade as current truth

14. **Bundle completeness verification**
   - every folder in the 4-folder manifest appears in the final run report
   - missing/blocked members are reported explicitly

15. **Thin-graph usefulness verification**
   - record connected-component count, isolated-node rate or equivalent, edge diversity, and a success/partial/fail judgment

16. **Scoped query provenance verification**
   - query output must surface the selected dataset/snapshot identity and prove it did not read the global latest snapshot silently

17. **Partial-run safety verification**
   - confirm incomplete runs are marked incomplete and cannot masquerade as current truth

18. **Outcome-classification verification**
   - explicitly classify M1 as `SUCCESS`, `PARTIAL`, or `FAIL`
   - reject any validation report that avoids making that judgment

19. **Execution-readiness verification**
   - explicitly state whether the M1 readiness gate was fully satisfied before coding began

20. **Artifact metadata verification**
   - verify each dataset artifact family carries the planned identity/freshness metadata needed to prove scope and recency

21. **Low-spec budget verification**
   - verify the implemented slice stayed inside the planned low-spec working-set assumptions rather than quietly broadening to whole-layer behavior

22. **M1→M2 boundary verification**
   - explicitly state whether M1 was able to complete without widening into review/promotion scoping
   - if M2 is triggered, state exactly which condition forced the widening

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

## 13A. Implementation Forbidden Moves

The following are explicitly forbidden during M1 unless a separately-audited migration or follow-on plan changes the boundary:

### Forbidden scope shortcuts
- hardcoding `PD-1096`, `RA-9514`, `BP-344`, or `BP-220` into core orchestration logic
- treating the first 4-folder bundle as an architectural primitive instead of a manifest instance
- widening M1 from a scoped graph proof into generic all-laws support without a new planning decision

### Forbidden artifact shortcuts
- reading global `latest_relationship_*` artifacts in dataset mode
- writing dataset proof outputs into global `latest_graph_snapshot.json`, `latest_graph_integrity_report.json`, or `latest_graph_snapshot.ttl`
- silently falling back from missing dataset-scoped artifacts to global latest artifacts
- allowing stale dataset artifacts to masquerade as current truth

### Forbidden truth-boundary shortcuts
- building the graph directly from raw PDFs
- skipping canonical/promoted truth-bearing inputs just to get a graph faster
- rewriting shared canonical truth in order to make the pilot appear successful

### Forbidden architecture shortcuts
- changing default/global CLI behavior to make dataset mode easier
- introducing a second parallel mini-pipeline that duplicates existing stage logic without strong justification
- making the first implementation depend on behavior that cannot generalize to a second manifest instance

### Forbidden optimization shortcuts
- moving orchestration/state/artifact-routing logic into Rust during M1
- introducing optimization work before the path audit and blast-radius findings are settled
- accepting high-memory whole-corpus behavior on the grounds that stronger hardware exists elsewhere

### Planning enforcement
If any proposed execution step requires one of the forbidden moves above, M1 must stop and return to planning.

## 13B. Assumptions and Invalidation Triggers

### Current planning assumptions
1. The 4-folder pilot bundle is graph-useful enough to justify a scoped proof.
2. Manifest-selected approved relationship inputs may be sufficient for the first proof.
3. A scoped query/snapshot selector can be added without breaking the default/global query path.
4. Dataset-scoped outputs can coexist with the current global `latest_*` outputs without ambiguity if freshness semantics are explicit.
5. The first meaningful low-spec wins will come from scope control and artifact isolation, not from moving code into Rust.

### Invalidation triggers
Return to planning immediately if any of these assumptions prove false:
- the selected bundle is too thin to support a useful graph even when scoped correctly
- approved relationship inputs are insufficient and force a much wider review/promotion rewrite than expected
- scoped query selection cannot be introduced without destabilizing the current global query path
- dataset-scoped outputs cannot be kept unambiguous about freshness/selection
- the only plausible implementation path requires pilot-specific hardcoding or high-memory behavior

### Planning use
These assumptions are allowed to guide M1 only until contradicted by path-audit evidence or future design review.

## 14. Execution Checklist
Execution status note (2026-04-16):
- M1 implementation executed after truth reconciliation and readiness re-check.
- Outcome: `PARTIAL` (PD-1096 covered; `RA-9514`, `BP-344`, and `BP-220` were initially blocked due absent selected canonical/promoted inputs).
- Follow-on work is now governed by `2026-04-16_laws-m2-admission-plan.md`:
  - M2A source admission is complete for `RA-9514`, `BP-344`, and `BP-220`
  - additive M2B dataset-safe stage wiring is complete
  - conservative RA-9514 relationship admission is complete
  - concept-fit follow-on slices are complete for `BP-344` and `BP-220`
  - current bounded pilot outcome is now `SUCCESS`; see `2026-04-16_laws-core-bundle-bounded-pilot-success-validation.md`

- [x] map the full source→graph path for the 4-folder core-laws-bundle pilot
- [x] produce the blast-radius list for commands/modules/artifacts/docs likely to change
- [x] perform optimization/rust triage and document what stays Python vs what could become future Rust candidates
- [x] document low-spec constraints and likely RAM/CPU pressure points for the first proof
- [x] create dataset manifest contract
- [x] add scoped graph build mode and dataset-specific outputs
- [x] add snapshot-selected/scoped query surface
- [x] define safe M1 relationship input policy (manifest-selected approved inputs or dataset staging)
- [x] define the macro-compatibility contract for future dataset manifests
- [x] prove no writes to global `latest_*`
- [x] run leakage, isolation, integrity, query, determinism, and boundary checks
- [x] run macro-compatibility and anti-special-case checks
- [x] run low-spec viability checks at the design level before approving implementation
- [x] write validation log for the core-laws-bundle proof
- [x] decide M2 trigger status (`hit and executed within the bounded follow-on lane`)

## 15. Recommended M1 Implementation Sequence by Dependency

| Step | Depends on | Why now | What it unlocks | What must stay untouched | Rollback implication |
|---|---|---|---|---|---|
| 1. Finalize dataset manifest contract | M0 path map + decision ledger + readiness gate | all later scoped behavior must read from data, not code branches | dataset identity, bounded scope, future manifest reuse | default/global commands and `latest_*` artifacts | if wrong, stop before code spreads |
| 2. Finalize artifact metadata + freshness contract | step 1 | scoped outputs cannot be trusted without identity/freshness metadata | replay, freshness checks, stale-output rejection | current global artifact semantics | metadata-only design rollback |
| 3. Finalize dataset-specific output roots | steps 1–2 | output isolation is the first hard runtime boundary | scoped snapshot/integrity/export outputs | global snapshot, integrity, export, and review artifacts | scoped outputs removable independently |
| 4. Add scoped graph build surface | steps 1–3 | smallest truthful graph proof surface | dataset-specific snapshot + integrity report | current `build-graph` default/global path | scoped build removable/ignorable without repairing global graph |
| 5. Add snapshot-selected/scoped query surface | steps 1–4 | graph proof without scoped query remains half-global | seeded scoped query validation | current global `query` / `query-structured` defaults | selector removable without changing global query behavior |
| 6. Finalize safe relationship input policy | steps 1–5 | graph proof must know which truth-bearing relationship inputs are in scope | leakage-safe node/edge population | global `latest_relationship_*` flows | if unsafe, stop before touching review/promotion |
| 7. Validate leakage / isolation / freshness / completeness / thin-graph outcomes | steps 1–6 | prove the proof is truthful before broadening | M1 `SUCCESS` / `PARTIAL` / `FAIL` judgment | shared canonical truth and global latest artifacts | failed proof should leave only removable dataset outputs |
| 8. Decide whether M2 review/promotion scoping is actually required | successful step 7 | do not widen the slice unless the proof truly needs it | precise M2 boundary | current review/promotion defaults if not needed | defer if approved inputs already suffice |

### Why this dependency order is recommended
- It starts with **scope, freshness, and artifact boundaries**, not broad orchestration changes.
- It reaches the first truthful scoped graph proof as early as possible.
- It keeps low-spec working-set control front and center.
- It delays truth-sensitive widening until after the graph proof itself is validated.

### Dependency anti-patterns to avoid
- starting with review/promotion rewiring before scoped graph build/query exist
- adding batch dataset wrappers before the graph proof surfaces are validated
- introducing pilot-specific branches before the manifest contract is settled
- changing global `latest_*` behavior to make the first pilot appear successful

## 15A. Defer Matrix After M1

Even if M1 succeeds, the following should remain deferred unless explicit evidence says otherwise:

| Area | Default after M1 | Why defer |
|---|---|---|
| dataset-scoped batch conversion wrappers | defer | graph proof does not require broad batch orchestration yet |
| dataset-scoped batch refinement wrappers | defer | same reason; avoid widening blast radius prematurely |
| dataset-scoped batch canonicalization wrappers | defer | same reason; shared truth boundary is too sensitive to broaden casually |
| full dataset-scoped review pipeline | defer unless M1 requires it | review scoping is truth-sensitive and should only widen when necessary |
| full dataset-scoped promotion pipeline | defer unless M1 requires it | promotion touches shared truth and should widen only on evidence |
| broader all-laws support | defer | first proof is not generic all-laws support |
| merged / interconnected multi-section graph | defer | collision/provenance policy must mature first |
| Rust implementation work | defer | only justified after profiling shows a real hot path |

### Rule
M1 success does **not** automatically authorize widening to M2, M3, or broader corpus work. Each widening step must be justified by evidence, not momentum.

## 16. Verification Surface Map for Future M1 Work

The following test/validation surfaces are the most likely to matter when M1 eventually begins:

| Future M1 change area | Primary verification surface(s) | Why these matter |
|---|---|---|
| scoped graph build | `scripts/tests/test_graph_builder.py`, `scripts/tests/test_graph_cli.py`, backcompat graph snapshot tests | graph scoping, leakage, deterministic snapshot behavior |
| scoped query/snapshot selector | `scripts/tests/test_query_cli.py`, `scripts/tests/test_query_engine.py`, `scripts/tests/test_query_seed_accuracy.py` | prove query answers come from the selected scoped snapshot |
| relationship input policy | `scripts/tests/test_run_promote.py`, `scripts/tests/test_integration_e2e.py`, extraction/Phase 5E tests | truth-bearing relationship input path and no global-latest contamination |
| default/global path preservation | `scripts/tests/test_pipeline_cli_byte_identity.py`, global graph/query CLI tests | prove dataset mode stays additive |
| artifact metadata/freshness | plan-specific validation log + dataset artifact inspection + any new fixture tests | stale-output detection and replayability |
| low-spec discipline | `.ai/00_performance/` notes + targeted runtime/size observations | record bounded working-set evidence without overclaiming |

### Planning note
The execution phase should prefer **small targeted test slices first**, then broader regression only after the scoped surfaces behave correctly.

## 17. M1 Evidence Package Template

When M1 eventually runs, the execution/validation layer should be required to produce a coherent evidence package with at least:

### A. Scope identity artifacts
- dataset manifest file
- manifest hash
- dataset id / run id
- selected raw slice anchors

### B. Scoped output artifacts
- dataset-specific graph snapshot
- dataset-specific integrity report
- dataset-specific query evidence samples
- dataset-specific export artifact(s) if export is in scope

### C. Truth / freshness artifacts
- upstream relationship input references
- artifact freshness metadata proving currentness
- statement that global `latest_*` artifacts were not used or mutated in dataset mode

### D. Coverage / usefulness artifacts
- per-folder coverage table
- connected-component / isolated-node / edge-diversity observations
- seeded query hit-rate summary
- explicit `SUCCESS` / `PARTIAL` / `FAIL` judgment

### E. Macro safety artifacts
- default/global path preservation evidence
- anti-special-case review evidence
- low-spec observations / working-set notes
- rollback/removability statement for dataset-scoped outputs

### F. Recommended home for the evidence package
- validation log under `.ai/05_logs/`
- benchmark / low-spec notes under `.ai/00_performance/`
- any machine-readable benchmark/state companions under `.ai/10_state/`

### Planning rule
M1 should not be considered complete until this evidence package exists in a form that another reviewer can inspect without reconstructing the run from memory.

## 18. Pilot Bundle Admission Checklist

Before M1 begins, the four-folder pilot bundle must be admitted explicitly rather than inferred casually.

| Admission question | Required answer before M1 |
|---|---|
| What is the exact raw anchor for each bundle member? | each of `PD-1096`, `RA-9514`, `BP-344`, and `BP-220` is named explicitly in the manifest |
| Are there adjacent related documents outside those folders? | each such document is explicitly included or excluded, with a reason |
| Is upstream lineage known? | conversion/refinement/canonical/promoted inputs are either traceable or explicitly marked blocked |
| Are multiple editions/variants present? | the manifest or sidecar policy states whether all, one, or a prioritized subset are in scope |
| Is expected coverage known? | each folder has an expected coverage note so “empty but technically valid” does not surprise the verifier |
| Is there any bundle ambiguity left? | no unresolved include/exclude ambiguity remains when M1 starts |

### Current boundary evidence
- `BP-344` already has an adjacent related source outside the pilot folder:
  - `001_Raw-Source-Layer/001-Laws/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.pdf`
- This means the pilot cannot rely on simple directory-pattern expansion without risking scope leakage.

### Rule
If pilot-bundle admission cannot be stated explicitly in manifest terms, M1 is not ready.

## 18A. Variant / Edition Admission Policy

The first pilot bundle contains multiple editions, scans, summaries, illustrative materials, and partial extracts. M1 must not treat those as interchangeable by default.

### Current variant evidence
- `PD-1096/` includes:
  - complete scan
  - full-text edition
  - illustrated edition
  - summary
  - compact edition
  - multiple IRR / RIRR files
  - partial rule extracts
- `BP-344/` includes at least:
  - a `2024 Revised Implementing Rules and Regulations...`
  - `BP-344 IRR Accessibility Law DPWH.pdf`

### Planning requirement
Before M1 begins, the manifest must say whether each file is:
- authoritative input
- supporting/reference input
- summary-only context
- illustrative/non-authoritative context
- excluded from the first proof

### Rule
If multiple variants are present but the manifest does not explain their role, M1 is not ready because duplicate or conflicting source semantics are still unresolved.

## 19. Requirement-to-Evidence Traceability Matrix

| Requirement | Governing section(s) | Minimum execution evidence | Failure signal |
|---|---|---|---|
| manifest-generic scoping | §§8, 9, 13A | manifest file + anti-special-case review note | folder names are hardcoded or only one pilot bundle works |
| default/global path preservation | §§9, 10H, 11.2, 11.10 | unchanged global outputs + backcompat CLI/query evidence | dataset mode silently repoints the default/global path |
| scoped truth/freshness | §§9, 11.4, 17C | artifact metadata + upstream refs + freshness statement | stale dataset outputs are indistinguishable from current truth |
| bundle completeness honesty | §§9, 11.12, 17D | per-folder coverage table + incompleteness markers if needed | a missing folder or skipped input is hidden |
| scoped query correctness | §§10G, 11.6, 11.15, 17B | seeded query evidence from the selected snapshot | answers come from the wrong snapshot or lack provenance |
| thin-graph honesty | §§9, 11.14, 17D | connected-component / isolated-node / hit-rate metrics | a sparse graph is reported as full success |
| low-spec viability | §§10G, 11.21, 17E | `.ai/00_performance/` notes + bounded working-set observations | proof only works by assuming large RAM or whole-corpus loads |
| rollback/removability | §§9, 11.3, 17E | dataset-output removal/archive proof | global/shared artifacts need repair after scoped outputs are removed |
| fresh blast-radius control | §§5A, 7(M0), 10F | fresh impact analysis on the current commit | implementation starts from stale graph/intelligence context |

### Rule
If a requirement has no clear evidence artifact, the plan is not yet execution-grade for that requirement.

## 20. M1 Authorization / Sign-Off Checklist

M1 should remain blocked until the following sign-off questions can each be answered clearly.

| Reviewer lane | Sign-off question | Authorization condition |
|---|---|---|
| planning | Is the cut line still truly M1 and not a hidden M2/M3 widening? | deliverables stay within scoped build/query/export plus bounded truth inputs |
| audit | Are leakage, adjacency, freshness, and global-latest risks explicitly controlled? | pilot admission, artifact isolation, and stop conditions are all explicit |
| architecture | Is the design additive, generic, and still aligned with macro codebase reuse? | default/global behavior stays intact and no pilot-specialized branches are required |
| verification | Is there a concrete evidence package and validation surface for proving success/failure? | verification plan + surface map + evidence template are all sufficient and specific |
| performance | Can the slice be attempted honestly on an 8 GB-class machine without whole-corpus behavior? | low-spec budget and no-go conditions still hold |
| tooling/intelligence | Is the code-intelligence context fresh enough for safe impact analysis? | GitNexus freshness is restored on the then-current commit before any code edits |

### Rule
M1 may begin only when every required authorization row can be answered **yes** on the current commit, not on an older planning snapshot.

## 21. Negative Verification Matrix for Future M1 Work

Later implementation should not rely only on success-path checks. The first execution slice should also prove the expected failure behavior for the following cases.

| Negative scenario | Expected outcome | Why this matters |
|---|---|---|
| manifest references an out-of-scope adjacent law-family document without explicit admission | run is rejected or clearly flagged before proof claims success | prevents silent bundle widening |
| manifest contains multiple variants with no role metadata | run is rejected at validation/planning gate | prevents false equivalence across summary/illustrative/authoritative files |
| dataset mode attempts to read global `latest_relationship_*` | explicit failure or policy violation | protects truth boundary |
| dataset mode mutates default/global graph/query outputs | explicit failure | preserves additive rollout |
| snapshot/query points at a stale or mismatched manifest hash | explicit stale-output failure | preserves freshness honesty |
| graph passes integrity but has near-zero useful coverage | `PARTIAL` or `FAIL`, not silent success | enforces thin-graph honesty |
| low-spec execution requires broad whole-corpus loading | fail planning/execution gate | keeps the pilot aligned with the 8 GB-class budget |

### Rule
M1 validation is incomplete if it checks only the happy path and does not define what safe failure looks like for the major misuse cases.

## 22. Implementation Session Bootstrap Protocol

When a later session is authorized to implement M1, the first execution pass should follow this bootstrap sequence before any code edit is made.

1. read authority/state docs in the order defined by `AGENTS.md`
2. read the supporting audit, research pack, and this implementation plan
3. run `npx gitnexus status`
4. if stale, run `./scripts/gitnexus_analyze.sh`
5. re-check the M1 readiness gate, authorization checklist, and stop conditions on the **current commit**
6. confirm the pilot bundle admission checklist and variant/role policy are still explicit enough to drive a manifest
7. run fresh impact analysis on the likely touched symbols/modules
8. only then start the smallest M1 code slice

### First-edit rule
The first implementation edit should land in the narrowest control-plane surface that establishes scoped inputs/outputs, not in review/promotion truth-bearing code unless the M1→M2 trigger is actually hit.

### Bootstrap failure rule
If any bootstrap step fails, the session should stop and record the blocker rather than improvising around it.

## 23. M1 Change Budget / Touchpoint Budget

M1 should be attempted as a bounded additive slice, not a repo-wide refactor.

### Likely initial touchpoints
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/graph/builder.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/vitruvius/ontology/cli.py`

### Maybe-touch surfaces only if required by evidence
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/vitruvius/relationships_sections.py`
- targeted tests/fixtures needed to prove scoped behavior and default/global preservation

### Default do-not-touch budget
Unless evidence forces widening, M1 should avoid broad edits across:
- conversion batch wrappers
- refine batch wrappers
- canonicalization batch wrappers
- unrelated CLI commands
- unrelated graph/query/export features
- Rust crates or bindings

### Budget rule
If the first honest M1 slice appears to require broad cross-layer rewiring outside the touchpoint budget, that is evidence to stop and re-evaluate the milestone boundary rather than push through by momentum.
