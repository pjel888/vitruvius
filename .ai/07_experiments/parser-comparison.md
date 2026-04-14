# Parser Comparison Experiment

> **Status:** Template / structure only. Populated during Sprint C, Phase 1B.
> **Owner:** Ingestion track
> **Last Updated:** 2026-04-14
> **Plan reference:** `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md`

## 1. Purpose
Benchmark the parser fallback chains defined in Phase 1B on the Golden Corpus (30 documents: 10 simple / 10 complex / 10 scanned). The goal is empirical parser selection — which parser wins for each `document_class` under real documents from the PD 1096 corpus and related Philippine building law sources.

This experiment drives the parser chain ordering in `phase-1b-multi-parser-integration-plan.md` §5 from "reasoned guess" to "measured."

## 2. Hypotheses to Test
1. **H1.** For `text_pdf_simple`, OpenDataLoader alone matches or beats Docling/Marker on page coverage and markdown_length, at 3–10× lower latency.
2. **H2.** For `text_pdf_complex` (tables, multi-column), Docling beats OpenDataLoader on table preservation (Gate-004 sanity) and header extraction (Gate-003 structure).
3. **H3.** For `hybrid_pdf`, Marker preserves inline image context better than OpenDataLoader and does not hallucinate captions.
4. **H4.** For `scanned_pdf_clean`, OCRmyPDF → Marker beats OCRmyPDF → OpenDataLoader on structural recovery (headings, lists).
5. **H5.** For `scanned_pdf_noisy`, Surya catches characters that Tesseract (via OCRmyPDF) misses on Filipino/English mixed text.
6. **H6.** Page-level isolation in the fallback chain reduces document-level `FALLBACK_EXHAUSTED` rate by >50% vs whole-document fallback.

## 3. Golden Corpus (to be assembled)

### 3.1 Composition
| Class | Target count | Rationale |
|---|---|---|
| text_pdf_simple | 10 | Typical gazette text; baseline. |
| text_pdf_complex | 10 | Multi-column layouts, tables (occupancy tables, setback tables). |
| scanned_pdf_clean | 5 | Recent high-resolution scans. |
| scanned_pdf_noisy | 5 | Old or poorly-scanned documents from historical archives. |
| hybrid_pdf | 5 | Mixed image/text (diagrams with inline text). |
| office_doc | 2 | DOCX drafts, reference handouts. |
| office_slide | 2 | PPTX lectures. |
| spreadsheet_structured | 1 | Occupancy table XLSX. |
| **Total** | **40** | — |

### 3.2 Selection Rules
- Each document MUST have a known-good ground-truth Markdown output (hand-curated reference).
- Each document MUST be reusable — no licensing restrictions that prevent re-processing.
- Documents MUST NOT leak into Sprint C training data for any parser.

## 4. Metrics

### 4.1 Quality Gates (binary)
- **Gate-001 (Integrity):** Markdown is well-formed UTF-8.
- **Gate-002 (Volume):** `markdown_length >= 500` chars or ≥10% of raw text length.
- **Gate-003 (Structure):** ≥1 H1 or H2 header if `pages_total > 5`.
- **Gate-004 (Sanity):** Post-conversion page count matches source ±1.

### 4.2 Quality Scores (continuous)
- `page_coverage_ratio`: `pages_processed / pages_total`.
- `header_recall`: headers detected / headers in ground truth.
- `table_recall`: tables preserved / tables in ground truth.
- `char_recall`: characters recovered / characters in ground truth.
- `hallucination_rate`: (confident-looking but wrong) spans / total extracted spans.
- `garbled_ratio`: non-printable or invalid unicode / total chars.

### 4.3 Operational Metrics
- `duration_ms`: end-to-end time.
- `peak_memory_mb`: RSS at peak.
- `ocr_applied`: bool.
- `fallback_depth`: how many parsers in the chain were tried before one succeeded.
- `failure_reason`: null or one of the Phase 1B fallback triggers.

## 5. Parser Set

### 5.1 Candidates
| ID | Library | Version | Notes |
|---|---|---|---|
| `opendataloader` | opendataloader_pdf | (currently installed) | Baseline; already in `conversion.py`. |
| `docling` | docling | TBD | Table + structure strength. |
| `marker` | marker-pdf | TBD | Layout + image-caption strength. |
| `surya` | surya-ocr | TBD | Multilingual OCR. |
| `tesseract` | ocrmypdf | (currently installed) | Baseline OCR. |
| `libreoffice` | soffice | (currently installed) | Office → PDF preprocessor. |

### 5.2 Chains Under Test (from Phase 1B §5)
```
text_pdf_simple       : [opendataloader]
text_pdf_complex      : [docling, marker, opendataloader]
scanned_pdf_clean     : [ocr_preprocessor, marker]
scanned_pdf_noisy     : [ocr_preprocessor, surya, marker]
hybrid_pdf            : [docling, marker]
office_doc            : [libreoffice_preprocessor, docling]
spreadsheet_unstructured : [spreadsheet_parser]
```

## 6. Protocol
1. **Freeze parser versions** at the start of the run. Record them in the result JSON.
2. **Dry-run on a single document** to verify each parser is callable and the wrappers don't crash.
3. **Run the full Golden Corpus** three times per parser configuration (median of 3 for latency; all-pass for gates).
4. **Record results** in `results/parser_comparison_YYYYMMDDTHHMMSSZ.json`.
5. **Human spot-check** 10% of outputs for hallucination and table integrity (things the quality gates don't catch).

## 7. Result Template (to be populated)
```json
{
  "run_id": "",
  "generated_at_utc": "",
  "parser_versions": {},
  "per_document": [
    {
      "doc_id": "",
      "document_class": "",
      "parsers_attempted": [],
      "parser_winner": "",
      "gates": {"001": true, "002": true, "003": true, "004": true},
      "scores": {
        "page_coverage_ratio": 0.0,
        "header_recall": 0.0,
        "table_recall": 0.0,
        "char_recall": 0.0,
        "hallucination_rate": 0.0,
        "garbled_ratio": 0.0
      },
      "operational": {
        "duration_ms": 0,
        "peak_memory_mb": 0,
        "ocr_applied": false,
        "fallback_depth": 0,
        "failure_reason": null
      }
    }
  ],
  "aggregates": {
    "per_class_winner_by_quality": {},
    "per_class_winner_by_latency": {},
    "recommended_chains": {}
  },
  "human_spot_checks": []
}
```

## 8. Decision Criteria
For each `document_class`, the parser chain is chosen by this order:
1. All quality gates must pass on ≥90% of the corpus.
2. Among gate-passing parsers, rank by `(header_recall + table_recall + char_recall) / 3`.
3. Break ties by latency (lower wins).
4. Break further ties by peak memory (lower wins).

The winning chain updates `scripts/vitruvius/rules/parser_chains.yaml` (to be created in Sprint C).

## 9. Known Unknowns
- Licensing on Docling/Marker — may constrain which parsers land in production.
- Surya memory footprint on long scanned documents — may force page-level isolation from the first attempt.
- Hallucination detection is heuristic — the final check is the human spot-check, not an automated metric.

## 10. Related Experiments
- `model-comparison.md` — LLM comparison for Phase 6A/6B (parallel effort, different track).

## Changelog
- **2026-04-14** — Template created. Populated during Sprint C, Phase 1B.
