# PD-1216 single-law OCR path inspection

## Scope
Task 1: inspect the exact existing OCR execution path for the single scanned law `PD-1216` and report leader-safe command(s).

## Fresh evidence
- `python3 scripts/pipeline_cli.py detect-one '001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'`
  - `RESULT: LIKELY_SCANNED_PDF`
  - `RECOMMENDED ROUTE: OCR_FIRST_THEN_OPENDATALOADER`
  - sampled pages 1-5 all returned `0 extracted characters`
- `python3 scripts/pipeline_cli.py convert-one '001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'`
  - hard-stops before conversion with `This file should go through OCR first, then OpenDataLoader.`
- Current tranche state already marks the law blocked pending OCR:
  - `config/datasets/laws-tranche-1.yaml`
  - `006_System-Manifests/runs/datasets/laws-tranche-1/20260417T051022Z/laws_tranche_source_admission_report.json`
- No PD-1216 OCR/conversion outputs currently exist under:
  - `002_Raw-Conversion-Layer/001-Laws/ocr_pdf/PD-1216/`
  - `002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1216/`
  - `002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-1216/`

## Exact existing code path
1. Detection classifies the PDF as scanned in `scripts/vitruvius/detection.py`.
2. Batch conversion would place PD-1216 into `latest_ocr_needed_report.json` as `ocr_required` in `scripts/vitruvius/conversion.py`.
3. `scripts/vitruvius/ocr.py::run_ocr_queue()` reads `latest_ocr_needed_report.json` and writes `latest_ocr_queue_report.json`.
4. `scripts/vitruvius/ocr.py::run_ocr_execute()`:
   - builds OCR PDF path via `build_ocr_pdf_relative_path()`
   - runs `ocrmypdf.ocr(..., skip_text=True, progress_bar=False)`
   - immediately calls `convert_pdf_at_path(...)` on the OCR PDF with route `OCR_THEN_OPENDATALOADER`
   - writes:
     - `002_Raw-Conversion-Layer/001-Laws/ocr_pdf/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf`
     - `002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md`
     - `002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.json`
5. Refinement is a separate required step in `scripts/vitruvius/normalization/refine.py::run_refine_one()` to produce:
   - `002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md`

## Leader-safe commands

### Safe inspection commands
```bash
cd /Users/philiplewis/vitruvius
python3 scripts/pipeline_cli.py detect-one '001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'
python3 scripts/pipeline_cli.py convert-one '001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'
```

### Safest single-law execution command using existing internals
This avoids overwriting shared `latest_ocr_needed_report.json` / `latest_ocr_queue_report.json` while still following the exact existing OCR -> OpenDataLoader -> refine implementation path.

```bash
cd /Users/philiplewis/vitruvius
PYTHONPATH=scripts python3 - <<'PY'
import ocrmypdf
from vitruvius.paths import get_repo_root, build_ocr_pdf_relative_path
from vitruvius.conversion import convert_pdf_at_path
from vitruvius.normalization.refine import run_refine_one

rel_path = '001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'
raw_md_rel = '001-Laws/raw_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md'
repo = get_repo_root()
source_pdf = repo / '001_Raw-Source-Layer' / rel_path
ocr_rel = build_ocr_pdf_relative_path(rel_path)
ocr_abs = repo / '002_Raw-Conversion-Layer' / ocr_rel
ocr_abs.parent.mkdir(parents=True, exist_ok=True)
if ocr_abs.exists():
    ocr_abs.unlink()
ocrmypdf.ocr(
    str(source_pdf),
    str(ocr_abs),
    languages=['eng'],
    deskew=True,
    skip_text=True,
    progress_bar=False,
)
convert_pdf_at_path(
    ocr_abs,
    rel_path,
    run_command='ocr-execute',
    detected_pdf_type='OCR_OUTPUT_PDF',
    processing_route='OCR_THEN_OPENDATALOADER',
    output_ocr_pdf_relative_path=f'002_Raw-Conversion-Layer/{ocr_rel.as_posix()}',
)
raise SystemExit(run_refine_one(relative_markdown_path=raw_md_rel))
PY
```

## Notes
- There is no existing first-class `ocr-one` CLI; the stock CLI path is queue-oriented and keyed off `latest_ocr_needed_report.json`.
- Because `run_ocr_execute()` does **not** refine outputs, a follow-up `refine-one` step is mandatory before PD-1216 can be reconsidered for tranche source admission.
