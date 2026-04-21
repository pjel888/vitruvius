---
task: ollama-review-runtime-wiring
phase: "09"
created: 2026-04-21
author: REVIEWER
supersedes: null
status: COMPLETE
---

# Validation — Ollama Review Runtime Wiring

## Scope

Validate Slice A only:
- `_call_llm(...)` is production-wired
- the live Tier-1 loop routes through `review_with_cache(...)`
- flag-off behavior remains compatible with existing review-path tests

## Files validated

- `scripts/vitruvius/ollama_review.py`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/dataset_pipeline.py`

## Commands run

### Narrow review-runtime test wave

```bash
PYTHONPATH=scripts python3 -m pytest \
  scripts/tests/test_config.py \
  scripts/tests/test_review_routing.py \
  scripts/tests/test_review_stateful_registry.py \
  scripts/tests/test_review_stateful_registry_vacuum.py \
  scripts/tests/test_review_stateful_registry_integration.py \
  scripts/tests/test_dataset_safe_stage_paths.py -q
```

Result:
- `41 passed in 1.19s`

### Direct review-module wiring checks

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_ollama_review_wiring.py -q
python3 -m py_compile scripts/vitruvius/ollama_review.py scripts/pipeline_cli.py scripts/vitruvius/dataset_pipeline.py
```

Results:
- `15 passed in 0.08s`
- `py_compile` passed with no output

## Observed behavior after the change

- `_call_llm(...)` is no longer a placeholder on the production cache path.
- `run_review_relationships_ollama(...)` now routes live candidates through `review_with_cache(...)`.
- Existing explicit input/output-path behavior for review artifacts remains green.
- Registry and routing tests remain green with current feature-flag defaults.

## Conclusion

Slice A passes the bounded validation pack and is safe to checkpoint independently.

## Follow-on

- Separate future slice: evaluate whether `select_review_model(...)` should replace or compose with `_choose_tier_model(...)` in the live loop.
