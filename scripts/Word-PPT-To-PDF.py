#!/usr/bin/env python3
"""
Recursively convert Word and PowerPoint files to PDFs, side by side.

Requirements:
- Windows
- Microsoft Word and PowerPoint installed
- pywin32 installed

Install:
    py -m pip install pywin32

Run:
    py office_to_pdf.py "D:\Your\Root\Folder"
    py office_to_pdf.py "D:\Your\Root\Folder" --overwrite
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pythoncom
import pywintypes
from win32com.client import DispatchEx

# Supported Office file families
WORD_EXTS = {".doc", ".docx", ".docm", ".dot", ".dotx", ".dotm"}
PPT_EXTS = {".ppt", ".pptx", ".pptm", ".pps", ".ppsx", ".ppsm", ".pot", ".potx", ".potm"}

# Word constants
WD_EXPORT_FORMAT_PDF = 17
WD_OPTIMIZE_FOR_PRINT = 0
WD_EXPORT_ALL_DOCUMENT = 0
WD_EXPORT_DOCUMENT_CONTENT = 0
WD_EXPORT_CREATE_HEADING_BOOKMARKS = 1
WD_DO_NOT_SAVE_CHANGES = 0

# PowerPoint constants
PP_SAVE_AS_PDF = 32


@dataclass(slots=True)
class ConversionStats:
    converted: int = 0
    skipped: int = 0
    failed: int = 0


class OfficePDFConverter:
    def __init__(
        self,
        root: Path,
        overwrite: bool = False,
        skip_up_to_date: bool = True,
        retries: int = 2,
        log: logging.Logger | None = None,
    ) -> None:
        self.root = root.resolve()
        self.overwrite = overwrite
        self.skip_up_to_date = skip_up_to_date
        self.retries = max(0, retries)
        self.log = log or logging.getLogger(__name__)
        self.stats = ConversionStats()

        self.word = None
        self.ppt = None
        self._com_initialized = False

    def start(self) -> None:
        pythoncom.CoInitialize()
        self._com_initialized = True

        # Use isolated Office instances so the script does not hijack
        # any document the user already has open.
        self.word = DispatchEx("Word.Application")
        self.word.Visible = False
        self.word.DisplayAlerts = 0

        self.ppt = DispatchEx("PowerPoint.Application")
        try:
            self.ppt.DisplayAlerts = 0
        except Exception:
            pass

    def close(self) -> None:
        self._quit_word()
        self._quit_ppt()

        if self._com_initialized:
            pythoncom.CoUninitialize()
            self._com_initialized = False

    def _quit_word(self) -> None:
        if self.word is not None:
            try:
                self.word.Quit(SaveChanges=WD_DO_NOT_SAVE_CHANGES)
            except Exception:
                try:
                    self.word.Quit()
                except Exception:
                    pass
            finally:
                self.word = None

    def _quit_ppt(self) -> None:
        if self.ppt is not None:
            try:
                self.ppt.Quit()
            except Exception:
                pass
            finally:
                self.ppt = None

    def restart_word(self) -> None:
        self._quit_word()
        time.sleep(0.5)
        self.word = DispatchEx("Word.Application")
        self.word.Visible = False
        self.word.DisplayAlerts = 0

    def restart_ppt(self) -> None:
        self._quit_ppt()
        time.sleep(0.5)
        self.ppt = DispatchEx("PowerPoint.Application")
        try:
            self.ppt.DisplayAlerts = 0
        except Exception:
            pass

    def iter_source_files(self) -> Iterable[Path]:
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            # Skip Office temporary lock files
            if path.name.startswith("~$"):
                continue

            suffix = path.suffix.lower()
            if suffix in WORD_EXTS or suffix in PPT_EXTS:
                yield path

    def _should_skip(self, src: Path, pdf: Path) -> str | None:
        if not pdf.exists():
            return None

        if self.overwrite:
            return None

        if self.skip_up_to_date and pdf.stat().st_mtime >= src.stat().st_mtime:
            return "PDF is already up to date"

        return "PDF already exists"

    def convert_all(self) -> ConversionStats:
        files = sorted(self.iter_source_files(), key=lambda p: str(p).lower())
        self.log.info("Found %s eligible files under %s", len(files), self.root)

        for src in files:
            suffix = src.suffix.lower()
            if suffix in WORD_EXTS:
                self.convert_word(src)
            elif suffix in PPT_EXTS:
                self.convert_ppt(src)

        return self.stats

    def convert_word(self, src: Path) -> None:
        pdf = src.with_suffix(".pdf")
        skip_reason = self._should_skip(src, pdf)

        if skip_reason:
            self.stats.skipped += 1
            self.log.info("SKIP  [WORD] %s  ->  %s  (%s)", src, pdf, skip_reason)
            return

        if self.overwrite and pdf.exists():
            pdf.unlink(missing_ok=True)

        last_error: Exception | None = None

        for attempt in range(1, self.retries + 2):
            doc = None
            try:
                doc = self.word.Documents.Open(
                    FileName=str(src),
                    ConfirmConversions=False,
                    ReadOnly=True,
                    AddToRecentFiles=False,
                    Visible=False,
                    OpenAndRepair=True,
                    Revert=False,
                    NoEncodingDialog=True,
                )

                doc.ExportAsFixedFormat(
                    OutputFileName=str(pdf),
                    ExportFormat=WD_EXPORT_FORMAT_PDF,
                    OpenAfterExport=False,
                    OptimizeFor=WD_OPTIMIZE_FOR_PRINT,
                    Range=WD_EXPORT_ALL_DOCUMENT,
                    Item=WD_EXPORT_DOCUMENT_CONTENT,
                    IncludeDocProps=True,
                    KeepIRM=True,
                    CreateBookmarks=WD_EXPORT_CREATE_HEADING_BOOKMARKS,
                    DocStructureTags=True,
                    BitmapMissingFonts=True,
                    UseISO19005_1=False,
                )

                doc.Close(SaveChanges=WD_DO_NOT_SAVE_CHANGES)
                doc = None

                if not pdf.exists() or pdf.stat().st_size == 0:
                    raise RuntimeError("Word reported success, but the PDF was not created correctly.")

                self.stats.converted += 1
                self.log.info("DONE  [WORD] %s  ->  %s", src, pdf)
                return

            except pywintypes.com_error as exc:
                last_error = exc
                self._safe_close_word_doc(doc)
                self.log.warning(
                    "WARN  [WORD] %s  attempt %s/%s failed with COM error: %s",
                    src,
                    attempt,
                    self.retries + 1,
                    exc,
                )
                self.restart_word()
                if attempt <= self.retries:
                    time.sleep(min(2 ** (attempt - 1), 5))

            except Exception as exc:
                last_error = exc
                self._safe_close_word_doc(doc)
                self.log.warning(
                    "WARN  [WORD] %s  attempt %s/%s failed: %s",
                    src,
                    attempt,
                    self.retries + 1,
                    exc,
                )
                if attempt <= self.retries:
                    time.sleep(min(2 ** (attempt - 1), 5))

        self.stats.failed += 1
        self.log.error("FAIL  [WORD] %s  ->  %s", src, pdf)
        if last_error:
            self.log.exception(last_error)

    def convert_ppt(self, src: Path) -> None:
        pdf = src.with_suffix(".pdf")
        skip_reason = self._should_skip(src, pdf)

        if skip_reason:
            self.stats.skipped += 1
            self.log.info("SKIP  [PPT ] %s  ->  %s  (%s)", src, pdf, skip_reason)
            return

        if self.overwrite and pdf.exists():
            pdf.unlink(missing_ok=True)

        last_error: Exception | None = None

        for attempt in range(1, self.retries + 2):
            pres = None
            try:
                pres = self.ppt.Presentations.Open(
                    FileName=str(src),
                    ReadOnly=True,
                    Untitled=False,
                    WithWindow=False,
                )

                pres.SaveAs(str(pdf), PP_SAVE_AS_PDF)
                pres.Close()
                pres = None

                if not pdf.exists() or pdf.stat().st_size == 0:
                    raise RuntimeError("PowerPoint reported success, but the PDF was not created correctly.")

                self.stats.converted += 1
                self.log.info("DONE  [PPT ] %s  ->  %s", src, pdf)
                return

            except pywintypes.com_error as exc:
                last_error = exc
                self._safe_close_presentation(pres)
                self.log.warning(
                    "WARN  [PPT ] %s  attempt %s/%s failed with COM error: %s",
                    src,
                    attempt,
                    self.retries + 1,
                    exc,
                )
                self.restart_ppt()
                if attempt <= self.retries:
                    time.sleep(min(2 ** (attempt - 1), 5))

            except Exception as exc:
                last_error = exc
                self._safe_close_presentation(pres)
                self.log.warning(
                    "WARN  [PPT ] %s  attempt %s/%s failed: %s",
                    src,
                    attempt,
                    self.retries + 1,
                    exc,
                )
                if attempt <= self.retries:
                    time.sleep(min(2 ** (attempt - 1), 5))

        self.stats.failed += 1
        self.log.error("FAIL  [PPT ] %s  ->  %s", src, pdf)
        if last_error:
            self.log.exception(last_error)

    @staticmethod
    def _safe_close_word_doc(doc) -> None:
        if doc is not None:
            try:
                doc.Close(SaveChanges=WD_DO_NOT_SAVE_CHANGES)
            except Exception:
                pass

    @staticmethod
    def _safe_close_presentation(pres) -> None:
        if pres is not None:
            try:
                pres.Close()
            except Exception:
                pass


def build_logger(log_file: Path | None, verbose: bool) -> logging.Logger:
    logger = logging.getLogger("office_to_pdf")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively convert Word and PowerPoint files to side-by-side PDFs."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root folder to crawl recursively. Defaults to the current folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PDFs.",
    )
    parser.add_argument(
        "--no-skip-up-to-date",
        action="store_true",
        help="Reconvert files even when the PDF is newer than the source.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Number of retries per failed file. Default: 2",
    )
    parser.add_argument(
        "--log-file",
        default="office_to_pdf.log",
        help="Path to the log file. Default: office_to_pdf.log",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug-level logging in the console.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()

    if not root.exists():
        print(f"Root folder does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"Root path is not a directory: {root}", file=sys.stderr)
        return 2

    log_file = Path(args.log_file).expanduser().resolve() if args.log_file else None
    logger = build_logger(log_file, args.verbose)

    logger.info("Starting conversion scan in: %s", root)
    logger.info("Overwrite existing PDFs: %s", args.overwrite)
    logger.info("Skip up-to-date PDFs: %s", not args.no_skip_up_to_date)
    logger.info("Retries per file: %s", args.retries)

    converter = OfficePDFConverter(
        root=root,
        overwrite=args.overwrite,
        skip_up_to_date=not args.no_skip_up_to_date,
        retries=args.retries,
        log=logger,
    )

    try:
        converter.start()
        stats = converter.convert_all()
    except KeyboardInterrupt:
        logger.error("Interrupted by user.")
        return 130
    finally:
        converter.close()

    logger.info(
        "Finished. Converted=%s | Skipped=%s | Failed=%s",
        stats.converted,
        stats.skipped,
        stats.failed,
    )

    return 1 if stats.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())