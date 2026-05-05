# Live Plans Index

**Updated:** 2026-05-03
**Purpose:** identify which plan docs are still live, which are supporting reference, and which are archived/superseded

## 1. Active Plan Families

### 1.1 Planning-surface governance

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `00-governing-implementation-plan.md` | implemented | authoritative dispatcher for plan consumption order | keep as first-read document for plan work |
| `INDEX.md` | implemented | live inventory surface for active plans | keep aligned with `/.ai/IMPLEMENTATION_MATRIX.md` |
| `2026-05-03_source_grounded_kg_ai_program_plan.md` | active planning reference | reconciles the main product goal: source-grounded KG AI with graph reasoning plus real source/resource grounding | use with `/.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`; implementation requires dedicated packets |

### 1.2 AEC execution-readiness family

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | planned but gated | large AEC implementation family remains reference for future work, not an active execution lane | reopen only through a new dedicated gated packet or valid external authority |
| `2026-04-16-aec-first-slice-session-packet-plan.md` | blocked | minimal execution-readiness packet tied to the master AEC plan | keep blocked until runtime roots are explicitly verified in a new packet |
| `AEC-MEPFS-Backbone/` | active for bounded taxonomy, semantic enrichment, and resolver/query-path validation; production/protected gates remain blocked | standards-backed AEC-MEPFS Backbone planning packet that reframes KG work as authored backbone first, document classification second; file-backed runtime/Explorer default are implemented locally, all 24 taxonomy roots were deeply populated and scaffold-cleaned, targeted standards/topic semantic enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_targeted_taxonomy_semantic_enrichment_packet.md`, cross-domain semantic overlay enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_cross_domain_overlay_enrichment_packet.md`, LEA/ALE Philippine architecture licensure subject-domain enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_lea_ale_subject_domain_enrichment_packet.md`, and LEA/ALE resolver/utilities/structural deepening is validated through `AEC-MEPFS-Backbone/2026-04-29_lea_ale_resolver_deepening_packet.md`, and domain-cluster interrelationship enrichment is validated through `AEC-MEPFS-Backbone/2026-05-01_aec_mepfs_domain_cluster_interrelationships_packet.md` (run `20260501T040000Z_DOMAIN_CLUSTER_ENRICHMENT`, shadow run `20260501T040000Z_DOMAIN_CLUSTER_SHADOW`, graph quality `20260501T040000Z_GRAPH_QUALITY`, resolver QA `20260501T040000Z_DOMAIN_CLUSTER_RESOLVER_QA`, 9939 learner-facing graph nodes / 13459 relationships, 115 typed domain interrelationships, 124 resolver cases, 114 source-rights rows), and Architecture/Civil/Structural KG loop enrichment and gap closure are validated through `AEC-MEPFS-Backbone/2026-05-01_architecture_civil_structural_kg_loop_packet.md`, `docs/knowledge-graph/architecture-civil-structural-progress.md`, and `.ai/05_logs/2026-05-01_acs_gap_closure_validation.md` (initial run `20260501T050000Z_ACS_ENRICHMENT_PATCH_02`; gap closure enrichment `20260501T062000Z_ACS_GAP_CLOSURE`; post-cleanup idempotence `20260501T064500Z_ACS_GAP_CLOSURE_POST_CLEANUP`; shadow run `20260501T062700Z`; ACS quality `20260501T062900Z_ACS_GAP_CLOSURE_QUALITY_FINAL`; graph quality `20260501T062500Z_ACS_GAP_CLOSURE_GRAPH_QUALITY`; 10006 learner-facing graph nodes / 13610 relationships, 95 typed ACS interrelationships, 135 resolver cases, 123 source-rights rows, 0 self-loops) | continue only with bounded rights-safe taxonomy/relationship/resolver/source-overlay work unless a new gated packet provides production Neo4j, KG rebuild, protected ingest, or external authority |

### 1.3 KG-first cleanup planning

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `kg-first-cleanup/` | active Phase 2/3/4 final validation | safe cleanup/reframing pass for moving from a legacy layer-centered operating story to a KG-first source-evidence workflow without deleting source custody, evidence extraction, AEC-MEPFS runtime, or validation history | commit behavior-preserving CLI wording, adapter docstrings, and plan-surface reconciliation; do not delete/refactor legacy pipeline code until exact GitNexus no-caller proof and regression tests are attached |

### 1.4 Secondary cleanup

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `secondary-cleanup/` | transcript and duplicate skill-doc cleanup implemented; imported/reference packs deferred | demotes historical transcript material, archives stale duplicate skill docs, and records `.ai/skills/` as canonical without touching runtime behavior | optional later rewrite/archive pass for imported reference packs |

## 2. Supporting Reference Docs (Not Active Dispatchers)

These docs may be important, but they are **reference-only** unless a new active plan explicitly reopens them.

### Laws-wave reference stack
- `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- `.ai/03_plans/laws-wave/LAWS_WAVE_README.md`
- `.ai/03_plans/laws-wave/LAWS_WAVE_RELOAD_PROTOCOL.md`

### Completed governance / implementation references
- `2026-05-03_vitruvius_database_projection_architecture_plan.md` — planning reference for a future database-backed Vitruvius serving architecture: canonical custody in manifests/PostgreSQL, Memgraph as graph projection, and API in-memory compiled adjacency for the hottest graph read paths; not an authorization for live graph mutation, production promotion, Resource Layer mutation, or protected payload admission
- `2026-04-24_kg_relationship_contract_and_rule_label_plan.md` — non-blocking KG relationship/rule-label maintenance reference; future semantic relationship work should be governed by the AEC-MEPFS Backbone readiness gate
- `2026-04-24_explorer_shell_layout_cleanup_plan.md` — completed Explorer shell layout cleanup; inspector header alignment and minimize behavior are validated in component/integration tests
- `2026-04-24_ai_relationship_enrichment_pilot_plan.md` — completed Phase 5E candidate-generation pilot; full-corpus enrichment is a separate operator-enabled run/review activity
- `2026-04-15-nested-agents-governance-plan.md` — completed reference
- `2026-04-16-whole-codebase-plans-upgrade-plan.md` — completed reference
- `2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan_v2.md` — completed reference
- AEC planning burst docs other than the master plan + session packet (`2026-04-16-aec-*.md`, `AEC_ENGINE_*_IMPLEMENTATION_PLAN.md`) — reference-only until runtime kickoff is reopened
- explorer planning docs (`explorer-graph-rendering-implementation-plan.md`, `explorer-graph-rendering-rewrite-plan.md`, `vitruvius-explorer-phase-1-foundation.md`, `vitruvius-explorer-remediation-plan.md`) — completed reference
- tranche / laws-wave plan burst (`2026-04-17_*`, `2026-04-18_*`) — historical reference unless explicitly reopened

## 3. Archived / Superseded Docs

These are not live work.

- Everything under `/.ai/09_archive/`
- `2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan.md` → superseded by `2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan_v2.md`

See also: `/.ai/archive/ARCHIVE_INDEX.md`

## 4. Where New Planning Should Be Added

- Add new live plans in `/.ai/03_plans/` only when the work is genuinely active or blocked but still intended.
- Track cross-cutting product goals in `/.ai/14_project_management/` when they span roadmap, source custody, graph enrichment, retrieval, and validation.
- Put execution support artifacts in `/.ai/04_tasks/`.
- Put validation evidence in `/.ai/05_logs/`.
- Move completed or superseded plans to `/.ai/09_archive/` when safe, or record archive-in-place in `/.ai/archive/ARCHIVE_INDEX.md`.

## 5. Operating Rules For This Index

- If a plan is completed, it must not stay listed as active.
- If a plan is duplicated or superseded, only the current successor belongs in the active surface.
- If repository evidence does not support a plan claim, treat the plan as `unverified` or `obsolete` until reconciled.

### 2026-05-03 Source-Grounded KG AI Execution Acceleration
- `2026-05-03_source_grounded_kg_ai_execution_acceleration_plan.md` - execution-sequencing plan for API answer context, Explorer answer UI, database projections, Rust benchmark gates, and local/cloud AI acceleration.
- `2026-05-03_source_grounded_kg_ai_program_plan.md` - north-star reconciliation and program plan.
- `2026-05-03_vitruvius_database_projection_architecture_plan.md` - planning reference for file/manifest custody plus Postgres import-only prototype, Memgraph projection, and API-memory projections.
