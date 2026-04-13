<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# Vitruvius Root

## Purpose
Local-first knowledge pipeline for architectural board exam preparation. Processes raw documents through scanning, conversion, canonicalization, and derivation layers to produce machine-readable knowledge for AI-assisted study.

## Key Files
| File | Description |
|------|-------------|
| `README.md` | Full project documentation |
| `AGENTS.md` | This file - AI agent guidance |
| `CLAUDE.md` | Claude Code-specific instructions |
| `GEMINI.md` | Gemini CLI instructions |
| `config/vitruvius.yaml` | Project configuration |
| `init_vitruvius_structure.sh` | Directory structure initialization script |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `scripts/` | Python pipeline CLI and core package (see `scripts/AGENTS.md`) |
| `config/` | Configuration files (see `config/AGENTS.md`) |
| `docs/` | Documentation files (see `docs/AGENTS.md`) |
| `001_Raw-Source-Layer/` | Original source documents (PDFs, scans) |
| `002_Raw-Conversion-Layer/` | Machine-extracted text outputs |
| `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge pages |
| `004_Derived-Content-Layer/` | Generated learning content |
| `005_Operational-Intelligence-Layer/` | Machine infrastructure (chunks, embeddings, graphs) |
| `006_System-Manifests/` | Pipeline control, audit logs, registries |

## For AI Agents

### Working In This Directory
- **ALWAYS use code-review-graph MCP tools** before using Grep/Glob/Read to explore the codebase
- **ALWAYS use gitnexus tools** for impact analysis before editing any symbol
- Run `npx gitnexus analyze` if the index becomes stale
- Follow the Content Trust Order: Canonical > Raw Conversion > Raw Source

### Pipeline Commands
```bash
# Full pipeline
python scripts/pipeline_cli.py run

# Convert PDFs
python scripts/pipeline_cli.py convert

# Detect PDF type
python scripts/pipeline_cli.py detect-one "path/to/file.pdf"

# Run OCR
python scripts/pipeline_cli.py ocr-execute
```

### Testing Requirements
- Test any pipeline modification with `test_pdf_text_detection.py` and `test_odl_one.py`
- Verify reports are written correctly to `006_System-Manifests/runs/`

### Common Patterns
- All pipeline modules are in `scripts/vitruvius/`
- Use the six-layer architecture consistently
- All outputs go to layer 6 for auditability

## Dependencies

### External
- `pypdf` - PDF text extraction for detection
- `opendataloader-pdf` - PDF-to-Markdown conversion
- `ocrmypdf` - OCR processing for scanned PDFs
- `PyYAML` - Configuration file parsing

### Internal
- `scripts/vitruvius/` - Core pipeline modules
- Six data layers for knowledge lifecycle

## Data Layers Overview

| Layer | Folder | Purpose |
|-------|--------|---------|
| 1 | `001_Raw-Source-Layer/` | Original source documents (git-ignored) |
| 2 | `002_Raw-Conversion-Layer/` | Machine-extracted text (Markdown, JSON, OCR PDFs) |
| 3 | `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge |
| 4 | `004_Derived-Content-Layer/` | Generated learning content |
| 5 | `005_Operational-Intelligence-Layer/` | Chunks, embeddings, graphs |
| 6 | `006_System-Manifests/` | Pipeline control and audit |

<!-- MANUAL: MCP tool configuration and GitNexus instructions are in the header above this file -->
