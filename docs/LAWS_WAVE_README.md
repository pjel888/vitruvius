# Laws Wave README

This document is the human-facing top-level summary for the completed laws dataset expansion/remediation wave.

## Current state
The laws wave is in a **saturated truth-complete** state.

That means:
- actionable primary-law / primary-regulation lanes were executed
- known truth-model mismatches were corrected
- the residual uncovered pool was explicitly dispositioned
- no stronger normal executable law lane remains in the current source pool under the present standards

## One-command aggregate graph
Run the completed authoritative laws wave as one aggregate graph:

```bash
python3 scripts/pipeline_cli.py run-laws-completed-aggregate --review-preset m2-8gb-safe
```

For a planning-only pass:

```bash
python3 scripts/pipeline_cli.py run-laws-completed-aggregate --dry-run --review-preset m2-8gb-safe
```

## Core artifact stack
### Quick start
- `docs/LAWS_WAVE_RELOAD_PROTOCOL.md`
- `docs/LAWS_WAVE_ARTIFACT_INDEX.md`
- `.ai/10_state/laws-wave-status.json`

### Machine-readable ledgers
- `config/datasets/laws-completed-lanes.yaml`
- `config/datasets/laws-remaining-dispositions.yaml`
- `config/datasets/laws-source-provenance.yaml`
- `config/datasets/laws-manifest-index.yaml`

### Human-readable roll-ups
- `.ai/05_logs/2026-04-18_laws-wave-completion-summary.md`
- `.ai/05_logs/2026-04-18_remaining-pool-final-disposition-validation.md`

## What was completed
### Tranches
- core bundle / pilot
- tranche 1 through tranche 14

### Special lanes
- PRC professional-practice resolution lane
- RA-9266 remediation-first lane
- RA-9279 remediation-first lane

### LGU sharded lane
Completed shards include:
- San Mateo
- Dagupan
- Malolos
- Meycauayan
- Davao
- Tarlac
- QC-CBD / Ordinance No. 2117
- Pasay

## Key truth corrections
- HLURB and DHSUD are now treated as distinct agencies in tranche metadata, while preserving the legacy combined raw folder reality
- the `RA-9279` folder is no longer treated as if it contained RA 9279 statute text; it is resolved as the Section 18 RA 7279 IRR surface

## Remaining uncovered raw folders
- `BERDE`
- `HB-3391`
- `HB-5207`
- `RA-11361`
- `RA-7920`
- `SB-2982`

## Why they remain uncovered
Because they are currently only:
- draft-only
- bill-only
- empty
- or non-law/user-guide material

## Reopening rule
Do not reopen the laws wave just because a source is text-readable.

Reopen only when there is:
- a genuinely authoritative enacted law
- a final IRR / final regulatory issuance
- a primary government resolution / board issuance
- or another source with comparable authority and finality

## Branch
- `ralph/laws-dataset-phases`
