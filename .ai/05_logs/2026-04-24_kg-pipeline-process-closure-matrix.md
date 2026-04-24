# KG Pipeline Process Closure Matrix — 2026-04-24

## Purpose

Repo-backed closure ledger for the recent raw-source → KG rerun remediation lane.

This document answers three questions:

1. What findings were audited?
2. What was fixed versus still open?
3. What process checks now need to happen before claiming a rerun is healthy?

## Closure Matrix

| Finding | Status | Evidence / Fix | Notes |
|---|---|---|---|
| `run-kg-pipeline --all --force` reset broke bootstrap assumptions around runs/registries | fixed | `scripts/pipeline_cli.py` force/full-path logic was changed earlier in session to enumerate full scope directly rather than depend on incremental status-only flow | addressed before this log; validated by subsequent bounded reruns reaching all later phases |
| Full-force path bypassed OCR because it used `run_convert_one()` directly | fixed | `scripts/pipeline_cli.py` now routes force preparation through `_convert_and_refine_for_kg_pipeline(...)` | regression-covered in `scripts/tests/test_kg_pipeline_force_path.py` |
| Non-force full run stopped at `run_convert()` and did not execute OCR queue/execute before refine | fixed | `scripts/pipeline_cli.py` now runs `run_ocr_queue()` then `run_ocr_execute()` before `run_refine()` | regression-covered in `scripts/tests/test_kg_pipeline_force_path.py` |
| OpenDataLoader crash on structural PDFs needed fallback | fixed | `scripts/vitruvius/conversion.py` Docling fallback; `scripts/tests/test_conversion_fallback.py` | pre-existing session fix retained |
| Canonical source pages were not reliably mapped back to refined markdown during Phase 3 | fixed | `scripts/vitruvius/canonicalize.py` writes `source_relative_markdown_path`; `scripts/pipeline_cli.py` prefers it in Phase 3 | validated in bounded rerun |
| Subject-scoped Phase 3 silently dropped freshly canonicalized sources because subject matching ignored `source_relative_markdown_path` | fixed | `scripts/pipeline_cli.py::_source_matches_subjects(...)` now checks `source_relative_markdown_path` first | validated by rerun: Phase 3 moved from 4 sources to full 7 sources for `003-Theory` |
| Zero-candidate review path returned success without writing `high_conf.json` | fixed | `scripts/vitruvius/ollama_review.py` now writes explicit empty high-confidence output | validated by per-source artifact read |
| Phase 3 report overstated “promoted” by counting source-level no-error execution rather than actual created/merged relationships | fixed | `scripts/pipeline_cli.py` now reports `promoted`, `promoted_sources`, `extracted_relationships`, `high_confidence_candidates`, `promotion_created`, `promotion_merged`, `promotion_skipped`, `promotion_rejected`, `promotion_errors`, `zero_relationship_sources`, `zero_high_confidence_sources` | validated by bounded rerun report |
| Same-title canonical sources silently overwrote each other (`toa.md` collision) | fixed | `scripts/vitruvius/canonicalize.py` now resolves collisions against existing canonical sources and falls back to canonical-id filename when needed | validated by rerun and regression test |
| Refined-markdown source identity could drift away from an already-existing canonical source after collision hardening | fixed | `scripts/vitruvius/source_identity.py` now prefers canonical source frontmatter matched by `source_relative_markdown_path` before falling back to plan-building | validated by direct PD 1096 positive-path rerun and regression test |
| Nested subject selectors (for example `001-Laws/PD-1096`) worked in Phase 1 but failed to match conversion-layer paths in Phase 2/3 | fixed | `scripts/pipeline_cli.py` now matches nested subjects across `raw_markdown`, `refined_markdown`, `sidecar_json`, and `ocr_pdf` path shapes | validated by integrated PD-1096 `run-kg-pipeline` rerun |
| Canonical source frontmatter was written as YAML-unsafe plain strings, causing false “No frontmatter” warnings for colon/tab-bearing titles | fixed | `scripts/vitruvius/canonicalize.py` now renders frontmatter via `yaml.safe_dump(...)`; affected legacy source files were normalized | validated by direct `EvidenceMaterializer._materialize_sources()` check returning zero warnings |
| Lettered sections were not recognized in section extraction | fixed | `scripts/vitruvius/relationships_sections.py`; `scripts/tests/test_relationships_sections_split.py` | pre-existing session fix retained |
| Relationship-rich refined markdown was not always used in extraction | fixed | Phase 3 input selection now prefers frontmatter path from canonical source | pre-existing session fix retained |
| OCR branch validated on a live detector-triggered corpus sample | fixed | `001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf` classified `LIKELY_SCANNED_PDF`; `run -> convert -> ocr-queue -> ocr-execute` completed with OCR PDF + markdown + sidecar outputs | see `latest_ocr_needed_report.json`, `latest_ocr_queue_report.json`, `latest_ocr_execute_report.json` |

## Bounded Live Validation Performed

### Targeted automated validation

- `python3 -m pytest scripts/tests/test_kg_pipeline_force_path.py scripts/tests/test_conversion_fallback.py scripts/tests/test_relationships_sections_split.py -q`
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/ollama_review.py scripts/vitruvius/canonicalize.py scripts/tests/test_kg_pipeline_force_path.py`

### Bounded live reruns

- `python3 scripts/pipeline_cli.py run-kg-pipeline --subject 003-Theory --force --tier lightweight`

Observed progression:

1. First bounded rerun exposed subject-filter loss between Phase 2 and Phase 3.
2. Subject-filter fix restored Phase 3 visibility.
3. Second bounded rerun exposed canonical source collision (`toa.md` overwrite).
4. Collision fix restored full subject coverage.
5. Final bounded rerun produced truthful Phase 3 metrics for all 7 theory sources.

Final bounded rerun report:

- `006_System-Manifests/runs/kg_pipeline_report_20260423T193414Z.json`

Key truthful Phase 3 outcome from that report:

- `sources_total: 7`
- `extracted: 7`
- `extracted_relationships: 0`
- `promoted: 0`
- `zero_relationship_sources: 7`
- `zero_high_confidence_sources: 7`

This proves the report no longer overclaims promotion when the subject produces no relationships.

### Live OCR-required validation

Real OCR-triggered corpus sample used:

- `001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf`

Observed sequence:

1. `python3 scripts/pipeline_cli.py detect-one "001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf" --sample-pages 1`
   - result: `LIKELY_SCANNED_PDF`
   - route: `OCR_FIRST_THEN_OPENDATALOADER`
2. `python3 scripts/pipeline_cli.py run`
   - status detected the file as changed
3. `python3 scripts/pipeline_cli.py convert`
   - `OCR required: 1`
   - wrote `latest_ocr_needed_report.json`
4. `python3 scripts/pipeline_cli.py ocr-queue`
   - queue size `1`
5. `python3 scripts/pipeline_cli.py ocr-execute`
   - `OCR completed: 1`
   - `Conversion completed: 1`
   - `Failed: 0`

Artifacts confirmed:

- `002_Raw-Conversion-Layer/001-Laws/ocr_pdf/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf`
- `002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md`
- `002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.json`

### Live positive-path relationship validation

Relationship-rich corpus sample used:

- `001-Laws/refined_markdown/PD-1096/PD 1096 - National Building Code.md`

Observed sequence:

1. Extraction:
   - `python3 scripts/pipeline_cli.py extract-relationships-sections-one "001-Laws/refined_markdown/PD-1096/PD 1096 - National Building Code.md" --json-out /tmp/pd1096_extract_realid2.json --txt-out /tmp/pd1096_extract_realid2.txt`
   - result: `Sections processed: 140`, `Unique relationships: 16`
2. Review:
   - `python3 scripts/pipeline_cli.py review-relationships-ollama --model qwen2.5:3b ... --input-report /tmp/pd1096_extract_realid2.json ... --high-confidence-out /tmp/pd1096_high_conf_realid2.json`
   - result: `auto_accept: 4`, `auto_reject: 3`, `needs_review: 9`
   - high-confidence output count: `7`
3. Promotion:
   - `python3 scripts/pipeline_cli.py promote --execute --input-report /tmp/pd1096_high_conf_realid2.json --relationships-out-dir /tmp/pd1096_promoted_realid2 --audit-log-path /Users/philiplewis/vitruvius/006_System-Manifests/runs/pd1096_validation_promotion.log`
   - result: `created: 7`, `rejected: 0`, `errors: []`

Artifacts confirmed:

- `/tmp/pd1096_high_conf_realid2.json` with `count: 7`
- `/tmp/pd1096_promoted_realid2/*.md` (7 files)
- one inspected example: `/tmp/pd1096_promoted_realid2/rel-law-national-building-code-of-the-philippines-governs-concept-building-permit.md`

### Additional process edge found during positive-path validation

- Using a manually wrong `source_id` override (`law-national-building-code`) caused expected promotion rejection.
- More importantly, a real consistency issue surfaced: refined-markdown source identity could diverge from the already-admitted canonical source ID after collision hardening.
- That drift is now fixed in `scripts/vitruvius/source_identity.py` by preferring existing canonical source frontmatter matched via `source_relative_markdown_path`.

### Live integrated positive-path orchestration validation

Real end-to-end positive-path orchestration used:

- `python3 scripts/pipeline_cli.py run-kg-pipeline --subject "001-Laws/PD-1096" --force --tier lightweight`

Why this mattered:

- Oracle explicitly required proof through the **primary orchestrated pipeline command**, not only direct extract/review/promote components.

Observed progression:

1. The first nested-subject attempt exposed another real bug: `001-Laws/PD-1096` matched the raw layer in Phase 1, but Phase 2/3 dropped everything because conversion-layer paths are shaped like `001-Laws/refined_markdown/PD-1096/...`.
2. That was fixed in `scripts/pipeline_cli.py` by adding nested-subject-aware conversion path matching.
3. The rerun after that fix completed with non-zero positive-path outputs all the way through Phase 5.

Final report:

- `006_System-Manifests/runs/kg_pipeline_report_20260423T203224Z.json`

Key integrated results from that report:

- `sources_total: 28`
- `extracted: 28`
- `extracted_relationships: 415`
- `promoted: 177`
- `promoted_sources: 17`
- `high_confidence_candidates: 177`
- `promotion_created: 177`
- `promotion_rejected: 0`
- `promotion_errors: 0`
- `relationship_assertions: 354`
- `fast_edges: 177`

This is the strongest end-to-end proof in the lane because it demonstrates the orchestrated rerun path succeeding on a real positive corpus slice.

### Final current-HEAD integrated validation

After the YAML-safe canonical frontmatter fix, the integrated PD-1096 pipeline was rerun again on the final code state:

- `python3 scripts/pipeline_cli.py run-kg-pipeline --subject "001-Laws/PD-1096" --force --tier lightweight`

Final current-head report:

- `006_System-Manifests/runs/kg_pipeline_report_20260423T221427Z.json`

Key final-state results:

- `sources_total: 34`
- `extracted_relationships: 485`
- `high_confidence_candidates: 203`
- `promotion_candidates: 203`
- `promotion_created: 3`
- `promotion_skipped: 200`
- `promotion_errors: 0`
- `relationship_assertions: 596`
- `fast_edges: 300`
- `warnings: []` in Phase 4

Interpretation:

- positive-path orchestration still works on the final code state
- promotion is now mostly skipping because prior promoted relationships already exist, not because the process is failing
- the earlier frontmatter warning set is gone on the final integrated rerun

## Process Hardening Checklist

Before calling a rerun healthy, do all of the following:

1. **Run a bounded subject rerun first** before `--all`.
2. **Inspect the Phase 3 report fields** in `kg_pipeline_report_*.json` — do not treat `status: ok` as meaning relationships were promoted.
3. **Verify per-source artifacts** for at least one zero-case and one positive-case source:
   - `extract.json`
   - `review.json`
   - `high_conf.json`
4. **Check for canonical source collisions** after Phase 2 by comparing number of refined inputs to subject-scoped canonical sources.
5. **Do not rely on detector assumptions** — confirm at least one live OCR-required source whenever OCR path changes land.
6. **Read the final Phase 4 counts** (`relationship_assertions`, `fast_edges`) and make sure they agree with Phase 3 promotion counts.
7. **Treat pre-existing Phase 4 warnings as separate debt** unless they were explicitly included in the current closure scope.
8. **For refined-markdown-based extraction, confirm source identity matches the already-admitted canonical source** before trusting downstream promotion results.
9. **For nested subject scopes, verify Phase 1, Phase 2, and Phase 3 agree on the same slice** — raw-layer filtering alone is not sufficient.
10. **Render canonical frontmatter through YAML serialization, not string concatenation** — titles with colons or tabs can otherwise create false “No frontmatter” failures downstream.

## Honest Remaining Caveats

- The theory slice validated truthful zero-output behavior; the PD-1096 nested-subject rerun validates the integrated positive path through `run-kg-pipeline`.
- The full PD-1096 rerun is operationally heavy and can exceed long interactive tool timeouts even when the underlying process is healthy; final proof therefore uses the completed current-head integrated report `kg_pipeline_report_20260423T221427Z.json` rather than partial console output.

## Conclusion

The audited **process defects discovered in this remediation lane** were fixed and revalidated with bounded live reruns plus targeted regression tests.

What remains is no longer the same category of defect:

- broader dataset-specific extraction quality work when a slice produces zero relationships

This means the immediate rerun-process repair lane is closed, but future closure claims should reference this matrix rather than only citing test passes.
