---
task: ollama-review-runtime-wiring
phase: "05"
created: 2026-04-21
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Plan — Ollama Review Runtime Wiring

## Objective

Integrate the shipped stateful review wrapper into the live Tier-1 review loop while preserving current flag-off behavior and avoiding unrelated review-layer redesign.

## Execution target

### In scope for this plan

- `scripts/vitruvius/ollama_review.py`
- only the minimal supporting call path needed from the existing live loop
- directly related tests that prove Tier-1 runtime behavior

### Explicitly deferred

- replacing `_choose_tier_model(...)` with `select_review_model(...)`
- changes to `ollama_review_second_pass.py`
- prompt/schema redesign
- feature-flag default flips

## Planned changes

### 1. Make `_call_llm(...)` a production adapter

Implement `_call_llm(...)` as a thin wrapper around the current live review invocation path so `review_with_cache(...)` can reuse the production logic instead of a test-only placeholder.

Boundaries:
- no new network client
- no new retry logic
- no new output schema

### 2. Route the live loop through `review_with_cache(...)`

In `run_review_relationships_ollama(...)`, replace the direct `review_relationship(...)` call with a `review_with_cache(...)` path that:
- computes or obtains stable `source_hash`, `relationship_hash`, and `model_version`
- preserves current behavior when `y_stateful_registry` is false
- preserves the current report item shape appended to `reviews`

### 3. Keep model routing unchanged for Slice A

Do not change the `_choose_tier_model(...)` live-routing behavior in the same edit unless validation or code structure proves it is required.

## Risks

1. **Schema drift risk**
   - `review_with_cache(...)` currently returns a different shape than `review_relationship(...)`.
   - The implementation must normalize the result back into the live report-item shape.

2. **Hashing/input-identity risk**
   - cache keys must remain stable across reruns without accidentally collapsing distinct candidates.

3. **Blast-radius risk**
   - this runtime surface fans out broadly in the graph, so edits must remain surgical and validated immediately.

## Validation strategy

### Narrow-first

1. run the most specific unit tests covering:
   - `_call_llm(...)` / cache-wrapper behavior
   - stateful registry integration
   - explicit review input/output path handling

### Then broaden only if needed

2. Tier-1 review CLI-related tests
3. dataset-safe-stage tests touching `run_review_relationships_ollama(...)`
4. optional targeted py_compile if imports change across the review path

> Final exact test list will be tightened when the still-running test-map task returns.

## Exit criteria

- `review_with_cache(...)` is used by the live Tier-1 review loop
- flag-off behavior remains compatible with the current runtime path
- no placeholder `NotImplementedError` remains on the production cache path
- targeted validation passes

## Execution Checklist

- [x] inspect the exact live review item shape and normalize cache-wrapper output to match it
- [x] wire `_call_llm(...)` to the current production review path
- [x] replace the direct live call with a `review_with_cache(...)` path
- [x] run narrow tests
- [x] expand validation only if the narrow tests reveal adjacent breakage
