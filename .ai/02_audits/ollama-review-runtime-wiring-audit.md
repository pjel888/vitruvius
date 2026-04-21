---
task: ollama-review-runtime-wiring
phase: "04"
created: 2026-04-21
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Audit — Ollama Review Runtime Wiring

## Scope

Audit the live Tier-1 review runtime to determine whether shipped helper infrastructure (`review_with_cache`, `select_review_model`) is actually wired into production review execution, and bound the smallest safe implementation slice.

## Repo Evidence

### 1. Live entrypoints

- CLI path:
  - `scripts/pipeline_cli.py:1820-1833`
  - `review-relationships-ollama` dispatches directly to `vitruvius.ollama_review.run_review_relationships_ollama(...)`

- Dataset pipeline path:
  - `scripts/vitruvius/dataset_pipeline.py:1053-1063`
  - dataset source-to-graph review stage also calls `run_review_relationships_ollama(...)`

### 2. Cache wrapper status

- `scripts/vitruvius/ollama_review.py:115-127`
  - `_call_llm(...)` still raises `NotImplementedError`
  - docstring explicitly says it is intended to be patched in tests or wired by a follow-on integration

- `scripts/vitruvius/ollama_review.py:130-193`
  - `review_with_cache(...)` is fully implemented as a flag-gated wrapper around `_call_llm(...)`
  - flag-off path calls `_call_llm(candidate)` directly
  - flag-on path uses the stateful review registry keyed on `(source_hash, relationship_hash, model_version)`

### 3. Live review-loop behavior

- `scripts/vitruvius/ollama_review.py:878-1073`
  - `run_review_relationships_ollama(...)` loads the extraction report, triages, resumes progress, warms the model, and iterates candidates
  - for candidates that are not short-circuited by the prefilter, it currently does:
    - optional `_choose_tier_model(candidate)` when `w_review_slm_routing` is enabled
    - direct `review_relationship(candidate, model=per_candidate_model, timeout_seconds=timeout_seconds)`

### 4. Model-routing status

- `scripts/vitruvius/ollama_review.py:279-310`
  - `select_review_model(...)` exists as the Y2.4 MoE-aware model selector

- `scripts/vitruvius/ollama_review.py:313-341`
  - `_choose_tier_model(...)` exists as the older complexity-based SLM routing path

- `scripts/vitruvius/ollama_review.py:1017-1025`
  - live review loop uses `_choose_tier_model(...)` only
  - `select_review_model(...)` is not used in the production loop section audited here

### 5. Feature-flag baseline

- `config/vitruvius.yaml`
  - `w_review_slm_routing: false`
  - `y_domain_routing_moe: false`
  - `y_stateful_registry: false`

This means the shipped helper paths currently default OFF and must preserve existing flag-off behavior.

## Findings

1. **The runtime gap is real.**
   - Production Tier-1 review still bypasses `review_with_cache(...)` and calls `review_relationship(...)` directly.

2. **`review_with_cache(...)` is not production-safe yet as written.**
   - Its dependency `_call_llm(...)` is still an unimplemented placeholder.
   - Replacing the live call with `review_with_cache(...)` before wiring `_call_llm(...)` would break review execution.

3. **The MoE model selector is shipped but not live-default.**
   - `select_review_model(...)` exists, but the current live loop still routes only through `_choose_tier_model(...)` when routing is enabled.

4. **Blast radius is high.**
   - Code graph impact scan on likely runtime files reported a high-radius surface, so the implementation must avoid collateral architectural cleanup.

## Safest bounded implementation slice

### Slice A — Cache-wrapper integration

Bounded objective:
- make `_call_llm(...)` a thin production adapter around the current `review_relationship(...)` behavior
- integrate `review_with_cache(...)` into the live loop without changing flag-off semantics

Constraints:
- preserve current direct-review behavior when `y_stateful_registry` is false
- preserve current output shape expected by `save_progress_report(...)`
- do not redesign prompt building, retry policy, or second-pass review

### Slice B — MoE routing follow-on

Bounded objective:
- after Slice A, decide whether `select_review_model(...)` should replace or compose with `_choose_tier_model(...)`

Constraint:
- this should remain a separate sub-step unless the test map shows they are already coupled tightly enough to validate together

## Audit conclusion

- **Proceed** with a narrow plan for Slice A first.
- **Do not** combine cache integration and model-routing replacement in one unbounded edit.
- **Do not** touch second-pass review or review-layer architecture beyond the live Tier-1 loop.

## Next artifact

- `.ai/03_plans/ollama-review-runtime-wiring-plan.md`
