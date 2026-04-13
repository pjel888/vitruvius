# Vitruvius

Vitruvius is a local-first knowledge pipeline for building a structured architecture dataset that can later power:

- a local RAG system
- a local wiki-style knowledge base
- AI-assisted article generation
- AI-assisted question generation
- graph-based knowledge relationships
- future online products such as Slatecamp

This repository is not the learner-facing app.
This repository is the **knowledge and pipeline engine** behind it.

---

## Core idea

Vitruvius is built around a layered workflow.

### 1. Raw Source Layer
This is the archive of original source material.

Examples:
- PDFs
- laws
- books
- reviewer handouts
- lecture notes
- scanned documents
- future DOCX, PPTX, XLSX, and other source formats

This layer is **evidence storage**, not trusted knowledge.

### 2. Raw Conversion Layer
This is where source files are converted into machine-readable text outputs.

Examples:
- raw Markdown
- OCR outputs
- parser sidecar JSON
- extracted assets such as tables or images

This layer is still not the final knowledge layer.
It is only a usable machine extraction layer.

### 3. Canonical Knowledge Layer
This is the trusted knowledge layer.

This is where Vitruvius will eventually maintain:
- cleaned topic pages
- law summaries
- provision pages
- structured concept pages
- source-backed knowledge articles
- update history and provenance

This is the layer the AI should trust first.

### 4. Derived Content Layer
This is for learner-facing and AI-generated outputs such as:
- articles
- question banks
- flashcards
- learning paths
- explainers
- summaries

### 5. Operational Intelligence Layer
This is for machine-use infrastructure such as:
- chunks
- embeddings
- graph nodes
- graph edges
- retrieval indexes
- caches
- pipeline artifacts

### 6. System Manifests
This is the control and audit layer.

It stores:
- tree snapshots
- file registries
- run reports
- lint reports
- status reports
- future lineage and conversion logs

---

## Important rule

**Never treat raw source files or raw extracted text as final truth.**

Trust order should be:

1. Canonical Knowledge Layer
2. Raw Conversion Layer
3. Raw Source Layer

That rule is fundamental.

---

## Repository structure

```text
Vitruvius/
├── 001_Raw-Source-Layer/
├── 002_Raw-Conversion-Layer/
├── 003_Canonical-Knowledge-Layer/
├── 004_Derived-Content-Layer/
├── 005_Operational-Intelligence-Layer/
├── 006_System-Manifests/
├── config/
├── docs/
└── scripts/
    └── pipeline_cli.py
```

---

## First command to run

**Always run the pipeline first after adding, deleting, or changing files in the raw source layer.**

Command:

```bash
python scripts/pipeline_cli.py run
```

This is the first command that should be run before doing anything else.

At the current stage of the project, `run` performs:

1. `scan`
2. `status`
3. `lint`

---

## Current CLI commands

### `run`
```bash
python scripts/pipeline_cli.py run
```
Runs the core pipeline sequence.

Current behavior:
- scans the raw source layer
- writes updated tree snapshots
- writes updated raw file registries
- compares the latest scan to the previous scan
- writes status reports
- checks the raw layer for obvious hygiene issues
- writes lint reports

Use this command first.

---

### `scan`
```bash
python scripts/pipeline_cli.py scan
```
Scans the raw source layer and writes:
- JSON tree snapshot
- TXT tree snapshot
- CSV raw file registry

Use when you only want a fresh snapshot without running comparison or lint.

---

### `status`
```bash
python scripts/pipeline_cli.py status
```
Compares the two latest timestamped file registries and reports:
- new files
- changed files
- missing files
- unchanged files

Use when you want to know what changed between scans.

---

### `lint`
```bash
python scripts/pipeline_cli.py lint
```
Checks the latest raw file registry for obvious issues.

Current behavior:
- flags non-PDF files in the raw source layer
- flags duplicate-like filenames

This command is meant to catch hygiene problems before conversion work begins.

---

## Current outputs written by the pipeline

### Tree snapshots
Location:

```text
006_System-Manifests/tree-snapshots/
```

Files produced:
- `latest_raw_tree_snapshot.json`
- `latest_raw_tree_snapshot.txt`
- timestamped versions of both

---

### Raw file registries
Location:

```text
006_System-Manifests/registries/
```

Files produced:
- `latest_raw_file_registry.csv`
- timestamped CSV registries

---

### Status reports
Location:

```text
006_System-Manifests/runs/
```

Files produced:
- `latest_status_report.json`
- `latest_status_report.txt`
- timestamped versions of both

---

### Lint reports
Location:

```text
006_System-Manifests/runs/
```

Files produced:
- `latest_lint_report.json`
- `latest_lint_report.txt`
- timestamped versions of both

---

## Basic workflow

### When adding new files to the dataset

1. Put the files into the correct place inside `001_Raw-Source-Layer/`
2. Run:

```bash
python scripts/pipeline_cli.py run
```

3. Review the output in:
   - `006_System-Manifests/tree-snapshots/`
   - `006_System-Manifests/registries/`
   - `006_System-Manifests/runs/`

4. Check whether there are:
   - new files
   - changed files
   - missing files
   - non-PDF files in the raw layer
   - duplicate-like groups that may need review

### Current discipline

Do not manually edit outputs inside:
- `006_System-Manifests/tree-snapshots/`
- `006_System-Manifests/registries/`
- `006_System-Manifests/runs/`

These are generated artifacts.

---

## Raw Source Layer rules

The raw source layer should contain only source knowledge assets.

Good examples:
- laws
- books
- reviewers
- manuals
- technical references
- scans
- official circulars
- guidance documents

Bad examples:
- logs
- pipeline scripts
- temporary working notes
- generated Markdown
- converted outputs
- random office automation files

If a file is not a source knowledge asset, it should not live in `001_Raw-Source-Layer/`.

---

## Naming and organization guidance

### For folders
Use clean, stable names.

Examples:
- `001-Laws`
- `002-History`
- `003-Theory`
- `004-Technology`
- `005-Utilities`
- `006-Structural`
- `007-Planning`
- `008-Design`
- `009-Practice`

Avoid creating alternate variants of the same folder name.

### For source files
Keep original names when useful for traceability, but avoid introducing unnecessary duplicates.

Do not delete duplicates blindly.
Some duplicate-like files may be intentional cross-postings across categories.

---

## Current scope of `pipeline_cli.py`

At this stage, `pipeline_cli.py` is the entrypoint for:
- scanning
- registry writing
- change detection
- raw layer linting

It is **not yet** doing:
- conversion to Markdown
- OCR execution
- canonical page generation
- chunking
- embeddings
- graph generation
- article generation
- question generation

Those come later.

---

## Planned next stages

Planned future commands and responsibilities may include:

- `convert`
  - identify files requiring conversion
  - convert raw files into raw Markdown and sidecar metadata

- `canonicalize`
  - compile raw conversions into trusted canonical knowledge pages

- `derive`
  - generate articles, questions, flashcards, and summaries from canonical knowledge

- `graph`
  - generate graph nodes and edges from canonical knowledge

- `embed`
  - generate embeddings and retrieval assets

---

## Design philosophy

Vitruvius is being built local-first because:
- the dataset is local
- the dataset is still actively changing
- source control and traceability matter
- canonical knowledge must be built carefully before online deployment

This project is meant to become the knowledge foundation behind later systems, not just a one-off script collection.

---

## Quick start

### Run the pipeline

```bash
python scripts/pipeline_cli.py run
```

### Scan only

```bash
python scripts/pipeline_cli.py scan
```

### Compare latest scans

```bash
python scripts/pipeline_cli.py status
```

### Lint the raw layer

```bash
python scripts/pipeline_cli.py lint
```

---

## Current status

As of the current stage:
- project structure has been initialized
- scan works
- registry generation works
- status comparison works
- lint works
- `run` is the standard first command

That is the current minimum viable backbone for Vitruvius.
