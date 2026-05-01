# Laws tranche risk-hardening context

## Task statement
Minimize or eradicate the main remaining risks before any broader widening beyond the current bounded tranche success.

## Desired outcome
1. Reduce duplicate/raw-alias risk around PD-957.
2. Tighten OCR quality confidence around PD-1216.
3. Improve graph richness where the tranche is still thin.
4. Keep broader all-laws execute gated until these are addressed.

## Known facts
- Bounded tranche source-to-graph execute now succeeds for PD-957, PD-1216, and PD-1185.
- Current execute evidence:
  - generated_relationship_count = 2
  - filtered_relationship_count = 0
  - shallow_representation_count = 0
  - duplicate_law_folders = [PD-957]
- PD-957 still has duplicate/raw-alias complexity, though contained.
- PD-1216 OCR-first preparation now works, but OCR output still deserves quality hardening/spot-review.
- This remains a bounded tranche success, not generic all-laws execute.

## Primary risks to reduce
- PD-957 duplicate/raw-alias complexity
- PD-1216 OCR quality uncertainty (stamp/signature noise)
- modest graph richness / sparse relationship generation
- premature interpretation of tranche success as all-laws readiness

## Constraints
- Preserve bounded-slice discipline.
- No generic all-laws execute opening.
- Keep raw layer immutable.
- Prefer smallest safe, auditable changes.

## Likely touchpoints
- scripts/vitruvius/laws_readiness.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/vitruvius/ocr.py
- config/datasets/laws-tranche-1.yaml
- .ai planning/state docs
