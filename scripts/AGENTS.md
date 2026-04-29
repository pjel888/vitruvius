<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# scripts

## Purpose
Python CLI and core Vitruvius package for source custody, extraction staging, evidence preparation, compatibility pipelines, and KG-first support tooling.

## Key Files
| File | Description |
|------|-------------|
| `pipeline_cli.py` | Main CLI entrypoint for source custody/evidence-prep, compatibility pipeline, and KG support commands |
| `Word-PPT-To-PDF.py` | Office-to-PDF batch converter |
| `test_odl_one.py` | Standalone OpenDataLoader test |
| `test_pdf_text_detection.py` | Standalone PDF text detection test |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `vitruvius/` | Core pipeline package (see `vitruvius/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Source custody, extraction staging, evidence preparation, and KG support logic lives in the `vitruvius/` subpackage
- Use `python scripts/pipeline_cli.py <command>` to run source/evidence compatibility commands
- Preserve old commands and output paths unless a tests-first cleanup packet explicitly changes them
- Test modifications with targeted tests before refactors

### Testing Requirements
- Run `test_odl_one.py` to verify PDF conversion works
- Run `test_pdf_text_detection.py` to verify PDF detection works
- Check `006_System-Manifests/runs/` for report outputs

### Common Patterns
- Each module in vitruvius/ handles one custody, staging, evidence, graph, or compatibility responsibility
- Reports are written to 006_System-Manifests/runs/
- CSV registries track source/file state across runs
- Legacy raw/conversion/canonical modules are compatibility infrastructure unless exact impact and tests prove otherwise

## Dependencies

### Internal
- `vitruvius/` package - all pipeline modules

### External
- `pypdf` - PDF text extraction
- `opendataloader-pdf` - PDF conversion
- `ocrmypdf` - OCR processing
- `PyYAML` - config parsing

<!-- MANUAL: -->