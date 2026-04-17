---
task: laws-tranche-2-candidate-scout-worker-1
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche-2 Candidate Scout (Worker 1)

## Question
Which tranche-2 laws are the safest next bounded candidates from the current readiness evidence, and which laws should be excluded or deferred because of duplicate/quality risk?

## Evidence used
1. Fresh whole-laws readiness from repo root:
   - `006_System-Manifests/runs/datasets/laws-all-readiness/20260417T082529Z/all_laws_dry_run_report.json`
2. Fresh whole-laws duplicate readiness from repo root:
   - `006_System-Manifests/runs/datasets/laws-duplicate-readiness/20260417T082529Z/laws_duplicate_dry_run_report.json`
3. Temporary tranche-2 scout manifest checks (repo root):
   - duplicate dry-run: `006_System-Manifests/runs/datasets/laws-tranche-2-candidate-scout/20260417T082924Z/laws_duplicate_dry_run_report.json`
   - source-prep dry-run: `006_System-Manifests/runs/datasets/laws-tranche-2-candidate-scout/20260417T083014Z/laws_tranche_source_prep_dry_run_report.json`
   - tranche dry-run: `006_System-Manifests/runs/datasets/laws-tranche-2-candidate-scout/20260417T083245Z/laws_tranche_dry_run_report.json`

## Fresh corpus facts
- Whole-laws readiness still keeps generic Phase 11 expansion gated.
- The corpus has `47` discovered law folders and `43` inventory-only folders beyond the pilot.
- Only seven law folders currently show any produced-data inventory, and the three non-pilot ones are the existing tranche-1 laws (`PD-957`, `PD-1216`, `PD-1185`).
- Duplicate readiness still flags `EO`, `HLURB-DHSUD`, `LGU`, `PD-1096`, `PD-957`, `RA-7160`, and `RA-9266`.

## Safest tranche-2 scout candidates

### Recommended bounded scout set
1. `RA-7279` — Urban Development and Housing Act
2. `RA-4726` — Condominium Act
3. `RA-7899` — Amendments to RA 4726

### Why these three are the safest next scout set
- **Domain adjacency:** they stay close to the current housing / subdivision / condominium slice instead of widening into broad mixed-topic folders.
- **No current duplicate hit:** the temporary duplicate dry-run returned:
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- **Direct text-PDF route:** the temporary source-prep dry-run classified all three candidate PDFs as:
  - `detection_result = TEXT_PDF`
  - `recommended_route = OPENDATALOADER_DIRECT`
- **No existing structure guardrails:** the temporary tranche dry-run returned:
  - `structure_guardrail_law_folders = []`
- **Tight boundedness:** each folder currently contributes exactly one supported direct-input PDF, which keeps tranche prep/admission scope small and auditable.

## Exclude / defer list from duplicate-quality review

### Exclude from tranche-2 scout manifest now
- `HLURB-DHSUD`
  - heterogeneous guidebook/manual folder, not a clean single-law unit
  - cross-folder duplicate with `RA-7160` (`LCG of 1991.pdf`)
- `LGU`
  - highly heterogeneous city CLUP/zoning corpus rather than a single law unit
  - multiple duplicate clusters already present
- `EO`
  - folder contains multiple executive orders rather than one bounded law unit
  - duplicate file already present for EO 1008

### Defer until duplicate/alias cleanup is explicit
- `RA-9266`
  - exact duplicate pair with conflicting IRR filename semantics
- `RA-7160`
  - cross-folder duplicate with `HLURB-DHSUD`
- `PD-957`
  - already part of tranche-1 and still carries conflicting law-vs-IRR filename semantics
- `PD-1096`
  - already pilot-covered and still duplicate-heavy; not a tranche-2 widening candidate

## Interpretation
Current readiness evidence does **not** show any additional non-tranche produced-data-ready laws. That means the truthful next move is not immediate tranche-2 execution; it is a **manifest-backed scout tranche** whose first concrete step is source preparation / admission for a small, low-duplicate housing-adjacent set.

## Recommendation
If leadership wants the smallest safe tranche-2 follow-on, use a scout manifest built around:
- `RA-7279`
- `RA-4726`
- `RA-7899`

Then run, in order:
1. tranche duplicate dry-run
2. tranche source-prep dry-run
3. tranche source-prep execute
4. tranche source-admission dry-run

Keep generic all-laws expansion gated.
