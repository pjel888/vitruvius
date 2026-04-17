---
task: laws-tranche-1-source-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche-1 Source Admission Research

## Question
After tranche-1 source preparation, what must happen before tranche-1 can safely enter source→graph dry-run and later execution?

## Fresh evidence
From the latest tranche-1 source-preparation execute report:
- command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-1.yaml`
- run id:
  - `20260417T022819Z`
- result:
  - `prepared_count = 5`
  - `ocr_required_count = 1`
  - `failed_count = 0`

Per-law state:
- `PD-957`
  - prepared: 4
  - OCR required: 0
- `PD-1185`
  - prepared: 1
  - OCR required: 0
- `PD-1216`
  - prepared: 0
  - OCR required: 1

## What this means
Tranche-1 is now partially produced-data-ready, but not uniformly source-admission-ready.

### Ready for admission review now
- `PD-957`
- `PD-1185`

### Not ready for admission review yet
- `PD-1216`
  - still requires OCR-first handling before it can join the tranche on equal footing

## Implication
The next truthful move is not tranche-1 source→graph execute.
The next move is a **tranche-1 source admission slice** that:
1. reviews the newly prepared tranche-1 produced-data outputs
2. decides which tranche-1 sources are eligible for canonical admission
3. records any exclusions / deferrals explicitly
4. treats OCR-blocked inputs separately rather than silently dropping them

## Recommended admission boundary
- tranche-1 source admission should proceed for the prepared `PD-957` and `PD-1185` documents only
- `PD-1216` should remain explicitly blocked until OCR-generated outputs exist and pass readiness checks

## Non-goal
- do not pretend tranche-1 is fully homogeneous
- do not silently exclude `PD-1216` from future tranche truth just because it is currently OCR-blocked
