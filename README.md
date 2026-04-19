# Vitruvius

```
 ██╗   ██╗██╗████████╗██████╗ ██╗   ██╗██╗   ██╗██╗██╗   ██╗███████╗
 ██║   ██║██║╚══██╔══╝██╔══██╗██║   ██║██║   ██║██║██║   ██║██╔════╝
 ██║   ██║██║   ██║   ██████╔╝██║   ██║██║   ██║██║██║   ██║███████╗
╚██╗ ██╔╝██║   ██║   ██╔══██╗██║   ██║╚██╗ ██╔╝██║██║   ██║╚════██║
 ╚████╔╝ ██║   ██║   █║  ██║╚██████╔╝ ╚████╔╝ ██║╚██████╔╝███████║
  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝

   ─────────────────────────────────────────────────────────────────
     An auditable document-to-knowledge engine for technical rule systems.
         Building toward compliance-grade reasoning and AEC decision support.
                    Firmitas · Utilitas · Venustas
   ─────────────────────────────────────────────────────────────────
```

**Vitruvius is a local-first, governance-first knowledge pipeline** that converts messy professional-domain source documents — statutes, codes, technical standards, scanned references — into a validated, queryable, evidence-backed knowledge graph.

> **Current product posture:** Pre-launch MVP. The goal is the most effective, accurate, and truthful knowledge foundation possible, not broad backwards compatibility with every intermediate artifact shape created during development.

---

## Table of Contents

- [What Vitruvius Does Today](#what-vitruvius-does-today)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Common Workflows](#common-workflows)
- [CLI Reference](#cli-reference)
- [Knowledge Graph v2](#knowledge-graph-v2)
- [Dataset Automation (Laws Wave)](#dataset-automation-laws-wave)
- [Testing](#testing)
- [Current Status](#current-status)
- [Documentation](#documentation)

---

## What Vitruvius Does Today

Vitruvius ingests heterogeneous source material and progressively hardens it through deterministic, auditable stages:

```
Raw docs → Parse / OCR → Normalize → Canonicalize → Extract → Review → Promote → Graph
```

**Core pipeline (operational):**
- **Scan & registry** — SHA-256 hashing, CSV registries, tree snapshots
- **Multi-route conversion** — text PDFs via OpenDataLoader, scanned PDFs via OCRmyPDF, Office via LibreOffice, spreadsheets via openpyxl
- **Normalization (Tier A/B)** — Unicode NFC, whitespace collapse, Setext→ATX heading conversion, section identifier normalization
- **Canonicalization** — Rules-driven ID assignment (`law-national-building-code`), YAML frontmatter, structured sections
- **Relationship extraction** — Regex-based, concept-aware, section-anchored with `source_section_id`
- **LLM review (Tier 1/2)** — Local Ollama review with `keep`/`review_further`/`reject` decisions, confidence scoring, second-pass adjudication
- **Promotion governance** — 17-rule validator, audit log, dry-run default, rollback support
- **Graph building** — JSON snapshot graph with integrity checks (orphan detection, dangling edge detection)
- **Unified KG pipeline** — Single command `run-kg-pipeline` goes from raw PDFs → refined markdown → canonical sources → extracted relationships → LLM review → promotion → KG v2 snapshot

**Cross-cutting systems (feature-flagged):**
- **Knowledge Graph v2** — Taxonomy-centered canonical graph with separate evidence layer, reified assertions, deterministic validation gates
- **Dataset automation** — Manifest-backed, tranche-by-tranche laws-wave pipeline with duplicate detection, OCR-first preparation, and concept-fit admission
- **Spatial intelligence** — TypeScript spatial daemon (GJK/AABB), Z3 constraint solver, IFC/OWL ontology export
- **Compound AI** — Adversarial swarm, differential dataflow, neuro-symbolic Datalog bridge, DSPy prompt compiler
- **Interactive Graph Explorer** — React 19 + vis-network browser app with search, path tracing, Cypher query panel, edge inspection, and neighbor expansion. Code-split main bundle (~294 KB).
- **High-performance backends** — RocksDB event store (18.7× faster than SQLite), GraphSAGE product quantization (32× compression), MinHash LSH fuzzy dedup

---

## Architecture Overview

Vitruvius is built as a **layered, filesystem-centric pipeline**. The filesystem is the database for document lineage; operational indexes (RocksDB, optional Neo4j/PostgreSQL) are queryable replicas.

| Layer | Folder | Role |
|---|---|---|
| 1 | `001_Raw-Source-Layer/` | Immutable input. Original PDFs, Office docs, scans. |
| 2 | `002_Raw-Conversion-Layer/` | Machine extracts. Markdown + JSON sidecars. (Git-ignored) |
| 3 | `003_Canonical-Knowledge-Layer/` | **The Brain.** Hardcoded trusted knowledge. |
| 4 | `004_Derived-Content-Layer/` | HTML visualizations, articles, summaries. (Git-ignored) |
| 5 | `005_Operational-Intelligence-Layer/` | Graph snapshots, embeddings, chunks. (Git-ignored) |
| 6 | `006_System-Manifests/` | Registries, run reports, audit logs. |

**Content trust order:** Canonical > Raw Conversion > Raw Source.

---

## Prerequisites

| Requirement | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Core runtime |
| Ollama | Latest | Local LLM review (default: `llama3.1:8b`) |
| Java | OpenJDK 21+ | PDF-to-Markdown conversion (docling/OpenDataLoader) |
| Node.js | 25+ | `spatial-daemon/` TypeScript subproject |

**Optional:**
- Neo4j Community/Enterprise — canonical graph index (KG v2)
- PostgreSQL 15+ — relational registry (KG v2)
- Rust toolchain — `engine_rs` pyo3 workspace (spatial kernels, stats kernels, PDF parser)

---

## Setup & Installation

One-time setup before you can run any pipeline commands. Instructions are provided for both platforms.

### 1. Clone or navigate to the repository

**macOS:**
```bash
cd /Users/philiplewis/vitruvius
```

**Windows:**
```powershell
cd C:\Users\philiplewis\vitruvius
```

### 2. Create and activate a Python virtual environment

**macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

> `.venv/` is already in `.gitignore` — it will never be committed.

### 3. Install Python dependencies

**Both platforms:**
```bash
pip install -r requirements.txt
```

This installs:
- `pypdf`, `opendataloader-pdf`, `ocrmypdf` — PDF processing
- `PyYAML`, `openpyxl` — config and spreadsheet handling
- `numpy`, `scipy`, `scikit-learn`, `networkx` — scientific stack
- `spacy`, `sentence-transformers` — NLP and embeddings
- `neo4j`, `psycopg[binary]`, `pydantic` — KG v2 backends and schemas
- `rocksdict` — high-performance KV store

### 4. Download the spaCy language model

**Both platforms:**
```bash
python -m spacy download en_core_web_sm
```

Required for SVO (subject-verb-object) extraction in relationship detection.

### 5. Verify the installation

**Both platforms:**
```bash
python scripts/pipeline_cli.py --help
```

You should see the full list of available commands.

### 6. (Optional) Install backend services

#### Neo4j — for KG v2 graph indexing

**macOS (Homebrew):**
```bash
brew install neo4j
brew services start neo4j
```

**Windows:**
```powershell
# Option A: Download Neo4j Desktop from https://neo4j.com/download/ and run the installer
# Option B: Use Docker
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

Verify at http://localhost:7474 (default user: `neo4j`, password: `password`)

#### PostgreSQL — for KG v2 relational registry

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb vitruvius
psql -d vitruvius -c "CREATE ROLE postgres WITH LOGIN PASSWORD 'password';"
```

**Windows:**
```powershell
# Option A: Download installer from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
# Option B: Use Chocolatey
choco install postgresql15

# Option C: Use Docker
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=vitruvium postgres:15
```

#### Ollama — for local LLM review

**macOS:**
```bash
brew install ollama
ollama serve
```

**Windows:**
```powershell
# Download and install from https://ollama.com/download/windows
# Then in a new terminal:
ollama serve
```

**Pull review models (both platforms):**
```bash
# Default — runs on both machines
ollama pull llama3.1:8b

# High-quality — desktop only (64GB RAM)
ollama pull gemma4:31b

# Lightweight — MacBook fast iteration (8GB RAM)
ollama pull qwen2.5:3b
```

### 7. (Optional) Rust toolchain

Only needed if you want to build the Rust compute modules (`engine_rs/`):

**macOS:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

**Windows:**
```powershell
# Download and run rustup-init.exe from https://rustup.rs/
# Or in PowerShell:
Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
.\rustup-init.exe
```

---

## Quick Start

This section gives you the six most common commands to go from raw documents to a working knowledge graph. Each step is explained below in more detail in [Common Workflows](#common-workflows).

### 1. Baseline pipeline (scan → status → lint)

```bash
python scripts/pipeline_cli.py run
```

This inventories every file in `001_Raw-Source-Layer/`, writes SHA-256 registries to `006_System-Manifests/registries/`, compares them to the previous run, and reports hygiene issues (non-PDF files, suspicious duplicates). Think of it as `git status` for your document corpus.

### 2. Convert raw documents

```bash
python scripts/pipeline_cli.py convert
```

This finds every new or changed file since the last run and sends it through the correct converter: text PDFs through OpenDataLoader, scanned PDFs through OCRmyPDF, spreadsheets through openpyxl, and Office documents through LibreOffice. Outputs land in `002_Raw-Conversion-Layer/`.

### 3. Refine and canonicalize

```bash
python scripts/pipeline_cli.py refine
python scripts/pipeline_cli.py canonicalize
```

`refine` batch-cleans the raw conversion markdown (collapses whitespace, normalizes section identifiers, converts Setext headings to ATX). `canonicalize` writes the cleaned files into `003_Canonical-Knowledge-Layer/` with stable IDs, YAML frontmatter, and structured sections.

### 4. Extract and review relationships

```bash
python scripts/pipeline_cli.py extract-relationships-sections-one "001-Laws/PD-1096/PD 1096.md"
python scripts/pipeline_cli.py review-relationships-ollama
```

The first command extracts candidate relationships from a single canonical file with section anchors. The second sends those candidates through a local Ollama model for keep/reject/review-further decisions.

### 5. Build the graph

```bash
python scripts/pipeline_cli.py build-graph
python scripts/pipeline_cli.py visualize-graph
```

`build-graph` reads every canonical node and relationship in Layer 3, validates integrity (no orphans, no dangling edges), and writes a JSON snapshot to Layer 5. `visualize-graph` renders an interactive HTML page in Layer 4.

### 6. Run the full composite path

```bash
python scripts/pipeline_cli.py run-with-review
```

This is the one-shot operator path: scan, status, lint, convert, refine, canonicalize, extract, review. Use it when you want the pipeline to handle everything after you drop new files into `001_Raw-Source-Layer/`.

---

## Running the App

This section tells you exactly how to run Vitruvius on your machines, with copy-paste commands for each.

### Your Machines

| Machine | Specs | Best For |
|---------|-------|----------|
| **Desktop** | Intel i9, 64GB RAM, RTX 4070 12GB | Full production runs, high-quality LLM review, parallelism |
| **MacBook Pro** | Apple M2, 8GB unified RAM | Development, iteration, lightweight review, single-subject tests |

> The bottleneck is always **Phase 3 — LLM Review**. Everything else (PDF conversion, canonicalization, snapshot building) runs on CPU and is merely slow. Review loads a multi-billion-parameter model into memory.

### One-Command: Raw Data → Knowledge Graph

After dropping PDFs into `001_Raw-Source-Layer/`, this single command runs the full pipeline:

**Desktop (recommended — best quality):**

```bash
# Full corpus with high-quality review (gemma4:31b, 4 parallel workers)
python scripts/pipeline_cli.py run-kg-pipeline --all \
  --review-model-preset high-quality \
  --review-parallel 4

# Or with the default model (llama3.1:8b) — still excellent, faster
python scripts/pipeline_cli.py run-kg-pipeline --all
```

**MacBook Pro M2 8GB:**

```bash
# Single subject with lightweight review (qwen2.5:3b, fits in 8GB)
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --tier lightweight

# Or skip AI review entirely for fast pipeline testing
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --skip-review

# Heavy tier with default model (llama3.1:8b, ~4.9GB — close all other apps first)
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --tier heavy
```

### What Happens

| Phase | Step | Time (Desktop) | Time (MacBook) |
|-------|------|----------------|----------------|
| 1 | Scan → Convert → Refine | 2–4 hrs | 8–12 hrs |
| 2 | Canonicalize | minutes | minutes |
| 3 | Extract → LLM Review | 2–4 hrs (31B, p=4) | 3–6 hrs (3B) or 4–8 hrs (8B) |
| 4 | Promote → Build KG v2 snapshot | minutes | minutes |
| | **Total** | **~4–8 hrs** | **~11–20 hrs** |

> MacBook thermal-throttles during long conversion runs. Expect it to get hot and slow after the first hour. Close all other apps before running review.

### Changing the AI Model for Better Results

The `--review-model-preset` flag bundles model + timeout + parallelism. Pick one:

| Preset | Model | Size | Min RAM | Quality | Best For |
|--------|-------|------|---------|---------|----------|
| `high-quality` | `gemma4:31b` | ~16–20GB | 24GB+ | **Highest** | Desktop production runs |
| `default` | `llama3.1:8b` | ~4.9GB | 8GB | Very Good | Desktop or MacBook |
| `8gb-safe` | `llama3.1:8b` | ~4.9GB | 8GB | Very Good | MacBook (longer timeout) |
| `ultra-light` | `qwen2.5:3b` | ~1.9GB | 4GB | Okay | MacBook fast iteration |

**Examples:**

```bash
# Desktop — absolute best quality (recommended for production truth)
python scripts/pipeline_cli.py run-kg-pipeline --all \
  --review-model-preset high-quality \
  --review-parallel 4

# Desktop — good quality, single worker (if doing other things)
python scripts/pipeline_cli.py run-kg-pipeline --all \
  --review-model-preset default

# MacBook — safest option, guaranteed to fit in RAM
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws \
  --review-model-preset ultra-light

# MacBook — better quality, but close every other app first
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws \
  --review-model-preset 8gb-safe
```

**Fine-grained control** (override any preset):

```bash
python scripts/pipeline_cli.py run-kg-pipeline --all \
  --review-model llama3.1:8b \
  --review-timeout-seconds 900 \
  --review-parallel 2
```

### Dry-Run First (Recommended)

See what would happen without actually doing it:

```bash
python scripts/pipeline_cli.py run-kg-pipeline --dry-run

# Or dry-run with your chosen model preset
python scripts/pipeline_cli.py run-kg-pipeline --dry-run \
  --review-model-preset high-quality
```

### Full Pipeline: Raw PDFs → Knowledge Graph (with Neo4j)

Run everything from raw sources through to the Neo4j graph in one command:

```bash
python scripts/pipeline_cli.py run-kg-pipeline \
  --subject 001-Laws \
  --force \
  --ensure-neo4j \
  --review-model-preset high-quality \
  --review-parallel 4
```

**What will happen:**

1. **Phase 1** — Converts all Laws PDFs to markdown, then refines them
2. **Phase 2** — Canonicalizes all refined markdown into `003_Canonical-Knowledge-Layer`
3. **Phase 3** — Extracts relationships, runs LLM review, promotes valid ones
4. **Phase 4** — Builds the unified KG v2 JSON snapshot
5. **Phase 5** — Loads everything into Neo4j automatically

**Heads up:** This will take a while. 182 PDF conversions alone can run for hours depending on file sizes. The pipeline prints progress after each phase.

**While it runs:** Keep http://localhost:7474/browser/ open. After Phase 5 completes, refresh the browser and run:

```cypher
MATCH (n) RETURN count(n)
```

To see how many nodes were loaded.

**Neo4j lifecycle commands:**

```bash
# Start Neo4j (auto-downloads Community edition if missing)
python scripts/pipeline_cli.py neo4j-start

# Stop Neo4j
python scripts/pipeline_cli.py neo4j-stop
```

### After the Run

Your outputs will be in:

| Artifact | Location |
|----------|----------|
| KG v2 snapshot | `005_Operational-Intelligence-Layer/graph/kg-v2/snapshot.json` |
| Visualization | `004_Derived-Content-Layer/graph-visualizations/kg-v2.html` |
| Canonical sources | `003_Canonical-Knowledge-Layer/shared/sources/` |
| Canonical relationships | `003_Canonical-Knowledge-Layer/shared/relationships/` |
| Run report | `006_System-Manifests/runs/kg_pipeline_report_*.json` |

Open the visualization:

```bash
open 004_Derived-Content-Layer/graph-visualizations/kg-v2.html
```

### Quick Iteration Loop (Development)

Use this on your MacBook when tuning extraction or testing pipeline changes:

```bash
# 1. Reset derived artifacts for a clean run
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws \
  --reset --force-reset

# 2. Run with lightweight review
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws \
  --tier lightweight

# 3. Inspect the snapshot
python scripts/pipeline_cli.py kg-validate-assertions
python scripts/pipeline_cli.py kg-detect-contradictions

# 4. Re-visualize after fixes
python scripts/pipeline_cli.py visualize-graph \
  --snapshot 005_Operational-Intelligence-Layer/graph/kg-v2/snapshot.json \
  --version v2
```

---

## Common Workflows

This section walks through the day-to-day tasks an operator performs with Vitruvius. Each workflow is a sequence of commands with explanations of what happens at each step and what files are produced.

---

### Workflow A: "I have a new PDF to add"

**Goal:** Ingest one new document and make it queryable in the graph.

**Step 1 — Drop the file into the raw layer**

Copy your PDF into the appropriate folder under `001_Raw-Source-Layer/`:

```bash
cp "my-document.pdf" "001_Raw-Source-Layer/001-Laws/My-Family/my-document.pdf"
```

**Step 2 — Scan and check status**

```bash
python scripts/pipeline_cli.py run
```

What happens:
- Every file in `001_Raw-Source-Layer/` gets SHA-256 hashed
- A new registry CSV is written to `006_System-Manifests/registries/`
- The CLI compares the new registry to the previous one and reports:
  - New files (your PDF)
  - Changed files (if any were modified)
  - Missing files (if any were removed)
- The linter checks for non-PDF files and suspicious duplicate filenames

**Step 3 — Detect if the PDF needs OCR**

```bash
python scripts/pipeline_cli.py detect-one "001_Raw-Source-Layer/001-Laws/My-Family/my-document.pdf"
```

What happens:
- The CLI samples pages from the PDF and checks for extractable text
- If the PDF is text-usable, it will be converted directly
- If it is scan-like (image-based), it will be queued for OCR

**Step 4 — Convert the document**

```bash
python scripts/pipeline_cli.py convert
```

What happens:
- New and changed files are sent through the appropriate converter
- Text PDFs → OpenDataLoader → Markdown
- Scan-like PDFs → OCRmyPDF → text PDF → Markdown
- Office docs → LibreOffice → Markdown
- Spreadsheets → openpyxl → CSV + JSON
- Outputs land in `002_Raw-Conversion-Layer/`

If your PDF was scan-like and needs OCR:

```bash
python scripts/pipeline_cli.py ocr-queue
python scripts/pipeline_cli.py ocr-execute
```

**Step 5 — Refine the conversion output**

```bash
python scripts/pipeline_cli.py refine
```

What happens:
- Markdown from `002_Raw-Conversion-Layer/` is batch-cleaned
- Unicode NFC normalization, whitespace collapse
- Setext headings converted to ATX (`## Heading`)
- Section identifiers normalized (`Sec. 101` → `Section 101`)
- Refined outputs overwrite the conversion layer files

**Step 6 — Canonicalize**

```bash
python scripts/pipeline_cli.py canonicalize
```

What happens:
- Each refined file gets a stable canonical ID (`law-my-document`)
- YAML frontmatter is generated (id, title, page_type, canonical_status)
- The file is written to `003_Canonical-Knowledge-Layer/shared/sources/`
- If a file with the same ID already exists, the canonicalizer compares content and either skips (unchanged) or rejects (protected status)

**Step 7 — Extract relationships**

```bash
python scripts/pipeline_cli.py extract-relationships-sections-one \
  "003_Canonical-Knowledge-Layer/shared/sources/my-document.md"
```

What happens:
- Regex patterns scan the canonical file for relationship language
  - `governs`, `defines`, `requires`, `limits`, `supersedes`, etc.
- Each candidate is anchored to a section ID (`source_section_id`)
- A pre-review filter auto-accepts obvious matches and auto-rejects junk
- Candidates are written to `006_System-Manifests/runs/.../extraction_report.json`

**Step 8 — Review with Ollama**

```bash
python scripts/pipeline_cli.py review-relationships-ollama
```

What happens:
- Each candidate not filtered in Step 7 is sent to a local LLM
- The LLM returns `keep`, `review_further`, or `reject` with confidence
- Results are written to `006_System-Manifests/runs/.../review_report.json`
- You can inspect the JSON or the companion `.txt` summary

**Step 9 — Promote approved relationships**

```bash
python scripts/pipeline_cli.py promote --execute
```

What happens:
- High-confidence `keep` decisions are validated against 17 governance rules
- Valid relationships are written to `003_Canonical-Knowledge-Layer/shared/relationships/`
- An audit log entry is appended to the promotion batch log
- Without `--execute`, this runs in dry-run mode (recommended first time)

**Step 10 — Build the graph**

```bash
python scripts/pipeline_cli.py build-graph
python scripts/pipeline_cli.py visualize-graph
```

What happens:
- All canonical nodes (sources, concepts, relationships) are loaded
- Integrity checks run (orphan detection, dangling edge detection)
- A JSON snapshot is written to `005_Operational-Intelligence-Layer/graph/`
- An interactive HTML visualization is written to `004_Derived-Content-Layer/graph-visualizations/`

Open the HTML file in a browser to explore your graph.

---

### Workflow B: "I want to review extracted relationships"

**Goal:** Understand what the pipeline found and decide what to promote.

**Step 1 — Run extraction**

```bash
python scripts/pipeline_cli.py extract-relationships-sections-one \
  "003_Canonical-Knowledge-Layer/shared/sources/my-document.md" \
  --json-out my-extraction.json \
  --txt-out my-extraction.txt
```

The `--json-out` and `--txt-out` flags let you specify explicit output paths instead of the default `006_System-Manifests/runs/` location.

**Step 2 — Inspect extraction output**

Open `my-extraction.txt` in your editor. You will see:
- Auto-accepted candidates (structural patterns, high occurrence count)
- Auto-rejected candidates (too short, self-reference, endpoint not in evidence)
- Candidates marked `needs_review` (these go to the LLM)

**Step 3 — Run Tier-1 review**

```bash
python scripts/pipeline_cli.py review-relationships-ollama \
  --input-report my-extraction.json \
  --review-json-out my-review.json \
  --review-txt-out my-review.txt \
  --model llama3.1:8b
```

What happens:
- Every `needs_review` candidate is sent to the specified Ollama model
- The model evaluates the evidence text and returns a decision
- You get a JSON report and a human-readable `.txt` summary

**Step 4 — Inspect review output**

Open `my-review.txt`. Each entry shows:
- The candidate (`from` → `to`, predicate)
- The LLM decision (`keep`, `reject`, `review_further`)
- Confidence score and reasoning

**Step 5 — Run Tier-2 adjudication (optional)**

If you have many `review_further` results and want a second opinion:

```bash
python scripts/pipeline_cli.py review-relationships-ollama-second-pass \
  --input-review-report my-review.json \
  --merged-out my-merged-review.json \
  --worklist-out my-human-worklist.txt
```

What happens:
- A different model (default: `qwen3:30b`) re-evaluates uncertain Tier-1 results
- Tier-1 `keep` results are preserved
- Tier-2 upgrades some `review_further` to `keep` or downgrades to `reject`
- Anything still uncertain is written to a human worklist

**Step 6 — Promote**

```bash
python scripts/pipeline_cli.py promote --execute \
  --input-report my-merged-review.json
```

---

### Workflow C: "I want to build and query the graph"

**Goal:** Turn canonical knowledge into a queryable graph and explore it.

**Step 1 — Build the snapshot**

```bash
python scripts/pipeline_cli.py build-graph
```

What happens:
- Reads all canonical nodes from `003_Canonical-Knowledge-Layer/shared/`
- Loads sources, concepts, relationships
- Validates integrity:
  - Every edge endpoint must exist (no dangling edges)
  - Every node must have at least one edge or be flagged as an orphan
- Writes a timestamped JSON snapshot to `005_Operational-Intelligence-Layer/graph/`

**Step 2 — Visualize**

**Option A: Static HTML visualization (no server needed)**

```bash
# Auto-detects snapshot version (v1 or v2) and renders appropriate viewer
python scripts/pipeline_cli.py visualize-graph

# Force v2 viewer for KG v2 snapshots
python scripts/pipeline_cli.py visualize-graph \
  --snapshot 005_Operational-Intelligence-Layer/graph/kg-v2/snapshot_repaired.json \
  --version v2 \
  --out 004_Derived-Content-Layer/graph-visualizations/kg-v2.html
```

Opens a self-contained HTML file in your browser.

**Option B: Interactive Graph Explorer (full-featured React app)**

```bash
# 1. Start the Graph API (serves data from Neo4j)
cd api && bun run index.ts

# 2. In another terminal, start the explorer dev server
cd explorer && bun run dev --host

# 3. Open http://localhost:5173
```

The explorer provides:
- **Live search** — fuzzy node search with keyboard navigation
- **Node inspector** — evidence spans, taxonomy path, incoming/outgoing relationships
- **Edge inspector** — click any edge to see confidence, reasoning, and source/target
- **Path tracer** — select two nodes and find the shortest path between them
- **Cypher query panel** — run custom read-only Cypher queries against Neo4j
- **Context menu** — right-click to expand neighbors, focus subgraph, hide nodes
- **Perspectives** — switch between All Knowledge, Concepts Only, Taxonomy Browser, Regulatory Rules, Evidence Map
- **Layouts** — ForceAtlas2, circular, random, clustered by taxonomy, timeline

See [`explorer/README.md`](explorer/README.md) for full details.

**Step 3 — Query by node ID**

```bash
python scripts/pipeline_cli.py query-graph law-pd-1096 concept-building-permit
```

What happens:
- Finds a path between the two nodes in the graph
- Prints the shortest path through intermediate nodes and edges

**Step 4 — Natural-language query**

```bash
python scripts/pipeline_cli.py query "What governs building permits?"
```

What happens:
- Parses the question into a structured graph query
- Searches for nodes and edges matching the intent
- Returns ranked results with evidence snippets

**Step 5 — Structured query**

```bash
python scripts/pipeline_cli.py query-structured get_sources_for_concept \
  --arg concept_id=concept-building-permit
```

What happens:
- Runs a predefined query function against the snapshot
- Returns machine-parseable JSON

---

### Workflow D: "I want to activate and use KG v2"

**Goal:** Enable the taxonomy-centered knowledge graph and build a unified snapshot.

**Step 1 — Enable the feature flag**

Edit `config/vitruvius.yaml` and set:

```yaml
kg_transition:
  enabled: true
```

KG v2 is gated behind this master kill-switch. When `enabled: false`, all KG v2 commands refuse to run and the legacy v1 graph builder remains active.

**Step 2 — Seed taxonomy roots**

```bash
python scripts/pipeline_cli.py kg-seed-taxonomy
```

What happens:
- Creates taxonomy root nodes in the canonical layer
- Example roots: `taxonomy-building-codes`, `taxonomy-structural-design`
- These are the anchor points that concepts will be placed under

**Step 3 — Ingest evidence**

```bash
python scripts/pipeline_cli.py kg-ingest-evidence \
  "003_Canonical-Knowledge-Layer/shared/sources/pd-1096.md"
```

What happens:
- Parses the source document into `DocumentVersion → Section → Chunk → EvidenceSpan`
- Evidence spans carry resolvable selectors (markdown ranges, text ranges, PDF bounding boxes)
- Writes JSONL sidecars to `005_Operational-Intelligence-Layer/graph/kg-v2/`

**Step 4 — Extract candidates**

```bash
python scripts/pipeline_cli.py kg-extract-candidates
```

What happens:
- Runs structured LLM extraction over canonical sources
- Produces `RelationshipAssertion` candidates with validator gating (E1–E9)
- Candidates are stored as JSONL records

**Step 5 — Canonicalize candidates**

```bash
python scripts/pipeline_cli.py kg-canonicalize-candidates
```

What happens:
- Deduplicates candidates by `(from, predicate, to)`
- Normalizes node labels
- Places concepts into the taxonomy if a path is inferable

**Step 6 — Materialize canonical assertions**

```bash
python scripts/pipeline_cli.py kg-materialize-canonical
```

What happens:
- Runs `AssertionValidator` (R1–R14) on all assertions
- Validates endpoint existence, predicate registry compatibility, type consistency
- Materializes fast edges from validated assertions

**Step 7 — Build the unified snapshot**

```bash
python scripts/pipeline_cli.py kg-build-unified
```

What happens:
- Loads taxonomy, concepts, evidence graph, and assertions
- Merges everything into a single `KgV2Snapshot`
- Generates placement assertions for concepts with taxonomy paths
- Materializes fast edges from all assertion types
- Writes a timestamped JSON snapshot to `005_Operational-Intelligence-Layer/graph/kg-v2/`

**Step 8 — Validate and inspect**

```bash
python scripts/pipeline_cli.py kg-validate-assertions
python scripts/pipeline_cli.py kg-detect-contradictions
```

What happens:
- `kg-validate-assertions` runs R1–R14 validation on the unified snapshot
- `kg-detect-contradictions` scans for 4 deterministic contradiction patterns:
  - `OVERRIDES` vs `APPLIES_TO`
  - `REQUIRES` vs `EXCLUDES`
  - Semantic shadowing
  - Weak bidirectional `DEPENDS_ON`

**Step 9 — Query the graph**

```bash
python scripts/pipeline_cli.py kg-query-nodes "building permit"
python scripts/pipeline_cli.py kg-query-neighborhood concept-building-permit
python scripts/pipeline_cli.py kg-inspect-node law-pd-1096
```

What happens:
- `kg-query-nodes` searches canonical nodes by label (case-insensitive)
- `kg-query-neighborhood` shows related nodes with assertion detail
- `kg-inspect-node` prints the full node record and its evidence

**Step 10 — Review queue**

```bash
python scripts/pipeline_cli.py kg-review-queue --status REVIEW_REQUIRED
python scripts/pipeline_cli.py kg-review-action assert-rel-001 --action approve
```

What happens:
- `kg-review-queue` lists assertions needing human review
- `kg-review-action` updates the assertion state (`approve`, `reject`, `escalate`)

---

### Workflow E: "I want to run the full pipeline from raw sources to KG v2"

**Goal:** Take everything in `001_Raw-Source-Layer/` and produce a validated KG v2 snapshot in one command.

**Prerequisites:**
- `kg_transition.enabled: true` in `config/vitruvius.yaml` (already set)
- Ollama running locally (for relationship review)

**Run the unified pipeline**

```bash
python scripts/pipeline_cli.py run-kg-pipeline
```

**What happens (4 phases):**

| Phase | Step | Output layer |
|-------|------|-------------|
| 1 | **Scan** → SHA-256 hash every file in `001/` | `006_System-Manifests/registries/` |
| 1 | **Convert** → PDFs → raw markdown | `002_Raw-Conversion-Layer/raw_markdown/` |
| 1 | **Refine** → Clean markdown (NFC, headings, sections) | `002_Raw-Conversion-Layer/refined_markdown/` |
| 2 | **Canonicalize** → Structured source pages with YAML frontmatter | `003_Canonical-Knowledge-Layer/shared/sources/` |
| 3 | **Extract** → Regex-based relationship candidates per source | `006_System-Manifests/runs/kg_pipeline_*/` |
| 3 | **Review** → Ollama LLM classifies keep / review_further / reject | Same run directory |
| 3 | **Promote** → Approved relationships → canonical records | `003_Canonical-Knowledge-Layer/shared/relationships/` |
| 4 | **Build snapshot** → `UnifiedSnapshotBuilder` merges all layers | `005_Operational-Intelligence-Layer/graph/kg-v2/` |

**Dry-run first (recommended)**

```bash
python scripts/pipeline_cli.py run-kg-pipeline --dry-run
```

This plans all 4 phases without writing anything, so you can see which sources will be processed and how many relationships are expected.

**Skip LLM review (faster, less accurate)**

```bash
python scripts/pipeline_cli.py run-kg-pipeline --skip-review
```

This bypasses the Ollama review step and promotes all extracted relationships. Useful for testing the pipeline end-to-end, but not recommended for production truth.

**Reset and re-run from scratch**

```bash
python scripts/pipeline_cli.py run-kg-pipeline --reset --force-reset
```

This deletes all machine-derived artifacts from previous runs:
- `002_Raw-Conversion-Layer/` — converted/refined markdown
- `003_Canonical-Knowledge-Layer/shared/sources/` — canonical source pages
- `003_Canonical-Knowledge-Layer/shared/relationships/` — promoted relationships
- `005_Operational-Intelligence-Layer/graph/kg-v2/` — old snapshots
- `006_System-Manifests/runs/` — run reports
- `006_System-Manifests/registries/` — scan registries

Then it runs the full pipeline fresh. This is how you test new extraction algorithms or review models against the same raw PDFs.

⚠️ `--force-reset` is required because this is destructive. Original PDFs in `001/`, taxonomy files, and concepts are preserved.

**Process all subjects (with automatic reset)**

```bash
python scripts/pipeline_cli.py run-kg-pipeline --all
```

Same as a full run, but automatically resets derived artifacts first so you start clean. This is the fastest way to do a true end-to-end run when you want everything rebuilt from the raw PDFs.

**Process only specific subject(s)**

```bash
# One subject
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws

# Multiple subjects
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --subject 002-History
```

This restricts every phase to files under the specified `001_Raw-Source-Layer/<subject>/` folders:
- **Phase 1** — Only converts/refines PDFs in the selected subject(s)
- **Phase 2** — Only canonicalizes refined markdown from the selected subject(s)
- **Phase 3** — Only extracts relationships from canonical sources whose original PDF is traced to the selected subject(s)
- **Phase 4** — Builds the snapshot from the filtered results

Useful for testing pipeline changes on a small corpus before running all 341 PDFs, or for iterating on extraction algorithms for a specific domain.

**Combine reset with subject filter**

```bash
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --reset --force-reset
```

This resets all derived artifacts, then re-runs only the laws subject. Other subjects' canonical sources that may exist from prior runs are removed by the reset.

**Customize review settings**

```bash
python scripts/pipeline_cli.py run-kg-pipeline \
  --review-model llama3.1:8b \
  --review-timeout-seconds 300 \
  --review-parallel 4
```

**Use a tier (simplest mental model)**

```bash
# Lightweight tier: qwen2.5:3b for review, nomic-embed-text for embeddings
python scripts/pipeline_cli.py run-kg-pipeline --tier lightweight

# Heavy tier: llama3.1:8b for review (default)
python scripts/pipeline_cli.py run-kg-pipeline --tier heavy

# Heavy tier with the best quality model
python scripts/pipeline_cli.py run-kg-pipeline --tier heavy --review-model-preset high-quality
```

The `--tier` flag is the easiest way to choose your model architecture:
- **`lightweight`** → review uses `qwen2.5:3b`. KG v2 already uses `qwen2.5:3b` + `nomic-embed-text`. Total RAM: ~2.5 GB.
- **`heavy`** → review uses `llama3.1:8b` (or `gemma4:31b` if you also pass `--review-model-preset high-quality`). Total RAM: ~5–20 GB.

**Use a preset (finer control)**

```bash
# Default preset: llama3.1:8b, parallelism=1, timeout=600s
python scripts/pipeline_cli.py run-kg-pipeline --review-model-preset default

# 8GB-safe preset: llama3.1:8b, parallelism=1, timeout=900s (same model, longer timeout)
python scripts/pipeline_cli.py run-kg-pipeline --review-model-preset 8gb-safe

# Ultra-light preset: qwen2.5:3b, parallelism=1, timeout=600s, num_ctx=2048
python scripts/pipeline_cli.py run-kg-pipeline --review-model-preset ultra-light

# High-quality preset: gemma4:31b, parallelism=1, timeout=1200s
python scripts/pipeline_cli.py run-kg-pipeline --review-model-preset high-quality
```

Presets bundle model + timeout + parallelism + context size into one flag. `--tier lightweight` is simply an alias for `--review-model-preset ultra-light`. `--tier heavy` is an alias for `--review-model-preset default`.

**How this differs from other commands:**

| Command | Scope | Graph version |
|---------|-------|---------------|
| `run-with-review` | Scan → Convert → Refine → Review | Stops at review reports |
| `build-graph` | Reads `003/` → v1 snapshot | Legacy v1 |
| `run-laws-pilot` | Manifest-bound laws tranche | Legacy v1 |
| `kg-build-unified` | Reads `003/` → v2 snapshot | KG v2, but requires `003/` already populated |
| **`run-kg-pipeline`** | **001 → 002 → 003 → KG v2** | **Full path, KG v2** |

**Artifacts produced:**
- `006_System-Manifests/runs/kg_pipeline_report_*.json` — structured summary
- `005_Operational-Intelligence-Layer/graph/kg-v2/snapshot.json` — the final KG v2 snapshot
- `003_Canonical-Knowledge-Layer/shared/relationships/rel-*.md` — promoted canonical relationships

---

### Hardware Guide: Which Machine Should Run What?

Your two machines have very different capabilities. This section tells you exactly what each can handle, what will fail, and how to work around it.

**Your machines:**
- **Machine A:** MacBook Pro M2, 8GB unified RAM
- **Machine B:** Desktop — Intel i9, 64GB RAM, RTX 4070 12GB VRAM

**The bottleneck is always Phase 3 — LLM Review.** Everything else (PDF conversion, canonicalization, snapshot building) runs on CPU and is merely slow. The AI review step loads a multi-billion-parameter model into memory and runs inference on every extracted relationship candidate.

#### Model Sizes vs RAM Requirements

| Model | Parameters | Quantized Size | Minimum RAM | Quality | Notes |
|-------|-----------|----------------|-------------|---------|-------|
| `llama3.1:8b` (default) | 8B | ~4.9GB | 8GB | Good | New default. Excellent instruction-following. Fits on Machine A. |
| `gemma4:31b` | 31B | ~16–20GB | 24GB+ | Best | Highest quality. Use `--review-model-preset high-quality`. |
| `gemma4:e4b` | ~9B | 9.6GB | 16GB+ | Very Good | You have this installed. Still too big for 8GB. |
| `qwen2.5:7b` | 7B | ~4–5GB | 8GB | Good | Previously the 8GB-safe preset. Now superseded by `llama3.1:8b`. |
| `qwen2.5:3b` | 3B | 1.9GB | 4GB | Okay | You have this installed. Fits easily on Machine A. More false positives. |

> **Rule of thumb:** A quantized model needs roughly 0.5–0.7GB RAM per billion parameters. Your 8GB Mac needs ~2–3GB just for macOS, leaving ~5GB for the model. That caps you at roughly 7B parameters *if you quit every other app*.

#### What Each Phase Actually Needs

| Phase | CPU | RAM | GPU | Network | Where it runs |
|-------|-----|-----|-----|---------|---------------|
| 1 — Scan | Low | ~500MB | No | No | Anywhere |
| 1 — Convert 341 PDFs | **High** (hours) | ~1GB | No | No | Anywhere |
| 1 — Refine | Medium | ~500MB | No | No | Anywhere |
| 2 — Canonicalize | Low | ~500MB | No | No | Anywhere |
| 3 — Extract | Low | ~500MB | No | No | Anywhere |
| 3 — **LLM Review** | Medium | **4–20GB** | Optional (Ollama) | No | **This is the constraint** |
| 4 — Build snapshot | Low | ~1GB | No | No | Anywhere |

#### Time Estimates (Full Corpus: 341 PDFs, ~5.8GB)

| Config | Phase 1 (Convert) | Phase 3 Review | Total | Machine |
|--------|-------------------|----------------|-------|---------|
| `--skip-review` (no AI) | 8–12 hrs | 0 | **8–12 hrs** | Either |
| `--tier lightweight` (qwen2.5:3b, parallelism=1) | 8–12 hrs | 3–6 hrs | **11–18 hrs** | Machine A (8GB) |
| `--tier heavy` (llama3.1:8b, parallelism=1) | 8–12 hrs | 4–8 hrs | **12–20 hrs** | Machine A (8GB) |
| `--review-model-preset high-quality` (gemma4:31b, parallelism=4) | 8–12 hrs | 2–4 hrs | **10–16 hrs** | **Machine B (64GB)** |

> These are wall-clock estimates with the machine dedicated to the task. The 7B/3B models on Machine A run at parallelism=1 because 8GB cannot hold multiple model instances. Machine B can run parallelism=4 with the 31B model because 64GB has headroom.

#### Machine A — MacBook Pro M2, 8GB

**What it can do:**
- ✅ Run the full mechanical pipeline (`--skip-review`)
- ✅ Run review with `llama3.1:8b` (4.9GB, already installed) — the new default
- ✅ Run review with `qwen2.5:3b` (1.9GB, already installed) — use `--review-model-preset ultra-light`
- ⚠️ Run review with `gemma4:e4b` (9.6GB) — too big, will swap to death
- ❌ Run review with `gemma4:31b` (~16-20GB) — will not load

**Recommended commands:**

```bash
# Test the pipeline mechanics on a small subject (no AI, ~3-4 hours)
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --skip-review

# Test review with the lightweight tier (qwen2.5:3b, ~3-5 hours for laws)
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --tier lightweight

# Test review with the heavy tier (llama3.1:8b, ~4-6 hours for laws)
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws --tier heavy
```

**⚠️ Important for Machine A:**
- Close **all** other apps before running review. Even Safari with a few tabs can push you into swap.
- The machine will thermal-throttle during long conversion runs. Expect it to get hot and slow down after the first hour.
- Do **not** run `--all` with review on this machine. It is a 20+ hour continuous load that will leave the machine barely usable and risk thermal issues.

#### Machine B — i9, 64GB RAM, RTX 4070 12GB

**What it can do:**
- ✅ Everything Machine A can do, faster
- ✅ Run review with `llama3.1:8b` (the default) at higher parallelism
- ✅ Run review with `gemma4:31b` via `--review-model-preset high-quality` (best quality)
- ✅ Run review with parallelism=4 (64GB has room for multiple model instances)
- ✅ GPU-accelerated Ollama inference (RTX 4070 will significantly speed up larger models vs CPU-only)

**Recommended commands:**

```bash
# Full rebuild with the default model (llama3.1:8b)
python scripts/pipeline_cli.py run-kg-pipeline --all

# Or with the high-quality preset for best results
python scripts/pipeline_cli.py run-kg-pipeline --all \
  --review-model-preset high-quality \
  --review-parallel 4

# If you want to test a subject first
python scripts/pipeline_cli.py run-kg-pipeline --subject 001-Laws
```

**Why this machine is better for review:**
- 64GB RAM means any model loads comfortably. `llama3.1:8b` (~4.9GB) is trivial. `gemma4:31b` (~16-20GB) also fits with headroom.
- RTX 4070 12GB VRAM means Ollama can offload layers to the GPU. `llama3.1:8b` fits entirely in VRAM. The 31B model won't fit entirely, but even partial GPU offload makes inference 3–5× faster than CPU-only on the M2.
- Parallelism=4 is realistic because 64GB can hold multiple model contexts simultaneously.

#### Two-Machine Workflow (Recommended)

Use both machines strategically:

1. **Machine A (M2 8GB)** — Development & iteration
   - Iterate on extraction regexes, test canonicalization, validate snapshot structure
   - Use `--skip-review` to get fast feedback loops
   - Use `--subject` to test on small slices
   - Use `--tier lightweight` for fast, RAM-safe review with `qwen2.5:3b`

2. **Machine B (i9 + RTX 4070)** — Production runs
   - Run `--all --tier heavy` for good-quality output fast
   - Run `--all --tier heavy --review-model-preset high-quality` for the absolute best quality
   - Let it run overnight — 10–16 hours for the full corpus
   - Copy the resulting `003/` and `005/` back to Machine A for analysis

#### Model Quality: What You Sacrifice at Each Tier

| Model | Relationship Accuracy | False Positive Rate | Best For |
|-------|----------------------|---------------------|----------|
| `gemma4:31b` (high-quality preset) | Highest | Lowest | Production truth on Machine B — best reasoning quality |
| `llama3.1:8b` (default) | Very Good | Low | Great balance of quality and accessibility. Runs on both machines. |
| `qwen2.5:3b` (ultra-light preset) | Okay | Higher | Quick testing on Machine A — expect to manually triage more |
| `--skip-review` | N/A (all extracted) | Highest | Pipeline testing only — never use for production truth |

> **Bottom line:** The new default is `llama3.1:8b` — it runs well on both machines and delivers very good quality. If you need the absolute best reasoning, use `--review-model-preset high-quality` (gemma4:31b) on Machine B. Use `--skip-review` or `--review-model-preset ultra-light` on Machine A for fast iteration.

---

### Workflow F: "I want to run dataset automation (laws wave)"

**Goal:** Process a bounded tranche of laws through the full pipeline with manifest-backed guardrails.

**Step 1 — Dry-run the full corpus**

```bash
python scripts/pipeline_cli.py run-laws-all-dry-run
```

What happens:
- Scans all raw folders without executing
- Reports readiness status for each family
- Identifies blocked families (missing OCR, missing concepts, etc.)

**Step 2 — Check for duplicates before widening**

```bash
python scripts/pipeline_cli.py run-laws-duplicate-dry-run
```

What happens:
- Hashes every raw PDF
- Surfaces exact-duplicate clusters
- Prevents wasted work on identical files

**Step 3 — Select a tranche and dry-run**

```bash
python scripts/pipeline_cli.py run-laws-tranche-dry-run --manifest config/datasets/my-tranche.yaml
```

What happens:
- Reads the tranche manifest (a bounded list of source families)
- Reports what would be processed, what is blocked, and why
- Validates that every family in the manifest exists in the raw layer

**Step 4 — Prepare sources (conversion + refinement)**

```bash
python scripts/pipeline_cli.py run-laws-tranche-source-prep \
  --manifest config/datasets/my-tranche.yaml
```

What happens:
- Converts every source in the tranche
- Runs OCR on scan-like documents
- Refines all conversion outputs
- Writes intermediate files to `002_Raw-Conversion-Layer/`

**Step 5 — Admit sources into canonical layer**

```bash
python scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run \
  --manifest config/datasets/my-tranche.yaml
python scripts/pipeline_cli.py run-laws-tranche-source-admission \
  --manifest config/datasets/my-tranche.yaml
```

What happens:
- Dry-run classifies every refined file as `ready` or `blocked`
- Blocked reasons: shallow representation, missing frontmatter, OCR quality too low
- The execute version copies `ready` files into `003_Canonical-Knowledge-Layer/`

**Step 6 — Build the tranche graph**

```bash
python scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run \
  --manifest config/datasets/my-tranche.yaml
python scripts/pipeline_cli.py run-laws-tranche-source-to-graph \
  --manifest config/datasets/my-tranche.yaml
```

What happens:
- Extracts relationships from all admitted canonical files
- Runs pre-review filter and Tier-1 Ollama review
- Promotes approved relationships
- Builds the graph snapshot and HTML visualization

**Step 7 — Aggregate all completed lanes**

```bash
python scripts/pipeline_cli.py run-laws-completed-aggregate
```

What happens:
- Reads `config/datasets/laws-completed-lanes.yaml`
- Builds a combined graph from all completed tranches
- Writes aggregate snapshot and visualization
- Reports residual families that still need work

---

## CLI Reference

All commands are exposed through a single entrypoint:

```bash
python scripts/pipeline_cli.py <command> [options]
```

Use `--output-mode operator` for human-friendly framing around command output. This mode explains what the command is about to do, shows progress, and summarizes results in plain English.

### Core Pipeline

| Command | Description |
|---|---|
| `run` | Baseline pipeline: scan → status → lint |
| `scan` | Inventory raw sources into registries and tree snapshots |
| `status` | Compare registries and report new/changed/missing files |
| `lint` | Hygiene check: non-PDF files, duplicate-like filenames |
| `convert` | Batch convert new/changed PDFs/Office/Spreadsheets |
| `convert-one <path>` | Convert a single source through the legacy path |
| `convert-parsers-one <path>` | Convert through the Phase 1B parser orchestrator |
| `convert-spreadsheet-one <path>` | Convert one spreadsheet to CSV/JSON |
| `detect-one <path>` | Classify a PDF as text-usable or scan-like |
| `ocr-queue` | Build the queue of files likely needing OCR |
| `ocr-execute` | Run OCR on queued files |
| `refine` | Batch-clean raw conversion markdown (Tier A/B normalization) |
| `refine-one <path>` | Refine a single markdown file |
| `canonicalize` | Batch-write refined sources into canonical pages |
| `canonicalize-one <path>` | Canonicalize a single refined markdown file |
| `canonicalize-plan-one <path>` | Preview canonicalization without writing |
| `canonicalize-concept-one <name>` | Create a canonical concept page scaffold |
| `reconcile` | Detect missing sources and stale derived outputs |
| `rotate-registries` | Prune old timestamped registry snapshots |
| `run-with-review` | Full pipeline: scan → convert → refine → LLM review |
| `run-kg-pipeline` | **Unified 4-phase orchestrator** (raw → canonical → extract → review → promote → KG v2 snapshot). Use `--tier lightweight` for qwen+nomic or `--tier heavy` for llama/gemma4. |

### Extraction & Review

| Command | Description |
|---|---|
| `extract-relationships-one <path>` | Regex-based relationship extraction from one file |
| `extract-relationships-sections-one <path>` | Section-aware extraction with `source_section_id` |
| `review-relationships-ollama` | Tier-1 local LLM review (`llama3.1:8b` default) |
| `review-relationships-ollama-second-pass` | Tier-2 adjudication on uncertain Tier-1 results |
| `promote` | Move approved reviews into canonical relationship records |
| `promote-generated-canonical-rules` | Promote LLM-generated rules into canonical rule records |
| `promote-scaffolded-concepts` | Promote scaffolded concept pages into canonical concepts |
| `promote-scaffolded-relationships` | Promote scaffolded relationships into canonical records |
| `enrich-concept-one <name>` | Enrich one concept with deterministic definition data |
| `enrich-concepts` | Batch-enrich concept pages |
| `suggest-concept-candidates-from-refined` | Suggest concept candidates from definition-style text in refined markdown |

### Graph & Query

| Command | Description |
|---|---|
| `build-graph` | Build the filesystem graph snapshot from canonical knowledge |
| `query-graph <from> <to>` | Return a path between two node IDs |
| `query "<question>"` | Natural-language query against the latest graph snapshot |
| `query-structured <function>` | Structured query function against the latest graph snapshot |
| `export-graph-snapshot` | Print the latest snapshot in a structured export format |
| `export-graph-owl` | Export the latest snapshot as RDF Turtle |
| `visualize-graph` | Render a browser-friendly HTML visualization |

### Knowledge Graph v2 (gated by `kg_transition.enabled`)

| Command | Description |
|---|---|
| `kg-ingest-evidence <source_path>` | Ingest document → version → section → chunk → evidence span |
| `kg-extract-candidates` | Structured LLM extraction with validator gating |
| `kg-canonicalize-candidates` | Deduplicate, normalize, place into taxonomy |
| `kg-materialize-canonical` | Validate assertions and materialize fast edges |
| `kg-build-unified` | Build unified v2 snapshot from canonical content |
| `kg-validate-assertions` | Run `AssertionValidator` (R1–R15) on a snapshot |
| `kg-detect-contradictions` | Run `ContradictionDetector` on relationship assertions |
| `kg-query-nodes <query>` | Case-insensitive label search over canonical nodes |
| `kg-query-neighborhood <node_id>` | Explore related nodes with assertion detail |
| `kg-inspect-node <node_id>` | Inspect a canonical node and its evidence |
| `kg-inspect-assertion <assertion_id>` | Inspect an assertion and its provenance |
| `kg-review-queue` | List assertions pending review |
| `kg-review-action <id> --action {approve,reject,escalate}` | Mutate assertion state |
| `kg-seed-taxonomy` | Seed taxonomy roots into the canonical layer |
| `kg-backfill-evidence` | Backfill evidence for existing canonical sources |

### Dataset Automation (Laws Wave)

| Command | Description |
|---|---|
| `run-laws-pilot` | One-command bounded 4-law pilot → graph + visualization |
| `run-laws-all-dry-run` | Inspect all-laws readiness without execution |
| `run-laws-tranche-dry-run` | Inspect a bounded tranche manifest with guardrails |
| `run-laws-duplicate-dry-run` | Report exact duplicate raw PDFs before widening |
| `run-laws-tranche-source-prep-dry-run` | Inventory tranche inputs before conversion |
| `run-laws-tranche-source-prep` | Run tranche conversion/refinement |
| `run-laws-tranche-source-admission-dry-run` | Classify tranche outputs into ready-vs-blocked |
| `run-laws-tranche-source-admission` | Admit selected tranche outputs into canonical pages |
| `run-laws-tranche-source-to-graph-dry-run` | Stage admitted tranche members in dry-run mode |
| `run-laws-tranche-source-to-graph` | Execute tranche source-to-graph wrapper |
| `run-laws-completed-aggregate` | One-command aggregate graph for all completed lanes |
| `build-laws-completed-aggregate-manifest` | Generate aggregate manifest from completed lanes |
| `run-dataset-graph` | Run manifest-defined dataset graph pipeline |
| `run-dataset-source-to-graph` | Bounded dataset pipeline through graph creation |
| `summarize-dataset-build-report` | Summarize the latest dataset build report |

### Completed Aggregate Automation (Advanced)

These commands manage the **completed-aggregate** workflow: a batched pipeline for families of sources that have already been converted, refined, and reviewed. Used when processing large corpora in lanes that complete at different times and need to be aggregated into unified datasets.

| Command | Description |
|---|---|
| `run-completed-aggregate` | Run the full aggregate pipeline for a completed ledger |
| `run-completed-aggregate-family` | Run aggregate pipeline for a single family within a ledger |
| `run-completed-aggregate-from-catalog` | Run aggregate from a catalog profile |
| `run-completed-aggregate-from-profile` | Run aggregate from an explicit YAML profile |
| `build-completed-aggregate-manifest` | Generate an aggregate manifest from a completed ledger |
| `build-completed-aggregate-from-catalog` | Build aggregate from a catalog definition |
| `build-completed-aggregate-from-profile` | Build aggregate from a profile YAML |
| `admit-completed-aggregate-manifest` | Admit an aggregate manifest into the canonical layer |
| `admit-concepts-to-manifest` | Admit scaffolded concepts into an aggregate manifest |
| `bootstrap-completed-aggregate-family-lane` | Bootstrap a new family lane (directories + manifest scaffold) |
| `check-completed-aggregate-family` | Validate a family lane for readiness |
| `inspect-completed-aggregate-lane-sources` | Inspect which sources are in a lane and their status |
| `prepare-completed-aggregate-lane-sources` | Prepare (convert + refine) all sources in a lane |
| `register-completed-aggregate-family` | Register a family as ready in the completed ledger |
| `scaffold-completed-aggregate-family` | Scaffold canonical artifacts for a family from templates |
| `scaffold-completed-aggregate-lane-manifest` | Scaffold a lane manifest for a family |
| `scaffold-completed-aggregate-lane-concepts` | Scaffold concept pages for a lane |
| `scaffold-completed-aggregate-lane-relationships` | Scaffold relationship records for a lane |
| `scaffold-completed-aggregate-lane-canonical-rules` | Scaffold canonical rule pages for a lane |
| `promote-completed-aggregate-lane-relationships` | Promote reviewed relationships for a lane into canonical records |
| `source-admit-completed-aggregate-lane` | Admit prepared lane sources into canonical pages |
| `source-admit-completed-aggregate-lane-dry-run` | Dry-run source admission for a lane |
| `suggest-completed-aggregate-family-candidates` | Suggest candidate sources for a family lane |

### Maintenance & Utilities

| Command | Description |
|---|---|
| `migrate-ids-plan` | Plan a canonical ID migration without applying |
| `migrate-ids-apply` | Apply a previously planned ID migration |
| `ple-kv-migrate` | Migrate SQLite ↔ RocksDB event/registry stores |
| `ple-registry-purge` | Purge old rows from the stateful review registry |
| `ple-cotrace-dump` | Summarize Chain-of-Thought audit directory |
| `ple-vision-probe` | Check RAM headroom and Ollama model availability |
| `ingest-spatial` | Ingest spatial artifacts into the spatial subsystem |
| `evaluate-spatial` | Evaluate spatial rules against supplied observations |

---

## Knowledge Graph v2

Vitruvius ships a **taxonomy-centered canonical knowledge graph** that separates evidence from canonical truth, and assertions from fast edges. Gated by `kg_transition.enabled`.

**Architecture:**
- **Evidence layer** — `DocumentVersion → Section → Chunk → EvidenceSpan` with resolvable selectors (`PdfBboxSelector`, `MarkdownRangeSelector`, `TextRangeSelector`)
- **Canonical layer** — `Taxonomy → Topic → Subtopic → Concept / Rule / Definition / Procedure / Exception`
- **Assertion layer** — Reified `RelationshipAssertion`, `PlacementAssertion`, `MergeAssertion`
- **Safety gates** — `ExtractionValidator` (E1–E10), `AssertionValidator` (R1–R15), `ContradictionDetector` (4 patterns)
  - E10: Evidence span existence validation (prevents phantom citations)
  - R14/R15: Review-state and self-referential guards (prevents circular placements)
- **Persistence** — File-native JSONL sidecars by default; optional Neo4j/PostgreSQL as Layer 5 indexes (AD-043)
- **Visualization** — Dual-mode HTML viewer (v1/v2 auto-detect) with interactive evidence panels, inference-type badges, and confidence-proportional sizing

**Status:** Implementation complete (2026-04-19). 281+ KG-specific tests passing. Snapshot integrity validated (0 orphaned edges, 0 dangling placements, 0 missing source nodes).

**Current snapshot:** `005_Operational-Intelligence-Layer/graph/kg-v2/snapshot_repaired.json` (178 canonical nodes, all references validated).

**Authoritative artifacts:**
- Post-implementation audit: `.ai/02_audits/2026-04-19_knowledge_graph_transition_post_implementation_audit.md`
- Rectification plan: `.ai/03_plans/2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan.md`

### Activating KG v2

1. Edit `config/vitruvius.yaml`
2. Set `kg_transition.enabled: true`
3. Run `python scripts/pipeline_cli.py kg-seed-taxonomy`
4. Ingest your first source: `python scripts/pipeline_cli.py kg-ingest-evidence <path>`
5. Build the unified snapshot: `python scripts/pipeline_cli.py kg-build-unified`

See [Workflow D](#workflow-d-i-want-to-activate-and-use-kg-v2) for the full step-by-step path.

---

## Dataset Automation (Laws Wave)

Vitruvius has a **bounded, manifest-backed dataset automation system** proven on Philippine building laws. It operates tranche-by-tranche with explicit guardrails:

- **Duplicate detection** — Exact-duplicate raw PDF clusters surfaced before widening
- **OCR-first preparation** — Scanned documents prepared before admission
- **Source admission** — Conservative ready-vs-blocked classification
- **Concept-fit admission** — Minimal concept slices to clear shallow-representation guardrails
- **Aggregate hardening** — Combined graph of all completed lanes with residual tracking

**Current state:** 25 completed lanes, 41/47 raw folders covered, `saturated_truth_complete` status.

**Artifact stack:**
- `config/datasets/laws-completed-lanes.yaml`
- `config/datasets/laws-remaining-dispositions.yaml`
- `config/datasets/laws-source-provenance.yaml`
- `config/datasets/laws-manifest-index.yaml`
- `docs/LAWS_WAVE_ARTIFACT_INDEX.md`

### Running a tranche

1. Create a tranche manifest YAML listing the families to process
2. Dry-run: `python scripts/pipeline_cli.py run-laws-tranche-dry-run --manifest <path>`
3. Prep sources: `python scripts/pipeline_cli.py run-laws-tranche-source-prep --manifest <path>`
4. Admit: `python scripts/pipeline_cli.py run-laws-tranche-source-admission --manifest <path>`
5. Build graph: `python scripts/pipeline_cli.py run-laws-tranche-source-to-graph --manifest <path>`

See [Workflow E](#workflow-e-i-want-to-run-dataset-automation-laws-wave) for the full step-by-step path.

---

## Testing

```bash
# Full test suite
python -m pytest scripts/tests/

# KG-specific tests only
python -m pytest scripts/tests/test_kg_*.py

# Skip known pre-existing failures
python -m pytest scripts/tests/ \
  --ignore=scripts/tests/test_3d_upgrade_backcompat.py \
  --ignore=scripts/tests/test_concept_stringency_migration.py \
  --ignore=scripts/tests/test_wiring_backcompat.py \
  --ignore=scripts/tests/test_wiring_e2e.py
```

**Current baseline:** 2048+ passed, 17 skipped, 7 pre-existing unrelated failures. (KG v2 adds 281+ dedicated tests.)

---

## Current Status

| System | Status |
|---|---|
| Core pipeline (scan → convert → refine → canonicalize → extract → review → promote → graph) | ✅ Operational |
| Multi-parser integration (Phase 1B) | ✅ Complete (Docling, LibreOffice, OCR, Rust PDF parser) |
| Normalization (Tier A/B) | ✅ Complete |
| Concept layer (20 PD 1096 concepts) | ✅ 16/20 enriched, deterministic |
| Relationship extraction | ✅ Regex-based, section-aware, 78% LLM savings via pre-review filter |
| LLM review (Tier 1/2) | ✅ Complete with resume, retry, parallelization |
| Promotion governance | ✅ Complete with audit log, rollback, dry-run |
| Graph building (v1) | ✅ Complete |
| Knowledge Graph v2 | ✅ Complete (2026-04-19) |
| Dataset automation (laws wave) | ✅ 25 lanes complete, aggregate hardening active |
| Spatial intelligence | ✅ Complete (TypeScript daemon, Z3 solver, IFC/OWL) |
| Compound AI | ✅ Complete (adversarial swarm, Datalog bridge, DSPy compiler) |
| High-performance backends | ✅ RocksDB (default), GraphSAGE PQ, MinHash LSH |

**Active bounded lane:** `ready-family-aggregate` residual hardening (`143 nodes / 266 edges / 1 warning`).

---

## Documentation

| Path | Purpose |
|---|---|
| `AGENTS.md` | Root operating contract for all AI agents |
| `.ai/01_roadmap/master-roadmap.md` | Strategic roadmap, phase contracts, sprint ledger |
| `.ai/01_roadmap/current-phase.md` | Live execution state and next valid gates |
| `.ai/01_roadmap/milestone-tracker.md` | Completion truth for every phase |
| `.ai/00_system/architecture.md` | Subsystem breakdown and runtime entry points |
| `.ai/00_system/pipeline-overview.md` | Stage-by-stage execution flow |
| `.ai/00_system/principles.md` | Non-negotiable architectural principles |
| `.ai/02_audits/` | Independent verification audits |
| `.ai/03_plans/` | Active implementation plans |
| `.ai/05_logs/` | Validation and execution logs |
| `.ai/10_state/decisions.md` | Architecture decision log (AD-001+) |

---

## License & Attribution

Vitruvius is a **headless, mathematically rigorous AEC physics and compliance engine**. Public-domain Philippine law (PD 1096, etc.) serves as the reference development corpus. Vertical specialization into AEC is deliberate: it lets every line of optimization work target spatial geometry, clash detection, and building code compliance.
