<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# vitruvius

## Purpose
Core Python package containing all pipeline logic for document processing, conversion, and knowledge extraction.

## Key Files
| File | Description |
|------|-------------|
| `__init__.py` | Package initialization and CLI setup |
| `constants.py` | Layer and folder name constants |
| `models.py` | Data models (FileEntry dataclass) |
| `paths.py` | Path resolution and directory helpers |
| `utils.py` | Timestamp, normalization, naming utilities |
| `reports.py` | JSON/CSV/TXT report writing |
| `scanner.py` | Raw layer scanning and tree snapshots |
| `status.py` | Registry diff and change detection |
| `linting.py` | Raw layer hygiene checks |
| `detection.py` | PDF text vs scanned detection |
| `conversion.py` | PDF-to-Markdown conversion |
| `reconcile.py` | Missing source and stale output detection |
| `ocr.py` | OCR queue and OCRmyPDF execution |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `rules/` | Canonicalization rules (see `rules/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Each module is self-contained with single responsibility
- CLI handlers are named `run_<command>()` 
- Use paths.py functions for all path resolution
- Always write reports to 006_System-Manifests/runs/

### Testing Requirements
- Test individual modules before committing
- Verify reports generate correctly
- Check CSV registry append works

### Common Patterns
- Dataclass models in models.py
- Path helpers in paths.py
- Report writers in reports.py
- CLI entrypoints in pipeline_cli.py delegate to run_*() functions

## Dependencies

### External
- `pypdf` - PDF page reading
- `opendataloader-pdf` - PDF conversion
- `ocrmypdf` - OCR processing

### Internal
- All modules are internal to this package

<!-- MANUAL: -->