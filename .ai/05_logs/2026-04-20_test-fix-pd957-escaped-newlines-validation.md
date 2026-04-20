# Validation Report: PD-957 Test Fixture Newline Fix

**Date:** 2026-04-20  
**Commit:** `ab831ff`  
**Scope:** `scripts/tests/test_dataset_pipeline_cli.py`  
**Test:** `test_run_laws_tranche_source_admission_exec_collapses_duplicate_pd957_variants_and_keeps_blocked_laws`

---

## Problem

The test used `\\n` instead of `\n` in three `refined_payload` string literals:
- Line 1279: `'# REVISED IMPLEMENTING RULES AND REGULATIONS FOR PD 957\\n'`
- Line 1281: `'# PRESIDENTIAL DECREE 957\\n\\nStudy slides\\n'`
- Line 1288: `'# FIRE CODE OF THE PHILIPPINES\\n'`

This wrote literal backslash-n characters into the refined markdown fixtures. During canonicalization, `extract_title_from_content` included the trailing backslash in the extracted title, and `slugify` converted it to `-n`, producing filenames like `revised-implementing-rules-and-regulations-for-pd-957-n.md` instead of the expected `revised-implementing-rules-and-regulations-for-pd-957.md`.

## Fix

Replaced `\\n` with `\n` in the three affected strings so the fixtures contain actual newline characters.

## Validation

- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py::test_run_laws_tranche_source_admission_exec_collapses_duplicate_pd957_variants_and_keeps_blocked_laws -xvs` → **PASSED**
- Full suite: `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -x --tb=short` → **87/87 PASSED**

## Impact

- **Blast radius:** Zero — test-only change, no production code modified.
- **Risk:** None.
