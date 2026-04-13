<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# scripts

## Purpose
Python pipeline CLI and core Vitruvius package for document processing and knowledge extraction.

## Key Files
| File | Description |
|------|-------------|
| `pipeline_cli.py` | Main CLI entrypoint for all pipeline commands |
| `Word-PPT-To-PDF.py` | Office-to-PDF batch converter |
| `test_odl_one.py` | Standalone OpenDataLoader test |
| `test_pdf_text_detection.py` | Standalone PDF text detection test |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `vitruvius/` | Core pipeline package (see `vitruvius/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- All pipeline logic is in the `vitruvius/` subpackage
- Use `python scripts/pipeline_cli.py <command>` to run pipeline
- Test modifications with standalone test scripts

### Testing Requirements
- Run `test_odl_one.py` to verify PDF conversion works
- Run `test_pdf_text_detection.py` to verify PDF detection works
- Check `006_System-Manifests/runs/` for report outputs

### Common Patterns
- Each module in vitruvius/ handles one pipeline responsibility
- Reports are written to 006_System-Manifests/runs/
- CSV registries track file state across runs

## Dependencies

### Internal
- `vitruvius/` package - all pipeline modules

### External
- `pypdf` - PDF text extraction
- `opendataloader-pdf` - PDF conversion
- `ocrmypdf` - OCR processing
- `PyYAML` - config parsing

<!-- MANUAL: -->