---
task: laws-tranche-2-candidate-risk-audit
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche-2 Candidate Risk Audit

## Audit question

Which currently plausible tranche candidates carry **duplicate or quality risks**
strong enough to exclude or defer them?

## Scope of evidence reviewed

- whole-repo readiness snapshot:
  - `006_System-Manifests/runs/datasets/laws-all-readiness/20260417T055021Z/all_laws_dry_run_report.json`
- tranche duplicate screen:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/20260417T054921Z/laws_duplicate_dry_run_report.json`
- tranche source-admission dry-run:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065949Z/laws_tranche_source_admission_dry_run_report.json`
- tranche source-admission execute report:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065958Z/laws_tranche_source_admission_report.json`
- current explicit tranche manifest:
  - `config/datasets/laws-tranche-1.yaml`

## Candidate-by-candidate verdict

### 1) PD-957 — **defer unless duplicate/alias exclusions stay explicit**

Verdict:

- not a clean “drop in and go” tranche candidate
- safe only if the duplicate cluster remains explicitly collapsed and excluded

Why:

- the duplicate dry-run found **1 duplicate cluster** and it belongs to `PD-957`
- the cluster has **3 same-hash raw files**
- the cluster carries the semantic flag
  `conflicting_law_irr_filename_semantics`
- the later source-admission reports keep two raw files explicitly excluded and
  warn that aliases must still be reviewed before widening execution

Evidence:

- duplicate cluster entries:
  - `PD 957 - Subdivision _ Condominium Buyer_s Act.pdf`
  - `PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf`
  - `PD 957 IRR - Subdivision and Condominium IRR.pdf`
- duplicate hash:
  - `sha256 = 1f9ab17a816885cfdbafafc03e3e9b64470a737447129a32a459836d6773f9ea`
- source-admission guardrails:
  - `duplicate raw variants collapsed to one representative ...`
  - `same-content raw variants carry conflicting law/IRR filename semantics ... review aliases before widening execution`

Operational rule:

- if `PD-957` is selected, keep the IRR representative only
- keep the illustrated / buyer-protection variants explicitly excluded from
  canonical admission
- do not treat the folder as duplicate-clean

### 2) PD-1216 — **do not exclude on duplicate/quality grounds**

Verdict:

- currently the cleanest candidate on the duplicate/quality lane

Why:

- the latest source-admission dry-run shows:
  - `blocked_law_folders = []`
  - `admission_guardrails = []`
  - `excluded_duplicate_raw_paths = []`
  - `selected_from_duplicate_group_size = 1`
- the execute report confirms `PD-1216` is no longer carrying the earlier OCR
  blockage seen in older dry-run attempts

Important nuance:

- older tranche evidence did show `PD-1216` blocked for OCR-first handling
- that is now historical, not current

Operational rule:

- do **not** defer `PD-1216` based on duplicate or quality risk alone
- if it is skipped, the reason should be thematic prioritization, not data hygiene

### 3) PD-1185 — **defer if tranche-2 is supposed to maximize net-new signal**

Verdict:

- not blocked by duplicate hygiene
- still a reasonable **defer** candidate if tranche-2 should avoid overlap-heavy
  legal coverage

Why:

- `PD-1185` has no duplicate cluster and no admission guardrails
- but the current tranche manifest frames it as **fire-code adjacency**
- the same manifest notes that its concept-fit slice uses **existing shared
  concepts** to keep graph richness moving
- the bounded pilot already includes `RA-9514`, so the fire-code domain is
  already represented in the active baseline

Evidence:

- `config/datasets/laws-tranche-1.yaml`:
  - candidate reason: `Fire-code adjacency cited by BP-220 and relevant to safety overlap.`
  - scope note: `PD-1185 concept-fit slice admits existing shared concepts and dataset-scoped governs relationships only.`
- `laws-core-bundle-m1` already contains `RA-9514`

Operational rule:

- if tranche-2 wants the highest-confidence **non-overlapping** expansion, prefer
  `PD-1216` first and treat `PD-1185` as a follow-on or secondary candidate
- if the operator explicitly wants to deepen the fire-code lane, `PD-1185`
  remains acceptable

## Summary decision

### Exclude outright

None of the current candidates need full exclusion at the folder level based on
today's evidence.

### Exclude at variant level

For `PD-957`, keep these explicit exclusions:

- `001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision _ Condominium Buyer_s Act.pdf`
- `001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf`
- illustrated-study material should remain excluded from canonical truth-bearing admission

### Defer

- `PD-957` — defer unless duplicate/alias exclusions are preserved
- `PD-1185` — defer if tranche-2 should maximize net-new non-overlapping signal

### Keep

- `PD-1216` — cleanest current candidate on duplicate/quality evidence

## Bottom line

On duplicate/quality grounds alone, `PD-1216` is the safest tranche-2
candidate, `PD-957` is usable only with explicit duplicate/alias exclusions, and
`PD-1185` is better treated as overlap-heavy follow-on work than the clean first
pick.
