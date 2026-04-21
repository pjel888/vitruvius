---
task: control-surface-consolidation
phase: meta
created: 2026-04-21
author: Hephaestus
status: COMPLETE
---

# Control-Surface Consolidation Validation — 2026-04-21

## Scope

Validate the active-doc consolidation slice that:
1. slimmed the live AEC plan family to the master plan + session packet,
2. synchronized roadmap/state wording around that reduced active surface,
3. corrected repo-facing testing commands in `README.md`.

## Files validated

- `.ai/03_plans/INDEX.md`
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/active_context.md`
- `.ai/archive/ARCHIVE_INDEX.md`
- `README.md`

## Validation checks

### 1. Live-doc drift grep

Checked the active-doc surface for:
- stale `/docs/` references,
- missing `ready-family-aggregate.html` viewer references,
- invalid active-plan filename references.

Result: **no matches found in the targeted live-doc set**.

### 2. Standalone pipeline smoke checks

```bash
python3 scripts/test_odl_one.py
python3 scripts/test_pdf_text_detection.py "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

Results:
- `test_odl_one.py` completed successfully and generated OpenDataLoader output for PD 1096.
- `test_pdf_text_detection.py` classified the same PDF as `TEXT_PDF` with `4/5` sampled pages containing usable text.

### 3. Targeted pytest slice

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_graph_builder.py -q
```

Result:
- `27 passed in 0.57s`

## Interpretation

- The live planning surface is materially tighter and internally more consistent than before this slice.
- The public testing instructions now match repo-proven invocation patterns.
- No runtime regressions were detected in the validation slice exercised here.

## Next best move

Open a dedicated implementation packet for the live `ollama_review.py` runtime wiring gap:
- integrate `review_with_cache(...)` into the production review loop,
- then wire `select_review_model()` into the same path behind its feature gate.
