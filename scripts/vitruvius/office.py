from __future__ import annotations

import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import CONVERSION_LAYER_NAME, RAW_LAYER_NAME
from .paths import build_office_pdf_relative_path, get_repo_root


SUPPORTED_OFFICE_EXTENSIONS = {
    ".docx",
    ".pptx",
    ".doc",
    ".ppt",
}


def is_supported_office_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in SUPPORTED_OFFICE_EXTENSIONS


def get_default_libreoffice_candidates() -> list[Path]:
    candidates = [
        Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
        Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        Path("/usr/bin/libreoffice"),
        Path("/snap/bin/libreoffice"),
        Path("/usr/bin/soffice"),
    ]
    return candidates


def find_soffice_executable() -> str:
    which_result = shutil.which("soffice") or shutil.which("libreoffice")
    if which_result:
        return which_result

    for candidate in get_default_libreoffice_candidates():
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError(
        "LibreOffice executable not found. Install LibreOffice and make sure "
        "soffice is available in PATH, or installed in a standard location."
    )


def convert_office_to_pdf(
    relative_source_path: str,
    *,
    overwrite: bool = True,
) -> dict[str, Any]:
    repo_root = get_repo_root()

    source_path = repo_root / RAW_LAYER_NAME / relative_source_path
    if not source_path.exists():
        raise FileNotFoundError(f"Office source file not found: {source_path}")

    if not is_supported_office_file(source_path):
        raise ValueError(
            f"Unsupported Office file type: {source_path.suffix}. "
            f"Supported types: {sorted(SUPPORTED_OFFICE_EXTENSIONS)}"
        )

    office_pdf_rel = build_office_pdf_relative_path(relative_source_path)
    office_pdf_abs = repo_root / CONVERSION_LAYER_NAME / office_pdf_rel
    office_pdf_abs.parent.mkdir(parents=True, exist_ok=True)

    if office_pdf_abs.exists() and overwrite:
        office_pdf_abs.unlink()

    soffice = find_soffice_executable()

    command = [
        soffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(office_pdf_abs.parent),
        str(source_path),
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            "LibreOffice conversion failed.\n"
            f"Command: {' '.join(command)}\n"
            f"STDOUT: {completed.stdout.strip()}\n"
            f"STDERR: {completed.stderr.strip()}"
        )

    expected_output = office_pdf_abs.parent / f"{source_path.stem}.pdf"

    if not expected_output.exists():
        raise FileNotFoundError(
            f"Expected converted PDF not found after LibreOffice run: {expected_output}"
        )

    if expected_output.resolve() != office_pdf_abs.resolve():
        if office_pdf_abs.exists():
            office_pdf_abs.unlink()
        expected_output.replace(office_pdf_abs)

    stat = source_path.stat()
    top_category = Path(relative_source_path).parts[0] if len(Path(relative_source_path).parts) > 0 else ""

    return {
        "source_relative_path": relative_source_path,
        "source_absolute_path": str(source_path),
        "source_extension": source_path.suffix.lower(),
        "source_size_bytes": stat.st_size,
        "source_modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "top_category": top_category,
        "office_pdf_output": str(office_pdf_abs),
        "office_pdf_output_relative": f"{CONVERSION_LAYER_NAME}/{office_pdf_rel.as_posix()}",
        "status": "converted_to_pdf",
        "converter": "libreoffice",
    }