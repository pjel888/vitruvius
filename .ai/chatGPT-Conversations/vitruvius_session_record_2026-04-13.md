# Vitruvius Session Record

Date: 2026-04-13

## Note

This is a reconstructed markdown record of the work completed in this session so far.

It is not a verbatim full transcript of every message, but it captures the key decisions, problems, fixes, commands, and implementation milestones in the order they happened.

---

## 1. Project Direction

The session focused on building the local ingestion and conversion backbone for **Vitruvius**, the AI-side knowledge system that will be built alongside Slatecamp.

Core objective:
- convert local source files into AI-usable artifacts
- preserve a clean layered pipeline
- support both text PDFs and scanned PDFs
- prepare for RAG, wiki generation, and future graph-based knowledge tooling

---

## 2. Pipeline Direction Agreed

A 3-line pipeline was established:

### 1st line: Raw source dataset
`001_Raw-Source-Layer`

This is the source of truth.
It contains the original files and folder hierarchy.

### 2nd line: Raw conversion layer
`002_Raw-Conversion-Layer`

This contains derivative artifacts such as:
- OCR PDFs
- raw markdown
- sidecar JSON

### 3rd line: structured AI-ready layer
A later layer intended for metadata enrichment, chunking, AI persistence, and downstream RAG or wiki use.

---

## 3. Repository and Folder Structure

The Vitruvius repo was initialized and folder structure was created.

A recurring design principle was enforced:
- raw source remains untouched
- derived outputs must be separated
- manifests and registries must track system state

---

## 4. Initial Manifest and Snapshot Tooling

A first CLI and manifest workflow was created to support:

- raw source scan
- tree snapshots
- file registries
- status comparison between scans
- linting of dataset structure

Commands used during the build:

```bash
python scripts/pipeline_cli.py scan
python scripts/pipeline_cli.py status
python scripts/pipeline_cli.py lint
python scripts/pipeline_cli.py run
```

Observed outputs during a clean state included:
- 424 files found
- 0 new
- 0 changed
- 0 missing
- 424 unchanged

---

## 5. Problems Encountered Early

Several implementation issues were encountered and fixed:

### Shell script issue
An initialization shell script had a malformed line and failed during folder creation.

### Python syntax issue
A `return` statement ended up outside a function in the earlier pipeline script and caused:

```text
SyntaxError: 'return' outside function
```

That required replacing the full file with a corrected version.

### Naming issue
The file name `001_vitruvius.py` was considered too vague and was renamed to a more descriptive CLI entrypoint pattern:
`pipeline_cli.py`

---

## 6. Java and OpenDataLoader PDF Setup

The pipeline was wired to use **OpenDataLoader PDF** for PDF-to-Markdown and PDF-to-JSON extraction.

### Problem encountered
An old Java 8 runtime was being picked up instead of a newer JDK, which caused incompatibility with OpenDataLoader.

### Root cause
Git Bash and integrated terminals were resolving Java 8 from:

```text
C:\Program Files (x86)\Java\jre1.8.0_481\bin
```

### Resolution
A newer Adoptium JDK was installed and eventually confirmed working.

Final confirmed JDK path:

```text
C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot
```

Confirmed Java output:

```text
openjdk version "25.0.2"
```

---

## 7. Integrated Terminal Environment Issue

A major side issue occurred where Java worked in standalone Git Bash but not inside the integrated Antigravity terminal.

Resolution path included:
- correcting environment propagation
- using shell profile setup
- updating `.bashrc` / `.bash_profile`
- verifying `JAVA_HOME`
- verifying `which java`
- confirming the correct JDK path was being used in the integrated environment

Eventually both environments were made consistent.

---

## 8. First OpenDataLoader PDF Proof of Concept

A single-file test was run against:

```text
001-Laws/PD-1096/PD 1096 - National Building Code.pdf
```

OpenDataLoader successfully created:
- Markdown
- JSON

This proved:
- Java setup was correct
- OpenDataLoader was callable
- Vitruvius could generate usable derivative outputs from a text PDF

---

## 9. PDF Text Detection Step

A detector was then added to distinguish between:
- text PDFs
- likely scanned PDFs

Test command used:

```bash
python scripts/test_pdf_text_detection.py "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

Observed result:

```text
RESULT: TEXT_PDF
Route: OpenDataLoader directly.
```

This became a key rule in the pipeline:

- text PDF -> OpenDataLoader directly
- scan PDF -> OCR first, then OpenDataLoader

---

## 10. `detect-one` Command Added to the Real CLI

Detection logic was folded into the main CLI.

Command added:

```bash
python scripts/pipeline_cli.py detect-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

Confirmed output:
- `TEXT_PDF`
- `OPENDATALOADER_DIRECT`

This also wrote detection reports into the manifests runs folder.

---

## 11. `convert-one` Command Added

A real one-file conversion command was implemented.

Command:

```bash
python scripts/pipeline_cli.py convert-one "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"
```

This:
- detected the file first
- refused scanned files
- ran OpenDataLoader for text PDFs
- preserved subfolder path structure
- wrote output into:

```text
002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/...
002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-1096/...
```

This solved the future filename collision problem by preserving nested source structure.

---

## 12. Batch `convert` Command Added

Batch conversion was then added so the pipeline could:
- read `new_files` and `changed_files`
- detect each PDF
- convert text PDFs
- send scan-like files to OCR-needed reporting
- skip non-PDF files
- emit queue and batch reports

Normal workflow became:

```bash
python scripts/pipeline_cli.py run
python scripts/pipeline_cli.py convert
```

---

## 13. Reconcile Logic Added

A `reconcile` command was added to address source-of-truth drift.

Command:

```bash
python scripts/pipeline_cli.py reconcile
```

Purpose:
- inspect missing raw PDFs
- determine whether derived markdown/json outputs still exist
- report stale outputs without deleting anything

This established a proper source-of-truth rule:

- raw source layer is the authority
- conversion layer is derived
- reconcile is the safety check before any future prune logic

---

## 14. Test File Lifecycle Verified

A new PDF was added temporarily to test the conversion queue.
It was successfully detected and converted.

Then:
- the raw test PDF was deleted
- the generated markdown and JSON were also deleted

After running scan and reconcile again, system state returned cleanly to:
- 424 files
- 0 new
- 0 changed
- 0 missing

This confirmed the reconcile workflow was sound.

---

## 15. Modular Refactor Began

The project then moved away from a giant single `pipeline_cli.py`.

A package layout under `scripts/vitruvius/` was created.

Shared foundation files created:
- `__init__.py`
- `constants.py`
- `models.py`
- `utils.py`
- `paths.py`
- `reports.py`

Then real logic files were separated:
- `scanner.py`
- `status.py`
- `linting.py`
- `detection.py`
- `conversion.py`
- `reconcile.py`
- `ocr.py`

`pipeline_cli.py` was reduced into a thin command router.

This was a major architectural cleanup and positioned the repo for future OCR and registry work.

---

## 16. Refactor Problems Encountered

During modularization, several import issues occurred.

### Relative import issue
At one point the wrong file contents were pasted into `pipeline_cli.py`, causing:

```text
ImportError: attempted relative import with no known parent package
```

Cause:
- a package-internal module was accidentally placed into the top-level CLI file

Fix:
- restore `pipeline_cli.py` as a top-level absolute-import entrypoint

### Missing exported symbol confusion
Later, import errors appeared around:
- `run_convert`
- `run_reconcile`

These turned out to be:
- on-disk file mismatches
- cache issues
- and in one case function naming mismatch in the reconcile module

These were resolved by:
- verifying functions with `grep`
- removing `__pycache__`
- rechecking import targets
- aligning names with the expected CLI imports

---

## 17. OCR Queue Module Added

A first OCR module was added in report form.

Command:

```bash
python scripts/pipeline_cli.py ocr-queue
```

This did not perform OCR yet.
It simply:
- read the OCR-needed report
- prepared a queue of scan-only candidates
- wrote OCR queue reports

This was intentionally staged before real OCR execution.

---

## 18. Real OCR Executor Added

The next milestone was wiring real OCR execution with **OCRmyPDF**.

Confirmed installed version:

```text
17.4.1
```

The OCR execution path was designed as:

- raw source PDF stays in `001_Raw-Source-Layer`
- OCR searchable PDF is written into:
  `002_Raw-Conversion-Layer/<category>/ocr_pdf/...`
- OpenDataLoader is then run on the OCR PDF
- markdown and sidecar JSON are written into the existing conversion structure

Command added:

```bash
python scripts/pipeline_cli.py ocr-execute
```

The executor was tested successfully in the zero-item case and produced correct reports without crashing.

Observed clean output included:

```text
OCR execute complete.
Queue count: 0
OCR completed: 0
Conversion completed: 0
Failed: 0
```

---

## 19. OCR Parser Conflict Fix

During OCR executor CLI wiring, an argparse error occurred:

```text
ValueError: conflicting subparser: ocr-execute
```

Cause:
- `ocr-execute` had been registered twice in `pipeline_cli.py`

Fix:
- remove the duplicate parser registration
- keep only the version that defines `--languages` and `--no-deskew`

After correction, the OCR queue and execute commands worked.

---

## 20. Current Working Commands

At the end of the current session state, the following commands are working:

```bash
python scripts/pipeline_cli.py scan
python scripts/pipeline_cli.py status
python scripts/pipeline_cli.py lint
python scripts/pipeline_cli.py run
python scripts/pipeline_cli.py detect-one "relative/path/to/file.pdf"
python scripts/pipeline_cli.py convert-one "relative/path/to/file.pdf"
python scripts/pipeline_cli.py convert
python scripts/pipeline_cli.py reconcile
python scripts/pipeline_cli.py ocr-queue
python scripts/pipeline_cli.py ocr-execute
```

---

## 21. Current Verified State

Most recently observed working state:

- `run` successful
- `convert` successful
- `reconcile` successful
- `ocr-queue` successful
- `ocr-execute` successful
- OCRmyPDF installed
- OpenDataLoader working
- Java configured correctly
- repo modularized

Latest clean status snapshot included:
- 424 files
- 0 new
- 0 changed
- 0 missing
- 0 OCR candidates

---

## 22. Current Architectural State

Vitruvius now has:

### Source-of-truth layer
- raw PDFs and other source files

### Manifest and operational layer
- snapshots
- registries
- run reports
- queue reports
- reconcile reports
- OCR reports

### Conversion layer
- OCR PDFs
- raw markdown
- sidecar JSON

### Routing intelligence
- text PDF detection
- OCR-needed routing
- batch queue processing
- one-file processing
- reconciliation of source vs derived state

---

## 23. Immediate Next Concern Identified

The next improvement identified after OCR execution was a **conversion registry**.

Goal:
- record every successful and failed conversion
- record whether OCR was used
- maintain traceability
- support future governance, rebuilds, and provenance

A desired file path was discussed:

```text
006_System-Manifests/registries/latest_conversion_registry.csv
```

At the time of discussion, it was noted that the registry file would not appear until at least one real conversion event appended a row, unless logic was added to pre-create the file with headers.

---

## 24. Suggested Next Steps After This Session

The likely next steps from here are:

1. finalize the conversion registry
2. optionally add a `doctor` command for dependency checks
3. move toward chunking and AI-ready structured persistence
4. build the third-layer ingestion and enrichment pipeline
5. prepare the dataset for local RAG and wiki generation

---

## 25. High-Level Outcome So Far

The project has moved from:
- rough concept
- manual experimentation
- environment problems
- single-file scripts

to a real working local ingestion pipeline with:
- deterministic layered structure
- text-vs-scan routing
- OCR execution
- OpenDataLoader conversion
- manifests and reports
- modular code organization

This is now a serious foundation for Vitruvius.

---
