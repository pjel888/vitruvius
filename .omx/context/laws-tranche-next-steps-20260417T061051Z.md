# Laws tranche next steps context

## Task statement
Advance from admitted tranche source-to-graph dry-run toward the next safe widening steps while reducing remaining risks.

## Desired outcome
1. Ground the OCR path for PD-1216.
2. Identify the shallow-representation issue from tranche source-to-graph dry-run.
3. Recommend or implement the smallest safe next slice without unlocking premature execute.

## Known facts
- Tranche-1 admitted source pages now exist for PD-957 and PD-1185.
- PD-1216 remains blocked pending OCR.
- Duplicate readiness now exists and PD-957 is flagged.
- Tranche source-to-graph dry-run stages PD-957 and PD-1185 only.
- Current live dry-run evidence:
  - planned_stage_count = 2
  - shallow_representation_count = 1
  - source_to_graph_execute_ready = false
- OCR stack present locally:
  - Python package: ocrmypdf installed
  - system binary: tesseract 5.5.2
  - CLI: ocrmypdf 17.4.1

## Constraints
- Generic Phase 11 expansion remains gated.
- Keep PD-1216 blocked until OCR-first preparation is truthfully ready.
- Use reporting-first, additive, conservative steps.
- No raw-layer mutation.

## Unknowns
- Which staged tranche law triggered shallow representation.
- Whether PD-1216 OCR can be run immediately with current stack or needs language/config setup.
- What the smallest safe post-dry-run slice should be.

## Likely touchpoints
- scripts/vitruvius/laws_readiness.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/vitruvius/ocr.py
- scripts/vitruvius/parsers/ocr_preprocessor.py
- config/datasets/laws-tranche-1.yaml
- 006_System-Manifests/runs/datasets/laws-tranche-1/source_to_graph_dry_run/20260417T060651Z/
