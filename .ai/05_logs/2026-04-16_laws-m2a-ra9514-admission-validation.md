# 2026-04-16 Laws M2A — RA-9514 Admission Validation

## Outcome
- Verdict: **PARTIAL / PASS for first-law M2A slice**
- Slice executed: `RA-9514` first-law admission
- Scope status:
  - `RA-9514` admitted into the truth-bearing source layer
  - `BP-344` and `BP-220` remain pending / blocked for later M2A slices
  - M2B dataset-safe extraction/review/promotion work is still deferred

## What changed
### Truth admission steps performed
1. `detect-one` on `RA9514-RIRR-rev-2019.pdf` → `TEXT_PDF`, `OPENDATALOADER_DIRECT`
2. `convert-one '001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf'`
3. `refine-one '001-Laws/raw_markdown/RA-9514/RA9514-RIRR-rev-2019.md'`
4. Added explicit canonical rule coverage for:
   - `RA-9514`
   - `BP-220`
   - `BP-344` authoritative default variant
5. Fixed `canonicalize-plan-one` CLI argument mismatch so the preview command works again
6. `canonicalize-one '001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md'`
7. Updated the dataset manifest to admit the new `RA-9514` canonical source page
8. Rebuilt the scoped dataset graph with the updated manifest

## New / changed truth-bearing artifacts
- raw markdown: `002_Raw-Conversion-Layer/001-Laws/raw_markdown/RA-9514/RA9514-RIRR-rev-2019.md`
- sidecar json: `002_Raw-Conversion-Layer/001-Laws/sidecar_json/RA-9514/RA9514-RIRR-rev-2019.json`
- refined markdown: `002_Raw-Conversion-Layer/001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md`
- refined manifest: `002_Raw-Conversion-Layer/001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.refined.json`
- canonical source page: `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-fire-code-of-the-philippines.md`

## Scoped graph evidence
Latest dataset rebuild:
- snapshot: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T051110Z_graph_snapshot.json`
- integrity: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T051110Z_graph_integrity_report.json`
- report: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T051110Z_build_graph_dataset_report.json`
- manifest hash: `046a385321c10e52d5397ca9382d8827f3db8c8c5fd02de8d02861ab7fe3f6ce`

Coverage delta:
- `PD-1096` → still `covered`
- `RA-9514` → now `covered` with `canonical_count=1`, `node_count_contributed=1`, `edge_count_contributed=0`
- `BP-344` → still `blocked`
- `BP-220` → still `blocked`

Integrity result:
- `passed: true`
- `warning_count: 1`
- warning is the expected orphan source node for newly admitted `RA-9514` because no RA-9514 relationships have been generated/promoted yet

## Team-assisted planning evidence used in this slice
Focused OMX team `m2-admission-planning-assist-f` completed and produced three planning findings that informed this slice:
- worker-1 pinned RA-9514 / BP-220 IRR default titles, ids, and aliases
- worker-2 confirmed BP-344 authoritative/reference/adjacent policy
- worker-3 mapped the exact M2B global-latest dependency chain across extraction/review/promotion

## Verification
### Command checks
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/canonicalize.py scripts/vitruvius/graph/cli.py scripts/vitruvius/graph/dataset_manifest.py` → **PASS**
- `PYTHONPATH=scripts pytest -q scripts/tests/test_canonicalize_body.py scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_canonicalize_plan_cli.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_pipeline_cli_byte_identity.py` → **24 passed in 1.82s**
- `python3 scripts/pipeline_cli.py canonicalize-plan-one '001-Laws/raw_markdown/RA-9514/RA9514-RIRR-rev-2019.md'` → **PASS**
- `python3 scripts/pipeline_cli.py build-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml` → **PASS**

### Global path preservation
Global graph artifact hashes remain unchanged:
- `latest_graph_snapshot.json` → `da95cec5e676cb70bdaeb79e0c372fd6e50223c65fb3d7fa3cd69d3335cc0461`
- `latest_graph_integrity_report.json` → `3964821543ca4d13ba66d4a5fbfed19bac941c69e94e0795d034456d0f84952b`
- `latest_graph_snapshot.ttl` → `ff5ac797373eab42fded00cba2551096c7c3960e6ca4f3fa116f8c1cad371338`

## Remaining issues
- The newly admitted `RA-9514` source page is truth-bearing but still low-quality in its auto-generated overview/key-points section due image-heavy frontmatter and weak heading extraction in the source markdown.
- `RA-9514` has no admitted relationship inputs yet, so it is currently an orphan source node in the scoped graph.
- `BP-344` and `BP-220` remain outside the truth-bearing pipeline.

## Next truthful step
- Continue M2A with either:
  1. `BP-220` admission using the newly pinned rule default, or
  2. `BP-344` admission using the confirmed NCDA/DPWH/DO037 policy
- After at least one additional law admission, decide whether to keep extending M2A or begin the dataset-safe M2B extraction/review/promotion lane.
