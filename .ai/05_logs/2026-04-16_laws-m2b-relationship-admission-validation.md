# 2026-04-16 Laws M2B — Relationship Admission Validation

## Outcome
- Verdict: **PARTIAL**
- Scope: dataset-safe relationship admission after M2A source admission

## What was proven
### Dataset-safe staging works
The extraction → review → second-pass → promotion lane can now run entirely under dataset-scoped paths without mutating global `latest_relationship_*` artifacts.

### Extraction quality improved materially
After improving section splitting to recognize markdown-prefixed section headings and numbered all-caps headings:
- `RA-9514` extraction produced `372` sections and `23` candidate relationships
- `BP-220` extraction produced `47` sections and `3` candidate relationships
- `BP-344` extraction produced `5` sections and `3` candidate relationships

### RA-9514 relationship admission succeeded conservatively
Using the improved extractor and dataset-safe M2B lane:
- `RA-9514` dataset-scoped review produced:
  - `auto_accept = 4`
  - `auto_reject = 14`
  - `needs_review = 5`
  - `high_confidence = 4`
- four staged promotion files were produced under:
  - `006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-ra9514-v2/relationships/`
- manual audit kept only **2** of those staged relationships as sufficiently trustworthy for official manifest admission:
  - `...governs-concept-certificate-of-occupancy`
  - `...governs-concept-means-of-egress`
- two staged relationships were **not** admitted because they were too weak/suspect for official truth:
  - `...governs-concept-yards`
  - `rel-concept-means-of-egress-requires-concept-occupancy-classification`
- human review was completed for the 2 non-admitted staged relationships:
  - `...governs-concept-yards` → **reject**
  - `rel-concept-means-of-egress-requires-concept-occupancy-classification` → **defer**
- human review ingestion log:
  - `/.ai/05_logs/2026-04-16_ra9514-human-review-ingestion-validation.md`

## Current official scoped graph state
Latest official scoped graph build:
- snapshot: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T055624Z_graph_snapshot.json`
- integrity: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T055624Z_graph_integrity_report.json`
- report: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T055624Z_build_graph_dataset_report.json`

Coverage summary:
- `PD-1096` → `covered`
- `RA-9514` → `covered` with `approved_relationship_input_count = 2`, `edge_count_contributed = 2`
- `BP-344` → `partial`
- `BP-220` → `partial`

Integrity summary:
- `passed: true`
- remaining orphan warnings: `BP-220`, `BP-344`
- `RA-9514` is no longer orphaned in the official graph

## Fresh verification evidence
### Regression / code safety
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/canonicalize.py scripts/vitruvius/relationships_sections.py scripts/vitruvius/ollama_review.py scripts/vitruvius/ollama_review_second_pass.py scripts/vitruvius/promotion/__init__.py scripts/vitruvius/graph/builder.py` → **PASS**
- `PYTHONPATH=scripts pytest -q scripts/tests/test_relationships_sections_split.py scripts/tests/test_dataset_safe_stage_paths.py scripts/tests/test_graph_builder.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_canonicalize_body.py scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_canonicalize_plan_cli.py scripts/tests/test_high_confidence_writer.py scripts/tests/test_second_pass_orchestrator.py scripts/tests/test_run_promote.py scripts/tests/test_pipeline_cli_byte_identity.py` → **69 passed in 2.32s**
- `git diff --check` → **PASS**

### Global latest isolation
Hashes remained unchanged after dataset-safe stage runs:
- `latest_relationship_extraction_sections.json` → `6b147c395626faa34ab653c099801633920d8d578dc1c5e333d9ec6c89bc18e1`
- `latest_relationship_review_ollama.json` → `f659579c25a0ca2911f05f84ea3e608ca50dfeec41f40afd3bc7943ec8ada2a1`
- `latest_relationship_review_high_confidence.json` → `1d77877b24a43493d5da41653c25f4d3e6439f87062cede34abcf280f83143e4`
- `latest_relationship_review_merged.json` → `01c71a1ad0c0337d88f580fc5fb10088da95ca82249b19febb87db7079b0f6bc`
- `latest_human_escalation_worklist.json` → `256920fe91ea44ca0232e23f2fa39cbba8e43f786d724c6787f55bae467d9f74`
- `latest_promotion_audit.log` → `459fce9dd46066d0be197e5e1453df6389c55e5856b80da6e27846b09fbc8d00`

## Interpretation
- M2B stage wiring is operationally real and no longer just plumbing.
- One newly admitted law (`RA-9514`) is now connected into the official scoped graph through a conservative dataset-safe relationship admission path.
- The overall milestone remains **PARTIAL** because `BP-220` and `BP-344` are still source-admitted but relationship-thin.

## Next truthful step
- continue conservative relationship auditing / extraction-quality improvement for `BP-220` and `BP-344`, or
- stop and report the current bounded milestone truthfully:
  - `PD-1096 = covered`
  - `RA-9514 = covered`
  - `BP-344 = partial`
  - `BP-220 = partial`
