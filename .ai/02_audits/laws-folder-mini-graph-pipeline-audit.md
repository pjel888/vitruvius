---
task: laws-folder-mini-graph-pipeline
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — Laws-Folder Mini Graph Pipeline Feasibility

## Purpose
Audit whether Vitruvius can already output a knowledge graph for a sample dataset or one raw-source folder, and identify the true gap between current capability and a repeatable mini dataset→graph pipeline.

## What Was Inspected
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/conversion.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/relationships.py`
- `scripts/vitruvius/relationships_sections.py`
- `scripts/vitruvius/ollama_review.py`
- `scripts/vitruvius/ollama_review_second_pass.py`
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/query/cli.py`
- `README.md`
- archived Phase 8 / Phase 9 / upstream pipeline plans

## What Works Already
- Vitruvius can already output a graph snapshot and graph-adjacent outputs from the canonical layer.
- Single-file operator commands exist for the main upstream transformations needed to get one source into canonical and relationship form.
- A one-law or one-source pilot is therefore technically feasible today by manually chaining existing one-file commands and then running `build-graph`.

## What Does Not Exist Yet
- a dataset-scoped orchestration command or workflow
- dataset-scoped review/promotion artifacts
- dataset-scoped graph build root/output
- a clean way to pilot one folder without mixing outputs into the shared/global canonical layer

## Core Finding
The repo is **graph-capable already**, but **not yet mini-dataset-pipeline-shaped**. The missing piece is not graph primitives; it is scoped orchestration, artifact isolation, and a clean scaling path from one folder → per-section → interconnected global graph.

The immediate next step should therefore be an **audit of the path** before implementation:
- map the exact source→graph path
- measure the blast radius of a scoped pilot
- identify which changes are orchestration-only
- identify whether any future optimization candidates would legitimately belong in Rust

## Severity-Ranked Findings
- `HIGH` `build-graph` is whole-canonical-root only. A one-folder pilot currently requires shared-layer coupling or a new scoped root parameter/workspace.
- `HIGH` review/promotion depend on latest global run artifacts, which makes dataset-scoped execution unsafe and non-repeatable.
- `MEDIUM` batch commands (`refine`, `canonicalize`, `convert`) are whole-layer operations; single-file commands exist, but folder-level orchestration does not.
- `LOW` the repo already has enough graph/query/export code that the planning risk is orchestration and governance, not graph feasibility.

## Initial Blast Radius (M0 started)

### Directly implicated modules / commands
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/conversion.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/relationships_sections.py`
- `scripts/vitruvius/ollama_review.py`
- `scripts/vitruvius/ollama_review_second_pass.py`
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/vitruvius/ontology/cli.py`

### Why the blast radius is non-trivial
- upstream single-file commands exist, but review/promotion are still global-artifact based
- graph build and query surfaces are global-latest based
- a truthful scoped proof therefore crosses raw, conversion, canonical, relationship, promotion, graph, query, and docs/state boundaries

### Current optimization note
At audit time, the likely first implementation pressure is still orchestration and artifact routing, not compute. That means:
- the first optimization discussion should remain in Python/design space
- Rust should only enter later if M0 identifies a genuine hot path after the scoped design is mapped

## Detailed Blast Radius Table

| Surface | Why touched | Current coupling | Likely future change class | Risk |
|---|---|---|---|---|
| `pipeline_cli.py` | registration of future scoped commands/wrappers | global command defaults | CLI/orchestration | HIGH |
| `conversion.py` | reusable single-file entrypoint for dataset orchestration | raw-layer path based, batch-all-layer alternative exists | orchestration reuse | MEDIUM |
| `normalization/refine.py` | reusable single-file entrypoint plus batch-all-layer mode | whole-layer batch semantics | orchestration reuse | MEDIUM |
| `canonicalize.py` | converts refined markdown into shared canonical sources | writes directly to shared canonical layer | truth/governance boundary | HIGH |
| `relationships_sections.py` | likely extractor entrypoint for a scoped proof | global latest extraction artifact + NBCP/IRR-specific source IDs | truth/scoping | HIGH |
| `ollama_review.py` | tier-1 review for scoped candidate set | loads latest global extraction report | artifact isolation | HIGH |
| `ollama_review_second_pass.py` | tier-2 review | reads latest global tier-1 output | artifact isolation | MEDIUM |
| `promotion/__init__.py` | promotion into relationships | reads latest global high-confidence file and writes to shared canonical truth | truth/governance boundary | HIGH |
| `graph/cli.py` | actual scoped graph proof surface | whole shared root + global latest snapshot | graph scoping | HIGH |
| `query/cli.py` | user-visible scoped query proof | global latest snapshot only | query scoping | HIGH |
| `ontology/cli.py` | scoped TTL export proof | global latest snapshot/export path | export scoping | MEDIUM |
| tests under `scripts/tests/graph*`, `query*`, `run_promote`, `integration_e2e` | regression safety | current tests mostly assume global/shared behavior | regression cost | HIGH |

## Additional Findings
- The first truthful scoped proof likely needs a **query snapshot selector** at the same time as a scoped graph build, otherwise graph creation and graph consumption remain mismatched.
- The first truthful scoped proof likely needs an explicit **relationship input policy** (manifest-selected approved files or dataset staging inputs) before touching promotion code.
- The current 4-folder bundle is graph-useful, but still small enough that **performance is not yet the main problem**. The main problem remains generic scoping design.
- Bundle-boundary evidence is stricter than folder names alone suggest: a BP-344-adjacent document already exists outside `001-Laws/BP-344/`, so manifest membership must be explicit.
- Current code-intelligence context is not fully fresh: `npx gitnexus status` reports the index stale (`616c14a` indexed vs `e3c2bda` current), so any future code-edit phase must refresh impact tooling first.

## Recommended M1 Execution Slice Order
1. dataset manifest contract
2. dataset-specific output roots
3. scoped graph build surface
4. snapshot-selected/scoped query surface
5. safe relationship input policy
6. only then consider whether scoped review/promotion changes are required for the first proof
7. leakage / isolation / determinism / low-spec / anti-special-case verification

Why this order:
- it produces the smallest truthful graph proof first
- it avoids prematurely dualizing every upstream stage
- it keeps low-spec working-set control front and center
- it preserves the option to defer broader review/promotion scoping until it is proven necessary

## Edge-Case and Failure-Mode Register

1. **Manifest references files that do not exist downstream**
   - raw files exist, but conversion/refinement/canonical inputs are incomplete or mismatched
2. **Scoped graph with no approved relationships**
   - graph may technically build but be too thin to validate query usefulness
3. **Scoped graph/query mismatch**
   - dataset snapshot exists, but query surface still reads the global latest snapshot
4. **Scoped proof leaks shared truth**
   - manifest or graph root still admits unrelated shared canonical pages or relationships
5. **Scoped proof reuses stale dataset artifacts**
   - previous run outputs remain and are mistaken for current scoped truth
6. **Pilot-specialization drift**
   - code starts recognizing `PD-1096`, `RA-9514`, `BP-344`, `BP-220` by name instead of through manifest data
7. **Mixed maturity across bundle members**
   - one folder has stronger canonical/promoted coverage than others, yielding skewed graph density
8. **False confidence from small artifact size**
   - current artifacts are modest today, but the design still encourages duplication and global coupling that will scale poorly
9. **Low-spec working-set surprise**
   - a seemingly small pilot still triggers broad shared traversals or broad review/promotion reads
10. **Future merge incompatibility**
   - scoped artifact conventions for M1 make later per-section or merged graphs harder to reconcile

## Additional Team-Assisted Findings
- worker lane 2 confirmed the strongest current global couplings are:
  - `graph/cli.py`
  - `query/cli.py`
  - `promotion/__init__.py`
  - `relationships_sections.py`
- worker lane 2 also confirmed current artifact sizes are modest but non-trivial, supporting the low-spec argument for bounded outputs
- worker lane 3 confirmed the relevant CLI help surfaces resolve cleanly and an additional graph/query CLI test slice passed

## Open Design Decisions That Affect Blast Radius

1. **Manifest of files vs dataset-specific canonical root**
2. **Approved relationship allowlist vs dataset staging inputs**
3. **Scoped query selector form** (`--snapshot` first vs dataset-id first)
4. **Scoped export selector form**
5. **Artifact freshness semantics**
6. **Pilot gate semantics**

## Recommended Defaults for Those Decisions
- canonical and relationship scope → manifest allowlists first
- relationship source → approved/staged manifest-selected inputs, never global `latest_relationship_*`
- query selector → `--snapshot <path>` first
- export selector → snapshot-in + explicit out path
- freshness model → `dataset_id` + `run_id` + `manifest_hash` + `generated_at`
- pilot gate → strict checklist before coding

## Dataset Artifact Metadata Expectations

At audit time, the following metadata should be treated as required for future dataset-scoped outputs:
- `dataset_id`
- `dataset_kind`
- `run_id`
- `manifest_hash`
- `generated_at`
- input fingerprint summary
- upstream artifact references

This is the minimum needed to keep freshness, scope, and provenance auditable.

## Optimization / Rust Findings
- Immediate scoped-pilot work is overwhelmingly orchestration and artifact-selection logic, which belongs in Python.
- The only plausible future Rust candidates are downstream graph/traversal or extraction hot loops **after** the scoped design exists and is profiled.
- Therefore the audit currently recommends: **no Rust in the first execution slice** unless profiling later proves a real hot path.

## Low-Spec Constraint Finding
The user explicitly requires that the stack remain practical on an **8 GB M2-class machine**. This makes optimization a first-class planning concern, but it does **not** change the architecture boundary:
- first optimize by reducing scope, working set, and global coupling
- do not move orchestration/state/artifact-routing logic into Rust just to chase performance
- only consider Rust later if M0/M1 profiling shows a real hot path after the scoped design exists

At audit time, the best low-spec strategy is:
1. bounded manifest-scoped execution
2. bounded artifact outputs
3. minimal reprocessing
4. only then targeted compute optimization

## M1 Go / No-Go Readiness Check

Treat M1 as **NO-GO** until all of the following are explicit in the planning layer:
- manifest contract
- relationship input policy
- scoped query selection path
- artifact freshness semantics
- anti-special-case guardrails
- low-spec execution assumptions

If any of those remain fuzzy, the risk of pilot distortion or stale-output truth failure is still too high.

The audit also recommends adding a **planning-level low-spec execution budget** before M1 starts, so the first scoped proof is forced to stay bounded on an 8 GB-class machine.

## Recommended Outcome Rubric for M1

The audit recommends that future validation must force one of three judgments:

### SUCCESS
- scoped graph is valid, attributable, fresh, queryable, and bounded
- all four bundle members are represented or explicitly and acceptably deferred
- no global `latest_*` contamination occurred

### PARTIAL
- scoped graph is truthful but thin
- one or more bundle members are blocked/deferred with explicit reason
- the proof is real, but not yet strong enough to claim the full pilot objective

### FAIL
- wrong snapshot or wrong relationship inputs were used
- global latest artifacts were mutated or silently reused
- stale outputs could masquerade as current truth
- implementation is pilot-specialized or not low-spec viable by design

## M1 → M2 Boundary Recommendation

### Stay in M1 if:
- approved relationship inputs can be selected safely by manifest
- no dataset-scoped review outputs are required for the first proof
- no dataset-scoped promotion outputs are required for the first proof

### Expand into M2 if:
- the first proof requires new review outputs
- the proof requires promotion but the only available path still depends on global `latest_relationship_*`
- freshness/scope truth cannot be guaranteed without dataset-scoped review/promotion artifacts

### Defer after M1 success
- broader batch dataset wrappers
- broader all-laws support
- any Rust implementation work

## Coverage / Thin-Graph Reporting Recommendation

The audit recommends the future M1 validation log include:
- one per-folder coverage row for each of the 4 bundle members
- connected-component count
- isolated-node count or rate
- edge type diversity
- seeded query hit rate
- final `SUCCESS` / `PARTIAL` / `FAIL` judgment tied to those observations

## Assumption Stress Points

The current planning stack still rests on these assumptions:
- the 4-folder bundle is graph-useful enough to justify a first proof
- approved relationship inputs may be sufficient for the proof
- scoped query selection can remain additive
- scoped freshness semantics can be made unambiguous
- adjacent related law-family sources can be governed cleanly by explicit manifest membership instead of accidental folder expansion

The audit recommends treating each of these as an assumption that may be invalidated by later path-audit evidence rather than as a guaranteed fact.

## Pilot Bundle Admission Recommendation

Before M1 starts, the audit recommends an explicit pilot-bundle admission pass covering:
- exact include/exclude membership for `PD-1096`, `RA-9514`, `BP-344`, and `BP-220`
- explicit treatment of related out-of-folder documents, starting with the BP-344-adjacent DPWH order
- explicit note on whether multiple editions/variants within a folder are all in scope or selectively prioritized
- explicit per-folder expectation so sparse coverage is not mistaken for accidental failure

## Variant / Role Classification Recommendation

The audit recommends that pilot-manifest entries carry explicit role metadata because the current raw bundle already includes:
- authoritative-looking law texts
- revised rules/IRR variants
- summary-style materials
- illustrated/reference materials
- partial extracts

Without role metadata, M1 risks treating heterogeneous sources as interchangeable and overstating the truth quality of the first graph proof.

## Authorization / Sign-Off Recommendation

The audit recommends M1 remain blocked until all of the following are true:
- the cut line is still M1 and not hidden M2/M3 widening
- artifact isolation and default/global preservation are still additive
- freshness semantics are explicit
- low-spec budget remains credible for an 8 GB-class machine
- GitNexus freshness is re-established on the then-current commit before code edits begin

## Negative Verification Recommendation

The audit recommends future M1 validation explicitly cover at least:
- adjacent out-of-folder document admission failure
- missing variant-role metadata failure
- stale snapshot / stale manifest mismatch failure
- global `latest_*` policy-violation failure
- thin-graph downgrade from `SUCCESS` to `PARTIAL` / `FAIL`

## Bootstrap / Touchpoint Recommendation

The audit recommends that the first implementation session enforce both:
- a **bootstrap protocol** before any edit (authority read, GitNexus freshness, readiness re-check, impact analysis)
- a **touchpoint budget** so the first slice stays concentrated in graph/query/control-plane surfaces unless evidence forces widening

This lowers the chance that M1 turns into an uncontrolled cross-layer refactor on the first coding pass.

## Audit Verdict
**Feasible and worth planning now.**

The right plan is not “invent graph support” but “package the existing source→canonical→relationship→graph capability into a dataset-scoped pilot lane.” The user-preferred first useful pilot bundle is `PD-1096`, `RA-9514`, `BP-344`, and `BP-220`; before implementation, the safest next move is to audit the full path and blast radius first rather than jump directly into command/graph rewiring.
