from __future__ import annotations

from pathlib import PurePosixPath


CONVERSION_REPRESENTATION_PARTS = {
    "raw_markdown",
    "refined_markdown",
    "sidecar_json",
    "ocr_pdf",
}


def logical_source_key_for_relative_path(relative_path: str) -> str:
    """Return a stable source key independent of conversion representation."""

    normalized = str(relative_path).replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    if len(parts) >= 3 and parts[1] in CONVERSION_REPRESENTATION_PARTS:
        subject = parts[0]
        tail = parts[2:]
        if tail:
            tail = (*tail[:-1], PurePosixPath(tail[-1]).stem)
        return PurePosixPath(subject, *tail).as_posix().lower()
    if parts:
        parts = (*parts[:-1], PurePosixPath(parts[-1]).stem)
    return PurePosixPath(*parts).as_posix().lower()
