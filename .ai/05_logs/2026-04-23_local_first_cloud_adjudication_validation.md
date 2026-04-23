---
task: local-first-cloud-adjudication
phase: meta
created: 2026-04-23
author: Hephaestus
status: COMPLETE
---

# Local-First Optional Cloud Adjudication Validation — 2026-04-23

## Scope

Validate the bounded review-pipeline slice that adds an optional cloud adjudication pass for relationship review while preserving the local Ollama path as the default baseline.

## Files validated

- `config/vitruvius.yaml`
- `README.md`
- `scripts/vitruvius/config.py`
- `scripts/vitruvius/cloud_review_adjudication.py`
- `scripts/vitruvius/ollama_review.py`
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/tests/test_cloud_review_adjudication.py`
- `scripts/tests/test_run_promote.py`

## Validation checks

### 1. New cloud adjudication unit tests

```bash
python3 -m pytest scripts/tests/test_cloud_review_adjudication.py -q
```

Result:
- covered by combined targeted run below
- verifies escalation criteria
- verifies disabled no-op behavior
- verifies provenance-preserving override when cloud adjudication is enabled
- raw log saved to `/.ai/05_logs/2026-04-23_cloud-adjudication-pytest.log`

### 2. Existing review/config regressions

```bash
python3 -m pytest scripts/tests/test_cloud_review_adjudication.py scripts/tests/test_run_promote.py scripts/tests/test_ollama_review_wiring.py scripts/tests/test_ollama_config.py -q
```

Result:
- `36 passed`
- confirms the new cloud adjudication tests, Gemini provider routing, promotion provenance, and the existing review/config wiring all behave after the optional cloud layer was added
- raw log saved to `/.ai/05_logs/2026-04-23_cloud-adjudication-pytest.log`

### 3. Manual QA — config load / default local-first path

```bash
python3 -c "from vitruvius.config import get_cloud_review_settings; import json; print(json.dumps(get_cloud_review_settings(), indent=2, sort_keys=True))"
```

Result:
- normalized settings loaded successfully
- `enabled` defaults to `false`
- no API key is required for the default local-only path
- openai-compatible remains the default provider shape until explicitly changed
- raw output saved to `/.ai/05_logs/2026-04-23_cloud-adjudication-settings.json`

Observed output:

```json
{
  "api_base_url": "",
  "api_key": "",
  "api_key_env": "VITRUVIUS_CLOUD_API_KEY",
  "enabled": false,
  "high_value_occurrences_threshold": 3,
  "low_confidence_threshold": 0.9,
  "model": "",
  "prefer_adjudicated_decision": true,
  "provider": "openai_compatible",
  "timeout_seconds": 60
}
```

## Interpretation

- Vitruvius now supports a local-first plus optional-cloud review pattern without changing the default pipeline behavior.
- The local Ollama review path remains the baseline.
- Cloud adjudication is opt-in, selective, and provenance-preserving.
- Promotion gates still operate on the effective reviewed payload rather than bypassing governance.

## Manual QA — runtime adjudication exercise

Saved output:
- `/.ai/05_logs/2026-04-23_cloud-adjudication-runtime.json`

Observed outcome:
- a low-confidence, high-occurrence local review candidate was selected for cloud adjudication
- the cloud adjudication summary reported `selected_count: 1`
- the runtime path remained non-destructive even when the external call failed, recording `failed_count: 1` instead of breaking the local-first pipeline

## Manual QA — Gemini provider routing exercise

Observed output:

```json
{"decision":"keep","confidence":0.91,"reason":"gemini","suggested_type":null}
```

Interpretation:
- the Gemini provider branch is reachable through the shared cloud adjudicator interface
- provider-specific responses normalize back into the governed review JSON surface

## Promotion provenance checkpoint

- promotion no longer hardcodes `reviewer_model: gemma4:31b` for cloud-adjudicated records
- effective reviewer model/provider now flows through promotion evidence
- local review provenance is retained alongside the effective review decision for auditability

## Deferred follow-on

- No provider credentials are stored in the repo; real cloud runs still depend on operator-supplied environment variables.
- A future follow-on can add CLI flags or report-level artifacts specifically for cloud-adjudicated runs if operators want richer observability.
