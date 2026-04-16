# 2026-04-16 Laws M2B — Dataset-Safe Stage Validation

## Outcome
- Verdict: **PASS for dataset-safe stage wiring; relationship admission still partial**
- Scope: add explicit dataset-safe path selection for:
  - extraction
  - review
  - second pass
  - promotion

## What changed
### New additive stage controls
- `extract-relationships-sections-one`
  - `--json-out`
  - `--txt-out`
  - `--source-id`
- `review-relationships-ollama`
  - `--input-report`
  - `--review-json-out`
  - `--review-txt-out`
  - `--triage-out`
  - `--high-confidence-out`
- `review-relationships-ollama-second-pass`
  - `--input-review-report`
  - `--merged-out`
  - `--worklist-out`
- `promote`
  - `--input-report`
  - `--relationships-out-dir`
  - `--audit-log-path`

### Code-level effect
These stages can now run in dataset mode without reading from or writing to global `latest_relationship_*` artifacts, while preserving current default/global behavior when explicit paths are not supplied.

## Fresh code verification
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/relationships_sections.py scripts/vitruvius/ollama_review.py scripts/vitruvius/ollama_review_second_pass.py scripts/vitruvius/promotion/__init__.py` → **PASS**
- `PYTHONPATH=scripts pytest -q scripts/tests/test_dataset_safe_stage_paths.py scripts/tests/test_run_promote.py scripts/tests/test_second_pass_orchestrator.py scripts/tests/test_high_confidence_writer.py scripts/tests/test_canonicalize_body.py scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_canonicalize_plan_cli.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_pipeline_cli_byte_identity.py` → **38 passed in 2.11s**

## Fresh runtime verification
### Dataset-safe extraction
Command:
- `python3 scripts/pipeline_cli.py extract-relationships-sections-one '001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md' --source-id irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines --json-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/extract.json --txt-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/extract.txt`

Observed result:
- dataset-scoped extraction artifacts written under dataset root only
- produced 2 candidate relationships
- no writes to global latest extraction artifact

### Dataset-safe review
Command:
- `python3 scripts/pipeline_cli.py review-relationships-ollama --input-report 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/extract.json --review-json-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/review.json --review-txt-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/review.txt --triage-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/triage.json --high-confidence-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/high_conf.json --timeout-seconds 120`

Observed result:
- triage, review, and high-confidence outputs written only to dataset-scoped paths
- both extracted candidates were auto-rejected by the deterministic pre-review filter
- `high_conf.json` count = `0`
- no writes to global latest review / high-confidence artifacts

### Dataset-safe second pass
Command:
- `python3 scripts/pipeline_cli.py review-relationships-ollama-second-pass --input-review-report 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/review.json --merged-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/merged.json --worklist-out 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/worklist.json`

Observed result:
- merged/worklist outputs written only to dataset-scoped paths
- second pass now skips synthetic `pre_review_filter` review items, so no false Tier-2 work is created when all candidates are deterministically rejected before LLM review
- no writes to global latest merged / worklist artifacts

### Dataset-safe promotion
Command:
- `python3 scripts/pipeline_cli.py promote --input-report 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/high_conf.json --relationships-out-dir 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/relationships --audit-log-path 006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514/promotion_audit.log --execute`

Observed result:
- promotion ran against explicit dataset-scoped input path
- no relationship files were created because `high_conf.json` was empty
- no writes to shared canonical relationships or global promotion audit log

## Global latest isolation check
Hashes before and after these M2B runtime checks remained unchanged:
- `006_System-Manifests/runs/latest_relationship_extraction_sections.json` → `6b147c395626faa34ab653c099801633920d8d578dc1c5e333d9ec6c89bc18e1`
- `006_System-Manifests/runs/latest_relationship_review_ollama.json` → `f659579c25a0ca2911f05f84ea3e608ca50dfeec41f40afd3bc7943ec8ada2a1`
- `006_System-Manifests/runs/latest_relationship_review_high_confidence.json` → `1d77877b24a43493d5da41653c25f4d3e6439f87062cede34abcf280f83143e4`
- `006_System-Manifests/runs/latest_relationship_review_merged.json` → `01c71a1ad0c0337d88f580fc5fb10088da95ca82249b19febb87db7079b0f6bc`
- `006_System-Manifests/runs/latest_human_escalation_worklist.json` → `256920fe91ea44ca0232e23f2fa39cbba8e43f786d724c6787f55bae467d9f74`
- `006_System-Manifests/runs/latest_promotion_audit.log` → `459fce9dd46066d0be197e5e1453df6389c55e5856b80da6e27846b09fbc8d00`

## Interpretation
- The dataset-safe M2B lane now exists and is additive.
- It is now possible to generate extraction/review/second-pass/promotion stage artifacts under dataset-specific roots without colliding with global latest state.
- Fresh re-verification under `architect-verify-ra9514-v2` confirms the lane can now also stage relationship files under a dataset-scoped root without touching shared/global artifacts:
  - extraction produced `27` candidates
  - review triage produced `3` auto-accept, `17` auto-reject, `7` LLM-routed candidates
  - second pass processed only the `7` real Tier-1 candidates (synthetic pre-review items were skipped)
  - dataset-scoped promotion created `3` relationship files under `006_System-Manifests/runs/datasets/laws-core-bundle-m1/architect-verify-ra9514-v2/relationships/`
  - global latest artifacts remained unchanged
- Relationship admission is still partial because those staged dataset-local relationship files have not yet been admitted into the shared/manifest relationship input set.

## Remaining work
- review and truth-admit the staged dataset-local relationship files that survive the bounded lane
- once admitted relationship files exist, add them to `relationship_input_manifest` and rerun the scoped graph to connect the new law nodes
