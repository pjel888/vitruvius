# Research Pack — Laws M2 Admission Path for RA-9514 / BP-344 / BP-220

## Purpose
Establish the current repo truth for admitting `RA-9514`, `BP-344`, and `BP-220` into the laws mini dataset→graph pipeline after the M1 scoped graph proof completed as `PARTIAL`.

## Current truth-bearing state
Fresh repo scan shows the live shared truth layer is still PD-1096-centric:
- shared canonical sources: 3 files, all PD-1096 / NBCP related
- shared canonical concepts: 20 files, all tied to the existing PD-1096 corpus
- shared approved relationships: 31 files, all within the current PD-1096/NBCP truth surface

Fresh search results:
- `003_Canonical-Knowledge-Layer/shared/sources/` → no `RA-9514`, `BP-344`, or `BP-220` hits
- `003_Canonical-Knowledge-Layer/shared/concepts/` → no `RA-9514`, `BP-344`, or `BP-220` hits
- `003_Canonical-Knowledge-Layer/shared/relationships/` → no `RA-9514`, `BP-344`, or `BP-220` hits

## Raw-source evidence by law
### RA-9514
Raw file present:
- `001_Raw-Source-Layer/001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf`

Detection evidence:
- `python3 scripts/pipeline_cli.py detect-one '001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf'`
- Result: `TEXT_PDF`
- Recommended route: `OPENDATALOADER_DIRECT`

Current downstream state:
- no raw_markdown match
- no refined_markdown match
- no canonical source page
- no admitted concepts
- no approved relationships

### BP-344
Raw files present:
- `001_Raw-Source-Layer/001-Laws/BP-344/2024 Revised Implementing Rules and Regulations Batas Pambansa Blg. 344 _ National Council on Disability Affairs.pdf`
- `001_Raw-Source-Layer/001-Laws/BP-344/BP-344 IRR Accessibility Law DPWH.pdf`
- adjacent/out-of-folder context: `001_Raw-Source-Layer/001-Laws/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.pdf`

Detection evidence:
- NCDA 2024 RIRR → `TEXT_PDF`, `OPENDATALOADER_DIRECT`
- DPWH IRR copy → `TEXT_PDF`, `OPENDATALOADER_DIRECT`
- DPWH DO037 adjacent memo → `TEXT_PDF`, `OPENDATALOADER_DIRECT`

Current downstream state:
- no raw_markdown match
- no refined_markdown match
- no canonical source page
- no admitted concepts
- no approved relationships

Research recommendation on variants:
- treat the 2024 NCDA RIRR as the primary authoritative admission candidate
- treat the DPWH IRR copy as explicit reference/secondary evidence unless later audit proves it is the controlling version
- keep DPWH DO037 as `adjacent_context`, not primary law text

### BP-220
Raw file present:
- `001_Raw-Source-Layer/001-Laws/BP-220/Revised_IRR_BP220_2008.pdf`

Detection evidence:
- `TEXT_PDF`
- recommended route: `OPENDATALOADER_DIRECT`

Current downstream state:
- no raw_markdown match
- no refined_markdown match
- no canonical source page
- no admitted concepts
- no approved relationships

## Dataset-manifest truth
The M1 manifest deliberately kept these laws as validation targets without admitting them as truth-bearing graph inputs:
- folder anchors were included in the bundle
- their classified raw entries remained `include_in_m1: false`
- reasons explicitly say they are tracked but not yet admitted as canonical/promoted truth inputs

This means the current `blocked` status is truthful, not accidental.

## Fresh worker-team evidence
A temporary OMX team audit was launched in a synchronized non-git snapshot because the live repo had uncommitted Ralph-owned work and the durable team runtime refused dirty-worktree startup.

Useful worker evidence harvested before shutdown:
- worker-2 confirmed with exact path evidence that `RA-9514`, `BP-344`, and `BP-220` currently have:
  - no admitted canonical sources
  - no approved relationship inputs
  - no conversion/refinement outputs
  - `blocked` rows in the latest dataset build report

Additional focused team findings from the follow-on `m2-admission-planning-assist-f` run:
- worker-1 recommended source-page defaults:
  - `RA-9514` → title `Implementing Rules and Regulations of the Fire Code of the Philippines`, id `irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines`, aliases including `RA 9514`, `Republic Act No. 9514`, `Fire Code of the Philippines`, `RA 9514 IRR`, `2019 Revised IRR`
  - `BP-220` → title `Revised Implementing Rules and Regulations of Batas Pambansa Blg. 220`, id `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220`, aliases including `BP 220`, `Batas Pambansa Blg. 220`, `BP 220 IRR`, `Revised IRR BP 220`, `2008 Revised IRR`
- worker-2 independently confirmed the BP-344 policy:
  - authoritative default = 2024 NCDA RIRR
  - DPWH IRR = explicit reference-only variant
  - DPWH DO037 = explicit adjacent context, excluded from default canonical admission
- worker-3 mapped the exact M2B dependency chain:
  - `relationships_sections.py` still writes/reads global latest extraction paths and hardcodes NBCP/IRR source-ID behavior
  - `ollama_review.py` reads global latest extraction, writes global latest review/high-confidence outputs, and reads global `latest_graph_snapshot.json` for ontology context
  - `ollama_review_second_pass.py` depends on global latest tier-1 outputs
  - `promotion/__init__.py` depends on global latest high-confidence review outputs and shared promotion audit surfaces

## M2 boundary reality
The current plan's original M2 label — "Dataset-Safe Review/Promotion Inputs" — is necessary but not sufficient for these three laws.

Why:
- they do not yet exist in converted/refined/canonical truth-bearing form
- therefore the next truthful path must include **law admission prerequisites** before review/promotion scoping can matter

## Upstream dependency reality
Current upstream modules still depend on global `latest_*` artifacts:
- `scripts/vitruvius/relationships_sections.py` → `latest_relationship_extraction_sections.json`
- `scripts/vitruvius/ollama_review.py` → `latest_relationship_extraction_sections.json`, writes `latest_relationship_review_*`
- `scripts/vitruvius/ollama_review_second_pass.py` → `latest_relationship_review_ollama.json`
- `scripts/vitruvius/promotion/__init__.py` → `latest_relationship_review_high_confidence.json`

Therefore, once the newly admitted laws need extraction/review/promotion, the path must become dataset-safe rather than silently reusing global latest state.

## Research conclusion
The proper next path is not "just flip these raw PDFs to included".

It is:
1. choose authoritative admission candidates per law
2. convert/refine/canonicalize them into truth-bearing source pages
3. define the dataset-safe extraction/review/promotion lane for their relationship generation
4. only then rerun the scoped graph and decide whether M3 orchestration is justified
