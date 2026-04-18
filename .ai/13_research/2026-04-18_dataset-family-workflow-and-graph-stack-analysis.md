---
task: dataset-family-workflow-and-graph-stack-analysis
created: 2026-04-18
status: complete
---

# Research — dataset-family workflow and graph stack analysis

## Why this note exists

Recent work clarified that the repository's current laws effort is only one
instance of a broader repeatable pattern in Vitruvius: take a bounded family of
raw source material, run it through the deterministic pipeline, admit truthful
knowledge artifacts, and produce an inspectable graph surface.

This note records that pattern in a domain-agnostic way so future sessions can
reuse it not only for laws, but also for history, theory, utilities,
technology, structural, and future dataset families under
`001_Raw-Source-Layer/`.

It is intended to answer four questions for a future reader:

1. what is the actual larger goal?
2. what workflow keeps repeating?
3. what tech stack implements that workflow today?
4. what has already been accomplished, so we do not redo solved work?

## Parent objective

The larger task is not "make one graph HTML file." The larger task is to make
Vitruvius a **repeatable bounded dataset-family automation system**.

This means:

- prove that many dataset families can be staged, prepared, admitted, executed,
  and aggregated through the same manifest-backed automation pattern
- preserve machine-readable lane status so future sessions do not have to infer
  completion/disposition state from commit history or chat
- keep expansion truthful and bounded rather than pretending all corpus growth
  is automatically safe or already normalized

The laws-wave is the most developed current example of this pattern because it
has the richest artifact stack and the most complete tranche/remediation history.
It should be treated as the strongest reference implementation, not the only
intended target.

## Why the work feels repetitive

Yes, broadly the path from raw source layer to a knowledge graph is a
**repetitive workflow with variable judgment inside it**.

### The repeatable pattern

1. choose a bounded lane or family
2. inspect raw/source readiness
3. prepare raw files when needed
4. convert and refine text
5. canonicalize/admit authoritative source pages
6. admit concepts conservatively
7. admit relationships conservatively
8. run source-to-graph
9. inspect graph output
10. harden weak spots
11. roll the completed lane into a larger aggregate/disposition system

### What is repetitive

- the stage order
- the command/operator shape
- the artifact families produced
- the validation/reporting pattern
- the residual-hardening loop
- the aggregate synthesis pattern

### What is not fully repetitive

- OCR and layout problems
- source-quality issues
- duplicate/raw-alias handling
- truth-model corrections
- concept-fit gaps
- deciding whether a lane is executable, remediation-only, or final-disposition

So the process is repetitive, but not mindless. Vitruvius is evolving toward
turning more of the work into reusable machinery while leaving the truth and
judgment boundary explicit.

## What has already been accomplished

The important progress is not just "a graph exists." The repo now has a much
more complete reusable operating pattern than it did at the start of the laws
effort.

### Automation and operating surfaces already in place

- one-command family/operator paths exist
- dataset manifests are now first-class operating artifacts
- bounded source-prep, admission, source-to-graph, and aggregate flows exist
- graph snapshots, integrity reports, run reports, and HTML viewers are written
  deterministically as artifacts
- completed/disposition/provenance state can now be recorded outside chat

### Reusable family workflow already proven

The reusable path has already been proven on multiple families:

- laws
- history
- theory
- utilities
- technology
- structural

This matters because the repo is no longer proving only a single domain lane. It
has evidence that the broader family pattern is reusable.

### Laws-wave end-state already achieved

For the laws-wave specifically, the following have already been done:

- bounded pilot/core bundle execution
- tranche widening
- tranche richness follow-ons
- remediation-first lanes
- LGU sharding lanes
- PRC lane
- truth-model correction lanes
- remaining-pool final-disposition pass

In other words, a large amount of the difficult operationalization work has
already been performed. Future work should build on the artifact stack rather
than re-deriving this history manually.

## Generalized family workflow

For any dataset family, the durable mental model is:

### Layer progression

1. `001_Raw-Source-Layer/`
   - original PDFs, office docs, spreadsheets, scans
2. `002_Raw-Conversion-Layer/`
   - extracted markdown, OCR output, sidecar JSON
3. `003_Canonical-Knowledge-Layer/`
   - canonical source pages, concepts, relationships
4. `005_Operational-Intelligence-Layer/`
   - graph snapshots, integrity reports, indices
5. `004_Derived-Content-Layer/`
   - viewer HTML and other downstream inspection artifacts
6. `006_System-Manifests/`
   - run reports, registries, admission/provenance evidence

### Operational lane progression

1. inventory a bounded family
2. create or refine a manifest
3. prep or OCR raw files where needed
4. admit source pages truthfully
5. improve concept-fit
6. improve relationship-fit
7. run dataset source-to-graph
8. validate graph quality
9. aggregate completed lanes
10. record disposition/provenance so the lane can be resumed later

### Typical artifact flow produced by one bounded lane

For one lane, the normal artifact pattern is:

1. research note in `.ai/13_research/`
2. audit in `.ai/02_audits/`
3. plan in `.ai/03_plans/`
4. validation log in `.ai/05_logs/`
5. manifest changes under `config/datasets/`
6. canonical knowledge changes under `003_Canonical-Knowledge-Layer/`
7. run reports under `006_System-Manifests/`
8. graph artifacts under `005_Operational-Intelligence-Layer/`
9. optional HTML viewer under `004_Derived-Content-Layer/`

That artifact pattern is itself one of the key reusable outputs of the current
system.

## Core tech stack behind the repetitive workflow

The work is repetitive partly because the repo already has a fairly stable
technical stack and artifact contract.

### Control plane

- Python CLI orchestrator:
  - `scripts/pipeline_cli.py`
- core orchestration modules:
  - `scripts/vitruvius/`
- command style:
  - manifest-driven CLI commands
  - deterministic report-writing into `006_System-Manifests/`

### Configuration and operating metadata

- YAML manifests:
  - `config/datasets/*.yaml`
- catalog/profile metadata:
  - dataset family catalogs and MVP profile files
- machine-readable state ledgers:
  - completed lanes
  - remaining dispositions
  - source provenance
  - manifest indices

### Input and preprocessing

- PDF extraction and detection:
  - `pypdf`
  - `opendataloader_pdf`
- OCR:
  - `ocrmypdf`
- Office preprocessing:
  - LibreOffice / `soffice`
- spreadsheets:
  - `openpyxl`
- normalization/refinement:
  - internal Python refinement pipeline

### Canonicalization and admission

- canonical source generation:
  - internal Python canonicalizer
- concept/relationship admission:
  - manifest-backed and validator-backed Python pipeline
- truth model:
  - canonical > converted > raw
  - bounded, explicit, additive changes preferred

### Graph build

- graph snapshot generation:
  - internal Python graph build pipeline
- output artifacts:
  - graph snapshot JSON
  - graph integrity report JSON
  - build/run report JSON

### Aggregate synthesis

- aggregate manifests can now be synthesized from machine-readable lane ledgers
- family-ready aggregates can be built from catalog/profile status rather than
  only by hand
- aggregate-quality hardening can be driven from warning summaries and residual
  target lists instead of ad hoc graph inspection alone

### Visualization

- static viewer generator:
  - `scripts/vitruvius/graph/visualize.py`
- frontend library:
  - bundled `Cytoscape.js`
- frontend implementation:
  - static HTML + inline CSS + vanilla JavaScript
- graph data source:
  - one snapshot JSON per rendered graph

### Why the current visualization choice matters

The current visualization design is intentionally conservative:

- static output is easy to check in, diff, and reopen later
- one-file data sourcing keeps provenance simple
- snapshot-driven rendering preserves the boundary between graph truth and graph
  presentation
- the viewer is an inspection surface, not the source of truth

### Validation and regression safety

- unit/integration tests:
  - `pytest`
- TypeScript tests for related subprojects:
  - `npm test`
- Rust verification where relevant:
  - `cargo test`
  - `cargo fmt`
  - `cargo clippy`

## The laws-wave as the best current reference implementation

The laws-wave is currently the clearest evidence that the family workflow above
is real and reusable.

As of `/.ai/10_state/laws-wave-status.json` on 2026-04-18:

- `status = saturated_truth_complete`
- `raw_folder_count = 47`
- `covered_raw_folder_count = 41`
- `remaining_uncovered_folder_count = 6`
- `completed_lane_count = 25`
- `resolved_truth_model_fix_count = 2`

Truthful conclusion:

- no stronger normal primary-law / primary-regulation lane remains in the
  current source pool under the present authority and source-quality rules

### Why the laws-wave is the strongest current example

The laws-wave forced the repo to solve many of the hard reusable problems:

- duplicate/raw-alias handling
- OCR-first preparation
- concept-fit admission
- remediation-first lanes
- shard-based widening
- aggregate synthesis
- remaining-pool disposition recording
- source provenance correction

That makes it the best current teaching example for the general dataset-family
workflow, even though the workflow should not stay laws-only.

## What `ready-family-aggregate` actually is

`ready-family-aggregate` is **not** the whole mission.

It is the current **combined proving surface** for the larger family-automation
system, using the laws-wave as the most mature example:

- a multi-family aggregate graph built from the currently `ready` families
- a health dashboard for graph quality, cross-family interconnectedness, and
  residual hardening opportunities
- the best current broad graph to inspect when the goal is to understand the
  present admitted graph state

Current verified baseline:

- snapshot:
  `005_Operational-Intelligence-Layer/graph/datasets/ready-family-aggregate/20260418T023807Z_graph_snapshot.json`
- build report:
  `006_System-Manifests/runs/datasets/ready-family-aggregate/20260418T023807Z_build_graph_dataset_report.json`
- viewer:
  `004_Derived-Content-Layer/graph-visualizations/ready-family-aggregate.html`
- result:
  - `node_count = 143`
  - `edge_count = 266`
  - `warning_count = 1`
  - `covered_folder_count = 45`
  - `partial_folder_count = 1`
  - remaining truthful residual family: `RA-386`

## Artifact-stack pattern

The laws-wave has the most complete artifact stack right now, but the pattern is
general and should be copied for other dataset families as they mature.

### Current laws-wave artifact stack

These artifacts are the reusable memory of the larger lane and should be read
together when resuming the laws-wave:

- completed lanes:
  `config/datasets/laws-completed-lanes.yaml`
- remaining dispositions:
  `config/datasets/laws-remaining-dispositions.yaml`
- source provenance:
  `config/datasets/laws-source-provenance.yaml`
- manifest index:
  `config/datasets/laws-manifest-index.yaml`
- artifact index:
  `docs/LAWS_WAVE_ARTIFACT_INDEX.md`
- completion summary:
  `/.ai/05_logs/2026-04-18_laws-wave-completion-summary.md`

### Generalized artifact-stack idea

For any mature family, expect some version of:

- completed-lanes ledger
- remaining-dispositions ledger
- source-provenance ledger
- manifest index
- artifact index
- completion summary

These artifacts are the main reason future sessions should not need to replay
the whole family history mentally.

## Where the current graph viewer gets its data

For the specific file:

- `004_Derived-Content-Layer/graph-visualizations/ready-family-aggregate.html`

the graph data comes from one snapshot JSON file:

- `005_Operational-Intelligence-Layer/graph/datasets/ready-family-aggregate/20260418T023807Z_graph_snapshot.json`

The HTML embeds the snapshot JSON directly and also embeds a derived Cytoscape
`elements` object. The viewer library itself is separate from the graph data.

## Current graph-visualization stack

The current viewer is intentionally lightweight:

- Python generator:
  `scripts/vitruvius/graph/visualize.py`
- output:
  static HTML
- graph library:
  bundled `Cytoscape.js`
- UI:
  inline HTML/CSS/vanilla JavaScript
- data source:
  one snapshot JSON file per rendered view

Current viewer capabilities:

- search by node id/title
- click-to-focus neighborhood highlighting
- source/concept toggles
- simple layout switching
- label mode switching

This is good enough as a repo-native inspection surface, but it should be
understood as a lightweight static explorer rather than a full graph product.

## Important boundaries and non-goals

The workflow is strong precisely because it keeps boundaries clear.

### What the graph is

- an admitted, bounded, artifact-backed representation of current canonical
  knowledge
- an inspection and validation surface
- a way to see cross-family connectedness and weak spots

### What the graph is not

- not a dump of every term mentioned in raw documents
- not a substitute for canonical source truth
- not permission to invent stronger relationships
- not proof that a whole family is solved just because one HTML exists

### What should not be redone casually

- full repo-wide audits that have already been archived and reconciled
- earlier lane discovery that is already captured in the artifact stack
- solved truth-model fixes already recorded in completion/disposition artifacts

## Why this matters beyond laws

The important reusable conclusion is:

- laws gave the repo the clearest proof that the family workflow can scale
- the same workflow is intended to be reused for non-laws dataset families
- the exact manifests, heuristics, and truth rules will vary by family
- the lane shape, artifact shape, and graph inspection pattern are increasingly
  standardized

This is why it is better to think in terms of **dataset families** and
**bounded lanes** rather than "the laws project" as a one-off.

## Recommended resume logic for future sessions

Before doing new family-expansion work:

1. identify the family and bounded lane
2. identify the current artifact stack for that family
3. determine whether the task is:
   - lane execution
   - residual hardening
   - aggregate synthesis
   - disposition/provenance maintenance
   - generic automation improvement derived from prior family work

For laws specifically:

1. read `/.ai/10_state/laws-wave-status.json`
2. read `docs/LAWS_WAVE_ARTIFACT_INDEX.md`
3. read `/.ai/05_logs/2026-04-18_laws-wave-completion-summary.md`
4. decide whether the next task is:
   - residual hardening inside `ready-family-aggregate`
   - generic dataset-automation work derived from the laws-wave pattern
   - maintenance of the laws-wave artifact stack after opening a new lane

For non-laws families, use the same logic:

1. identify the family manifest/profile/catalog surfaces
2. identify whether the family already has a completed-lanes/disposition/provenance stack
3. identify whether the current task is lane execution, aggregate synthesis, or
   automation/framework improvement
4. avoid importing laws-specific assumptions when the family has different truth
   constraints

For the current bounded aggregate follow-on:

- the next truthful bounded step is to investigate whether `RA-386` can be
  improved using the same conservative mechanisms already proven in this lane:
  - explicit concept admission into manifests
  - canonical source-page refreshes that only mirror admitted concepts
  - aggregate rebuild + graph rebuild + warning-summary verification

## Bottom line

The work from raw source layer to knowledge graph is a repeatable operating
pattern. The repo is no longer at the stage where each lane is a bespoke
experiment. The bigger project is becoming a bounded dataset-family automation
system with reusable artifacts, and the laws-wave is currently the strongest
reference implementation of that system. `ready-family-aggregate` is the
current aggregate proving surface inside that broader pattern.
