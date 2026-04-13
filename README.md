# Vitruvius

Vitruvius is a local-first knowledge pipeline for architectural board exam preparation.

It takes raw source documents — laws, books, reviewers, manuals, scanned references — and processes them through a structured series of layers: scanning, conversion, canonicalization, and derivation. The goal is to produce a trusted, machine-readable knowledge foundation that can power learning tools, retrieval systems, and AI-assisted study.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Repository Structure](#repository-structure)
- [Layer Descriptions](#layer-descriptions)
- [Pipeline CLI](#pipeline-cli)
- [Vitruvius Package](#vitruvius-package)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Utility Scripts](#utility-scripts)
- [Pipeline Workflow](#pipeline-workflow)
- [Output Artifacts Reference](#output-artifacts-reference)
- [Content Trust Order](#content-trust-order)
- [Raw Source Layer Rules](#raw-source-layer-rules)
- [Dependencies](#dependencies)
- [Design Philosophy](#design-philosophy)
- [Current Status](#current-status)

---

## Architecture Overview

Vitruvius organizes knowledge into six numbered layers, each with a specific role in the data lifecycle:

| Layer | Folder | Purpose |
|-------|--------|---------|
| 1 | `001_Raw-Source-Layer/` | Original source documents (PDFs, scans, books) |
| 2 | `002_Raw-Conversion-Layer/` | Machine-extracted text outputs (Markdown, JSON, OCR PDFs) |
| 3 | `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge pages |
| 4 | `004_Derived-Content-Layer/` | Generated learning content (articles, flashcards, questions) |
| 5 | `005_Operational-Intelligence-Layer/` | Machine infrastructure (chunks, embeddings, graphs, indexes) |
| 6 | `006_System-Manifests/` | Pipeline control, audit logs, registries, and run reports |

---

## Repository Structure

```text
Vitruvius/
├── .gitignore
├── README.md
├── init_vitruvius_structure.sh
│
├── config/
│   └── vitruvius.yaml
│
├── docs/
│   ├── CANONICAL_FRONTMATTER_TEMPLATE.md
│   └── CONTENT_RULES.md
│
├── scripts/
│   ├── .gitkeep
│   ├── pipeline_cli.py                  # Main CLI entrypoint
│   ├── Word-PPT-To-PDF.py              # Office-to-PDF batch converter
│   ├── test_odl_one.py                  # OpenDataLoader single-file test
│   ├── test_pdf_text_detection.py       # Standalone PDF text detection test
│   │
│   └── vitruvius/                       # Core pipeline package
│       ├── __init__.py
│       ├── constants.py                 # Layer and folder name constants
│       ├── models.py                    # Data models (FileEntry)
│       ├── paths.py                     # Path resolution and directory helpers
│       ├── utils.py                     # Timestamp, normalization, and naming utilities
│       ├── reports.py                   # JSON/CSV/TXT report writing and reading
│       ├── scanner.py                   # Raw layer scanning and tree snapshot generation
│       ├── status.py                    # Registry diff and change detection
│       ├── linting.py                   # Raw layer hygiene checks
│       ├── detection.py                 # PDF text vs scanned detection
│       ├── conversion.py                # PDF-to-Markdown conversion (single and batch)
│       ├── reconcile.py                 # Missing source and stale output detection
│       └── ocr.py                       # OCR queue building and OCRmyPDF execution
│
├── 001_Raw-Source-Layer/                # [git-ignored] Original source documents
│   ├── 001-Laws/
│   ├── 002-History/
│   ├── 003-Theory/
│   ├── 004-Technology/
│   ├── 005-Utilities/
│   ├── 006-Structural/
│   ├── 007-Planning/
│   ├── 008-Design/
│   └── 009-Practice/
│
├── 002_Raw-Conversion-Layer/
│   └── 001-Laws/
│       ├── raw_markdown/                # Extracted Markdown from text PDFs
│       │   └── PD-1096/
│       │       └── PD 1096 - National Building Code.md
│       ├── sidecar_json/                # Structural metadata sidecar files
│       │   └── PD-1096/
│       │       └── PD 1096 - National Building Code.json
│       └── ocr_pdf/                     # OCR-processed PDF outputs (for scanned PDFs)
│
├── 003_Canonical-Knowledge-Layer/
│   ├── 001-Laws/
│   │   ├── index.md
│   │   └── log.md
│   ├── 002-History/
│   │   ├── index.md
│   │   └── log.md
│   ├── 003-Theory/
│   │   ├── index.md
│   │   └── log.md
│   ├── 004-Technology/
│   │   ├── index.md
│   │   └── log.md
│   ├── 005-Utilities/
│   │   ├── index.md
│   │   └── log.md
│   ├── 006-Structural/
│   │   ├── index.md
│   │   └── log.md
│   ├── 007-Planning/
│   │   ├── index.md
│   │   └── log.md
│   ├── 008-Design/
│   │   ├── index.md
│   │   └── log.md
│   ├── 009-Practice/
│   │   ├── index.md
│   │   └── log.md
│   └── shared/
│       ├── index.md
│       ├── concepts/
│       ├── glossary/
│       ├── relationships/
│       └── templates/
│
├── 004_Derived-Content-Layer/
│   ├── articles/
│   │   └── 001-Laws/ ... 009-Practice/
│   ├── drafts/
│   ├── explainers/
│   │   └── 001-Laws/ ... 009-Practice/
│   ├── exports/
│   ├── flashcards/
│   │   └── 001-Laws/ ... 009-Practice/
│   ├── learning-paths/
│   │   └── 001-Laws/ ... 009-Practice/
│   ├── questions/
│   │   └── 001-Laws/ ... 009-Practice/
│   └── summaries/
│       └── 001-Laws/ ... 009-Practice/
│
├── 005_Operational-Intelligence-Layer/
│   ├── cache/
│   ├── chunks/
│   ├── embeddings/
│   ├── graph/
│   │   ├── edges/
│   │   ├── exports/
│   │   ├── nodes/
│   │   └── snapshots/
│   ├── indexes/
│   │   ├── bm25/
│   │   ├── hybrid/
│   │   └── vector/
│   ├── models/
│   ├── pipelines/
│   │   ├── canonicalize/
│   │   ├── derive/
│   │   ├── graph-build/
│   │   └── ingest/
│   └── retrieval/
│
└── 006_System-Manifests/
    ├── checksums/
    ├── conversions/
    ├── duplicates/
    ├── lineage/
    ├── logs/
    │   └── office_to_pdf.log
    ├── registries/
    │   ├── latest_raw_file_registry.csv
    │   ├── latest_conversion_registry.csv
    │   ├── canonical_registry.csv
    │   ├── conversion_registry.csv
    │   ├── graph_registry.csv
    │   ├── source_registry.csv
    │   └── <timestamp>_raw_file_registry.csv  (timestamped snapshots)
    ├── runs/
    │   ├── latest_status_report.json / .txt
    │   ├── latest_lint_report.json / .txt
    │   ├── latest_convert_queue.json / .txt
    │   ├── latest_convert_batch_report.json / .txt
    │   ├── latest_convert_one_report.json / .txt
    │   ├── latest_detect_one_report.json / .txt
    │   ├── latest_ocr_needed_report.json / .txt
    │   ├── latest_ocr_queue_report.json / .txt
    │   ├── latest_ocr_execute_report.json / .txt
    │   ├── latest_reconcile_report.json / .txt
    │   └── <timestamp>_*.json / .txt         (timestamped snapshots)
    └── tree-snapshots/
        ├── latest_raw_tree_snapshot.json
        ├── latest_raw_tree_snapshot.txt
        └── <timestamp>_raw_tree_snapshot.json / .txt
```

---

## Layer Descriptions

### Layer 1 — Raw Source Layer (`001_Raw-Source-Layer/`)

The evidence storage layer. Contains original, unmodified source documents organized by topic category.

This layer is **git-ignored** because the source files are large binary PDFs. It is managed locally only.

Accepted file types: PDFs (primary), with possible future support for DOCX, PPTX, XLSX.

**Categories:**
- `001-Laws` — legislation, codes, presidential decrees
- `002-History` — architectural history references
- `003-Theory` — design theory, architectural principles
- `004-Technology` — building technology, materials, systems
- `005-Utilities` — mechanical, electrical, plumbing, fire protection
- `006-Structural` — structural engineering references
- `007-Planning` — site planning, urban design, zoning
- `008-Design` — architectural design, programming, space planning
- `009-Practice` — professional practice, contracts, ethics, project management

### Layer 2 — Raw Conversion Layer (`002_Raw-Conversion-Layer/`)

Machine-extracted outputs from the raw source layer. Not editorial knowledge — just usable text extraction.

Each source category can contain three subdirectories:

| Subdirectory | Contents |
|-------------|----------|
| `raw_markdown/` | Markdown files extracted from text-based PDFs via OpenDataLoader |
| `sidecar_json/` | Structural metadata JSON files produced alongside Markdown |
| `ocr_pdf/` | OCR-processed PDF copies of scanned documents (produced by OCRmyPDF) |

### Layer 3 — Canonical Knowledge Layer (`003_Canonical-Knowledge-Layer/`)

The trusted knowledge layer. Contains curated, cleaned, and structured knowledge pages organized by topic.

Each category folder has:
- `index.md` — category overview and table of contents
- `log.md` — change log for updates to that category

The `shared/` directory contains cross-category resources:
- `concepts/` — concept definitions
- `glossary/` — term glossary
- `relationships/` — cross-topic relationships
- `templates/` — page templates

### Layer 4 — Derived Content Layer (`004_Derived-Content-Layer/`)

Learner-facing and AI-generated outputs built from canonical knowledge:

| Subdirectory | Purpose |
|-------------|---------|
| `articles/` | Long-form topic articles |
| `explainers/` | Simplified explanations |
| `flashcards/` | Study flashcards |
| `learning-paths/` | Structured learning sequences |
| `questions/` | Practice questions and answer banks |
| `summaries/` | Condensed topic summaries |
| `drafts/` | Work-in-progress content |
| `exports/` | Final export-ready content |

### Layer 5 — Operational Intelligence Layer (`005_Operational-Intelligence-Layer/`)

Machine-use infrastructure for AI and retrieval systems:

| Subdirectory | Purpose |
|-------------|---------|
| `chunks/` | Text chunks for retrieval |
| `embeddings/` | Vector embeddings |
| `graph/` | Knowledge graph (nodes, edges, exports, snapshots) |
| `indexes/` | Search indexes (bm25, vector, hybrid) |
| `cache/` | Cached computation results |
| `models/` | Model artifacts |
| `pipelines/` | Pipeline configuration (ingest, canonicalize, derive, graph-build) |
| `retrieval/` | Retrieval system artifacts |

### Layer 6 — System Manifests (`006_System-Manifests/`)

Control, audit, and traceability layer. All pipeline outputs are written here.

| Subdirectory | Purpose |
|-------------|---------|
| `tree-snapshots/` | JSON and TXT snapshots of the raw source layer directory tree |
| `registries/` | CSV file registries tracking all raw and converted files |
| `runs/` | Timestamped JSON and TXT reports for every pipeline command execution |
| `logs/` | Operational logs (e.g. office-to-PDF conversion log) |
| `checksums/` | File integrity checksums (planned) |
| `conversions/` | Conversion tracking artifacts (planned) |
| `duplicates/` | Duplicate detection records (planned) |
| `lineage/` | Data lineage and provenance records (planned) |

---

## Pipeline CLI

The pipeline is operated through a single entrypoint:

```bash
python scripts/pipeline_cli.py <command>
```

### Commands

#### `run` — Full pipeline sequence

```bash
python scripts/pipeline_cli.py run
```

Runs the standard pipeline sequence:
1. `scan` — snapshot the raw source layer
2. `status` — compare latest two snapshots for changes
3. `lint` — check raw layer hygiene

This is the **first command you should run** after adding, removing, or modifying files in the raw source layer.

---

#### `scan` — Scan raw source layer

```bash
python scripts/pipeline_cli.py scan
```

Recursively scans `001_Raw-Source-Layer/` and produces:
- JSON tree snapshot (`006_System-Manifests/tree-snapshots/`)
- TXT tree snapshot (human-readable directory listing)
- CSV file registry (`006_System-Manifests/registries/`)

Each run writes both a timestamped file and a `latest_` symlink-style copy.

---

#### `status` — Compare latest scans

```bash
python scripts/pipeline_cli.py status
```

Compares the two most recent timestamped file registries and reports:
- New files
- Changed files (by size, modified date, or extension)
- Missing files
- Unchanged files

Outputs to `006_System-Manifests/runs/` as JSON and TXT.

---

#### `lint` — Raw layer hygiene check

```bash
python scripts/pipeline_cli.py lint
```

Checks the latest raw file registry for issues:
- **Non-PDF files** in the raw source layer
- **Duplicate-like filenames** (normalized name collisions)

Outputs to `006_System-Manifests/runs/` as JSON and TXT.

---

#### `convert` — Batch convert all new/changed PDFs

```bash
python scripts/pipeline_cli.py convert
```

Processes all new and changed files from the latest status report:

1. Detects whether each PDF is text-based or scanned
2. Converts text-based PDFs directly using OpenDataLoader
3. Queues scanned PDFs for OCR processing
4. Writes a conversion registry entry for each file
5. Produces three reports:
   - **Convert queue** — what was queued for processing
   - **Convert batch report** — results of the batch (converted, OCR-needed, failed)
   - **OCR needed report** — scanned PDFs requiring OCR before conversion

Also automatically runs `ocr-queue` and `ocr-execute` after batch conversion.

---

#### `convert-one` — Convert a single text PDF

```bash
python scripts/pipeline_cli.py convert-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

Converts a single text-based PDF. The path is relative to `001_Raw-Source-Layer/`.

Options:
- `--sample-pages N` — number of pages to sample for text detection (default: 5)

The command will refuse to convert scanned PDFs — they must go through OCR first.

---

#### `detect-one` — Detect PDF type

```bash
python scripts/pipeline_cli.py detect-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

Analyzes a single PDF to determine if it contains extractable text or is likely a scanned image.

Options:
- `--sample-pages N` — number of pages to sample (default: 5)

Reports:
- `TEXT_PDF` → route to OpenDataLoader directly
- `LIKELY_SCANNED_PDF` → route through OCR first, then OpenDataLoader

---

#### `reconcile` — Detect stale outputs

```bash
python scripts/pipeline_cli.py reconcile
```

Checks for missing raw source files that still have derived outputs in the conversion layer. Reports:
- **Stale converted outputs** — conversion artifacts exist but the source PDF is gone
- **Missing without outputs** — source is gone and no conversion artifacts exist either

---

#### `ocr-queue` — Build OCR queue

```bash
python scripts/pipeline_cli.py ocr-queue
```

Reads the latest OCR-needed report and builds a pending OCR queue. This is a report-only step — it does not execute OCR.

---

#### `ocr-execute` — Run OCR on queued PDFs

```bash
python scripts/pipeline_cli.py ocr-execute
python scripts/pipeline_cli.py ocr-execute --languages eng tgl
python scripts/pipeline_cli.py ocr-execute --no-deskew
```

Processes the OCR queue:

1. Runs OCRmyPDF on each queued scanned PDF
2. Produces an OCR-processed PDF in `002_Raw-Conversion-Layer/<category>/ocr_pdf/`
3. Converts the OCR output to Markdown and sidecar JSON via OpenDataLoader
4. Writes conversion registry entries for each file

Options:
- `--languages` — Tesseract language codes (default: `eng`)
- `--no-deskew` — disable page deskewing during OCR

---

## Vitruvius Package

The `scripts/vitruvius/` package contains all core pipeline logic, modularized by responsibility.

### `constants.py`

Layer and folder name constants used across all modules:

| Constant | Value |
|----------|-------|
| `RAW_LAYER_NAME` | `001_Raw-Source-Layer` |
| `CONVERSION_LAYER_NAME` | `002_Raw-Conversion-Layer` |
| `MANIFESTS_NAME` | `006_System-Manifests` |
| `TREE_SNAPSHOTS_NAME` | `tree-snapshots` |
| `REGISTRIES_NAME` | `registries` |
| `RUNS_NAME` | `runs` |

### `models.py`

Data models used by the scanner and report writer.

- **`FileEntry`** — dataclass representing a single file in the raw source layer:
  - `relative_path`, `name`, `extension`, `size_bytes`, `modified_utc`, `parent_folder`, `top_category`

### `paths.py`

Path resolution utilities:

| Function | Purpose |
|----------|---------|
| `get_repo_root()` | Returns the repository root path |
| `ensure_snapshot_dir()` | Creates and returns the tree snapshots directory |
| `ensure_registry_dir()` | Creates and returns the registries directory |
| `ensure_runs_dir()` | Creates and returns the runs directory |
| `build_conversion_relative_paths()` | Computes Markdown and sidecar JSON output paths for a source file |
| `build_ocr_pdf_relative_path()` | Computes the OCR PDF output path for a source file |

### `utils.py`

General-purpose utilities:

| Function | Purpose |
|----------|---------|
| `utc_now_stamp()` | Returns a UTC timestamp string like `20260413T054443Z` |
| `iso_utc_from_timestamp()` | Converts a Unix timestamp to ISO 8601 UTC string |
| `normalize_filename()` | Strips non-alphanumeric characters and lowercases for duplicate detection |
| `normalize_text()` | Collapses whitespace for text comparison |
| `safe_name_for_report()` | Sanitizes a filename for use in report filenames |

### `reports.py`

Report I/O utilities:

| Function | Purpose |
|----------|---------|
| `write_json()` | Writes a dict as formatted JSON |
| `write_text()` | Writes a string to a text file |
| `write_csv()` | Writes a list of `FileEntry` objects as CSV |
| `read_csv_entries()` | Reads a CSV file into a list of dicts |
| `get_timestamped_registry_files()` | Lists all timestamped registry CSVs (excluding `latest_`) |
| `build_signature()` | Builds a comparison signature tuple from a registry row |
| `append_conversion_registry_row()` | Appends a row to the conversion registry CSV |
| `snapshot_conversion_registry()` | Copies the latest conversion registry to a timestamped snapshot |

### `scanner.py`

Scans the raw source layer and generates tree snapshots and file registries.

- `build_file_entries()` — recursively lists all files with metadata
- `build_tree_lines()` — generates a human-readable directory tree
- `run_scan()` — orchestrates the scan command

### `status.py`

Compares two consecutive registry snapshots to detect changes.

- `run_status()` — diffs the two latest timestamped registries

### `linting.py`

Checks the raw layer for hygiene issues.

- `run_lint()` — flags non-PDF files and duplicate-like filenames

### `detection.py`

Determines whether a PDF contains extractable text or is a scanned document.

- `detect_pdf_type()` — samples pages and measures extracted character counts
- `run_detect_one()` — CLI handler for single-file detection

Classification logic:
- A page is considered to have "usable text" if it yields ≥ 50 characters
- A PDF is classified as `TEXT_PDF` if at least half the sampled pages have usable text and total characters ≥ 300

### `conversion.py`

Handles PDF-to-Markdown conversion using OpenDataLoader.

- `convert_pdf_at_path()` — low-level converter that takes any PDF path and a logical source path
- `convert_text_pdf()` — converts a text-based PDF from the raw layer (with detection guard)
- `run_convert_one()` — CLI handler for single-file conversion
- `run_convert()` — CLI handler for batch conversion of all new/changed files
- `_write_conversion_registry_entry()` — records each conversion attempt in the conversion registry

### `reconcile.py`

Detects orphaned outputs and missing sources.

- `run_reconcile()` — cross-references missing files from the status report against conversion layer outputs

### `ocr.py`

OCR queue management and execution using OCRmyPDF.

- `run_ocr_queue()` — builds a report-only queue from the OCR-needed report
- `run_ocr_execute()` — runs OCRmyPDF on queued PDFs, then converts the OCR outputs to Markdown

---

## Configuration

### `config/vitruvius.yaml`

```yaml
project_name: Vitruvius
version: 0.1.0

categories:
  - 001-Laws
  - 002-History
  - 003-Theory
  - 004-Technology
  - 005-Utilities
  - 006-Structural
  - 007-Planning
  - 008-Design
  - 009-Practice

paths:
  raw: 001_Raw-Source-Layer
  conversion: 002_Raw-Conversion-Layer
  canonical: 003_Canonical-Knowledge-Layer
  derived: 004_Derived-Content-Layer
  ops: 005_Operational-Intelligence-Layer
  manifests: 006_System-Manifests
```

---

## Documentation

### `docs/CONTENT_RULES.md`

Five rules governing content trust and lineage:

1. Raw source files are evidence, not truth.
2. Raw conversion files are machine-readable extraction, not editorial knowledge.
3. Canonical knowledge files are the trusted knowledge layer.
4. Derived content must point back to canonical knowledge.
5. Canonical knowledge should preserve source references and update history.

### `docs/CANONICAL_FRONTMATTER_TEMPLATE.md`

YAML frontmatter template for canonical knowledge pages:

```yaml
---
id: ""
title: ""
category: ""
subtopic: ""
status: draft
source_refs: []
related_topics: []
last_updated: ""
---
```

---

## Utility Scripts

### `scripts/Word-PPT-To-PDF.py`

Batch converter for Office documents (DOCX, PPTX) to PDF. Used to prepare non-PDF source files for ingestion into the raw source layer.

### `scripts/test_pdf_text_detection.py`

Standalone test script for PDF text detection. Samples pages from a PDF and reports character counts to determine if the document is text-based or scanned.

### `scripts/test_odl_one.py`

Standalone test script for OpenDataLoader PDF conversion. Tests the conversion of a single PDF into Markdown and JSON output.

---

## Pipeline Workflow

### Standard workflow after adding new files

```bash
# 1. Place files into the correct category folder
#    inside 001_Raw-Source-Layer/

# 2. Run the core pipeline
python scripts/pipeline_cli.py run

# 3. Convert all new/changed text PDFs and queue scanned PDFs for OCR
python scripts/pipeline_cli.py convert

# 4. Review reports in 006_System-Manifests/runs/
```

### Conversion routing

```text
PDF detected as TEXT_PDF
  └─→ OpenDataLoader directly
       └─→ raw_markdown/*.md + sidecar_json/*.json

PDF detected as LIKELY_SCANNED_PDF
  └─→ OCRmyPDF first
       └─→ ocr_pdf/*.pdf
            └─→ OpenDataLoader on OCR output
                 └─→ raw_markdown/*.md + sidecar_json/*.json
```

### Conversion output structure

For a source file at:
```
001_Raw-Source-Layer/001-Laws/PD-1096/PD 1096 - National Building Code.pdf
```

The conversion layer produces:
```
002_Raw-Conversion-Layer/
└── 001-Laws/
    ├── raw_markdown/PD-1096/PD 1096 - National Building Code.md
    ├── sidecar_json/PD-1096/PD 1096 - National Building Code.json
    └── ocr_pdf/PD-1096/PD 1096 - National Building Code.pdf  (only if scanned)
```

---

## Output Artifacts Reference

Every pipeline command produces both a `latest_` file and a timestamped copy.

| Command | Report Files |
|---------|-------------|
| `scan` | `latest_raw_tree_snapshot.json`, `.txt`, `latest_raw_file_registry.csv` |
| `status` | `latest_status_report.json`, `.txt` |
| `lint` | `latest_lint_report.json`, `.txt` |
| `convert` | `latest_convert_queue.json/.txt`, `latest_convert_batch_report.json/.txt`, `latest_ocr_needed_report.json/.txt` |
| `convert-one` | `latest_convert_one_report.json`, `.txt` |
| `detect-one` | `latest_detect_one_report.json`, `.txt` |
| `reconcile` | `latest_reconcile_report.json`, `.txt` |
| `ocr-queue` | `latest_ocr_queue_report.json`, `.txt` |
| `ocr-execute` | `latest_ocr_execute_report.json`, `.txt` |

Additionally, every conversion (successful or failed) appends a row to:
- `006_System-Manifests/registries/latest_conversion_registry.csv`

---

## Content Trust Order

**Never treat raw source files or raw extracted text as final truth.**

Trust order:

1. **Canonical Knowledge Layer** — curated and verified
2. **Raw Conversion Layer** — machine-extracted, unverified
3. **Raw Source Layer** — original evidence, unprocessed

This rule is fundamental to the integrity of the knowledge system.

---

## Raw Source Layer Rules

The raw source layer should contain **only** source knowledge assets.

**Good examples:** laws, books, reviewers, manuals, technical references, scans, official circulars, guidance documents

**Bad examples:** logs, pipeline scripts, temporary working notes, generated Markdown, converted outputs, random office automation files

If a file is not a source knowledge asset, it does not belong in `001_Raw-Source-Layer/`.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pypdf` | PDF page reading and text extraction for detection |
| `opendataloader-pdf` | PDF-to-Markdown and PDF-to-JSON conversion |
| `ocrmypdf` | OCR processing of scanned PDFs (wraps Tesseract) |

---

## Design Philosophy

Vitruvius is built **local-first** because:

- The dataset is local and large
- The dataset is still actively changing
- Source control and traceability matter
- Canonical knowledge must be built carefully before online deployment
- Every conversion and transformation must be auditable

This project is meant to become the **knowledge foundation** behind later systems — not just a one-off script collection.

---

## Current Status

As of the current stage:

- [x] Project structure initialized across all six layers
- [x] Raw layer scanning and tree snapshot generation
- [x] CSV file registry generation
- [x] Change detection between scans (status)
- [x] Raw layer linting (non-PDF detection, duplicate filename detection)
- [x] PDF text vs scanned detection
- [x] Single-file and batch PDF-to-Markdown conversion via OpenDataLoader
- [x] OCR queue building and OCRmyPDF execution for scanned PDFs
- [x] Conversion registry tracking (append-only CSV)
- [x] Reconciliation of missing sources and stale outputs
- [x] Pipeline modularized into the `vitruvius` package
- [ ] Canonical knowledge page generation
- [ ] Chunking for retrieval
- [ ] Embedding generation
- [ ] Knowledge graph construction
- [ ] Derived content generation (articles, questions, flashcards)

---

## Quick Start

```bash
# Run the full pipeline (scan → status → lint)
python scripts/pipeline_cli.py run

# Convert all new/changed PDFs
python scripts/pipeline_cli.py convert

# Detect a single PDF type
python scripts/pipeline_cli.py detect-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"

# Convert a single text PDF
python scripts/pipeline_cli.py convert-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"

# Run OCR on scanned PDFs
python scripts/pipeline_cli.py ocr-execute --languages eng

# Check for stale outputs
python scripts/pipeline_cli.py reconcile
```
