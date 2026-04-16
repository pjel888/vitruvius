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

## Audit Verdict
**Feasible and worth planning now.**

The right plan is not “invent graph support” but “package the existing source→canonical→relationship→graph capability into a dataset-scoped pilot lane.” The user-preferred first useful pilot bundle is `PD-1096`, `RA-9514`, `BP-344`, and `BP-220`; before implementation, the safest next move is to audit the full path and blast radius first rather than jump directly into command/graph rewiring.
