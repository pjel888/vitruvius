---
task: laws-folder-mini-graph-pipeline
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research Pack — Laws-Folder Mini Graph Pipeline

## 01 — Discover
The repo already ships a real graph pipeline, but it is shaped as a whole-canonical-layer graph builder rather than a dataset-scoped or folder-scoped orchestration flow. The planning question is therefore not “can Vitruvius output a graph at all?” but “what is the smallest truthful way to package the existing stages into a repeatable mini dataset→graph workflow for one laws folder, then scale it?”

## 02 — Existing End-to-End Surfaces

### Raw / conversion / refinement
From `scripts/pipeline_cli.py` and the backing modules:
- `scan`
- `convert`
- `convert-one`
- `refine`
- `refine-one`

Observed implementation shape:
- `run_convert_one(relative_pdf_path)` accepts an individual raw-layer file path.
- `run_refine_one(relative_markdown_path)` accepts an individual conversion-layer markdown path.
- batch `run_refine()` walks all `002_Raw-Conversion-Layer/**/raw_markdown/**/*.md`.

### Canonicalization / concepts
Commands and code paths:
- `canonicalize-plan-one`
- `canonicalize-one`
- `canonicalize`
- `canonicalize-concept-one`

Observed implementation shape:
- `run_canonicalize_one(relative_markdown_path)` works one file at a time.
- batch `run_canonicalize()` walks the whole conversion layer.

### Relationship extraction / review / promotion
Commands and code paths:
- `extract-relationships-one`
- `extract-relationships-sections-one`
- `review-relationships-ollama`
- `review-relationships-ollama-second-pass`
- `promote`

Observed implementation shape:
- extraction commands are one-file/one-markdown-path oriented.
- review loads the latest global extraction report.
- promotion loads the latest global high-confidence review report.
- these latest-report assumptions are the main blocker for dataset scoping.

### Graph snapshot / query / export
Commands and code paths:
- `build-graph`
- `query-graph`
- `export-graph-snapshot`
- `export-graph-owl`
- `query`
- `query-structured`

Observed implementation shape:
- `run_build_graph()` calls `build_snapshot(canonical_root)` where `canonical_root` is fixed to `003_Canonical-Knowledge-Layer/shared`.
- graph output is already real and queryable once canonical sources, concepts, and promoted relationships exist.
- graph/query are therefore downstream-ready, but not yet dataset-scoped.

## 02A — Initial Path Map (M0 started)

The currently observable source→graph path for a future scoped pilot is:

1. **Raw slice anchor**
   - `001_Raw-Source-Layer/001-Laws/<bundle>/...`
2. **Conversion**
   - `convert-one` / `run_convert_one(relative_pdf_path)`
   - outputs under `002_Raw-Conversion-Layer/.../raw_markdown/` + sidecars
3. **Refinement**
   - `refine-one` / `refine_one_inner(relative_markdown_path)`
   - writes `refined_markdown/...` + `.refined.json`
4. **Canonicalization**
   - `canonicalize-one` / `build_structured_source_file(relative_markdown_path)`
   - writes into `003_Canonical-Knowledge-Layer/shared/sources/`
5. **Relationship extraction**
   - `extract-relationships-sections-one`
   - currently reads one conversion-layer markdown path and writes a global latest extraction artifact
6. **Review**
   - `review-relationships-ollama`
   - currently loads the latest global extraction report
7. **Promotion**
   - `run_promote_inner()`
   - currently loads `latest_relationship_review_high_confidence.json`
   - writes into `003_Canonical-Knowledge-Layer/shared/relationships/`
8. **Graph build**
   - `run_build_graph()`
   - currently reads the whole `003_Canonical-Knowledge-Layer/shared`
   - writes `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json`
9. **Query / export**
   - `query`, `query-structured`, `query-graph`, `export-graph-owl`
   - currently read the global latest snapshot or write the global latest Turtle export

This confirms the main scoping problem: the repo already has the whole path, but the middle and downstream stages still collapse into shared/global artifact assumptions.

## 02B — Stage-by-Stage Coupling Table (M0 deepened)

| Stage | Primary command(s) | Primary function(s) | Main output(s) | Current scoping issue | Test surface |
|---|---|---|---|---|---|
| Raw inventory | `scan` | `scanner.run_scan` | `latest_raw_tree_snapshot.*`, `latest_raw_file_registry.csv` | global raw-layer snapshots only | scanner/status/lint tests indirectly; pipeline smoke |
| Conversion | `convert-one`, `convert` | `conversion.run_convert_one`, `run_convert` | `raw_markdown/*`, sidecar JSON, conversion registry | batch mode is whole-layer; no dataset run manifest | conversion tests, parser tests |
| Refinement | `refine-one`, `refine` | `refine.refine_one_inner`, `run_refine` | `refined_markdown/*`, `.refined.json` | batch mode is whole-layer; no dataset artifact namespace | refine/normalization tests |
| Canonicalization | `canonicalize-one`, `canonicalize` | `canonicalize.build_structured_source_file`, `run_canonicalize_one`, `run_canonicalize` | `003/shared/sources/*` | writes directly to shared canonical layer | canonicalize tests |
| Relationship extraction | `extract-relationships-sections-one` | `relationships_sections.run_extract_relationships_sections_one` | `006_System-Manifests/runs/latest_relationship_extraction_sections.json` | output is global `latest_*`; `build_source_id()` still NBCP/IRR-specific | extraction + Phase 5E tests |
| Tier-1 review | `review-relationships-ollama` | `ollama_review.run_review_relationships_ollama` | `latest_relationship_review_ollama.json`, `latest_relationship_review_high_confidence.json` | loads global latest extraction report; writes global latest review artifacts | review/stateful-registry tests |
| Tier-2 review | `review-relationships-ollama-second-pass` | `ollama_review_second_pass.run_second_pass_inner` | `latest_relationship_review_merged.json`, `latest_human_escalation_worklist.json` | still global-latest report chain | second-pass review tests |
| Promotion | `promote` | `promotion.run_promote_inner` | shared relationship files + `latest_promotion_audit.log` | reads global latest high-confidence review artifact; writes into shared canonical truth | promotion + integration tests |
| Graph build | `build-graph` | `graph.cli.run_build_graph`, `graph.builder.build_snapshot` | `latest_graph_snapshot.json`, `latest_graph_integrity_report.json` | whole shared canonical root only; global latest snapshot only | graph builder/integrity/CLI/backcompat tests |
| Query/export | `query`, `query-structured`, `query-graph`, `export-graph-owl` | `query.cli`, `graph.cli`, `ontology.cli` | formatted answers, `latest_graph_snapshot.ttl` | all read/write global latest snapshot/export paths | query/ontology CLI tests |

## 02C — Initial Blast Radius Summary (M0 deepened)

Directly implicated code roots for a truthful scoped graph proof:
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/conversion.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/relationships_sections.py`
- `scripts/vitruvius/ollama_review.py`
- `scripts/vitruvius/ollama_review_second_pass.py`
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/graph/builder.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/vitruvius/ontology/cli.py`

Directly implicated test roots:
- `scripts/tests/test_graph_builder.py`
- `scripts/tests/test_graph_cli.py`
- `scripts/tests/test_query_cli.py`
- `scripts/tests/test_query_engine.py`
- `scripts/tests/test_query_seed_accuracy.py`
- `scripts/tests/test_run_promote.py`
- `scripts/tests/test_integration_e2e.py`
- `scripts/tests/test_pipeline_cli_byte_identity.py`
- review / second-pass / phase-5e related tests

This is a **cross-layer orchestration blast radius**, not a single-module change.

## 02D — Formal Blast-Radius Matrix by Module

| Module / Surface | Stage | Why in blast radius | Current global/shared coupling | Expected scoped change class | Low-spec note | Rust candidacy |
|---|---|---|---|---|---|---|
| `scripts/pipeline_cli.py` | command registration | dataset-scoped wrappers or flags will likely be surfaced here | global/default commands only | orchestration / CLI routing | avoid duplicate convenience commands that trigger broad work | no |
| `scripts/vitruvius/conversion.py` | conversion | single-file entrypoint already exists; future dataset orchestration will reuse it | batch mode is whole-layer | orchestration reuse | keep per-file conversion, avoid whole-bundle eager processing if memory spikes | no |
| `scripts/vitruvius/normalization/refine.py` | refinement | single-file + batch flows both matter | batch mode walks whole conversion layer | orchestration reuse | prefer manifest-bounded refinement list over whole-layer traversal | no |
| `scripts/vitruvius/canonicalize.py` | canonicalization | turns refined markdown into canonical source pages | writes into shared canonical layer | truth/governance + scoping | avoid pilot-specific branches; may need staging/manifest control | no |
| `scripts/vitruvius/relationships_sections.py` | extraction | likely main extractor for scoped proof | writes `latest_relationship_extraction_sections.json`; NBCP/IRR-specific source IDs | truth/scoping | avoid broad section processing beyond manifest scope | maybe later only if extraction loops profile hot |
| `scripts/vitruvius/ollama_review.py` | tier-1 review | needed if scoped proof includes review path | reads latest global extraction report, writes latest global review artifacts | artifact isolation | global latest coupling is both truth risk and low-spec rework risk | no |
| `scripts/vitruvius/ollama_review_second_pass.py` | tier-2 review | follow-on review lane for scoped runs | reads latest global tier-1 output | artifact isolation | not first optimization target; first concern is scoped artifact selection | no |
| `scripts/vitruvius/promotion/__init__.py` | promotion | needed for truthful relationship inputs unless using staging | reads latest global high-confidence file; writes shared truth | truth/governance boundary | first proof may need explicit manifest-selected approved inputs to minimize work | no |
| `scripts/vitruvius/graph/cli.py` | graph build / graph query | actual proof surface for dataset graph | fixed shared canonical root + global latest snapshot paths | graph scoping | highest leverage low-spec win is bounded graph input/output | maybe later for larger graph workloads, not now |
| `scripts/vitruvius/graph/builder.py` | graph builder | source/concept/relationship walkers define graph breadth | whole shared root semantics | graph scoping / leakage control | manifest-bounded input set should reduce work and memory first | maybe later if profiling proves large-corpus hot path |
| `scripts/vitruvius/query/cli.py` | query | user-visible graph inspection path | global latest snapshot only | query scoping | snapshot selector likely required to avoid copying/overwriting global snapshot | no |
| `scripts/vitruvius/ontology/cli.py` | graph export | useful for human-inspectable output | global latest snapshot/export path | export scoping | dataset-specific Turtle export is a likely bounded output win | no |
| `scripts/tests/test_graph_*`, `test_query_*`, `test_run_promote.py`, `test_integration_e2e.py`, `test_pipeline_cli_byte_identity.py` | regression safety | scoped design must preserve default/global mode and add dataset-scoped behavior safely | many tests assume current global/shared defaults | regression + compatibility | tests are the main protection against pilot-specialization | no |

## 02E — Recommended M1 Execution Slice Order

1. **Define the dataset manifest contract**
   - make the first 4-folder bundle a manifest instance, not code logic
2. **Add dataset-specific output roots**
   - under `006_System-Manifests/runs/datasets/<dataset_id>/`
   - under `005_Operational-Intelligence-Layer/graph/datasets/<dataset_id>/`
3. **Add scoped graph build**
   - explicit dataset/root/output selection
   - no mutation of global latest snapshot
4. **Add snapshot-selected/scoped query path**
   - because graph proof without scoped query remains half-global
5. **Define safe relationship input policy**
   - manifest-selected approved relationship files or dataset staging
   - never global `latest_relationship_*`
6. **Only then consider whether M2 review/promotion scoping is necessary for the first proof**
   - if pre-existing approved inputs suffice for the proof, defer deeper review/promotion changes
7. **Run leakage, isolation, determinism, low-spec, and anti-special-case validation**

This order intentionally delays deeper upstream rewiring until after the smallest truthful graph proof surfaces are defined.

## 02F — Current Artifact Footprint Baseline

Fresh team-assisted inspection found that the current shared/global artifacts are still relatively small, but already large enough that duplicate broad rewrites matter on low-spec machines:
- `latest_graph_snapshot.json` ≈ **38 KB**
- `latest_relationship_extraction_sections.json` ≈ **96 KB**
- `latest_relationship_review_high_confidence.json` ≈ **37 KB**
- current shared graph footprint: **23 nodes / 30 edges / 6 orphan warnings / 0 errors**

Interpretation:
- the first problem is still scoping and artifact routing, not raw artifact size
- however, low-spec pressure will increase quickly if dataset mode duplicates broad `latest_*` artifacts instead of bounding them
- this supports the plan’s bias toward **manifest-bounded outputs** and away from whole-layer/global rewrites

## 03 — Evidence of Existing Graph Capability
- The repo already contains graph builder, integrity, traversal, query, and OWL export modules.
- The README documents the current operator ladder from extract/review/promote to graph/query.
- Archived Phase 8 and Phase 9 plans describe a filesystem-backed graph snapshot and structured query interface; much of that surface is now shipped.

## 04 — Scope Reality for a Pilot Dataset
A one-folder or one-law pilot is possible today in a manual/operator-driven sense because single-file commands already exist for the crucial upstream stages. However, it is not yet a clean productized “mini dataset→graph pipeline” because:
1. batch stages operate on the whole layer
2. latest-report review/promotion artifacts are global
3. graph build operates on the whole canonical shared root

## 05 — Raw Folder Evidence
The raw source layer already has a clear laws namespace:
- `001_Raw-Source-Layer/001-Laws/`
- many law-family subfolders including `PD-1096/`

Matching conversion subtrees already exist under:
- `002_Raw-Conversion-Layer/001-Laws/raw_markdown/...`
- `002_Raw-Conversion-Layer/001-Laws/refined_markdown/...`
- related sidecar / OCR / spreadsheet folders

This makes `001-Laws/PD-1096/` a strong first pilot target.

The user then widened the preferred first useful pilot bundle to:
- `PD-1096`
- `RA-9514`
- `BP-344`
- `BP-220`

Fresh filesystem evidence:
- `PD-1096` file count: **15**
- `RA-9514` file count: **1**
- `BP-344` file count: **2**
- `BP-220` file count: **1**
- there is already at least one BP-344-adjacent source outside the `BP-344/` folder:
  - `001_Raw-Source-Layer/001-Laws/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.pdf`
- `PD-1096/` is visibly variant-rich rather than edition-uniform, containing names such as:
  - `...Complete Scan.pdf`
  - `...Full Text (Malacanang Edition).pdf`
  - `...Illustrated (Pedro Santos Jr).pdf`
  - `...Summary.pdf`
  - `...Compact).pdf`
  - multiple `IRR` / `RIRR` files and partial rule extracts
- `BP-344/` also already shows variant/authority questions:
  - `2024 Revised Implementing Rules and Regulations ...`
  - `BP-344 IRR Accessibility Law DPWH.pdf`

This confirms the 4-folder bundle is materially richer than a 1–2 document pilot, but still quite small and bounded.
It also confirms that folder-name heuristics are insufficient; manifest membership must stay explicit.
It further confirms that file-role metadata is needed because bundle membership alone does not answer which variant is authoritative, supporting, summary-only, or excluded.

## 05A — Fresh Tooling Evidence
- `python3 scripts/pipeline_cli.py build-graph --help` → PASS
- `python3 scripts/pipeline_cli.py query --help` → PASS
- `python3 scripts/pipeline_cli.py promote --help` → PASS
- `python3 scripts/pipeline_cli.py extract-relationships-sections-one --help` → PASS

## 05B — Tooling Availability Note
`code-review-graph` MCP was **not available** as an MCP server in-session, so the path audit used:
- `omx explore`
- `npx gitnexus query`
- `npx gitnexus context`
- direct code inspection

Fresh GitNexus status evidence:
- `npx gitnexus status` → `Status: ⚠️ stale (re-run gitnexus analyze)`
- indexed commit: `616c14a`
- current commit: `e3c2bda`

That bundle is more graph-useful than a one-law proof, but it should still be treated as a **bounded pilot bundle**, not as proof that current extraction/query logic is already generic across all laws folders.

## 06 — Viable Planning Options

### Option A — Manual one-law operator recipe
Use existing one-file commands only and accept global artifacts.
- Pros: fastest path, minimal implementation
- Cons: not reproducible as a dataset-scoped pipeline, collides with latest global artifacts

### Option B — Dataset-scoped pilot workspace (recommended)
Introduce an explicit dataset manifest/workspace and dataset-scoped artifacts while reusing existing stage logic.
- Pros: clean pilot path, safe scaling to per-section and global graphs
- Cons: requires orchestration and artifact scoping work

### Option C — Whole-laws-folder immediately on shared canonical layer
Run the pilot directly against shared canonical outputs and whole-layer graph build.
- Pros: fewer moving parts
- Cons: mixes pilot and global truth too early, weak rollback/isolation

## 07 — Recommendation
Plan around **Option B**:
- use the **4-folder core-laws bundle** (`PD-1096`, `RA-9514`, `BP-344`, `BP-220`) as the first *useful* pilot target
- but make the *next step* an explicit **path audit** before implementation:
  - map the full source→graph path
  - identify the exact blast radius
  - identify optimization opportunities
  - triage whether any future hot-path pieces would legitimately belong in Rust
- create dataset-scoped manifests/artifacts/workspace outputs only after that path audit is complete
- reuse the existing stage implementations wherever possible
- defer truly global interconnected graph work until per-dataset graphs are stable and reproducible

## 08 — Fresh CLI Evidence
The following command surfaces are present and callable now:
- `python3 scripts/pipeline_cli.py build-graph --help`
- `python3 scripts/pipeline_cli.py query --help`
- `python3 scripts/pipeline_cli.py promote --help`
- `python3 scripts/pipeline_cli.py extract-relationships-sections-one --help`

This confirms the relevant orchestration surfaces already exist; the current planning gap is scope control, not command absence.

Additional team-assisted verification evidence:
- targeted graph/query pytest slice passed at **57 tests**
- additional graph/query CLI slice observed by a worker passed at **13 tests**
- `build-graph --dry-run` remains healthy on the current shared graph (`23` nodes / `30` edges / `6` warnings / `0` errors)

## 09 — Initial Optimization / Rust Triage

### Clearly Python / orchestration for now
- dataset manifest loading
- artifact scoping / path routing
- CLI wrapper/orchestrator work
- review/promotion artifact selection
- snapshot-selection query routing
- docs/state/reporting updates

These are control-plane tasks and should **not** move to Rust.

### Low-spec constraint now elevated
The user explicitly stated that the stack must remain viable on an **8 GB M2 MacBook Pro-class machine**. This changes the planning emphasis:
- reducing working set is a first-class goal
- bounded dataset manifests are not just truth/governance tools; they are also likely memory-control tools
- whole-layer traversals and global artifact rewrites are now both a truth risk **and** a low-spec performance risk

### Potential future hot-path candidates only if profiling proves it
- graph traversal / path-search on much larger merged graphs
- graph builder walk cost on significantly larger canonical corpora
- relationship extraction inner loops if large-scale section splitting + dedupe become dominant costs

### Current verdict
No immediate M0 finding justifies Rust work yet. The first problem is still **scope and artifact routing**, not compute bottlenecks.

### Practical low-spec opportunities already visible
- prefer manifest-bounded graph builds over whole-shared-root graph builds
- prefer dataset-specific query/export against selected snapshots over global latest snapshot dependence
- prefer scoped artifacts over global `latest_*` rewrites to reduce accidental broad reprocessing
- keep first execution slices small and composable before considering any deeper optimization work

### Additional low-spec note from team-assisted review
Even when artifact sizes are still modest today, low-spec pressure will come from:
- duplicated artifact generations across scoped and global lanes
- unnecessary whole-layer traversals
- broad review/promotion reuse of global `latest_*`

So the first low-spec optimization is still **scope control**, not compute specialization.

## 10 — M1 Decision Ledger (Recommended Defaults)

### Manifest shape
- Default: one dataset manifest per pilot bundle
- Recommended fields: `dataset_id`, `dataset_kind`, `raw_slice_anchors`, `canonical_input_manifest`, `relationship_input_manifest`, `graph_output_root`, `run_output_root`, `query_snapshot_path`, `freshness_policy`, `pilot_gate`

### Canonical input selection
- Default: explicit canonical allowlist, not a free-form root scan

### Relationship input policy
- Default: manifest-selected approved relationship files or dataset staging inputs only
- Explicit prohibition: never read global `latest_relationship_*` when dataset mode is requested

### Scoped query selector
- Default: `--snapshot <path>` first, `--dataset <dataset_id>` later

### Scoped export selector
- Default: `export-graph-owl --snapshot <path> --out <path>`

### Freshness model
- Default: outputs are fresh only when tied to exact `dataset_id` + `run_id` + `manifest_hash` + input fingerprint set

### Pilot gate
- Default: strict go/no-go checklist before coding

## 11 — M1 Readiness Rubric

M1 is ready to start only when:
- path map is explicit
- blast-radius matrix is explicit
- artifact coupling list is explicit
- manifest contract has recommended defaults
- freshness/selection contract is explicit
- scoped query selector choice is explicit
- anti-special-case rule is explicit
- low-spec constraints and likely working-set pressure points are documented
- no unresolved design choice remains that would force pilot-specific hardcoding

## 12 — Dataset Artifact Metadata Defaults

For future dataset-scoped outputs, the planning default metadata set should be:
- `dataset_id`
- `dataset_kind`
- `run_id`
- `manifest_hash`
- `generated_at`
- input fingerprint summary
- upstream artifact refs

This metadata set is the minimum needed to defend freshness, replayability, and scope truthfulness.

## 13 — Planning-Level Low-Spec Budget

Before M1 starts, the planning layer should explicitly record:
- expected working-set controls
- expected traversal bounds
- expected artifact-writing bounds
- no-go conditions if the proof still depends on whole-layer/global-latest behavior
