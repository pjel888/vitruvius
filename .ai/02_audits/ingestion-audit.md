> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline. It is retained here as a frozen historical record of what the codebase looked like before Sprints A + B + C + D + Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z + HP.3-R shipped. Almost every "weakness" or "missing feature" flagged below has since been addressed.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-029
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout (including post-Sprint-D additions)
> - `/.ai/00_system/pipeline-overview.md` — current execution flow

---

# Ingestion Audit — Code-Forensic Findings

**Audit Target**: `C:\Users\Philip Lewis\Desktop\Vitruvius\.ai\02_audits\ingestion-audit.md`  
**Date**: 2026-04-13  
**Scope**: Full codebase crawl for INGESTION layer (file discovery → type detection → parsing → artifact creation → registry updates)

---

## 1. Repository Map

### Python Files Related to Ingestion (25 files)

| File | Purpose | Status |
|------|---------|--------|
| `scripts/pipeline_cli.py` | CLI entrypoint, dispatch | ACTIVE |
| `scripts/Word-PPT-To-PDF.py` | Office→PDF prep (standalone) | UTILITY |
| `scripts/vitruvius/scanner.py` | Raw layer file discovery | ACTIVE |
| `scripts/vitruvius/detection.py` | PDF type classification | ACTIVE |
| `scripts/vitruvius/conversion.py` | PDF→Markdown conversion + registry | ACTIVE |
| `scripts/vitruvius/ocr.py` | OCR queue + execution | ACTIVE |
| `scripts/vitruvius/office.py` | DOCX/PPTX→PDF conversion | ACTIVE |
| `scripts/vitruvius/spreadsheets.py` | XLSX parsing | ACTIVE |
| `scripts/vitruvius/reports.py` | CSV/JSON registry I/O | ACTIVE |
| `scripts/vitruvius/models.py` | FileEntry dataclass | ACTIVE |
| `scripts/vitruvius/paths.py` | Path builders (input→output) | ACTIVE |
| `scripts/vitruvius/constants.py` | Layer names | ACTIVE |
| `scripts/vitruvius/utils.py` | Timestamps, normalization | ACTIVE |

---

## 2. Entry Points

### CLI Commands → Handler Functions

| CLI Command | Handler Function | Module | File Path |
|------------|------------------|--------|----------|
| `scan` | `run_scan()` | `scanner.py` | `scripts/vitruvius/scanner.py` |
| `detect-one` | `run_detect_one()` | `detection.py` | `scripts/vitruvius/detection.py` |
| `convert-one` | `run_convert_one()` | `conversion.py` | `scripts/vitruvius/conversion.py` |
| `convert` | `run_convert()` | `conversion.py` | `scripts/vitruvius/conversion.py` |
| `ocr-queue` | `run_ocr_queue()` | `ocr.py` | `scripts/vitruvius/ocr.py` |
| `ocr-execute` | `run_ocr_execute()` | `ocr.py` | `scripts/vitruvius/ocr.py` |
| `convert-spreadsheet-one` | `run_convert_spreadsheet_one()` | `spreadsheets.py` | `scripts/vitruvius/spreadsheets.py` |

### File Flow Into System

```
1. Office documents (DOCX, PPTX) → Word-PPT-To-PDF.py → 001_Raw-Source-Layer/
2. Raw Source Layer (001_Raw-Source-Layer/)
   └── scan → builds file registry + tree snapshot
3. Files discovered → detect-one/convert → type classification
4. Text PDFs → OpenDataLoader → raw_markdown/*.md + sidecar_json/*.json
5. Scanned PDFs → ocr-execute → ocr_pdf/*.pdf → OpenDataLoader → Markdown/JSON
```

---

## 3. Import Graph

```
pipeline_cli.py
├── vitruvius.scanner (run_scan)
├── vitruvius.detection (run_detect_one)
├── vitruvius.conversion (run_convert, run_convert_one)
├── vitruvius.ocr (run_ocr_queue, run_ocr_execute)
├── vitruvius.spreadsheets (run_convert_spreadsheet_one)
└── vitruvius.reports (write_csv, write_json, append)
```

### Supporting Dependencies

| Module | Imports | Purpose |
|--------|---------|---------|
| `scanner.py` | paths, reports, models, utils | File discovery |
| `detection.py` | reports, utils | PDF text extraction via pypdf |
| `conversion.py` | detection, reports, paths, utils | PDF parsing via OpenDataLoader |
| `ocr.py` | detection, conversion, reports, paths | OCRmyPDF execution |
| `reports.py` | pandas (CSV), json | Registry I/O |

---

## 4. Ingestion Pipeline (Actual)

### Full Execution Flow

```
CLI: python scripts/pipeline_cli.py scan
└─→ scanner.run_scan()
    ├─ get_repo_root() → RAW_LAYER_NAME (001_Raw-Source-Layer/)
    ├─ build_file_entries(raw_root) → List[FileEntry]
    │   └─ Captures: relative_path, name, extension, size_bytes, 
    │                modified_utc, parent_folder, top_category
    ├─ build_tree_lines(raw_root) → human-readable tree
    └─ Outputs:
        ├─ 006_System-Manifests/tree-snapshots/latest_raw_tree_snapshot.json
        ├─ 006_System-Manifests/tree-snapshots/latest_raw_tree_snapshot.txt
        └─ 006_System-Manifests/registries/latest_raw_file_registry.csv

CLI: python scripts/pipeline_cli.py detect-one "<path>"
└─→ detection.run_detect_one(relative_pdf_path, sample_pages=5)
    ├─ detect_pdf_type(pdf_path, sample_pages)
    │   ├─ PdfReader extracts text per page
    │   ├─ Counts characters per page
    │   └─ Classification logic:
    │       ├─ ≥50 chars/page = "usable text"
    │       ├─ ≥50% usable pages + ≥300 total = TEXT_PDF
    │       └─ else = LIKELY_SCANNED_PDF
    └─ Outputs:
        ├─ 006_System-Manifests/runs/latest_detect_one_report.json
        └─ 006_System-Manifests/runs/latest_detect_one_report.txt

CLI: python scripts/pipeline_cli.py convert
└─→ conversion.run_convert()
    ├─ Reads latest status report for new/changed files
    ├─ For each PDF:
    │   ├─ run detection → TEXT_PDF or SCANNED_PDF
    │   ├─ TEXT_PDF → convert_text_pdf() → OpenDataLoader
    │   │   └─ 002_Raw-Conversion-Layer/<cat>/raw_markdown/*.md
    │   │   └─ 002_Raw-Conversion-Layer/<cat>/sidecar_json/*.json
    │   └─ SCANNED_PDF → QUEUED_FOR_OCR
    ├─ Writes conversion registry entry per file
    └─ Outputs:
        ├─ 006_System-Manifests/registries/latest_conversion_registry.csv
        ├─ 006_System-Manifests/runs/latest_convert_queue.json
        └─ 006_System-Manifests/runs/latest_ocr_needed_report.json

CLI: python scripts/pipeline_cli.py ocr-execute
└─→ ocr.run_ocr_execute()
    ├─ Reads OCR queue
    ├─ For each queued PDF:
    │   ├─ ocrmypdf.ocr(input, output, languages, deskew)
    │   └─ convert_pdf_at_path() on OCR output
    └─ Outputs:
        └─ 002_Raw-Conversion-Layer/<cat>/ocr_pdf/*.pdf
           (then → raw_markdown + sidecar_json)
```

---

## 5. Module Breakdown

### scanner.py — File Discovery

**Location**: `scripts/vitruvius/scanner.py`

| Function | Purpose |
|----------|---------|
| `build_file_entries(raw_root)` | Recursively scans raw layer, returns `List[FileEntry]` |
| `build_tree_lines(root)` | Generates human-readable directory tree |
| `run_scan()` | Orchestrates scan command |

**Metadata Captured** (per file):
- `relative_path` — POSIX path relative to raw root
- `name` — filename
- `extension` — lowercased extension (e.g., `.pdf`)
- `size_bytes` — file size in bytes
- `modified_utc` — ISO-8601 UTC timestamp
- `parent_folder` — parent directory
- `top_category` — first path segment (001-Laws, etc.)

**NOTE**: No file hashes computed.

---

### detection.py — Type Classification

**Location**: `scripts/vitruvius/detection.py`

| Function | Purpose |
|----------|---------|
| `detect_pdf_type(pdf_path, sample_pages=5)` | Classifies PDF as TEXT_PDF or LIKELY_SCANNED_PDF |
| `run_detect_one()` | CLI handler for single-file detection |

**Classification Logic**:
```python
# For each sampled page:
text = page.extract_text()
if len(text) >= 50:
    usable_pages += 1

# Classification:
likely_text_pdf = usable_pages >= (sample_pages / 2) and total_chars >= 300
# Return: "TEXT_PDF" or "LIKELY_SCANNED_PDF"
```

---

### conversion.py — Parsing + Registry

**Location**: `scripts/vitruvius/conversion.py`

| Function | Purpose |
|----------|---------|
| `convert_text_pdf(source_path)` | Converts TEXT_PDF via OpenDataLoader |
| `run_convert_one()` | Single file CLI |
| `run_convert()` | Batch processing with queue reports |

**Registry Fields** (per conversion):
- `timestamp_utc`, `run_command`, `source_relative_path`
- `logical_source_relative_path`, `source_extension`, `source_size_bytes`
- `source_modified_utc`, `top_category`
- `detected_pdf_type`, `processing_route`
- `status` (SUCCESS/FAILED/QUEUED_FOR_OCR)
- `output_markdown_relative_path`, `output_json_relative_path`
- `output_ocr_pdf_relative_path`, `error_message`

---

### ocr.py — OCR Processing

**Location**: `scripts/vitruvius/ocr.py`

| Function | Purpose |
|----------|---------|
| `run_ocr_queue()` | Builds OCR queue from OCR-needed report |
| `run_ocr_execute()` | Runs OCRmyPDF on queued PDFs |

**OCRmyPDF Execution**:
```python
ocrmypdf.ocr(
    input_file=pdf_path,
    output_file=ocr_pdf_path,
    languages=languages,
    deskew=not args.no_deskew,
)
```

---

## 6. Parser Integrations

### Active Parsers

| Parser | Library | Use | Output |
|--------|---------|-----|--------|
| PDF Text Extraction | `pypdf` | detection.py | Character count per page |
| PDF→Markdown | `opendataloader` | conversion.py | `.md` + `.json` |
| OCR | `ocrmypdf` | ocr.py | OCR'd PDF + Markdown/JSON |
| Office→PDF | `soffice` (LibreOffice) | office.py | PDF |
| Spreadsheets | `openpyxl` | spreadsheets.py | CSV/JSON |

---

## 7. File Routing Logic

### Input → Output Path Mapping (via paths.py)

| Input Type | Output Subdirectory | Filename Pattern |
|-----------|-------------------|-----------------|
| Text PDF | `raw_markdown/<cat>/...` | `stem.md` |
| Text PDF sidecar | `sidecar_json/<cat>/...` | `stem.json` |
| Scanned PDF | `ocr_pdf/<cat>/...` | `original_filename.pdf` |
| Office PDF | `office_pdf/<cat>/...` | `stem.pdf` |
| Spreadsheet | `spreadsheet_csv/<cat>/...` | `stem.csv` |
| Spreadsheet data | `spreadsheet_json/<cat>/...` | `stem.json` |

---

## 8. Filesystem and Artifact Flow

### Directory Structure

```
001_Raw-Source-Layer/           # INPUT
└── <category>/<subfolder>/<file>.pdf

002_Raw-Conversion-Layer/       # OUTPUT
└── <category>/
    ├── raw_markdown/<subfolder>/<file>.md
    ├── sidecar_json/<subfolder>/<file>.json
    ├── ocr_pdf/<subfolder>/<file>.pdf  (if OCR'd)
    ├── office_pdf/<subfolder>/<file>.pdf  (if converted from Office)
    ├── spreadsheet_csv/<subfolder>/<file>.csv
    └── spreadsheet_json/<subfolder>/<file>.json

006_System-Manifests/          # REGISTRY
├── registries/
│   ├── latest_raw_file_registry.csv
│   └── latest_conversion_registry.csv
├── tree-snapshots/
│   ├── latest_raw_tree_snapshot.json
│   └── latest_raw_tree_snapshot.txt
└── runs/
    ├── latest_detect_one_report.json
    ├── latest_convert_queue.json
    └── latest_ocr_needed_report.json
```

---

## 9. Data and Metadata Flow

### Metadata Captured at Each Stage

| Stage | Metadata Fields |
|------|---------------|
| **Scan** | relative_path, name, extension, size_bytes, modified_utc, parent_folder, top_category |
| **Detection** | total_pages, pages_sampled, pages_with_usable_text, total_extracted_characters, detected_pdf_type |
| **Conversion** | source_* fields + detected_pdf_type, processing_route, status, output paths, error_message |
| **OCR** | same as conversion + OCR status, error_message on failure |

### Normalization

- Filenames normalized for duplicate detection via `utils.normalize_filename()` 
- Text normalized for comparison via `utils.normalize_text()`

---

## 10. Error Handling and Fallbacks

### Error Handling Patterns

| Stage | Behavior |
|-------|----------|
| **Scan** | Missing raw layer → print error, return 1. No per-file retry. |
| **Detection** | FileNotFoundError ��� return error dict. |
| **Conversion** | Per-file try/except → log FAILED registry entry, continue batch. |
| **OCR** | ocrmypdf exception → log FAILED registry entry with error_message, continue. |

### No Retry Loop

- Retries are accomplished by re-running the batch/queue commands
- No automatic retry mechanism in code

---

## 11. Supported File Types (Verified)

| File Type | Status | Processing Path |
|-----------|--------|-----------------|
| `.pdf` (text-based) | ✅ ACTIVE | OpenDataLoader → raw_markdown |
| `.pdf` (scanned) | ✅ ACTIVE | OCRmyPDF → ocr_pdf → OpenDataLoader |
| `.docx` | ⚠️ PREP | soffice → PDF → then standard path |
| `.pptx` | ⚠️ PREP | soffice → PDF → then standard path |
| `.xlsx` | ✅ ACTIVE | openpyxl → CSV/JSON |

---

## 12. Missing or Partial Implementations

| Component | Status | Notes |
|-----------|--------|-------|
| File hashing | **MISSING** | No SHA/MD5 computed |
| Staging directory | **NOT IMPLEMENTED** | Direct pipeline, no on-disk staging |
| Automatic retry | **NOT IMPLEMENTED** | Manual re-run required |
| OCR parallelization | **NOT IMPLEMENTED** | Sequential OCRmyPDF execution |

---

## 13. Dead Code

No dead code found. All ingestion modules are actively imported via pipeline_cli.py.

---

## 14. Performance Risks

| Risk | Severity | Description |
|------|----------|-------------|
| Large PDF memory | MEDIUM | pypdf loads pages into memory |
| Sequential OCR | HIGH | No parallelization of OCRmyPDF |
| Registry growth | MEDIUM | CSV appends indefinitely, no rotation |

---

## 15. Changelog

### Audit Findings

| Finding | Type | Description |
|---------|------|-------------|
| Scanner metadata fields verified | ✅ CONFIRMED | 7 fields captured, no hashes |
| Detection heuristic verified | ✅ CONFIRMED | ≥50 chars ≥50% pages ≥300 total = TEXT_PDF |
| Parser integrations verified | ✅ CONFIRMED | OpenDataLoader, OCRmyPDF, soffice, openpyxl |
| Filesystem flow verified | ✅ CONFIRMED | 001→002 mapping via paths.py |
| Registry structure verified | ✅ CONFIRMED | Per-file CSV entries with status |
| No retry loop confirmed | ✅ CONFIRMED | Re-run required, no auto-retry |
| No file hashing confirmed | ✅ CONFIRMED | Only size_bytes and mtime stored |

---

*Audit completed via code-forensic analysis. All claims traced to actual file contents.*