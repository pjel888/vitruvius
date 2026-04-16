# 2026-04-16 Laws Mini Dataset M1 — Low-Spec Observations

## task / topic
Manifest-backed M1 scoped graph proof for the `laws-core-bundle-m1` dataset manifest.

## date
2026-04-16

## hardware context
- Planning target: **8 GB Apple M2-class machine**
- Observed on current local host via `/usr/bin/time -l`
- Caveat: the shell did not expose a full hardware fingerprint in-command, so the measured resource numbers below are host-local observations checked against the 8 GB M2-class budget rather than a claimed full machine spec

## workload description
- Command: `python3 scripts/pipeline_cli.py build-graph --dry-run --dataset-manifest config/datasets/laws-core-bundle-m1.yaml`
- Selected inputs: 54 manifest-selected truth-bearing files
  - 3 canonical source pages
  - 20 canonical concept pages
  - 31 approved relationship pages
- Raw validation anchors tracked: 4 folders (`PD-1096`, `RA-9514`, `BP-344`, `BP-220`)

## baseline
- Existing global graph path scans the shared canonical roots and writes global `latest_*` artifacts.
- M1 budget requirement: avoid whole-corpus/global-latest coupling for dataset mode and stay bounded enough for 8 GB-class hardware.

## current result
- Dry-run wall time: **0.21 s real**
- Peak memory footprint: **17,023,384 bytes**
- Maximum resident set size: **26,198,016 bytes**
- Scoped output size (non-dry-run reference run `20260416T041201Z`):
  - snapshot JSON: **77,640 bytes**
  - integrity JSON: **24,783 bytes**
  - Turtle export: **8,302 bytes**
  - build report JSON: **27,903 bytes**

## interpretation
- The M1 slice stayed bounded by the manifest-selected working set and did not require whole-corpus loading.
- Observed memory usage is comfortably inside the 8 GB-class planning budget.
- The largest cost increase versus the pre-M1 global snapshot is metadata richness, not graph size explosion.

## caveats
- The current pilot is still `PARTIAL`: only `PD-1096` contributes truth-bearing canonical/promoted inputs today; `RA-9514`, `BP-344`, and `BP-220` remain blocked and are reported as such.
- Determinism comparisons must normalize run-specific metadata fields (`run_id`, selected output paths, `generated_at_utc`) because dataset freshness linkage is intentionally explicit.
- No Rust work was introduced; optimization remains in Python/orchestration as planned.

## follow-ups
- If future manifests grow far beyond the current 54 selected inputs, re-measure with the same `/usr/bin/time -l` method before considering any widening.
- Revisit compute-level optimization only if manifest-bounded profiling shows a real hot path after M2/M3 scoping needs are proven.
