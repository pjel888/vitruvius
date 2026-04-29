# Live Plans Index

**Updated:** 2026-04-29
**Purpose:** identify which plan docs are still live, which are supporting reference, and which are archived/superseded

## 1. Active Plan Families

### 1.1 Planning-surface governance

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `00-governing-implementation-plan.md` | implemented | authoritative dispatcher for plan consumption order | keep as first-read document for plan work |
| `INDEX.md` | implemented | live inventory surface for active plans | keep aligned with `/.ai/IMPLEMENTATION_MATRIX.md` |

### 1.2 AEC execution-readiness family

| File | Status | Why it matters | Next concrete action |
|---|---|---|---|
| `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | planned but gated | large AEC implementation family remains reference for future work, not an active execution lane | reopen only through a new dedicated gated packet or valid external authority |
| `2026-04-16-aec-first-slice-session-packet-plan.md` | blocked | minimal execution-readiness packet tied to the master AEC plan | keep blocked until runtime roots are explicitly verified in a new packet |
| `AEC-MEPFS-Backbone/` | active for bounded taxonomy and semantic enrichment; production/protected gates remain blocked | standards-backed AEC-MEPFS Backbone planning packet that reframes KG work as authored backbone first, document classification second; file-backed runtime/Explorer default are implemented locally, all 24 taxonomy roots were deeply populated and scaffold-cleaned, targeted standards/topic semantic enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_targeted_taxonomy_semantic_enrichment_packet.md`, cross-domain semantic overlay enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_cross_domain_overlay_enrichment_packet.md`, and LEA/ALE Philippine architecture licensure subject-domain enrichment is validated through `AEC-MEPFS-Backbone/2026-04-29_lea_ale_subject_domain_enrichment_packet.md` (run `20260429T091500Z`, shadow run `20260429T092800Z`, 9403 nodes / 10979 relationships, 236 new LEA/ALE/source nodes, 65 improved nodes, 1193 new governed relationships, 79 source-rights rows) | continue only with bounded rights-safe taxonomy/relationship/source-overlay work unless a new gated packet provides production Neo4j, KG rebuild, protected ingest, or external authority |

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
- Put execution support artifacts in `/.ai/04_tasks/`.
- Put validation evidence in `/.ai/05_logs/`.
- Move completed or superseded plans to `/.ai/09_archive/` when safe, or record archive-in-place in `/.ai/archive/ARCHIVE_INDEX.md`.

## 5. Operating Rules For This Index

- If a plan is completed, it must not stay listed as active.
- If a plan is duplicated or superseded, only the current successor belongs in the active surface.
- If repository evidence does not support a plan claim, treat the plan as `unverified` or `obsolete` until reconciled.
