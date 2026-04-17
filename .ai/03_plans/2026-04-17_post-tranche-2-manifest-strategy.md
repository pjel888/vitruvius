---
task: post-tranche-2-manifest-strategy
created: 2026-04-17
author: worker-3
status: DRAFT
---

# Post–tranche-2 manifest strategy

## Goal
Define the safest broader manifest strategy **after** tranche-2 scouting without reopening a generic all-laws execute path.

## Current evidence snapshot

### Repo-wide readiness baseline
From `006_System-Manifests/runs/datasets/laws-all-readiness/20260417T082529Z/all_laws_dry_run_report.json`:
- 47 law folders discovered
- 43 remain inventory-only
- 9 duplicate clusters are still present
- 5 folders trigger structure guardrails: `BP-220`, `BP-344`, `PD-1216`, `PD-957`, `RA-9514`
- only 11 refined-markdown artifacts exist repo-wide, so broader widening is still source-readiness constrained

### Tranche-2 scout baseline
From `006_System-Manifests/runs/datasets/laws-tranche-2-candidate-scout/20260417T083245Z/laws_tranche_dry_run_report.json` and `20260417T083525Z/laws_tranche_source_prep_dry_run_report.json`:
- current tranche-2 scout members are `RA-7279`, `RA-4726`, and `RA-7899`
- all 3 have raw PDFs present
- all 3 are still `not-ready` for graph widening because refined markdown, admitted sources, concepts, and relationships are all zero
- duplicate scout for this slice returned zero duplicate clusters
- source-prep dry-run recommended `OPENDATALOADER_DIRECT` for all 3 files

## What tranche-2 evidence implies
Tranche-2 is a good **scout + source-prep candidate slice**, but not yet a source-to-graph slice.

That means the safe broader strategy is:
1. keep tranche manifests explicit and sibling-scoped
2. advance raw-only scout tranches into source-prep/admission first
3. keep graph execute gated until a tranche has truthful source-admission evidence

## Recommended post–tranche-2 tranche taxonomy

### Wave A — single-statute scout tranches
Use this shape for folders that currently look simplest:
- one apparent authoritative PDF
- no known duplicate-cluster pressure in the current readiness report
- no structure-guardrail warning yet
- bounded legal/theme adjacency

Why: these are the cheapest candidates to move from inventory-only into source-prep truthfully.

Examples from the current raw corpus that fit the *shape* better than multi-file families:
- `PD-1517`
- `RA-4566`
- `RA-11285`
- `RA-9003`
- `RA-10066`
- `RA-6969`

These should still go through scout -> duplicate dry-run -> source-prep dry-run before any admission work.

### Wave B — paired law/IRR or amendment tranches
Use a separate manifest family for folders that already show likely pairing or version-selection work.

Why: they are still bounded, but they need authoritative-variant choice before admission.

Examples:
- `RA-11201` (law + IRR pair)
- `PD-1067` (law + IRR variants)
- `RA-9266` (duplicate/IRR-semantic risk already visible)
- `RA-9184` (multiple law/IRR files)

Rule: do **not** mix these with Wave A single-statute manifests.

### Wave C — complex normalization/backlog tranches
Treat large multi-file folders and collections as normalization programs, not normal tranche members.

Why: folder-level manifests are too coarse when a directory contains many aliases, editions, or unrelated operational documents.

Examples from current readiness/duplicate evidence:
- `PD-1096` (multiple duplicate clusters + law/IRR semantic conflicts)
- `HLURB-DHSUD`
- `LGU`
- `UAP`
- `EO`
- `BP-344`
- `RA-9514`

Rule: these need file-level curation or sub-manifests before they should ever join a standard scout tranche.

## Ordering recommendation

### 1. Finish tranche-2 as a source-prep/admission experiment
Do not open a new graph tranche yet. The current evidence says tranche-2 should next prove:
- source-prep outputs exist
- refined markdown is truthful
- source admission can stay conservative
- condo/housing slice remains duplicate-clean

### 2. Expand with more Wave A scout manifests
After tranche-2 source-prep/admission evidence is good, widen using additional Wave A single-statute scout manifests.

This preserves:
- small blast radius
- low duplicate ambiguity
- low memory/operator overhead
- easy rollback when a folder turns out to be noisier than expected

### 3. Open a dedicated Wave B paired-law lane
Only after Wave A continues to behave predictably should the repo widen into paired law/IRR manifests.

This should remain a separate lane because the main risk is no longer raw existence but authoritative selection.

### 4. Keep Wave C out of normal tranche rotation
Do not let complex folders pressure the tranche queue into becoming a disguised all-laws execute path.

If a folder needs sub-selection first, create a normalization/scout artifact for that folder instead of forcing it into a standard tranche manifest.

## Manifest design rules to preserve
- Keep `phase_11_gate: gated` on every new tranche manifest.
- Prefer explicit law-folder membership over directory sweeps.
- Preserve one readiness truth per tranche stage: scout, source-prep, source-admission, then source-to-graph.
- Do not mix single-statute folders, paired law/IRR folders, and collection folders in the same tranche.
- Promote a tranche only when the previous stage has written truthful artifacts, not when a raw PDF merely exists.

## Bottom line
After tranche-2, the safest broader strategy is **not** “tranche-3 = more laws.”
It is:
1. finish tranche-2 source-prep/admission truthfully
2. widen next through more **Wave A single-statute scout manifests**
3. reserve **Wave B** for paired law/IRR selection work
4. quarantine **Wave C** complex collections behind separate normalization artifacts

That keeps expansion additive, reversible, and manifest-backed while Phase 11 generic all-laws execute stays gated.
