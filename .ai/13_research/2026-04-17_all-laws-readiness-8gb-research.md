---
task: all-laws-readiness-8gb
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 All-Laws Readiness & 8GB Rollout Research

## Question
After the successful bounded 4-law pilot, what is the correct next step toward broader all-laws execution on a MacBook Pro M2 with 8GB RAM?

## Repo-local facts

### 1. Generic all-laws expansion is still gated
- `/.ai/01_roadmap/current-phase.md` states the laws lane is a **bounded pilot** only and any broader all-laws / merged-graph / section-scoped work needs a **fresh accepted slice**.
- `/.ai/01_roadmap/milestone-tracker.md` states Phase 11 generic expansion remains gated even though the bounded pilot succeeded.
- `config/datasets/laws-core-bundle-m1.yaml` explicitly says the manifest does **not** imply generic Phase 11 corpus expansion.

### 2. Current corpus size is much larger than the pilot
Repo-local counts from `001_Raw-Source-Layer/001-Laws`:
- top-level law folders: **48**
- PDFs: **183**

The accepted pilot uses only:
- `PD-1096`
- `RA-9514`
- `BP-344`
- `BP-220`

### 3. Current bounded source→graph review defaults are not 8GB-safe by default
`config/vitruvius.yaml` still sets:
- `review.ollama.default_model: gemma4:31b`
- `review.ollama.num_ctx_cap: 8192`
- `review.ollama.default_parallelism: 1`

`scripts/vitruvius/dataset_pipeline.py` also defaults the bounded source→graph lane to:
- `review_model = "gemma4:31b"`
- `review_timeout_seconds = 600`

### 4. The repo already contains an 8GB-hardening direction
Archived but still relevant guidance exists in:
- `/.ai/09_archive/plans/live-wiring-and-8gb-hardening-plan.md`

That plan already points toward:
- model-pool routing
- smaller default model on 8GB-class machines
- context-budget enforcement
- keeping heavier models for larger-memory hosts only

### 5. Current bounded pilot correctness baseline is good
Latest bounded pilot operator path is already verified:
- `run-laws-pilot` / `./run-laws-pilot`
- self-contained HTML browser artifact
- bounded source→graph dry-run and execute paths working

### 6. Current bounded pilot source-quality profile already identifies hard documents
The pilot trust reports consistently flag:
- `PD-1096 IRR`
- `RA-9514 RIRR`

as manual-review-required / high-severity inputs.

## Research conclusion
The correct next move is **not** to attempt a full all-laws source→graph execution on the current defaults.

The correct next move is:
1. create a whole-dataset readiness plan
2. introduce an 8GB-safe review preset
3. create an all-laws dry-run command path first
4. widen execution only in measured, accepted slices

## Recommended sequencing

### Stage A — readiness only
- all-laws dry-run path
- no LLM-heavy review
- no large execute run
- capture counts, selected law units, likely expensive stages, and artifact growth

### Stage B — 8GB-safe preset
- introduce an explicit small-model preset for bounded / exploratory large-scope runs
- preserve current higher-memory defaults for larger machines unless explicitly overridden
- keep the preset additive and opt-in at first

### Stage C — accepted widening slices
- widen by manifest and by batch
- keep graph/report outputs dataset-local
- re-measure after every scope increase

## Non-goal for this slice
- generic all-laws execute on 8GB with current `gemma4:31b` default
